# Check‑In / Check‑Out Process

> **Module:** `Reservation` area (`WebUIMvc/Areas/Reservation`)
> **Scope:** The two pivotal Front Office transactions — **check‑in** (arrival → in‑house) and **check‑out** (departure → checked‑out) — plus early checkout and late checkout, at full technical depth: required guest info, room assignment, deposit/payment handling, registration card (GRC), guest signature, outstanding‑balance check, invoice/bill settlement, room‑status update to dirty, and housekeeping notification.
> Every controller/action, service, stored‑procedure (SP), table and column below was verified against the source tree and the live `HotelResWeb_Browns` database (SP bodies were read with `OBJECT_DEFINITION`). Where something could not be confirmed it is marked **"Not found in the project"** (with where we looked).
>
> **Read alongside:** `02-front-office-process.md` (the whole FO screen map and guest‑registration/room‑allocation detail) and `03-reservation-process.md` (the reservation → check‑in hand‑off). This document is the authoritative source for the check‑in and checkout **SP internals**.

---

## Purpose

**Check‑in** converts a confirmed reservation into a live **in‑house stay**. Technically it *migrates* the record out of `ReservationHeaders/ReservationDetails/ReservationProfiles` into `InhouseReservationHeaders/InHouseReservationDetails/InHouseReservationProfiles`, stamps `CheckedInDate = GETDATE()`, generates a **Guest Registration Card (GRC) number**, creates the folio, flips the room to **Occupied / Occupied Clean** for Housekeeping, and fires door‑lock, PABX and OHIP events.

**Check‑out** ends the stay. It first **blocks if the folio is unsettled**, then migrates the record from the `Inhouse*` tables into `CheckedOutReservationHeaders/Details/Profiles`, stamps `CheckedOutDate = FOSettings.CurrentDate`, flips the room to **Vacant / Vacant Dirty** (so Housekeeping cleans it), removes the door‑lock key, and fires the OHIP checkout event.

Both are deliberately **all‑or‑nothing per reservation** (each iteration is wrapped in `BEGIN TRANSACTION … COMMIT`, with a `BEGIN CATCH` that rolls back and logs to `GEN_ErrTable`).

---

## Relevant users / departments

| User / department | Involvement |
|---|---|
| Front Office / Reception | Runs quick check‑in and quick check‑out; issues keys; prints GRC. |
| Cashier | Takes deposit/advance at check‑in; settles the folio/invoice at checkout (doc 05). |
| Housekeeping | Receives Occupied Clean (check‑in) / Vacant Dirty (checkout) status and cleans the room. |
| Guest | Provides identity (passport/NIC), signs the registration card. |
| Night Auditor | Handles early/late checkout dating and day‑end. |

**Access control:** `[UserWisePageAccess(2017, "I")]` = perform Quick Check‑In; `[UserWisePageAccess(4030, "I", 5570)]` = perform Quick Check‑Out (the extra `5570` is a secondary page‑access requirement).

---

## Preconditions

**For check‑in** (all enforced inside `Reservation_T_QuickCheckInUpdate`):
1. Reservation status allows check‑in — `ReservationStatus.IsAllowedToCheckIn = 1` (only **Confirmed = 3**).
2. A physical room is allocated (via Room Allocation — doc 02 §C).
3. The room's housekeeping status allows check‑in — `RoomStatus.IsAllowCheckIn = 1` (verified: only **`22 Vacant Inspected`** qualifies).
4. The room is **not already occupied** by another live in‑house reservation.
5. The room rate is **not zero** on a chargeable, occupancy‑bearing room (`IsComplimentary = 0` and `ConciderForOccupancy = 1`).
6. The **guest profile is complete** — no `TBA`, `-`, default nationality (`1025`), default country (`1`/`258`), default salutation (`6`), or placeholder email (`-`, `tba`, `TBA@TBA.COM`).
7. **Arrival date = current hotel date** (`FOSettings.CurrentDate` for the property).

**For check‑out** (enforced inside `Reservation_T_QuickCheckOutUpdate`):
1. **No open folio** — `FolioHeader` must have no row for the reservation, else `RAISERROR('UnsettledBills')`.
2. No unsettled restaurant/POS bill when `SystemSettings SS003` is enabled (checked in the controller before calling the SP).
3. Room‑night vs. folio‑night consistency (accommodation charge `ChargeCodeID = 6` count ≥ room‑night count) for actual rooms.
4. Checkout date consistency with the hotel date.

---

## Check‑in — step‑by‑step (6‑step format)

**Screen:** `QuickCheckInsController` (page `2017`) → `Areas/Reservation/Views/QuickCheckIns/_Grid.cshtml`.
**SP:** `Reservation_T_QuickCheckInUpdate(@qCheckIns NVARCHAR(MAX), @CheckInRemark NVARCHAR(50), @UserId INT, @PropertyId INT)`.

| # | Stage | What happens (verified) |
|---|---|---|
| **1** | **User action** | The desk opens **Quick Check‑In**, sees today's arrivals (`QuickCheckIns/SelectForGrid` → `ReservationHeaderService.ReservationQuickCheckInListSelect` → SP `Reservation_T_QuickCheckin_Select`), ticks the arriving reservation(s), optionally types a **check‑in remark**, and confirms. Front end posts `POST QuickCheckIns/QuickCheckIn(qCheckIns, CheckInRemark)`. |
| **2** | **System validation** | `ReservationHeaderService.QuickCheckIn` serialises the selection to JSON and calls the SP. The SP loads all currently active in‑house rooms (`InhouseReservationHeaders_Active_Rooms`) and, per selected reservation, validates (in order): room rate ≠ 0 on chargeable rooms → *"Update the room rates before the check‑in process."*; room not already in‑house → *"…is already in occupied."*; housekeeping status `IsAllowCheckIn = 1` → *"…not in allowed housekeeping status to checkin."*; `IsAllowedToCheckIn = 1` → *"Reservation is not ready to be checked‑in…"*; guest profile complete (no TBA/`-`/defaults) → *"Guest profile is not completed…"*; arrival = hotel date → *"…not in current hotel date"*. Dummy/non‑occupancy rooms (`ConciderForOccupancy = 0`) skip the rate and HK‑status checks. |
| **3** | **Database change (migrate + number + folio)** | Inside a per‑reservation transaction the SP: generates the **GRC number** via `EXEC UpdateNextDocNoWithUpdate 'GRC', @PropertyId, @GRCNo OUTPUT`; runs `Reservation_T_FolioRemoval` then `Reservation_T_FolioCreation` to (re)build the folio; runs `Admin_SchedulePosting_To_ExtraPosting_On_Chekin`; **inserts into `InhouseReservationHeaders`** copying every column from `ReservationHeaders` but setting `CheckedInDate = GETDATE()`, `CheckedInUserId = @UserId`, `GRCNo = @GRCNo`, `CheckInRemark = @CheckInRemark`, `ArrivalTxnDateTime = GETDATE()`; inserts `InHouseReservationDetails` and `InHouseReservationProfiles` from their reservation counterparts. It also validates `RoomCategoryId`/`MealPlanId` ≠ 0 → *"Update room category and meal plan."* |
| **4** | **Related module update (housekeeping + occupancy)** | `EXEC HouseKeeping_ProcessWiseStatusChanges_Update 'CKI', @checkInRoomId, @UserId, @PropertyId` sets the room's **FO status → `2050 Occupied`** and **housekeeping status → `2030 Occupied Clean`** (via `HouseKeeping_UpdateRoomStatus`, with `Admin_T_LinenChange`). If the room still appears in the in‑house list for another reservation it aborts: *"Room still appearing in the inhouse level for another reservation…"*. Occupancy/revenue is recomputed by `Dayend_RevenueAndOccupancySummary_Executions_M_Save`. |
| **5** | **Notification / integration** | Door lock: `DoorLockEvent_T_Save 'CI', …` (room, guest, arrival/departure, tel, email). PABX: `TelMonEvent_T_Save 'CI', …`. OHIP / message queue: `RabbitMQ_GuestCheckIn`. Guest Portal (if the reservation has a portal login): `GuestPortal_A_Login_InStaySendEmail`. Audit: `HotelResWeb_AuditTail_WriteToLog 'InhouseReservationHeaders' … 'CKINRHI','I'` (+ before‑change snapshots and `InHouseReservationDetails_History`). |
| **6** | **Final result** | The **originating reservation rows are deleted** (`DELETE FROM ReservationHeaders/ReservationDetails/ReservationProfiles WHERE …`) and the filtration cache row removed. Controller returns `Json("success")` (or `"ERR-<message>"`). The guest now appears on the **In‑House Reservation List**, the room is Occupied Clean, the folio is open, and the GRC can be printed/sent. |

### Required guest information (check‑in gate)

The check‑in SP will **refuse** the check‑in unless the main guest (`GuestProfileTypeId = 1`) profile is real:

| Field | Rejected placeholder values |
|---|---|
| First / Middle / Last name | `TBA`, `-` |
| Nationality | `1025` (default), `0` |
| Country | `1`, `258` (defaults), `0` |
| Salutation | `6` (default) |
| Email (`CommunicationTypeId = 2`) | `-`, `tba`, `TBA@TBA.COM` |

So the Front Office must complete the guest profile (name, nationality, country, salutation, contact email) **before** check‑in — this is where passport/NIC capture (`ScanedPassport_M_Save` / `ReservationDocument_M_Save`) and the guest signature (`GuestProfileWiseGuestSignature`) are collected (see doc 02 §M–N).

### Room assignment

The physical room must already be allocated (doc 02 §C, `ReservationHeaders_T_Save_ReservationHeaderWiseRooms` / `SaveQuickRoomAllocation`). At check‑in the SP reads the allocated room from `ReservationDetails.RoomId` and drives all room‑level side‑effects (occupancy check, HK status, door lock) off it.

### Deposit / payment handling at check‑in

Deposits (advances) are **not** posted by the check‑in SP itself. They are taken through the folio/advance mechanism documented in `03-reservation-process.md §E` and `05-cashiering-and-finance-process.md`:
- In‑house advance: `AdvancePaymentService.Save` → `Advance_Payment_T_Save` (posts a credit `DRCR='C'` to the folio using `BookingSettings.ChargeCodeAdvancedPayments`).
- Online advance link: Sampath IPG (`Advance/Payment` → `SampathIPGController`).

`Reservation_T_QuickCheckInUpdate` opens the folio (`Reservation_T_FolioCreation`) so that any advance already taken, and all future room/extra postings, attach to the in‑house stay.

### Registration card (GRC) & guest signature

- **GRC number:** issued at check‑in by `UpdateNextDocNoWithUpdate 'GRC'` and stored on `InhouseReservationHeaders.GRCNo`.
- **GRC print list:** `ReservationsController.GRCReservationList` (page `6000`) → `ReservationHeaderService.SelectGRCReservationList` → SP `ReservationListForGRC_T_Select`; the registration document itself is `Report_Guest_Registration` (SSRS report, verified present).
- **GRC delivery:** as document type `8 GRC` via `DocumentDelivery` → `HK_Save_DocumentToDeliver` (Email/WhatsApp, doc 02 §P).
- **Signature:** captured against the guest profile in `GuestProfileWiseGuestSignature`. *Caveat:* the code‑referenced SP `Reservation_T_SaveSignature` is **Not found in `HotelResWeb_Browns`** (queried `sys.objects`); the signature *table* exists and header tables carry `GuestSignature` columns copied during check‑in.

### Check‑in flow diagram

```
 QUICK CHECK-IN  (QuickCheckIns.QuickCheckIn → Reservation_T_QuickCheckInUpdate)

  Arrivals grid (today)                 per selected reservation
  Reservation_T_QuickCheckin_Select
          │
          ▼
   ┌─────────────────────── VALIDATE (RAISERROR on fail) ───────────────────────┐
   │ rate≠0 · room not occupied · HK status IsAllowCheckIn=1 · status can check  │
   │ in · guest profile complete (no TBA/-/defaults) · arrival = hotel date      │
   └────────────────────────────────────┬───────────────────────────────────────┘
                                         ▼
        EXEC UpdateNextDocNoWithUpdate 'GRC'  ──▶  @GRCNo
        Reservation_T_FolioRemoval → Reservation_T_FolioCreation  (open folio)
        Admin_SchedulePosting_To_ExtraPosting_On_Chekin
                                         │
                                         ▼
   ReservationHeaders ─┐  INSERT (CheckedInDate=GETDATE, GRCNo, CheckInRemark)
   ReservationDetails  ├────────────────────────────▶  InhouseReservationHeaders
   ReservationProfiles ┘                                InHouseReservationDetails
                                         │              InHouseReservationProfiles
                                         ▼
        HouseKeeping_ProcessWiseStatusChanges_Update 'CKI'
             → room FO=2050 Occupied · HK=2030 Occupied Clean
        DoorLockEvent_T_Save 'CI' · TelMonEvent_T_Save 'CI'
        RabbitMQ_GuestCheckIn · (GuestPortal in-stay email)
        Dayend_RevenueAndOccupancySummary_Executions_M_Save · audit trail
                                         │
                                         ▼
        DELETE Reservation* rows   ──▶   guest is now IN-HOUSE
```

---

## Check‑out — step‑by‑step (6‑step format)

**Screen:** `QuickCheckOutController` (page `4030`) → `Areas/Reservation/Views/QuickCheckOut/_Grid.cshtml`.
**SP:** `Reservation_T_QuickCheckOutUpdate(@qCheckOut NVARCHAR(MAX), @CheckOutRemark NVARCHAR(50), @UserId INT, @PropertyId INT)`.

| # | Stage | What happens (verified) |
|---|---|---|
| **1** | **User action** | The desk opens **Quick Check‑Out**, sees departures (`QuickCheckOut/SelectForGrid` → `ReservationHeaderService.SelectGridCheckOut` → SP `Reservation_T_QuickCheckOutSelect`), ticks the departing reservation(s), and confirms. Front end posts `POST QuickCheckOut/QuickCheckOut(qCheckOut, CheckOutRemark)`. |
| **2** | **System validation (controller pre‑check: POS bills)** | If `SystemSettings SS003` (restaurant/POS integration) is enabled, the controller calls `ValidateRestaurantBillStatus(ReservationNo)` (intended SP `Reservations_W_ValidatePOSBill_AtCheckout`) for each reservation and **refuses** checkout listing any reservation with unsettled restaurant bills: *"There are unsettled restaurant bills for …"*. *(Note: the referenced SP is not deployed in `HotelResWeb_Browns` — see "Not found" below; when SS003 is off this check is skipped.)* |
| **3** | **System validation (SP: outstanding balance)** | `Reservation_T_QuickCheckOutUpdate` first checks **`IF EXISTS(SELECT 1 FROM FolioHeader WHERE ReservationHeaderID IN (@Temp))`** → `RAISERROR('UnsettledBills', 16, 1)`. An open folio header means the bill has not been settled/closed, so **checkout is blocked until the folio is fully settled** (settlement moves charges to `FolioDetailsHistory` / bill tables — see doc 05). It then checks room‑night vs. accommodation‑folio‑night counts (`ChargeCodeID = 6`) and raises *"There is a mismatch between room nights and folio nights…"* if folio nights are short (actual rooms only). |
| **4** | **Database change (migrate + date)** | Per reservation, inside a transaction, the SP **inserts into `CheckedOutReservationHeaders`** copying from `InhouseReservationHeaders` but setting `CheckedOutDate = FOSettings.CurrentDate`, `CheckedOutUserId = @UserId`, `CheckOutRemark = @CheckOutRemark`, `CheckOutTxnDateTime = GETDATE()`; inserts `CheckedOutReservationDetails` and `CheckedOutReservationProfiles`. Checkout‑date must equal the hotel date (actual rooms) → *"Check out date of room X is not in current hotel date"*. |
| **5** | **Related module update (housekeeping) + notification** | `EXEC HouseKeeping_ProcessWiseStatusChanges_Update 'CKO', @RoomId, @UserId, @PropertyId` sets the room's **FO status → `2061 Vacant`** and **housekeeping status → `2034 Vacant Dirty`** — this is the **housekeeping notification** that the room needs cleaning. Occupancy/revenue recomputed via `Dayend_RevenueAndOccupancySummary_Executions_M_Save`. Door lock cleared: `DoorLockEvent_T_Save 'CO'` **and** `DoorLockEvent_T_InsertOrDeleteKeyCode(@…, 'C', …)` (removes key codes). PABX: `TelMonEvent_T_Save 'CO'`. OHIP: `RabbitMQ_GuestCheckOut`. Guest Portal post‑stay email if a portal login exists. Audit: `HotelResWeb_AuditTail_WriteToLog … 'CKOTRHA','I'`. |
| **6** | **Final result** | The **in‑house rows are deleted** (`DELETE FROM InhouseReservationHeaders/InHouseReservationDetails/InHouseReservationProfiles`). Controller returns `Json("success")` (or the error message). The guest moves to the **Checked‑Out Reservation List**, the room is **Vacant Dirty** for Housekeeping, and the door key is revoked. |

### Outstanding balance / invoice / bill settlement

The checkout SP does **not** generate or settle the invoice itself — it is a **hard gate**: the presence of any `FolioHeader` row for the reservation means the bill is still open, and checkout is refused with `UnsettledBills`. The cashier must therefore **settle the folio first** (generate the final invoice, take payment, close/settle the folio) using the Cashiering module. The settled‑bill data that the checked‑out reservation later reads is `InvoiceDetails_M_SelectForCheckedOutReservations` (`ReservationHeaderService.SelectBillSettlementDetails`). See **`05-cashiering-and-finance-process.md`** for `BillHeader`/`BillTrans`/`BillSettlementDetails`, tax and invoice numbering.

### Room status update to dirty & housekeeping notification

This is the concrete mechanism (verified in `HouseKeeping_ProcessWiseStatusChanges_Update` + `HouseKeeping_ProcessWiseStatusChanges` mapping):

| Process code | Trigger | FO status set | Housekeeping status set |
|---|---|---|---|
| `CKI` | Check‑in | `2050 Occupied` | `2030 Occupied Clean` |
| `CKO` | Check‑out | `2061 Vacant` | **`2034 Vacant Dirty`** |
| `RCGO` | Room change — old room | `2061 Vacant` | `2034 Vacant Dirty` |
| `RCGN` | Room change — new room | `2050 Occupied` | `2030 Occupied Clean` |

The status write goes through `HouseKeeping_UpdateRoomStatus` (updating `RoomDetails.CurrentHouseKeepingStatusId` and the FO status) and `Admin_T_LinenChange`. Housekeeping's screens/API then pick up the **Vacant Dirty** room to clean and inspect (an inspected room becomes `22 Vacant Inspected`, the only status that re‑allows check‑in).

### Check‑out flow diagram

```
 QUICK CHECK-OUT  (QuickCheckOut.QuickCheckOut → Reservation_T_QuickCheckOutUpdate)

  Departures grid                        controller pre-check (if SS003 on):
  Reservation_T_QuickCheckOutSelect      ValidateRestaurantBillStatus → block if POS bills open
          │
          ▼
   ┌──────────────── SP VALIDATE (RAISERROR on fail) ────────────────┐
   │ FolioHeader exists for reservation?  → 'UnsettledBills'  (STOP)  │
   │ folio-nights (ChargeCodeID=6) ≥ room-nights?                     │
   │ checkout date = hotel date (actual rooms)?                       │
   └───────────────────────────────┬─────────────────────────────────┘
                                    ▼   (folio already settled by cashier)
   InhouseReservationHeaders ─┐  INSERT (CheckedOutDate=CurrentDate, remark, user)
   InHouseReservationDetails  ├──────────────────▶  CheckedOutReservationHeaders
   InHouseReservationProfiles ┘                     CheckedOutReservationDetails
                                    │                CheckedOutReservationProfiles
                                    ▼
        HouseKeeping_ProcessWiseStatusChanges_Update 'CKO'
             → room FO=2061 Vacant · HK=2034 Vacant Dirty  ⟶ HOUSEKEEPING cleans
        DoorLockEvent_T_Save 'CO' + DoorLockEvent_T_InsertOrDeleteKeyCode 'C'  (revoke key)
        TelMonEvent_T_Save 'CO' · RabbitMQ_GuestCheckOut · (GuestPortal post-stay email)
        Dayend_RevenueAndOccupancySummary_Executions_M_Save · audit trail
                                    │
                                    ▼
        DELETE Inhouse* rows   ──▶   guest is now CHECKED-OUT
```

---

## Early checkout

Handled by the **same** `Reservation_T_QuickCheckOutUpdate` SP. When the property's `FOSettings.CurrentDate` differs from the real calendar date (i.e. the guest is leaving *before* the recorded departure while the system runs on the hotel/audit date), the SP automatically stamps the remark:

```
ELSE IF (SELECT CONVERT(date, CurrentDate) FROM FOSettings WHERE PropertyId=@PropertyId) <> CONVERT(date, GETDATE())
    SET @CheckOutRemark = 'Early checkout: confirmed'
```

For a **shorten‑stay / early departure with rate implications**, the desk uses **Change Stay** first (doc 02 §F, SP `Reservation_T_ChangeStaySave`) — its `StayChangeReasons` include `2 Early Departure With Charge` and `3 Early Departure Without Charge` — to adjust the room‑nights and folio, then checks out normally. There is no separate "early checkout" controller; it is the ordinary quick checkout, optionally preceded by a change‑stay adjustment. The `UnsettledBills` gate still applies, so the shortened bill must be settled first.

## Late checkout

There is no distinct late‑checkout transaction. Late departure is represented on the stay via `ExpectedDepartureTime` / `LeaveAfter` (carried into `InhouseReservationHeaders` at check‑in and passed to the door‑lock/PABX events). Checkout still runs through Quick Check‑Out on the departure hotel date. An **automatic late‑checkout fee** is **Not found in the project** — `Reservation_T_QuickCheckOutUpdate` posts no charge; any late‑checkout fee is a manual folio posting (doc 05). (Searched the checkout SP and `BookingSettings`.)

---

## Screens / modules involved

| Screen / view | Controller.Action (page) | Purpose |
|---|---|---|
| Quick Check‑In `_Grid` | `QuickCheckIns.SelectForGrid` / `QuickCheckIn` (`2017`) | Select arrivals, check in |
| Quick Check‑Out `_Grid` | `QuickCheckOut.SelectForGrid` / `QuickCheckOut` (`4030`) | Select departures, check out |
| In‑House Reservation List | `InhouseReservationList.List` | Live in‑house guests |
| Checked‑Out Reservation List | `CheckedOutReservationList.List` | Departed guests + bill settlement details |
| GRC list / `ReservationListForGRC` | `Reservations.GRCReservationList` (`6000`) | Registration cards |
| Document / Scan | `Document` (`13044`/`14937`) | Passport/NIC + signature/docs (pre‑check‑in) |
| Key Request `_KeyRequest` | `Reservations.KeyRequest` | Encode/revoke door keys |

## Database / API involvement

**Tables:**
- Pre‑arrival: `ReservationHeaders`, `ReservationDetails`, `ReservationProfiles`.
- In‑house: **`InhouseReservationHeaders`**, **`InHouseReservationDetails`**, **`InHouseReservationProfiles`**.
- Departed: **`CheckedOutReservationHeaders`**, **`CheckedOutReservationDetails`**, **`CheckedOutReservationProfiles`**.
- Rooms/status: `RoomDetails`, `RoomStatus`, `HouseKeeping_ProcessWiseStatusChanges`.
- Folio/bill: `FolioHeader`, `FolioDetails`, `FolioDetailsHistory`, `FolioHeaderHistory`, `ExtraPostingDetails` (settlement: `BillHeader`/`BillTrans`/`BillSettlementDetails` — doc 05).
- Numbering/settings: `DocumentNumbers` (`Code='GRC'`), `FOSettings` (`CurrentDate`), `BookingSettings` (`AccomadationChargeCodeId`).
- Audit/error: `HotelResWeb_AuditTail..InHouseReservationDetails_History`, `GEN_ErrTable`.

**SPs (verified):**
- Check‑in: **`Reservation_T_QuickCheckInUpdate`**, `Reservation_T_QuickCheckin_Select`, `InhouseReservationHeaders_Active_Rooms`, `Reservation_T_FolioCreation`/`_FolioRemoval`, `Admin_SchedulePosting_To_ExtraPosting_On_Chekin`, `UpdateNextDocNoWithUpdate`.
- Check‑out: **`Reservation_T_QuickCheckOutUpdate`**, `Reservation_T_QuickCheckOutSelect`, `InvoiceDetails_M_SelectForCheckedOutReservations`.
- Shared side‑effects: `HouseKeeping_ProcessWiseStatusChanges_Update` → `HouseKeeping_UpdateRoomStatus` + `Admin_T_LinenChange`; `Dayend_RevenueAndOccupancySummary_Executions_M_Save`; `DoorLockEvent_T_Save`, `DoorLockEvent_T_InsertOrDeleteKeyCode`; `TelMonEvent_T_Save`; `RabbitMQ_GuestCheckIn`/`_GuestCheckOut`; `GuestPortal_A_Login_InStaySendEmail`/`_PostStaySendEmail`; `HotelResWeb_AuditTail_WriteToLog`.
- Reinstate (undo): `InHouseReservationList_M_Reinstate` (undo checkout back to in‑house — `ReinstateInHouseReservations`), `CheckOutReservationList_M_Reinstate` (`ReinstateCheckOutReservations`).

**External integrations:** door‑lock device (machine IP), PABX (`TelMonEvent`), OHIP via RabbitMQ, Guest Portal email, Azure Blob (docs/signature), `HotelResWeb_PassportScan` DB.

## Business rules

1. **Check‑in gate:** allocated room + `RoomStatus.IsAllowCheckIn = 1` + status Confirmed + complete guest profile + arrival = hotel date + non‑zero rate on chargeable rooms.
2. **Migration is one‑way per stage:** `Reservation* → Inhouse*` on check‑in (source deleted); `Inhouse* → CheckedOut*` on checkout (source deleted). A stay lives in exactly one set of tables.
3. **GRC number** generated at check‑in (`UpdateNextDocNoWithUpdate 'GRC'`), stored on `InhouseReservationHeaders.GRCNo`.
4. **Room status is automatic:** check‑in → Occupied Clean; checkout → Vacant Dirty; room‑change out/in → Vacant Dirty / Occupied Clean.
5. **Checkout is blocked by an open folio** (`UnsettledBills`) and by unsettled POS bills (when `SS003` on). Settle first.
6. **Room‑night ↔ folio‑night** must reconcile (accommodation `ChargeCodeID = 6`) for actual rooms.
7. **Door key is issued** conceptually at check‑in (via Key Request) and **revoked at checkout** (`DoorLockEvent_T_InsertOrDeleteKeyCode 'C'`).
8. **Early checkout** auto‑stamps *"Early checkout: confirmed"* when the hotel date ≠ calendar date; **no automatic early/late fee** is posted.
9. Everything is transactional and scoped to `PropertyId`; failures roll back and log to `GEN_ErrTable`.

## Expected result

**After check‑in:** the reservation is an in‑house stay with a GRC number, an open folio, the room Occupied Clean, keys encoded, and OHIP/PABX/door‑lock notified — visible on the In‑House Reservation List.
**After checkout:** the stay is on the Checked‑Out Reservation List with `CheckedOutDate`, the folio settled, the room Vacant Dirty (queued for Housekeeping), and the door key revoked.

## Error scenarios

| Trigger | System behaviour |
|---|---|
| Zero rate on chargeable room | Check‑in refused: *"Update the room rates before the check‑in process."* |
| Room already occupied / still in in‑house list | *"…is already in occupied."* / *"Room still appearing in the inhouse level…"* |
| Room HK status not check‑in‑able | *"…not in allowed housekeeping status to checkin."* |
| Reservation status not check‑in‑able | *"Reservation is not ready to be checked‑in…"* |
| Incomplete guest profile | *"Guest profile is not completed, please update TBA/‑ values."* |
| Arrival ≠ hotel date | *"Check in date … is not in current hotel date"* |
| Missing category/meal plan | *"Update room category and meal plan."* |
| Checkout with open folio | `RAISERROR('UnsettledBills')` — checkout refused. |
| Unsettled POS/restaurant bill (SS003 on) | Controller returns *"There are unsettled restaurant bills for …"* |
| Room‑night/folio‑night mismatch | *"There is a mismatch between room nights and folio nights…"* |
| Checkout date ≠ hotel date (actual room) | *"Check out date of room … is not in current hotel date"* |
| Any SQL error | Rolled back; logged to `GEN_ErrTable`; message surfaced to the desk. |

## Related documents

- `02-front-office-process.md` — full FO screen map, guest registration, room allocation, room change, extend stay, passport/NIC, signature, document delivery.
- `03-reservation-process.md` — booking life‑cycle and the reservation → check‑in hand‑off.
- `05-cashiering-and-finance-process.md` — folio, advances/deposits, invoice generation and bill settlement (the checkout `UnsettledBills` gate).
- `12-database-and-technical-architecture.md` — table/SP conventions and multi‑DB layout.

---

### "Not found in the project" items

- **`Reservations_W_ValidatePOSBill_AtCheckout` stored procedure** — referenced by `ValidateRestaurantBillStatus` in code but **not deployed** in `HotelResWeb_Browns` (queried `sys.objects`; `OBJECT_DEFINITION` returned NULL). The POS‑bill pre‑check only runs when `SystemSettings SS003` is enabled.
- **`Reservation_T_SaveSignature` stored procedure** — referenced in `ReservationHeaderEntry.cs` but **not present** in `HotelResWeb_Browns`. Signature table (`GuestProfileWiseGuestSignature`) exists. (Queried `sys.objects`.)
- **Automatic early‑check‑in / late‑checkout fee** — none posted by the check‑in/checkout SPs; fees are manual folio postings. (Searched `Reservation_T_QuickCheckInUpdate`, `Reservation_T_QuickCheckOutUpdate`, `BookingSettings`.)
