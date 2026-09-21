# Hotel PMS Documentation — Shared Research Pack

> **Purpose:** Authoritative shared facts + rules for every documentation agent. Read this fully before writing.
> This keeps all 21 documents consistent, accurate, and grounded in the actual source code / database.

---

## 0. GOLDEN RULES (apply to every file)

1. **Never invent.** Document only what exists in the source code or database. If something cannot be confirmed, write **"Not found in the project"** (and note where you looked).
2. **Cite the source** for every technical statement, whenever possible:
   - File path · Class name · Method name · Controller/Action · Table name · Stored procedure name · Screen/View name.
3. **Verify against reality**: read the actual `.cs`/`.cshtml`/`.sql` files and query the live DB before asserting behaviour.
4. **Business + technical**: explain the hotel business process in plain language for hotel staff, then back it with the technical detail.
5. Prefer **tables, numbered steps, bullet points, and flow diagrams** over long paragraphs.
6. Cross-link related documents by filename.

## 1. Standard file structure (use for every numbered doc)

```
# <Title>
## Purpose
## Relevant users / departments
## Preconditions
## Step-by-step process
## Screens / modules involved
## Database / API involvement
## Business rules
## Expected result
## Error scenarios
## Related documents
```

For each workflow, where applicable use the 6-step format:
1. User action → 2. System validation → 3. Database change → 4. Related module update → 5. Notification / integration → 6. Final result.

---

## 2. System identity

- **Product:** Scienter HotelERP — "Destinity Inspire / Destinity Horizon" Front Office ERP (Hotel PMS).
- **Vendor namespace:** `Scienter.HotelERP.*`
- **Stack:** ASP.NET **MVC 5** (.NET Framework), C#, SQL Server 2019, jQuery/Bootstrap front end, SignalR (real-time), SSRS (reports), EPPlus (Excel), Select.HtmlToPdf (PDF).
- **Architecture:** N-tier **modular monolith**, multi-tenant SaaS (per-property database switching), central SSO.
- **Deployment context:** Sri Lankan hotel chains (Jetwing, Araliya, Hotel J, Browns, etc.). Currency LKR; Sri Lanka tax model (VAT / Service Charge / TDL etc.).

## 3. Solution projects (from `Scienter.HotelERP.sln`)

> ⚠️ **VERIFIED CORRECTION:** Only **9 projects are physically present** in this checkout (have a `.csproj`):
> `Common.AzureUtility`, `Common.Data`, `Common.DbUtility`, `Common.Domain`, `Common.Utility`,
> `FrontOffice.Service`, `FrontOffice.SMSSender`, `FrontOffice.WebUIMvc`, `ReportDownloader`
> (plus `FrontOffice.Resources` resources folder).
> These `.sln`-referenced projects are **NOT in this working copy** — treat their standalone source as **"Not found in the project"**, but note their *capabilities still exist* via WebUIMvc controllers/services and DB SPs:
> `FrontOffice.IPG`, `FrontOffice.DeviceHub`, `BEMailSender`, `FrontOffice.DayEndSummaryExecution`, `BookingEngine`, `BookingEngine.BellWoodManor`, `SampleBookingEngine`, `HouseKeeping.API`.
> (e.g. Sampath IPG works via `SampathIPGController` in WebUIMvc; day-end via `DayEndProcessController` + `DayEnd*` SPs; email via `EmailTemplateController`/`DocumentDeliveryController`.)

| Project | Layer / role |
|---|---|
| `Scienter.HotelERP.FrontOffice.WebUIMvc` | Presentation (MVC 5, Areas, Controllers, Views, JS) |
| `Scienter.HotelERP.FrontOffice.Service` | Business logic (Service classes) — 189 services |
| `Scienter.HotelERP.Common.Data` | Data access (`*Entry` repository classes) — 187 files |
| `Scienter.HotelERP.Common.Domain` | Domain models / entities |
| `Scienter.HotelERP.Common.DbUtility` | DB connectivity helpers |
| `Scienter.HotelERP.Common.Utility` | Cross-cutting utilities |
| `Scienter.HotelERP.Common.AzureUtility` | Azure Blob storage (documents/images) |
| `Scienter.HotelERP.FrontOffice.IPG` | Sampath Internet Payment Gateway integration |
| `Scienter.HotelERP.FrontOffice.DeviceHub` | Device hub (fiscal printer / hardware) |
| `Scienter.HotelERP.FrontOffice.SMSSender` | SMS integration |
| `Scienter.HotelERP.BEMailSender` | Email sending |
| `Scienter.HotelERP.FrontOffice.DayEndSummaryExecution` | Night audit / day-end batch execution |
| `Scienter.HotelERP.BookingEngine` / `.BellWoodManor` / `SampleBookingEngine` | Internet Booking Engine (IBE) |
| `Scienter.HotelERP.HouseKeeping.API` | Housekeeping API (mobile/device) |
| `ReportDownloader` | SSRS report execution/download utility |

## 4. MVC Areas (modules) — `WebUIMvc/Areas/`

`Administration` · `Auditing` · `CashieringAndPosting` · `DataAnalysis` · `GuestPortal` · `HouseKeeping` · `Maintenance` · `MealReservation` · `Reporting` · `Reservation` · `SpaReservation` · `UserAccess`

Root (non-area) controllers: `AutoLogin`, `Base`, `CommonMethod`, `DocumentDelivery`, `EmailTemplate`, `Error`, `Login`, `Saas`, `SaasLogin`, `SampathIPG`.

## 5. Databases (multi-DB)

| Database | Role |
|---|---|
| `HotelResWeb_<Property>` (e.g. `HotelResWeb_Browns`) | **Main per-property PMS DB** — 895 tables, 2,889 procs, 66 functions, 5 views |
| `HotelResWeb_PassportScan` | Passport / NIC scan image storage |
| `CentralAccessDB` / `CentralAccessApi` | Central SSO, users, cross-property access |
| `Categlog_vrV2` | Inventory / POS catalog DB |
| `DestinityHorizon_Saas` | SaaS tenant/property registry |
| `destinity` / `central` | Central configuration |

**Verified `Web.config` connection-string names (map to the DBs above):**
| Connection string name | Points to |
|---|---|
| `SqlServer2016ConnectionString` | Main per-property PMS DB (`HotelResWeb_<Property>`) |
| `SqlServer2016POS` | POS DB (`Categlog_vrV2`) |
| `SqlServer2016Inventory` | Inventory DB |
| `PassportDbConnection` | `HotelResWeb_PassportScan` |
| `CentralAccessDbConnectionString` | `CentralAccessDB` (SSO / central users) |

**Audit note (verified):** primary audit trail is `AuditTrialService` (`FrontOffice.Service`) + `AuditTrialController` (Auditing area) writing to `AuditTrial*` tables; a separate `HotelResWeb_AuditTail` DB is referenced once (lightly used). Document audit as application-service driven via `AuditTrialService`; mention the AuditTail DB as a secondary/legacy sink.

**Live main DB for verification:** SQL Server `10.4.1.180`, database `HotelResWeb_Browns` (SQL auth — connection details provided by the orchestrator in each agent prompt; do NOT hard-code credentials into any doc).

Query with:
```
sqlcmd -S 10.4.1.180 -U <user> -P '<pwd>' -d HotelResWeb_Browns -h -1 -W -Q "…"
```

## 6. Naming conventions

- **Stored procedures:** `<Domain>_<M|T>_<Action>` — `M` = Master (config), `T` = Transaction. Common actions: `Select`, `Save`, `Delete`, `Select_ById`, `Select_ForGrid`, `Update`, `Chart`, `Parameterized`. Beware duplicate variants suffixed `_OLD`, `_Dev`, `_OPT`, `_NEW`.
- **Data layer:** each `Common.Data/<Name>Entry.cs` wraps a set of SPs (Save/Select/Delete).
- **Services:** `Common.Service? No →` `FrontOffice.Service/<Name>Service.cs` orchestrates one or more `*Entry` classes.
- **Controllers:** `WebUIMvc/Areas/<Area>/Controllers/<Name>Controller.cs`; views in `Areas/<Area>/Views/<Name>/*.cshtml`.
- **Tables:** many have dated/backup twins (`_20211204`, `_bk`, `_History`, `_BeforeRemoval`) — treat the un-suffixed name as canonical; note history/backup tables separately.

## 7. Pre-extracted structured maps (graphify) — USE THESE

Located in `graphify-out/`:

| File | Contents |
|---|---|
| `ctrl_actions.json` | `Area → Controller → [ "HTTP:Action", … ]` — every controller action |
| `ctrl_deps.json` | `Area → Controller → [dependencies]` |
| `svc_deps.json` | `Service → { data_deps:[Entry], domain_types:[Model] }` |
| `data_sps.json` | `Entry → { Save:[SP], Select:[SP], Delete:[SP] }` — maps data classes to stored procedures |
| `all_sps.json` | `{ unique_sp_names: [ … ] }` — full SP catalog referenced by code |
| `graph.json` / `GRAPH_REPORT.md` | Knowledge graph + architecture narrative |

Object-name lists exported to `docs/hotel-pms/_research/`:
- `db_tables.txt` (895) · `db_procs.txt` (2,889) · `db_functions.txt` (66)

## 8. Core domain entities (canonical tables — verify columns before citing)

| Concept | Key table(s) |
|---|---|
| Reservation header/detail | `ReservationHeader`, reservation room/detail tables (prefix `Reservation*`, 57 tables) |
| Guest profile | `GuestProfile*` (prefix `Guest*`, 90 tables) |
| Room master / status | `RoomDetails`, `RoomTypes`, `RoomCategories`, room status tables (prefix `Room*`, 38 tables) |
| Folio / billing | `FolioHeader`, `FolioDetails`, `FolioWisePostingBreakUp`, `FoliowiseTaxDetails` (prefix `Folio*`, 35+ tables) |
| Bill / settlement | `BillHeader`, `BillTrans`, `BillSettlementDetails`, `BillToRoomLog` |
| Advance / deposit | `AdvanceRequestHeaders`, `AdvanceRequestDetails`, `AdvancePaymentLinks`, `AdvanceRequestOnline*` |
| Posting / charges | `Posting*`, `FolioWisePostingBreakUp`, `Core_ProfitCenterTransaction*` (POS) |
| Tax | `Tax*` (13 tables), `FoliowiseTaxDetails` |
| Day-end / night audit | `DayEnd*` / `Dayend*` (17+ tables), `DayEndSummary`, `DayEndSummaryGuestLedger` |
| Spa | `Core_Spa*` |
| Profit centers (POS/outlets) | `Core_ProfitCenter*` |
| Users / access | `User*` (11 tables) + `CentralAccessDB` |

## 9. Confirmed external integrations

| Integration | Evidence |
|---|---|
| Channel Managers | SP prefixes `Staah*` (23), `Bookingwhizz*` (11), `CM*` (12), `CMReservation*` tables (9), OTA controllers (`OTABookingController`) |
| Payment gateway | `Scienter.HotelERP.FrontOffice.IPG`, `SampathIPGController`, `Administration/SampathIPGController` |
| Fiscal printer / device | `FiscalPrinterService`, `FrontOffice.DeviceHub` (localhost:1304 per graph) |
| SMS | `FrontOffice.SMSSender` |
| Email | `BEMailSender`, `EmailTemplateController` |
| WhatsApp / document delivery | `DocumentSendService`, `DocumentDeliveryController`, `DocumentService` |
| Reports | SSRS (`ReportDownloader`, SSRS execution web reference) |
| Message queue | SP prefix `RabbitMQ*` (15) |
| Passport scan | `HotelResWeb_PassportScan` DB |
| Cloud storage | `Common.AzureUtility` (Azure Blob) |
| Real-time | SignalR |
| Central SSO | `login.inspire.destinity.lk`, `CentralAccessDB`, `AutoLoginController`, `SaasLoginController` |

## 10. Output location

All docs → `docs/hotel-pms/`. Research scratch → `docs/hotel-pms/_research/` (do not link from README).
