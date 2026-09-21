# Hotel PMS Documentation — Scienter HotelERP / Destinity Inspire Front Office

Complete operational + technical documentation for the Hotel Property Management System in this repository.
Every document is grounded strictly in the actual source code and the live `HotelResWeb_Browns` database — nothing is invented, and unconfirmable items are marked **"Not found in the project"** (consolidated in [DOCUMENTATION-GAPS](DOCUMENTATION-GAPS.md)).

> **System in one line:** an ASP.NET **MVC 5** multi-tenant hotel PMS (C# · SQL Server 2019 · **895 tables · 2,889 stored procedures**) covering Reservations, Front Office, Housekeeping, Cashiering, F&B posting, Administration, Reporting and Night Audit for Sri-Lankan hotel chains.

---

## 1. Document index

### Core process documents
| # | Document | What it covers |
|---|---|---|
| 00 | [Project overview](00-project-overview.md) | Purpose, tech stack, modules, roles, architecture |
| 01 | [Complete hotel process](01-complete-hotel-process.md) | Booking → checkout → post-stay, per-stage modules & users |
| 02 | [Front Office process](02-front-office-process.md) | All FO screens: registration, allocation, check-in, room change, walk-in |
| 03 | [Reservation process](03-reservation-process.md) | Create/modify/cancel, group, rates, meal plans, deposits, channels |
| 04 | [Check-in / Check-out](04-check-in-check-out-process.md) | Step-by-step check-in & checkout, deposits, invoice, room release |
| 05 | [Cashiering & finance](05-cashiering-and-finance-process.md) | Folios, postings, taxes, payments, transfers, settlement, day-end |
| 06 | [Rooms & housekeeping](06-rooms-and-housekeeping-process.md) | Room master, status model, cleaning/inspection, OOO/maintenance |
| 07 | [F&B & outlets](07-fnb-and-outlet-process.md) | Profit centres, POS → folio posting, outlet taxes/discounts |
| 08 | [Admin & configuration](08-admin-and-configuration-process.md) | All master setup: property, rooms, rates, tax, charges, settings |
| 09 | [User roles & permissions](09-user-roles-and-permissions.md) | Permission model, 25 roles, action gating, sensitive operations |
| 10 | [Reports & business information](10-reports-and-business-information.md) | Report catalog, categories, SSRS/Excel/dashboards, access control |
| 11 | [Integrations & data flow](11-integrations-and-data-flow.md) | 13 external systems: channels, IPG, SMS, email, RabbitMQ, SSRS |
| 12 | [Database & technical architecture](12-database-and-technical-architecture.md) | Schema, key tables, SPs, layers, request lifecycle, transactions |
| 13 | [End-to-end use cases](13-end-to-end-use-cases.md) | 17 real scenarios in step-by-step form |
| 14 | [Business rules & validations](14-business-rules-and-validations.md) | 60+ rules, status transitions, error-message catalog |
| 15 | [Known issues & improvements](15-known-issues-and-improvement-suggestions.md) | 29 audit findings with evidence and fixes |

### Cross-cutting summaries
| Document | What it covers |
|---|---|
| [SYSTEM-WIDE-FLOW](SYSTEM-WIDE-FLOW.md) | The whole hotel as one flow: Reservation → FO → HK → Cashiering → Accounts → Checkout → Reports |
| [MODULE-DEPENDENCY-MAP](MODULE-DEPENDENCY-MAP.md) | How every module connects; change-impact reference |
| [GLOSSARY](GLOSSARY.md) | Hotel + PMS + technical terms in plain language |
| [DOCUMENTATION-GAPS](DOCUMENTATION-GAPS.md) | Everything that could not be confirmed, and why |

### Complete object catalogs (100% coverage)
| Document | What it covers |
|---|---|
| [APPENDIX-A-tables.md](APPENDIX-A-tables.md) | **Every one of the 895 tables**, grouped by module, with column + row counts, key-table purposes, and backup/variant flags |
| [APPENDIX-B-stored-procedures.md](APPENDIX-B-stored-procedures.md) | **Every one of the ~2,890 stored procedures**, grouped by module then prefix, tagged M/T/R/W, with variant flags |

> The numbered process docs (00–15) cite the *important* SP/table behind each workflow (~437 SPs, ~267 tables in context). The two appendices above give **exhaustive** coverage — every object is listed and linked to the module that owns it. (SP count is a point-in-time snapshot; the live DB fluctuates ±.)

---

## 2. Recommended reading order

**For hotel staff / operations:** [GLOSSARY](GLOSSARY.md) → [01](01-complete-hotel-process.md) → [SYSTEM-WIDE-FLOW](SYSTEM-WIDE-FLOW.md) → your department doc (02/04/05/06/07/10) → [13 use cases](13-end-to-end-use-cases.md) → §12 training manual below.

**For system administrators:** [00](00-project-overview.md) → [08](08-admin-and-configuration-process.md) → [09](09-user-roles-and-permissions.md) → [10](10-reports-and-business-information.md) → [14](14-business-rules-and-validations.md).

**For developers / maintainers:** [00](00-project-overview.md) → [12](12-database-and-technical-architecture.md) → [MODULE-DEPENDENCY-MAP](MODULE-DEPENDENCY-MAP.md) → [05](05-cashiering-and-finance-process.md) (the tightest-coupled core) → [15](15-known-issues-and-improvement-suggestions.md) → [DOCUMENTATION-GAPS](DOCUMENTATION-GAPS.md).

---

## 3. Executive summaries

### 3.1 The complete Hotel PMS process, simply
A guest **books** a room (walk-in, phone, website, OTA, or company). On arrival the front desk **checks them in** — a physical room is assigned and a **folio** (their running bill) is opened. During the stay, **room rent posts automatically each night**, and any **extras** (spa, laundry, F&B) post to the folio too, with taxes added. **Housekeeping** cleans and inspects rooms so they're ready for the next guest. At **check-out** the guest settles the bill, gets an invoice, and the room is released as "dirty" for cleaning. Once a day, **night audit (day-end)** posts room charges, freezes the numbers, and moves the hotel to the next date. **Reports** then tell management how the hotel performed. → [01](01-complete-hotel-process.md), [SYSTEM-WIDE-FLOW](SYSTEM-WIDE-FLOW.md).

### 3.2 How each department uses the system
| Department | Main screens | Main actions |
|---|---|---|
| Reservations | Reservation, Availability Chart | Create/modify/cancel bookings, groups, rates, deposits |
| Front Office | Check-in, Room Allocation, Room Change | Register guests, allocate rooms, check-in/out, room moves |
| Housekeeping | Room Status, Inspection, OOO | Update cleaning status, inspect, block rooms for maintenance |
| Cashier / Front Office cashier | Posting, Folio Management, Settlement | Post charges/payments, advances, transfers, settle bills |
| Accounts / Night Auditor | Day-End Process, Reports | Run night audit, guest ledger, revenue/occupancy, journals |
| Outlets (Spa/Restaurant) | POS / Profit-centre posting | Record outlet sales, charge to room, settle |
| Administration | Administration area (108 controllers) | Configure rooms, rates, tax, charge codes, settings |
| Management / Owner | Reporting, DataAnalysis dashboards | Read revenue, occupancy, ADR/RevPAR, arrivals/departures |
| IT / Admin | UserAccess | Manage users, roles, page/report permissions |

### 3.3 The complete guest lifecycle
`Enquiry → Reservation (Confirmed) → Pre-arrival (deposit, allocation) → Arrival & Check-in (in-house) → Stay (folio charges, extras, room changes) → Payments/Advances → Check-out (settle + invoice) → Post-stay (feedback, documents) → Guest history`.
Technically the record moves `ReservationHeader` → `Inhouse*` (at check-in) → `CheckedOut*` (at check-out), while money lives on `FolioHeader/FolioDetails` → `BillHeader/BillSettlementDetails`. → [01](01-complete-hotel-process.md), [13](13-end-to-end-use-cases.md).

### 3.4 The complete payment & cashiering flow
```
Advance/Deposit ─┐
Room rent (nightly, day-end) ─┤
F&B / Spa / Laundry / Extras ─┼─► FOLIO (FolioHeader/FolioDetails) ─► + Taxes (VAT/SC/SSCL/TDL)
Manual charges ─┘                        │
                                         ▼
                     Payments: cash · card · bank · online (IPG) · currency encashment
                                         │
                                         ▼
                     Settlement (SettleBill → Save_Folio) ─► BillSettlementDetails ─► Invoice
                                         │
                     (unsettled folio BLOCKS checkout: RAISERROR 'UnsettledBills')
```
Charges can be **routed/transferred** between folios or to a company folio; **discounts, voids, rebates and refunds** are permission-gated. Night audit snapshots the **guest ledger**. → [05](05-cashiering-and-finance-process.md).

### 3.5 How an administrator configures the system
Recommended setup order: **Property → Floors/Room Types/Room Categories/Rooms → Bed types & features → Seasons & Rate Codes & Room Rates → Meal Plans → Tax Types & Tax Groups → Charge Codes/Posting Categories → Payment Modes → Market Segments/Booking Sources → Departments/Designations/Staff → Guest types/VIP/Salutations → Companies → `SystemSettings` feature flags (580) → Users, Roles & page/report permissions.** Integration config (email/SMS/channel/IPG) is partly in Administration screens and partly in `Web.config`. → [08](08-admin-and-configuration-process.md), [09](09-user-roles-and-permissions.md).

### 3.6 Main responsibility of each module
| Module | Responsibility |
|---|---|
| Reservation | Own the booking and its lifecycle to check-in |
| Front Office | Arrivals, room allocation, check-in/out, guest profile |
| Housekeeping | Room readiness (clean/inspect) and out-of-order |
| CashieringAndPosting | The folio: all charges, payments, settlement, day-end |
| F&B / Profit centres | Outlet sales and posting them to the guest room |
| Administration | All master/reference configuration |
| UserAccess | Authorize every screen and action |
| Reporting / DataAnalysis | Turn data into management information |
| Auditing | Track who changed what |
| GuestPortal | Guest self-service requests |
| Maintenance / Spa / Meal | Supporting operational sub-modules |

### 3.7 Recommended reading order
See §2 above (role-based paths).

### 3.8 Critical business logic & database procedures (memorize these)
| Concern | Object |
|---|---|
| Create reservation | `Reservation_T_Save_New` (numbering `UpdateNextDocNoWithUpdate 'RESNO'`) |
| Availability | `RoomAvailability_R_Select` (Actual − Reservations − OOO − Balance) |
| Check-in | `Reservation_T_QuickCheckInUpdate` (+ `Reservation_T_FolioCreation`, status `'CKI'`) |
| Check-out | `Reservation_T_QuickCheckOutUpdate` (gate `RAISERROR 'UnsettledBills'`, status `'CKO'`) |
| Room change | `InHouseReservationDetail_T_ChangeRoom` |
| Post charge/payment | `Posting_InHouse_T_Save` / `Posting_WalkIn_T_Save` (POS → `Insert_Folio`) |
| Tax calc | `Folio_T_CalculateTaxTaxGroupWise`, `TaxCalculations` |
| Settle bill | `FolioManagementController.SettleBill` → `Save_Folio` → `BillSettlementDetails` |
| Day-end | steps in `DayEnd_CompleteDayEnd_SP_ExecutionSteps`; room posting `Reservation_T_FolioWisePostingBreakUp_Save`; date roll `DayEnd_UpdateHotelDate` |
| Permission gate | `[UserWisePageAccess]` → `UserAccess_M_AccessPermission` |

### 3.9 What a developer must know to maintain the system
1. **Architecture:** Controller (`WebUIMvc`) → Service (`FrontOffice.Service`) → `*Entry` (`Common.Data`, Dapper) → **stored procedure** → table. Business logic lives mostly in **SPs**, not C#.
2. **Multi-tenant:** one codebase, one DB per property (`HotelResWeb_<Property>`); connection strings `SqlServer2016*`, `PassportDbConnection`, `CentralAccessDbConnectionString`.
3. **The core is hard-coupled:** reservation → `Inhouse*` → folio → day-end → checkout → bill. Test all of these together. → [MODULE-DEPENDENCY-MAP](MODULE-DEPENDENCY-MAP.md).
4. **SP drift is real:** many `_OLD/_NEW/_Dev/_OPT` twins — confirm the canonical SP before editing. Some SPs referenced in code are **not deployed on every property**.
5. **Only 9 of ~18 `.sln` projects are in this checkout** (see [DOCUMENTATION-GAPS](DOCUMENTATION-GAPS.md) §2).
6. **Audit** = `AuditTrialService` → `HotelResWeb_AuditTail` DB. **Real-time SignalR hub is commented out.**
7. **Read [15](15-known-issues-and-improvement-suggestions.md) first** — secrets in `Web.config`, heaps, undeployed SPs.

### 3.10 Hotel-staff training manual (quick start)
> A concise, task-oriented guide. Each task points to the detailed doc.

**Log in:** Use your central SSO account. You only see the screens your **role** allows (25 roles exist — e.g. Front Office Agent, Cashier, Executive Housekeeper). If a button is missing, it's a permission, not a bug.

**Take a booking** *(Reservations)*: Availability Chart → pick dates/room type → enter guest → choose rate & meal plan → save. You get a confirmation number (e.g. `OEB0049910`). Take a deposit if required. → [03](03-reservation-process.md).

**Check a guest in** *(Front Office)*: Open today's arrivals → select the booking → assign a **Vacant Inspected** room (only those are allowed) → capture ID/passport & signature → confirm → the guest is now **in-house** and a folio opens. → [04](04-check-in-check-out-process.md).

**Post a charge** *(Cashier / Outlet)*: Posting screen → select the in-house room → choose charge code → enter amount → save. Taxes apply automatically. Spa/outlet charges can be **charged to the room**. → [05](05-cashiering-and-finance-process.md), [07](07-fnb-and-outlet-process.md).

**Change a room** *(Front Office)*: Room Change → pick guest → pick new (ready) room → confirm. The move is logged. → [02](02-front-office-process.md).

**Check a guest out** *(Cashier)*: Open the folio → review the balance → take payment (cash/card/bank/online) → **settle** → print invoice. If there's an unpaid balance the system **blocks checkout** until it's settled or authorized. The room becomes **dirty** for housekeeping. → [04](04-check-in-check-out-process.md).

**Clean & ready a room** *(Housekeeping)*: Room Status → update **Dirty → Clean**, then Supervisor/**Inspected** → the room becomes bookable again. Block a broken room as **Out of Order**. → [06](06-rooms-and-housekeeping-process.md).

**Close the day** *(Night Auditor)*: Run **Day-End** at end of shift — it posts room rent, freezes the guest ledger and revenue/occupancy, and rolls the hotel date. Don't skip steps. → [05](05-cashiering-and-finance-process.md).

**Read the numbers** *(Manager)*: Reporting area → pick a report (revenue, occupancy, arrivals/departures, cashier). Access depends on your report permissions. → [10](10-reports-and-business-information.md).

**If you see an error code** (e.g. `UnsettledBills`, `104-…`): check the error-message catalog in [14](14-business-rules-and-validations.md) for the cause.

---

## 4. Documentation stats
- **23 documents** (16 numbered + 5 summaries + 2 full object-catalog appendices) · grounded in 9 code projects + a live 895-table / ~2,890-SP database.
- **Object coverage:** process docs cite the key objects in context; **Appendices A & B list 100% of tables and stored procedures**, grouped by module.
- **73 "Not found in the project"** markers ensure honesty about coverage (see [DOCUMENTATION-GAPS](DOCUMENTATION-GAPS.md)).
- Research scratch (object-name lists, generator script, shared pack) is under `_research/` and is not part of the deliverable.
