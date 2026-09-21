# Reports & Business Information

> Scienter HotelERP — Destinity Inspire Front Office. Module areas: `Areas/Reporting` and `Areas/DataAnalysis`.
> Every controller action, service method, stored procedure, table and configuration key named below was read from the actual source code and/or verified against the live `HotelResWeb_Browns` database. Where something could not be confirmed it is marked **"Not found in the project"** with a note on where it was checked.

## Purpose

The reporting subsystem turns the operational data captured by the PMS (reservations, folios, postings, payments, housekeeping, day-end statistics) into **printable documents** (invoices, registration cards, confirmations) and **management information** (occupancy, revenue, ADR/RevPAR, agent production, guest analytics).

There are three distinct delivery mechanisms, all grounded in source:

1. **SSRS server reports** — the main catalogue. A registry table (`ReportDetails`) maps a report to a stored procedure and parameter set; the report is rendered by a remote SQL Server Reporting Services server and displayed/printed inside the app. Driven by `ReportController` → `ReportTemplate.aspx`.
2. **In-app DevExpress "DocumentViewer" grid reports** — a smaller set of list-style reports built as `XtraReport` objects, shown in an interactive grid and exported to PDF/XLS. Driven by `ReservationController` and `RoomSaleController`.
3. **Data-analysis dashboards / charts** — interactive JSON-fed charts (occupancy, pickup, guest/room-night analysis) rendered client-side. Driven by `DataAnalysisController` + `DataAnalysisService`, backed by `Analysis_*` and `DashboardAPI_*` SPs.

## Relevant users / departments

| Role | Typical reports used |
|---|---|
| Front-office cashier | Invoices, proforma invoices, advance/rebate receipts, currency encashment, cashier returns |
| Front-office / reception | Arrival, departure, in-house guest lists, registration cards, information sheet |
| Reservations | Reservation details, cancelled reservations, allotment, on-the-book, forecast |
| Night auditor | Daily Revenue Report, Day-End Summary, Hotel Statistics, Manager Report, void/rebate logs |
| Revenue / management | Occupancy, ARR/ADR/RevPAR, revenue by segment/agent/company, sales-person statistics, dashboards |
| Sales & marketing | Agent production, Room Nights by Agent, agent-wise pickup, tour-operator performance |
| Housekeeping | Housekeeping room-wise status, discrepancy, out-of-order rooms, room-boy assignment |
| Guest relations | Guest history, VIP list, birthdays, guest by country/nationality, allergies |
| Finance / audit | Guest ledger, billing journals, tax reports, GL/day-end reports, user-access & trace logs |

## Preconditions

- User is authenticated (SSO / `VerifyLoggedUser`).
- **Report-level permission** is granted. The SSRS entry point `ReportController.DirectToReport` is decorated with `[VerifyLoggedUser]` and `[UserWiseReportAccess]` (see [Report access control](#report-access-control-userwisereportaccess)). DataAnalysis pages use `[UserWisePageAccess(<pageId>, "S")]`.
- The SSRS report server is reachable and the report `.rdl` exists in the configured server folder (`Web.config` → `ReportServer`, `SSRSReportsFolder`).
- The user has a **logged property** (`SessionObjects.LoggedUser.LoggedProperty.Id`) — every SSRS report receives it as a `PropertyId` parameter (multi-tenant scoping).

---

## How reports are generated

### 1. SSRS pipeline (primary — the report catalogue)

The bulk of management/operational reports are **SQL Server Reporting Services** reports. Flow:

1. **User action** — user opens a report from the reports menu; `ReportController.DirectToReport(int Id)` (or `Index`) loads the report shell view. `SelectReportParamaters(reportName)` (POST) returns the `_ReportParameter` partial that renders only the parameter inputs this report needs.
2. **Metadata lookup** — parameters and viewer options come from the **`ReportDetails`** registry table via `ReportService.SelectReportParamaters` → `ReportEntry.SelectReportParameters` (SP `Report_Parameters_byReportName`). The set of selectable reports comes from `Report_Select_ReportNames`.
3. **Render request** — `ReportController.ViewReport()` reads the query-string filters (a large fixed list: `FromDate`, `ToDate`, `Date`, `ResNo`, `Arrival`, `Departure`, `Status`, `Company`, `RateCode`, `Segment`, `PaymentType`, `PropertyId`, `SalesPerson`, `RoomBoyId`, `DepartmentId`, `Market`, etc.) and builds a URL to **`/ReportTemplate.aspx?ReportName=…&<params>`**, returned inside the `Report_Iframe` view.
4. **SSRS execution** — `ReportTemplate.aspx.cs` (`Page_Load`) configures a **`Microsoft.Reporting.WebForms.ReportViewer`** (`rvSiteMapping1`) in **remote** processing mode:
   - `ServerReport.ReportServerUrl` = `AppSettings["ReportServer"]`
   - `ServerReport.ReportPath` = `/{SSRSReportsFolder}/{ReportName}`
   - Credentials = `DestinityReportServerCredentials`
   - Standard parameters injected: `ReportConStr` (built from SaaS/property connection info via `ReportSourceConStr`), `UserName`, `PropertyId`, plus report-specific parameters (`IsPreview`, `IsLKROnlyInvoice`, etc.).
   - Viewer toolbar behaviour (`ShowExportControls`, `ShowPrintButton`, `ShowToolBar`, `ShowZoomControl`…) is read per-report from `ReportDetails` via `ReportService.SelectReportDetailsByReportName` (SP `ReportDetails_M_SelectByReportName`).
5. **Output** — the ReportViewer renders in-browser; the user prints or uses SSRS's own export controls (PDF/Excel/Word) when enabled. Configured in `Web.config`:

| `Web.config` key | Value (Browns) | Meaning |
|---|---|---|
| `ReportServer` | `http://10.4.1.180:8080/ReportServer` | SSRS report server endpoint |
| `SSRSReportsFolder` | `Front Office Reports Server Projects` | SSRS folder holding the `.rdl` files |
| `ReportSourceConStr` | `Data Source=…;Initial Catalog=HotelResWeb_Browns` | Template for the `ReportConStr` report data-source |
| `ReportHeight` | `530` | Viewer iframe height |
| `ReportViewerWebControlHandler` | `Microsoft.Reporting.WebForms.HttpHandler` v15 | ReportViewer AXD handler registration |

> **Print copy tracking:** for invoice-type documents, `ReportController.SaveReportPrintCopyCount` (SP `ReportPrintCopyLog_Insert`, table `ReportPrintCopyLog`) records how many times an invoice was printed.

### 2. In-app DevExpress DocumentViewer grid reports

A smaller set of list reports are built as **DevExpress `XtraReport`** objects (namespace `DevExpress.Web.Mvc`) instead of SSRS. Pattern (verified in `ReservationController`, `RoomSaleController`):

- A `…Rpt` action returns `PartialView("_DocumentViewerPartial", <report>)` — the interactive viewer.
- A `…RptExport` action returns `DocumentViewerExtension.ExportTo(<report>, Request)` — export to **PDF/XLS** through DevExpress.
- The report `DataSource` is filled from a service (e.g. `ReservationHeaderService.GetRoomSaleList`, `SelectReservationList`, `HotelBookingConfirmation`, `GetReservationInformation`).

Examples of DocumentViewer reports (all under `Areas/Reporting`):

| Report action | Service data source | Report |
|---|---|---|
| `RoomSale/RoomSales` (+ `…Rpt`/`…RptExport`) | `ReservationHeaderService.GetRoomSaleList` | Room Sales list |
| `Reservation/FutureReservations` | `SelectReservationList` | Future Reservations |
| `Reservation/ProformaInvoice` | `ProformaInvoiceSelect` | Proforma Invoice |
| `Reservation/ReservationConfirmation` / `…Group` | `HotelBookingConfirmation` | Reservation Confirmation (single/group) |
| `Reservation/GuestRegistraionForm` | `GetGuestReservationDetails` | Guest Registration Form |
| `Reservation/InformationSheet` / `InformationSummary` | `GetReservationInformation` / `InformationSummary` | Information Sheet / Summary |
| `Reservation/RoomtypeWiseForeCastView` | `RoomTypeWiseForeCastRpt` | Room-type-wise forecast |
| `Reservation/GuestArrivalAlphabetically` / `GuestDepartureAlphabetically` | `SelectGuestArrivalAlphabetically` / `…Departure…` | Alphabetical arrival/departure |
| `Reservation/ComplementaryReservation` | `SelectComplementaryReservations` | Complementary reservations |

`Reporting/Home` exposes `Designer` and `Viewer` view stubs (a DevExpress report designer/viewer scaffold — trivial `return View()`).

> **Dead code note:** `FolioController`, `CountryController`, `GuestProfilebyCountryController`, `PropertyDetailReportHeaderController` and most of `PostingController`/`ArrivalDepartureController` are **entirely (or almost entirely) commented out** in this checkout. Their equivalents are served today through the SSRS catalogue (`ReportController`). Documented as legacy/dead code.

### 3. Excel / PDF libraries

- **EPPlus 6.2.8** (`packages/EPPlus.6.2.8`) and **Select.HtmlToPdf 20.2.0** (`packages/Select.HtmlToPdf.20.2.0`) are referenced in the solution and used elsewhere in the app for Excel/PDF document generation. They are **not** invoked directly by the `Areas/Reporting` controllers — grid-report export in Reporting is handled by DevExpress `DocumentViewerExtension.ExportTo`, and SSRS handles PDF/Excel for server reports. (Searched `Areas/Reporting/**/*.cs` for `OfficeOpenXml`/`ExcelPackage`/`HtmlToPdf` — no matches.)

### 4. Batch PDF generation — `ReportDownloader`

`ReportDownloader/Program.cs` is a standalone worker (console loop, `Thread.Sleep(2000)`) that renders SSRS reports to PDF **outside** the web request:

1. Polls SP **`HK_DocumentsToDownload`** for a queued document (JSON → `ReportRequest`).
2. Calls the SSRS **`ReportExecutionService`** SOAP endpoint (`AppSettings["SsrsUrl"]`, `NetworkCredential(SsrsUsername, SsrsPassword, SsrsDomain)`): `LoadReport(ReportPath)` → `SetExecutionParameters` → `Render("PDF", …)`.
3. Saves the PDF to `OutputDirectory` with a GUID filename and updates status via **`HK_DocumentsToDownload_UpdateStatus`** (`DOWNLOAD_SUCCESS` / `DOWNLOAD_FAILED`).

This underpins document delivery (e.g. emailing/WhatsApp of generated reports).

---

## Report access control (`UserWiseReportAccess`)

Report visibility is **per-user**, not just role-based.

- **Attribute:** `UserWiseReportAccess` (class in `WebUIMvc/Controllers/BaseController.cs`, extends `CustomAuthorizeAttribute`). Applied to `ReportController.DirectToReport`. On each request it resolves the page/report id for the requested URL and checks the logged user's access:
  - **Central SSO mode** (`IsCentralLoginEnabled=true`): calls `CentralAccessApi` endpoints `api/user/reportaccess` and `api/user/validateaccess`; access is granted only when the API returns `"Access granted."` / HTTP 200.
  - **Local mode:** `UserWiseIndividualAccessService.GetAccessPermission(userId, pageId, "S", …)`.
  - On denial: redirects (unauthenticated) or returns a 403 "You don't have permission to access…" message.
- **Assignment UI:** `Areas/UserAccess/Controllers/UserWiseReportAccessController` (`[UserWisePageAccess(4201, …)]`):
  - `SelectReportPages()` → `ReportService.SelectReportNames()` lists all reports.
  - `Save(UserWiseReportsAccess)` → `UserWiseReportAccessService.Save` (SP `UserWiseReportsAccess_M_Save`).
  - `SelectPagesByUser(userId)` → SP `UserWiseReportsAccess_M_SelectPagesByUser`.
- **Storage:** table **`UserWiseReportAccess`** (`Id`, `UserId`, `ReportId`). Access-change auditing via `UserWisePageAndReportAccessLog`.

---

## The report registry — `ReportDetails`

The SSRS catalogue is data-driven. Table **`ReportDetails`** (219 rows; **207 active**) is the master registry. Key columns:

| Column | Purpose |
|---|---|
| `ReportName` / `DisplayName` | Internal key / menu label |
| `ReportSPName` | Backing stored procedure (or `SP` when the `.rdl` embeds its own query) |
| `ReportViewerWidth` | Viewer width |
| `ReportCategory` | Menu grouping (numeric 1–8, see below) |
| `Param*` flags (`ParamFromDate`, `ParamArrival`, `ParamCompany`, `ParamSegment`, `ParamSalesPerson`, `ParamRoomBoy`, `ParamPaymentType`, `ParamProfitCenter`, …) | Which filter inputs to render for this report |
| `Show*` flags (`ShowExportControls`, `ShowPrintButton`, `ShowToolBar`, …) | ReportViewer toolbar behaviour |
| `DocType`, `IsDirectPrint`, `IsPrintCopy`, `IsLKROnlyInvoice`, `IsBreifInvoice` | Document-type behaviour |

The numeric `ReportCategory` values map (from the active `DisplayName` groupings) to:

| Cat | Meaning | Count (active) |
|---|---|---|
| 1 | Reservation / Arrival–Departure operational lists | 49 |
| 2 | Occupancy | 16 |
| 3 | Forecast | 6 |
| 4 | Revenue (accommodation, company, encashment, advances) | 24 |
| 5 | Printable documents (invoices, confirmations, registration, receipts) | 35 |
| 6 | Financial / management / night-audit (Daily Revenue, Manager, Hotel Statistics, ARR/ADR/RevPAR, ledgers) | 27 |
| 7 | Guest, housekeeping, telephone, transport, misc | 42 |
| 8 | Guest In-House / Information Sheet | 20 |

## Stored-procedure inventory

The reporting SPs verified against `HotelResWeb_Browns`:

| Group (name prefix / pattern) | Count | Role |
|---|---|---|
| `Report*` + `Reports*` | **406** | Report data SPs (the report catalogue backbone) |
| `DashboardAPI_*` | 193 | DataAnalysis dashboard cards/charts/tables |
| `Analysis_*` | 9 | DataAnalysis forecast/analysis feeds |
| `Dashboard_*` (legacy) | ~12 | Older dashboard occupancy/revenue feeds |

> Many report SPs have dated/dev twins (`_OLD`, `_Dev`, `_TEST`, `_Parameterized`, `_20250813`, `_Browns`, etc.). Treat the un-suffixed name as canonical; `_Parameterized` variants take an explicit `@PropertyId`. Only representative, verified names are listed in the catalogue below — the full list is not reproduced.

---

## REPORT CATALOG

Reports below were confirmed either in `ReportDetails` (`DisplayName` → `ReportSPName`) and/or as existing procedures in the live DB. "Source" gives the controller/action and/or SP (SSRS unless noted DevExpress).

### Financial reports (folio, revenue, tax, GL, cashier/settlement, day-end)

| Report name | Purpose | Department | Key filters | Business information provided | Source (controller/SP or SSRS) |
|---|---|---|---|---|---|
| Daily Revenue Report | Trading-day revenue breakdown by department/charge | Night audit / Finance | Date | Room, F&B and other revenue for the day; feeds GL | SSRS · `Report_DailyRevenueReport`, `Report_DailyRevenueReport_Summary` |
| DAILY REPORT (Browns) | Consolidated daily management figures | Management | Date | Occupancy + revenue snapshot | SSRS · `Report_DailyRevenueReport_Summary_Browns` |
| Day-End Summary | Night-audit close summary | Night audit | Date | Cash/credit ledger balances at day close | SSRS · `Report_Day_End_Summary`, `Report_DayEndSummary_CashAndCrd` |
| Guest Ledger | Outstanding in-house guest balances (trial balance) | Finance / audit | Date | Per-folio ledger balances | SSRS · `Report_GuestLedger`, `Report_Get_GuestLedger` |
| Guest Billing Journals | Journal of billing transactions | Finance | Date range | Posting/billing journal entries | SSRS · `Report_BillingJurnal` |
| Guest Account Journals / Sales of the Day Journal | Accommodation & day posting journals | Finance | Date range | Charge journals for the day | SSRS · `Report_RoomSales`, `Report_RoomRevSum` |
| Invoice Tax / Invoice Settlements | Tax on invoices, settlement breakdown | Finance / audit | Date range | VAT/SC/TDL per invoice; how invoices were paid | SSRS · `Report_InvoiceTax`, `Report_InvoiceSettelements` |
| Payment Type Wise / Payment Wise Summary | Sales grouped by payment method | Cashier / Finance | Date range, payment type | Cash vs card vs city-ledger totals | SSRS · `Report_PaymentTypeWise`, `Report_PaymentWiseSummary` |
| Bill Type Wise Sales | Extra-posting sales by bill type | Finance | Date range | Bill-type revenue split | SSRS · `Report_BillTypeWiseSales` |
| Bank Deposit | Bankable cash/cheque deposit slip | Cashier / Finance | Date | Amounts to bank | SSRS · `Report_BankDeposit` |
| Miscellaneous Billing Detail | Non-room extra postings | Finance | Date range | Misc. charge detail | SSRS · `Report_NewMiscellaneousBillingSummary` |
| VAT Upload Schedule | Tax authority upload schedule | Finance | Date range | VAT return data | SSRS · `Report_VATUploadSchedule` |

### Occupancy reports

| Report name | Purpose | Department | Key filters | Business information provided | Source |
|---|---|---|---|---|---|
| Occupancy by Room Nights (Agent/Country/Market/Nationality/RateCode/Segment wise) | Room-nights occupancy sliced by dimension | Revenue / Reservations | Date range + dimension | Room nights & occupancy % per agent/country/segment… | SSRS · `Report_OccupancyByRoomNights` (`…_Parameterized`) |
| Occupancy by Pax (…wise) | Guest-nights (pax) occupancy by dimension | Revenue | Date range + dimension | Guest nights per dimension | SSRS · `Report_OccupancyByPax` |
| Occupancy Daily | Day-by-day occupancy | Revenue / Reservations | Date range | Daily rooms sold, occupancy % | SSRS · `Reports_OccupancyDaily` (`…_Common`, `…_Parameterized`) |
| On The Book | Rooms/revenue currently on the books | Revenue | As-of / range | Confirmed future business on hand | SSRS · `Report_OnTheBook` |
| Monthly Average Occupancy (with/without complimentary room nights) | Monthly occupancy incl./excl. comps | Management | Month/range | Average occupancy %, comp impact | SSRS · `Report_MonthlyAverageOccupancy_WithAndWithoutComplimentaryRoomNights` |
| Property-wise Occupancy Summary (MTD/Today) | Multi-property occupancy roll-up | Management | Date, property | Occupancy % per property | SSRS · `Report_PropertyWiseOccupancySummary_MTD/_Today` |
| Room Availability Summary | Rooms available/sold/OOO | Reservations / FO | Date, property | Availability snapshot | SSRS · `ReportRoomAvailabilitySummary` (special `PropertyId` param) |

### Revenue reports (ADR / RevPAR, revenue by segment / source / agent)

| Report name | Purpose | Department | Key filters | Business information provided | Source |
|---|---|---|---|---|---|
| ARR / ADR / RevPar Analysis | Average Room Rate, Average Daily Rate, Revenue per Available Room | Revenue / Management | From date, date, property | ARR, ADR, RevPAR trend | SSRS · `Report_ARR_ADR_RevPar_Analysis` (verified: params `@FromDate, @Date, @PropertyId`); also `ReportRevPAR` |
| Accommodation Revenue by (Company/Country/Market/MealPlan/RateCode/Room/Room Category/Segment) wise | Room revenue sliced by dimension | Revenue | Date range + dimension | Revenue per segment/company/country… | SSRS · `Report_RevenueDetails`, `Report_RevenueDetailsCommon` |
| Accommodation Revenue Detail / Summary | Room-sales revenue detail & summary | Revenue | Date range | Room revenue detail & totals | SSRS · `Report_RoomSales`, `Report_RoomRevSum` |
| Room Nights by Agent / Agent Wise Room Revenue | Room nights & revenue produced per travel agent/OTA | Sales | Date | Agent production ranking (room nights, revenue) | SSRS · `Reports_AgentWiseRoomRevenue` (a.k.a. "Room Nights by Agent Report" per graph); `Dashboard_AgentWiseRoomRevenue` |
| Agent Performance Summary | Agent production summary | Sales | Date range | Bookings, room nights, revenue by agent | SSRS · `Report_AgentPerformanceSummary`, `ReportAgentsProduction` |
| Company Wise Revenue (Daywise / Date range) | Revenue by corporate account | Sales / Finance | Date range, company | Corporate revenue contribution | SSRS · `Reports_CompanywiseRevenue` |
| Sales Person Wise Revenue / Statistics | Revenue & KPIs per sales person | Sales | Date range, sales person | Sales-person production | SSRS · `Report_SalesPersonWiseRevenue`, `Report_SalesPersonWiseStatistics` |
| Room Category Wise Tour Operator Performance | TO performance by room category | Sales | Date range | Tour-operator room-category production | SSRS · `Report_RoomCategoryWiseTourOperatorPerformance` |
| Nationality Wise Guest Nights / Extra F&B Revenue | Guest nights & F&B revenue by nationality | Revenue | Date range | Nationality contribution | SSRS · `Reports_NationalityWiseGuestNights_Actual`, `Report_NationalityWiseExtraFandBRevenue` |
| Segment Wise Revenue with Budget / PMS Segments Accommodation Revenue Budget | Revenue vs budget by segment | Revenue / Management | Date range | Actual vs budget by market segment | SSRS · `Report_SegmentWise_RevenueDetailsWithBudget`, `Report_PMSSegments_AccommodationRevenueBudget_Report` |

### Arrival & departure reports (arrivals, departures, in-house)

| Report name | Purpose | Department | Key filters | Business information provided | Source |
|---|---|---|---|---|---|
| Arrival Report / Expected Arrival Details | Guests arriving | Front office | Date | Today's/expected arrivals with room, rate, agent | SSRS · `Getthesearrivals` / `Getthesearrived` |
| Daily Arrival Report | Detailed daily arrival list | Front office | Date | Arrival detail | SSRS · `Report_DailyArrivalDetail` |
| Departure / Expected Departure Report | Guests departing | Front office | Date | Departures with balance/settlement status | SSRS · `GettheseDepartures` / `GettheseExpectedDepartures` |
| Day Wise Arrival / Departure Summary | Arrival/departure counts by day | Front office | Date range | Arrival/departure volumes | SSRS · `Report_DayWiseArrivalOrDepatureSummary` |
| Guest Arrival / Departure Alphabetically | Alphabetical arrival/departure lists | Front office | Date | Sorted arrival/departure roster | DevExpress · `Reservation/GuestArrivalAlphabetically`, `…Departure…` |
| In-House Room Summary | Rooms currently occupied summary | Front office | As-of | In-house room roster | DevExpress · `Reservation/InHouseRoomSummary` (`GetInHouseRoomsSummarySP`) |
| Guest In House (With/Without Rates) | Full in-house guest list | Front office | Date | In-house guests, rooms, rates, agent | SSRS (Category 8) · `ReportInHouse_ReservationHeaders`, `Reports_InHouseGuests` |
| Information Sheet / Summary | Daily FO information sheet (arrivals/stayovers/departures/counts) | Front office / Management | Date | Consolidated day sheet | SSRS · `Report_InformationSheet*`, `Reports_InformationSummary` |

### Guest reports (history, country/nationality, VIP, birthday)

| Report name | Purpose | Department | Key filters | Business information provided | Source |
|---|---|---|---|---|---|
| Guest History | Past-stay history for a guest | Guest relations | Guest / date range | Stay history, spend, preferences | SSRS · `ReportGuestHistory` |
| Guest Profile By Country / Nationality | Guests grouped by country/nationality | Guest relations / Revenue | Date range, country | Source-market analysis | SSRS · `Reports_GuestInHouseReservationCountryWise`, `…NationaltyWise` |
| Guest Profile - VIP List | VIP guests | Guest relations | Date | VIP guest roster | SSRS · `Report_GuestDetails_VIP` |
| Guest Birthday Details / In-House Birthday | Guests with birthdays (arriving/in-house/reservation) | Guest relations | Date | Birthday list for recognition | SSRS · `ReportGuestBirthdayInhouse`, `ReportGuestBirthdayReservation`, `Report_GuestinHouse_BirthdayDetails` |
| Guest Repeaters | Returning/repeat guests | Marketing | Date range | Loyalty/repeat analysis | SSRS · `Rpt_GuestReservationRepiters` |
| Alphabet / Email Wise Guest Details | Guest contact lists | Marketing | Filter | Contact/email lists for campaigns | SSRS · `Report_Guest_Profile_List`, `Report_Guest_Profile_EmailList` |
| Allergies Details | Guest allergy/dietary notes | F&B / Guest relations | Date | In-house allergy alerts | SSRS · `Report_GuestAllergies` |
| Guest Balance Analysis (Short) | Outstanding guest balances | Finance / FO | As-of | High-balance alerts | SSRS · `Report_GuestBalanceAnalysisShortFormat`, `Reports_GuestBalanceAnalysis` |
| Police / Tourist-Board Report | Statutory guest registration returns | Front office / Compliance | Date | Guest data for authorities | SSRS · `Rpt_GuestPoliceReports`, `Reports_Tourist_Board_Statistics` |

### Cashier reports (returns, encashment, advances)

| Report name | Purpose | Department | Key filters | Business information provided | Source |
|---|---|---|---|---|---|
| Cashier Returns | Cashier return-sales/refunds | Cashier | Date range | Refunds/returns by cashier | SSRS · `Report_CashierReturnSales` |
| Currency Encashment Details / Summary / Receipt | Foreign-currency exchange transactions | Cashier | Date range | Encashment amounts, rates | SSRS · `Report_Currency_Encashment_Details`, `Report_Currency_Encashment_Receipt` |
| Cash Encashment | Cash encashment listing | Cashier | Date range | Cash encashment detail | SSRS · `Report_CashEncashment` |
| Advance Payment / Advance Details | Deposits/advances received | Cashier / Reservations | Date range | Advance receipts & balances | SSRS · `Report_Rebate` (advance receipt), `Reports_Advance_Receipt`, `Reports_AdvanceDetails_Reservation` |
| Rebate Receipt / Rebate Details | Rebate/allowance transactions | Cashier / Audit | Date range | Rebate audit trail | SSRS · `Report_Rebate_Receipt`, `Report_RebateDetails` |
| Advance & Refund with Opening Balance | Advance ledger with opening balance | Finance | Date range | Advance movement | SSRS · `Report_AdvanceAndRefundWithOpeningBalance` |

### Housekeeping reports (room status, discrepancy, OOO)

| Report name | Purpose | Department | Key filters | Business information provided | Source |
|---|---|---|---|---|---|
| Housekeeping Room Wise Status | Current HK status per room | Housekeeping | As-of | Clean/dirty/inspected/occupied status | SSRS · `Report_HouseKeepingStatus` |
| Housekeeping Discrepancy | FO vs HK room-status mismatches | Housekeeping / FO | Date | Skips/sleeps/discrepancies | SSRS · `Reports_HouseKeepingDiscrepancy` |
| Out Of Order Room Details | Rooms blocked OOO/OOS | Housekeeping / Maintenance | Date range | OOO rooms & reasons | SSRS · `Report_OutOfOrder`, `Report_OutOfOrderRoomDetails`, `Reports_OutOfOrderRoom_Details` |
| Housekeeping Room Wise Room Boys | Room-boy assignment sheet | Housekeeping | Date | Room-to-attendant allocation | SSRS · `Report_Housekeeping_RoomWiseRoomBoys` |
| Room Change / Room Upgrade Details | Room moves & upgrades | Housekeeping / FO | Date range | Room-change/upgrade log | SSRS · `Report_RoomChangeDetails`, `Reports_RoomChange_Details` |
| Lost And Found Details | Lost-and-found register | Housekeeping | Date range | LAF items & status | SSRS · `Report_LostAndFound`, `Report_LostAndFoundDetails` |
| Damage Request | Room/asset damage requests | Housekeeping / Maintenance | Date range | Damage records | SSRS · `Report_Damage_Request` |

### Audit reports (audit trail, night-audit, void/rebate/discount logs)

| Report name | Purpose | Department | Key filters | Business information provided | Source |
|---|---|---|---|---|---|
| Hotel Statistics | Night-audit statistical KPI sheet | Night audit / Management | Date | Occupancy, ADR, revenue, pax KPIs | SSRS · `Reports_HotelStatistics_NEW` (view label "Hotel Statistics") |
| Manager Report | Consolidated management report | Management | Date | Key operational & financial figures | SSRS · `Reports_ManagerReport`, `Reports_ManagerReportSub` |
| Folio Voids / Extra Posting Voids | Voided folios & extra postings | Audit | Date range | Void audit trail (who/what/when) | SSRS · `Reports_Void_Folio_Details`, `Reports_Void_ExtraPosting_Details` |
| Void Bill Listing / Void Currency Encashment | Voided bills & encashments | Audit | Date range | Voided transactions | SSRS · `Report_VoidBillListing`, `Report_Void_Currency_Encashment_Details` |
| Discount / Discounted Invoices / FO Discount | Discounts & allowances granted | Audit / Finance | Date range | Discount audit (amount, authoriser) | SSRS · `Report_Discount`, `Report_DiscountDetails`, `Report_FODiscount` |
| Rebate Details | Rebate/adjustment audit | Audit | Date range | Rebate log | SSRS · `Report_RebateDetails` |
| User Access / User Roles Details | User permission snapshot | IT / Audit | — | Who can access what | SSRS · `Reports_UserWiseAccess_Details`, `Reports_UserAccessRole_Details` |
| Trace Log / User Changes Log / Room Rate Change Log | Change/trace logs | Audit | Date range | System change audit | SSRS · `Report_Trace_Log`, `Report_UserChanges_Log`, `Report_ReservationRoomRateChangeLog_Select` |
| Down Time Report (Pending Folios) | Folios pending at down-time cutoff | Night audit | Date | Unposted/pending folios | SSRS · `Report_DowntimeReport_PendingFolios` |

### Forecast reports

| Report name | Purpose | Department | Key filters | Business information provided | Source |
|---|---|---|---|---|---|
| Forecast Weekly | 7-day rooms/occupancy forecast | Revenue / Reservations | From/To date | Weekly rooms & occupancy outlook | SSRS · `Report_ForecastWeekly` |
| Room Category Wise Forecast | Forecast by room category | Revenue | Date range | Category-level availability outlook | SSRS · `Reports_RoomCategoryWise_ForecastSummary` |
| Reservation Room Forecast / Actuals | Forecast vs actual room nights | Revenue | Date range | Forecast accuracy | SSRS · `Reports_ReservationRoomNight`, `Reports_ReservationRoomNight_Actual` |
| Market Forecast | Market-level forecast | Revenue | Date range | Demand outlook by market | SSRS · `ReportMarketForecast` |
| Room-type-wise Forecast | Forecast by room type | Reservations | From/To, status | Room-type availability outlook | DevExpress · `Reservation/RoomtypeWiseForeCastView` |

---

## Data-analysis dashboards

`Areas/DataAnalysis` provides interactive analytics separate from the printable report catalogue.

### DataAnalysis pages (`DataAnalysisController` + `DataAnalysisService`)

Each landing page is a view guarded by `[UserWisePageAccess(<id>, "S")]`; the chart data is fetched via JSON actions that call `DataAnalysisService` → `DataAnalysisEntry` → an `Analysis_*` SP:

| Page action (pageId) | JSON feed action | Service method | SP |
|---|---|---|---|
| `RoomNightsByCountryDateRange` (12020) | `AnalysisInformation` | `RoomNightAnalysisCountry` | `Analysis_RoomNight_GuestNightByCountry` |
| `GuestNightsByCountryDateRange` (12021) | `AnalysisInformation` | (same, area switch) | `Analysis_RoomNight_GuestNightByCountry` |
| `GuestCountByCountry` (12022) | `GuestBaseAnalysis` | `GuestBaseAnalysis` | `Analysis_GuestCountByCountry` |
| `OccupancyAnalysisForecast` (12024) | `DailyOcupancyForecastAnalysis` | `OccupanyAnalysisDaily` | `Analysis_DailyOcupancy` |
| `RoomGuestNightsAnalysisForecast` (12025) | `DailyGuestRoomNightForecastAnalysis` | `DailyGuestRoomNightForecastAnalysis` | `Analysis_DailyGuestRoomNights` |
| `RoomPickupAnalysisForecast` (12026) | `DailyRoomPickupForecastAnalysis` | `DailyRoomPickupForecastAnalysis` | `Analysis_DailyRoomPickups` |
| `MonthlyRoomPickupAnalysisForecast` (12027) | `MonthlyRoomPickupForecastAnalysis` | `MonthlyRoomPickupForecastAnalysis` | `Analysis_MonthlyRoomPickups` |
| `MonthlyRoomGuestNightsAnalysis` (12028) | `MonthlyRoomNightGuestNightsAnalysis` | `MonthlyRoomGuestNightsAnalysis` | `Analysis_MonthlyGuestRoomNights` |

### `DashboardAPI_*` SPs (mini-dashboard / management dashboard)

193 `DashboardAPI_*` procedures feed a management dashboard of KPI cards, charts and drill-down tables. Representative verified examples:

| Dashboard area | Representative SPs |
|---|---|
| Occupancy | `DashboardAPI_OccupancyData_Select`, `DashboardAPI_OccupancyDaily_ForDashboardAPI_Chart`, `DashboardAPI_Select_MonthlyOccupancyStatistics_Chart` |
| ADR / ARR / RevPAR / RevPAC | `DashboardAPI_MonthlyADR_Select_Chart`, `DashboardAPI_MonthlyARR_Select_Chart`, `DashboardAPI_MonthlyRevPARAnalysis_Select_Chart`, `DashboardAPI_MonthlyRevPACAnalysis_Select_Chart` |
| Profit (GOP/NOP) | `DashboardAPI_MonthlyGOP_Select_Chart`, `DashboardAPI_MonthlyNOP_Select_Chart`, `DashboardAPI_Select_GOPNOPCardFigures` |
| Revenue (room/food/beverage/total) | `DashboardAPI_RoomRevenueYear_Select`, `DashboardAPI_FoodRevenueYear_Select`, `DashboardAPI_BeverageRevenueYear_Select`, `DashboardAPI_TotalRevenueYear_Select`, `DashboardAPI_RevenueForecast_Select_Chart` |
| Agent / country / nationality / rate-code / room-category analysis | `DashboardAPI_AgentRoomNightsAnalysis_Select_Chart`, `DashboardAPI_CountryRoomNightsAnalysis_Select_Chart`, `DashboardAPI_NationalityRoomNightsAnalysis_Select_Chart`, `DashboardAPI_RateCodeRoomNightsAnalysis_Select_Chart`, `DashboardAPI_RoomCategoryRoomNightsAnalysis_Select_Chart` |
| Length of stay / arrivals-departures | `DashboardAPI_Select_AverageLengthOfStay_Chart`, `DashboardAPI_DayArrivalsStayOversDepartures_Select`, `DashboardAPI_RoomAvailability_Today_ArrivedStayOversDeparted` |
| Outlet / menu-engineering (POS) | `DashboardAPI_MonthlyOutletSales_Select_Chart`, `DashboardAPI_OutletSalesMix_Select_Chart`, `DashboardAPI_MenuEngineeringMatrix_Stars_ForDashboardAPI_Chart_*` |
| Revenue-management card figures | `DashboardAPI_Select_RevenueManagementCardFigures`, `DashboardAPI_Select_YeildManagementCardFigures`, `DashboardAPI_RevenueManagement_Select_Table` |

> **Note:** the .cshtml/JS that render the `DashboardAPI_*` cards and the controller wiring for the mini-dashboard were **not read in this pass** — the SP layer is confirmed in the live DB, but the exact front-end controller/action for each `DashboardAPI_*` SP is **Not found in this pass** (searched `Areas/DataAnalysis/Controllers` — it only wires the `Analysis_*` SPs above; the `DashboardAPI_*` consumers likely live elsewhere/in a separate dashboard app).

---

## Database / API involvement (summary)

| Concern | Object |
|---|---|
| Report registry | Table `ReportDetails` (207 active); SP `Report_Select_ReportNames`, `Report_Parameters_byReportName`, `ReportDetails_M_SelectByReportName` |
| Report data | 406 `Report*`/`Reports*` SPs |
| SSRS rendering | `ReportTemplate.aspx` (`Microsoft.Reporting.WebForms.ReportViewer`), server `ReportServer` + folder `SSRSReportsFolder`, credentials `DestinityReportServerCredentials` |
| Batch PDF | `ReportDownloader` → `ReportExecutionService`; SPs `HK_DocumentsToDownload`, `HK_DocumentsToDownload_UpdateStatus` |
| Report access | Table `UserWiseReportAccess`; SPs `UserWiseReportsAccess_M_Save`, `UserWiseReportsAccess_M_SelectPagesByUser`; log `UserWisePageAndReportAccessLog` |
| Print copy tracking | Table `ReportPrintCopyLog`; SP `ReportPrintCopyLog_Insert` |
| Dashboards | 193 `DashboardAPI_*` + 9 `Analysis_*` SPs |

## Business rules

- Reports are **property-scoped**: `PropertyId` is always passed from the logged property (except `ReportRoomAvailabilitySummary` which accepts an explicit `PropertyId`).
- Report visibility is **per-user** via `UserWiseReportAccess`, enforced by the `UserWiseReportAccess` authorize attribute (central-API or local check).
- Which filter inputs appear for a report is **data-driven** by the `Param*` flags in `ReportDetails`, not hard-coded per report.
- Invoice-type documents track reprints (`ReportPrintCopyLog`) and support preview vs final (`IsPreview`), LKR-only invoice (`IsLKROnlyInvoice`) and brief-invoice (`IsBreifInvoice`) modes.

## Error scenarios

- **No report access** → 403 "You don't have permission to access…" (AJAX) or redirect (non-AJAX) from `UserWiseReportAccess`.
- **SSRS server unreachable / missing `.rdl`** → ReportViewer surfaces an SSRS error; `ReportController.Error` view shows the message.
- **Missing parameter** → the report SP/`.rdl` errors; the viewer shows the failure (no app-level pre-validation beyond required inputs).

## Related documents

- `03-reservation-process.md` — reservation data behind reservation/arrival reports.
- `05-cashiering-and-finance-process.md` — folios, postings, day-end feeding financial/audit reports.
- `06-rooms-and-housekeeping-process.md` — room status behind housekeeping reports.
- `12-database-and-technical-architecture.md` — DB/SP conventions, connection strings.

---

### "Not found in the project" items (where checked)

- **EPPlus / Select.HtmlToPdf direct use in reporting controllers** — packages exist and are used elsewhere in the app, but no direct call in `Areas/Reporting/**/*.cs` (grid export uses DevExpress `DocumentViewerExtension.ExportTo`).
- **Front-end wiring for `DashboardAPI_*` SPs** — the SPs are confirmed in the DB; the specific controller/action/view that consumes each is not present in `Areas/DataAnalysis/Controllers` (only the `Analysis_*` feeds are wired there). Not located in this pass.
- **`ReportViewerWebControlHandler` standalone config** — present in `Web.config` as an `httpHandlers`/`handlers` registration (`Reserved.ReportViewerWebControl.axd`), not a separate file.
- **Named report-category lookup table** — `ReportCategory` is a numeric code (1–8) in `ReportDetails`; no category-name master table found (searched `sys.tables` for `%Category%`/`%ReportMenu%`).
