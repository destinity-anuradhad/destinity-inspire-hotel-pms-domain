# 08 — Administration & Configuration Process

> **Module:** `Areas/Administration` (the master configuration module of the Front Office PMS)
> **Product:** Scienter HotelERP — Destinity Inspire / Destinity Horizon Front Office
> **Scope of this document:** everything a system administrator sets up *before* the hotel can take a reservation, post a charge, or run a report. This is the "back-of-house control panel" of the PMS.

---

## Purpose

The **Administration module** is where the hotel's operating rules are defined once and then reused everywhere else in the system. Reservations, cashiering, housekeeping, and reporting all read from the master data configured here. Nothing in the PMS is hard-coded — room types, rates, taxes, charge codes, payment modes, meal plans, market segments, departments, and feature switches are all **data-driven** and maintained from Administration screens.

**Business meaning:** think of Administration as the hotel's rulebook. When a receptionist creates a booking and the system automatically calculates VAT + Service Charge, applies a rate for the season, offers a Bed & Breakfast meal plan, and posts the room charge to the correct ledger — every one of those behaviours came from a record an administrator entered in this module.

**Technical structure:** the module contains **108 controllers** in
`Scienter.HotelERP.FrontOffice.WebUIMvc/Areas/Administration/Controllers/`.
Each controller follows the same 3-tier pattern:

```
Controller (Areas/Administration/Controllers/<Name>Controller.cs)
      │  instantiates
      ▼
Service  (Scienter.HotelERP.FrontOffice.Service/<Name>Service.cs)
      │  instantiates
      ▼
Entry    (Scienter.HotelERP.Common.Data/<Name>Entry.cs)
      │  calls
      ▼
Stored Procedure  (<Table>_M_Save / _Select / _Delete / _Update …)
      │  reads / writes
      ▼
Table    (SQL Server — HotelResWeb_<Property>)
```

The naming convention (from the Research Pack §6) is `<Domain>_M_<Action>` where **`M` = Master data**. Almost every configuration table has a matching set of SPs `<Table>_M_Save`, `<Table>_M_Select`, `<Table>_M_Delete`.

---

## Relevant users / departments

| Who | Why they use Administration |
|---|---|
| **System Administrator / Property IT** (roles `Admin`, `Property IT`, `HO IT`) | Full configuration — property, rooms, rates, taxes, users, settings |
| **Revenue Manager** | Rate codes, seasons, room rates, child-age rates, market/segment setup |
| **Finance Controller / Chief Cashier** | Charge codes, posting categories, tax groups, payment modes, currencies |
| **Front Office Manager** | Front-office settings, guest profile types, VIP levels, cancellation policies |
| **Executive Housekeeper** | Housekeeping settings, room features/areas, out-of-order reasons |
| **Sales Manager** | Companies, company categories, company-wise markets/segments/rates |

> Access to each Administration screen is controlled by the permission model documented in **`09-user-roles-and-permissions.md`**. Every action here is protected by a `[UserWisePageAccess(pageId, "S/I/U/D")]` attribute.

---

## Preconditions

1. The user is authenticated (via central SSO or local login — see doc 09).
2. The user's role (or individual access) grants the relevant page permission.
3. A **Property** exists (`Properties`) — this is the root of all other configuration, because most master tables carry a `PropertyId` and are configured **per property** in this multi-tenant system.
4. For dependent data, parents must exist first (e.g. a `RoomType` before a `RoomRate`; a `TaxType` before a `TaxGroupDetail`; a `Season` before seasonal rates).

---

## The configuration order (recommended setup sequence)

```
1. PROPERTY            Properties
        │
2. PHYSICAL LAYOUT     Floors → RoomCategories → RoomTypes → BedTypes
        │              → RoomFeatures → RoomAreas → RoomDetails (actual rooms)
        │
3. COMMERCIAL MODEL    Seasons → RateCodeHeaders → RoomRates
        │              → RoomRatesForChildAge → MealPlans → MealTimes
        │
4. FINANCE BACKBONE    TaxTypes → TaxGroups → TaxGroupDetails
        │              → ChargeTypes → ChargeCodes → PostingCategories
        │              → PostingTypes → PostingRhythms → ModulePostings
        │
5. PAYMENT             PaymentModes → GuestPaymentModes → PaymentPolicies
        │              → Currencies → CurrencyConversion
        │
6. GUEST & MARKET      GuestProfileType / VIPLevels / Salutations / Genders
        │              / Nationalities / Countries / Languages / ProfileStatuses
        │              Markets → Segments → BookingSources
        │
7. ORGANISATION        Departments → Designations → StaffCategories
        │              → Employees → StaffDetails
        │              Companies → CompanyCategories → CompanyWise* links
        │
8. SYSTEM BEHAVIOUR    FrontOfficeSettings (FOSettings + SystemSettings)
                       BookingSettings, HKSettings, EmailSettings
```

Each numbered layer depends on the layers above it.

---

## Master configuration reference table

The table below is the core of this document: every major configuration item, the **controller** that manages it, the **primary table(s)** it writes to, the **stored-procedure prefix**, and the **business purpose**. All controllers live in `Areas/Administration/Controllers/`; all Entry classes in `Scienter.HotelERP.Common.Data/`; all Services in `Scienter.HotelERP.FrontOffice.Service/`.

> **Convention note:** SPs follow `<Table>_M_<Action>`. Where the exact table/SP name was verified against the live DB or the `*Entry.cs` source it is stated as canonical; where only the code pattern was observed the standard `_M_` prefix is shown. Verify the precise SP name in the relevant `*Entry.cs` before relying on it in scripts.

### A. Property / hotel setup

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Property master | `PropertiesController` | `Properties` (12 rows live — one per hotel in the chain) | `Properties_M_` | The hotel itself: name, prefix/code, logo, current business date, DB connection, renewal date. Root of the multi-property model — nearly every other table has a `PropertyId`. |

### B. Rooms & physical layout

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Floors | `FloorsController` | `Floors` | `Floors_M_` | Physical floors used to organise rooms. |
| Room categories | `RoomCategoriesController` | `RoomCategories` | `RoomCategories_M_` | Broad grouping of rooms (e.g. Standard / Deluxe / Suite) with images. |
| Room types | `RoomTypesController` | `RoomTypes` | `RoomTypes_M_` | The sellable room type (drives rates & availability). PageId **41**. |
| Bed types | `BedTypesController` | `BedTypes` | `BedTypes_M_` | Single / Double / King / Queen options per room. |
| Room features | `RoomFeaturesController` | `RoomFeatures` | `RoomFeatures_M_` | Amenities catalogue (sea view, balcony, minibar…). |
| Room areas | `RoomAreasController` | `RoomAreas` | `RoomAreas_M_` | Zones/sections within a room or property. |
| Actual rooms | `RoomDetailsController` | `RoomDetails` | `RoomDetails_M_` | The individual physical rooms (room number → type/category/floor/features). |

### C. Rates & pricing

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Seasons | `SeasonsController` | `Seasons` | `Seasons_M_` | Date periods that change pricing (peak/off-peak). |
| Rate code headers | `RateCodeHeadersController` | `RateCodeHeader` | `RateCodeHeaders_M_` | Named rate plans (BAR, Corporate, Promo) with rules. |
| Room rates | `RoomRatesController` | `RoomRates` | `RoomRates_M_` | The actual price by room type / rate code / season / meal plan. |
| Child-age rates | `RoomRatesForChildAgeController` | `RoomRatesForChildAge` | `RoomRatesForChildAge_M_` | Age-banded child pricing. |
| Promotions | (`RoomRates_PromotionSettings` table) | `RoomRates_PromotionSettings` | — | Promotion parameters attached to rates. |

### D. Meal plans

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Meal plans | `MealPlansController` | `MealPlans` | `MealPlans_M_` | RO / BB / HB / FB / AI packages tied to rates. |
| Meal times | `MealTimesController` | `MealTimes` | `MealTimes_M_` | Service windows for breakfast/lunch/dinner. |

### E. Tax

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Tax types | `TaxTypesController` | `TaxTypes` | `TaxTypes_M_` | Individual taxes (VAT, Service Charge, TDL, SSCL…). |
| Tax groups | `TaxGroupsController` | `TaxGroups` | `TaxGroups_M_` | A bundle of taxes applied together to a charge. |
| Tax group details | `TaxGroupDetailsController` | `TaxGroupDetails` | `TaxGroupDetails_M_` | Which tax types belong to which group, and order of application. |

> **Business meaning (Sri Lanka tax model):** a room charge is linked to a **tax group**; the group's **details** list the component taxes and their compounding order (e.g. Service Charge first, then VAT on top). This drives `FoliowiseTaxDetails` at posting time.

### F. Charges & posting backbone

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Charge types | `ChargeTypesController` | `ChargeTypes` | `ChargeTypes_M_` | High-level charge classification (room / F&B / incidental…). |
| Charge codes | `ChargeCodesController` | `ChargeCodes` | `ChargeCodes_M_` | Every postable item (Room, Laundry, Minibar…) with its tax group. |
| Posting categories | `PostingCategoriesController` | `PostingCategories` | `PostingCategories_M_` | Ledger buckets for revenue grouping. |
| Posting types | `PostingTypesController` | `PostingTypes` | `PostingTypes_M_` | Debit / Credit / Transfer / Adjustment behaviour. |
| Posting rhythms | `PostingRhythmsController` | `PostingRhythms` | `PostingRhythms_M_` | How often a charge auto-posts (per night, once, etc.). |
| Module postings | `ModulePostingsController` | `ModuleCategoryWiseItems` / module-posting tables | `ModulePostings_M_` | Maps modules (POS, spa, laundry) to their posting configuration. |

### G. Payment configuration

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Payment modes | `PaymentModesController` | `PaymentModes` | `PaymentModes_M_` | Cash / Card / Bank Transfer / City Ledger settlement methods. |
| Guest payment modes | `GuestPaymentModesController` | `GuestPaymentModes` | `GuestPaymentModes_M_` | Guest-selectable payment options (portal / IBE). |
| Payment policies | `PaymentPoliciesController` | `PaymentPolicies` | `PaymentPolicies_M_` | Deposit % and payment-terms rules. |
| Currencies | `CurrenciesController` | `Currencies` | `Currencies_M_` | Currency master + base currency (LKR) + symbols. |
| Currency conversion | `CurrencyConversionController` | `CurrencyConversion` | `CurrencyConversion_M_` | FX rates for foreign-currency folios/invoices. |

### H. Guest types & reference data

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Guest profile types | `GuestProfileTypeController` | `GuestProfileType` | `GuestProfileType_M_` | Corporate / Leisure / Group classification. |
| Profile statuses | `ProfileStatusesController` | `ProfileStatuses` | `ProfileStatuses_M_` | Lifecycle of a guest profile. |
| VIP levels | `VIPLevelsController` | `VIPLevels` | `VIPLevels_M_` | VIP tiers for service prioritisation. |
| Salutations | `SalutationsController` | `Salutations` | `Salutations_M_` | Mr / Mrs / Dr … name prefixes. |
| Genders | `GendersController` | `Genders` | `Genders_M_` | Gender options on profiles. |
| Nationalities | `NationalitiesController` | `Nationalities` | `Nationalities_M_` | Guest nationality list (statutory reporting). |
| Countries | `CountriesController` | `Countries` | `Countries_M_` | Country reference. |
| Languages | `LanguagesController` | `Languages` | `Languages_M_` | Guest language preference / document language. |

### I. Market, segment & booking source

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Markets | `MarketsController` | `Markets` | `Markets_M_` | Market of business (Web, GDS, Tour Operator…). |
| Segments | `SegmentsController` | `Segments` | `Segments_M_` | Business / Leisure / Group segmentation for statistics. |
| Booking sources | `BookingSourcesController` | `BookingSources` | `BookingSources_M_` | Channel of the booking (Direct, OTA, Agent…). |
| Company-wise markets | `CompanyWiseMarketsController` | `CompanyWiseMarkets` | `CompanyWiseMarkets_M_` | Default market per company/agent. |
| Company-wise segments | `CompanyWiseSegmentsController` | `CompanyWiseSegments` | `CompanyWiseSegments_M_` | Default segment per company/agent. |
| Company-wise rate codes | `CompanyWiseRateCodesController` | `CompanyWiseRateCodes` | `CompanyWiseRateCodes_M_` | Negotiated rates per company. |

### J. Departments, staff & organisation

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Departments | `DepartmentsController` | `Departments` | `Departments_M_` | Hotel departments (HK, F&B, FO…). |
| Designations | `DesignationsController` | `Designations` | `Designations_M_` | Job titles. |
| Staff categories | `StaffCategoriesController` | `StaffCategories` | `StaffCategories_M_` | Permanent / contract classification. |
| Employees | `EmployeesController` | `Employees` | `Employees_M_` | Employee master (a `User` is linked to an `EmployeeId`). |
| Staff details | `StaffDetailsController` | `StaffDetails` | `StaffDetails_M_` | Extended staff information/assignments. |

### K. Companies / agents

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Companies | `CompaniesController` | `Companies` (+ `CompanyActivityLog`) | `Companies_M_` | Corporate & travel-agent accounts (with approval workflow, gated by SystemSetting `Consider for company approval`). |
| Company categories | `CompanyCategoriesController` | `CompanyCategories` | `CompanyCategories_M_` | Company classification. |
| Company profile types | `CompanyProfileTypesController` | `CompanyProfileTypes` | `CompanyProfileTypes_M_` | Type of company profile. |
| Company contacts | `CompanyWiseContactsController` | `CompanyWiseContacts` | `CompanyWiseContacts_M_` | Contact persons per company. |

### L. Extensions, packages, laundry & other operational config

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Extensions | `ExtensionsController` | `Extensions` | `Extensions_M_` | Room telephone extensions. |
| Extension groups | `ExtensionGroupsController` | `ExtensionGroups` | `ExtensionGroups_M_` | Grouping of extensions. |
| Package headers | `PackageHeadersController` | `PackageHeaders` | `PackageHeaders_M_` | Package/offer definitions. |
| Package details | `PackageDetailsController` | `PackageDetails` | `PackageDetails_M_` | Line items and pricing within a package. |
| Laundry items | `LaundryItemsController` | `LaundryItems` | `LaundryItems_M_` | Laundry item master. |
| Laundry categories | `LaundryItemCategoriesController` | `LaundryItemCategories` | `LaundryItemCategories_M_` | Laundry item grouping. |
| Laundry charge types | `LaundryChargeTypesController` | `LaundryChargeTypes` | `LaundryChargeTypes_M_` | Laundry charge classification. |
| Laundry patterns | `LaundryPatternsController` | `LaundryPatterns` | `LaundryPatterns_M_` | Laundry service schedule/patterns. |

### M. Alerts, complaints, cancellation & attributes

| Config item | Controller | Table(s) | SP prefix | Business purpose |
|---|---|---|---|---|
| Alert types | `AlertTypesController` | `AlertTypes` | `AlertTypes_M_` | Types of guest/staff alerts. |
| Communication types | `CommunicationTypesController` | `CommunicationTypes` | `CommunicationTypes_M_` | Channels for notifications (email/SMS/phone) referenced by booking & IBE settings. |
| Complaint types | `ComplainTypesController` | `ComplainTypes` | `ComplainTypes_M_` | Complaint classification. |
| Complaint categories | `ComplainCategoryController` | `ComplainCategories` | `ComplainCategories_M_` | Complaint grouping. |
| Cancellation policies | `CancellationPoliciesController` | `CancellationPolicies` | `CancellationPolicies_M_` | Cancellation terms & penalties. |
| Cancellation reasons | `CancellationReasonsController` | `CancellationReasons` | `CancellationReasons_M_` | Standard cancel reasons for reporting. |
| Out-of-order reasons | `OutOfOrderReasonsController` | `OutOfOrderReasons` | `OutOfOrderReasons_M_` | Reasons a room is taken out of inventory. |
| Sensitivity levels | `SensitivityLevelController` | `SensitivityLevels` (live rows: Normal, Medium, High) | `SensitivityLevels_M_` | Classifies sensitivity of records/actions. |
| Severity levels | `SeverityLevelController` | `SeverityLevels` | `SeverityLevels_M_` | Severity scale for complaints/maintenance. |
| Colors / Attributes / Statuses | `ColorsController` / `AttributesController` / `StatusController` | `Colors` / `Attributes` / `Status` | `*_M_` | UI/label attributes used across screens. |
| Reservation status | `ReservationStatusController` | `ReservationStatus` | `ReservationStatus_M_` | Reservation lifecycle statuses. |
| Profit centre (config side) | `ProfitCenterController` | `Core_ProfitCenter*` | `ProfitCenter*_M_` | POS/outlet profit-centre setup (config side of POS). |

> The full list of 108 controllers includes further niche items (`TransferModes`, `TransferTypes`, `TransportAttributes`, `SalesCallCategories`, `VisitPurposes`, `IBESliderImages`, `Budget`, `Allotments`, `InventoryItems`, `RoomWiseInventoryItems`, `FrontOfficeInventory`, `FrontOfficeRoomStatus`, `Dashboard`/`DashboardMini`, `ProductTour`, `ServiceHub`, `UserWiseQuickNavigations`, `GuestComplain`, `GuestHistory`, `GuestInformation`, `GuestInquiry`, `GuestProfiles`, `LostAndFound`, `RoomBoyDetails`, `RoomInspectionDetails`, `Traces`, `AdvancedPayment`, `POSApi`, `Test`). Each follows the identical Controller → Service → Entry → `_M_` SP → Table pattern.

---

## System parameters / settings (the critical part)

Unlike the master tables above (list/CRUD data), the **settings** control *how the whole PMS behaves*. There are three "singleton-per-property" settings tables plus one key-value catalog. All were verified live in `HotelResWeb_Browns` (each holds **12 rows — one per property**, except the key-value catalog).

### 1. `FOSettings` — Front Office core operational settings

- **Controller:** `FrontOfficeSettingsController`
- **Service:** `FrontOfficeSettingService` (`SelectSettings()`)
- **Table:** `FOSettings` (12 rows)
- **Loaded into session** at login: `SessionObjects.FOSettings` is populated in `BaseController.CheckTokenValidity()` (line 84) so every request has the property's operating parameters in memory.
- **Verified columns include:** `BaseCurrencyISO`, `BaseName`, `CurrentDate` (the hotel business date), `CommissionPercentage`, `BillToRoomId`, `AdvancedPostingName`, `AdvancedPayment_taxtGroupId`, `AdvancedPayment_PostingCatgId`, `AdvancedPayment_ChargeCodeId`, `AdvancedPayment_PostingTypeId`, `PropertyId`.

**Business meaning:** `FOSettings.CurrentDate` is the "hotel date" that day-end (night audit) advances; the advance-payment charge/posting/tax IDs tell the system exactly which ledger to use when a deposit is taken.

### 2. `SystemSettings` — the feature-flag / parameter catalog

- **Table:** `SystemSettings` (**580 rows** live across all properties)
- **Structure (verified):** `Code nvarchar`, `Description nvarchar`, `PropertyId int`, `GroupId int`, `IsEnable bit`, `Value nvarchar` — i.e. a classic **key-value settings store**, evaluated per property.
- **Session cache:** `SessionObjects.SystemSettingsWiseProperties` (a `List<SystemSettings>`).
- **Feature-restriction SP** referenced in code: `SystemSettings_M_SelectForFeatureRestriction`.

**Sample live settings (Code group → Description), showing the breadth of behaviour it governs:**

| Group | Example flags (from live `Description`) |
|---|---|
| `SS0x` general | Consider tentative/dayuse/allotment for occupancy · Consider out of order · Consider for company approval · Consider for POS bill check · Consider for reservation profile creation |
| `SS1x` reservation | Is auto room allocation required · Is Banquet Module Enable · IsAutoRateUpdateRequiredOnConfirmation · IsHeadCountWiseGuestProfileRequired · Printing Method (D=Direct, R=…) · Is required guest profile validation |
| `SS2x` stay/billing | Is Allow early departure · Is Allow to change the ratecode after… · Is Required ESignature (Enable=1) · Meal allocation currency code · Package wise folio creation · Spa Inventory Item Id |
| `SS3x` occupancy | Consider checked out for occupancy · Exclude complimentary/dummy/house-use from occupancy numerator/denominator |
| `DSH0` dashboard | IsMiniDashboardEnable |
| `GPSS` / `GPPAy` guest portal | IsEnableGuestPortal · HNB IPG – Local/Foreign card mapping |
| `PT00` product tour | IsEnableProductTour |
| `SC00` | Consider for reservation / for room availability |

**Business meaning:** this single table is the master switchboard. Turning `Is Banquet Module Enable` on, changing the occupancy formula, enabling e-signature capture, or setting the printing method all happen here — no code change required.

### 3. `BookingSettings` — IBE / booking-engine defaults

- **Controller:** `BookingSettingsController`
- **Table:** `BookingSettings` (12 rows)
- **Verified columns include:** `LocalCountryId`, `BookingEngineUserId`, `BookingEnginePropertyId`, `IBEBookingStatusId`, `IBEEmailCommiunicationTypeId`, `IBETelephoneCommiunicationTypeId`, `WebAgentId`, `AccomadationChargeCodeId`, `AccomadationTaxGroupId`, `FCAccomadationTaxGroupId`.

**Business meaning:** when an online booking arrives, these settings decide which status it lands in, which charge code/tax group the room revenue posts to, which web-agent it is attributed to, and which communication types send the confirmation.

### 4. `HKSettings` — Housekeeping settings

- **Controller:** `HKSettingsController` · **Table:** `HKSettings` (12 rows) · SPs `HKSettings_Select` / `HKSettings_Update`.
- Stores walk-in vs in-house posting categories and housekeeping module behaviour.

### 5. Other settings tables present in the DB

`ChannelManagerSettings`, `EmailSettings`, `PaymentGateWaySettings`, `ReservationPostingSettings`, `MaintenanceSettings`, `KDSSettings`, `Notification_Parameters`/`Notification_ParameterValues`, `Notification_EmailSettings`, `Staah_DefaultSettings`, `OccupancyPropertyConfig`, `IBE_ADMIN_SiteSettings`, and the Guest-Portal settings family (`GuestPortal_EmailSettings`, `GuestPortal_PaymentGateWaySettings`, `GuestPortal_ProcessWiseEmailSMSSettings`, `GuestPortal_PropertySettings`, `GuestPortal_ReportSettings`). A snapshot backup `SystemSettings_23092024` also exists (treat as history — see Research Pack §6).

---

## Email / SMS / WhatsApp / integration configuration

| Channel | Where configured | Evidence |
|---|---|---|
| **Email (SMTP + templates)** | `EmailSettings` table (17 rows live) + `EmailTemplateController` (root, non-area) | Verified columns: `ConfirmationFromName/FromMail/ToMail/CC/BC`, `AlertFromName/FromMail/ToMail/CC/BC`, `EmailHost`, `EmailUserName`, `EmailPassword`, `ReportServerUserName`. Templates rendered by `EmailTemplateController` (`AdvanceRequestTemplate`, `AdvanceResponseTemplate`, `AdvanceRequestOfflineTemplate`). Email logging → `EmailLog` table. |
| **Document delivery (Email / WhatsApp)** | `DocumentDeliveryController` (root) | Actions `GetDocumentSendingMethods`, `GetDocumentTypes`, `SaveDocumentToDeliver` choose the channel; backed by `DocumentSendService` / `DocumentService` (Research Pack §9). |
| **SMS** | `FrontOffice.SMSSender` project (per Research Pack) + `CommunicationTypes` config | The SMSSender project is present; channel choice is a `CommunicationType`. Standalone SMS-provider config screen: **Not found in the Administration area** (configured at project/`Web.config` level). |
| **Channel managers (STAAH / Bookingwhizz)** | `ChannelManagerSettings`, `Staah_DefaultSettings` tables | Room type / rate / currency mappings per channel (verified `ChannelManagerSettings` columns: `ChannelId`, `AssignedRateId01/02`, `AssignedCurrencyId01/02`, `AssignedRoomTypeId01`, `MealPlanId`, `CompanyId`, `PackageId`, `PropertyId`). |
| **Payment gateway (Sampath / HNB IPG)** | `SampathIPGController` (Administration + root) + `PaymentGateWaySettings` / `GuestPortal_PaymentGateWaySettings` + `SystemSettings` group `GPPAy` | HNB IPG local/foreign card mapping is stored as `SystemSettings` rows (`GPPAy01/02`). |
| **Notifications** | `Notification_Parameters` / `Notification_ParameterValues` / `Notification_EmailSettings` | Parameterised notification configuration. |

> The dedicated SMS-provider gateway configuration screen and a WhatsApp-provider credential screen are **not present as Administration controllers** — those credentials live in project config / `Web.config` app-settings read via the `Configs` utility (looked in `Areas/Administration/Controllers/` and the settings tables). Document delivery *routing* is in-app; provider *credentials* are in config.

---

## Audit logging

- **Application-service audit (primary):** per Research Pack §5, the intended primary audit trail is `AuditTrialService` (`FrontOffice.Service`) surfaced by `AuditTrialController` in the **Auditing** area — `Landing(FromDate, ToDate, UserId, ProcessCode, Keyword)` lets an auditor filter the trail; `SelectAuditProcesses()` lists the tracked processes.
- **Live-DB note (verified):** in `HotelResWeb_Browns` there is **no `AuditTrial*` table** (queried `sys.tables LIKE '%AuditTr%'` → empty). The `AuditTrailEntry.cs` data class references the separate **`HotelResWeb_AuditTail`** DB — the secondary/legacy sink noted in the Research Pack. So on this property the trail is written to the AuditTail DB, not to a table in the main PMS DB.
- **Access audit (verified live):** every permission check writes a row to `UserWisePageAndReportAccessLog` via SP `Admin_T_Save_UserWisePagesAndReportsAccess` (see doc 09). Login/logout events log to `UserWiseAccessLog` (columns `UserId, IPAddress, MechineName, DateTime, IsLoggedIn`).
- **Domain change logs:** the DB carries many `*_Log` tables (`CityLedgerLog`, `BillToRoomLog`, `CancelledReservationLog`, `ChangeStay_Log`, `Folio_TransferLog`, `CompanyActivityLog`, `GuestActivityLog`, `EmailLog`, `GL_Posting_*_Log`, etc.) written by the relevant transaction SPs — these are the per-domain audit sinks.

---

## Screens / modules involved

| Screen (View) | Location |
|---|---|
| Any config landing/grid/form | `Areas/Administration/Views/<Name>/Landing.cshtml`, `_Grid.cshtml`, `_Form.cshtml`, `_Detail.cshtml` |
| Front Office settings | `Areas/Administration/Views/FrontOfficeSettings/` |
| Booking settings | `Areas/Administration/Views/BookingSettings/` |
| HK settings | `Areas/Administration/Views/HKSettings/` |
| Audit trail | `Areas/Auditing/Views/AuditTrial/` |

Every list screen uses the same MVC actions: `Landing` (page shell), `Grid` / `SelectForGrid` (data grid), `Form` (new), `Edit` (load), `Save` (persist), `Delete`, `Print`.

---

## Database / API involvement

- **Data access:** `DbConnectivity().ExecuteSP(...)`, `ExecuteSelectSP<T>(...)`, `SelectSingleSP<T>(...)` in each `*Entry` class (`Common.Data`). Connection resolved per property from `SessionObjects.LoggedUser.LoggedProperty` (multi-tenant DB switching) or the named connection string (`SqlServer2016ConnectionString`, `CentralAccessDbConnectionString`, etc.).
- **Settings read at login:** `FOSettings`, base currency, and system settings are cached in `SessionObjects` by `BaseController` on each request, avoiding repeated DB round-trips.

---

## Business rules

1. **Property-scoped:** almost all config is per `PropertyId`; the same code runs for every hotel in the chain with different data. Settings tables hold one row per property (12 live).
2. **Referential order:** dependent config cannot be created before its parent (rate needs room type; tax-group-detail needs tax type).
3. **Feature switches are data, not code:** behaviour like occupancy formula, module enablement, e-signature, printing method is toggled in `SystemSettings` — no deployment needed.
4. **Every write is permission-gated:** `[UserWisePageAccess(pageId, "I/U/D/S")]` guards each action (doc 09).
5. **Backup/history twins exist:** tables/SPs suffixed `_OLD`, `_bk`, `_History`, dated snapshots (`SystemSettings_23092024`) are non-canonical — use the un-suffixed name.

---

## Expected result

After configuration, the operational modules "just work": Reservations show correct room types, rates, and meal plans; Cashiering posts charges with the right charge codes, posting categories, and tax groups; Housekeeping uses the configured statuses and reasons; Reports filter by the configured markets, segments, and departments; and the whole system's behaviour matches the `SystemSettings` switches.

## Error scenarios

| Scenario | Cause | Handling |
|---|---|---|
| "You don't have permission to save records in this …" | Action-level permission missing | `UserWisePageAccess` returns 403 (AJAX) or throws `UnauthorizedAccessException` (doc 09). |
| Cannot delete a master record | Record referenced by transactions/child config | `<Table>_M_Delete` SP raises an FK/guard error surfaced to the grid. |
| Setting change has no effect | Edited wrong property row, or session cache stale | `SystemSettings`/`FOSettings` are per-`PropertyId` and cached in session — re-login or property switch reloads them. |
| Missing parent config | Creating dependent data before parent | Combo boxes are empty; save fails validation. |

## Related documents

- `00-project-overview.md` — system identity & architecture
- `09-user-roles-and-permissions.md` — how every Administration action is authorised
- `03-reservation-process.md` — consumes room/rate/meal/market config
- `05-cashiering-and-finance-process.md` — consumes charge/posting/tax/payment config
- `06-rooms-and-housekeeping-process.md` — consumes room/HK config
- `12-database-and-technical-architecture.md` — DB & SP conventions
