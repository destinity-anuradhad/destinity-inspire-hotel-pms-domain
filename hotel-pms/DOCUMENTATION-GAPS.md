# Documentation Gaps

> **Purpose:** A single authoritative list of everything that **could not be confirmed** from the source code or the live database during this documentation effort — so readers know exactly where the documentation is grounded vs. inferred, and maintainers know what to verify next.
> Across the 16 numbered documents there are **73 explicit "Not found in the project" markers**; this file groups and explains them, plus the structural limits of the analysis.

---

## 1. How this documentation was grounded

| Source | Access | Confidence |
|---|---|---|
| Source code (9 present projects) | Full read access | **High** |
| Main DB `HotelResWeb_Browns` (895 tables, 2,889 SPs) | Live query access | **High** |
| Pre-built graphify extraction maps | Read | High (cross-checked against code/DB) |
| Companion databases | **No direct connection** | Documented from code references only |
| `.sln` projects absent from checkout | **Source not present** | Capability inferred from callers/DB only |

Every technical claim in the numbered docs cites a file / controller / SP / table. Where a claim could not be verified, the docs say **"Not found in the project"** and this file consolidates those.

---

## 2. Source code that could not be inspected (projects absent from this checkout)

These are referenced by `Scienter.HotelERP.sln` but their folders/`.csproj` are **not in this working copy**. Their *capabilities* are documented from their callers (WebUIMvc controllers/services) and DB SPs, but their **internal implementation is a gap**.

| Absent project | What it does | Documented from | Gap |
|---|---|---|---|
| `FrontOffice.IPG` | Sampath payment-gateway integration | `SampathIPGController`, `Web.config` IPG keys | Gateway request/response internals |
| `FrontOffice.DeviceHub` | Fiscal/receipt printer bridge (`localhost:1304`) | `FiscalPrinterService`, config | Device protocol, print formatting |
| `BEMailSender` | Email dispatch | `EmailTemplateController`, `EmailSettings` | SMTP send internals |
| `FrontOffice.DayEndSummaryExecution` | Night-audit batch runner | `DayEndProcessController`, `DayEnd*` SPs | Standalone batch scheduling internals |
| `BookingEngine` / `.BellWoodManor` / `SampleBookingEngine` | Internet Booking Engine (IBE) | reservation inbound paths, `BookingSource` | IBE UI and booking-capture internals |
| `HouseKeeping.API` | Mobile housekeeping API | `HKSettings.HouseKeepingApiUrl` | API endpoints/auth internals |

---

## 3. Companion databases not directly connected

Only `HotelResWeb_Browns` was queried live. The following are documented from **code references and connection strings only**:

| Database | Connection string | Not confirmed |
|---|---|---|
| `Categlog_vrV2` (POS) | `SqlServer2016POS` / `SqlServer2016Inventory` | POS menu/recipe/stock/KOT internals; only the **posting into folios** is visible from the PMS side |
| `CentralAccessDB` | `CentralAccessDbConnectionString` | Central SSO user store, `validateaccess` internals |
| `HotelResWeb_PassportScan` | `PassportDbConnection` | Passport/NIC image storage schema |
| `HotelResWeb_AuditTail` | (referenced in code) | Actual audit-table schema/volume (the `AuditTrial*` tables are **not** in the main Browns DB) |
| `DestinityHorizon_Saas` | (SaaS template) | Tenant/property registry internals |

---

## 4. Features wired in code but not deployed on this property

Verified **absent** from `HotelResWeb_Browns` via `sys.objects` — the C# calls them, but the SP does not exist here (may exist on other properties):

| Missing object | Feature affected | Where called | Doc |
|---|---|---|---|
| `Reservation_T_SaveSignature` | Guest signature save/sync | `ReservationHeaderEntry.cs` | 02, 04, 13 (UC16), 15 |
| `Merge_MultipleFolio`, `Save_Merged_MultipleFolio` | Merge multiple folios | `FolioEntry.cs` | 05, 15 |
| `Reservations_W_ValidatePOSBill_AtCheckout` | Block checkout on unsettled POS bill | `QuickCheckOutController` | 04, 07, 13 (UC5), 15 |

---

## 5. Integrations that are external or inactive (behaviour not fully confirmable)

| Integration | Status found | Gap |
|---|---|---|
| Channel managers (Staah/Bookingwhizz/CM/RateTiger) | Inbound/outbound SPs present (Staah 24, CM 12, Bookingwhizz 11) | External endpoint URLs, credentials, retry/SLA — **external to the codebase** |
| WhatsApp document sending (UC17) | Documents **queued** via `HK_Save_DocumentToDeliver` | No dispatcher/endpoint that actually transmits WhatsApp — **Not found** |
| Payment refund to gateway (UC7) | Refund is a manual folio/advance operation | No automated IPG refund call — **Not found** |
| Real-time GL / external accounting post | GL posting during FO day-end is **commented out**; no external accounting connector | **Not found / inactive** |
| Door-lock system | Only `DoorLockEvent*` key-code **logging** exists | No external lock-controller command path — **Not found** |
| SignalR real-time push | `NotificationHub` server class **fully commented out** | Real-time push is not operational; `ServiceHub*` DB-polling is the actual mechanism |
| Sampath IPG (this checkout) | Handlers largely commented; redirects instead of calling paycorp | Live path non-functional **in this checkout** |

---

## 6. Business behaviour that is manual, not automated (so not codified)

| Expected rule | Reality in code | Doc |
|---|---|---|
| Cancellation charge/penalty | `CancellationPolicies` is **textual terms only**; cancel SP stores reason + remark, no monetary calc | 03, 13 (UC9), 14 |
| No-show fee | No fee computation; status set via day-end `Reservations_T_UpdateNoShow` | 03, 13 (UC10) |
| Early-checkout / late-checkout fee | Manual folio postings, not auto-computed | 13 (UC11/UC12) |
| One-click walk-in | No single walk-in endpoint; walk-in = create reservation + immediate check-in | 02, 13 (UC1) |
| Mark-as-no-show endpoint | No dedicated action; handled by `BookingSettings.NoShowStatusId` + day-end | 03, 13 (UC10) |

---

## 7. Property-specific limitation (Browns = spa/retail)

- The live property `HotelResWeb_Browns` has **profit centres SPA / SALON / GIFT SHOP — no restaurant/F&B outlets**. The F&B/outlet document (07) therefore describes the **posting mechanism** (POS → folio) from code + config, not from live restaurant transaction data on this property. Behaviour on an F&B-heavy property was not observed.
- The `Core_ProfitCenter*` tables (11) hold **0 rows** and are unused by code — the canonical POS path is `ProfitCenter_txn*` / `ExtraPostingDetails`.

---

## 8. Reporting / dashboard specifics not confirmable

- Some Reporting controllers (`FolioController`, `CountryController`, `GuestProfilebyCountryController`, `PropertyDetailReportHeaderController`) are **dead/commented code**.
- Front-end wiring for the 193 `DashboardAPI_*` SPs was **not fully traced**.
- Report **categories are numeric codes** in `ReportDetails` — there is **no named report-category master table**.
- The SSRS report **definitions (.rdl)** live on the report server (`ReportServer`), not in this repo — report layouts are a gap.

---

## 9. Structural limits of the analysis

1. **One property only.** All live verification used `HotelResWeb_Browns`. Because SPs/schema **drift per property** (see issue #10 in doc 15), objects marked "absent" mean absent **here** — they may exist elsewhere.
2. **Static analysis only.** No query-plan/load profiling was run; performance observations (doc 15 #23–#26) are schema/index-shape inferences, not measured regressions.
3. **Secrets by location only.** Credential exposure (doc 15 #19–#22) is cited by file/line; no values were reproduced or tested.
4. **Graphify corpus.** The pre-built knowledge graph included marketing/image assets (hotel logos, OTA lists) that are **not** part of the PMS logic and were excluded from functional docs.

---

## 10. Recommended verifications for a maintainer

| To confirm… | Do this |
|---|---|
| Per-property SP/schema drift | Run a schema-diff of `sys.procedures`/`sys.tables` across all `HotelResWeb_*` DBs |
| Missing-SP runtime risk | CI check that every SP named in `Common.Data/*Entry.cs` resolves in each target DB |
| POS internals | Connect to `Categlog_vrV2` and document menu/stock/KOT + the `DayEndGL_Posting` bridge |
| SSO/audit internals | Connect to `CentralAccessDB` and `HotelResWeb_AuditTail` |
| Absent project behaviour | Obtain source for IPG/DeviceHub/BookingEngine/HouseKeeping.API/BEMailSender |
| Integration endpoints | Inspect the deployment `Web.config` transforms (redacted here) for live URLs |

---

## 11. Related documents
[15 Known issues & improvements](15-known-issues-and-improvement-suggestions.md) · [11 Integrations & data flow](11-integrations-and-data-flow.md) · [README](README.md).
