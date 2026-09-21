# 15 — Known Issues & Improvement Suggestions

> **Product:** Scienter HotelERP — Destinity Inspire / Destinity Horizon Front Office (Hotel PMS)
> **Scope:** A rigorous but fair code + database audit of the Front Office application at `F:\GitHub\destinity-inspire-front-office-v2`, cross-checked against the live `HotelResWeb_Browns` database (`10.4.1.180`, 895 tables / 2,889 procs). Every finding cites a file, controller, stored procedure or table. Counts were measured live (queries run 2026-09-18). Secret **values are never reproduced** — only their location is referenced.
>
> This is an engineering-quality report: it flags bugs, dead/incomplete features, duplicate logic, code referencing objects not deployed, risky areas, security, performance and UX. Where a concern is a *design trade-off* rather than a defect, that is stated. **"Not found in the project"** marks anything unverifiable in this checkout.

---

## Purpose

To give the maintainers a prioritized, evidence-backed list of technical debt, defects and risks — with concrete remediation suggestions — so the team can plan cleanup and hardening without re-deriving the analysis.

## Relevant users / departments

Development team, DBAs, DevOps/security, and the product owner (for prioritization).

## Method & evidence base

- Source tree: **227** `*Controller.cs`, **185** services (`FrontOffice.Service`), **187** data-access `*Entry` classes.
- Live DB: **895** tables, **2,889** procedures, **66** functions, **5** views, **79** foreign keys.
- SP error text harvested directly via `OBJECT_DEFINITION` (488 SPs contain `RAISERROR`).
- Object-existence claims verified with `sys.objects` / `sys.procedures` / `sys.tables`.

---

## Executive summary — issue counts by category

| Category | Count of findings below |
|---|---|
| Bugs / correctness | 3 (#1–#3) |
| Incomplete / dead features | 6 (#4–#9) |
| Duplicate logic | 4 (#10–#13) |
| Code referencing undeployed DB objects | 1 grouped (#14, 3 objects) |
| Risky areas / missing validations | 4 (#15–#18) |
| Security | 4 (#19–#22) |
| Performance | 4 (#23–#26) |
| UX | 3 (#27–#29) |
| **Total** | **29 findings** |

### Top 5 most important issues

1. **#19 — Plaintext production secrets in `Web.config`** (DB passwords, IPG `authToken`/`hmacSecret`, email password, Azure SAS) committed to source control.
2. **#14 — Code calls stored procedures that are not deployed** (`Merge_MultipleFolio`, `Save_Merged_MultipleFolio`, `Reservation_T_SaveSignature`, and the checkout POS gate `Reservations_W_ValidatePOSBill_AtCheckout`) → runtime failures when those paths execute.
3. **#23 — 416 of 895 tables are heaps** (no clustered index) and the schema has only 79 FKs → scan-heavy, integrity-by-convention.
4. **#10/#11 — Massive SP duplication**: 66 `_OLD`, 58 `_NEW`, 52 `_Dev`, 27 `_OPT`, 28 `test` procedures; 58 canonical SPs have an `_OLD` twin → ambiguity about which is authoritative.
5. **#15 — Checkout POS-bill gate silently disabled**: the intended validation SP is missing, so when `SS003` is off the unsettled-POS-bill check is skipped entirely.

---

## Findings

| # | Category | Finding | Evidence (file / SP / table) | Impact | Suggested improvement |
|---|---|---|---|---|---|
| **1** | Bug | **Signature save calls a non-existent SP.** `ReservationHeaderEntry.cs` invokes `Reservation_T_SaveSignature`, which does **not** exist in `HotelResWeb_Browns` (verified `sys.objects` returns nothing). If this path runs, Dapper throws "Could not find stored procedure". | `Common.Data/ReservationHeaderEntry.cs`; SP absent in DB | Guest-signature save fails at runtime on this property. | Deploy the SP, or remove the dead code path; add an integration test asserting every SP referenced in `Common.Data` exists in the target DB. |
| **2** | Bug | **Folio-merge calls two non-existent SPs.** `FolioEntry.cs` references `Merge_MultipleFolio` and `Save_Merged_MultipleFolio`; neither is present in `HotelResWeb_Browns` (verified). | `Common.Data/FolioEntry.cs`; SPs absent | The "merge folios" action errors on Browns (feature partially deployed per-property). | Gate the feature by capability/property, or deploy the SPs everywhere; fail gracefully with a user message instead of a raw SQL error. |
| **3** | Bug | **`GuestPotal_Laundry.cs` is a typo-named near-duplicate of `GuestPortal_Laundry.cs`** (both 1,8xx bytes, same content shape). One is dead; the typo can be wired by mistake. | `Common.Domain/GuestPotal_Laundry.cs` vs `GuestPortal_Laundry.cs` | Confusion / accidental use of the wrong model. | Delete the misspelled duplicate; standardize on `GuestPortal_*`. |
| **4** | Dead feature | **`CreditNotesNOTUSEController` / `DebitNotesNOTUSEController`** are explicitly "NOT USE" but still compiled, still carry `[UserWisePageAccess(3021,…)]` and live `Save*` actions, and contain commented-out branches. | `Areas/CashieringAndPosting/Controllers/CreditNotesNOTUSEController.cs`, `DebitNotesNOTUSEController.cs` | Dead attack/permission surface; superseded by `CreditOrDebitNotesNewController`. | Remove both; keep only `CreditOrDebitNotesNewController`. |
| **5** | Dead feature | **`RoomInspectionDetailsController` (Administration) is an empty stub** — only `Index()` returning a view; the real inspection lives in the HouseKeeping area. | `Areas/Administration/Controllers/RoomInspectionDetailsController.cs` (16 lines) | Orphan menu entry / confusion. | Remove the stub or implement the intended master config. |
| **6** | Dead feature | **SignalR server hub is fully commented out.** `NotificationHub.cs` has its entire class body (incl. `SqlDependency` wiring) commented; the client still references `$.connection.notificationHub`. | `WebUIMvc/Models/Hubs/NotificationHub.cs` (lines 15–84 commented); `Views/Shared/_Layout.cshtml` | Real-time push is dead; client wiring is misleading. | Either delete the SignalR client references or reinstate a working hub; document the `ServiceHub*` DB-polling alternative that is actually used. |
| **7** | Dead feature | **Sampath IPG request/response handlers are largely commented out** in this checkout; `proceed`/response paths redirect rather than call paycorp — yet merchant IDs and secrets are live in config. | `Controllers/SampathIPGController.cs`, `Areas/Administration/Controllers/SampathIPGController.cs`; `Web.config` IPG keys | Online advance/settlement is wired but non-functional here; live secrets exposed for a disabled feature. | Finish/enable or fully stub the integration; do not ship live merchant secrets for a disabled path. |
| **8** | Dead schema | **`Core_ProfitCenter*` — 11 tables, all 0 rows**, and **no C# code references them** (the active path uses `ProfitCenter_txn*`). A parallel "Core_" schema not in use. | `sys.tables` (`Core_ProfitCenter%` = 11, 0 rows); doc 07 | Schema bloat / confusion over the canonical POS tables. | Archive/drop the unused `Core_ProfitCenter*` set, or document it as a future schema. |
| **9** | Dead/empty | **Empty landing-only controllers**: `RoomCleaningScheduleController.Index`, `OOOReasonsController.Index` have views but no wired service in this checkout (per doc 06). `ModuleCategoryWiseTXN` staging table is empty (0 rows) — the module-posting staging feature appears unused on Browns. | doc 06; `ModuleCategoryWiseTXN` (0 rows) | Half-built screens; unclear feature status. | Confirm intended status; implement, hide, or remove. |
| **10** | Duplicate logic | **Pervasive SP versioning duplication.** Live counts: **66 `_OLD`**, **58 `_NEW`**, **52 `_Dev`**, **27 `_OPT`**, **28 `test/…`**, **4 `backup`**, **55 dated (`_2019`–`_2024`)** procedures. **58 canonical SPs have an `_OLD` twin; 16 have a `_NEW` twin.** | `sys.procedures` name-pattern counts | Impossible to know which SP is authoritative; risk of editing the wrong one; deploy drift across properties. | Establish a single source of truth per SP; move history to source control; drop `_OLD/_Dev/_OPT/test/backup/dated` variants from production DBs. |
| **11** | Duplicate logic | **Duplicate `ProfitCenter` controllers**: `ProfitCenterWisePostingController` **and** `Profit_CenterWise_PostingController` both exist in `CashieringAndPosting` (plus an Administration `ProfitCenterController` and a CashieringAndPosting `ProfitCenterController`). | `Areas/CashieringAndPosting/Controllers/ProfitCenterWisePostingController.cs`, `Profit_CenterWise_PostingController.cs`, `ProfitCenterController.cs`; `Areas/Administration/Controllers/ProfitCenterController.cs` | Two code paths for the same POS-posting concept → divergence risk. | Consolidate to one controller/service; delete the redundant variant. |
| **12** | Duplicate logic | **Duplicate `AdvancedPaymentController`** in two areas (Administration + CashieringAndPosting). | `Areas/Administration/Controllers/AdvancedPaymentController.cs`; `Areas/CashieringAndPosting/Controllers/AdvancedPaymentController.cs` | Two advance-payment entry points to maintain. | Pick one canonical location; redirect/remove the other. |
| **13** | Duplicate logic | **Legacy vs. new credit/debit-note stacks coexist**: `DebitAndCreditNotesService` (`CreditNotes_T_Save`/`DebitNotes_T_Save`) alongside `CreditOrDebitNotesNewService` (`CreditOrDebitNote_*`). Plus the NOTUSE controllers (#4). | doc 05; `CreditOrDebitNotesController` (legacy), `CreditOrDebitNotesNewController` | Three overlapping note implementations. | Retire the legacy + NOTUSE paths; keep `CreditOrDebitNotesNew*`. |
| **14** | Undeployed refs | **Code calls SPs absent from the DB** (grouped): `Reservation_T_SaveSignature`, `Merge_MultipleFolio`, `Save_Merged_MultipleFolio` (in `*Entry.cs`), and `Reservations_W_ValidatePOSBill_AtCheckout` (checkout POS gate). All verified **absent** via `sys.objects`. | `ReservationHeaderEntry.cs`, `FolioEntry.cs`, `QuickCheckOutController` | Runtime SQL errors / silently-skipped validation when these paths run on Browns. | Add a startup/CI check that every SP name in `Common.Data` resolves in the target DB; deploy or remove. |
| **15** | Missing validation | **Checkout POS-bill gate is effectively optional and broken.** The unsettled-restaurant-bill check runs only when `SystemSettings SS003` is enabled, and it calls the **missing** `Reservations_W_ValidatePOSBill_AtCheckout`. So when SS003 is off, checkout can proceed with open POS bills; when on, it errors. | `QuickCheckOutController.ValidateRestaurantBillStatus`; SP absent; `SystemSettings SS003` | Guests can check out with unsettled outlet charges (revenue leakage) or checkout errors. | Deploy the SP and make the POS-bill check unconditional for POS-integrated properties. |
| **16** | Missing validation | **No hard over-payment / one-profile-per-NIC constraints.** Settlement enforces total-equality but relies on `BalanceGiven` for change; guest de-dup is search-assisted, not constraint-enforced (only 79 FKs, no unique NIC/passport index found). | `Save_Folio`; `sys.foreign_keys` (79); doc 14 §7 | Duplicate guest profiles; manual over-collection cleanup. | Add a filtered unique index on active NIC/passport; add explicit over-payment handling. |
| **17** | Risky area | **Integrity by convention, not constraints.** With **79 FKs across 895 tables**, most relationships are logical joins inside SPs. Orphan rows and referential drift are possible if an SP misses a cleanup. | doc 12; `sys.foreign_keys` | Data-quality risk on inserts/deletes outside the SP happy-path. | Add FKs on the billing/reservation core (some already exist on `FolioDetails`); add periodic orphan-detection jobs. |
| **18** | Risky area | **Business rules concentrated in 2,889 SPs (488 with `RAISERROR`).** Rules like the checkout gate, tax logic and day-end are opaque to the app tier and vary per-property DB (see #10 drift). | live DB counts | Hard to test, version and reason about; property-to-property behavior divergence. | Introduce SP unit tests (e.g. tSQLt), a schema-diff gate across property DBs, and move a validation contract into the service tier. |
| **19** | Security | **Plaintext production secrets committed in `Web.config`.** DB passwords on all connection strings (lines ~9–13), IPG `authToken`/`hmacSecret` (~86–87), `emailPassword` (~77), SaaS `Password` (~62), and a base64-encoded **Azure Blob SAS** (`LocalStorage`, ~42). *(Locations only — values not reproduced.)* | `WebUIMvc/Web.config` | Full DB, gateway, email and storage compromise if the repo/config leaks. | Move secrets to environment variables / a secret manager (Azure Key Vault); rotate all exposed credentials; use `configBuilders`/encrypted sections; scrub git history. |
| **20** | Security | **Same DB login (`stplfo`) reused across every DB and property**, embedded in config. | `Web.config` connection strings | One credential = access to all tenant DBs (Browns, POS, Passport, Central). | Per-service least-privilege logins; per-tenant credentials resolved at runtime (the SaaS template already supports `{0..3}` — use it). |
| **21** | Security | **SQL built by string in places.** Cross-DB reads use inline `SELECT … FROM Location_Ref` and dynamic per-property connection strings; several `*_SpPara` logging tables capture raw SP calls. While most access is parameterized SPs, the inline paths and `EXEC`-style dynamic SQL inside SPs warrant an injection review. | `ReservationHeaderEntry.cs:~1966`; `*_SP_Para` tables | Potential SQL-injection surface in the non-SP paths. | Audit all `ExecuteQuery`/inline-SQL call sites; ensure parameterization; review dynamic SQL inside SPs. |
| **22** | Security | **Fiscal/DeviceHub and Housekeeping API endpoints are hardcoded HTTP** (`http://localhost:1304`, `http://190.92.199.235:8040/`, vButler `http://10.4.1.180:6069`). No TLS on device/API hops. | `Web.config`; doc 06/11 | Cleartext on local/LAN hops; endpoint spoofing. | Move device/API endpoints to config per environment; use HTTPS where the device supports it; validate responses. |
| **23** | Performance | **416 of 895 tables are heaps** (no clustered index) and there are only **139 non-clustered indexes** total. Heaps + few indexes → table scans on large transaction tables. | `sys.indexes`/`sys.tables` (heaps=416, NC indexes=139) | Slow queries as data grows; fragmentation; forwarded-record overhead. | Add clustered keys (or PK-clustered) to hot heaps (folio/posting/reservation/log tables); index common join/filter columns. |
| **24** | Performance | **Schema bloat from backup/history twins.** Live: **25 dated tables**, **12 `_bk/backup/BeforeRemoval`**, **28 `History`**, **3 `_OLD`**, **11 `_TEMP/tmp`**, **57 `*Log`** tables — plus the SP duplication in #10. | `sys.tables` pattern counts | Larger backups, slower migrations, confusion over canonical objects. | Move backup/dated twins to an archive DB or drop; keep only canonical + intentional history tables. |
| **25** | Performance | **2,889 SPs, many wide/reporting `_W_` and per-property duplicates.** Combined with heaps, reporting SPs (`AuditTrial_W_Select`, availability, day-end) can be expensive. | doc 12; live counts | Report/day-end latency; plan-cache pressure. | Profile the top day-end/reporting SPs; add covering indexes; retire duplicate variants. |
| **26** | Performance | **Cross-DB and inline reads at request time** (POS `Categlog_vrV2`, Passport DB, Central API on every authorized request) add network round-trips; `BaseController` re-validates the SSO token per request. | doc 09/11; `BaseController.CheckTokenValidity()` | Added latency and external-dependency coupling per page load. | Cache token validation for its lifetime; batch/cache cross-DB combos (venues, stock locations). |
| **27** | UX | **Coded error strings leak to users** (`104-…`, `105-…`, `ERR-<message>`, raw SP text like `UnsettledBills`). Users see internal codes and developer phrasing ("please contact scienter"). | doc 14 §8; controllers' `catch` → `"ERR-"+ex.Message` | Confusing, unpolished, sometimes exposes internals. | Map SP error codes to friendly localized messages; never surface raw `ex.Message`. |
| **28** | UX | **Inconsistent JSON error conventions**: some actions return `"ERR-…"`, others `"Err…"`, `"Error -…"`, or a 403 JSON — the client must handle several shapes. | doc 03/06 error scenarios; grep of `"ERR-"`/`"Err"` | Fragile client handling; inconsistent toasts. | Standardize an error envelope (`{ ok:false, message }`) across all JSON actions. |
| **29** | UX | **Validation split confuses the model.** Transaction models (`ReservationHeader.cs`) carry **no** `[Required]`, so bad data saves and only fails at check-in with a server error, while master models do validate client-side — inconsistent feedback timing. | `Common.Domain/ReservationHeader.cs` (no `[Required]`) vs `Company.cs`/`Country.cs`; doc 14 | Late, server-round-trip validation for core flows. | Add client/model validation for mandatory reservation/guest fields to fail fast before check-in. |

---

## Cross-cutting observations (fair-audit notes)

- **What is done well:** transactional integrity (SP `BEGIN TRAN…CATCH…ROLLBACK` + `GEN_ErrTable` logging), a clean layered architecture (Controller → Service → `*Entry` → SP), a genuinely data-driven permission model (deny-by-default, audited), and durable async patterns (RabbitMQ pending/failure logs — 15 SPs; OTA manual re-push — 24 Staah SPs). These are strengths, not defects.
- **Per-property DB drift is the root multiplier.** Many findings (#10, #14, #18) stem from schema/SP divergence between property databases. A schema-diff/deploy pipeline would neutralize a whole class of issues.
- **"Wired but disabled" features** (#6 SignalR, #7 IPG) suggest in-flight work; they should be feature-flagged rather than left as commented code shipping live secrets.

## Limits of this audit

- Verified against **one** property database (`HotelResWeb_Browns`); some referenced objects (#14) may exist in *other* property DBs. Findings marked "absent" mean absent **here**.
- Projects **not in this checkout** (`DeviceHub`, `BEMailSender`, `IPG`, `BookingEngine`, `HouseKeeping.API`, `DayEndSummaryExecution`) could not be inspected — their internals are **Not found in the project** (per Research Pack §3).
- Runtime/performance claims are **static** (schema/index shapes, heap counts) — no query-plan or load profiling was run; treat #23–#26 as directions to profile, not measured regressions.
- Secret exposure is reported by **location only**; the audit did not attempt to use any credential.

## Related documents

- `14-business-rules-and-validations.md` — the rules these gaps weaken or duplicate.
- `05-cashiering-and-finance-process.md`, `07-fnb-and-outlet-process.md` — folio/POS paths behind #2, #8, #11, #15.
- `09-user-roles-and-permissions.md` — the permission model behind #4, #19.
- `11-integrations-and-data-flow.md` — #6, #7, #22 integration status.
- `12-database-and-technical-architecture.md` — schema, SP conventions, transactions (#17, #23–#26).
