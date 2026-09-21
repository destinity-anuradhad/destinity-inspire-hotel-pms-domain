# 14 — Business Rules & Validations

> **Product:** Scienter HotelERP — Destinity Inspire / Destinity Horizon Front Office (Hotel PMS)
> **Scope:** A consolidated, cited catalog of every enforced business rule and validation in the Front Office application — mandatory fields, date/availability/rate/tax/amount validations, status-transition rules, payment/settlement restrictions, cancellation and check-in/checkout restrictions, permission-gated sensitive actions, duplicate-prevention, and the operational error messages with their causes.
>
> Every rule below cites its enforcement point: a `.cs` file (controller / service / `*Entry` / model), a stored procedure (SP), or a database table. All SP error text was read from the **live `HotelResWeb_Browns`** database (`10.4.1.180`) via `OBJECT_DEFINITION`. Where a rule could not be confirmed it is marked **"Not found in the project"** with a note on where we looked.
>
> **Read alongside:** `03-reservation-process.md`, `04-check-in-check-out-process.md`, `05-cashiering-and-finance-process.md`, `06-rooms-and-housekeeping-process.md`, `07-fnb-and-outlet-process.md`, `09-user-roles-and-permissions.md`, `12-database-and-technical-architecture.md`.

---

## Purpose

The PMS is a modular monolith where **the vast majority of business rules live in stored procedures**, not in application code. Of 2,889 procedures in the live DB, **488 contain `RAISERROR`** and 5 contain `THROW` — the rules are enforced server-side, atomically, inside `BEGIN TRAN … CATCH … ROLLBACK` blocks that log to `GEN_ErrTable`. The MVC layer adds a thin outer ring: `[VerifyLoggedUser]` (authentication) and `[UserWisePageAccess(pageId, "S|I|U|D")]` (authorization) action filters, plus some client-side jQuery validation. This document catalogs those rules.

## Relevant users / departments

Reservations agents, Front Office / Reception, Cashiers, Night Auditors, Housekeeping, Finance, and System Administrators — each constrained by the permission model (doc 09) and the validations below.

## Preconditions

- A logged-in user (`SessionObjects.LoggedUser`) scoped to a `PropertyId` (multi-tenant).
- The property has a current hotel date (`FOSettings.CurrentDate`), a `BookingSettings` row, and `DocumentNumbers` series.
- Master data (rooms, rates, tax groups, payment types, charge codes) configured in Administration.

---

## Where validation is enforced (the three rings)

| Ring | Mechanism | Evidence |
|---|---|---|
| **1. Authentication** | `[VerifyLoggedUser]` filter redirects unauthenticated requests | `WebUIMvc/Controllers/BaseController.cs` |
| **2. Authorization** | `[UserWisePageAccess(pageId, "S/I/U/D")]` → SP `UserAccess_M_AccessPermission` (deny-by-default) | `BaseController.cs`; `Common.Data/UserWiseIndividualAccessEntry.cs`; doc 09 |
| **3. Business validation** | `RAISERROR` / branch logic inside stored procedures (488 SPs) | e.g. `Reservation_T_Save_New`, `Save_Folio`, `Reservation_T_QuickCheckInUpdate` |

> **Key architectural fact (verified):** transaction/operational models such as `ReservationHeader.cs` carry **no `[Required]` attributes** — mandatory-field enforcement for reservations, guests, check-in and postings is done **entirely in the SPs**. Only master-data models (e.g. `Company.cs`, `Country.cs`, `MealPlan.cs`, `PackageHeader.cs`) use `[Required]`/`[Display]` DataAnnotations for client/model validation (78 domain files contain `[Required]`, 106 occurrences). This split is called out as a risk in doc 15.

---

## 1. Mandatory fields (per key screen)

### 1a. Guest profile (at check-in gate — server-enforced)

The guest **profile is validated at check-in**, not at profile creation. `Reservation_T_QuickCheckInUpdate` refuses check-in unless the main guest (`GuestProfileTypeId = 1`) is real:

| Field | Rejected placeholder / default | Enforced by (verified SP text) |
|---|---|---|
| First / Middle / Last name | `TBA`, `-` | `SET @Error = ' Guest profile is not completed, please update TBA values.'` / `… please update - values.` |
| Nationality | `1025` (default), `0` | same check-in SP |
| Country | `1`, `258` (defaults), `0` | same |
| Salutation | `6` (default) | same |
| Email (`CommunicationTypeId = 2`) | `-`, `tba`, `TBA@TBA.COM` | `SET @Error = ' Guest profile is not completed, please update - or tba mail values.'` |

> `GuestProfile.cs` itself has **no** `[Required]` attributes (verified) — so a TBA/placeholder profile can be *saved*, but *cannot be checked in*. Passport/NIC auto-classification: a value containing `v` → local `IdNum`, otherwise `PassportNo` (`GuestProfiles_M_Save_OnReservationCreation`, doc 03).

### 1b. Reservation (Make Reservation → `Reservation_T_Save_New`)

| Mandatory condition | Rule | Enforced by (verified) |
|---|---|---|
| Room rate must exist for Category + Type + Meal Plan + dates | else reservation rejected | `RAISERROR('104-No Room Rates for the selected Meal Plan, Room Type & Room Category. Are you want to place this reservation as tentative?',16,1)` |
| Room category & meal plan | `RoomCategoryId`/`MealPlanId` ≠ 0 required at check-in | `Reservation_T_QuickCheckInUpdate`: `SET @Error = 'Update room category and meal plan.'` |
| Sales person (when configured mandatory) | required | `Reservation_T_Save_New`: `RAISERROR('Please select a sales person..',16,1)` |
| Property scope | every reservation stamped `PropertyId` from session | `ReservationCreationController` / `ReservationHeaderEntry` |

### 1c. Posting (extra charge → `Posting_InHouse_T_Save` / `ProfitcenterWisePosting_M_Save`)

| Mandatory condition | Enforced by (verified) |
|---|---|
| GL mapping present for the charge | `Posting_InHouse_T_Save`: `RAISERROR('Please complete GL mapping.',16,1)` |
| Valid charge code / posting type / tax group | resolved from `ProfitCenters`/`PostingTypes`; error if missing |
| Day-end not running | `RAISERROR('Day end is processing, you are not allowed to do postings.',16,1)` |

### 1d. Settlement (Settle Bill → `Save_Folio`)

| Mandatory condition | Enforced by (verified) |
|---|---|
| At least one payment type selected | `RAISERROR('Please select at least one payment type before settling the bill.', 16, 1)` |
| No unposted extra-posting bills outstanding | `RAISERROR('There are unposted extra posting bills for this reservation, Please contact administrator',16,1)` |
| Bill total = settlement total | `RAISERROR('Bill total and settlement total mismatch. …',16,1)` / `RAISERROR('Folio total and settlement total mismatch.',16,1)` |
| Valid settlement amount | `RAISERROR('Invalid settlement amount',16,1)` / `RAISERROR('Invalid settlement. Please refresh and try again.', 16, 1)` |
| Day-end not running | `RAISERROR('Day end is processing, you are not allowed to do settlement.',16,1)` |

### 1e. Advance payment (`Advance_Payment_T_Save`)

| Mandatory condition | Enforced by (verified) |
|---|---|
| Room / record must exist | `RAISERROR('Room not found. Please contact scienter.',16,1)` / `RAISERROR('No record exists.',16,1)` |
| Day-end not running | `RAISERROR('Day end is processing, you are not allowed to do advance postings.',16,1)` |

### 1f. Out-of-Order block (`OutOfOrderTXN_M_Insert`)

| Mandatory condition | Enforced by (verified) |
|---|---|
| At least one room selected | `RAISERROR('Please select at least one room to continue.',16,1)` |
| `FromDate < ToDate` | `RAISERROR('Invalid date range.',16,1)` |
| `FromDate ≠ ToDate` | `RAISERROR('The From and To dates cannot be the same.',16,1)` |

---

## 2. Validation rules (dates, availability, rate, tax, amounts)

| # | Rule | Where enforced (verified) |
|---|---|---|
| V1 | **Availability / overbooking**: at reservation save, a final per-category availability re-check blocks oversold categories (`Available X, Requested Y`). | `Reservation_T_Save_New` (overbooking guard); computed by `RoomAvailability_R_Select`: `Available = ActualRooms − (ReservationCount + OOOCount + RoomBalance)` |
| V2 | **OOO/OOS rooms removed from sellable inventory** for every blocked date (`OOOCount` from `OutOfOrderTXN`). | `RoomAvailability_R_Select`; `06-rooms-and-housekeeping-process.md` |
| V3 | **Rate must exist** for Category+Type+MealPlan+dates or reservation rejected (unless placed tentative). | `Reservation_T_Save_New` (error `104`) |
| V4 | **Zero-rate block at check-in** on chargeable, occupancy-bearing rooms (`IsComplimentary=0 AND ConciderForOccupancy=1`). | `Reservation_T_QuickCheckInUpdate`: *"Update the room rates before the check-in process."* |
| V5 | **Arrival = hotel date** required to check in; **checkout date = hotel date** required to check out (actual rooms). | check-in/checkout SPs: *"… is not in current hotel date"* |
| V6 | **Room-night ↔ folio-night reconciliation** at checkout (accommodation `ChargeCodeID = 6` count ≥ room-nights). | `Reservation_T_QuickCheckOutUpdate`: *"… mismatch between room nights and folio nights…"* |
| V7 | **Taxes are always derived, never typed free-hand** — every folio charge carries a `TaxGroupID`; taxes expanded by SP. | `TaxCalculations`, `ProfitCenter_TaxCalculations`, `Folio_T_CalculateTaxTaxGroupWise`; stored in `FoliowiseTaxDetails` |
| V8 | **Tax-inclusive vs tax-on-top** driven per property by `FOSettings.IsTaxInclusiveExtraPosting`; inclusive back-computes net (`Amount / TaxBreakValue`), on-top grosses up. | `ProfitcenterWisePosting_M_Save`, `GetOriginal_PostingAmount` |
| V9 | **FX gain/loss** captured on multi-currency settlement (`ConRateGainOrLoss`, `PaidAmountInFc`). | `BillSettlementDetails`; `Save_Folio` |
| V10 | **First-night FX rate locked** at day-end. | `Dayend_ChangeConvertionOn_FirstNight` (inside `DayEnd_CompleteDayEnd`) |
| V11 | **OOO block cannot overlap** an existing block, an in-house allocation, or a future reservation. | `OutOfOrderTXN_M_Insert`: *"Room already has been out of order." / "… allocated to an Inhouse reservation." / "… allocated to a reservation."* |

---

## 3. Status-transition rules

### 3a. Reservation status (`ReservationStatus`, 6 live values)

| Id | Name | AllowInMakeReservation | AllowedToCheckIn | ApplicableToOccupancy | Terminal |
|---|---|:--:|:--:|:--:|:--:|
| 3 | Confirmed | ✔ | ✔ | ✔ | |
| 4 | Tentative | ✔ | | | |
| 5 | Inquiry | ✔ | | | |
| 6 | Waitlisted | ✔ | | | |
| 1 | Cancelled | | | | ✔ |
| 2 | No-Show | | | | ✔ |

Rules (from `ReservationStatus` columns + `BookingSettings`, doc 03):
- **Only Confirmed (3)** counts toward occupancy, is allowed to check in, and writes room-rate rows on save.
- **Approve-as-tentative** switches status → `BookingSettings.BookingTentitiveStatusId (4)` and rate → tentative default (`Reservation_T_Save_New`).
- **Cancelled (1)** and **No-Show (2)** are terminal; they free inventory and push a `CMUpdateRanges` channel-manager update.

```
 RESERVATION STATUS TRANSITIONS
                 approve-as-tentative
   ┌────────────┐  ◄─────────────────  ┌───────────┐   allocate room    ┌──────────────┐
   │ Tentative  │ ───────────────────► │ Confirmed │ ─────────────────► │ Room Alloc.  │
   │   (4)      │                      │   (3)     │                    └──────┬───────┘
   └────────────┘                      └─────┬─────┘                           │ QuickCheckIn
   Inquiry (5) ─┐                            │                                 │ (Reservation_T_
   Waitlisted(6)┴──────────────────────────► │                                 ▼ QuickCheckInUpdate)
                (allowed in make-reservation) │                       copies to InhouseReservation*
                                              │                                 │ deletes Reservation*
              cancel ◄────────────────────────┼──────────────► No-Show (2)      ▼
              Cancelled (1)                    │                (night audit)  IN-HOUSE ─► checkout
              + CMUpdateRanges push            │                                        Inhouse* ─►
              (blocked if settled bills)       │                                        CheckedOut*
```

> **Cancellation guard (verified):** `CancelReservation_M_Save`: `RAISERROR('Cancel is not allowed. There are settled bills.',16,1)` — a reservation with settled bills cannot be cancelled.

### 3b. Room status (unified `RoomStatus` master, category-driven)

Only **`22 Vacant Inspected`** has `IsAllowCheckIn = 1` **and** `IsAllowRoomChange = 1` (verified by live query — it is the *sole* row returned). Every other HK status blocks check-in and room change. Status changes are always mediated by `HouseKeeping_UpdateRoomStatus`; event→status mapping is data-driven via `HouseKeeping_ProcessWiseStatusChanges` and `FrontOfficeStatusWiseHouseKeepingStatus`.

Process-code targets (verified, doc 04/06):

| Process | Trigger | FO status | HK status |
|---|---|---|---|
| `CKI` | Check-in | 2050 Occupied | 2030 Occupied Clean |
| `CKO` | Check-out | 2061 Vacant | **2034 Vacant Dirty** |
| `RCGO` / `RCGN` | Room change old / new | 2061 Vacant / 2050 Occupied | 2034 Vacant Dirty / 2030 Occupied Clean |
| `OOO` / `OOS` | Out of Order / Service | 2067 Out of Order/Svc | 2044 / 2045 |

```
 ROOM (HOUSEKEEPING) STATUS TRANSITIONS
                              check-in (CKI)                       check-out (CKO)
                                   │                                    │
   ┌──────────────┐  clean   ┌────────────┐  inspect  ┌────────────────▼───┐
   │ Vacant Dirty │ ───────► │ Vacant     │ ────────► │ Vacant Inspected   │  IsAllowCheckIn=1
   │   (2034)     │          │ Clean(2033)│           │      (22)          │ ─► SELLABLE / check-in
   └──────┬───────┘          └────────────┘           └────────────────────┘
          ▲                                                    │ allocate + CKI
          │ checkout leaves room dirty                         ▼
          │                                            ┌────────────────┐  guest in-house
          └────────────────────────────────────────── │ Occupied (2030 │  (FO = Occupied 2050)
                                                       │ Clean / 6 Dirty│
                                                       └────────────────┘
   ── OUT-OF-ORDER (any status) ──────────────────────────────────────────────
      OutOfOrderTXN save (OOO/OOS): validates no reservation/no overlap, From<To
        └► Out of Order (2044) / Out Of Service (2045)  → removed from availability
           on ReleaseAs / QuickDelete → returns to ReleaseAsId HK status
```

### 3c. Folio / bill states

| State | Meaning | Set / cleared by | Effect |
|---|---|---|---|
| Open folio | `FolioHeader` row exists | created at check-in (`Reservation_T_FolioCreation`) | **blocks checkout** (see §5) |
| Settled / locked | `FolioHeader.IsLock = 1` + stamped `InvoiceNo` | `Save_Folio` | no further postings until reopened |
| Reopened / voided | un-settle a closed bill | `VoidSettledFolios_T_Update` | folio postable again (before day-end only) |

---

## 4. Payment restrictions (settlement, over-payment, currency, advance)

| # | Restriction | Enforced by (verified) |
|---|---|---|
| P1 | Cannot settle without a payment type. | `Save_Folio`: *"Please select at least one payment type…"* |
| P2 | Settlement total must equal bill total (no over/under mismatch committed). | `Save_Folio`: bill/folio-total-mismatch RAISERRORs |
| P3 | **Under-payment** leaves a positive folio balance (partial payment) — an additional `BillSettlementDetails` row is needed; the invoice stays open. | `Save_Folio` / `BillSettlementDetails`; doc 05 |
| P4 | Split / multi-currency settlement supported (list of payment lines; FX gain/loss captured). | `Save_Folio`; `BillSettlementDetails.ConRateGainOrLoss`, `PaidAmountInFc` |
| P5 | Cannot post/settle to a **locked** folio (must reopen via void). | `FolioHeader.IsLock`; `VoidSettledFolios_T_Update` |
| P6 | No settlement / posting / advance while **day-end is running**. | `Save_Folio`, `Posting_InHouse_T_Save`, `ProfitcenterWisePosting_M_Save`, `Advance_Payment_T_Save` (all guard `DayEndDayEndStepCompletion`) |
| P7 | Advance is posted as a folio **credit** (`DRCR='C'`) using `BookingSettings.ChargeCodeAdvancedPayments`. | `Advance_Payment_T_Save`; doc 03/05 |
| P8 | Bill-to-room only for an **in-house** reservation that is **not** `IsStopPosting`. | `ProfitcenterWisePosting_M_Save`, `Posting_InHouse_T_Save`: `RAISERROR('Reservation marked as stop posted',16,1)` |
| P9 | **No automatic over-payment refund / change** logic beyond `BalanceGiven`; a genuine over-collection remains a manual reversal (advance cancellation / credit note). | `BillSettlementDetails.BalanceGiven`; no dedicated SP found (searched settlement SPs) |

> **A dedicated "block over-payment" validation was Not found** — `Save_Folio` enforces *mismatch* between bill and settlement totals but the modelled path is exact settlement plus `BalanceGiven` (change). Over-collection is corrected via advance/credit-note flows.

---

## 5. Cancellation, check-in & checkout restrictions

### Cancellation
- Sets `StatusId = 1 (Cancelled)`, writes `CancelledReservationLog` (reason + remark), frees inventory (`ReservationWiseInventoryAllocation` delete), returns allotment rooms (`Reservation_T_RemoveAllotments`), pushes `CMUpdateRanges` to OTAs. (`CancelReservation_M_Save`, doc 03.)
- **Blocked if settled bills exist**: `RAISERROR('Cancel is not allowed. There are settled bills.',16,1)`.
- **No automatic monetary cancellation penalty** — `CancellationPolicies` stores textual terms only; any charge is a manual folio posting. (**Not found in the project** — searched `CancelReservation_M_Save`, `CancellationPolicies`.)

### Check-in restrictions (all in `Reservation_T_QuickCheckInUpdate`)
Allocated room + `RoomStatus.IsAllowCheckIn = 1` (only Vacant Inspected) + status Confirmed + complete guest profile (no TBA/`-`/defaults) + arrival = hotel date + non-zero rate on chargeable rooms + room not already occupied + category & meal plan set.

### Checkout restrictions (`Reservation_T_QuickCheckOutUpdate`)
- **Open folio blocks checkout**: `IF EXISTS(SELECT 1 FROM FolioHeader WHERE ReservationHeaderID IN (@Temp)) → RAISERROR('UnsettledBills',16,1)`. Settle the folio first.
- **Unsettled POS/restaurant bills** block checkout when `SystemSettings SS003` is enabled (controller pre-check `ValidateRestaurantBillStatus`; see doc 15 — its intended SP `Reservations_W_ValidatePOSBill_AtCheckout` is **not deployed**, verified via `sys.objects`).
- Room-night ↔ folio-night reconciliation (V6); checkout date = hotel date.
- **No automatic early/late-checkout fee** (early checkout only auto-stamps *"Early checkout: confirmed"*). (**Not found** — searched checkout SP + `BookingSettings`.)

---

## 6. Permission-based restrictions (sensitive actions)

Sensitive operations are gated by a dedicated `PageId` + right (`S/I/U/D`) via `[UserWisePageAccess]` → `UserAccess_M_AccessPermission` (deny-by-default), so a user can *view* a folio yet be denied *void/discount* on it (doc 09).

| Sensitive action | Gating / evidence |
|---|---|
| **Discount** | own `PageId`/right; SP family `GL_POSTING_FO_DISCOUNT`, `FolioChargers_T_Save_Discount`. Authorisation list via `Discount_SelectAuthorizedUsersToApproveDiscounts`. |
| **Void posting** | separate right; `ExtraPostings_T_Void`, `ExtraPosting_T_Void_ByDocumentNo`; fiscal re-void `BaseController.FiscalPrinter_VoidPosting`. |
| **Void settled folio** | `VoidSettledFolios_T_Update`: `RAISERROR('Access denied.',16,1)` if not authorised. |
| **Rebate / allowance** | `GL_POSTING_FO_REBATE`, `DirectRebate`. |
| **Refund** | `GL_POSTING_FO_ADVANCE_REFUND`; `Advance_Payment_Cancellation_T_Save`. |
| **Day-end / night audit** | restricted to Night/Income Auditor / Finance / Admin via page permission; `DayEnd_CompleteDayEnd`, `DayEnd_UpdateHotelDate`. |
| **Rate override** | rate-change gated; `Reservation_T_RoomRate_Update_SpPara`. |
| **Cashier re-auth** | `Login/CashierLoginVerify` + `ValidatePasswordOnPopup` before sensitive cashier actions. |

Sensitivity classification masters (`SensitivityLevels`: Normal/Medium/High; `SeverityLevels`) flag data for higher-privileged handling (doc 09).

---

## 7. Duplicate prevention

| Mechanism | How | Evidence |
|---|---|---|
| **Document-number generation** | Atomic, property-prefixed, zero-padded running numbers issued inside the save SP — no client-supplied numbers. Codes: `RESNO`, `GRRESNO`, `GRC`, `PRC`, `INV`. | `UpdateNextDocNoWithUpdate 'RESNO'/…`; `DocumentNumbers` (Code, Prefix, Length, NextNo) |
| **Voucher-number duplicate check** | reservation save blocks duplicate voucher unless user approves. | `Reservation_T_Save_New`: `RAISERROR('105-Voucher number already exist. Do you want to continue?',16,1)`; `IsApproveVoucherNumberDuplication` |
| **Duplicate username** | checked before user save. | `UsersController` → `User_M_Select_ByUserName` (doc 09) |
| **Guest / company de-dup search** | `GuestProfiles_Search` and search SPs surface existing profiles for reuse before creating new. | `ReservationCreation/SearchGuest`; `GuestProfiles_Search` table |
| **Physical FK integrity** | only **79 FKs** in the DB — most relationships are *logical* joins in SP code, so referential-duplicate prevention relies on SP logic, not constraints. | `sys.foreign_keys`; doc 12 (risk in doc 15) |

> A hard **unique constraint / index guaranteeing one active profile per NIC/passport was Not found** — de-duplication is search-assisted, not constraint-enforced (searched guest indexes). See doc 15.

---

## 8. Error messages & their causes (verified from live SP bodies)

| Message text (verbatim) | Trigger / cause | Where (SP / controller) |
|---|---|---|
| `104-No Room Rates for the selected Meal Plan, Room Type & Room Category. Are you want to place this reservation as tentative?` | No rate for selection at reservation save | `Reservation_T_Save_New` |
| `105-Voucher number already exist. Do you want to continue?` | Duplicate voucher number | `Reservation_T_Save_New` |
| `Please select a sales person..` | Sales person required but missing | `Reservation_T_Save_New` |
| `Error in reservation insert. Source -> DB-RH/RP/RPS, Level -> 01/02/04.` | Header/profile insert failure | `Reservation_T_Save_New` |
| `Sorry, there is an issue in placing the reservation. Category(s) overbooking. (Category Available X, Requested Y)` | Category oversold at save | `Reservation_T_Save_New` (doc 03) |
| `Cancel is not allowed. There are settled bills.` | Cancelling a reservation with settled bills | `CancelReservation_M_Save` |
| `Update the room rates before the check-in process.` | Zero rate on chargeable room | `Reservation_T_QuickCheckInUpdate` |
| `The room allocated for <ResNo> is already in occupied.` | Room already in-house | `Reservation_T_QuickCheckInUpdate` |
| `The room allocated for <ResNo> is not in allowed housekeeping status to checkin.` | HK status not Vacant Inspected | `Reservation_T_QuickCheckInUpdate` |
| `Reservation is not ready to be checked-in.Please check the reservation status.` | Status not check-in-able | `Reservation_T_QuickCheckInUpdate` |
| `Guest profile is not completed, please update TBA / - / - or tba mail values.` | Placeholder guest data | `Reservation_T_QuickCheckInUpdate` |
| `Check in date of reservation <ResNo> is not in current hotel date` | Arrival ≠ hotel date | `Reservation_T_QuickCheckInUpdate` |
| `Update room category and meal plan.` | Category/meal plan = 0 | `Reservation_T_QuickCheckInUpdate` |
| `<Room> - Room still appearing in the inhouse level for another reservation. Please checkout the existing one and try again.` | Room still in-house elsewhere | `Reservation_T_QuickCheckInUpdate` |
| `UnsettledBills` | Open `FolioHeader` at checkout | `Reservation_T_QuickCheckOutUpdate` |
| `Check out date of room <Room> is not in current hotel date` | Checkout date ≠ hotel date | `Reservation_T_QuickCheckOutUpdate` |
| `There is a mismatch between room nights and folio nights…` | Folio nights < room nights | `Reservation_T_QuickCheckOutUpdate` |
| `There are unsettled restaurant bills for …` | POS bills open (SS003 on) | `QuickCheckOutController.ValidateRestaurantBillStatus` |
| `Day end is processing, you are not allowed to do postings / settlement / advance postings.` | Any transaction during open day-end step | `Posting_InHouse_T_Save`, `ProfitcenterWisePosting_M_Save`, `Save_Folio`, `Advance_Payment_T_Save` |
| `Reservation marked as stop posted` | Posting to a stop-posting reservation | `Posting_InHouse_T_Save`, `ProfitcenterWisePosting_M_Save` |
| `Please complete GL mapping.` | Missing GL account mapping for charge | `Posting_InHouse_T_Save` |
| `Error in inserting restaurent bill to folio.` | Folio insert failure on POS bill | `Posting_InHouse_T_Save` |
| `There are unposted extra posting bills for this reservation, Please contact administrator` | Un-posted extra postings at settlement | `Save_Folio` |
| `Please select at least one payment type before settling the bill.` | No payment line at settlement | `Save_Folio` |
| `Bill total and settlement total mismatch. …` / `Folio total and settlement total mismatch.` | Settlement ≠ bill total | `Save_Folio` |
| `Invalid settlement amount` / `Invalid settlement. Please refresh and try again.` | Bad settlement amount | `Save_Folio` |
| `Void Posting not allowed after day end.` | Voiding after day-end | `ExtraPostings_T_Void` |
| `Void Posting not allowed. Document(s) %s already settled.` | Voiding a settled document | `ExtraPostings_T_Void` |
| `Void Posting not allowed. (Transferred folio exists . Please reinstate it to the previous state).` | Voiding a transferred folio | `ExtraPostings_T_Void` |
| `Void fail. Cannot void after the dayend.` / `Access denied.` / `Invalid invoice no to void !` | Void-settled-folio guards | `VoidSettledFolios_T_Update` |
| `Room not found. Please contact scienter.` / `No record exists.` | Advance to unknown room/record | `Advance_Payment_T_Save` |
| `Requested date and hotel dates are miss matching. Please re-login to the system and try again.` | Day-end date mismatch | `DayEnd_CompleteDayEnd` |
| `Please select at least one room to continue.` / `Invalid date range.` / `The From and To dates cannot be the same.` | OOO block validation | `OutOfOrderTXN_M_Insert` |
| `Room already has been out of order.` / `… allocated to an Inhouse reservation.` / `… allocated to a reservation.` | OOO conflict | `OutOfOrderTXN_M_Insert` |
| `ERR-Dayend validation(s) fail.` | Day-end pre-check failed | `DayEndProcessController.CompleteDayEnd` |
| `ERR-<message>` / `Error -<message>` (generic) | Any caught service/SP exception | controllers' `catch` blocks |
| HTTP 403 `{ Message:"You don't have permission…", Error:"Unauthorized" }` | Page/action not permitted (AJAX) | `BaseController.OnAuthorization` |

---

## Business rules summary (numbered)

1. Every reservation, folio and posting is scoped to the session `PropertyId` (multi-tenant).
2. A rate must exist for the selection or the reservation is rejected (error 104) unless placed tentative.
3. Only **Confirmed** reservations count to occupancy, write rate rows and may check in.
4. Category overbooking is blocked at save; OOO/OOS rooms are removed from availability.
5. Check-in requires an allocated room in **Vacant Inspected** HK status, Confirmed status, a complete guest profile, arrival = hotel date and non-zero rate on chargeable rooms.
6. Room status is automatic per event (CKI/CKO/RCG/OOO) and only **Vacant Inspected** re-allows check-in / room change.
7. **Checkout is blocked by any open folio** (`UnsettledBills`) and by unsettled POS bills when SS003 is on — settle first.
8. Cancellation is blocked when settled bills exist; there is no automatic monetary cancellation penalty.
9. No posting, settlement or advance is allowed while day-end is running.
10. Taxes are always derived from a tax group; inclusive/on-top is a per-property setting.
11. Settlement requires a payment type and total-equality; split/multi-currency supported; locked folios must be reopened first (before day-end).
12. Void/discount/rebate/refund/day-end/rate-override are permission-gated per page + right (deny-by-default).
13. Document numbers are issued atomically server-side; duplicate vouchers and usernames are guarded.

## Expected result

Front-office actions succeed only when all mandatory data is present, dates/availability/rates/taxes/amounts are valid, the actor holds the required permission, and no conflicting state (open folio, day-end running, settled bill, occupied room) exists — otherwise the SP raises a precise, catalogued error and rolls back.

## Error scenarios

See §8 (each verbatim message with trigger and enforcing SP/controller).

## Related documents

- `03-reservation-process.md`, `04-check-in-check-out-process.md`, `05-cashiering-and-finance-process.md`, `06-rooms-and-housekeeping-process.md`, `07-fnb-and-outlet-process.md` — the workflows these rules govern.
- `09-user-roles-and-permissions.md` — the permission ring (`UserWisePageAccess`).
- `12-database-and-technical-architecture.md` — SP conventions, transactions, audit.
- `15-known-issues-and-improvement-suggestions.md` — where these rules are weak, missing or duplicated.

---

### "Not found in the project" items

- **Automatic monetary cancellation penalty** — `CancellationPolicies` holds text only; no penalty computation in `CancelReservation_M_Save`.
- **Automatic early-check-in / late-checkout fee** — none posted by check-in/checkout SPs.
- **Hard over-payment block** — `Save_Folio` enforces total-equality + `BalanceGiven` (change), not an explicit over-collection reject.
- **Unique constraint for one profile per NIC/passport** — de-duplication is search-assisted, not constraint-enforced (only 79 FKs; searched guest indexes).
- **`Reservations_W_ValidatePOSBill_AtCheckout`** (checkout POS gate) — referenced in code but not deployed in `HotelResWeb_Browns` (verified `sys.objects`). See doc 15.
