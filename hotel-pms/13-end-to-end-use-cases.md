# 13 — End-to-End Use Cases

> Scienter HotelERP — Destinity Inspire / Destinity Horizon Front Office (Hotel PMS).
> **This is a synthesis document.** It replays the verified module docs as concrete, step-by-step **use cases** a hotel actually runs. Every controller/action, service, stored procedure (SP), table and status value is **carried over from the already-written docs** — nothing is invented. Each use case uses the **6-step format** (1. user action → 2. system validation → 3. database change → 4. related module update → 5. notification/integration → 6. final result), followed by the **expected result** and **error scenarios**. Where a feature is absent or partial, the intended flow is described from code and the gap is flagged **"Not found in the project."**

> **Deep-dive references:** booking `03-reservation-process.md`; front office `02-front-office-process.md`; check-in/out `04-check-in-check-out-process.md`; cashiering/day-end `05-cashiering-and-finance-process.md`; rooms/housekeeping `06-rooms-and-housekeeping-process.md`; F&B/POS `07-fnb-and-outlet-process.md`; integrations `11-integrations-and-data-flow.md`. For the whole lifecycle narrative see `01-complete-hotel-process.md`.

## Purpose

To give front-office, cashier, housekeeping and night-audit staff (and implementers) a single reference of **exactly what the system does** for the most common real-world situations — from a walk-in booking to a WhatsApp document send — so each scenario can be followed, tested and supported end to end.

## Relevant users / departments

Reservations agent · Front Office / Reception · Cashier · Housekeeping (room boy / supervisor) · Maintenance / Engineering · Night Auditor · Guest Relations / Duty Manager. Access to every action is enforced by `[UserWisePageAccess(<pageId>, "<S|I|U|D>")]`, scoped to the logged-in user's `PropertyId`.

## Preconditions (apply to all use cases)

- Master data configured (rooms, rates, meal plans, taxes, payment types, profit centres, `BookingSettings`, `FOSettings`, `DocumentNumbers`).
- A logged-in user with the relevant page access; property DB (`HotelResWeb_<Property>`) reachable; a current hotel date in `FOSettings.CurrentDate`.

**Status quick-reference (verified):** ReservationStatus — Confirmed **3**, Tentative **4**, Cancelled **1**, No-Show **2**, Inquiry **5**, Waitlist **6**. Room HK status — **22 Vacant Inspected** (only status that allows check-in), **2034 Vacant Dirty**, **2033 Vacant Clean**, **2030 Occupied Clean**, **2044 Out of Order**, **2045 Out of Service**. Room FO status — **2050 Occupied**, **2061 Vacant**, **2067 Out of Order/Service**.

---

## Use case 1 — Walk-in guest booking → checkout

**Scenario:** A guest arrives with no prior reservation, is booked in on the spot, stays, and checks out. A walk-in is the ordinary *create → allocate → quick-check-in* sequence with `BookingSourceId = 6 Walk-in` (there is **no single one-click walk-in super-action** — Not found in the project).

1. **User action** — FO creates the booking via *Make Reservation* with source Walk-in, status Confirmed, arrival = today; creates/picks the guest inline; allocates a room; then opens *Quick Check-In* and confirms.
2. **System validation** — Create: rate must exist for category+type+meal-plan+dates (else `104`), category not oversold. Check-in gate: allocated room, `RoomStatus.IsAllowCheckIn = 1` (only **22 Vacant Inspected**), status Confirmed, complete guest profile (no `TBA`/defaults), arrival = hotel date, non-zero rate.
3. **Database change** — Create: `Reservation_T_Save_New` writes `ReservationHeaders`/`Details` and issues `RESNO`. Allocate: `ReservationHeaders_T_Save_ReservationHeaderWiseRooms` sets `RoomId`. Check-in: `Reservation_T_QuickCheckInUpdate` inserts `Inhouse*`, deletes `Reservation*`, issues `GRC` (`UpdateNextDocNoWithUpdate 'GRC'`), opens the folio (`Reservation_T_FolioCreation`).
4. **Related module update** — `HouseKeeping_ProcessWiseStatusChanges_Update 'CKI'` → room FO **2050 Occupied** / HK **2030 Occupied Clean**; occupancy recompute. At checkout: `'CKO'` → FO **2061 Vacant** / HK **2034 Vacant Dirty**.
5. **Notification / integration** — Door lock `'CI'`, PABX `'CI'`, `RabbitMQ_GuestCheckIn`; at checkout key revoke + `RabbitMQ_GuestCheckOut`.
6. **Final result** — Guest stays (room charge auto-posted at day-end + any extras). Cashier settles the folio (`SettleBill` → `Save_Folio` → `BillSettlementDetails` + `InvoiceNo`). Checkout (`Reservation_T_QuickCheckOutUpdate`) migrates to `CheckedOut*`.

**Expected result:** A same-day booking becomes an in-house stay with a GRC and open folio, is billed and settled, and departs with the room released dirty for housekeeping.

**Error scenarios:** no rate → `104` (offer tentative); dirty/uninspected room → check-in refused; incomplete profile → *"Guest profile is not completed…"*; open folio at checkout → `RAISERROR('UnsettledBills')`.

---

## Use case 2 — Online reservation → check-in

**Scenario:** An OTA booking (Booking.com/Expedia via Staah) flows into the PMS and the guest is later checked in.

1. **User action** — The channel posts the booking (XML/API) into the Staah request tables. The reservations agent reviews received bookings and (if needed) re-pushes into the PMS; on arrival day, FO does Quick Check-In.
2. **System validation** — Inbound mapping resolves OTA room-category/meal-plan codes to PMS ids (`STAAH_Mapping_*`); voucher-number duplication checked. Check-in gate as in use case 1.
3. **Database change** — Inbound: `OTABookingController.ReceivedOTABookings` (`Staah_ReservationRequests_Select_ReceivedReservations`), re-push `Staah_ReservationRequestRePush`; the synced booking becomes a `ReservationHeaders` row (`BookingMethod = IBE`/API, `BookingSourceId = 4 OTA`). Check-in: `Reservation_T_QuickCheckInUpdate` as above.
4. **Related module update** — Room allocation (if not pre-assigned) then `'CKI'` housekeeping status; occupancy recompute.
5. **Notification / integration** — Inbound from Staah; on any inventory change, outbound `CMUpdateRanges` / `Staah_AvailabilityPush`. Check-in fires door lock / PABX / `RabbitMQ_GuestCheckIn`.
6. **Final result** — The OTA booking is a normal confirmed reservation, then an in-house stay.

**Expected result:** OTA bookings appear in the PMS and check in exactly like direct bookings, with mapping applied.

**Error scenarios:** failed inbound booking stays pending → manual **Re-Push** (`Staah_ReservationRequestRePush`); channel API endpoints/credentials and automatic retry are **Not found in the project (external worker)** (doc 11).

---

## Use case 3 — Group booking

**Scenario:** A tour operator books 10 rooms under one group; rooms are allocated and checked in together.

1. **User action** — Reservations creates multiple room reservations sharing a `GroupReservationNo` (e.g. `GOEB005009`); or attaches existing reservations to a group. At arrival, FO does group room allocation then group check-in.
2. **System validation** — Group number issued via `UpdateNextDocNoWithUpdate 'GRRESNO'`; each room validated for rate/availability as normal; check-in loops the per-reservation gate.
3. **Database change** — Create: `Reservation_T_Save_New` (shared group no). Attach/detach: `Reservation_T_AttachToGroupSave` / `Reservation_T_Multiple_DetachSave`. Group allocation: `Reservation_T_RoomAllocation_GroupBooking` → `AllocatedRoomsForGroupReservation_T_Update`. Check-in: `Reservation_T_QuickCheckInUpdate` loops per reservation.
4. **Related module update** — Each room independently flips to `'CKI'` Occupied Clean; in-house group view via `InhouseReservationList_T_Select_AdvanceSearch_GroupReservations`.
5. **Notification / integration** — Per-room door lock / PABX / RabbitMQ check-in events; allotment rooms (if from an `AllotmentHeaders` block) drawn down.
6. **Final result** — A group operates as many linked stays; billing may route to a master/company folio (see use case 8 / folio transfers in doc 05).

**Expected result:** One group number ties together many rooms that allocate, check in and (optionally) bill together.

**Error scenarios:** any room oversold blocks that room's save; a room without a valid rate cannot check in.

---

## Use case 4 — Room change (move an in-house guest)

**Scenario:** An in-house guest is moved from room 210 to room 315 (upgrade).

1. **User action** — FO opens *Room Change* (page `4031`/`5526`), selects the in-house reservation, picks the target room and a reason (`1 Room Upgrade`, `4 Room Change`, `3 Room Upsale`, `2 Other`), enters a remark, and submits.
2. **System validation** — `InHouseReservationDetail_T_ChangeRoom` validates the target room is free and in an allowed HK status (Vacant Inspected); re-runs `RoomAvailability_R_Select`.
3. **Database change** — Writes a `RoomChangeLogs` row (from/to room, reason, from/to category, hotel date, remark); moves the room on `InHouseReservationDetails`, `FolioHeader`, `FolioDetails(History)` and `ExtraPostingDetails` from the hotel date forward; recomputes `IsAddToOccupancy`.
4. **Related module update** — Old room → `HouseKeeping_ProcessWiseStatusChanges_Update 'RCGO'` (Vacant / Vacant Dirty); new room → `'RCGN'` (Occupied / Occupied Clean); occupancy recompute (`Dayend_RevenueAndOccupancySummary_Executions_M_Save`).
5. **Notification / integration** — `CMUpdateRanges` (push freed dates to OTAs); `DoorLockEvent_T_Save 'RC'`; `TelMonEvent_T_Save 'RC'`; `RabbitMQ_GuestRoomChange`.
6. **Final result** — The guest, folio and housekeeping all reflect the new room; the old room queues for cleaning.

**Expected result:** Guest and all charges follow the guest to the new room; both rooms carry the correct status.

**Error scenarios:** target room occupied/blocked/uninspected → *"Room X already allocated…"* / *"not in allowed housekeeping status"*.

---

## Use case 5 — Guest checkout with outstanding balance

**Scenario:** FO tries to check out a guest whose folio still has an open balance.

1. **User action** — FO opens *Quick Check-Out* (page `4030`), ticks the departing reservation, confirms.
2. **System validation** — `Reservation_T_QuickCheckOutUpdate` runs `IF EXISTS(SELECT 1 FROM FolioHeader WHERE ReservationHeaderID IN (@Temp))` → **`RAISERROR('UnsettledBills', 16, 1)`**. If `SystemSettings SS003` is on, the controller also pre-checks unsettled restaurant/POS bills.
3. **Database change** — **None** — the transaction is aborted before any migration. No `CheckedOut*` rows are written.
4. **Related module update** — None; the room stays Occupied and the stay stays in-house.
5. **Notification / integration** — None; the desk sees the error and must settle first.
6. **Final result** — Checkout is refused until the cashier settles the folio (bill preview → `SettleBill` → `Save_Folio`, writing `BillSettlementDetails` and stamping `InvoiceNo`). After settlement, checkout proceeds normally.

**Expected result:** The system guarantees no guest leaves with an open folio; the balance must be settled (or transferred to a company/master folio, use case 8) first.

**Error scenarios:** open `FolioHeader` → `UnsettledBills`; unsettled POS bill (SS003) → *"There are unsettled restaurant bills for …"* (note: the referenced pre-check SP `Reservations_W_ValidatePOSBill_AtCheckout` is **Not found in Browns**; when SS003 is off the check is skipped).

---

## Use case 6 — Split payment

**Scenario:** A guest settles one invoice partly by cash and partly by card.

1. **User action** — Cashier opens the folio, previews the bill, and enters **multiple payment lines** (e.g. LKR 20,000 cash + LKR 15,000 VISA), then settles.
2. **System validation** — `CalculateFolioChargersToBill` returns the `BillPaymentView` (net + taxes + discounts); the settlement object accepts a **list** of payment lines.
3. **Database change** — `FolioService.SaveBill` → `Save_Folio` writes **one `BillSettlementDetails` row per payment line** (each with its `PaymentTypeID`, `PaidAmount`, currency), stamps the `InvoiceNo`, and settles the folio.
4. **Related module update** — FX gain/loss captured in `BillSettlementDetails.ConRateGainOrLoss`; foreign amounts in `PaidAmountInFc`; folio marked `IsLock`.
5. **Notification / integration** — Fiscal invoice via `FiscalPrinter_FolioInvoice`; online card portion may use Sampath IPG.
6. **Final result** — The invoice is fully settled across several payment types; balance goes to zero (or a residual if under-paid — a partial payment leaves the folio with a positive balance).

**Expected result:** A single bill is settled by any mix of cash / card / bank / voucher and currencies, each as its own settlement row.

**Error scenarios:** under-payment → folio retains a positive balance (add another `BillSettlementDetails` line); settling a locked folio → reopen first (`VoidSettledFolios_T_Update`).

---

## Use case 7 — Refund

**Scenario:** An advance/deposit is refunded (e.g. cancelled reservation, or over-payment).

1. **User action** — Cashier opens *Advance Cancellation* (`AdvanceCancelationController`), selects the reservation and the advance to reverse, chooses a refund payment type, and confirms; at reservation cancellation the refund popup is `RefundAtReservationCancellation`.
2. **System validation** — Page access; the advance must exist and not already be reversed.
3. **Database change** — `SaveCancelAdvancePayment` → `AdvancePaymentService.SaveCancelAdvance` → **`Advance_Payment_Cancellation_T_Save`** reverses the advance posting and processes the refund via the chosen `RefundPaymentTypeId`.
4. **Related module update** — The guest-ledger column `DepositRefund` captures the refund at day-end; folio balance adjusts.
5. **Notification / integration** — Cash/card refund handled at the cashier; online (IPG) advances were taken via Sampath IPG. (A dedicated **automated gateway refund/void call** is not evidenced — refund is recorded through the advance-cancellation SP; the IPG request/response handlers are largely stubbed in this checkout, doc 11.)
6. **Final result** — The advance is reversed and the refund recorded; the reversal appears in `DayEndSummaryGuestLedger.DepositRefund` and `DayEndSummary.DepositRefunds`.

**Expected result:** Deposits can be reversed/refunded and are reflected on the guest and property ledgers.

**Error scenarios:** advance already reversed → blocked; **post-settlement invoice refunds** are handled instead by **credit notes** (`CreditOrDebitNote_InvoiceNoWiseDetails_Save`, DRCR = C), not by this advance-refund path.

---

## Use case 8 — Posting a restaurant charge to a room

**Scenario:** A guest in room 320 orders in the restaurant and closes the bill as "Bill to Room".

1. **User action** — The bill is closed in the POS (or the outlet cashier fills the *Profit-Centre Wise Posting* screen), selecting the room, item(s), quantity, charge type, tax group, and **Bill to Room**.
2. **System validation** — PMS checks: day-end not running (`DayEndDayEndStepCompletion`); the room has an **in-house** reservation (`InHouseReservationDetails`); reservation not `IsStopPosting`; valid `ChargeCodeId`/`PostingTypeId`/tax group.
3. **Database change** — Tax computed (`ProfitCenter_TaxCalculations` / `TaxCalculations`). Charge row → `ExtraPostingDetails` (incl. tax, `IsBillToRoom = 1`, `RefDocNo`), taxes → `ExtraPostingDetailWiseTaxes`, POS txn rows → `ProfitCenter_txn*` (manual path), settlement `BILL TO ROOM` → `ExtraPostingSettlements`. Document numbers `PRC…`/`INV…` via `UpdateNextDocNoWithUpdate`.
4. **Related module update** — **`Insert_Folio`** appends the charge to the guest's live `FolioHeader`/`FolioDetails` (+ folio taxes) so the outstanding balance rises; `Dayend_RevenueAndOccupancySummary_Executions_M_Save` updates summaries.
5. **Notification / integration** — The POS receives a JSON `ApiResponse` (`HttpCode 200` + document no); `RestaurantOrderNo` links the folio line back to the POS order. Entry points: `Administration/POSApi/SaveInHousePOSAPIPosting` → `Posting_InHouse_T_Save`, or `ProfitcenterWisePosting_M_Save`.
6. **Final result** — The restaurant charge is a line on the guest folio, payable at checkout; the outlet revenue is recorded.

**Expected result:** Outlet consumption reaches the room bill via `Insert_Folio`, fully taxed and GL-coded.

**Error scenarios:** day-end running → *"Day end is processing…"*; `IsStopPosting` reservation → *"Reservation marked as stop posted"*; room not in-house → falls back to walk-in handling (no folio line). POS-internal ordering/KOT is **Not found in the project (separate `Categlog_vrV2` DB)**.

---

## Use case 9 — Reservation cancellation

**Scenario:** A future (not-yet-arrived) booking is cancelled.

1. **User action** — Agent opens `CancelReservationController` (page `5509`), `CancelReservationByHeaderId` (single) or `CancelReservationByGroupResNo` (group), selects a cancellation reason and enters a remark; submits.
2. **System validation** — Page access; a valid reason from `CancellationReasons` (e.g. `6 Guest Cancellation`, `8 OTA Booking Cancellation`).
3. **Database change** — `CancelReservationService.Save` → **`CancelReservation_M_Save`** sets `StatusId = BookingSettings.BookingCancelStatusId` (**Cancelled = 1**); writes `CancelledReservationLog`; deletes `ReservationWiseInventoryAllocation`.
4. **Related module update** — If attached to an allotment, rooms returned via `Reservation_T_RemoveAllotments`; revenue/occupancy summary re-executed; filtration columns refreshed.
5. **Notification / integration** — Inserts `CMUpdateRanges` (`proccessID='A'`) so freed inventory is pushed back to OTAs; OTA-originated bookings also call `RateTiger_Reservation_API_Cancel`.
6. **Final result** — Booking is Cancelled, disappears from active lists, inventory freed.

**Expected result:** A cancelled reservation frees its rooms and pushes availability back to the channel manager.

**Error scenarios:** an already **checked-in** guest cannot be cancelled — they are checked out instead. **Automatic monetary cancellation penalty is Not found in the project** (`CancellationPolicies` holds textual terms only); any charge is a manual folio posting.

---

## Use case 10 — No-show

**Scenario:** A guaranteed booking's guest never arrives and is marked No-Show at night audit.

1. **User action** — During day-end, the night auditor runs *Update No-Shows* (`DayEndProcessController.UpdateNoShows`) which marks reservations that never arrived. (There is **no dedicated single "mark-as-no-show" FO endpoint** — Not found in the project; No-Show is applied via the day-end/status mechanism.)
2. **System validation** — Only unarrived, not-checked-in reservations for the closing hotel date qualify; No-Show status is `BookingSettings.NoShowStatusId = 2`.
3. **Database change** — `Reservations_T_UpdateNoShow` sets the reservation `StatusId = 2 (No-Show)` (`ReservationStatus.IsNoshow = 1`).
4. **Related module update** — Like Cancelled, No-Show is excluded from occupancy; the day summary counts it (`DayEndSummary.NoShow`).
5. **Notification / integration** — Freed inventory (if the reservation held rooms) is reflected in availability/occupancy recompute.
6. **Final result** — The reservation is terminal (No-Show); any no-show charge is posted manually to a folio.

**Expected result:** Unarrived guaranteed bookings are cleanly retired as No-Show during night audit and counted in the day summary.

**Error scenarios:** a No-Show charge/penalty is **not auto-posted** — **Not found in the project** (manual folio posting only, doc 03/04).

---

## Use case 11 — Early checkout

**Scenario:** A guest departs before the recorded departure date.

1. **User action** — If the shortened stay changes the rate/room-nights, FO first runs *Change Stay* (`Reservations.ChangeStaySave`) with an early-departure reason (`2 Early Departure With Charge` or `3 Early Departure Without Charge`); then does the normal Quick Check-Out.
2. **System validation** — Change Stay: mandatory reservation/reason/remark/meal-plan/room-type/company/rate-code validation; **blocked while day-end is in progress** (`DayEndDayEndStepCompletion` must be empty). Checkout: the `UnsettledBills` gate still applies.
3. **Database change** — `Reservation_T_ChangeStaySave` adjusts `InHouseReservationDetails` room-nights and the folio accordingly (logs to `StayChange_ProcessTimeConsum_Log`). Checkout: `Reservation_T_QuickCheckOutUpdate` migrates `Inhouse* → CheckedOut*`; when hotel date ≠ calendar date it auto-stamps remark *"Early checkout: confirmed"*.
4. **Related module update** — `'CKO'` → room FO **2061 Vacant** / HK **2034 Vacant Dirty**; occupancy recompute.
5. **Notification / integration** — Door key revoke; `RabbitMQ_GuestCheckOut`; Guest Portal post-stay email.
6. **Final result** — The bill is shortened, settled, and the guest checks out; **no automatic early-departure fee** is posted by the SP.

**Expected result:** An early departure is handled as (optional) change-stay adjustment + normal checkout; the shortened bill must be settled first.

**Error scenarios:** change-stay during day-end → blocked; open folio at checkout → `UnsettledBills`. There is **no separate "early checkout" controller** (Not found in the project — it is the ordinary quick checkout).

---

## Use case 12 — Late checkout

**Scenario:** A guest stays past the standard checkout time on the departure day.

1. **User action** — Late departure is represented on the stay via `ExpectedDepartureTime` / `LeaveAfter` (set on the reservation and carried into `InhouseReservationHeaders` at check-in). At departure, FO runs the normal Quick Check-Out on the departure hotel date.
2. **System validation** — Standard checkout validation (`UnsettledBills` gate, room-night/folio-night reconciliation).
3. **Database change** — `Reservation_T_QuickCheckOutUpdate` migrates `Inhouse* → CheckedOut*` as usual.
4. **Related module update** — `'CKO'` housekeeping status; occupancy recompute.
5. **Notification / integration** — `ExpectedDepartureTime`/`LeaveAfter` are passed to the door-lock/PABX events (key validity/time).
6. **Final result** — The guest checks out; any late-checkout charge is a **manual** folio posting.

**Expected result:** Late checkout is a normal checkout with the late-departure time recorded on the stay.

**Error scenarios:** **automatic late-checkout fee is Not found in the project** — `Reservation_T_QuickCheckOutUpdate` posts no late fee; there is **no distinct late-checkout transaction** (doc 04).

---

## Use case 13 — Room maintenance issue (Out of Order)

**Scenario:** Room 118's AC fails; engineering blocks it out of sale for repair.

1. **User action** — Maintenance/HK opens *Out-of-Order TXN* (`OutOfOrderTXNController`, page `4166`), picks the room(s), from/to dates, a reason (e.g. *AC REPAIR*), and the target/release status; saves.
2. **System validation** — `OutOfOrderTXN_M_Insert` requires ≥1 room, rejects `FromDate ≥ ToDate`, and **blocks conflicts**: refuses if the room in that range is already OOO, in-house-allocated (`InhouseReservationDetails`), or future-allocated (`ReservationDetails`).
3. **Database change** — Inserts `OutOfOrderTXN` (`RoomId, FromDate, ToDate, OutOfOrderReasonId, OutOfOrderStatusId, ReleaseAsId, …`).
4. **Related module update** — Calls `HouseKeeping_ProcessWiseStatusChanges_Update 'OOO'` (or `'OOS'`) → room FO **2067 Out of Order/Service**, HK **2044 Out of Order** / **2045 Out of Service**. Availability (`RoomAvailability_R_Select`) subtracts OOO rooms from sellable inventory for every blocked date.
5. **Notification / integration** — Pushes `Staah_AvailabilityPush` for each affected date so OTAs stop selling the room.
6. **Final result** — The room is out of inventory for the block; when the period ends / on `QuickDeleteRoomWise`, it returns to the `ReleaseAsId` HK status.

**Expected result:** A maintenance room is safely held out of sale, cannot be reserved or checked into, and is invisible to OTAs for the blocked dates.

**Error scenarios:** `FromDate ≥ ToDate` → *"Invalid date range."*; room reserved/in-house → *"Room already allocated to …"*; overlapping block → *"Room already has been out of order."*

---

## Use case 14 — Day-end cashier closing (night audit)

**Scenario:** The night auditor closes the trading day.

1. **User action** — Auditor runs the pre-check (`CheckValidations`), verifies room rates (`RoomRateCheck` → `RoomRateSave`), marks No-Shows (`UpdateNoShows`), then runs `CompleteDayEnd` (page `6001`).
2. **System validation** — `CheckDayEndValidations` requires: no pending expected arrivals (`DayEnd_FrontOffice_Check`), pseudo-room check, room rates verified (`DayEnd_RoomRates_Check`), POS orders settled/signed/uploaded, GL reachable. Day-end will not run while any check fails.
3. **Database change** — `DayEnd_CompleteDayEnd` runs ordered steps (from `DayEnd_CompleteDayEnd_SP_ExecutionSteps`): FX lock on first night; remove unconfirmed folios; **auto room posting `Reservation_T_FolioWisePostingBreakUp_Save`** (→ `FolioWisePostingBreakUp`); GL prep (`Dayend_GL_*`); guest ledger (`DayEndSummaryGuestLedger`); room status; property summary (`DayEndSummary`). Each step guarded/recorded in `DayEndDayEndStepCompletion` (idempotent/resumable).
4. **Related module update** — Housekeeping status changes (DND/dirty on departure); OOO rooms whose block expired are released; next day's folio headers created.
5. **Notification / integration** — Day-end GL/kitchen data pushed to `Categlog_vrV2` (`DayEndGL_Posting`, `POS_spInsertKitchenIssues`); daily revenue-report email job queued.
6. **Final result** — `DayEnd_UpdateHotelDate` advances `FOSettings.CurrentDate` by one day; the guest ledger and property summary are produced.

**Expected result:** The trading day is closed, room revenue posted, ledgers produced, and the hotel date rolled forward — safely resumable if interrupted.

**Error scenarios:** validation fails → `"ERR-Dayend validation(s) fail."` (nothing committed); a step exception → logged to `GEN_ErrTable`, step narration recorded, `"ERR-<message>"` returned; on Browns, real-time external GL post is inactive (`CallGLSps` commented out — Not found in the project).

---

## Use case 15 — Resending an invoice

**Scenario:** A guest asks for their final invoice (or GRC) to be sent again after checkout.

1. **User action** — Staff opens *Document Delivery* (`DocumentDeliveryController`), selects the reservation, the document type (e.g. `7 Final Invoice`, `8 GRC`, `1 Reservation Confirmation`, `6 Outstanding Statement`) and a sending method (`1 Email`, `2 WhatsApp`), and saves to send.
2. **System validation** — Document types from `HKDocumentTypes_Select`; methods from `HK_Select_DocumentSendingMethods`; the settled-bill data is read via `InvoiceDetails_M_SelectForCheckedOutReservations`.
3. **Database change** — `SaveDocumentToDeliver` → `DocumentSendService.SaveDocumentToDeliver` → **`HK_Save_DocumentToDeliver`** queues the document for delivery.
4. **Related module update** — The invoice/registration document itself is rendered by SSRS (e.g. `Report_Guest_Registration` for the GRC); the final invoice comes from the settled folio (`BillSettlementDetails`, `InvoiceNo`).
5. **Notification / integration** — Email dispatch via SMTP/`BEMailSender` (external worker; `IsMailEnabled` config); WhatsApp — see gap below.
6. **Final result** — The document is queued and (for email) dispatched by the external sender; the guest receives the invoice again.

**Expected result:** Any previously produced document can be re-queued and re-sent from Document Delivery by email or WhatsApp.

**Error scenarios:** the actual **email send worker (`BEMailSender`) and WhatsApp dispatcher are Not found in this checkout** — documents are only **queued** (`HK_Save_DocumentToDeliver`); the send/retry runs in an external worker (doc 11). See use case 17.

---

## Use case 16 — Guest signature synchronization

**Scenario:** The guest signs on a signature pad at check-in and the signature is stored against the guest profile (so it follows the guest across stays).

1. **User action** — At registration the desk captures the guest signature on the GRC screen.
2. **System validation** — The signature is attached to the **guest profile**, not the reservation, so it is reused across future stays.
3. **Database change (intended)** — `ReservationHeaderEntry.SaveSignature(reservationNo, signature)` calls SP **`Reservation_T_SaveSignature`** (`@ReservationNo`, `@Signature`) to persist into table **`GuestProfileWiseGuestSignature`** (`GuestProfileId`, `GuestSignature`, `CreatedDateTime`).
4. **Related module update** — Check-in / checkout / room-change SPs copy `GuestSignature` fields between the header tables as the stay migrates; the GRC (`Report_Guest_Registration`) prints the signature.
5. **Notification / integration** — None external; the signature image is stored in-DB (table) / Azure Blob for document images.
6. **Final result (with gap)** — The signature *table* exists and is used indirectly, **but the SP `Reservation_T_SaveSignature` is Not found in `HotelResWeb_Browns`** (queried `sys.objects`). On this property the save-via-this-path would fail, so signature "sync" through this code path is **not deployable here**.

**Expected result (intended):** A captured signature is saved once against the guest profile and reused/printed across the guest's stays.

**Error scenarios / gap:** **`Reservation_T_SaveSignature` Not found in the project (Browns)** — the C# reference exists, the procedure is not deployed; the signature save via this path errors on this DB (docs 02 §N, 04).

---

## Use case 17 — Sending documents through WhatsApp

**Scenario:** Staff sends a confirmation/invoice to the guest via WhatsApp.

1. **User action** — In *Document Delivery*, staff selects the document type and chooses **WhatsApp** (`2`) as the sending method, then saves.
2. **System validation** — WhatsApp is a valid `HK_Select_DocumentSendingMethods` option (`2 WhatsApp`); the document type and reservation are validated as in use case 15.
3. **Database change** — `SaveDocumentToDeliver` → **`HK_Save_DocumentToDeliver`** writes the document to the delivery queue with method = WhatsApp.
4. **Related module update** — The rendered document (SSRS) is the payload; for the guest-app path, `GuestPortal_Save_VButlerInvitationToDeliver` is used when `ReservationType == "vButler"`.
5. **Notification / integration (intended)** — An external sender (`FrontOffice.SMSSender` / `BEMailSender` / a WhatsApp worker) would pick up the queue and dispatch.
6. **Final result (with gap)** — The document is **queued only**. **No WhatsApp API endpoint, config, or dispatch code exists in this checkout** — the actual WhatsApp send is **Not found in the project** (doc 11). So on this checkout the WhatsApp option records intent but does not itself send.

**Expected result (intended):** WhatsApp delivery of guest documents by queuing them for an external WhatsApp dispatcher.

**Error scenarios / gap:** **WhatsApp send implementation Not found in the project** — only the "sending method" option and the delivery queue exist; there is no dispatcher/endpoint/credentials in this MVC checkout (doc 11).

---

## Summary — features fully evidenced vs flagged gaps

| # | Use case | Status |
|---|---|---|
| 1 | Walk-in booking → checkout | Fully evidenced (no one-click walk-in super-action) |
| 2 | Online reservation → check-in | Evidenced; channel endpoints/retry external (Not found) |
| 3 | Group booking | Fully evidenced |
| 4 | Room change | Fully evidenced |
| 5 | Checkout with outstanding balance | Fully evidenced (`UnsettledBills` gate) |
| 6 | Split payment | Fully evidenced |
| 7 | Refund | Evidenced (advance-cancel); automated gateway refund not evidenced |
| 8 | Restaurant charge to room | Fully evidenced (`Insert_Folio`); POS-internal in `Categlog_vrV2` (Not found) |
| 9 | Reservation cancellation | Evidenced; auto penalty Not found |
| 10 | No-show | Evidenced (day-end); auto charge Not found, no dedicated FO endpoint |
| 11 | Early checkout | Evidenced (change-stay + checkout); auto fee Not found |
| 12 | Late checkout | Evidenced (time fields + normal checkout); auto fee Not found |
| 13 | Room maintenance (OOO) | Fully evidenced |
| 14 | Day-end closing | Fully evidenced; external real-time GL post inactive |
| 15 | Resending an invoice | Evidenced (queued); email/WhatsApp send worker external |
| 16 | Guest signature sync | **Gap**: `Reservation_T_SaveSignature` not deployed in Browns |
| 17 | WhatsApp document send | **Gap**: WhatsApp dispatcher Not found in the project |

## Related documents

- `01-complete-hotel-process.md` — the end-to-end lifecycle these use cases instantiate.
- `02`/`03`/`04` — front office, reservation, check-in/out internals.
- `05`/`06`/`07` — cashiering/day-end, rooms/housekeeping, F&B/POS.
- `11-integrations-and-data-flow.md` — payment gateway, channel manager, fiscal printer, SMS/email/WhatsApp, RabbitMQ, SSRS, Azure, SSO, POS DB.

---

### "Not found in the project" items (consolidated)

- **`Reservation_T_SaveSignature`** — referenced in `ReservationHeaderEntry.cs`, not deployed in `HotelResWeb_Browns` (use case 16).
- **WhatsApp send implementation / dispatcher** — only a queued "sending method"; no endpoint/config/code (use cases 15, 17).
- **`Reservations_W_ValidatePOSBill_AtCheckout`** — referenced by the checkout POS pre-check, not deployed in Browns (use case 5).
- **Automatic penalties/fees** — cancellation penalty, No-Show charge, early-departure fee, late-checkout fee are all manual folio postings, not auto-computed (use cases 9–12).
- **One-click walk-in super-action** — walk-in is create → allocate → quick-check-in with source Walk-in (use case 1).
- **Dedicated mark-as-No-Show FO endpoint** — applied via day-end/status mechanism (use case 10).
- **Channel-manager API endpoints/credentials & automatic retry** — external worker (use case 2).
- **Automated payment-gateway refund/void call** — refund recorded via advance-cancellation SP; IPG request/response handlers largely stubbed here (use case 7).
