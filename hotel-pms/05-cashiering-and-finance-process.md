# Cashiering & Finance Process

> Scienter HotelERP — Destinity Inspire Front Office. Module area: `Areas/CashieringAndPosting`.
> Every controller action, service method, `*Entry` method, stored procedure and table named below was read from the actual source code and verified against the live `HotelResWeb_Browns` database. Where something could not be confirmed it is marked **"Not found in the project"** with a note on where it was checked.

## Purpose

The cashiering and finance module records every **money movement** that happens against a guest stay and turns it into an auditable bill. It is **folio-centric**: each in-house reservation owns one or more **folios** (bill windows), charges (postings) accumulate on those folios during the stay, taxes/discounts are calculated on them, and at check-out the folio is converted into an **invoice** and **settled** with one or more payment types. The **day-end (night audit)** batch closes the trading day, auto-posts the room charge for the night, produces the guest-ledger trial balance, and advances the hotel date.

## Relevant users / departments

| Role | Uses |
|---|---|
| Front-office cashier | Postings, folio management, bill settlement, currency encashment, advances |
| Night auditor | Day-end process, room-rate verification, no-show update |
| Finance / accounts | Credit & debit notes, GL ledger (day-end GL SPs), audit trail |
| Reservations | Advance payments / deposits at booking |
| F&B / POS outlets | Profit-centre / module-category charges routed to guest folios |

## Preconditions

- User is authenticated (SSO / `VerifyLoggedUser`) and has the relevant `UserWisePageAccess` right (e.g. `4129` advance payment, `6001` day-end, `9189` advance cancellation).
- The property has a current **hotel date** (`SessionObjects.FOSettings.CurrentDate`) — postings are stamped with it.
- For in-house postings the reservation must be **checked in** (in-house) and have a **FolioHeader** (created on check-in, or on demand by `Folio_U_CreateFolioHeaderIfNotExists`).
- Tax groups, tax types, payment types, charge codes and profit centres are configured in Administration.

---

## Cashiering workflow overview (folio-centric)

```
                          ┌─────────────────────────────────────────────┐
   RESERVATION            │              GUEST STAY (in-house)           │
   ┌──────────┐  check-in │  ┌──────────┐   charges     ┌────────────┐   │
   │ Advance/ │──────────▶│  │FolioHeader│◀────postings──│ Posting    │   │
   │ Deposit  │           │  │ (bill     │   (FolioDetails)│(InHouse/  │   │
   │Advance_  │           │  │  window)  │               │ WalkIn)    │   │
   │Payment_  │           │  └────┬──────┘               └────────────┘   │
   │T_Save    │           │       │                                       │
   └──────────┘           │       │  ◀── Room charge (auto @ day-end)     │
                          │       │        Reservation_T_FolioWise-       │
                          │       │        PostingBreakUp_Save            │
                          │       │  ◀── F&B / POS  (ProfitCentre →       │
   ┌──────────┐           │       │        ProfitcenterWisePosting_M_Save)│
   │ Extra    │           │       │  ◀── Discounts (FolioDiscount_T_Update│
   │ services │──────────▶│       │        / FolioChargers_T_Save_Discount│
   └──────────┘           │       │  ◀── Taxes   (FoliowiseTaxDetails,    │
                          │       │        TaxCalculations SP)            │
                          │       ▼                                       │
                          │  ┌───────────────┐  CalculateFolioChargersTo- │
                          │  │ Bill preview  │  Bill (BillPaymentView)     │
                          │  └───────┬───────┘                            │
                          │          │ settle                             │
                          │          ▼                                    │
                          │  ┌───────────────┐  Save_Folio →              │
                          │  │  SETTLEMENT   │  BillSettlementDetails      │
                          │  │ cash/card/    │  + InvoiceNo generated      │
                          │  │ bank/IPG      │                            │
                          │  └───────┬───────┘                            │
                          └──────────┼──────────────────────────────────-─┘
                                     ▼
                          ┌─────────────────────────┐
                          │   DAY-END / NIGHT AUDIT  │  DayEnd_CompleteDayEnd
                          │  auto room posting,      │  → DayEndSummaryGuestLedger
                          │  guest ledger, room      │  → DayEndSummary
                          │  status, hotel date +1   │  → DayEnd_UpdateHotelDate
                          └─────────────────────────┘
```

### Core tables (verified — `HotelResWeb_Browns`)

| Table | Role | Key columns (verified via `sys.columns`) |
|---|---|---|
| `FolioHeader` | The bill window per room/reservation | `FolioHeaderID`, `ReservationHeaderID`, `RoomID`, `FolioNo`, `InvoiceNo`, `FolioAddress`, `FolioCompanyName`, `IsLock` |
| `FolioDetails` | Individual charge lines (postings) | `FolioDetailID`, `FolioHeaderID`, `PostingTypeID`, `ChargeCodeID`, `ChargeDate`, `ChargeAmount`, `DRCR`, `TaxGroupID`, `CurrencyID`, `ConvertionRate`, `IsComplimentory`, `IsDirectRoomPosting`, `RefFolioDetailID`, `TransferRefFolioDetailID` |
| `FoliowiseTaxDetails` | Tax lines for each folio charge | `FolioTaxID`, `FolioDetailID`, `TaxID`, `Percentage`, `Amount`, `TaxName`, `AccountCode`, `CurrencyId` |
| `FolioWiseDiscount` | Folio-level / total discounts | `ReservationHeaderID`, `FolioNo`, `isPercentage`, `isValue`, `Amount`, `Description`, `PostingTypeId` |
| `FolioWisePostingBreakUp` | Posting breakup used by revenue/GL & day-end | `ReservationHeaderId`, `FolioNo`, `Date`, `ChargeCodeId`, `Amount`, `PostingTypeId`, `AccountCode`, `RoomTypeId`, `MealPlanId`, `Segmentcode` |
| `BillSettlementDetails` | Payments applied to settle a bill | `ID`, `ReservationHeaderID`, `InvoiceNo`, `PaymentTypeID`, `PaidAmount`, `BalanceGiven`, `SettlementDate`, `CurrencyId`, `PaidAmountInFc`, `ConRateGainOrLoss` |
| `BillHeader` / `BillTrans` | POS (restaurant) order header / lines | `OrderNo`, `Subtotal`, `Discount`, `ServiceCharge`, `TaxVal1..4`, `TDL`, `RoomCode`, `BilltoAgent` |
| `BillToRoomLog` | Text audit log of bill-to-room / transfers | `LogText`, `SysDate`, `PropertyId` |
| `PaymentTypes` | Payment-method master | `PayCode`, `Description`, `Cash`, `CreditCard`, `Credit`, `AccCode`, `VOUCHER` |

> Layering convention: **Controller** (`Areas/CashieringAndPosting/Controllers/*Controller.cs`) → **Service** (`FrontOffice.Service/*Service.cs`) → **Entry / repository** (`Common.Data/*Entry.cs`) → **stored procedure** → **tables**. The `*Entry` classes usually serialise the domain object to JSON and pass it to a single SP.

---

## Folio creation & charges (postings)

### What a folio is
A **folio** is a numbered bill window attached to a reservation+room (`FolioHeader`). A guest can have several folios (e.g. folio 1 = own account, folio 2 = company/master, folio 3 = incidentals). Charges live in `FolioDetails`, taxes in `FoliowiseTaxDetails`, and their revenue breakup in `FolioWisePostingBreakUp`. The folio header is auto-created if missing by SP `Folio_U_CreateFolioHeaderIfNotExists` (verified in `db_procs`).

### Flow 1 — Post an extra charge to an in-house guest (manual posting)

**Controller:** `PostingController` · **Action:** `POST SaveInHouse(Posting posting)`
`Areas/CashieringAndPosting/Controllers/PostingController.cs`

1. **User action** — Cashier picks the in-house room, a **posting type / charge code** (e.g. Laundry, Mini-bar, Telephone), an amount, currency and tax group, then saves.
2. **System validation** — Controller checks logged user / page access; the amount, currency, and reservation are validated; the invoice type may be validated via `Validate_Invoice_Type`.
3. **Database change** — `PostingService.SaveInHousePosting(posting)` → `PostingEntry.SaveInHousePosting(...)` serialises to JSON and calls SP **`Posting_InHouse_T_Save`** (verified in DB). This writes to `FolioDetails` (the charge line), `FoliowiseTaxDetails` (its taxes) and `FolioWisePostingBreakUp`.
4. **Related module update** — Tax breakup is computed via the tax engine (see *Taxes*); revenue breakup rows feed reporting and day-end GL.
5. **Notification / integration** — An invoice/bill preview can be printed via `Posting_Bill_Preview`; fiscal print via `FiscalPrinter_FolioInvoice` (see *Fiscal printer*).
6. **Final result** — The charge appears on the guest folio and increases the outstanding balance.

### Flow 2 — Walk-in posting (no reservation)

**Controller:** `PostingController` · **Action:** `POST SaveWalkIn(Posting posting)`
→ `PostingService.SaveWalkInPosting` → `PostingEntry.SaveWalkInPosting` → SP **`Posting_WalkIn_T_Save`** (verified). Used for a casual/ walk-in guest (name + address held on the posting) who pays immediately; payment modes travel in the same posting object.

### Flow 3 — Rebate / negative posting & void

| Action (PostingController) | Service method | Stored procedure | Meaning |
|---|---|---|---|
| `POST RebatePosting` | `SaveInHousePosting` (negative amount) | `Posting_InHouse_T_Save` | Reduce/allowance a charge |
| `GET DirectRebate` | `PostingService.DirectRebateBill` | `DirectRebate` (verified) | Direct rebate of a specific folio line |
| `GET VoidPosting` / `DeletePosting` | `PostingService.ExtraPostingVoid` | `ExtraPostings_T_Void` (verified) | Void an extra posting |
| `GET GetAllVoidedPostings` | — | `VoidExtraPosting_T_Select_CurrentDate` | List today's voids (audit) |

> Extra-posting later-settlement is supported via `ExtraPostingSettlements_LaterSettlements_T_Settle` / `..._T_SelectToSettle` (actions `SaveLaterSettlement`, `ExtraPostingsToSettle`, `LoadPendingExtraPostingsToSettle`).

### Room charges — auto night posting vs manual

- **Automatic (normal path):** The nightly **room charge** is NOT posted by the cashier — it is posted by the **day-end** process. During `DayEnd_CompleteDayEnd`, step *"Inserting Folio Wise Posting BreakUp"* calls **`Reservation_T_FolioWisePostingBreakUp_Save`** per in-house reservation (verified inside the SP body). This posts the accommodation charge (room rate × night) for the closing day into the folio/breakup tables. Rates used are the ones **verified** in the day-end **Room Rate Check** step.
- **Manual room posting:** `FolioDetails.IsDirectRoomPosting` marks a directly-posted room charge (rare, e.g. rate correction) as opposed to the auto night audit posting.

---

## Restaurant / F&B & POS charges (Profit-centre → folio)

Two routes bring outlet charges onto a guest folio:

### Route A — Profit-centre-wise posting (direct outlet charge to folio)

**Controllers:** `ProfitCenterWisePostingController` / `Profit_CenterWise_PostingController` · **Action:** `Save`
→ `Profit_CenterWise_PostingService.Save(...)` → `Profit_CenterWise_PostingEntry.Save(...)` → SP **`ProfitcenterWisePosting_M_Save`** (verified).

- The posting carries three JSON blocks: `ProfitcenterDetailsJson` (items & amounts), `TaxDetailsJson` (taxes) and `PaymentDetailsJson` (payments).
- `BillToRoomCheck` decides whether the charge is **billed to the guest room folio** (bill-to-room) or paid at the outlet; `IsComplementary` marks it free of charge.
- Taxes for the outlet charge are computed by `GetTaxes_ProfitCenter` → SP **`ProfitCenter_TaxCalculations`** (verified).
- POS master data lives in `Core_ProfitCenters`, `Core_ProfitCenterItems`, `Core_ProfitCenterItemCategories`, `Core_ProfitCenterChargePrices`; the transaction lands in `Core_ProfitCenterTransactionHeader` / `...Detail` / `...Tax` / `...Payment` (all verified tables).

### Route B — Module-category-wise transaction

**Controller:** `ModuleCategoryWiseTXNController` · **Actions:** `SelectReservationNumbersByType`, `ModuleCategoryWiseTXNSave`
→ `ModulePostingService` / `ModuleCategoryWiseTXNEntry` → SP **`ModuleCategoryWiseTXN_T_Save`** (verified). Module masters: `ModuleCategories`, `ModuleCategoryWiseItem` (config saved via `ModuleCategories_M_Save`). Used for inventory-linked outlet items charged to a reservation.

### Unbilled POS pickup
SP **`Folio_PostUnbilled_POS_Bills`** (verified) sweeps unbilled POS bills onto folios (also referenced by day-end).

### Laundry-wise posting
**Controller:** `LaundryWisePostingController.Save` → `LaundryWisePostingService` → SP `LaundryWisePosting_M_Save` (from `data_sps.json`). Laundry has its own tax group (`LAUNDRYTAX-DONOTREMOVE`, verified in `TaxGroups`).

---

## Discounts

**Controller:** `DiscountController` (`Index`, `ApplyDiscount`, `SaveDiscount`, `RemoveDiscount`) and `FolioManagementController` (`FolioDiscount`, `FolioDiscountSave`).

| Purpose | Path | Stored procedure (verified) |
|---|---|---|
| List discountable folio lines | `FolioService.FilterTransactionsByFolioNoForDiscount` | `FolioChargers_T_Select_For_Discount` |
| Save line-level discounts | `DiscountController.SaveDiscount` → `FolioService.SaveDiscount` → `FolioEntry.SaveDiscount` | `FolioChargers_T_Save_Discount` |
| Remove a line discount | `DiscountController.RemoveDiscount` → `FolioEntry.RemoveDiscount` | `FolioChargers_T_Cancel_Discount` |
| Folio/total discount (value or %) | `FolioManagementController.FolioDiscountSave` → `FolioService.FolioDiscount` → `FolioEntry.FolioDiscount` | `FolioDiscount_T_Update` |

- The `Discount` domain object carries `DiscountType` (value vs percentage), `DiscountAmount`, `ChargeAmount`, `DiscountRemark`.
- Total (folio-wide) discounts persist to `FolioWiseDiscount` (`isPercentage` / `isValue` flags, verified columns). `isTotalDiscount` on the action distinguishes total vs per-line.
- Only charge codes flagged discountable are offered (`ChargeCodeService.SelectDiscountableCharegCodes`).

---

## Taxes & service charges

**Controller:** `TaxCalculationController` — actions `GET GetTaxes`, `POST GetOriginalBillValue`, `GET GetTaxes_ProfitCenter` (verified by reading the file).

### How the Sri-Lanka tax model is configured (verified data in `HotelResWeb_Browns`)

- **`TaxTypes`** — individual taxes with a `Rate`. Live examples: `Service Charge 10%` (10%), `VAT` (18%), `SSCL` (2.56%), `TDL 1%` (1%), `NBT`, `No TAX`. `IsCalculateFromBaseAmount` controls whether the tax applies to the base amount or on top of prior taxes (compounding).
- **`TaxGroups`** — named bundles of tax types with a pre-computed `TaxBreakValue` multiplier. Live examples: `SC + SSCL + VAT` (multiplier `1.33128…`), `SC + VAT` (`1.298`), `SSCL + VAT` (`1.2102…`), `NONTAX` (`1.0`), `LAUNDRYTAX-DONOTREMOVE`.
- **`TaxGroupDetails`** — the link table (`TaxGroupId` → `TaxTypeId`, with `OrderId` for compounding order).
- Property scoping via `TaxGroupWiseProperties` / `TaxTypeWiseProperties`.

### How tax is applied to a charge

1. Every folio charge (`FolioDetails.TaxGroupID`) points at a tax group.
2. `GetTaxes(TaxGroupAmontJson, ResId, FolioNo, Operation)` → `TaxCalculationService.GetTaxes` → SP **`TaxCalculations`** (verified) expands the group into individual tax lines.
3. `GetOriginalBillValue` → SP **`GetOriginal_PostingAmount`** (verified) back-calculates the tax-exclusive base from a tax-inclusive amount (needed when prices are quoted gross).
4. Resulting tax lines are stored in **`FoliowiseTaxDetails`** (one row per `TaxID` per `FolioDetailID`, with `Percentage`, `Amount`, `TaxName`, `AccountCode`).
5. Tax-group-wise recomputation on the whole folio is done by SP **`Folio_T_CalculateTaxTaxGroupWise`** (verified).

### Tax removal (tax-exempt guests)
`FolioManagementController` actions `RemoveTax` / `ApplyTaxRemoval` → `FolioService.ApplyTaxRemoval` → `FolioEntry.ApplyTaxRemoval` → SP **`Save_TaxRemoval`** (verified). Removed taxes are archived in `TaxRemovedFoliowiseTaxDetails` / `TaxRemovedFolioWiseTaxDetailItems`; policies live in `TaxRemovalPolicies` (all verified tables). Guest-ledger column `TaxRemoval` captures the effect at day-end.

---

## Deposits / advances

Advances are money taken **before** or **during** the stay (deposits) and later offset against the bill.

**Controller:** `AdvancedPaymentController` (`Landing`, `ReservationList`, `SaveAdvancePayment`, `SaveAdvancePaymentLink`, `SelectAdvancePaymentCurrencies`, `GetAdvancedPaymentDetails`).

1. **User action** — Reservations/cashier selects a reservation and records an advance amount (multi-currency supported).
2. **System validation** — Page access `4129`; advance charge config loaded via `GetAdvancedPaymentDetails` → SP **`AdvancedPyment_Charges_T_Select`** (verified: returns `AdpTaxId`, `AdpPostingCatgId`, `AdpChargeCodeId`, `AdpPostingTypeId`).
3. **Database change** — `POST SaveAdvancePayment(Posting)` → `AdvancePaymentService.Save` → `AdvancePaymentEntry` → SP **`Advance_Payment_T_Save`** (verified). Returns a `RoomInvoiceView` with the advance document number.
4. **Related module update** — Currencies come from `SelectAdvancePaymentCurrencies`; the advance later offsets the folio balance at settlement.
5. **Notification / integration (online advance link)** — `POST SaveAdvancePaymentLink` → SP **`OnlineAdvancePayment_Insert`** (verified) creates a UUID payment link stored in `AdvanceRequestHeaders` (columns `GUID`, `DocNo`, `Amount`, `CurrencyCode`, `Email`, verified) with related tables `AdvanceRequestOnline`, `AdvanceRequestOnlinePayment`, `AdvanceRequestOnlinePaymentResponse`, `AdvanceRequestOnlineEmails`. The guest pays through the IPG gateway and the response is written back (`AdvanceRequestOnlinePaymentResponse_T_Save`).
6. **Final result** — Advance is recorded as a credit/deposit; shown as `Deposits` on the guest ledger at day-end.

### Advance cancellation / refund
**Controller:** `AdvanceCancelationController` — `ReservationListForCancelAdvance`, `InHouseReservationListForCancelAdvance`, `SelectAdvanceForReservationCancellation`, `POST SaveCancelAdvancePayment`, `RefundAtReservationCancellation`.
→ `AdvancePaymentService.SaveCancelAdvance` → SP **`Advance_Payment_Cancellation_T_Save`** (verified). Reverses the advance posting and processes the refund via the chosen `RefundPaymentTypeId`. Guest-ledger column `DepositRefund` captures it.

---

## Payment types & settlement

### Payment methods (live `PaymentTypes` rows in `HotelResWeb_Browns`)

| PayCode | Description | Flags |
|---|---|---|
| `C` | CASH | `Cash=1` |
| `BR` | BILL TO ROOM | `NoValue=1` (routes to room, no cash) |
| `01` | VISA / MASTER | `CreditCard=1` |
| `02` | AMEX | `CreditCard=1` |
| `03` | STAFF DEBTOR | `Credit=1` |
| `CL` | T.AGENT | `Credit=1` (travel-agent debtor) |
| `05`/`06`/`08` | D.Bank Acc … | bank deposit accounts |
| `07` | GAIN AND LOSS | FX gain/loss |
| `12`/`13` | HO – CASH / HO – Credit Cards | head-office |

`PaymentTypes` columns include `Cash`, `CreditCard`, `Credit`, `NoValue`, `cheque`, `VOUCHER`, `AccCode` (GL mapping), `DrawerOpen`.

Payment channels covered:
- **Cash / card / bank / cheque / voucher** — via `PaymentTypes` at settlement.
- **Online (IPG)** — Sampath Internet Payment Gateway (`Scienter.HotelERP.FrontOffice.IPG`, `SampathIPGController`), used for advance links and online settlement.
- **Currency encashment** — foreign-cash exchange (below).
- **Split / partial payments** — the settlement object accepts a **list** of payment lines, so a single invoice can be settled by several `BillSettlementDetails` rows (part cash + part card, or partial payment leaving a balance).

### Bill preview & settlement flow

**Controller:** `FolioManagementController`
`Areas/CashieringAndPosting/Controllers/FolioManagementController.cs`

1. **User action** — Cashier opens the folio, reviews charges (`FolioDetails`, `FolioChargers_T_Select`) and requests a **bill preview**.
2. **System validation** — `CalculateBillTotal` → `FolioService.CalculateBillTotal` → SP **`CalculateFolioChargersToBill`** (verified) returns a `BillPaymentView` (net + taxes + discounts).
3. **Database change** — On **SettleBill**, `FolioService.SaveBill` → `FolioEntry.SaveBill` → SP **`Save_Folio`** (verified). This writes payment lines to **`BillSettlementDetails`**, stamps the **`InvoiceNo`** on `FolioHeader`, and locks/settles the folio.
4. **Related module update** — FX gain/loss captured in `BillSettlementDetails.ConRateGainOrLoss`; foreign amounts in `PaidAmountInFc`.
5. **Notification / integration** — Invoice can be printed/emailed; fiscal invoice via `FiscalPrinter_FolioInvoice`.
6. **Final result** — Folio becomes a settled invoice; balance goes to zero (or remains as a partial balance if under-paid).

### Group / multiple-folio settlement
- `GroupSettlementSave` → SP **`Save_MultipleFolio`** (verified) settles several rooms' folios together.
- Merge variants `Merge_MultipleFolio` / `Save_Merged_MultipleFolio` are **referenced in `FolioEntry.cs`** but the procedures were **not found in the live `HotelResWeb_Browns` database** (checked `sys.procedures`); they may exist only in other property databases / a merge feature not deployed to Browns.

### Managing settled folios / void settlement
`ManageSettledFolios`, `LoadManageSettledFolios`, `VoidSettledFoliosByRoom` → `FolioService.VoidSettledFolios` → SP **`VoidSettledFolios_T_Update`** (verified) reverses a settled folio (un-settles a mistakenly closed bill).

---

## Transfer between folios / charge routing

All under `FolioManagementController`; each Entry method serialises to JSON and calls one SP (all verified in DB):

| Business action | Action(s) | Service → SP |
|---|---|---|
| Move whole folio charges to another room (route to master/company folio) | `RoomToRoomTransfer` / `RoomToRoomTransferSave` | `FolioService.RoomToRoomTransfer` → `Folio_T_RoomToRoomTransfer` |
| Move selected line items to another room | `LineItemTransfer` / `LineItemRoomToRoomTransferSave` | `FolioService.LineItemRoomToRoomTransferSave` → `Folio_T_LineItemRoomToRoomTransfer` |
| Split one charge across folios/amounts | `ItemSplit` | `FolioService.ItemSplit` → `Folio_T_ItemSplit` |
| Swap folio numbers | `ExchangeFolio` | `FolioService.ExchagenFolioNos` → `FolioNoExchange_T_Update` |
| Renumber charges to a different folio | `ChangeFolioNumber` | `FolioService.ChangeFolioNumber` → `FolioNumberChange_T_Update` |
| Split reservation into folios | `FolioSplitWiseReservation(Save)` | `FolioSplit_T_Update` |
| Change bill-to company/customer name | `ChangeCompanyAndCustomerName` / `SaveCompanyAndCustomerName` | `FolioInvoice_T_ChangeGuestAndCompanyName` |
| Remove transferred folios | `RemoveTransferedFolios` | `Folio_T_RemovePostingInRecords` |

- Transfer linkage is tracked on `FolioDetails` via `RefFolioDetailID`, `TransferRefFolioDetailID`, `OriginalTransferRefFolioDetailID`.
- `BillToRoomLog` holds a plain-text audit trail of bill-to-room / transfer events.
- Routing a charge to a **company / master folio** is done by transferring line items to the folio that carries `FolioCompanyName` (company account).

---

## Credit notes / debit notes

Post-settlement adjustments to a closed invoice.

**Current controller:** `CreditOrDebitNotesNewController` — `index`, `SelectDetailsByReservationOrInvoiceNo`, `Grid_FoliDetails`, `Save_FolioDetails`.

| Step | Path | Stored procedure (verified) |
|---|---|---|
| Find a settled invoice | `CreditOrDebitNotesNewService.SelectDetailsByReservationOrInvoiceNo` | `CreditOrDebitNote_BillSettlementDetails_Select_ByReservationNoOrInvoiceNo` |
| Load its folio lines | `SelectFolioDetailsByInvoiceNo` | `CreditOrDebitNote_SettledFolioDetails_Select_ByInvoiceNo` |
| Save credit/debit adjustment | `Save_FolioDetails` | `CreditOrDebitNote_InvoiceNoWiseDetails_Save` |

- The line VM carries `DRCR` / `CreditOrDebit` (C = credit note reduces the invoice, D = debit note increases it) and `AdjustableAmount`.
- **Legacy path** (`DebitAndCreditNotesService`): `SaveCreditNote` → SP `CreditNotes_T_Save`; `SaveDebitNote` → SP `DebitNotes_T_Save` (both verified). Existing notes: `CreditAndDebitNotesDetails_M_Save` / `..._SelectByResHeaderId`. `CreditOrDebitNotesController` (legacy) exposes `Creditnote` / `Debitnote` / grid.
- Day-end guest-ledger columns `CRNotes` / `DRNotes` and `DayEndSummary.CRNotes` / `DRNotes` roll these up.

> `CreditNotesNOTUSEController` and `DebitNotesNOTUSEController` exist but are dead code (their names mark them "NOT USE").

---

## Currency encashment (foreign-cash exchange)

Guest exchanges foreign currency for local cash at the cashier.

**Controller:** `CurrencyEncashmentController` — `Save`, `CurrencyEncashmentVoid`, `CurrencyEncashmentVoidById`, plus separate control partials for **walk-in** vs **in-house guest** (`CurrencyEncashmentControlsForWalkIn` / `...ForGuest`).

| Step | Service → SP (verified) |
|---|---|
| Save an encashment | `CurrencyEncashmentService.Save` → **`CurrencyEncashment_M_Save`** |
| List encashments to void | `CurrencyEncashmentVoid` → **`CurrencyEncashment_T_SelectToVoid`** |
| Void one | `CurrencyEncashmentVoidById` → **`CurrencyEncashmentVoid_T_Save`** |

`CurrencyEncashmentViewModel` records `CurrencyId`, `Rate`, `Amount`, `ConvertedAmount`, `PassportNo`, `ReferenceNo`, `CustomerType` (guest vs walk-in). Encashment supports the multi-currency posting model used across the module (`ConvertionRate`, `AmountInFC` on `FolioDetails`).

---

## Void / adjustments summary

| Object | How it is voided/adjusted | SP |
|---|---|---|
| Extra posting | `PostingController.VoidPosting` / `DeletePosting` | `ExtraPostings_T_Void` |
| Folio line (rebate) | `PostingController.DirectRebate` | `DirectRebate` |
| Settled folio | `FolioManagementController.VoidSettledFoliosByRoom` | `VoidSettledFolios_T_Update` |
| Currency encashment | `CurrencyEncashmentVoidById` | `CurrencyEncashmentVoid_T_Save` |
| Advance | `AdvanceCancelationController.SaveCancelAdvancePayment` | `Advance_Payment_Cancellation_T_Save` |
| Removed tax | `ApplyTaxRemoval` | `Save_TaxRemoval` |

---

## Day-end (night audit) process

The night auditor closes the trading day. There are **two layers**:
(a) the **controller-level orchestration** in `DayEndProcessController.CompleteDayEnd` (verified by reading the file), and
(b) the **internal SP steps** inside `DayEnd_CompleteDayEnd`, whose exact ordered narrations are logged to table **`DayEnd_CompleteDayEnd_SP_ExecutionSteps`** (values below are **live audit rows** read from the DB).

### Cashier / auditor pre-checks (validation gate)

`GET CheckValidations` → private `CheckDayEndValidations()` builds a checklist; day-end cannot proceed unless every item passes:

| Check | Service method | Stored procedure (verified) |
|---|---|---|
| Pending expected arrivals (front office) | `SelectDayEndFrontOfficeCheck` | `DayEnd_FrontOffice_Check` |
| Pseudo rooms | `SelectDayEndPseudoRoomCheck` | `DayEnd_PseudoRoom_Check` |
| Room rates verified | `SelectDayEndRoomRatesCheck` | `DayEnd_RoomRates_Check` |
| POS unsettled/unsigned/unuploaded orders | `POSValidateDayEnd` | (POS validation SP) |
| GL reachable | `GLPostingCheck` | (connectivity) |

Supporting auditor actions before completion:
- `RoomRateCheck` / `POST RoomRateSave` → `DayEndService.RoomRateVerificationSave` — the auditor **verifies room rates** for the night; these feed the auto room posting. Verified rates are stored (see `DayEnd_T_VerifiedRoomRate` table).
- `UpdateNoShows` → marks reservations that never arrived as **no-show**.
- `BillPaymentLKRUpdate` → sets whether a reservation's bill settles in LKR vs foreign currency (`FolioWisePostingBreakUp.IsBillPaymentFromLKR`).

### Controller orchestration (`CompleteDayEnd`)

Each step is guarded by `CheckDayEndStepCompletion` and recorded by `StepCompletionInsert` into **`DayEndDayEndStepCompletion`** (verified columns: `HotelDate`, `Step`, `IsCompleted`, `Narration`, `TxnDateTime`, `UserId`, `PropertyId`), so a failed/half-run day-end can safely resume.

| Ctrl step | Condition | Service call | Effect |
|---|---|---|---|
| 0 | always | `StepCompletionInsert(0,…)` | Log start (user, property, date) |
| 1 | FO enabled | `des.CompleteDayEnd(hotelDate)` → SP `DayEnd_CompleteDayEnd` | The whole front-office night audit (see below) |
| 2 | POS enabled | `des.POSKitchenIssues()` | POS day kitchen issues |
| 3 | POS enabled | `des.POSUpdateDayend()` | Advance POS current date |
| 4 | FO enabled | `des.UpdateHotelDate()` → SP `DayEnd_UpdateHotelDate` | **Advance the hotel date by one day** |

> GL posting SPs (`CallGLSps`) are present but **commented out** in the current controller — a note in the code (stehani, 2023-02-17) says GL postings were moved out of front office. GL data is instead prepared inside `DayEnd_CompleteDayEnd` (steps 5–6 below) via `Dayend_GL_ExtraPosting_Save` and `Dayend_GL_MainBillSettlementDetails_Save`.

### What `DayEnd_CompleteDayEnd` actually does — verified ordered steps

Read from live `DayEnd_CompleteDayEnd_SP_ExecutionSteps` and confirmed against the SP body (`EXEC` calls in brackets are verified inside `OBJECT_DEFINITION`):

1. `DayEnd CompleteDayEnd Started`
2. `Change Convertion Rate On First Night` — `[EXEC Dayend_ChangeConvertionOn_FirstNight]` (locks the FX rate used for a reservation's first night)
3. `Removing not confirmed reservation folios` — cleans folios of unconfirmed reservations
4. **`Inserting Folio Wise Posting BreakUp`** — `[EXEC Reservation_T_FolioWisePostingBreakUp_Save]` **← this is the automatic room-charge night posting** into `FolioWisePostingBreakUp`
5. `Inserting to Dayend GL ExtraPosting Save` — `[EXEC Dayend_GL_ExtraPosting_Save]` (→ `Dayend_GL_ExtraPostingDetails` etc.)
6. `Inserting to Dayend GL MainBillSettlementDetails Save` — `[EXEC Dayend_GL_MainBillSettlementDetails_Save]` (→ `Dayend_GL_BillSettlementDetails`)
7. `Inserting to Day End Currency Conversion` — `[EXEC DayEndCurrencyConversion_M_Save]` (→ `DayEndCurrencyConversion`)
8. `Inserting to DayEnd Summary Guest Ledger` — `[EXEC DayEnd_SummaryGuestLedger_M_Save]` (→ `DayEndSummaryGuestLedger`)
9. `Inserting to DayEnd RoomStatus` — `[EXEC DayEnd_RoomStatus_M_Save]` (→ `DayEndRoomStatus`)
10. `Inserting to DayEnd RoomPickups` — `[EXEC DayEnd_RoomPickup_M_Save]` (→ `DayEndRoomPickup`)
11. `Inserting to DayEnd Summary` — `[EXEC DayEnd_Summary_M_Save]` (→ `DayEndSummary`)
12. `Changing HouseKeeping Status` — `[EXEC HouseKeeping_ProcessWiseStatusChanges_Update]` (DND / dirty on departure)
13. `Releasing OOO Rooms` — releases out-of-order rooms whose block expired
14. `DayEnd CompleteDayEnd SP Ended`
15–16. Daily revenue-report email job inserted / ended
17–18. `Update Hotel Date Started / Ended`
21–24. Revenue Details + Common Occupancy inserts
25–26. `Folio Creation Next Date Started / Ended` — creates next day's folio headers
1000. `Dayend process totally completed.`

### The guest-ledger trial balance (`DayEndSummaryGuestLedger`)

Produced in step 8, this is the night-audit **ledger** — one row per in-house room with the classic movement columns (verified): `OpeningBalance`, `RoomRev`, `FnB`, `ExtraRev`, `Rebates`, `Deposits`, `DepositRefund`, `PostingIn`, `PostingOut`, `Settlements`, `Discount`, `TaxRemoval`, `GainOrLoss`, `ClosingBalance`. Closing = Opening + charges − settlements, per room.

### The property day summary (`DayEndSummary`)

Step 11 rolls up occupancy & revenue for the day (verified columns): `TotalRoom`, `OccupiedRooms`, `Occupancy`, `Arrivals`, `Departures`, `StayOvers`, `NoShow`, `RoomRev`, `FnB`, `Rebates`, `Deposits`, `DepositRefunds`, `CRNotes`, `DRNotes`, `Settlements`, `ServiceCharge`, `Taxes`, `ARR`, `RoomNights`, `GuestNights`, etc.

---

## Cashier reports & financial audit trail

- **Step-completion audit:** `DayEndDayEndStepCompletion` (+ `_History`) and `DayEnd_CompleteDayEnd_SP_ExecutionSteps` timestamp every day-end step per user/property — a full night-audit audit trail.
- **Void/rebate audit:** `VoidExtraPosting_T_Select_CurrentDate` (today's voids), `BillToRoomLog` (transfer log), `TaxGroupDetailDeleteLog`.
- **Settlement audit:** `BillSettlementDetails` (who settled what invoice with which payment type, when, with FX gain/loss).
- **Guest & property ledgers:** `DayEndSummaryGuestLedger`, `DayEndSummary`, `Dayend_RevenueAndOccupancySummary_Executions`.
- **Payment-status changes:** advance link status is tracked through `AdvanceRequestOnline` / `AdvanceRequestOnlinePaymentResponse`; folio `IsLock` and stamped `InvoiceNo` mark a folio as settled; settled folios can be reopened via `VoidSettledFolios_T_Update`.
- Formatted cashier/finance reports themselves are produced by the **Reporting** area (SSRS) and are documented separately — the finance SPs above are their data source.

---

## Screens / modules involved

| Screen (`.cshtml`) area | Controller | Purpose |
|---|---|---|
| Posting (Landing/Form/InHouse) | `PostingController` | Add extra charges, rebate, void |
| Folio management (ManageFolio, BillPreview, BillSettlement) | `FolioManagementController` | Folios, transfers, discounts, settlement |
| Advance payment / cancellation | `AdvancedPaymentController` / `AdvanceCancelationController` | Deposits & refunds |
| Discount | `DiscountController` | Apply/remove discounts |
| Tax calculation partials | `TaxCalculationController` | Tax breakup on postings |
| Credit/Debit notes | `CreditOrDebitNotesNewController` | Post-invoice adjustments |
| Currency encashment | `CurrencyEncashmentController` | Foreign-cash exchange |
| Profit-centre / module posting | `ProfitCenterWisePostingController`, `ModuleCategoryWiseTXNController` | POS→folio |
| Day-end process | `DayEndProcessController` | Night audit |

## Database / API involvement

- **DB:** `HotelResWeb_<Property>` (verified against `HotelResWeb_Browns`). Key SPs & tables named throughout.
- **API / integrations:** Sampath IPG (`FrontOffice.IPG`) for online payments/advance links; fiscal printer via `FiscalPrinter_FolioInvoice` / `FiscalPrinterService` and `DirectPrintService`; SSRS for reports.

## Business rules

1. Charges cannot be posted to a folio that is locked/settled (`FolioHeader.IsLock`, stamped `InvoiceNo`) — reopen it first (`VoidSettledFolios_T_Update`).
2. Room charge for the night is posted automatically by day-end (`Reservation_T_FolioWisePostingBreakUp_Save`), not manually, using **verified** room rates.
3. Day-end will not run while validation checks fail (pending arrivals, unsettled POS orders, unverified rates).
4. Each folio charge carries a tax group; taxes are always derived, never entered free-hand (`TaxCalculations`, `FoliowiseTaxDetails`).
5. Complimentary charges (`IsComplimentory` / `IsComplementary`) are recorded but excluded from revenue.
6. A bill can be settled by multiple payment lines (split/partial) and in multiple currencies (FX gain/loss captured in `ConRateGainOrLoss`).
7. Day-end is idempotent per step via `DayEndDayEndStepCompletion`.

## Error scenarios

| Scenario | System behaviour |
|---|---|
| Day-end validation fails | `CompleteDayEnd` returns `"ERR-Dayend validation(s) fail."`; nothing is committed. |
| Exception inside a day-end step | Error logged to `GEN_ErrTable` (seen in SP body); step marked with the exception narration; `"ERR-<message>"` returned. |
| Posting to a settled/locked folio | Blocked by `FolioHeader.IsLock`; user must void the settled folio first. |
| Under-payment at settlement | Folio retains a positive balance (partial payment) — additional `BillSettlementDetails` line needed. |
| Merge-folio SP absent (Browns) | `Merge_MultipleFolio` / `Save_Merged_MultipleFolio` referenced in code but **not found in `HotelResWeb_Browns`** — merge action would error on this property. |

## Related documents

- `01-*` Reservation / check-in (folio & advance creation context)
- Housekeeping process (day-end room-status changes)
- Reporting (SSRS cashier / finance reports)
- `_research/RESEARCH-PACK.md` (shared facts & conventions)

---

### "Not found in the project" items

- **`Merge_MultipleFolio` / `Save_Merged_MultipleFolio`** — referenced in `Common.Data/FolioEntry.cs` but **not present** in the live `HotelResWeb_Browns` `sys.procedures` (checked directly). Likely a merge feature deployed only to other property databases.
- **GL posting during front-office day-end** — the `CallGLSps()` block in `DayEndProcessController` is **commented out**; GL data is prepared inside `DayEnd_CompleteDayEnd` instead. A standalone real-time GL post from the FO day-end is therefore not active.
- **`TaxTypes.TaxName` / `TaxTypes.Percentage`** — those exact column names do **not** exist; the master uses `Name` and `Rate` (verified). `TaxName`/`Percentage` exist on `FoliowiseTaxDetails`, not `TaxTypes`.
