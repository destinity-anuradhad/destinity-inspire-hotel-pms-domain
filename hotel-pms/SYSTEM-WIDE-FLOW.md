# System-Wide Flow — Reservation → Front Office → Housekeeping → Cashiering → Accounts → Checkout → Reports

> **Purpose:** Show the complete operational flow of the hotel through the PMS as one continuous story, and how a guest and their money move across every module. Every stage links to its detailed document.
> **Grounding:** All controller / stored-procedure / table / status names below were verified against the source code and the live `HotelResWeb_Browns` database.

---

## 1. The one-page picture

```
                          ┌───────────────────────────────────────────────────────────────┐
                          │                    HOTEL "BUSINESS DATE"                        │
                          │      advanced only by the nightly DAY-END (night audit)         │
                          └───────────────────────────────────────────────────────────────┘

  OTA / Channel Mgr ─┐
  Booking Engine    ─┤
  Walk-in / Phone   ─┼──►  (1) RESERVATION  ──►  (2) FRONT OFFICE  ──►  (3) HOUSEKEEPING
  Company / Agent   ─┘        create/confirm        arrival/check-in        clean → inspect → ready
                              deposit (advance)      room allocation                │
                                   │                      │                         │  (room status gates
                                   │                      ▼                         │   the next check-in)
                                   │             (4) CASHIERING & POSTING  ◄─────────┘
                                   │                 folio charges, room rent,
                                   │                 POS/F&B, taxes, discounts,
                                   │                 payments, advances
                                   │                      │
                                   ▼                      ▼
                          (5) ACCOUNTS / DAY-END  ──► (6) CHECK-OUT  ──► (7) REPORTS & DASHBOARDS
                          night audit, guest ledger,   settle bill,       revenue, occupancy,
                          revenue & occupancy summary,  invoice,           arrivals/departures,
                          hotel-date roll-forward       room → dirty       cashier, audit
```

Detailed docs per stage: [03](03-reservation-process.md) · [02](02-front-office-process.md) / [04](04-check-in-check-out-process.md) · [06](06-rooms-and-housekeeping-process.md) · [05](05-cashiering-and-finance-process.md) · [07](07-fnb-and-outlet-process.md) · [10](10-reports-and-business-information.md).

---

## 2. Stage-by-stage flow

### Stage 1 — Reservation *(module: Reservation)*
**Business:** A room (or block of rooms) is booked for a guest/company for specific dates, at a rate and meal plan, from some source (walk-in, phone, OTA, company, booking engine). A deposit/advance may be taken.

| Step | What happens | Key technical objects |
|---|---|---|
| Availability | Check free rooms per night | SP `RoomAvailability_R_Select` (Actual − Reservations − OOO − Balance) |
| Create | Save reservation header + room + guest | `ReservationCreationController.SaveReservationNew` → `ReservationHeaderService.SaveReservationNew` → SP `Reservation_T_Save_New` |
| Numbering | Generate confirmation no. | `UpdateNextDocNoWithUpdate 'RESNO'` (group `'GRRESNO'`) → e.g. `OEB0049910` |
| Status | Confirmed / Tentative / Waitlist | `ReservationStatus` (Confirmed **3**, Tentative **4**, Cancelled **1**, No-Show **2**) |
| Deposit | Advance request / online link | `AdvanceRequestHeaders/Details`, `AdvancePaymentLinks`, Sampath IPG |
| Channel | OTA bookings inbound | `OTABookingController` ↔ `Staah_*` / `CMReservation*` |

**Hand-off:** a Confirmed reservation waits in the arrivals list for its arrival date. → *Stage 2*.

### Stage 2 — Front Office / Check-in *(module: Reservation FrontDesk + GuestProfiles)*
**Business:** On arrival day, the guest is identified, a physical room is allocated, ID/passport and signature are captured, a deposit may be taken, and the guest is **checked in** — becoming "in-house".

| Step | What happens | Key technical objects |
|---|---|---|
| Allocate room | Assign a specific ready room | `RoomAllocationController`; only **Vacant Inspected** rooms allow check-in (`IsAllowCheckIn=1`) |
| Register | Capture guest, passport/NIC, signature | `GuestProfilesController`; passport images in `HotelResWeb_PassportScan` |
| Check-in | Convert reservation → in-house | SP `Reservation_T_QuickCheckInUpdate`: GRC via `'GRC'`, copies `Reservation*`→`Inhouse*`, opens folio via `Reservation_T_FolioCreation` |
| Room status | Mark occupied | `HouseKeeping_ProcessWiseStatusChanges_Update 'CKI'` → FO **2050 Occupied** / HK **2030 Occupied Clean** |
| Notify | Door lock / PABX / queue | door-lock key-code event, `RabbitMQ_GuestCheckIn` |

**Hand-off:** in-house guest now accrues charges (→ *Stage 4*); room becomes Housekeeping's responsibility (→ *Stage 3*).

### Stage 3 — Housekeeping *(module: HouseKeeping + Maintenance)*
**Business:** Rooms are cleaned, inspected and returned to "ready" so the next guest can check in. Rooms needing repair are taken **Out of Order / Out of Service** and removed from availability.

| Step | What happens | Key technical objects |
|---|---|---|
| Status model | Unified `RoomStatus` referenced by `RoomDetails.Current*StatusId` | HK: Vacant Dirty **2034** / Clean **2033** / Inspected **22** / Ready **2068**; Occupied Dirty **6** / Clean **2030** |
| Cleaning | Attendant updates, supervisor reviews, room inspected | `HouseKeeping_UpdateRoomStatus`, `HouseKeeping_ProcessWiseStatusChanges_Update`, `RoomInspectionDetails_T_Save` |
| OOO/OOS | Block room for maintenance | `OutOfOrderTXN_M_Insert` (subtracted in `RoomAvailability_R_Select`) |
| Mobile | Field updates | HouseKeeping API (`HKSettings.HouseKeepingApiUrl`) |

**Feedback loop:** room status **gates availability and the next check-in** — closing the loop back to Stages 1–2.

### Stage 4 — Cashiering & Posting *(module: CashieringAndPosting)*
**Business:** Every charge and payment lands on the guest **folio**. Room rent posts automatically at night; F&B/spa/laundry/extras post during the stay; taxes and discounts apply; the guest pays by cash/card/bank/online.

| Step | What happens | Key technical objects |
|---|---|---|
| Folio | Opened at check-in | `FolioHeader` / `FolioDetails` (+ `FolioWisePostingBreakUp`, `FoliowiseTaxDetails`) |
| Manual posting | Charge or payment line | `PostingController` → `Posting_InHouse_T_Save` / `Posting_WalkIn_T_Save` |
| Room rent | Auto per night | Day-end step → `Reservation_T_FolioWisePostingBreakUp_Save` |
| POS / F&B | Outlet charge to room | `POSApiController.SaveInHousePOSAPIPosting` → `Posting_InHouse_T_Save` → `Insert_Folio` |
| Tax | VAT 18% / SC 10% / SSCL 2.56% / TDL 1% | `TaxTypes`, `TaxGroups`, `Folio_T_CalculateTaxTaxGroupWise` |
| Advances | Deposits / IPG | `AdvanceRequest*`, `AdvancePaymentLinks` |
| Transfer/route | Between folios / to company | `Folio_T_RoomToRoomTransfer`, `BillToRoomLog` |

**Hand-off:** balances feed the nightly ledger (→ *Stage 5*) and the checkout settlement (→ *Stage 6*).

### Stage 5 — Accounts / Day-End (Night Audit) *(module: CashieringAndPosting + NightAudit)*
**Business:** Once a day the hotel "closes the day": it posts room rent, freezes the day's numbers, produces the guest ledger and revenue/occupancy summary, then advances the hotel business date.

| Step | What happens | Key technical objects |
|---|---|---|
| Orchestration | Ordered day-end steps (1–26) | table `DayEnd_CompleteDayEnd_SP_ExecutionSteps`; `DayEndProcessController` → `DayEndService` |
| Auto room posting | Post night's room rent | step 4 → `Reservation_T_FolioWisePostingBreakUp_Save` |
| Guest ledger | Snapshot of open balances | `DayEnd_SummaryGuestLedger_M_Save` → `DayEndSummaryGuestLedger` |
| Summaries | Revenue & occupancy | `DayEndSummary`, `Dayend_RevenueAndOccupancySummary_Executions` |
| Date roll | Advance business date | `DayEnd_UpdateHotelDate` |

**Note:** GL posting during FO day-end is present but **commented out** (see [15](15-known-issues-and-improvement-suggestions.md)); external accounting/GL export is **Not found in the project**.

### Stage 6 — Check-out *(module: Reservation + CashieringAndPosting)*
**Business:** The guest settles the bill, gets an invoice, and leaves; the room is released to Housekeeping as dirty.

| Step | What happens | Key technical objects |
|---|---|---|
| Balance gate | Block checkout if folio open | SP `Reservation_T_QuickCheckOutUpdate` → `RAISERROR('UnsettledBills')` |
| Settle | Pay & close folio, write invoice | `FolioManagementController.SettleBill` → `FolioService.SaveBill` → `Save_Folio`; `BillSettlementDetails` |
| Move guest | In-house → checked-out | `Inhouse*` → `CheckedOut*` |
| Room status | Release room | `'CKO'` → FO **2061 Vacant** / HK **2034 Vacant Dirty** → back to *Stage 3* |
| Post-stay | Feedback / documents | GuestPortal feedback; document delivery/email |

### Stage 7 — Reports & Business Information *(module: Reporting + DataAnalysis)*
**Business:** Management reads the results — revenue, occupancy, arrivals/departures, cashier, housekeeping, audit — to run the hotel.

| Category | Representative report / SP | Delivery |
|---|---|---|
| Revenue | `Report_ARR_ADR_RevPar_Analysis`, `Reports_AgentWiseRoomRevenue` | SSRS `ReportServer` |
| Occupancy | forecast / pickup / room-nights | SSRS / grid |
| Arrivals & Departures | `ArrivalDepartureController` | DevExpress grid → PDF/XLS |
| Cashier / Financial | day-end summary, guest ledger, settlements | SSRS |
| Audit | void / discount / rebate / access logs | SSRS / grid |
| Dashboards | `DashboardAPI_*` (193 SPs) | DataAnalysis JSON charts |

Report access is controlled by `UserWiseReportAccess`. Registry: `ReportDetails` (219 reports).

---

## 3. Where the "money" and the "guest" objects live at each stage

| Stage | Guest record lives in | Money/charges live in |
|---|---|---|
| Reservation | `ReservationHeader` + reservation profiles | `AdvanceRequest*` (deposits) |
| Check-in → stay | `InhouseReservationHeaders/Details/Profiles` | `FolioHeader` / `FolioDetails` |
| Day-end | (unchanged) | `DayEndSummaryGuestLedger`, `FolioWisePostingBreakUp` |
| Check-out | `CheckedOutReservationHeaders/…` | `BillHeader` / `BillSettlementDetails` |

---

## 4. Cross-stage integrations (who gets notified)

- **Check-in/out** → door-lock key-code event, PABX, `RabbitMQ_*` messages, guest notifications.
- **Reservation** ↔ **Channel managers** (Staah / Bookingwhizz / CM) keep OTA availability in sync.
- **Advances / settlement** ↔ **Sampath IPG** for online card payments.
- **Documents/invoices** → email / document-delivery (WhatsApp dispatcher itself: *Not found in the project*).
- Full detail: [11-integrations-and-data-flow.md](11-integrations-and-data-flow.md).

---

## 5. Related documents
[01 Complete hotel process](01-complete-hotel-process.md) · [05 Cashiering & finance](05-cashiering-and-finance-process.md) · [06 Rooms & housekeeping](06-rooms-and-housekeeping-process.md) · [13 End-to-end use cases](13-end-to-end-use-cases.md) · [MODULE-DEPENDENCY-MAP](MODULE-DEPENDENCY-MAP.md).
