# Front Office Process

> **Module:** `Reservation` area + `Administration` area (`WebUIMvc/Areas/Reservation`, `WebUIMvc/Areas/Administration`)
> **Scope:** Everything the Front Office (Reception) desk does after a booking exists: guest registration and profile management, room availability checking, room allocation, check‑in, room changes, extend/shorten stay, early/late checkout, no‑show, cancellation, walk‑ins, group bookings (FO view), passport/NIC capture and scanning, guest signature capture, and the flow of data from Front Office into Housekeeping, Cashiering and Reporting.
> All controller/action, service, stored‑procedure (SP), table and screen names below were verified against the source tree and the live `HotelResWeb_Browns` database. Where something could not be confirmed it is marked **"Not found in the project"** (with where we looked).
>
> **Read alongside:** `03-reservation-process.md` (booking life‑cycle and the reservation → check‑in hand‑off) and `04-check-in-check-out-process.md` (the detailed 6‑step check‑in / checkout with SP internals). This document does **not** repeat the check‑in / checkout SP internals — it maps the whole Front Office and defers the step‑by‑step to doc 04.

---

## Purpose

The **Front Office** (FO) is the operational heart of the property once guests start arriving. Where the *reservation* is a promise of a stay, the Front Office turns that promise into a live **in‑house stay**: it seats the guest in a physical room, registers their identity (passport/NIC, signature, registration card), opens the folio, tells Housekeeping the room is now occupied, and — at departure — settles the bill and releases the room.

In Scienter HotelERP the FO is not a single screen but a family of screens spread across the **Reservation** area (arrivals, allocation, quick check‑in, room change, in‑house list, checkout, documents, guest messages) and the **Administration** area (guest profiles, guest information, guest history, room details). They all pivot on one architectural fact established in doc 03: **check‑in physically migrates a record out of `ReservationHeaders`/`ReservationDetails`/`ReservationProfiles` into the `Inhouse*` tables, and checkout migrates it again into the `CheckedOut*` tables.**

---

## Relevant users / departments

| User / department | Involvement in Front Office |
|---|---|
| Front Office / Reception | Arrivals list, room allocation, quick check‑in, key issue, guest registration, room change, checkout. |
| Cashier | Deposit/advance at check‑in, folio, checkout bill settlement (see `05-cashiering-and-finance-process.md`). |
| Housekeeping | Receives room‑status changes on check‑in (Occupied Clean), checkout (Vacant Dirty) and room change; cleans and inspects rooms. |
| Reservations agent | Creates/edits the booking that FO checks in (doc 03); walk‑ins are also created here. |
| Guest Relations / Duty Manager | Guest messages, complaints, VIP handling, registration‑card and document delivery. |
| Night Auditor | Rolls the hotel date, actions No‑Shows, runs day‑end (`DayEndSummary*`). |
| Group / Sales coordinator | Group‑booking room allocation and group check‑in. |

Access to each action is enforced by `[UserWisePageAccess(<pageId>, "<permission>")]` on the controller action. Permissions are single letters: **S**=Select/view, **I**=Insert, **U**=Update, **D**=Delete. Verified FO page ids include `2017` Quick Check‑In, `4030` Quick Check‑Out, `4031`/`5526` Room Change, `16` Guest Profiles, `5201` Guest Information, `7` Guest History, `5540` Guest Message, `13044` Document Upload, `14937` Existing Scanned Documents, `13010` Guest Profile Merge, `6000` GRC list.

---

## Preconditions

Before the Front Office can act on an arrival:

1. **A confirmed reservation exists** — status `Confirmed (3)` with `IsAllowedToCheckIn = 1` (see doc 03). Only Confirmed reservations may be checked in.
2. **A physical room is allocated** — via Room Allocation (below). Check‑in refuses a reservation with no allocated room.
3. **The room is in a check‑in‑able housekeeping status** — `RoomStatus.IsAllowCheckIn = 1` for the room's `CurrentHouseKeepingStatusId`. Verified check‑in‑allowing statuses in `HotelResWeb_Browns`: only **`22 Vacant Inspected`** carries `IsAllowCheckIn = 1` among housekeeping‑category statuses.
4. **The guest profile is complete** — the check‑in SP rejects placeholder values (`TBA`, `-`, default country/nationality/salutation, `TBA@TBA.COM` email). See *Guest registration* below.
5. **The arrival date equals the current hotel date** — `FOSettings.CurrentDate` for the property. Check‑in of a future/past‑dated arrival is refused.
6. **A logged‑in user with the relevant page access**, scoped to `SessionObjects.LoggedUser.PropertyId` (multi‑tenant).

---

## The Front Office screen map

```
                          ┌──────────────────────────── RESERVATION AREA ────────────────────────────┐
 Booking (doc 03)         │                                                                            │
 ReservationHeaders ─────▶│  Room Availability ──▶ Room Allocation ──▶ Quick Check-In ──▶ In-House ────┼──▶ CHECKOUT
 (Confirmed, status 3)    │  (RoomAvailability,   (ReservationsController  (QuickCheckIns   Reservation │    (QuickCheckOut
                          │   AvailabilityChart,   .RoomAllocation /        page 2017)      List        │     page 4030)
                          │   ReservationChart)    SaveQuickRoomAllocation)                 (report)    │
                          │        │                     │                     │                        │
                          │        │                     │                     ├─ Room Change (4031)     │
                          │        │                     │                     ├─ Extend/Change Stay     │
                          │        │                     │                     ├─ Key Request (door lock)│
                          │        │                     │                     ├─ Guest Message (5540)   │
                          │        │                     │                     └─ Document / Scan (13044)│
                          └────────┼─────────────────────┼─────────────────────┼────────────────────────┘
                                   │                     │                     │
                          ┌────────┼─── ADMINISTRATION AREA ──────────────────┼──┐
                          │  Guest Profiles (16) ◀── create/edit/merge guest ◀┘  │
                          │  Guest Information (5201) · Guest History (7)         │
                          │  Room Details (room master, HK/FO status)            │
                          └──────────────────────────────────────────────────────┘

 Downstream on state change (check-in / room change / checkout):
   Housekeeping  ◀── HouseKeeping_ProcessWiseStatusChanges_Update ('CKI'/'CKO'/'RCGO'/'RCGN')
   Cashiering    ◀── Reservation_T_FolioCreation / FolioHeader-FolioDetails / bill settlement (doc 05)
   Reporting     ◀── Dayend_RevenueAndOccupancySummary_Executions_M_Save, DayEndSummary*
   Door locks    ◀── DoorLockEvent_T_Save / DoorLockEvent_T_InsertOrDeleteKeyCode
   PABX / phones ◀── TelMonEvent_T_Save
   OHIP / queue  ◀── RabbitMQ_GuestCheckIn / _GuestCheckOut / _GuestRoomChange
   Channel mgr   ◀── CMUpdateRanges (freed/changed inventory pushed to OTAs)
```

---

## Step-by-step process (the FO functions)

### A. Guest registration & guest profile management

The **guest profile** (`GuestProfiles` table) is the person record: name, salutation, nationality, country, NIC (`IdNum`) and/or passport (`PassportNo`), contacts, image, signature, allergies, preferences and notes. It is shared across all of a guest's stays (history).

**Screen:** `GuestProfilesController` (page `16`) → `Areas/Administration/Views/GuestProfiles/*.cshtml`.

| Function | Controller.Action | Service → SP |
|---|---|---|
| List / search profiles | `GuestProfiles/Grid`, `SelectForGrid` | `GuestProfileService.Select/SelectGrid` → `GuestProfiles_M_Select_ForGrid` |
| Create / update profile | `POST GuestProfiles/Save` | `GuestProfileService.Insert/Update` → **`GuestProfiles_M_Save`**; profile image uploaded via `FileUploadUtility.UploadDocumentByte("GuestProfileImages", …)` |
| Edit / print one profile | `GuestProfiles/Edit`, `Print` | `GuestProfileService.Select(id)` → `GuestProfiles_M_Select_ById` |
| Communication details (phone/email) | `SaveGuestCommunicationDetails`, `SelectGuestCommunicationDetails` | `GuestProfileWiseContactDetailService.save` → `Guest_Communication_Details_M_Save`; read `Guest_Communication_Details_M_Select` |
| Allergies | `SaveGuestAlergies`, `SelectGuestAlergies` | `Guest_Alergies_M_Save` / `Guest_Alergies_M_Select` |
| Preferences | `SaveGuestPreference`, `SelectGuestPreferences` | `Guest_Preferences_M_Save` / `Guest_Preferences_M_Select` |
| Notes | `SaveGuestNotes`, `SelectGuestNoteTypes` | `GuestNotes_M_Save` / `GuestNote_M_Select` |
| **Merge duplicate profiles** | `GuestProfileMerge` (page `13010`), `POST GuestProfileMergeSave` | `GuestProfileService.GuestProfileMergeSave` → `GuestProfileMerge_T_Save` |
| Reservations by guest | `SelectFutureReservationByGuest`, `SelectInHouseAndCheckOutReservationByGuest` | `GuestProfiles_M_SelectReservationsByGuest` |

**NIC vs passport classification.** A guest profile stores **both** `IdNum` (local NIC) and `PassportNo` as separate columns; the save SP `GuestProfiles_M_Save` receives both `@IdNum` and `@PassportNo` (verified in `ReservationHeaderEntry.cs` lines 29–30, 101–102, and `GuestProfileEntry.Save`). During *reservation‑time* inline guest creation the auto‑classifier described in doc 03 (a value containing `v` → local `IdNum`, else `PassportNo`) applies via `GuestProfiles_M_Save_OnReservationCreation`; the standalone Guest Profiles screen instead lets the agent fill the correct field directly.

**Guest information & history (read‑only views for the desk):**

| Screen | Controller (page) | Purpose |
|---|---|---|
| Guest Information | `GuestInformationController` (`5201`) | Look up a guest's in‑house / checked‑out / future / cancelled reservations and complaints by reservation no. |
| Guest History | `GuestHistoryController` (`7`) | Stay history, allergies, notes, extra postings, and CRM summaries (`CRMLoadGuest*`) for a `GuestProfileId`. |

### B. Room availability checking

Availability is checked before allocation/walk‑in. The detailed availability algorithm and SPs are documented in **doc 03 §C** (core SP `RoomAvailability_R_Select @From, @To, @PropertyId`; grids via `RoomAvailabilityController`, `AvailabilityChartController`, `ReservationChartController`). Front Office typically uses the **Reservation Chart** (Gantt of rooms vs. dates) and the **Availability Chart** to find a free room for an arrival or walk‑in. Room change and extend‑stay re‑run the same `RoomAvailability_R_Select` before committing (verified inside `InHouseReservationDetail_T_ChangeRoom`).

### C. Room allocation (assign a physical room)

At booking time a reservation is by **room category + room type + meal plan**; the **physical room number** is assigned at Front Office by *Room Allocation*.

**Screens/actions** (in `ReservationsController` and `ReservationListController`, page `5500`):

| Function | Controller.Action | Service → SP |
|---|---|---|
| Open allocation panel | `Reservations/RoomAllocation` → view `_RoomAllocationMainOutter` | — |
| List rooms to pick from | `Reservations/RoomListForRoomAllocation`, `ReservationList/RoomListForAllocation` | `ReservationHeaderService.SelectRoomsForReservationheaderWiseRoomAllocation` → `Reservation_T_SelectRoomsforReservationRoomAllocation` |
| Save rooms + attributes | `ReservationList/SaveReservationWiseRoomsAndAttributes` | `ReservationHeaderService.InsertReservationWiseRoomsAndAttributes` → **`ReservationHeaders_T_Save_ReservationHeaderWiseRooms`** |
| One‑click assign / unassign | `POST Reservations/SaveQuickRoomAllocation(roomId, reservationHeaderId, operation)` | `ReservationHeaderService.SaveQuickRoomAllocation` |
| Group‑booking allocation | `Reservations/SelectReservationListForRoomAllocation(groupReservationNo)`, `RoomAllocationGroupBookingCombo` | `ReservationHeaderService.SelectReservationRoomAllocationGroupBooking` → `Reservation_T_RoomAllocation_GroupBooking`; save `AllocatedRoomsForGroupReservation_T_Update` |

> Note: the dedicated `RoomAllocationController` in the Reservation area is a thin shell (only `Landing`/`Form` views, no service calls). The real allocation logic lives in `ReservationsController` / `ReservationListController` as above.

### D. Check‑in (arrival → in‑house)

The fastest path is **Quick Check‑In** (`QuickCheckInsController`, page `2017`): the desk selects arrivals from the grid and confirms. This migrates the reservation into the `Inhouse*` tables, generates a **GRC number**, creates the folio, flips room status to Occupied Clean, issues the door‑lock/PABX events and fires the OHIP `RabbitMQ_GuestCheckIn` message.

- **Action:** `POST QuickCheckIns/QuickCheckIn(qCheckIns, CheckInRemark)` → `ReservationHeaderService.QuickCheckIn` → `ReservationHeaderEntry.QuickCheckIn` → SP **`Reservation_T_QuickCheckInUpdate`**.
- **Full 6‑step detail, validations, GRC/folio/housekeeping side‑effects, and error list → see `04-check-in-check-out-process.md`.**

**Key issue (door lock).** After check‑in the desk can encode keys: `Reservations/KeyRequest` → `ReservationHeaderService.KeyRequest` → `RoomDetailsWiseKeyCode_M_Select`; `POST Reservations/KeyRequestSave` → `KeyRequestSave` → **`DoorLockEvent_T_InsertOrDeleteKeyCode`** (machine IP passed through to the door‑lock device).

### E. Room change (move an in‑house guest to another room)

**Screen:** `RoomChangeController` (pages `4031`, `5526`) → `Areas/Reservation/Views/RoomChange/*.cshtml`.

| # | Stage | Detail |
|---|---|---|
| 1 | Select in‑house reservation | `RoomChange/InHouseReservationList` (page `4031`,`5526`) → `RoomChangeService.GetAllInhouseReservations` → SP **`InHouseReservationHeaders_T_Select_ForRoomChange`**. |
| 2 | Pick target room + reason | `RoomChange/InhouseReservationHeaderWiseDateAndRoomDetails` lists available rooms via `InhouseReservation_T_SelectRoomsforReservationRoomChange`; reasons via `RoomChangeReasonSelect` → **`RoomChangeReason_M_Select`** (values: `1 Room Upgrade`, `4 Room Change`, `3 Room Upsale`, `2 Other`). |
| 3 | Submit | `POST RoomChange/SaveRoomChange(ReservationHeaderId, RoomChangedReasonId, changedRoomId, Remark)` → `RoomChangeService.Save` → `RoomChangeEntry.Insert` → SP **`InHouseReservationDetail_T_ChangeRoom`** (`@UserId`, `@PropertyId`). |
| 4 | DB change (in SP) | Validates the target room is free and in an allowed HK status; writes a **`RoomChangeLogs`** row (from/to room, reason, from/to category, hotel date, remark); moves the room on `InHouseReservationDetails`, `FolioHeader`, `FolioDetails(History)` and `ExtraPostingDetails` from the hotel date forward; recomputes `IsAddToOccupancy`. |
| 5 | Downstream | Old room → **`HouseKeeping_ProcessWiseStatusChanges_Update 'RCGO'`** (Vacant / Vacant Dirty); new room → `'RCGN'` (Occupied / Occupied Clean). Inserts `CMUpdateRanges` (push freed dates to OTAs), re‑runs `Dayend_RevenueAndOccupancySummary_Executions_M_Save`, fires `DoorLockEvent_T_Save 'RC'`, `TelMonEvent_T_Save 'RC'` and `RabbitMQ_GuestRoomChange`. |
| 6 | Result | Guest now shows in the new room across FO, folio and housekeeping. |

### F. Extend / shorten stay (change stay), early departure

**Screen:** `ReservationsController.ChangeStay` / `ChangeStaySave` (with availability grid `ChangeStayGrid`, reasons combo `StayChangeReason`).

- **Action:** `POST Reservations/ChangeStaySave(selectedReservations, arrival, departure, roomCategoryId, rateCodeHeaderId, mealPlanId, roomTypeId, companyId, ratecodeHeaderId, stayChangeReasonId, remark)` → `ReservationHeaderService.ChangeStaySave` → `ReservationHeaderEntry.ChangeStaySave` → SP **`Reservation_T_ChangeStaySave`**.
- **Reasons** (`StayChangeReasons`, verified live): `1 Change Stay`, `2 Early Departure With Charge`, `3 Early Departure Without Charge`, `5 Extend Stay / Other`, `6 Guest Request`, `7 System Error`, `8 Agent Request` (plus duplicate‑numbered variants).
- **Behaviour (verified in SP):** mandatory validation of reservation, reason, remark, meal plan, room type, company and rate code; logs to `StayChange_ProcessTimeConsum_Log`; **blocked while day‑end is in progress** (`DayEndDayEndStepCompletion` must be empty); early‑departure reasons (`IsEarlyDeparture = 1`) drive the shorten‑stay path. Extend/shorten adjusts `InHouseReservationDetails` room‑nights and the folio accordingly.

### G. Late checkout / late check‑out charge

There is no separate "late checkout" screen; late checkout is expressed on the reservation via the **`ExpectedDepartureTime`** / `LeaveAfter` fields (carried from `ReservationHeaders` into `InhouseReservationHeaders` at check‑in and passed to the door‑lock/PABX events). Standard checkout still runs through Quick Check‑Out (doc 04). A **parameter‑driven automatic late‑checkout penalty** was **Not found in the project** (searched the checkout SP `Reservation_T_QuickCheckOutUpdate`, `BookingSettings`, and folio SPs — the checkout SP posts no late fee; any late‑checkout charge is posted manually as a folio charge — see doc 05).

### H. Early check‑in

Early check‑in is handled by the **same** Quick Check‑In path; the check‑in SP enforces that `CONVERT(date,@Arrival) = @HotelDate` (arrival must equal the current hotel date), so a genuinely early (future‑dated) arrival cannot be checked in until the hotel date reaches it or the reservation's arrival date is changed. A distinct "early check‑in with fee" endpoint was **Not found in the project** (searched Reservation‑area controller actions and the check‑in SP).

### I. No‑show

As documented in doc 03, **No‑Show is status `2`** (`ReservationStatus.IsNoshow = 1`, `BookingSettings.NoShowStatusId = 2`). It is applied through the status/booking‑settings mechanism, typically at night audit, and — like Cancelled — excludes the booking from occupancy. A dedicated single "mark‑as‑no‑show" FO endpoint was **Not found in the project** (searched `ctrl_actions.json` Reservation area).

### J. Cancellation (from Front Office)

Cancellation is the same `CancelReservationController` flow documented in **doc 03 §H** (SP `CancelReservation_M_Save`, reasons `CancellationReasons`, `CancelledReservationLog`, inventory freed and `CMUpdateRanges` pushed). Front Office uses it to cancel an arriving‑today booking that will not turn up (subject to policy). Note: an already **checked‑in** guest is not "cancelled" — they are checked out (possibly early, see doc 04).

### K. Walk‑in guest process

A walk‑in is a guest arriving **without** a prior reservation. Operationally the Front Office:

1. Creates the booking on the spot — **Make Reservation** with `BookingSourceId = 6 Walk‑in` (verified `BookingSources` value in doc 03), status Confirmed, arrival = today (`ReservationsController.MakeReservation` / `ReservationCreationController.SaveReservationNew` → SP `Reservation_T_Save_New`, doc 03).
2. Creates or picks the guest profile inline (`SaveGuest` → `GuestProfiles_M_Save_OnReservationCreation`).
3. Allocates a room (§C) and checks in (§D).

A single one‑click "walk‑in" super‑action that does all three in one call was **Not found in the project** as a distinct endpoint (searched `ReservationsController`, `ReservationListController`, `QuickCheckInsController`); the walk‑in is the ordinary create → allocate → quick‑check‑in sequence with source = Walk‑in. (An `EventReservations/WalkInReservationPopup` exists but is for **venue/event** walk‑ins, not room stays.)

### L. Group booking (Front Office view)

Groups are created in Reservation (doc 03 §B, shared `GroupReservationNo`). At the desk the FO‑relevant group functions are:

| Function | Controller.Action | Service → SP |
|---|---|---|
| Group room allocation | `Reservations/SelectReservationListForRoomAllocation(groupReservationNo)` | `Reservation_T_RoomAllocation_GroupBooking`, save `AllocatedRoomsForGroupReservation_T_Update` |
| In‑house group detail | `InhouseReservationList/InhouseGroupReservationsDetails` | `InhouseReservationList_T_Select_AdvanceSearch_GroupReservations` |
| Checked‑out group detail | `CheckedOutReservationList/CheckedOutGroupReservationsDetails` | `CheckedOutReservationList_T_Select_AdvanceSearch_GroupReservations` |
| Group check‑in | Quick Check‑In (select all group rooms) | `Reservation_T_QuickCheckInUpdate` (loops per reservation) |

### M. Passport / NIC capture & scanning

Two mechanisms exist:

1. **Document scan / upload** (`DocumentController`, Reservation area; upload popup page `13044`, existing‑scans page `14937`):
   - Load scan panel: `Document/DocumentScan(reservationHeaderId, guestProfileId, documentProcessId)` → view `_DocumentScan`; document types via `DocumentService.SelectDocumentProcessWiseDocument` → `DocumentProcessWiseDocument_M_Select_ByDocProcessId`.
   - Save a scan: `POST Document/SaveScannedDocument` (hard‑codes `DocumentProcessId = 2` = scanned docs) → file bytes uploaded via `FileUploadUtility.UploadDocumentByte(FolderName, DocumentUrl, GUID)` (Azure Blob / local), metadata saved by `DocumentService.SaveReservationDocument` → **`ReservationDocument_M_Save`** (table `ReservationDocument`).
   - Save an uploaded (non‑scan) document: `POST Document/SaveReservationDocument` → same `ReservationDocument_M_Save`.
   - The passport document upload path also has `PassportDocumentDetails_M_Save` (table `UploadedPassportDocumentDetails`).

2. **Dedicated passport‑scan store (`HotelResWeb_PassportScan` DB).** `ReservationHeaderService.SavePassportOnHotelResWeb_PassportScan(guestId)` → `ReservationHeaderEntry` → SP **`ScanedPassport_M_Save`**. In `HotelResWeb_Browns` the `ScanedPassport` table holds only **metadata** (`GuestId`, `PropertyId`, `Uuid`, `UserId`, `CreatedDateTime`) — the actual scan **image** is stored in the separate **`HotelResWeb_PassportScan`** database (per the research pack and confirmed by the thin metadata‑only table here). Retrieval: `RetriveRecordsByUuid` → `ScanedPassport_M_Select`.

### N. Guest signature capture & sync

- **Signature store:** table **`GuestProfileWiseGuestSignature`** (columns `Id, GuestProfileId, GuestSignature, CreatedDateTime`) — the signature is captured against the **guest profile**, so it follows the guest across stays.
- **Code path:** `ReservationHeaderEntry.SaveSignature(reservationNo, signature)` (data layer, line 269) calls SP **`Reservation_T_SaveSignature`** with `@ReservationNo` and `@Signature`.
- **Verification note:** the SP **`Reservation_T_SaveSignature` was Not found in the `HotelResWeb_Browns` database** (queried `sys.objects` — no row). The C# reference exists but the procedure is not deployed to this property DB, so signature save via this path would fail here. The signature *table* exists and is used by the check‑in/checkout/room‑change SPs indirectly (they copy `GuestSignature` fields between header tables). Documented as a discrepancy.

### O. Guest messages

`GuestMessageController` (page `5540`): the desk records a message left for an in‑house guest by room. `POST GuestMessage/Save` → `GuestMessageService.Save` → **`GuestMessage_M_Save`**; grid `GuestMessages_M_Select_ForGrid`; `MarkAsDelivered` → `GuestMessages_M_UpdateIsDelivered`. This tracks physical/desk messages, not a chat channel.

### P. Document delivery (registration card, invoice) to the guest

`DocumentDeliveryController` (root, non‑area) + `DocumentSendService`:
- Document types: `DocumentSendService.GetDocumentTypes` → `HKDocumentTypes_Select` (verified live types include `1 Reservation Confirmation`, `7 Final Invoice`, **`8 GRC`** (Guest Registration Card), proforma invoices, `6 Outstanding Statement`).
- Sending methods: `GetDocumentSendingMethods` → `HK_Select_DocumentSendingMethods` (verified live: **`1 Email`, `2 WhatsApp`**).
- Queue for delivery: `POST DocumentDelivery/SaveDocumentToDeliver` → `DocumentSendService.SaveDocumentToDeliver` → **`HK_Save_DocumentToDeliver`**. WhatsApp/Email dispatch is then handled by the SMS/email/WhatsApp senders (`FrontOffice.SMSSender`, `BEMailSender`).

---

## Data flow from Front Office to other modules

Every FO state change (check‑in, room change, checkout) fans out through the SPs listed above. Consolidated:

| Downstream module | Triggered by | How (SP / table) |
|---|---|---|
| **Housekeeping** | Check‑in, checkout, room change | `HouseKeeping_ProcessWiseStatusChanges_Update` with process code `CKI` (→ Occupied Clean), `CKO` (→ Vacant Dirty), `RCGO`/`RCGN` (room change out/in) → `HouseKeeping_UpdateRoomStatus` updates `RoomDetails.CurrentHouseKeepingStatusId`; also `Admin_T_LinenChange`. |
| **Cashiering / Folio** | Check‑in (open folio), room change (move charges), checkout (settle) | `Reservation_T_FolioCreation`/`_FolioRemoval` at check‑in; `FolioHeader`/`FolioDetails` room reassignment at room change; unsettled‑bill guard + bill settlement at checkout (doc 05). |
| **Reporting / Night audit** | Check‑in, room change, checkout | `Dayend_RevenueAndOccupancySummary_Executions_M_Save`; day‑end/night‑audit consumes `InhouseReservation*`/`CheckedOut*` and `DayEndSummary*`. |
| **Door locks** | Check‑in, room change, checkout, key request | `DoorLockEvent_T_Save` (`CI`/`RC`/`CO`), `DoorLockEvent_T_InsertOrDeleteKeyCode`. |
| **PABX / telephone** | Check‑in, room change, checkout | `TelMonEvent_T_Save` (`CI`/`RC`/`CO`). |
| **OHIP / message queue** | Check‑in, room change, checkout | `RabbitMQ_GuestCheckIn` / `_GuestRoomChange` / `_GuestCheckOut`. |
| **Channel manager (OTA)** | Room change (freed dates), cancellation | `CMUpdateRanges` insert (pushed to Staah/OTAs). |
| **Guest Portal** | Check‑in / checkout (if guest has portal login) | `GuestPortal_A_Login_InStaySendEmail` / `GuestPortal_A_Login_PostStaySendEmail`. |

---

## Screens / modules involved

| Screen / view | Controller.Action (page) | Purpose |
|---|---|---|
| Guest Profiles | `GuestProfilesController` (`16`) | Create/edit/merge guest, contacts, allergies, prefs, notes |
| Guest Information | `GuestInformationController` (`5201`) | Look up a guest's stays and complaints |
| Guest History | `GuestHistoryController` (`7`) | Stay history + CRM summaries |
| `_RoomAllocationMainOutter` | `Reservations.RoomAllocation` (`5500`) | Assign physical room |
| `_Grid` (Quick Check‑In) | `QuickCheckIns` (`2017`) | Arrivals → in‑house |
| Room Change | `RoomChange` (`4031`/`5526`) | Move in‑house guest |
| `_ChangeStay` | `Reservations.ChangeStay` | Extend / shorten stay, early departure |
| `_KeyRequest` | `Reservations.KeyRequest` | Encode door‑lock keys |
| In‑House Reservation List | `InhouseReservationList` | Live in‑house report |
| `_Grid` (Quick Check‑Out) | `QuickCheckOut` (`4030`) | Departures → checked‑out |
| Checked‑Out Reservation List | `CheckedOutReservationList` | Departed report |
| Document / Scan | `Document` (`13044`/`14937`) | Passport/NIC + document upload/scan |
| `_DocumentDelivery` | `DocumentDelivery` | Email/WhatsApp send GRC/invoice |
| Guest Message | `GuestMessage` (`5540`) | Messages for in‑house guests |

## Database / API involvement

**Core FO tables:** `GuestProfiles`, `GuestProfileWiseCommunicationDetails`, `GuestProfileWiseGuestSignature`, `Guest_Alergies`/`Guest_Preferences`/`GuestNote*`, `ReservationHeaders`/`ReservationDetails`/`ReservationProfiles` (pre‑arrival), `InhouseReservationHeaders`/`InHouseReservationDetails`/`InHouseReservationProfiles` (in‑house), `CheckedOutReservationHeaders`/`CheckedOutReservationDetails`/`CheckedOutReservationProfiles` (departed), `RoomDetails`/`RoomStatus`/`HouseKeeping_ProcessWiseStatusChanges`, `RoomChangeLogs`, `StayChange_ProcessTimeConsum_Log` + `*_StayChange_Log`, `FolioHeader`/`FolioDetails`, `ReservationDocument`/`UploadedPassportDocumentDetails`/`ScanedPassport`, `HKDocumentTypes`/`HKDocumentSendingMethods`, `GuestMessages`.

**Key FO SPs:** `GuestProfiles_M_Save`, `GuestProfileMerge_T_Save`, `Reservation_T_SelectRoomsforReservationRoomAllocation`, `ReservationHeaders_T_Save_ReservationHeaderWiseRooms`, `Reservation_T_QuickCheckInUpdate` (check‑in), `InHouseReservationDetail_T_ChangeRoom` (room change), `Reservation_T_ChangeStaySave` (extend/shorten), `Reservation_T_QuickCheckOutUpdate` (checkout), `HouseKeeping_ProcessWiseStatusChanges_Update`, `ReservationDocument_M_Save`, `ScanedPassport_M_Save`, `HK_Save_DocumentToDeliver`, `GuestMessage_M_Save`.

**External integrations:** Azure Blob (document/image storage), door‑lock device (via `DoorLockEvent_*`, machine IP), PABX (`TelMonEvent_*`), OHIP/RabbitMQ, channel manager (`CMUpdateRanges`), Email/WhatsApp senders, `HotelResWeb_PassportScan` DB (passport images).

## Business rules

1. Check‑in requires an **allocated room**, **check‑in‑able housekeeping status** (`RoomStatus.IsAllowCheckIn = 1`), a **complete guest profile** (no `TBA`/`-`/default values), and **arrival = current hotel date**.
2. Check‑in **migrates** the record `Reservation* → Inhouse*`; checkout migrates `Inhouse* → CheckedOut*`. The originating rows are deleted so a reservation lives in exactly one stage.
3. A **GRC number** is generated at check‑in (`UpdateNextDocNoWithUpdate 'GRC'`).
4. Room status is machine‑driven by process code: `CKI`→Occupied Clean, `CKO`→Vacant Dirty, room‑change out/in `RCGO`/`RCGN`.
5. Room change and extend‑stay re‑check availability and **cannot run during day‑end** (extend‑stay guarded by `DayEndDayEndStepCompletion`).
6. Guest identity is stored per profile: **NIC in `IdNum`, passport in `PassportNo`** (separate columns); passport **images** live in `HotelResWeb_PassportScan`.
7. Guest **signature** is captured against the guest profile (`GuestProfileWiseGuestSignature`), shared across stays.
8. Document delivery to the guest is by **Email or WhatsApp** (`HKDocumentSendingMethods`).
9. Everything is scoped to the logged‑in user's `PropertyId` (multi‑tenant).

## Expected result

A guest who arrives with a confirmed booking (or as a walk‑in) is registered (profile complete, passport/NIC captured, signature and registration card produced), seated in a physical room, checked in to the `Inhouse*` tables with a GRC number and an open folio, their room marked Occupied Clean for Housekeeping, keys encoded, and — at departure — checked out with the folio settled and the room released as Vacant Dirty for cleaning.

## Error scenarios

| Trigger | System behaviour |
|---|---|
| Check‑in with no/dirty room or wrong status | `Reservation_T_QuickCheckInUpdate` raises an error (e.g. "not in allowed housekeeping status", "already occupied"). |
| Incomplete guest profile (TBA/`-`/defaults) | Check‑in refused: "Guest profile is not completed…". |
| Arrival not today | "Check in date … is not in current hotel date". |
| Room rate = 0 on chargeable room | "Update the room rates before the check‑in process." |
| Room change to an occupied/blocked room | "Room X already allocated to reservation Y" / "not in allowed housekeeping status". |
| Extend/shorten during day‑end | Blocked (`DayEndDayEndStepCompletion` present). |
| Checkout with unsettled folio | `Reservation_T_QuickCheckOutUpdate` raises `UnsettledBills` (see doc 04). |
| Signature save on a DB without the SP | Fails — `Reservation_T_SaveSignature` **not deployed** in `HotelResWeb_Browns`. |

## Related documents

- `03-reservation-process.md` — booking life‑cycle, availability algorithm, allotments, reservation → check‑in hand‑off.
- `04-check-in-check-out-process.md` — full step‑by‑step check‑in and checkout with SP internals and diagrams.
- `05-cashiering-and-finance-process.md` — folio, deposits/advances, bill settlement, taxes.
- `00-project-overview.md` — architecture and module map.
- `12-database-and-technical-architecture.md` — table/SP conventions, multi‑DB layout.

---

### "Not found in the project" items

- **Automatic late‑checkout / early‑check‑in penalty calculation** — no fee is posted by the check‑in/checkout SPs; charges are manual folio postings. (Searched `Reservation_T_QuickCheckInUpdate`, `Reservation_T_QuickCheckOutUpdate`, `BookingSettings`.)
- **A single one‑click walk‑in endpoint** — walk‑in is the ordinary create → allocate → quick‑check‑in sequence with `BookingSourceId = Walk‑in`. (Searched `ReservationsController`, `ReservationListController`, `QuickCheckInsController`.)
- **A dedicated mark‑as‑No‑Show FO endpoint** — applied via `BookingSettings.NoShowStatusId`/status master (see doc 03). (Searched Reservation‑area `ctrl_actions.json`.)
- **`Reservation_T_SaveSignature` stored procedure** — referenced in `ReservationHeaderEntry.cs` but **not present** in `HotelResWeb_Browns`. (Queried `sys.objects`.)
