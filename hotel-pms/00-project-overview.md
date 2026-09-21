# 00 — Project Overview: Scienter HotelERP / Destinity Inspire Front Office

## Purpose

This document gives hotel staff, operators, and technical readers a single, accurate picture of **what the Front Office system is, what business problems it solves, which modules it contains, how users and permissions work, and how the parts fit together.**

Everything below is grounded in the actual source code (`F:\GitHub\destinity-inspire-front-office-v2`) and the live database (`HotelResWeb_Browns` on SQL Server `10.4.1.180`). Where a fact could not be confirmed in this checkout, it is marked **"Not found in the project."**

## Relevant users / departments

| User / Department | What they use it for |
|---|---|
| Front Desk / Reception | Reservations, check-in, check-out, room allocation, guest profiles |
| Cashier / Night Auditor | Folio postings, bill settlement, advances, currency encashment, **Day-End (night audit)** |
| Housekeeping | Room status, room-boy allocation, cleaning, lost & found, inspections |
| Reservations / Sales | Bookings, allotments, rate codes, companies, OTA/channel bookings |
| Maintenance / Engineering | Jobs, preventive maintenance, assets, complaints |
| Spa & Meal outlets | Spa reservations, meal reservations, event/table reservations |
| Management | Dashboards, data analysis, reporting (SSRS) |
| System administrators | Master configuration (Administration area), user access & roles (UserAccess area), auditing |
| Guests | Self-service **Guest Portal** (requests, laundry, feedback, stay changes) |

## Preconditions

- A logged-in user with an assigned **UserRole** and property access (`UserWiseProperties`).
- The property's per-tenant database (`HotelResWeb_<Property>`) must be reachable.
- Central login/SSO enabled (`IsCentralLoginEnabled = 1`, portal `login.inspire.destinity.lk`) — verified in `Scienter.HotelERP.FrontOffice.WebUIMvc/Web.config`.

---

## 1. Project overview & main business purpose

**Scienter HotelERP – Destinity Inspire / Destinity Horizon Front Office** is a **web-based Hotel Property Management System (PMS)** used by Sri Lankan hotel chains (e.g. Browns, Jetwing, Araliya, Hotel J). It runs the full front-office guest lifecycle:

```
Enquiry → Reservation → Check-in → In-house stay (postings/charges)
        → Folio & Billing → Settlement → Check-out → Night Audit (Day-End)
```

The business problems it solves:

- **Single source of truth for the guest stay** — one reservation record drives room allocation, folio charges, taxes, bills and settlement.
- **Accurate revenue & tax capture** — every charge (room, F&B/POS, laundry, spa, extras) is posted to a folio with Sri-Lanka tax rules (VAT / Service Charge / TDL) and rolled up for accounting.
- **Night audit / Day-End close** — rolls the hotel business date forward, posts room revenue, validates folios, generates statistics.
- **Multi-property operation from one application** — one code base serves many hotels, each with its own database (multi-tenant SaaS).
- **Distribution** — connects to OTAs / channel managers (Staah, BookingWhizz, Profitroom) and an internet booking engine.
- **Guest experience** — self-service Guest Portal, complaints, feedback, document delivery (email/WhatsApp).

## 2. Technologies used (verified)

Verified from `Scienter.HotelERP.FrontOffice.WebUIMvc/*.csproj`, `packages.config`, `Web.config`, and `Scienter.HotelERP.Common.DbUtility/DbConnectivity.cs`.

| Concern | Technology | Evidence |
|---|---|---|
| Framework | **ASP.NET MVC 5.2.7** on **.NET Framework 4.8** | `TargetFrameworkVersion v4.8`; `Microsoft.AspNet.Mvc 5.2.7` |
| Language | **C#** | all `.cs` source |
| Database | **SQL Server 2019** (2016-compatible connection strings) | connection strings `SqlServer2016*`; live DB verified |
| Data access | **Dapper 1.50.5** micro-ORM calling **stored procedures** | `DbConnectivity.cs` (`using Dapper`, `Query<T>`, `Execute`, `CommandType.StoredProcedure`) |
| Real-time | **SignalR** (server 2.2.2; client scripts 2.2.2 & 2.4.3) | `Microsoft.AspNet.SignalR 2.2.2`; `Models/Hubs/NotificationHub.cs`; `Scripts/jquery.signalR-*.js` |
| Auth / SSO | **OWIN / OAuth 4.2.2**, central login portal | `Microsoft.Owin 4.2.2`; `Web.config` `IsCentralLoginEnabled`, `LoginPortalUrl` |
| Reports | **SQL Server Reporting Services (SSRS)** via **Microsoft ReportViewer** (`ReportingServices.ReportViewerControl.WebForms 150.900.148`, `ReportViewerForMvc14 140.1000.523`) | packages.config; `Microsoft.ReportViewer.*` DLL references; `ReportServer`, `SSRSReportsFolder` app settings; `ReportDownloader` project |
| Excel export | **EPPlus 6.2.8** | `EPPlus 6.2.8`; `OfficeOpenXml` usage |
| Front-end | **jQuery 3.3.1, Bootstrap 3.0.0, DataTables, DayPilot (availability calendar), Intro.js (guided tours)** | `packages.config`; `Scripts/daypilot-all.js`, `datatable/jquery.dataTables.min.js`, `Scripts/intro.js-7.2.0` |
| Cloud storage | **Azure Blob** (documents/images) + Managed Identity | `Scienter.HotelERP.Common.AzureUtility`; `Azure.Identity 1.12.0`, `Azure.Core 1.40.0` in `DbConnectivity.cs` |
| Fiscal printer | Device hub HTTP endpoint | `FiscalPrinterURL = http://localhost:1304/` (Web.config); `FiscalPrinterService` |
| SMS | SMS sender project | `Scienter.HotelERP.FrontOffice.SMSSender` |

> **Note on this checkout:** The v2 solution (`Scienter.HotelERP.sln`) contains **9 projects** (Web UI, Service, Common.Data, Common.Domain, Common.DbUtility, Common.Utility, Common.AzureUtility, SMSSender, ReportDownloader). Separate `BookingEngine`, `HouseKeeping.API`, `IPG`, `DeviceHub`, and `BEMailSender` projects referenced in general product documentation are **not present as projects in this checkout** — related capabilities appear here as MVC controllers (e.g. `SampathIPGController`), services (`FiscalPrinterService`), and stored procedures (`WebApi_*`, `Staah_*`). A dedicated HTML-to-PDF library was **not found in the project**; printable output is produced via **SSRS ReportViewer** and **EPPlus** (Excel).

## 3. Main modules (the 12 MVC Areas + root controllers + APIs)

Modules are ASP.NET MVC **Areas** under `Scienter.HotelERP.FrontOffice.WebUIMvc/Areas/`. Controller counts below are from the actual folders.

| Area (module) | Controllers | Business purpose (one line) |
|---|---|---|
| **Administration** | 106 | Master/setup data — rooms, rate codes, companies, currencies, taxes, payment modes, packages, channel-manager & payment-gateway settings, **POSApiController** |
| **Reservation** | 27 | Create/manage bookings, room allocation, check-in/out, availability chart, OTA bookings, transport, quick check-in/out |
| **CashieringAndPosting** | 20 | Folio management, postings, discounts, credit/debit notes, advances, currency encashment, tax calc, **Day-End process** |
| **GuestPortal** | 14 | Guest self-service — requests, laundry, feedback, complaints, stay changes, promotions |
| **Maintenance** | 13 | Engineering jobs, preventive maintenance, assets, complaints, service hub |
| **HouseKeeping** | 12 | Room status, room-boy allocation, cleaning/inspection, lost & found |
| **Reporting** | 10 | Operational & financial reports (SSRS) |
| **UserAccess** | 7 | Users, roles, page/report access, per-property access |
| **MealReservation** | 2 | Meal/restaurant reservations |
| **SpaReservation** | 2 | Spa bookings, therapists, time slots, spa billing |
| **Auditing** | 1 | Audit trail viewer (`AuditTrialController`) |
| **DataAnalysis** | 1 | Analytical dashboards (occupancy, room nights, forecasts) |

**Root (non-area) controllers** (`WebUIMvc/Controllers/`): `Login`, `AutoLogin`, `SaasLogin`, `Saas` (SSO / multi-tenant entry), `Base` (`BaseController`), `CommonMethod`, `DocumentDelivery`, `EmailTemplate`, `SampathIPG` (payment gateway), `Error`.

**APIs / integrations exposed from within the MVC app:**
- **POSApiController** (Administration area) — JSON endpoints for the POS/outlet system (backed by `POSApiService` → `POSApiEntry`).
- **SignalR NotificationHub** (`Models/Hubs/NotificationHub.cs`) — real-time front-office notifications.
- **`WebApi_*` stored procedures** (e.g. `WebApi_RoomAvailability`, `WebApi_Reservcation_Select_ToSync_HotelRes`) — data-sync endpoints for external/mobile clients.
- Channel-manager integration via `Staah_*`, `BookingWhizz_*`, `Profitroom_*`, `CMReservation*` tables & SPs, plus `OTABookingController`.

## 4. User roles & permissions

Access control is data-driven and modelled in the **UserAccess** area (`Areas/UserAccess/Controllers/`) plus `User*` tables and the shared **CentralAccessDB** (SSO).

**Controllers (verified):** `UsersController`, `UserRolesController`, `UserRoleWisePagesController`, `UserWiseRolesController`, `UserWiseIndividualAccessesController`, `UserWiseReportAccessController`, `UserWisePropertiesController`.

**How it is modelled:**

| Table / concept | Meaning |
|---|---|
| `Users` | Individual login accounts |
| `UserRoles` | Named roles (e.g. Front Desk, Cashier, Manager) |
| `UserWiseRoles` | Which role(s) a user has |
| `UserRoleWisePages` | Which pages/screens a **role** may open |
| `UserWiseIndividualAccess` | Per-user overrides (grant/deny an individual screen/action) |
| `UserWiseReportAccess` | Which reports a user may run |
| `UserWiseProperties` | Which hotels/properties a user may operate |
| `UserWiseQuickNavigationAreas` / `...Pages` | Personalised quick-launch menu |
| `UserWiseAccessLog`, `UserWisePageAndReportAccessLog` | Access audit logs |

Central SSO users live in **CentralAccessDB / CentralAccessApi**; the app calls it for single sign-on (`Central_UsersEntry` → `Central_UserWiseModuleLogin_*`). Effective permissions = **role-wise pages + report access + individual overrides**, all scoped to the user's allowed properties.

## 5. Relationship between modules

The **Reservation** module is the hub. Almost every other module reads or updates a reservation, its rooms, its guests, or its folio.

```
                         +------------------+
                         |  Administration  |  (masters: rooms, rates,
                         |  (setup/config)  |   companies, taxes, POS)
                         +--------+---------+
                                  | provides master data to all
                                  v
   +-----------+   allocates   +------------------+   charges   +-----------------------+
   | HouseKeep |<------------- |   RESERVATION    | ----------> | CashieringAndPosting  |
   | (room     |  room status  | (bookings,       |   folios    | (folio, bill, advance,|
   |  status)  | ------------->|  check-in/out)   |<----------- |  Day-End night audit) |
   +-----------+               +---+----------+---+  settlement +-----------+-----------+
                                   |          |                             |
                 guest profile     |          | meal/spa/event               | posts revenue
                 (Guest*)          v          v                             v
                              +---------+  +-------------+           +---------------+
                              |Guest    |  |Meal/Spa/    |           | Reporting /   |
                              |Portal   |  |Event resvns |           | DataAnalysis  |
                              +---------+  +-------------+           +---------------+
                 Maintenance (jobs/complaints) attaches to rooms & reservations
                 Auditing records changes across all modules
```

Dependency evidence: `graphify-out/svc_deps.json` shows most services depend on `ReservationHeaderEntry` and/or `FolioEntry`; e.g. `FolioService` → `FolioEntry` + `ReservationHeaderEntry`; `PostingService`, `MealReservationService`, `AdvancePaymentService`, `GuestPortalService` all reference reservation/folio/posting types.

## 6. Overall system architecture

**N-tier modular monolith, multi-tenant (one DB per property), central SSO.**

```
        BROWSER (jQuery, Bootstrap, DataTables, DayPilot, SignalR client)
                                 |  HTTPS
                                 v
  +----------------------------------------------------------------------+
  |  PRESENTATION  — Scienter.HotelERP.FrontOffice.WebUIMvc (MVC 5)       |
  |  12 Areas + root controllers + SignalR NotificationHub + POSApi       |
  |  BaseController enforces login/session (SessionObjects.LoggedUser)    |
  +---------------------------------+------------------------------------+
                                    | calls
                                    v
  +----------------------------------------------------------------------+
  |  BUSINESS LOGIC — Scienter.HotelERP.FrontOffice.Service (189 files)   |
  |  <Name>Service orchestrates one or more *Entry classes               |
  +---------------------------------+------------------------------------+
                                    | calls
                                    v
  +----------------------------------------------------------------------+
  |  DATA ACCESS — Scienter.HotelERP.Common.Data (187 *Entry classes)     |
  |  each *Entry wraps a set of stored procedures (Save/Select/Delete)    |
  +---------------------------------+------------------------------------+
                                    | via
                                    v
  +----------------------------------------------------------------------+
  |  DB UTILITY — Common.DbUtility (DbConnectivity.cs, Dapper)            |
  |  picks per-property connection string; Begin/Commit/Rollback         |
  +---------------------------------+------------------------------------+
                                    | T-SQL (stored procedures)
                                    v
  +----------------------------------------------------------------------+
  |  SQL SERVER 2019                                                      |
  |  HotelResWeb_<Property>  (895 tables · 2,889 procs · 66 fns · 5 views)|
  +----------------------------------------------------------------------+

  Cross-cutting / external:
   • CentralAccessDB / CentralAccessApi ...... SSO, users, cross-property access
   • DestinityHorizon_Saas ................... tenant/property registry (SaaS)
   • Categlog_vrV2 (SqlServer2016POS) ........ POS/inventory catalog DB
   • HotelResWeb_PassportScan ................ passport / NIC scan images
   • Azure Blob (Common.AzureUtility) ........ documents & images
   • SSRS ReportServer ....................... report rendering
   • Fiscal printer (localhost:1304) ......... fiscal receipts
   • Channel managers (Staah/BookingWhizz/Profitroom), Sampath IPG (payments)
```

- **Shared domain/utility layers:** `Common.Domain` (models/DTOs), `Common.Utility` (`SessionObjects`, `Configs`, `SaasConfig`), `Common.AzureUtility`.
- **Multi-tenant switching** is verified in `DbConnectivity.cs`: connection strings are formatted with `SaasConfig.SaasServer / SaasDb / Username / Password` (chosen per property at login), and the DB access class also injects the logged-in user into SQL Server `sp_set_session_context` for DB-side audit.

## Expected result

A correctly deployed system lets each department run its part of the guest lifecycle against its own property database, while sharing one login and one consistent set of reservation/folio/bill records — with all financial postings and taxes captured for accounting and reporting.

## Error scenarios

| Scenario | Cause | Where it surfaces |
|---|---|---|
| Login fails / redirects to portal | Central SSO unreachable or session expired | `LoginController` / `AutoLoginController`; `BaseController` session check |
| "Property not accessible" | User lacks `UserWiseProperties` entry | UserAccess area |
| Page/report blocked | Missing `UserRoleWisePages` / `UserWiseReportAccess` | UserAccess checks |
| Posting/settlement fails midway | DB error inside a multi-step SP or transaction | `DbConnectivity` transaction is rolled back; see `12-database-and-technical-architecture.md` |
| Day-End cannot complete | Open folios / unposted room rates / POS not validated | `DayEndProcessController` validation SPs (`DayEnd_*_Check`) |
| Report does not render | SSRS server unreachable (`ReportServer` setting) | Reporting area / ReportViewer |

## Related documents

- `12-database-and-technical-architecture.md` — databases, tables, stored procedures, request lifecycle, transactions, audit.
- `_research/RESEARCH-PACK.md` — shared research facts (internal).
- `graphify-out/GRAPH_REPORT.md`, `svc_deps.json`, `data_sps.json`, `ctrl_actions.json` — extracted structural maps (internal).
</content>
</invoke>
