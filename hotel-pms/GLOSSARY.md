# Glossary

> **Purpose:** Plain-language explanations of the hotel-industry and system-specific terms used across this documentation. Hotel terms first, then PMS/technical terms, then this system's naming conventions.
> System-specific object names (tables, SPs, controllers) were verified against the source and the live `HotelResWeb_Browns` database.

---

## A. Hotel operations terms

| Term | Plain meaning |
|---|---|
| **PMS** | Property Management System — the core hotel software that manages reservations, front desk, rooms, guest billing and reporting. This product (Scienter HotelERP) is a PMS. |
| **Front Office (FO)** | The reception/front desk function: arrivals, check-in, room allocation, check-out. |
| **Reservation** | A confirmed booking of a room for a guest for specific dates, rate and meal plan. |
| **Folio** | A guest's running bill/account during their stay. Every charge and payment posts to the folio. |
| **Posting** | Adding a charge (room, food, spa, tax) or a payment line to a folio. |
| **Room Rent / Room Revenue** | The nightly charge for the room, usually posted automatically during night audit. |
| **Advance / Deposit** | Money paid before or during the stay, held against the final bill. |
| **Bill / Invoice** | The finalized document the guest settles at check-out. |
| **Settlement** | The act of paying off (closing) the folio/bill by cash, card, bank, etc. |
| **Check-in** | Registering an arriving guest and giving them a room; the reservation becomes "in-house". |
| **Check-out** | The guest settles the bill and leaves; the room is released for cleaning. |
| **In-house** | A guest currently staying (checked in, not yet checked out). |
| **No-show** | A guest who had a confirmed reservation but never arrived. |
| **Walk-in** | A guest who arrives without a prior reservation and books on the spot. |
| **Early check-in / Late check-out** | Arriving before, or leaving after, the standard time — sometimes chargeable. |
| **Group / Block / Allotment** | A set of rooms reserved together (tour group, company, event); an allotment is rooms held for an agent/company. |
| **Rate Code / Rate Plan** | A named price for a room type under certain conditions (season, source, meal plan). |
| **Meal Plan** | What meals are included (Room Only, Bed & Breakfast, Half Board, Full Board, All-Inclusive). |
| **Market Segment** | Business category of the booking (corporate, leisure, group, OTA) — used for analysis. |
| **Booking Source / Channel** | Where the booking came from (walk-in, phone, OTA, company, booking engine). |
| **OTA** | Online Travel Agency (e.g. Agoda, Booking.com) — sells rooms online. |
| **Channel Manager** | Software that syncs room availability/rates/bookings between the PMS and many OTAs (here: Staah, Bookingwhizz, RateTiger/CM). |
| **ADR** | Average Daily Rate — average room revenue per occupied room. |
| **RevPAR** | Revenue Per Available Room — room revenue ÷ total rooms. |
| **Occupancy %** | Occupied rooms ÷ available rooms. |
| **GRC** | Guest Registration Card — the form a guest signs at check-in (this system generates a `'GRC'` number). |
| **Housekeeping (HK)** | The department that cleans and inspects rooms and sets their status. |
| **Room Status** | The current condition of a room — e.g. Occupied, Vacant, Dirty, Clean, Inspected, Ready, Out of Order. |
| **Out of Order (OOO) / Out of Service (OOS)** | A room removed from sale for maintenance; OOO rooms don't count as available. |
| **Turndown** | Evening housekeeping service. |
| **Night Audit / Day-End** | The once-a-day process that posts room rent, freezes the day's figures, produces the guest ledger and revenue/occupancy summary, and advances the hotel's business date. |
| **Guest Ledger** | The total of all in-house guests' outstanding folio balances at a point in time. |
| **City Ledger / Accounts Receivable** | Amounts owed by companies/agents after guests have left (bill-to-company). |
| **Charge Routing / Transfer** | Moving a charge from one folio to another (e.g. to a company/master folio). |
| **Rebate / Adjustment** | Reducing a charge already posted (a correction or goodwill discount). |
| **Void** | Cancelling a posted transaction. |
| **Credit / Debit Note** | Accounting documents that decrease/increase what a guest or company owes. |
| **VIP Level** | A guest's priority/service tier. |
| **Profit Center / Outlet** | A revenue point such as a restaurant, bar, spa, salon or gift shop. |
| **POS** | Point of Sale — the till system in an outlet that records sales (here backed by the separate `Categlog_vrV2` DB). |
| **Hotel / Business Date** | The operational "today" of the hotel, changed only by day-end — not the calendar clock. |

---

## B. PMS / system-specific terms

| Term | Meaning in this system |
|---|---|
| **Property** | One hotel. The platform is multi-property; each property typically has its own `HotelResWeb_<Property>` database. |
| **Multi-tenant / SaaS** | One codebase serves many properties, switching database per property (Destinity Horizon SaaS). |
| **Central SSO** | Single sign-on via `login.inspire.destinity.lk` / `CentralAccessDB`; users log in once for multiple properties. |
| **Area** | An ASP.NET MVC module folder (Reservation, CashieringAndPosting, HouseKeeping, …). |
| **Controller / Action** | A C# class/method that handles a screen or request (e.g. `ReservationCreationController.SaveReservationNew`). |
| **Service** | Business-logic class in `FrontOffice.Service` (e.g. `FolioService`). |
| **Entry class** | Data-access class in `Common.Data` (e.g. `FolioEntry`) that calls stored procedures via Dapper. |
| **Stored Procedure (SP)** | SQL Server routine that does the actual data work; 2,889 exist in the main DB. |
| **SystemSettings** | Key-value feature-flag/config table (580 rows) controlling optional behaviour per property. |
| **Inhouse\* / CheckedOut\* tables** | A reservation's data is copied from `Reservation*` → `Inhouse*` at check-in, and `Inhouse*` → `CheckedOut*` at check-out. |
| **FolioWisePostingBreakUp** | Detailed breakdown of postings per folio (used by day-end room posting). |
| **DayEndSummaryGuestLedger** | The frozen guest-ledger snapshot produced by day-end. |
| **UserWisePageAccess** | The authorization attribute that gates each action by page + operation (S/I/U/D = Select/Insert/Update/Delete). |
| **AuditTrial** (sic) | This system's spelling of "Audit Trail" — the change-tracking mechanism (`AuditTrialService`, `HotelResWeb_AuditTail` DB). |
| **IPG** | Internet Payment Gateway — online card payments via Sampath Bank. |
| **DeviceHub / Fiscal Printer** | Local hardware bridge (e.g. fiscal/receipt printer at `localhost:1304`). |
| **RabbitMQ** | Message queue used to publish events (e.g. `RabbitMQ_GuestCheckIn`) to other systems. |
| **SignalR** | Real-time push to the browser (note: the `NotificationHub` server is currently commented out — see [15](15-known-issues-and-improvement-suggestions.md)). |
| **SSRS** | SQL Server Reporting Services — the report server that renders many reports. |
| **DayPilot** | The calendar/availability-chart UI component. |

---

## C. Naming conventions (how to read object names)

| Pattern | Meaning | Example |
|---|---|---|
| `<Domain>_M_<Action>` | **M**aster (configuration) SP | `MealPlans_M_Select` |
| `<Domain>_T_<Action>` | **T**ransaction SP | `Reservation_T_Save_New` |
| `<Domain>_R_<Action>` | Reporting/read SP | `RoomAvailability_R_Select` |
| `…_Select_ById` / `…_Select_ForGrid` | fetch one row / fetch grid rows | `Activities_M_Select_ForGrid` |
| `…_Save` / `…_Delete` / `…_Update` | write operations | `CancelReservation_M_Save` |
| `…_OLD` / `…_Dev` / `…_OPT` / `…_NEW` | superseded/experimental SP twins — **not canonical** | (see known-issues) |
| `<Name>Controller` | MVC controller (a screen/feature) | `FolioManagementController` |
| `<Name>Service` | business-logic class | `DayEndService` |
| `<Name>Entry` | data-access class | `FolioEntry` |
| Tables with `_YYYYMMDD` / `_bk` / `_History` / `_BeforeRemoval` | dated backups/history — **not the live table** | `FolioDetails_24082025` |

**Status code quick reference (verified):** Reservation — Confirmed 3, Tentative 4, Cancelled 1, No-Show 2, Inquiry 5, Waitlist 6. Room — Occupied (FO 2050), Vacant (FO 2061), Vacant Dirty (HK 2034), Occupied Clean (HK 2030), Vacant Inspected (only this allows check-in), Out of Order 2044 / Out of Service 2045.

---

## D. Sri-Lanka-specific tax terms (this deployment)

| Term | Meaning |
|---|---|
| **VAT** | Value Added Tax (18% in the live config). |
| **SC** | Service Charge (10%) — distributed to staff. |
| **SSCL** | Social Security Contribution Levy (2.56% effective). |
| **TDL** | Tourism Development Levy (1%). |
| **Tax Group** | A bundle of tax types applied together (e.g. "SC + SSCL + VAT" with a combined multiplier). |

---

## E. Related documents
Every term above is used in context in the numbered docs [00](00-project-overview.md)–[15](15-known-issues-and-improvement-suggestions.md). Start with [README](README.md) and [SYSTEM-WIDE-FLOW](SYSTEM-WIDE-FLOW.md).
