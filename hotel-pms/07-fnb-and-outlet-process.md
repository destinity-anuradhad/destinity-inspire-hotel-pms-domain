# F&B and Outlet (Profit Centre / POS) Process

> Scienter HotelERP — Destinity Inspire Front Office. Module areas: `Areas/CashieringAndPosting` and `Areas/Administration`.
> Every controller action, service method, `*Entry` method, stored procedure and table named below was read from the actual source code and verified against the live `HotelResWeb_Browns` database. Where something could not be confirmed it is marked **"Not found in the project"** with a note on where it was checked.
>
> **Important scope note.** The internal F&B / POS catalogue (menu items, kitchen recipes, stock, KOT) lives in a **separate database `Categlog_vrV2`** which is a distinct product. This document describes what the **PMS side** does: how outlet charges are **posted into the guest folio** and how outlet cash/card sales are recorded. POS-internal specifics are explicitly marked **"Not found in the project (separate `Categlog_vrV2` DB)"**.

---

## Purpose

Hotels earn revenue not only from rooms but from **outlets** — restaurants, bars, room service, spa, salon, gift shop, laundry, transport, etc. In this PMS each revenue outlet is modelled as a **Profit Centre** (table `ProfitCenters`). When a guest consumes something in an outlet, the charge must reach the guest's **folio** (the room bill) so it can be paid at check-out, **or** be settled immediately at the outlet by cash/card.

This module provides three posting paths that all end up in the same folio/extra-posting tables:

| Path | Who triggers it | Entry point | Landing SP |
|---|---|---|---|
| **Profit-Centre Wise Posting** (manual, front-office/outlet cashier UI) | Cashier picks outlet + item + charge type | `CashieringAndPosting/ProfitCenter` + `ProfitCenterWisePosting` | `ProfitcenterWisePosting_M_Save` |
| **External POS API** (automated, e.g. the `Categlog_vrV2` restaurant POS pushes a bill) | External POS system HTTP call | `Administration/POSApi` → `SaveInHousePOSAPIPosting` | `Posting_InHouse_T_Save` |
| **Module-Category-Wise TXN** (module posting staging, e.g. minibar/stock item consumption) | Cashier UI | `CashieringAndPosting/ModuleCategoryWiseTXN` | `ModuleCategoryWiseTXN_T_Save` (staging only) |

All three ultimately write to **`ExtraPostingDetails`** (+ `ExtraPostingDetailWiseTaxes`, `ExtraPostingSettlements`) and, when *bill-to-room*, call **`Insert_Folio`** to append the charge onto the guest's live **`FolioHeader` / `FolioDetails`**. See `05-cashiering-and-finance-process.md` for the folio/settlement side.

---

## Relevant users / departments

| Role | Uses |
|---|---|
| Outlet cashier (restaurant/bar/spa/shop) | Profit-Centre Wise Posting screen; settle cash/card at outlet or bill-to-room |
| Front-office cashier | Same screen; posting outlet charges onto an in-house guest's folio |
| Housekeeping | Profit-centre posting interface for minibar/service items (code comment: "House Keeping Profit Center Posting Interface") |
| External POS system | Server-to-server `POSApi/SaveInHousePOSAPIPosting` call to bill a restaurant order to a room |
| Administrator | Configures outlets (`ProfitCenterController`), items, item categories, charge types, prices, patterns |
| Night auditor | Day-end picks up these postings into revenue/occupancy and GL summaries |

---

## Preconditions

- User is authenticated (`[VerifyLoggedUser]`) and holds page rights. Profit-centre posting screens require **`[UserWisePageAccess(3031, ...)]`** with function codes `3024, 4090, 4091` (see `ProfitCenterController`, `ProfitCenterWisePostingController`).
- The property has outlets configured in **`ProfitCenters`** (each row carries a **`ChargeCodeId`** and **`PostingTypeId`** that decide how the charge is booked, plus `IsNeedToShowWarkingBillTaxes`).
- Items, item categories, charge types and prices are configured (`ProfitCenterItems`, `ProfitCenterItemCategories`, `ProfitCenterChargeTypes`, `ProfitCenterItemCategoryWiseTypeWisePrcing`).
- Tax groups are configured (`TaxGroups`, `TaxTypes`) and a group is assigned to the item/posting.
- For **bill-to-room** the target room must currently have an **in-house** reservation (`InHouseReservationDetails` / `InhouseReservationHeaders`), and that reservation must **not** be flagged `IsStopPosting = 1`.
- **Day-end must not be running** — every posting SP first checks `DayEndDayEndStepCompletion` and raises *"Day end is processing, you are not allowed to do postings."* if a day-end step is open.

---

## Outlets / Profit Centres — the core concept

```
        PROPERTY
           │
           ▼
   ┌───────────────────────────────────────────────┐
   │  ProfitCenters  (one row per outlet)           │
   │  Id · Name · IsActive · ChargeCodeId ·         │
   │  PostingTypeId · IsNeedToShowWarkingBillTaxes  │
   └───────────────────────────────────────────────┘
        │                 │                  │
        ▼                 ▼                  ▼
 ProfitCenterItem   ProfitCenter        ProfitCenter
 Categories         Items               ChargeTypes
        │                 │                  │
        └──────── ProfitCenterItemCategoryWiseTypeWisePrcing ────────┘
                        (price per item × category × charge-type × price-type)
```

Each outlet (`ProfitCenters` row) points at:
- a **Charge Code** (`ChargeCodeId`) — the revenue/charge classification used on the folio,
- a **Posting Type** (`PostingTypeId`) — which maps (via `PostingTypes.AccountCode`) to a GL account code.

**Verified outlets in `HotelResWeb_Browns`** (`SELECT Id, Name, ChargeCodeId, PostingTypeId FROM ProfitCenters`): this property is spa/retail-oriented — e.g. `SPA` (ChargeCodeId 5, PostingTypeId 4), `SALON` (5, 9), `GIFT SHOP` (12, 97), plus `Ayurweda`, `BOUTIQUE SHOP`, `RICE SALE`, `SPA NO TAX`. There are **46 profit-centre rows** across properties. **Restaurant/bar F&B outlets are not present in this particular property's data**, so on the Browns DB F&B charges arrive predominantly via the **external POS API** path (`Posting_InHouse_T_Save`). The profit-centre UI mechanism is identical for restaurant outlets at other properties.

### Configuration screens (Administration)

| Screen / controller | File | Purpose |
|---|---|---|
| `ProfitCenterController` (Administration) | `Areas/Administration/Controllers/ProfitCenterController.cs` | CRUD for outlets, items, item categories, charge types, patterns, prices |
| `ModuleCategoryWiseItemsController` | `Areas/Administration/Controllers/ModuleCategoryWiseItemsController.cs` | Maps stock items ↔ modules/stock-locations; **`StockLocationCombo()`** and `modulesCategoryCombo()` |
| `ModulePostingsController` / `PostingCategoriesController` | `Areas/Administration/Controllers/*.cs` | Posting-category & module-posting master config |
| `POSApiController` | `Areas/Administration/Controllers/POSApiController.cs` | External POS integration endpoints (see below) |

Service `ProfitCenterService` (`FrontOffice.Service/ProfitCenterService.cs`) wraps `ProfitCenterEntry` for every master operation (`ProfitCenter_M_Save/_Select/_Delete`, `ProfitCenterItems_M_*`, `ProfitCenterChargeTypes_M_*`, `ProfitCenterItemCategories_M_*`, `ProfitCenterPatterns_M_*`).

> **POS-internal item master, recipes, KOT/BOT printing, stock deduction, table plans:** **Not found in the project (separate `Categlog_vrV2` DB).** The PMS reads only *stock locations / venues* from that DB (see "Link to the POS catalogue DB" below).

---

## POS order process — as far as it is visible in the PMS

The **taking of the order** (table, covers, menu items, KOT/kitchen ticket, modifiers) happens inside the external POS product and is **Not found in the project (separate `Categlog_vrV2` DB)**. What the PMS sees is the **finished bill** arriving through one of the three paths.

### Link to the POS catalogue DB (`Categlog_vrV2`)

The PMS **does hold a live connection** to the POS/inventory DB. `Web.config` defines connection string **`SqlServer2016Inventory`** → `Initial Catalog=Categlog_vrV2` (server `10.4.1.180`, prod Azure `jwh-pms-db-prod...database.windows.net`). It is used in a handful of read/cross-post places (`Configs.GetConnectionSting("SqlServer2016Inventory")`):

| Caller | File · line | What it reads/writes in `Categlog_vrV2` |
|---|---|---|
| `ModulePostingEntry.SelectStockLocation` | `Common.Data/ModulePostingEntry.cs:69` | `StockLocations_M_Select` (outlet stock locations for the module-posting screen) |
| `ReservationHeaderEntry` (venue combo) | `Common.Data/ReservationHeaderEntry.cs:1966` | `SELECT code, description FROM Location_Ref` (venues) |
| `DayEndEntry` (day-end) | `Common.Data/DayEndEntry.cs:140,178` | `DayEndGL_Posting`, `POS_spInsertKitchenIssues` (push day-end GL / kitchen issues to POS DB) |

Everything else about the POS catalogue (item pricing logic, stock levels, kitchen issues detail) lives in `Categlog_vrV2` and is **Not found in the project**.

---

## Charging an outlet consumption to the guest room — the posting flow

### Path A — Profit-Centre Wise Posting (manual UI)

**UI:** `CashieringAndPosting/ProfitCenter/Landing` (+ `ProfitCenterWisePosting/Landing`). The cashier chooses the outlet, item(s), charge type and quantity; the screen loads prices from `ProfitCenterService.SelectPrice()` → `ProfitCenter_ItemWiseCategoryWiseChargeTypeWisePricing_M_SelectByItemId` and calculates taxes from `ProfitCenter_TaxCalculations`. On save it POSTs a JSON payload to the data layer:

- **Data layer:** `Common.Data/Profit_CenterWise_PostingEntry.cs` → `Save(...)` calls stored procedure **`ProfitcenterWisePosting_M_Save`** with:
  `@RoomId, @Name, @Address, @ProfitcenterItemCategoryId, @ProfitcenterDetailsJson, @TaxDetailsJson, @PaymentDetailsJson, @InhousePaymentAmount, @BillToRoomCheck, @UserId, @IsComplementary, @PropertyId, @CompanyId`.

**Inside `ProfitcenterWisePosting_M_Save` (verified from the live DB):**

1. Guards day-end (`DayEndDayEndStepCompletion`) → error if running.
2. Reads `IsTaxInclusiveExtraPosting` from `FOSettings` (tax-inclusive vs tax-on-top pricing).
3. Resolves the outlet's `ChargeCodeId`, `PostingTypeId`, `Name` from `ProfitCenters`; the GL `AccountCode` from `PostingTypes`.
4. Allocates a document number `PRC…` via `UpdateNextDocNoWithUpdate 'PRC'`.
5. Determines **room vs walk-in**: if `InHouseReservationDetails` has the `@RoomId`, it is an **in-house** charge and it resolves `ReservationHeaderId`, `GuestProfileId`, guest name/address; otherwise it is a **walk-in** outlet sale. Raises an error if the reservation is `IsStopPosting = 1`.
6. Writes the POS transaction record set:
   - `ProfitCenter_txnHeader` (one header per posting; DocumentNo, RoomId, GuestId, ProfitCenterId, ChargeDateTime = `dbo.GetCurrentDate`),
   - `Profitcenter_txnDetails` (each item line: item, charge type, qty, unit price, price, tax group; **discount lines are stored with negative amounts**),
   - `ProfitCenter_txnTaxes` (per-line tax breakdown via `TaxCalculations`),
   - `ProfitCenter_txnPayments` (how the txn was settled).
7. Writes the **folio-facing extra posting**:
   - `ExtraPostingDetails` — the actual charge that hits the guest ledger (ChargeCode, DocumentNo `INV…`, ChargeAmount incl. tax, `OrginalAmount` excl. tax, `DRCR`, `AccountCode`, currency, `IsBillToRoom`, `RefDocNo` = the `PRC…` doc). Discounts are posted as a separate `DIS`-prefixed credit line (`ChargeCodeId 15`, `PostingTypeId 36`, `DRCR = 'C'`).
   - `ExtraPostingDetailWiseTaxes` — tax rows for that posting.
   - `ExtraPostingSettlements` — the settlement row (payment mode + amount + account code).
8. **If `@BillToRoomCheck = 1`** (bill-to-room, in-house):
   - It sets the settlement `PaymentTypeId = FOSettings.BillToRoomId` (i.e. "BILL TO ROOM"),
   - Calls **`EXEC Insert_Folio @ReservationHeaderId, @ChargeCodeId, @ExtraPostingDetailId, @PropertyId, @UserId, 0`** → this appends the charge to `FolioHeader`/`FolioDetails` (+ folio taxes) so it appears on the room bill,
   - Calls `Dayend_RevenueAndOccupancySummary_Executions_M_Save` so the outlet revenue is reflected in day-end summaries.
9. Returns `{ DocumentNo, Name, Address }` for the outlet receipt.

### Path B — External POS API (restaurant bill → room)

An **external POS system** (e.g. the restaurant POS backed by `Categlog_vrV2`) calls MVC action **`Administration/POSApi/SaveInHousePOSAPIPosting`** (`POSApiController.cs`) with:
- `posting` (JSON bill: amount, tax group, charge code, `IsBillToRoom`, and a `RoomDetails` array with `RoomId`/`ReservationNo`/`GuestProfileId`),
- `RestaurantOrderNo`, `PropertyId`, `UserId`, `isRestaurantBill`.

Controller → `PostingService.SaveInHousePOSAPIPosting` → `PostingEntry.SaveInHousePOSAPIPosting` (`Common.Data/PostingEntry.cs:216`) → stored procedure **`Posting_InHouse_T_Save`** (params `@postingData` JSON, `@RestaurantOrderNo`, `@isRestaurantBill`, `@PropertyId`, `@UserId`). Verified in the live DB: `Posting_InHouse_T_Save` calculates tax (`#TempTaxDetails`), writes `ExtraPostingDetails` + `ExtraPostingDetailWiseTaxes`, and — when `IsBillToRoom` — calls **`Insert_Folio`** exactly like Path A. It logs its raw call into `Posting_InHouse_T_Save_SP_Para` and guards day-end. The controller wraps the result in a small JSON `ApiResponse` (`HttpCode 200/500`, `Description`). `RestaurantOrderNo` is stored so the room posting is traceable back to the POS order.

The same controller exposes **`MealReservationJson`** / **`MealReservationUpdateJson`** (outbound meal-reservation feed for the POS) and **`SelectRoomList` / `SelectRoomDetails`** (so the POS can look up which rooms/guests are in-house before billing).

### Path C — Module-Category-Wise TXN (staging)

`CashieringAndPosting/ModuleCategoryWiseTXNController.ModuleCategoryWiseTXNSave` → `ModuleCategoryWiseTXNService` → `ModuleCategoryWiseTXNEntry.ModuleCategoryWiseTXNSave` → SP **`ModuleCategoryWiseTXN_T_Save`**. Verified: this SP **only inserts a staging row into the `ModuleCategoryWiseTXN` table** (applying the discount to compute `Rate` — `A` = absolute, else percentage). It does **not** itself post to the folio; it is a capture/staging step for module-category consumption. *(The `ModuleCategoryWiseTXN` table is currently empty on Browns — 0 rows.)*

---

## 6-step process: post a restaurant charge to a room

> Business scenario: a guest in room 320 orders in the restaurant; the waiter closes the bill as **"Bill to Room"**.

| # | Stage | What happens | Where (verified) |
|---|---|---|---|
| **1** | **User action** | The bill is closed in the POS (or the outlet cashier fills the Profit-Centre Wise Posting screen), selecting the room, item(s), quantity, charge type, tax group, and choosing **Bill to Room**. | POS system *(Categlog_vrV2)* → `POSApi/SaveInHousePOSAPIPosting`; or `CashieringAndPosting/ProfitCenter` UI |
| **2** | **System validation** | PMS checks: day-end not running (`DayEndDayEndStepCompletion`); the room has an **in-house** reservation (`InHouseReservationDetails`); reservation is **not** `IsStopPosting`; a valid `ChargeCodeId`/`PostingTypeId`/tax group exist. | `Posting_InHouse_T_Save` / `ProfitcenterWisePosting_M_Save` |
| **3** | **Database change** | Tax is calculated (`ProfitCenter_TaxCalculations` / `TaxCalculations`). A charge row is written to **`ExtraPostingDetails`** (amount incl. tax, `RefDocNo`, `AccountCode`, `IsBillToRoom = 1`), tax rows to **`ExtraPostingDetailWiseTaxes`**, POS txn rows to `ProfitCenter_txnHeader/Details/Taxes/Payments` (manual path), and a `BILL TO ROOM` settlement to **`ExtraPostingSettlements`**. | live DB |
| **4** | **Related module update** | **`Insert_Folio`** appends the charge onto the guest's live folio — `FolioHeader` / `FolioDetails` (+ folio taxes) — so it shows on the room bill and the outstanding balance rises. `Dayend_RevenueAndOccupancySummary_Executions_M_Save` updates revenue/occupancy summaries. | `Insert_Folio`, cashiering module |
| **5** | **Notification / integration** | The POS receives a JSON `ApiResponse` (`HttpCode 200` + document no) confirming the room posting; `RestaurantOrderNo` links the folio line back to the POS order. Night audit later posts these to the GL and pushes day-end GL/kitchen issues back to `Categlog_vrV2` (`DayEndGL_Posting`, `POS_spInsertKitchenIssues`). | `POSApiController`, `DayEndEntry` |
| **6** | **Final result** | The restaurant charge is now a line on the guest's folio, payable at check-out; the outlet's revenue is recorded and reconciled. | `05-cashiering-and-finance-process.md` |

---

## Cash / card payments at the outlet (not billed to room)

When the guest pays **at the outlet** (walk-in, or in-house guest who settles immediately):

- `@BillToRoomCheck = 0` on `ProfitcenterWisePosting_M_Save` (or `IsBillToRoom = false` on the POS bill).
- The chosen payment types come in via `@PaymentDetailsJson` (`PaymentTypeId`, `PaymentTypeName`, `Amount`).
- The SP writes the settlement to **`ExtraPostingSettlements`** (`PaymentType`, `Amount`, `AccountCode` from `PaymentModes`, `CurrencyId`, `ConvertionRate`) and to **`ProfitCenter_txnPayments`** — **no `Insert_Folio` call**, so nothing lands on a room folio.
- Multiple payment lines (split cash + card) are supported (each JSON element becomes one settlement row).
- Payment modes come from `PaymentModeService.Select(ActiveOnly)` (`ProfitCenterController.Select_payementmood`).

> The detailed cash-drawer / shift reconciliation for outlet cashiers beyond `ExtraPostingSettlements` is handled by the general cashiering module — see `05-cashiering-and-finance-process.md`.

---

## Discounts on F&B / outlet charges

Two mechanisms exist:

1. **Line-level discount inside the posting** (`ProfitcenterWisePosting_M_Save`): a detail row flagged `IsDiscount = 1` is stored with **negative** unit price/price, and posted to the folio as a **separate `DIS`-prefixed credit** with `ChargeCodeId 15`, `PostingTypeId 36`, `DRCR = 'C'`, remark "*<Outlet> - Discount*". So discount and gross charge are auditable separately.
2. **Module-category discount** (`ModuleCategoryWiseTXN_T_Save`): `@DiscountType = 'A'` → absolute deduction (`Rate = OriginalAmount − DiscountRate`); any other value → percentage (`Rate = OriginalAmount − (OriginalAmount/100 × DiscountRate)`).

---

## Taxes & service charges on F&B

- Tax is computed by stored procedures **`ProfitCenter_TaxCalculations`** (POS/profit-centre path) and **`TaxCalculations`** (generic), driven by the item's **Tax Group** (`TaxGroups`, `TaxBreakValue`) and its member **Tax Types** (`TaxTypes` → VAT / Service Charge / SSCL / TDL, etc. — the Sri Lanka tax model).
- **Tax-inclusive vs tax-on-top** is controlled per property by `FOSettings.IsTaxInclusiveExtraPosting`. When inclusive, the SP back-computes the net (`Amount / TaxBreakValue`); when on-top it grosses up (`Amount × TaxBreakValue`).
- Each tax component is stored per posting in `ExtraPostingDetailWiseTaxes` and per POS line in `ProfitCenter_txnTaxes`, each carrying its own GL `AccountCode` and `TaxName`.
- **Service Charge** is modelled as one of the tax types within the tax group (not as a separate hard-coded field). The exact tax-group membership per outlet is data-driven in `TaxGroups`/`TaxGroupWiseTaxTypes`.

> Whether an outlet shows taxes on a **walk-in** receipt is toggled by `ProfitCenters.IsNeedToShowWarkingBillTaxes`.

---

## Order cancellation / reversal

- The PMS does not expose a dedicated "cancel POS order" action in these controllers; the **taking and voiding of an order** is a POS-internal operation — **Not found in the project (separate `Categlog_vrV2` DB)**.
- On the **folio side**, a wrongly posted outlet charge is reversed like any other posting — by a **rebate / credit note** in the cashiering module (`ExtraPostingDetails.IsRebate`, credit-note flow). See `05-cashiering-and-finance-process.md`.
- A **discount** effectively partially reverses a charge (negative `DIS` line, above).

---

## Integration with Front Office & Cashiering

```
   OUTLET / POS                         FRONT OFFICE / CASHIERING
 ┌───────────────┐   room lookup    ┌──────────────────────────────┐
 │ Restaurant /  │◀── SelectRoomList│  In-house reservations       │
 │ Bar / Spa POS │   MealReservation│  (InHouseReservationDetails)  │
 │ (Categlog_    │───────────────▶  │                              │
 │   vrV2)       │  SaveInHouse-    │   ExtraPostingDetails         │
 └───────────────┘  POSAPIPosting   │   + WiseTaxes + Settlements   │
        ▲                           │            │ Insert_Folio     │
        │ ProfitCentre UI           │            ▼                  │
 ┌───────────────┐  Profitcenter-   │   FolioHeader / FolioDetails  │──▶ Bill / check-out
 │ Outlet cashier│  WisePosting_    │            │                  │    settlement
 │  (PMS screen) │  M_Save          │            ▼                  │
 └───────────────┘───────────────▶  │   Day-end: revenue/occupancy, │
                                    │   GL, kitchen issues → POS DB │
                                    └──────────────────────────────┘
```

- **Inbound to folio:** outlet charges become `ExtraPostingDetails` → `FolioDetails` (bill-to-room) and are paid at check-out through the normal settlement flow.
- **Outbound to POS:** the PMS gives the POS the in-house room list (`SelectRoomList`/`SelectRoomDetails`) and meal reservations (`MealReservationJson`), and at day-end pushes GL and kitchen-issue data into `Categlog_vrV2`.
- **Cashiering** owns the settlement, taxes, credit notes and reporting for these postings (see `05-cashiering-and-finance-process.md`).

---

## Screens / modules involved

| Screen / action | File |
|---|---|
| `CashieringAndPosting/ProfitCenter` (Landing, Form, Grid, price/tax combos, BillPayment) | `Areas/CashieringAndPosting/Controllers/ProfitCenterController.cs` |
| `CashieringAndPosting/ProfitCenterWisePosting` (Landing, Grid, Form, Save, BillPayment) | `Areas/CashieringAndPosting/Controllers/ProfitCenterWisePostingController.cs` |
| `CashieringAndPosting/ModuleCategoryWiseTXN` (Index, SelectReservationNumbersByType, Save) | `Areas/CashieringAndPosting/Controllers/ModuleCategoryWiseTXNController.cs` |
| `Administration/POSApi` (SaveInHousePOSAPIPosting, MealReservationJson, SelectRoomList…) | `Areas/Administration/Controllers/POSApiController.cs` |
| `Administration/ProfitCenter`, `ModuleCategoryWiseItems`, `ModulePostings`, `PostingCategories` | `Areas/Administration/Controllers/*.cs` |

---

## Database / API involvement (verified)

**Master / config tables:** `ProfitCenters`, `ProfitCenterItems`, `ProfitCenterItemCategories`, `ProfitCenterChargeTypes`, `ProfitCenterPatterns`, `ProfitCenterItemCategoryWiseTypeWisePrcing`, `ProfitCenterWiseDocumentNo`.

**Transaction tables (active path):** `ProfitCenter_txnHeader`, `Profitcenter_txnDetails`, `ProfitCenter_txnTaxes`, `ProfitCenter_txnPayments`; `ExtraPostingDetails`, `ExtraPostingDetailWiseTaxes`, `ExtraPostingSettlements`; `ModuleCategoryWiseTXN` (staging); `Posting_InHouse_T_Save_SP_Para` (POS-API call log).

**Folio side:** `FolioHeader`, `FolioDetails` (+ folio taxes) via `Insert_Folio`.

**Key stored procedures:** `ProfitcenterWisePosting_M_Save`, `Posting_InHouse_T_Save`, `ModuleCategoryWiseTXN_T_Save`, `Insert_Folio`, `ProfitCenter_TaxCalculations`, `TaxCalculations`, `UpdateNextDocNoWithUpdate`, `Dayend_RevenueAndOccupancySummary_Executions_M_Save`, plus the `ProfitCenter*_M_*` masters and `ProfitCenter_Posting_Bill_Preview`, `Report_ProfitCenterWisePostingDetails`, `Select_ProfitCenterInvoicePayments`, `Select_ProfitCenterInvoiceTaxes`.

**Cross-DB (`Categlog_vrV2`, connection `SqlServer2016Inventory`):** `StockLocations_M_Select`, `Location_Ref` (read), `DayEndGL_Posting`, `POS_spInsertKitchenIssues` (write at day-end).

> **Naming note.** The empty tables **`Core_ProfitCenterTransactionHeader/Detail/Payment/Tax`, `Core_ProfitCenterItems`, `Core_ProfitCenterChargePrices`, `Core_ProfitCenters`** also exist in the schema but held **0 rows** at verification time (2026-09-18) and are **not** referenced by the C# code paths above (which use the `ProfitCenter_txn*` / `ProfitCenters` tables). They appear to be a newer/parallel "Core_" schema not yet in use here. No C# file references `Core_ProfitCenter*` — **Not found in the project (code side)**.

---

## Business rules

1. No posting is allowed while day-end is running (all three SPs guard `DayEndDayEndStepCompletion`).
2. Bill-to-room is only possible for an **in-house** reservation that is not `IsStopPosting`.
3. Discounts are posted as separate negative/`DIS` credit lines — gross and discount are never merged.
4. Tax treatment (inclusive/on-top) is a per-property setting (`FOSettings.IsTaxInclusiveExtraPosting`).
5. Each posting gets a `PRC…` profit-centre document number and an `INV…` extra-posting document number (`UpdateNextDocNoWithUpdate`).
6. Every folio-facing charge carries a GL `AccountCode` (from `PostingTypes`/`PaymentModes`) for the day-end GL.

## Expected result

- Outlet consumption is either **on the guest's folio** (bill-to-room, payable at check-out) or **settled at the outlet** (cash/card), with full tax and GL breakdown, and is picked up by night audit into revenue/occupancy and GL summaries.

## Error scenarios

| Trigger | System response |
|---|---|
| Day-end in progress | `RAISERROR('Day end is processing, you are not allowed to do postings.')` |
| Reservation flagged stop-posting | `RAISERROR('Reservation marked as stop posted')` |
| Any SP failure | Transaction rolled back, error logged to `GEN_ErrTable`, message re-raised; POS-API returns `HttpCode 500` with the message |
| Room not in-house (POS bill-to-room) | Charge falls back to walk-in handling (no folio line) |

## Related documents

- `05-cashiering-and-finance-process.md` — folios, settlement, credit notes, day-end GL.
- `03-reservation-process.md` — in-house reservations, `IsStopPosting`.
- `11-integrations-and-data-flow.md` — the external POS API integration and `Categlog_vrV2` connection in the wider integration landscape.
- `12-database-and-technical-architecture.md` — multi-DB / connection-string architecture.
