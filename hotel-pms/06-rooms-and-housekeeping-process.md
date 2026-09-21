# 06 — Rooms & Housekeeping Process

## Purpose

This document explains how **rooms are configured** and how the **housekeeping process** runs in Scienter HotelERP / Destinity Inspire Front Office: room master data (types, categories, floors, bed types, features), the actual **room status values** used, the **housekeeping cleaning / inspection / supervisor-review workflow**, the **out-of-order / out-of-service (maintenance)** process, and how a room's status controls **Front Office availability and check-in**.

Everything below is grounded in the actual source code (`F:\GitHub\destinity-inspire-front-office-v2`) and the live database (`HotelResWeb_Browns` on SQL Server `10.4.1.180`). Where a fact could not be confirmed in this checkout, it is marked **"Not found in the project."**

## Relevant users / departments

| User / Department | What they do here |
|---|---|
| **System Administrator** | Configures room master data (rooms, types, categories, floors, bed types, features) and the status master lists — `Administration` area. |
| **Housekeeping Supervisor** | Assigns room boys to rooms, reviews/approves cleaning, updates room status — `HouseKeeping` area. |
| **Room Boy / Attendant** | Cleans rooms, updates housekeeping status (via desktop screen or mobile Housekeeping API). |
| **Front Desk / Reception** | Consumes room status for check-in and room allocation; blocked from checking into non-ready rooms. |
| **Maintenance / Engineering** | Places rooms Out of Order / Out of Service and runs maintenance jobs — `Maintenance` + `HouseKeeping/OutOfOrderTXN`. |

## Preconditions

- A logged-in user with property access and the relevant page permission (`[VerifyLoggedUser]` + `[UserWisePageAccess(<pageId>, "<S|I|U|D>")]` on every controller action).
- Room master data configured (rooms exist in `RoomDetails`, with type/category/floor/bed type).
- The property's per-tenant DB (`HotelResWeb_<Property>`) reachable; housekeeping settings row present in `HKSettings`.

---

## 1. Room master data — where it is configured and stored

All room master data is configured under the **Administration** area (`Scienter.HotelERP.FrontOffice.WebUIMvc/Areas/Administration/Controllers/`). Each is a standard CRUD screen (`Landing` → `Grid`/`SelectForGrid` → `Form`/`Edit` → `Save` → `Delete`) backed by a `*Service` → `*Entry` → master stored procedure.

| Concept | Business meaning | Controller | Service → Entry | Master table | Key SPs | Live count (Browns) |
|---|---|---|---|---|---|---|
| **Room** | A physical sellable room (its code, type, category, floor, bed type, area, features) | `RoomDetailsController` (pageId 36) | `RoomDetailService` → `RoomDetailEntry` | `RoomDetails` | `RoomDetails_M_Save`, `RoomDetails_M_Select`, `RoomDetails_M_Select_ById`, `Roomdetails_M_Delete` | **1,087 rooms** |
| **Room Type** | Bed configuration / physical layout (e.g. Double, Twin) | `RoomTypesController` (41) | `RoomTypeService` → `RoomTypeEntry` | `RoomTypes` | `RoomTypes_M_Save`, `RoomTypes_M_Select`, `RoomTypes_M_SelectForAddRoom` | 48 |
| **Room Category** | Sales/rate grouping (e.g. Luxury, Deluxe) — the unit of availability | `RoomCategoriesController` (35) | `RoomCategoryService` → `RoomCategoryEntry` | `RoomCategories` | `RoomCategories_M_Save`, `RoomCategories_M_Select`, `RoomCategories_M_SelectForAvailability` | 91 |
| **Floor** | Building floor / level | `FloorsController` (14) | `FloorService` → `FloorEntry` | `Floors` | `Floors_M_Save`, `Floors_M_Select`, `Floors_M_Select_ByDisplayOrder` | 33 |
| **Bed Type** | Bed size/kind assigned to a room | `BedTypesController` (1) | `BedTypeService` → `BedTypeEntry` | `BedTypes` | `BedTypes_M_Save`, `BedTypes_M_Select` | 4 |
| **Room Feature / Attribute** | Amenities/attributes of a room (e.g. Sea View) | `RoomFeaturesController` | `RoomFeaturesService` → `RoomFeaturesEntry` | `RoomFeatures` | `RoomFeatures_M_Save`, `RoomFeatures_M_Select_ForGrid`, `RoomFeatures_M_SelectById` | 1 |
| **Room Area** | Physical zone within a room used for allocation | `RoomAreasController` (33) | `RoomAreaService` → `RoomAreaEntry` | `RoomAreas` | `RoomAreas_M_Save`, `RoomAreas_M_Select` | — |

**Room record fields** (from `RoomDetails` columns): `RoomCode`, `RoomTypeId`, `RoomCategoryId`, `RoomAreaId`, `RoomFloorId`, `BedTypeId`, `CleaningCredit`, `RoomIndex`, `IsDriverRoom`, `ConciderForOccupancy`, plus the five live status columns (see §2). When saving a room, `RoomDetailsController.Save` passes both the room and its selected **room features** — the `Form`/`Edit` actions preload the feature checklist via `HKChangeService().HKRoomFeatureSelect()`.

> Room categories store an image (uploaded to Azure Blob via `FileUploadUtility.UploadDocumentByte("RoomCategories", …)`), and support a **Villa** grouping (`AssignVillaCategories` → `RCategoryWiseRoomDetails_M_Save`).

**Room Boy master:** managed via `RoomBoyDetailsController` (pageId 12). Its combo uses `RoomBoyDetailService` (`RoomBoyDetails_M_Select`), but its CRUD grid/form delegate to `EmployeeService` — i.e. **room boys are employees** flagged for housekeeping.

---

## 2. Room statuses — the ACTUAL values used

The system tracks **five parallel status dimensions** per room. They are stored on the room record itself:

`RoomDetails` current-status columns (verified via `sys.columns`):

| Column | Dimension | Category id |
|---|---|---|
| `CurrentFrontOfficeStatusId` | Front Office status | 1 |
| `CurrentHouseKeepingStatusId` | Housekeeping status | 2 |
| `CurrentGuestStatusId` | Guest status | 3 |
| `CurrentReservationStatusId` | Reservation status | 4 |
| `CurrentTurnDownStatusId` | Turndown status | 5 |

These IDs point into the **unified `RoomStatus` master table** (one table, split by `RoomStatusCategory`). This is confirmed by the update stored procedure `HouseKeeping_UpdateRoomStatus`, which routes each incoming `{RoomId, RoomStatusCategoryId, RoomStatusId}` to the matching `RoomDetails.Current*StatusId` column based on the category id (2→HK, 3→Guest, 5→Turndown, 1→FO, 4→Reservation).

> **Important — two status master tables coexist.** There is an older pair of masters, `HouseKeepingStatus` (14 rows) and `FrontOfficeRoomStatus` (5 rows), each with prefix codes and an `IsAllowToCheckIn` flag. These are administered by `RoomStatusController.SelectHouseKeepingStatus` (`HouseKeeping_Status_Select`) and `FrontOfficeRoomStatusController`. **However**, the live `RoomDetails.Current*StatusId` values in Browns all reference the **unified `RoomStatus` table** (IDs 2050/2061/2067 for FO; 6/22/2030/2033/2034/2044 for HK) — confirmed by `SELECT DISTINCT` on `RoomDetails`. The unified `RoomStatus` table (category-driven) is therefore the **operational** master; the `HouseKeepingStatus`/`FrontOfficeRoomStatus` pair is legacy/reference. Both are documented below.

### 2a. Status categories (`RoomStatusCategory`)

| Id | Category | Code | Icon |
|---|---|---|---|
| 1 | Front Office Status | fos | vacant.png |
| 2 | House Keeping Status | hks | tie.png |
| 3 | Guest Status | gs | user_mark.png |
| 4 | Reservation Status | rs | credit-card.png |
| 5 | Turndown Status | tds | bed.png |

### 2b. Operational status legend — unified `RoomStatus` table (live, Browns)

**Front Office statuses (category 1):**

| Id | Status | Business meaning |
|---|---|---|
| 2050 | **Occupied** | A guest is in the room. |
| 2061 | **Vacant** | No guest in the room. |
| 2067 | **Out of Order / Service** | Room withdrawn from front-office sale (maintenance/repair). |

**Housekeeping statuses (category 2)** — this is the cleaning lifecycle:

| Id | Status | OOO entry? | Allow Check-In? | Allow Room Change? | Business meaning |
|---|---|---|---|---|---|
| 2034 | **Vacant Dirty** | – | No | No | Empty but not yet cleaned. |
| 2033 | **Vacant Clean** | – | No | No | Empty and cleaned, awaiting inspection. |
| 22 | **Vacant Inspected** | – | **Yes** | **Yes** | Empty, cleaned **and inspected** → ready to sell/check-in. |
| 2068 | **Vacant Ready** | – | – | – | Empty and ready (see `HKSettings.VacantReadyStatusId`). |
| 6 | **Occupied Dirty** | – | No | No | Guest in room, needs cleaning. |
| 2030 | **Occupied Clean** | – | No | No | Guest in room, cleaned. |
| 1030 | **Occupied Inspected** | – | No | No | Guest in room, cleaned and inspected. |
| 2031 | **Occupied Ready** | – | No | No | Guest in room, serviced and ready. |
| 2044 | **Out of Order** | **Yes** | No | No | Room being repaired; still counted in inventory but not sellable. |
| 2045 | **Out Of Service** | **Yes** | No | No | Room removed from inventory for a reason (e.g. repairs). |

**Guest statuses (category 3):** `2032 Sleep Out`, `2035 Do Not Disturb`, `2036 Light Baggage`, `2037 Refuse Service`, `2038 No Baggage`, `2064 N/A`.

**Reservation statuses (category 4):** `2039 Stay Over`, `2040 Not Reserved`, `2041 Due Out`, `2042 Arrival`, `2043 Departed`, `2048 Arrived`, `2049 Due In`, `2065 Due Out/Arrival`, `2066 Due In/Departure`.

**Turndown statuses (category 5):** `2047 TD Completed`, `2062 TD Requested`, `2063 TD Not Requested`.

> The **only housekeeping status that permits check-in and room change is `22 Vacant Inspected`** (`IsAllowCheckIn = 1`, `IsAllowRoomChange = 1`). Every other HK status blocks check-in. `Out of Order` (2044) and `Out Of Service` (2045) are the only ones flagged `IsApplicableforOutOfOrderEntry = 1`, so they are the two release/target statuses offered on the Out-of-Order screen (`RoomStatusController.RoomStatusCombo` → `HouseKeeping_RoomStatus_Select_ByCategory`).

### 2c. Legacy status legend — `HouseKeepingStatus` master (14 rows)

Column set: `Id, Name, Prefix, Remarks, Color, IsOccupied, FO_RoomStatusID, IsActive, IsAllowToCheckIn, GroupId`.

| Prefix | Name | IsOccupied | IsAllowToCheckIn |
|---|---|---|---|
| VC | Vacant Clean | 0 | 0 |
| VD | Vacant Dirty | 0 | 0 |
| INS | Vacant Inspected | 0 | **1** |
| NB | No Baggage | 0 | 0 |
| OC | Occupied Clean | 1 | 0 |
| OD | Occupied Dirty | 1 | 0 |
| OR | Occupied Inspected | 1 | 0 |
| DP | Departed | 0 | 0 |
| DND | Do Not Disturb | 1 | 0 |
| LB | Light Baggage | 0 | 0 |
| RS | Refuse Service | 1 | 0 |
| SO | Sleep Out | 1 | 0 |
| OOO | Out Of Order | 0 | 0 |
| OOS | Out Of Service | 0 | 0 |

Legacy **Front Office** master `FrontOfficeRoomStatus` (5 rows): `RES Reservation`, `INH In-House`, `OOO Out Of Order`, `AVL Available`, `PEN Pending`.

### 2d. Housekeeping status **icon system**

The desktop room-status boards render each status as a coloured icon from
`Scienter.HotelERP.FrontOffice.WebUIMvc/Images/HouseKeepingIcons/` (also documented as the *"Housekeeping Room Status Icon System"* community in `graphify-out/GRAPH_REPORT.md`). Confirmed asset files include:

```
Vacant.png  VacantClean.png  VacantDirty.png  VacantInspected.png
Occupied.png  OccupiedClean.png  OccupiedDirty.png  OccupiedInspected.png  OccupiedReady.png
OutofOrder.png  OutOfService.png  OOO.png  SleepOut.jpg
VC-S.png  VD-S.png  OC-S.png  OD-S.png  OI-S.png  OR-S.png  OO-S.png  OS-S.png   (small "-S" variants)
```

Colour/shape convention (per the graph community): **Green = Vacant**, **Square "-S" = the small variant**, `*-OLD.png` files are superseded prior icons. Master source: `Scienter Front Office HouseKeeping Icons.png` / `Scienter Front Office.cdr`.

---

## 3. Housekeeping workflow — step by step

The daily housekeeping cycle spans four screens in the `HouseKeeping` area:
**assign room boys → cleaning/status update → room inspection → supervisor review.**

### 3.1 Assign room boys (and supervisors) to rooms

**Screen:** `HouseKeeping/AssignRoomBoys` and `HouseKeeping/SupervisorWiseRooms`
**Controller:** `HouseKeepingController` (`AssignRoomBoys` pageId 13098; `SupervisorWiseRooms` pageId 14969)

1. **User action** — Supervisor opens *Assign Room Boys*. The page loads all room boys (`RoomDetailService.SelectRoomBoys` → `RoomBoys_M_Select`) and rooms (`RoomDetailService.Select(ActiveOnly)`) into a `HouseKeepingRoomBoyViewModel`.
2. **Assignment** — For a given `hotelDate` and `inspectionTimeId`, the supervisor drags/ticks rooms for each room boy.
3. **Save** — `SaveHouseKeepingRoomBoys(List<RoomWiseRoomBoys>)` → `RoomDetailService.SaveHouseKeepingRoomBoys` → `HouseKeeping_M_SaveRoomWiseRoomBoys`.
4. **Database change** — writes to `Housekeeping_RoomWiseRoomBoys` (columns: `RoomId, RoomBoyId, HotelDate, InspectionTimeId, CleaningPatternId, IsArea, PropertyId`) and mirrors to `Housekeeping_RoomWiseRoomBoys_Log`.
5. **Supervisor-wise** — `SupervisorWiseRooms` assigns rooms to a supervisor: `SaveSupervisorWiseRooms` → `HouseKeeping_M_SaveSupervisorWiseRooms` → table `Housekeeping_SupervisorWiseRooms` (+ `_Log`). Existing assignments read back via `SelectSupervisorWiseAssignedRooms` (`HouseKeeping_M_SelectSupervisorWiseAssignedRooms`).
6. **Result** — Returns `"OK"` or `"ERR-<message>"`.

### 3.2 Cleaning & housekeeping-status update

Two desktop paths exist plus the mobile API (§6). Both change the room's HK/FO status.

**Path A — Update Housekeeping Status board**
**Screen:** `HouseKeeping/UpdateHouseKeepingStatus/Landing` (also newer `UpdateHouseKeepingStatusNew`)
**Controller:** `UpdateHouseKeepingStatusController` (pageIds 3019/4028/4029)

1. Board loads current status per room via `UpdateHouseKeepingStatusService.SelectStatus(DateTime.Now, filteringCriteria, frontOfficeStatusId)` → `UpdateHouseKeepingEntry.Select` → `HouseKeeping_M_Select_DateWise`. Rooms can be filtered by category, floor (`FloorService.Select("active-only")`) and FO status.
2. User selects rooms and a new status.
3. **Save** — `UpdateRoomStatus(List<HouseKeepingStatusUpdateTXN>)` → `UpdateHouseKeepingStatusService.Save` → `UpdateHouseKeepingEntry.Insert` → **`HouseKeeping_UpdateRoomStatus`** (JSON payload).

**Path B — HK Change / room-search board**
**Screen:** `HouseKeeping/HKChange/Index`
**Controller:** `HKChangeController` → `HKChangeService`

- Provides cascading filters: room categories, floors, HK/FO/service status, room features (`HKRoomCategoriesSelect`, `HKFloorSelect`, `HKHouseKeepingRoomStatusSelect`, `HKFrontOfficeRoomStatusSelect`, `HKRoomFeatureSelect`, `ReservationPrioritySelect`).
- Search rooms: `HKStatusWiseRoomSearch(HKChange)` (POST).
- Update status: `HKHouseKeepingStatusUpdate(HKChange)` (POST) → returns `"OK"`/`"Err<msg>"`.
- Also `HKGuestServiceStatusUpdate` (guest-service flags) and `HKRemoveRoomsFromQueue` (remove rooms from the cleaning queue).

**What `HouseKeeping_UpdateRoomStatus` does** (verified SP body — this is the heart of every status change):
1. Parses the incoming JSON array of `{RoomId, RoomStatusCategoryId, RoomStatusId}` (via `OPENJSON`).
2. For each row, updates the matching `RoomDetails.Current*StatusId` column by category (2→HK, 3→Guest, 5→Turndown, 1→FO, 4→Reservation).
3. Writes an audit entry via `HotelResWeb_AuditTail_WriteToLog 'RoomDetails', …, 'FO','HKS','I', …`.
4. Upserts a **daily transaction row** in `HouseKeepingStatusUpdate_TXN` (one row per room/category/date) and always appends to `HouseKeepingStatusUpdate_Log`.

**Status-transition rules** are data-driven, not hard-coded. Two tables govern them:
- `FrontOfficeStatusWiseHouseKeepingStatus` — which HK statuses are permitted under each FO status (surfaced by `RoomStatusController.FrontOfficeStatusWiseHouseKeepingStatus` → `HouseKeeping_FrontOfficeStatusWiseHouseKeepingStatus`). Live mapping in Browns:

  | Front Office status | Allowed housekeeping statuses |
  |---|---|
  | **Occupied** | Occupied Clean · Occupied Dirty · Occupied Inspected · Occupied Ready |
  | **Vacant** | Sleep Out · Vacant Clean · Vacant Dirty · Vacant Inspected |
  | **Out of Order / Service** | Out of Order · Out Of Service |

- `HouseKeeping_ProcessWiseStatusChanges` — process-code → target (FO status, HK status), applied by SP `HouseKeeping_ProcessWiseStatusChanges_Update`. Codes seen live: `CKI` (check-in), `CKO` (check-out), `DEAUT` (day-end auto), `DND`, `OOO`, `OOS`, `OOR`, `RINS` (reinstate), `RCGN`/`RCGO` (room change new/old), `RICK`. That SP calls `HouseKeeping_UpdateRoomStatus` twice (HK + FO) and then `Admin_T_LinenChange` to log linen usage.

### 3.3 Room inspection

**Screen:** `HouseKeeping/RoomInspection/Landing`
**Controller:** `RoomInspectionController` (pageId 11009) → `RoomInspectionService` → `RoomInspectionEntry`

1. Supervisor picks an **inspection time** (`RoomInspectionTimesCombo` → `RoomInspectionTimes_M_Select`; live times = *Morning / Mid Day / Evening*) and date.
2. Grid of rooms to inspect: `GetGridData(inspectionTimeId, inspectionDate)` → `RoomInspection_T_Select_ForUpdate`.
3. **Save** — `Save(List<RoomInspection>, saveType)` → `RoomInspectionService.SaveRoomInspection` → **`RoomInspectionDetails_T_Save`**.
4. **Database change** — inserts into `RoomInspectionDetails` recording, per room: the **entered** `HouseKeepingStatusId` and `RoomTypeId` vs. the room's **actual** `CurrentHouseKeepingStatusId` / `RoomTypeId` (stored as `ActualHouseKeepingStatusId` / `ActualRoomTypeId`), inspection time, remark, user, timestamp. This lets the hotel spot discrepancies between what the room boy reported and the inspector's finding.

> `Administration/RoomInspectionDetailsController` is an **empty stub** (`Index` only) in this checkout — inspection master config there is **Not found in the project**; the operational inspection lives entirely in the `HouseKeeping` area.

### 3.4 Supervisor review (cleaning approval + checklist)

**Screen:** `HouseKeeping/SupervisorReview/Index`
**Controller:** `SupervisorReviewController` (pageId 14956) → `SupervisorReviewService` → `SupervisorReviewEntry`

1. Supervisor selects a room boy (`SelectRoomBoys`) and loads that room boy's assigned rooms with checklist progress: `SelectRoomBoyAssignRooms(roomBoyId)` → `HK_RoomBoyWiseRoomChecklistProgress_T_SelectByRoomBoyId`.
2. Supervisor reviews changes made by the room boy: `RoomBoyUpdates(roomId, roomBoyId)` → `HK_RoomBoyChangesByRoomIdAndRoomBoyId`.
3. **Save decisions** — `SaveSupervisorDecisions(SupervisorReview)` → `HK_RoomBoyWiseRoomChecklistProgress_T_Update`.
4. **Database change** — `HKRoomBoyWiseRoomChecklistProgress` records, per room/room-boy/date: `CheckListItemList`, `StartTime`/`EndTime`/`ActualTime`, `CurrentHouseKeepingStatusUpdatedByRoomBoy`, and the supervisor fields `SupervisorApproved`, `SupervisorApprovedDateTime`, `SupervisorRemark`, `SupervisorCheckListItemList`, `CurrentHouseKeepingStatusUpdatedSupervisor`. Checklist definitions live in `HKCheckListItems` and `HKRoomCategoryWiseCheckListItemWithDefaultValues`.

### 3.5 Room cleaning schedule & OOO reasons (config screens)

- `RoomCleaningScheduleController.Index` — cleaning-schedule landing (view only in this checkout; underlying schedule data **Not found in the project** as a wired service).
- `OOOReasonsController.Index` — landing shell for out-of-order reasons (master CRUD is in Administration, §4).
- Cleaning-pattern master exists as table `Housekeeping_CleaningPatterns` (referenced by `Housekeeping_RoomWiseRoomBoys.CleaningPatternId`).

---

## 4. Maintenance & Out-of-Order / Out-of-Service process

### 4.1 Placing a room Out of Order / Out of Service

**Screen:** `HouseKeeping/OutOfOrderTXN/Landing`
**Controller:** `OutOfOrderTXNController` (pageId 4166) → `OutOfOrderTXNService` → `OutOfReasonsTXNEntry`

| Action | Method → SP |
|---|---|
| List existing OOO records | `SelectForGrid` → `OutOfOrderTxn_Select_ForGrid` |
| Open form (pick rooms, dates, reason, release-as) | `Form` / `RoomList` (`Select_M_RoomList`) |
| **Save** | `Save(OutOfOrderTXN)` → `OutOfOrderTXNService.Insert` → **`OutOfOrderTXN_M_Insert`** |
| Room-wise list | `SelectOutOfOrderListRoomWise(roomId)` → `OutOfOrder_T_Select_RoomWise` |
| Quick delete (release) | `QuickDeleteRoomWise(id)` → `OutOfOrder_T_RoomWise_QuickDelete` |
| Delete | `Delete(id)` → `OutofOrderTxn_M_Delete` |

**`OutOfOrderTXN` record** (verified columns): `RoomId, FromDate, ToDate, OutOfOrderReasonId, OutOfOrderStatusId, ReleaseAsId, Remarks, PropertyId`.
- **Reasons** are master data from `OutOfOrderReasons` (Administration `OutOfOrderReasonsController`, pageId 24 → `OutofOrderReasons_M_Select`). Live examples: *AC REPAIR, ROOM CONSTRUCTION, ROOM PAINTING, WATER LEAKING, DOOR LOCK ERROR, VVIP FUNCTION*.
- **`OutOfOrderStatusId`** = the target HK status (`2044 Out of Order` or `2045 Out Of Service`). **`ReleaseAsId`** = the HK status the room returns to when the OOO period ends.

**What `OutOfOrderTXN_M_Insert` enforces** (verified SP body — the business rules live here):
1. Requires at least one selected room; rejects `FromDate > ToDate` and `FromDate = ToDate`.
2. Distinguishes **Out of Service** (`IsOutOfService = 1` → status `2045`, process `OOS`) from **Out of Order** (process `OOO`, only applied when the OOO start = today's hotel date).
3. Sets the room status by calling **`HouseKeeping_ProcessWiseStatusChanges_Update 'OOO' | 'OOS'`** (which flips FO → *Out of Order/Service* and HK → *Out of Order* / *Out Of Service* per §3.2).
4. **Blocks conflicts** — refuses the block if the room, within the date range, is already OOO, allocated to an in-house reservation (`InhouseReservationDetails`), or allocated to a future reservation (`ReservationDetails`). Errors: *"Room already has been out of order."*, *"Room already allocated to an Inhouse reservation."*, *"Room already allocated to a reservation."*
5. Pushes an availability update to the **Staah** channel manager (`Staah_AvailabilityPush`) for each affected date so OTAs stop selling the room.

### 4.2 Maintenance module (jobs / preventive maintenance / assets)

The broader **`Maintenance` area** manages engineering work (distinct from the OOO block itself):

| Function | Controller | Service → SP root |
|---|---|---|
| Maintenance jobs | `JobsController`, `JobWiseNotesController`, `JobTypesController` | `JobService` → `Maintenance_Jobs_M_Save/Select` |
| Preventive maintenance schedules | `PreventiveMaintenanceScedulesController` | `PreventiveMaintenanceSceduleService` → `PreventiveMaintenanceScedule_M_Save` |
| Assets & asset types | `AssetsController`, `AssetsTypesController` | `Assests_M_Save` |
| Activities / maintenance types | `ActivitiesController`, `MaintenanceTypesController`, `ActivityWiseMaintenanceTypesController` | `Activities_M_Save`, `MaintenanceTypes_M_Save` |
| Locations / production centers | `LocationsController`, `ProductionCentersController` | `Locations_Save`, `ProductionCenters_M_Save` |
| Settings | `MaintenanceSettingController` | `MaintenanceSettings_M_Update` |

A `ServiceHub` (Administration `ServiceHubController`) dispatches guest-service/maintenance jobs to department assignees (`ServiceHub_ServiceJob_M_Save`).

---

## 5. How room status drives Front Office availability & check-in

Room status is the gate between housekeeping and the front desk. Two mechanisms:

**A. Category-level availability (booking/allocation).**
The availability calculation `RoomAvailability_R_Select` (verified) computes, per room category per date:

```
AvailableRooms = ActualRooms − ( ReservationCount + OOOCount + RoomBalance )
```

where `OOOCount` is drawn straight from `OutOfOrderTXN` (a `#tempOOORooms` temp table joined by category/date). **Out-of-Order and Out-of-Service rooms are therefore subtracted from sellable inventory** for every date in their block, so they cannot be reserved or allocated. In Browns today, 8 rooms carry FO status *Out of Order/Service* (2067) and HK *Out of Order* (2044), matching live OOO transactions.

**B. Room-level check-in gate.**
Check-in and room-change eligibility are governed by the housekeeping status flags on `RoomStatus`:
- **`IsAllowCheckIn`** — only `22 Vacant Inspected` = 1. A room that is Vacant Dirty / Vacant Clean / Occupied / OOO / OOS cannot be checked into.
- **`IsAllowRoomChange`** — same: only *Vacant Inspected* permits a room move.
- Legacy `HouseKeepingStatus.IsAllowToCheckIn` mirrors this (only INS = 1).

`HKSettings` wires the automatic transitions used at the desk (verified live values, Browns):

| Setting | Value | Meaning |
|---|---|---|
| `CheckInRoomStatusId` | 22 (*Vacant Inspected*) | Status a room must have (and is set to) at check-in |
| `OOORoomStatusId` | 2044 (*Out of Order*) | Default OOO status |
| `VacantReadyStatusId` | 2034 (*Vacant Dirty*) | "ready/reset" status after checkout in this property |
| `HouseKeepingApiUrl` | `http://190.92.199.235:8040/` | Base URL of the mobile Housekeeping API |

**End-to-end example:** guest checks out → process code `CKO` → `HouseKeeping_ProcessWiseStatusChanges_Update` sets FO = *Vacant*, HK = *Vacant Dirty* → room boy cleans and updates HK = *Vacant Clean* → supervisor inspects and sets HK = *Vacant Inspected* (`IsAllowCheckIn = 1`) → front desk can now allocate/check-in the next guest.

---

## 6. Housekeeping via the mobile Housekeeping API

- The mobile API base URL is configured in `HKSettings.HouseKeepingApiUrl` (live: `http://190.92.199.235:8040/`), and the web app exposes its own base to the API via `HKSettings.FrontOfficeBaseUrl`. This confirms room boys update status from a **mobile device**, hitting the same status pipeline (`HouseKeeping_UpdateRoomStatus`).
- The project **`Scienter.HotelERP.HouseKeeping.API`** is referenced in the solution's source-control bindings (`Scienter.HotelERP.sln`, `SccProjectName14 = Scienter.HotelERP.HouseKeeping.API`) **but the project folder is not present in this checkout** — its internal controllers/endpoints are **Not found in the project** (searched: repo root, all `*.csproj`, `Areas/HouseKeeping`). Documented here from the configuration and solution reference only.

---

## 7. Screens / modules involved

| Screen (route) | Controller | Purpose |
|---|---|---|
| `HouseKeeping/UpdateHouseKeepingStatus/Landing` | `UpdateHouseKeepingStatusController` | Update room HK/FO status board |
| `HouseKeeping/HKChange` | `HKChangeController` | Filtered room search + status change |
| `HouseKeeping/HouseKeeping/AssignRoomBoys` | `HouseKeepingController` | Assign room boys / supervisors to rooms |
| `HouseKeeping/RoomInspection/Landing` | `RoomInspectionController` | Record room inspections |
| `HouseKeeping/SupervisorReview` | `SupervisorReviewController` | Approve cleaning + checklist |
| `HouseKeeping/RoomStatus/Landing` | `RoomStatusController` | Maintain unified `RoomStatus` master |
| `HouseKeeping/RoomStatusChart/Landing` | `RoomStatusChartController` | Visual room-status board (by floor/date) |
| `HouseKeeping/OutOfOrderTXN/Landing` | `OutOfOrderTXNController` | Out-of-Order / Out-of-Service blocks |
| `Administration/RoomDetails`, `RoomTypes`, `RoomCategories`, `Floors`, `BedTypes`, `RoomFeatures`, `RoomBoyDetails`, `OutOfOrderReasons`, `FrontOfficeRoomStatus`, `HKSettings` | (respective) | Room + housekeeping master data |

## 8. Database / API involvement

- **Master tables:** `RoomDetails`, `RoomTypes`, `RoomCategories`, `Floors`, `BedTypes`, `RoomFeatures`, `RoomAreas`, `RoomBoyDetails`, `RoomStatus`, `RoomStatusCategory`, `HouseKeepingStatus`, `FrontOfficeRoomStatus`, `OutOfOrderReasons`, `RoomInspectionTimes`, `HKCheckListItems`, `HKSettings`.
- **Transaction/log tables:** `OutOfOrderTXN`, `HouseKeepingStatusUpdate_TXN`, `HouseKeepingStatusUpdate_Log`, `HK_HouseKeeping_Status_Update_Log`, `Housekeeping_RoomWiseRoomBoys` (+ `_Log`), `Housekeeping_SupervisorWiseRooms` (+ `_Log`), `HKRoomBoyWiseRoomChecklistProgress` (+ `_Log`), `RoomInspectionDetails`.
- **Core SPs:** `HouseKeeping_UpdateRoomStatus`, `HouseKeeping_ProcessWiseStatusChanges_Update`, `OutOfOrderTXN_M_Insert`, `RoomInspectionDetails_T_Save`, `RoomAvailability_R_Select`, `HouseKeeping_FrontOfficeStatusWiseHouseKeepingStatus`, `HouseKeeping_M_SaveRoomWiseRoomBoys`, `HK_RoomBoyWiseRoomChecklistProgress_T_Update`.
- **API:** mobile Housekeeping API (`Scienter.HotelERP.HouseKeeping.API`) — URL in `HKSettings.HouseKeepingApiUrl`; project not in checkout.

## 9. Business rules

1. A room can only be **checked into when its HK status = Vacant Inspected** (`RoomStatus.IsAllowCheckIn = 1`); the same status also gates room changes (`IsAllowRoomChange`).
2. Housekeeping status changes are **always mediated by `HouseKeeping_UpdateRoomStatus`**, which updates `RoomDetails.Current*StatusId`, audits, and logs (`HouseKeepingStatusUpdate_TXN` / `_Log`).
3. **Permitted status transitions are data-driven** by `FrontOfficeStatusWiseHouseKeepingStatus` (FO→HK) and `HouseKeeping_ProcessWiseStatusChanges` (event→status).
4. An OOO/OOS block **cannot overlap** an existing block or any in-house/future reservation for that room, and reduces category availability for every blocked date; it also notifies the Staah channel manager.
5. Only `Out of Order (2044)` and `Out Of Service (2045)` are valid OOO target/release statuses (`IsApplicableforOutOfOrderEntry = 1`).
6. Room inspection records both the **reported** and the **actual** HK status/room type to surface discrepancies.

## 10. Expected result

Rooms flow cleanly through the cycle *Occupied → (checkout) Vacant Dirty → Vacant Clean → Vacant Inspected → sellable*, with maintenance rooms held safely out of inventory via OOO/OOS, and the front desk only ever able to check into inspected, ready rooms.

## 11. Error scenarios

| Scenario | System response |
|---|---|
| Save OOO with `FromDate ≥ ToDate` | `OutOfOrderTXN_M_Insert` raises *"Invalid date range."* / *"The From and To dates cannot be the same."* |
| OOO on a reserved/in-house room | Raises *"Room already allocated to …"* and rolls back. |
| OOO overlapping an existing block | Raises *"<Room> - Room already has been out of order."* |
| Check-in on a non-inspected room | Blocked by `IsAllowCheckIn = 0` (front-office allocation logic). |
| Room-boy/supervisor save failure | Controller returns `"ERR-<message>"` / `"Err<message>"` JSON. |
| Any SP failure | Wrapped in TRY/CATCH, logged to `GEN_ErrTable`, re-raised. |

## 12. Related documents

- `00-project-overview.md` — system-wide overview, areas and permissions.
- Reservation / check-in and availability documents (front-office allocation consuming room status).

---

### ASCII room-status transition diagram

```
                         ┌─────────────────────────────────────────────────────┐
                         │                    ROOM LIFECYCLE                    │
                         └─────────────────────────────────────────────────────┘

   CHECK-IN (process CKI)                                     CHECK-OUT (process CKO / DEAUT)
        │                                                              │
        ▼                                                              ▼
  ┌───────────────┐   guest stays,        ┌───────────────┐    ┌───────────────┐
  │  OCCUPIED     │   room serviced       │  OCCUPIED     │    │ VACANT DIRTY  │◄── checkout leaves
  │  DIRTY (6)    │──────────────────────►│  CLEAN (2030) │    │   (2034)      │    room dirty
  └───────┬───────┘                       └───────┬───────┘    └───────┬───────┘
          │ inspect                               │ inspect            │ room boy cleans
          ▼                                        ▼                    ▼
  ┌───────────────┐                       ┌───────────────┐    ┌───────────────┐
  │  OCCUPIED     │                       │  OCCUPIED     │    │ VACANT CLEAN  │
  │  INSPECTED    │                       │  READY (2031) │    │   (2033)      │
  │  (1030)       │                       └───────────────┘    └───────┬───────┘
  └───────────────┘                                                    │ supervisor inspects
        (guest still in-house — FO = Occupied 2050)                    ▼
                                                             ┌───────────────────────┐
                                                             │  VACANT INSPECTED (22) │
                                                             │  IsAllowCheckIn = 1    │──► SELLABLE /
                                                             │  (FO = Vacant 2061)    │    ready for
                                                             └───────────┬────────────┘    next check-in
                                                                         │
                                                                         └────► back to CHECK-IN

   ── OUT-OF-ORDER BRANCH (any status) ─────────────────────────────────────────────────────
        │  OutOfOrderTXN save (process OOO / OOS)                validates: no reservation,
        ▼                                                        no overlap; FromDate<ToDate
  ┌────────────────────────────┐        ToDate reached /        ┌────────────────────────────┐
  │ OUT OF ORDER (2044)  or     │  ReleaseAs / QuickDelete       │ returns to ReleaseAsId HK   │
  │ OUT OF SERVICE (2045)       │──────────────────────────────►│ status (e.g. Vacant Dirty)  │
  │ FO = Out of Order/Svc 2067  │                                └────────────────────────────┘
  │ removed from availability   │
  └────────────────────────────┘
```
