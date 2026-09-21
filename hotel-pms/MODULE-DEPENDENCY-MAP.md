# Module Dependency Map

> **Purpose:** Explain how each module of the Hotel PMS is connected to the others — what it produces, what it consumes, and the technical link (shared table / SP / service). Use this to understand ripple effects before changing anything.
> **Grounding:** Modules = MVC Areas in `Scienter.HotelERP.FrontOffice.WebUIMvc/Areas/`. Links verified against source + the live `HotelResWeb_Browns` DB.

---

## 1. Layered dependency (technical stack)

```
  Browser (Razor .cshtml + jQuery/Bootstrap/DataTables/DayPilot/SignalR)
        │  HTTP (MVC action)
        ▼
  Presentation      Scienter.HotelERP.FrontOffice.WebUIMvc  (12 Areas, ~200 controllers)
        │  method call
        ▼
  Business Logic    Scienter.HotelERP.FrontOffice.Service   (189 *Service classes)
        │
        ▼
  Data Access       Scienter.HotelERP.Common.Data           (187 *Entry classes, Dapper)
        │  via
        ▼
  DB Connectivity   Scienter.HotelERP.Common.DbUtility  ──►  SQL Server (2,889 stored procedures)
        ▲
  Domain Models     Scienter.HotelERP.Common.Domain    (shared entity/DTO types, used by all layers)
  Utilities         Scienter.HotelERP.Common.Utility / .AzureUtility
```

**Every functional module depends on all four common layers.** The map below is about *functional* (module-to-module) dependencies.

---

## 2. Module-to-module dependency matrix

Legend: **▲ produces for** (upstream) · **▼ consumes from** (downstream). Read a row as "Module X depends on / feeds …".

| Module (Area) | Depends on (consumes) | Feeds (produces for) | Primary shared link |
|---|---|---|---|
| **Reservation** | Administration (rooms, rates, meal plans, sources), Channel mgrs | Front Office/Check-in, Cashiering (folio), Housekeeping (arrivals), Reporting | `ReservationHeader` → `Inhouse*`; `RoomAvailability_R_Select` |
| **Front Office / Check-in-out** | Reservation (confirmed bookings), Housekeeping (ready rooms), Administration (guest config) | Cashiering (opens folio), Housekeeping (dirty rooms), Reporting | `Reservation_T_QuickCheckInUpdate` / `…QuickCheckOutUpdate` |
| **HouseKeeping** | Front Office (occupancy events), Administration (room master), Maintenance (OOO) | Reservation & Front Office (room availability / check-in gate) | `RoomStatus`, `HouseKeeping_ProcessWiseStatusChanges_Update` |
| **Maintenance** | Administration (assets, room master) | HouseKeeping / availability (OOO blocks rooms) | `OutOfOrderTXN`, `Activities`/`Jobs` |
| **CashieringAndPosting** | Reservation & Front Office (folio, in-house guests), F&B/POS (charges), Administration (tax, charge codes, payment modes) | Reporting, Accounts/Day-end, Check-out | `FolioHeader/Details`, `Posting_InHouse_T_Save`, `BillSettlementDetails` |
| **F&B / Outlets (ProfitCenter/POS)** | Administration (profit centres, items, tax), external POS (`Categlog_vrV2`) | Cashiering (posts charge to folio) | `Posting_InHouse_T_Save` → `Insert_Folio`; `ExtraPostingDetails` |
| **NightAudit / Day-End** | Cashiering (open folios), Reservation (in-house) | Reporting (ledger/summaries), advances hotel date for ALL modules | `DayEnd_CompleteDayEnd_SP_ExecutionSteps`, `DayEndSummaryGuestLedger` |
| **Reporting** | Every transactional module (read-only) | Management / DataAnalysis | `Report*` SPs, `ReportDetails`, SSRS |
| **DataAnalysis** | Every transactional module (read-only) | Management dashboards | `DashboardAPI_*` SPs |
| **Administration** | — (master configuration source) | **All modules** (config data) | `SystemSettings`, master tables |
| **UserAccess** | Administration (users/employees), Central SSO | **All modules** (page/action authorization) | `[UserWisePageAccess]` → `UserAccess_M_AccessPermission` |
| **Auditing** | All modules (change events) | Management / compliance | `AuditTrialService` → `AuditTrial*` (`HotelResWeb_AuditTail` DB) |
| **GuestPortal** | In-house data (folio, room, services) | Reservation/Housekeeping/Cashiering (guest requests) | guest-facing SPs (`GuestPortal_*`) |
| **MealReservation / SpaReservation** | Administration (meal times, spa config), Reservation | Cashiering (posts charges) | `Core_Spa*`, meal allocation tables |
| **Notification** | Check-in/out, day-end, guest events | SMS/Email/WhatsApp/SignalR/RabbitMQ | `Notification*`, `RabbitMQ_*` SPs |

---

## 3. The two "everything depends on it" modules

```
                 ┌──────────────────────────────────────────────┐
                 │            ADMINISTRATION (master data)         │
                 │  rooms · rates · meal plans · tax · charge      │
                 │  codes · payment modes · sources · SystemSettings│
                 └──────────────────────────────────────────────┘
                                     │ configures
     ┌───────────────┬───────────────┼───────────────┬───────────────┐
     ▼               ▼               ▼               ▼               ▼
 Reservation   Front Office   Housekeeping   Cashiering      Reporting
     ▲               ▲               ▲               ▲               ▲
     └───────────────┴───────────────┴───────────────┴───────────────┘
                                     │ authorizes every action
                 ┌──────────────────────────────────────────────┐
                 │        USER ACCESS  (roles & permissions)       │
                 │  [UserWisePageAccess] on BaseController          │
                 └──────────────────────────────────────────────┘
```

- **Administration** is the configuration backbone — nothing works until rooms, rates, tax, charge codes and `SystemSettings` (580 feature-flag rows) are set up. See [08](08-admin-and-configuration-process.md).
- **UserAccess** is the authorization backbone — every controller action is gated by `[UserWisePageAccess(pageId,"S/I/U/D")]` in `BaseController.cs`. See [09](09-user-roles-and-permissions.md).

---

## 4. The critical transactional chain (tightest coupling)

```
 Reservation ──► Check-in ──► Folio (Cashiering) ──► Day-End ──► Check-out ──► Bill/Settlement
     │              │             │                     │            │
 ReservationHeader  Inhouse*   FolioHeader/Details   DayEndSummary  BillHeader/
                                                     GuestLedger    BillSettlementDetails
```

These are **hard-coupled**: a change to the folio schema, the check-in SP, or the day-end step list can break check-out and reporting. Highest-risk area for maintenance.

---

## 5. External dependencies per module

| Module | External system |
|---|---|
| Reservation | Channel managers (Staah, Bookingwhizz, CM/RateTiger), Booking Engine |
| Cashiering / Advances | Sampath IPG (payment gateway) |
| F&B / POS | `Categlog_vrV2` POS DB, `SqlServer2016Inventory` |
| Front Office | Door-lock event log, PABX, `HotelResWeb_PassportScan` |
| Notification | SMS (Mobitel/Dialog), Email, WhatsApp/document delivery, SignalR, RabbitMQ |
| Reporting | SSRS Report Server |
| All | `CentralAccessDB` (SSO), Azure Blob (documents) |

Full detail + directions: [11-integrations-and-data-flow.md](11-integrations-and-data-flow.md).

---

## 6. Change-impact quick reference

| If you change… | Re-test these modules |
|---|---|
| Room status model (`RoomStatus`) | Housekeeping, Front Office check-in gate, Reservation availability |
| Folio schema / posting SPs | Cashiering, F&B posting, Day-end, Check-out, Financial reports |
| Day-end step list | Accounts, Reporting, hotel-date-dependent logic **everywhere** |
| `SystemSettings` flags | Any module reading that flag (search `SystemSettings` usage) |
| Permission model / `BaseController` | **Every** module (authorization) |
| Tax config | Cashiering, F&B, Reservation rate calc, Reports |

---

## 7. Related documents
[00 Project overview](00-project-overview.md) · [12 DB & technical architecture](12-database-and-technical-architecture.md) · [SYSTEM-WIDE-FLOW](SYSTEM-WIDE-FLOW.md).
