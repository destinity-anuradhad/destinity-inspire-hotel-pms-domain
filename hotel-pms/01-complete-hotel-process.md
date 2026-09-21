# 01 — Complete Hotel Process (End-to-End Guest Lifecycle)

> Scienter HotelERP — Destinity Inspire / Destinity Horizon Front Office (Hotel PMS).
> **This is a synthesis document.** It stitches the already-written module docs into one end-to-end narrative of a guest's entire journey — from the first enquiry to post-stay. Every controller/action, service, stored procedure (SP), table and status value below is **carried over verbatim from the verified module docs**; nothing new is invented. Where a capability is absent or only partly present it is marked **"Not found in the project."**
>
> **Read the deep-dives for full internals:** `03-reservation-process.md` (booking), `02-front-office-process.md` (front-office map), `04-check-in-check-out-process.md` (check-in/out SP internals), `05-cashiering-and-finance-process.md` (folio/billing/day-end), `06-rooms-and-housekeeping-process.md` (room status), `07-fnb-and-outlet-process.md` (POS→folio), `11-integrations-and-data-flow.md` (external systems). For concrete step-by-step scenarios see `13-end-to-end-use-cases.md`.

---

## Purpose

A hotel stay is not one transaction — it is a **chain of transactions** that must all agree with one another: the booking must match the room allocated, the room charge must match the folio, the folio must be settled before the guest can check out, and the night audit must reconcile the whole day. This document shows how Scienter HotelERP moves **one guest record** through that entire chain, which module owns each stage, which controller/SP performs the work, which tables change, who does it, and what fires downstream.

The single architectural fact that governs everything: **a stay physically migrates between three sets of tables as its state changes.**

```
   Reservation*  ──(check-in)──▶  Inhouse*  ──(check-out)──▶  CheckedOut*
   (pre-arrival)                  (in-house)                  (departed)
```

A stay lives in exactly one set at a time; the source rows are deleted as it moves on (verified in `04-check-in-check-out-process.md`).

## Relevant users / departments

| User / department | Where they act in the lifecycle |
|---|---|
| Reservations agent | Enquiry, reservation create/price/confirm, group blocks, allotments, OTA re-push |
| Front Office / Reception | Pre-arrival prep, room allocation, quick check-in, key issue, room change, checkout |
| Cashier | Advances/deposits, folio postings, discounts, taxes, bill settlement, refunds |
| Housekeeping | Room cleaning/inspection driven by check-in / checkout / room-change status codes |
| F&B / outlet cashier | Posts outlet charges to the guest folio (bill-to-room) or settles at the outlet |
| Night Auditor | Room-rate verification, No-Show marking, day-end close, hotel-date roll |
| Guest Relations / Duty Manager | Guest messages, VIP handling, document delivery (GRC / invoice) |
| Guest | Provides identity (passport/NIC), signs the GRC, consumes services, pays |

Access to each screen is enforced by `[UserWisePageAccess(<pageId>, "<S|I|U|D>")]` on the controller action, scoped to `SessionObjects.LoggedUser.PropertyId` (multi-tenant).

## Preconditions

- Master data configured: rooms/categories/types (`RoomDetails`, `RoomCategories`, `RoomTypes`), rate codes & rates (`RateCodeHeaders`, `RoomRates`), meal plans, tax groups/types, payment types, profit centres, `BookingSettings`, `FOSettings`, document number series (`DocumentNumbers`: `RESNO`, `GRRESNO`, `GRC`, `PRC`, …).
- A logged-in user with page access, and the property's per-tenant DB (`HotelResWeb_<Property>`) reachable.
- The property has a **current hotel date** (`FOSettings.CurrentDate`) — every posting and the check-in/out gates key off it.

---

## Master flow — the complete guest lifecycle

```
 ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
 │                              GUEST LIFECYCLE (end to end)                                       │
 └──────────────────────────────────────────────────────────────────────────────────────────────┘

  1. RESERVATION                 2. PRE-ARRIVAL              3. ARRIVAL / CHECK-IN
  ┌───────────────────┐          ┌──────────────────┐        ┌────────────────────────────┐
  │ Make Reservation  │          │ Room allocation  │        │ Quick Check-In (page 2017) │
  │ ReservationCreation│  status │ (assign physical │        │ Reservation_T_QuickCheckIn │
  │ .SaveReservationNew│  =3     │  room)           │        │  Update                    │
  │ →Reservation_T_    │ Confirmed│ ReservationHeaders_T_    │  • GRC via 'GRC'           │
  │  Save_New          │────────▶│  Save_ReservationHeader- │  • Reservation_T_Folio-    │
  │ RESNO / GRRESNO    │         │  WiseRooms               │     Creation (open folio)  │
  │ (Confirmed 3,      │         │ Guest profile complete   │  • 'CKI' → FO 2050 Occupied│
  │  Tentative 4,      │         │ Passport/NIC scan        │     / HK 2030 Occ. Clean   │
  │  Cancelled 1,      │         │ (ScanedPassport_M_Save)  │  Reservation* ─▶ Inhouse*  │
  │  No-Show 2,        │         │ Signature capture        │  Door lock 'CI' · PABX ·   │
  │  Inquiry 5,        │         │ (GuestProfileWise-       │  RabbitMQ_GuestCheckIn     │
  │  Waitlist 6)       │         │  GuestSignature)         │                            │
  └─────────┬─────────┘          └──────────────────┘        └─────────────┬──────────────┘
            │  OTA inbound (Staah/Bookingwhizz → CMReservation*)          │
            │  Advance/deposit (Advance_Payment_T_Save / Sampath IPG)     ▼
            │                                              4. GUEST STAY (in-house)
            │                          ┌───────────────────────────────────────────────────────┐
            │                          │  Room charge (auto @ day-end):                         │
            │                          │    Reservation_T_FolioWisePostingBreakUp_Save          │
            │                          │  Extra services / outlet charges (bill-to-room):       │
            │                          │    Posting_InHouse_T_Save / ProfitcenterWisePosting_    │
            │                          │    M_Save → Insert_Folio → FolioHeader / FolioDetails   │
            │                          │  Room change: InHouseReservationDetail_T_ChangeRoom     │
            │                          │  Extend/shorten: Reservation_T_ChangeStaySave           │
            │                          │  Taxes (TaxCalculations → FoliowiseTaxDetails)          │
            │                          └───────────────────────────┬───────────────────────────┘
            │                                                       ▼
            │                                          5. PAYMENTS / SETTLEMENT
            │                          ┌───────────────────────────────────────────────────────┐
            │                          │ FolioManagementController.SettleBill →                 │
            │                          │   FolioService.SaveBill → Save_Folio                   │
            │                          │   → BillSettlementDetails + InvoiceNo on FolioHeader    │
            │                          │ Split / partial / multi-currency supported             │
            │                          └───────────────────────────┬───────────────────────────┘
            │                                                       ▼
            │                                          6. DEPARTURE / CHECK-OUT
            │                          ┌───────────────────────────────────────────────────────┐
            │                          │ Quick Check-Out (page 4030)                            │
            │                          │  Reservation_T_QuickCheckOutUpdate                     │
            │                          │  • GATE: open FolioHeader → RAISERROR('UnsettledBills') │
            │                          │  • Inhouse* ─▶ CheckedOut*                              │
            │                          │  • 'CKO' → FO 2061 Vacant / HK 2034 Vacant Dirty       │
            │                          │  • door key revoked · RabbitMQ_GuestCheckOut           │
            │                          └───────────────────────────┬───────────────────────────┘
            │                                                       ▼
            │                                          7. INVOICE / POST-STAY
            │                          ┌───────────────────────────────────────────────────────┐
            │                          │ Final invoice (settled folio, InvoiceNo)               │
            │                          │ Credit/Debit notes for post-invoice adjustment         │
            │                          │ Document delivery: GRC / invoice via Email / WhatsApp   │
            │                          │  (HK_Save_DocumentToDeliver)                           │
            │                          │ Guest Portal post-stay email · Guest History / CRM      │
            │                          └───────────────────────────────────────────────────────┘

  ═══════════════════════════════════════════════════════════════════════════════════════════
  NIGHT AUDIT (DAY-END) runs once per trading day across all in-house stays:
    DayEndProcessController.CompleteDayEnd → DayEnd_CompleteDayEnd (ordered steps)
      auto room posting (Reservation_T_FolioWisePostingBreakUp_Save) · guest ledger
      (DayEndSummaryGuestLedger) · property summary (DayEndSummary) · No-Show update
      (Reservations_T_UpdateNoShow) · HouseKeeping status · release OOO rooms
      → DayEnd_UpdateHotelDate advances the hotel date by one day
  ═══════════════════════════════════════════════════════════════════════════════════════════
```

---

## Stage-by-stage detail

Each stage below gives: **What happens (business)** · **Module/screen** · **Key controller/SP** · **DB tables touched** · **Users involved** · **Notifications/integrations.**

### Stage 1 — Reservation

| Aspect | Detail |
|---|---|
| **What happens (business)** | The guest's intent to stay is recorded: dates, room category/type, meal plan, rate, source, optional deposit, and status. May originate as a walk-in (source 6), a direct booking, or an OTA booking pushed in by the channel manager. |
| **Module / screen** | Reservation area — *Make Reservation* (page `6176`); *OTA Booking* for channel bookings. |
| **Key controller / SP** | `ReservationCreationController.SaveReservationNew` → `ReservationHeaderService.SaveReservationNew` → **`Reservation_T_Save_New`**. Numbering: `UpdateNextDocNoWithUpdate 'RESNO'` (and `'GRRESNO'` for groups). OTA inbound: `OTABookingController` → `Staah_*` SPs. |
| **DB tables touched** | `ReservationHeaders`, `ReservationDetails`, reservation profile/rate tables, `DocumentNumbers`, `BookingSettings`, `CMUpdateRanges` (outbound OTA push), `CMReservation*`/`Staah_ReservationRequests` (OTA inbound). |
| **Users involved** | Reservations agent (or OTA channel, automated). |
| **Notifications / integrations** | Confirmation email (`Reservation_T_Confirmation_Hotel`); channel-manager inventory push (`CMUpdateRanges`); online advance via Sampath IPG. |

**Status values (ReservationStatus, verified):** Confirmed **3**, Tentative **4**, Cancelled **1**, No-Show **2**, Inquiry **5**, Waitlist **6**. Only **Confirmed (3)** counts toward occupancy and is allowed to check in.

### Stage 2 — Pre-arrival

| Aspect | Detail |
|---|---|
| **What happens (business)** | Before the guest arrives, Front Office assigns a physical room, completes the guest profile (name, nationality, country, salutation, contact — no `TBA`/placeholder values), captures passport/NIC and signature, and (optionally) takes an advance/deposit. |
| **Module / screen** | Reservation area — *Room Allocation* (page `5500`); *Document / Scan* (`13044`/`14937`); Administration — *Guest Profiles* (`16`). |
| **Key controller / SP** | Allocation: `ReservationList.SaveReservationWiseRoomsAndAttributes` → **`ReservationHeaders_T_Save_ReservationHeaderWiseRooms`** (or `SaveQuickRoomAllocation`). Passport: `Document.SaveScannedDocument` → `ReservationDocument_M_Save`; `ScanedPassport_M_Save`. Signature: table `GuestProfileWiseGuestSignature`. Advance: `AdvancePaymentService.Save` → `Advance_Payment_T_Save`. |
| **DB tables touched** | `ReservationDetails` (RoomId), `GuestProfiles`, `ReservationDocument`/`UploadedPassportDocumentDetails`/`ScanedPassport` (image in `HotelResWeb_PassportScan`), `GuestProfileWiseGuestSignature`, folio (advance credit). |
| **Users involved** | Reservations agent, Front Office, Cashier (advance). |
| **Notifications / integrations** | Azure Blob (document/image store); `HotelResWeb_PassportScan` DB; Sampath IPG (online advance link). |

> **Gap:** the code-referenced signature-save SP `Reservation_T_SaveSignature` is **Not found in `HotelResWeb_Browns`** (the signature *table* exists); see doc 02 §N and doc 13 use case 16.

### Stage 3 — Arrival / Check-in

| Aspect | Detail |
|---|---|
| **What happens (business)** | At arrival the desk turns the confirmed booking into a live in-house stay: validates the guest and room, generates the Guest Registration Card (GRC) number, opens the folio, marks the room Occupied, and encodes keys. |
| **Module / screen** | Reservation area — *Quick Check-In* (page `2017`); *Key Request* (door lock). |
| **Key controller / SP** | `QuickCheckIns.QuickCheckIn` → `ReservationHeaderService.QuickCheckIn` → **`Reservation_T_QuickCheckInUpdate`** (GRC via `UpdateNextDocNoWithUpdate 'GRC'`; folio via `Reservation_T_FolioCreation`; status via `HouseKeeping_ProcessWiseStatusChanges_Update 'CKI'`). Keys: `DoorLockEvent_T_InsertOrDeleteKeyCode`. |
| **DB tables touched** | `InhouseReservationHeaders`/`InHouseReservationDetails`/`InHouseReservationProfiles` (inserted), `ReservationHeaders`/`Details`/`Profiles` (deleted), `FolioHeader`/`FolioDetails`, `RoomDetails` (status → FO **2050 Occupied**, HK **2030 Occupied Clean**), `DocumentNumbers`, audit tables. |
| **Users involved** | Front Office / Reception; Cashier (deposit at check-in); Guest (signs GRC). |
| **Notifications / integrations** | Door lock `DoorLockEvent_T_Save 'CI'`; PABX `TelMonEvent_T_Save 'CI'`; OHIP `RabbitMQ_GuestCheckIn`; Guest Portal in-stay email; occupancy recompute (`Dayend_RevenueAndOccupancySummary_Executions_M_Save`). |

**Check-in gate:** allocated room + `RoomStatus.IsAllowCheckIn = 1` (only **22 Vacant Inspected**) + status Confirmed + complete guest profile + arrival = current hotel date + non-zero rate on chargeable rooms.

### Stage 4 — Guest stay (room charges + extra services)

| Aspect | Detail |
|---|---|
| **What happens (business)** | During the stay, charges accumulate on the folio: the nightly **room charge** (posted automatically at day-end), plus extra services (laundry, minibar, telephone) and **outlet charges** (restaurant/bar/spa) billed to the room. The desk may also change the room or extend/shorten the stay. |
| **Module / screen** | CashieringAndPosting — *Posting*, *Profit-Centre Posting*; Reservation — *Room Change* (`4031`/`5526`), *Change Stay*. |
| **Key controller / SP** | Room charge (auto): **`Reservation_T_FolioWisePostingBreakUp_Save`** (inside day-end). Manual extra: `PostingController.SaveInHouse` → **`Posting_InHouse_T_Save`**. Outlet→folio: `ProfitcenterWisePosting_M_Save` / `Posting_InHouse_T_Save` → **`Insert_Folio`**. Room change: **`InHouseReservationDetail_T_ChangeRoom`** (`RoomChangeLogs`). Extend/shorten: **`Reservation_T_ChangeStaySave`**. Taxes: `TaxCalculations`. |
| **DB tables touched** | `FolioHeader`, `FolioDetails`, `FoliowiseTaxDetails`, `FolioWisePostingBreakUp`, `ExtraPostingDetails`(+taxes/settlements), `ProfitCenter_txn*`, `RoomChangeLogs`, `InHouseReservationDetails`. |
| **Users involved** | Cashier, F&B/outlet cashier, Front Office (room change/extend), Night Auditor (auto room posting). |
| **Notifications / integrations** | POS API (`Posting_InHouse_T_Save`); room-change fan-out (`RCGO`/`RCGN` housekeeping, door lock, PABX, `RabbitMQ_GuestRoomChange`, `CMUpdateRanges`). |

### Stage 5 — Payments / settlement

| Aspect | Detail |
|---|---|
| **What happens (business)** | The cashier previews the bill, applies any discounts/tax removals, generates the invoice and settles the folio with one or more payment types (cash, card, bank, voucher, bill-to-room), possibly split or partial and in multiple currencies. Advances taken earlier are offset here. |
| **Module / screen** | CashieringAndPosting — *Folio Management* (bill preview / bill settlement). |
| **Key controller / SP** | Preview: `FolioManagementController.CalculateBillTotal` → `CalculateFolioChargersToBill`. Settle: **`FolioManagementController.SettleBill`** → `FolioService.SaveBill` → **`Save_Folio`** (writes `BillSettlementDetails`, stamps `InvoiceNo`, locks folio). Group: `Save_MultipleFolio`. |
| **DB tables touched** | `BillSettlementDetails`, `FolioHeader` (`InvoiceNo`, `IsLock`), `FolioDetails`, `PaymentTypes`. |
| **Users involved** | Front Office cashier. |
| **Notifications / integrations** | Fiscal printer (`FiscalPrinter_FolioInvoice`, localhost:1304); Sampath IPG (online settlement); FX gain/loss captured in `BillSettlementDetails.ConRateGainOrLoss`. |

### Stage 6 — Departure / check-out

| Aspect | Detail |
|---|---|
| **What happens (business)** | The desk checks the guest out. Checkout is **hard-gated by an open folio** — the bill must be settled first. On success the stay migrates to the checked-out tables, the room is released dirty for cleaning, and the door key is revoked. |
| **Module / screen** | Reservation area — *Quick Check-Out* (page `4030`). |
| **Key controller / SP** | `QuickCheckOut.QuickCheckOut` → **`Reservation_T_QuickCheckOutUpdate`** (gate: open `FolioHeader` → `RAISERROR('UnsettledBills')`; status via `HouseKeeping_ProcessWiseStatusChanges_Update 'CKO'`; key via `DoorLockEvent_T_InsertOrDeleteKeyCode 'C'`). |
| **DB tables touched** | `CheckedOutReservationHeaders`/`Details`/`Profiles` (inserted), `InhouseReservationHeaders`/`Details`/`Profiles` (deleted), `RoomDetails` (status → FO **2061 Vacant**, HK **2034 Vacant Dirty**). |
| **Users involved** | Front Office / Reception; Cashier (final settlement). |
| **Notifications / integrations** | Door lock `DoorLockEvent_T_Save 'CO'` + key revoke; PABX `'CO'`; OHIP `RabbitMQ_GuestCheckOut`; Guest Portal post-stay email; occupancy recompute. |

### Stage 7 — Invoice / post-stay

| Aspect | Detail |
|---|---|
| **What happens (business)** | The settled folio is the final invoice. Post-departure adjustments are made by credit/debit notes. Documents (GRC, final invoice, outstanding statement) can be re-sent to the guest by email or WhatsApp, and stay history feeds CRM. |
| **Module / screen** | CashieringAndPosting — *Credit/Debit Notes*; root *Document Delivery*; Administration — *Guest History* (`7`). |
| **Key controller / SP** | Notes: `CreditOrDebitNotesNewController.Save_FolioDetails` → `CreditOrDebitNote_InvoiceNoWiseDetails_Save`. Delivery: `DocumentDeliveryController.SaveDocumentToDeliver` → **`HK_Save_DocumentToDeliver`** (types via `HKDocumentTypes_Select`; methods `1 Email`, `2 WhatsApp`). Settled-bill read: `InvoiceDetails_M_SelectForCheckedOutReservations`. |
| **DB tables touched** | `BillSettlementDetails`, credit/debit note tables, `HK_DocumentToDeliver` (delivery queue), `CheckedOut*`. |
| **Users involved** | Cashier, Finance, Guest Relations. |
| **Notifications / integrations** | Email (SMTP/`BEMailSender`) / WhatsApp — **WhatsApp send implementation Not found in the project** (only queued); SSRS for the invoice/registration documents. |

### Night audit (day-end) — the daily reconciliation across all stages

| Aspect | Detail |
|---|---|
| **What happens (business)** | Once per trading day the night auditor closes the day: verifies room rates, auto-posts each in-house room's night charge, produces the guest-ledger trial balance and property summary, marks No-Shows, updates housekeeping status, releases expired OOO rooms, then advances the hotel date. |
| **Module / screen** | CashieringAndPosting — *Day-End Process* (page `6001`). |
| **Key controller / SP** | `DayEndProcessController.CompleteDayEnd` → **`DayEnd_CompleteDayEnd`** (ordered steps from `DayEnd_CompleteDayEnd_SP_ExecutionSteps`); auto room posting **`Reservation_T_FolioWisePostingBreakUp_Save`**; No-Show **`Reservations_T_UpdateNoShow`**; hotel-date roll **`DayEnd_UpdateHotelDate`**. |
| **DB tables touched** | `FolioWisePostingBreakUp`, `DayEndSummaryGuestLedger`, `DayEndSummary`, `DayEndRoomStatus`, `DayEndDayEndStepCompletion`, `FOSettings` (`CurrentDate`+1). |
| **Users involved** | Night Auditor. |
| **Notifications / integrations** | GL data prepared internally (`Dayend_GL_*`); day-end GL/kitchen push to `Categlog_vrV2`; revenue-report email job. |

---

## Modules & users involved per stage — summary table

| Stage | Primary module(s) | Key screen | Key SP | Main users | Fires downstream |
|---|---|---|---|---|---|
| 1. Reservation | Reservation | Make Reservation (6176) | `Reservation_T_Save_New` | Reservations agent / OTA | Email confirm, `CMUpdateRanges` |
| 2. Pre-arrival | Reservation + Administration | Room Allocation (5500), Guest Profiles (16), Doc/Scan (13044) | `ReservationHeaders_T_Save_ReservationHeaderWiseRooms`, `ScanedPassport_M_Save`, `Advance_Payment_T_Save` | Reservations, FO, Cashier | Azure Blob, PassportScan DB, IPG |
| 3. Check-in | Reservation | Quick Check-In (2017) | `Reservation_T_QuickCheckInUpdate` | Front Office | HK `CKI`, door lock, PABX, RabbitMQ, Guest Portal |
| 4. Guest stay | CashieringAndPosting + Reservation + F&B | Posting, Profit-Centre, Room Change (4031), Change Stay | `Posting_InHouse_T_Save`, `Insert_Folio`, `Reservation_T_FolioWisePostingBreakUp_Save`, `InHouseReservationDetail_T_ChangeRoom` | Cashier, F&B cashier, FO, Night Auditor | POS API, HK `RCGO`/`RCGN`, RabbitMQ |
| 5. Settlement | CashieringAndPosting | Folio Management (bill settlement) | `Save_Folio` | Cashier | Fiscal printer, IPG |
| 6. Check-out | Reservation | Quick Check-Out (4030) | `Reservation_T_QuickCheckOutUpdate` | Front Office, Cashier | HK `CKO`, door-key revoke, RabbitMQ, Guest Portal |
| 7. Invoice / post-stay | CashieringAndPosting + Document Delivery + Administration | Credit/Debit Notes, Document Delivery, Guest History (7) | `CreditOrDebitNote_InvoiceNoWiseDetails_Save`, `HK_Save_DocumentToDeliver` | Cashier, Finance, Guest Relations | Email / WhatsApp (queued), SSRS |
| Night audit (all) | CashieringAndPosting | Day-End Process (6001) | `DayEnd_CompleteDayEnd`, `DayEnd_UpdateHotelDate` | Night Auditor | GL/kitchen push to `Categlog_vrV2` |

---

## Cross-cutting business rules (carried from the module docs)

1. A stay lives in exactly one table set; check-in migrates `Reservation* → Inhouse*`, checkout migrates `Inhouse* → CheckedOut*`, and source rows are deleted.
2. Only **Confirmed (3)** reservations count toward occupancy and may check in; only Confirmed writes room rates on save.
3. Numbers are property-prefixed, zero-padded, issued atomically by `UpdateNextDocNoWithUpdate` (`RESNO`/`GRRESNO`/`GRC`/`PRC`…).
4. Room status is machine-driven by process code: `CKI` → Occupied Clean, `CKO` → Vacant Dirty, room change `RCGO`/`RCGN`; **only `22 Vacant Inspected` allows check-in** (`IsAllowCheckIn = 1`).
5. Checkout is **blocked by any open `FolioHeader`** (`UnsettledBills`) — the bill must be settled first.
6. The nightly room charge is posted **automatically by day-end** (`Reservation_T_FolioWisePostingBreakUp_Save`), not manually, using verified rates.
7. No posting is allowed while day-end is running (SPs guard `DayEndDayEndStepCompletion`); extend-stay/room-change also blocked mid-day-end.
8. Everything is transactional and scoped to `PropertyId`; failures roll back and log to `GEN_ErrTable`.

## Expected result

A guest flows cleanly through booking → arrival → stay → payment → departure with one consistent record: a priced reservation becomes an in-house stay with a GRC and an open folio, charges (room + extras + outlets) accrue and are taxed, the folio is settled into a numbered invoice, checkout releases the room dirty for housekeeping and revokes the key, and the night audit reconciles the day and rolls the hotel date. Every financial movement is captured for accounting and every state change fans out to housekeeping, door locks, PABX, OHIP and (where configured) the channel manager and guest portal.

## Error scenarios (lifecycle-level)

| Where | Trigger | System behaviour |
|---|---|---|
| Reservation | No rate / category oversold | `104-No Room Rates…` (offer tentative) / overbooking block |
| Check-in | Dirty/occupied room, incomplete profile, arrival ≠ hotel date, zero rate | `Reservation_T_QuickCheckInUpdate` raises the specific error; check-in refused |
| Stay | Posting during day-end / stop-posting reservation | *"Day end is processing…"* / *"Reservation marked as stop posted"* |
| Settlement | Under-payment | Folio retains a positive balance (partial payment) |
| Check-out | Open folio / unsettled POS bill (SS003) | `RAISERROR('UnsettledBills')` / *"unsettled restaurant bills…"* — checkout refused |
| Day-end | Validation fails (pending arrivals, unverified rates, unsettled POS) | `CompleteDayEnd` returns `"ERR-Dayend validation(s) fail."`; nothing committed |
| Post-stay | WhatsApp document send | Only queued — **WhatsApp dispatcher Not found in the project** |

## Related documents

- `13-end-to-end-use-cases.md` — concrete step-by-step use cases for every scenario above.
- `03-reservation-process.md`, `02-front-office-process.md`, `04-check-in-check-out-process.md` — booking → front office → check-in/out.
- `05-cashiering-and-finance-process.md`, `06-rooms-and-housekeeping-process.md`, `07-fnb-and-outlet-process.md` — money, rooms, outlets.
- `11-integrations-and-data-flow.md` — payment gateway, channel manager, fiscal printer, SMS/email/WhatsApp, RabbitMQ, SSRS, Azure, SSO, POS DB.
- `00-project-overview.md` — architecture and module map.

---

### "Not found in the project" items (carried from module docs)

- **`Reservation_T_SaveSignature`** — referenced in `ReservationHeaderEntry.cs` but not deployed in `HotelResWeb_Browns` (signature *table* exists).
- **`Reservations_W_ValidatePOSBill_AtCheckout`** — referenced by the checkout POS pre-check but not deployed in Browns; only runs when `SystemSettings SS003` is on.
- **WhatsApp send implementation** — WhatsApp is offered as a delivery method; the document is only queued (`HK_Save_DocumentToDeliver`); no dispatcher in this checkout.
- **Automatic early-check-in / late-checkout / cancellation penalty** — no fee is posted by the check-in/checkout/cancel SPs; charges are manual folio postings.
