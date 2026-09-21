# Reservation Process

> **Module:** `Reservation` area (`WebUIMvc/Areas/Reservation`)
> **Scope:** How a booking is created, priced, confirmed, modified, cancelled, and handed over to the Front Office for check-in in Scienter HotelERP / Destinity Inspire Front Office.
> All controller/action, service, stored‑procedure (SP), table and screen names below were verified against the source tree and the live `HotelResWeb_Browns` database. Where something could not be confirmed it is marked **"Not found in the project"**.

---

## Purpose

A **reservation** records a guest's intent to stay: who is coming, when they arrive and depart, which room category/type and rate they booked, the meal plan, any deposit taken, and the booking's status (Confirmed, Tentative, etc.). It is the master record that the rest of the property management system builds on — availability, rates, housekeeping, folio/billing and night audit all key off it.

This document covers the complete reservation life‑cycle:

- Creating an individual reservation.
- Group / block / allotment reservations.
- Room type & room selection and availability logic.
- Rate codes, meal plans, promotions/discounts/packages.
- Deposits / advance payments (in‑house and online payment link).
- Confirmation and reservation‑number generation.
- Modification, cancellation, and No‑show handling.
- Booking source & channel‑manager (OTA / Staah / Bookingwhizz) integration.
- Reservation status values and the hand‑off from **reservation → check‑in**.

---

## Relevant users / departments

| User / department | Involvement |
|---|---|
| Reservations agent | Creates, prices, confirms, modifies and cancels bookings. |
| Front Office / Reception | Room allocation, quick check‑in, key requests, hand‑off from reservation to stay. |
| Reservations manager / Revenue | Rate codes, promotions, allotments, availability & occupancy forecasts, inquiry stats. |
| Sales / Group coordinator | Group reservations, allotments (travel‑agent room blocks), block dates. |
| Cashier | Advance / deposit posting, advance refund. |
| Channel/OTA coordinator | Receives and re‑pushes OTA bookings via the channel manager. |
| Housekeeping | Reservation traces/tasks, queue rooms for arrivals. |

Access to each action is enforced by the `[UserWisePageAccess(<pageId>, "<permission>")]` attribute on the controller action (e.g. `6176` = Make Reservation, `5509` = Cancel Reservation, `2017` = Quick Check‑In, `5500` = Room Allocation, `2018/2019` = Availability, `6171` = Allotment).

---

## Preconditions

Before a reservation can be created, the following master data must exist and be active:

1. **Rooms & categories** — `RoomDetails`, `RoomCategories`, `RoomTypes` (rooms flagged `IsActive = 1` and `ConciderForOccupancy = 1` count toward availability).
2. **Rate codes & room rates** — `RateCodeHeaders`, `RoomRates` (a rate must exist for the chosen Room Category + Room Type + Meal Plan + date range, otherwise the reservation is rejected — see error `104`).
3. **Meal plans** — `MealPlans`, `Meals`.
4. **Booking settings** — one `BookingSettings` row per property defines the default statuses used by the workflow:
   - `BookingConfirmStatusId = 3` (Confirmed)
   - `BookingTentitiveStatusId = 4` (Tentative)
   - `BookingCancelStatusId = 1` (Cancelled)
   - `NoShowStatusId = 2` (No‑Show)
   - plus default tentative rate code (`DefaultRatecodeIdForTentative`), accommodation charge/tax codes, advance‑payment charge code, etc.
5. **Document number series** — a `DocumentNumbers` row per property with `Code = 'RESNO'` (reservation number) and `Code = 'GRRESNO'` (group reservation number).
6. A **logged‑in user** with the relevant page access; the reservation is always scoped to `SessionObjects.LoggedUser.PropertyId` (multi‑tenant).
7. A **guest profile** — either selected from existing profiles or created inline during reservation.

---

## Step-by-step process

### A. Creating a new individual reservation (6‑step format)

The primary screen is **Make Reservation** (`ReservationsController.MakeReservation` → `Areas/Reservation/Views/Reservations/MakeReservation.cshtml`, page id `6176`). The availability grid and save are served by **`ReservationCreationController`**.

| # | Stage | What happens (technical detail) |
|---|---|---|
| **1** | **User action** | Agent opens *Make Reservation*, enters arrival/departure dates and guest country, and requests availability. Front end calls **`POST ReservationCreation/GetAvailability(fromDate, toDate, CountryId, reservatonStatusId, reservationForId)`**. |
| **2** | **System validation / availability** | The action calls **`RoomAvailabilityService.SelectRoomAvailability(...)`** → `RoomAvailabilityEntry` → SP **`RoomAvailability_R_Select_ForManageReservationList`**. Room types are loaded via `RoomTypeService.SelectForAvailability`. Availability itself is computed by counting active, occupancy‑bearing rooms per category minus existing reservations per night (see *Availability logic* below). The chosen country is remembered in `SessionObjects.SelectdCountryId` (used later to pick local vs. foreign rate). |
| **3** | **Guest selection / creation** | Agent picks an existing guest (`ReservationCreation/ExistingGuestProfile`, `POST SearchGuest`) or creates one inline via **`SaveGuest`** → **`ReservationHeaderService.SaveGuestProfileOnReservationCreation`** → SP **`GuestProfiles_M_Save_OnReservationCreation`**. NIC/passport is auto‑classified: a value containing `v` is stored as local `IdNum`, otherwise as `PassportNo`. |
| **4** | **Database change (save)** | Agent picks rooms/rate/meal plan and submits. Front end posts a `ReservationWrapper` (guest, stay, rooms, other details) to **`POST ReservationCreation/SaveReservationNew(quickReservation, IsApproveAsTentative, IsApproveVoucherNumberDuplication, IsCustomRate)`**. The controller sets `BookingMethod = "HTL"` (hotel/manual), stamps `UserId`, a fresh `Uuid` (GUID, dashes stripped), `BookingStatusId = SelectedOtherDetails.StatusId`, and `PropertyId`, then calls **`ReservationHeaderService.SaveReservationNew`** → `ReservationHeaderEntry` → SP **`Reservation_T_Save_New`** (wrapper passed as XML). The SP: generates the reservation number, inserts the header/detail/profile rows, room rates and (optionally) applied promotions, all inside `BEGIN TRY`. |
| **5** | **Related module updates & integration** | Inside `Reservation_T_Save_New`: the **reservation number** is generated by `EXEC UpdateNextDocNoWithUpdate 'RESNO', @PropertyId, @ReservationNo OUTPUT` and the **group number** by `'GRRESNO'`; **category overbooking is re‑checked** and the save is blocked if any category is oversold; audit is written via `HotelResWeb_AuditTail_WriteToLog`. If the reservation status is **Confirmed**, room‑rate rows are written; if approved as tentative the status/rate switch to the tentative defaults from `BookingSettings`. |
| **6** | **Final result** | On success the JSON of the saved `ReservationWrapper` (now carrying `Uuid` and generated numbers) is returned; the UI shows the reservation. A confirmed booking becomes visible in the reservation list, availability charts and forecasts. Errors surface as coded messages (`104`, `105`, `ERR - …`). |

**Reservation‑number format (verified with live data):** per‑property alphanumeric prefix + 10‑char zero‑padded running number. Example real values in `HotelResWeb_Browns`: reservation `OEB0049910`, group `GOEB005009` (group numbers are prefixed with the property `Prefix` = `G…`). Configured in `DocumentNumbers (Code, Prefix, Length, NextNo)`; the generator is SP `UpdateNextDocNoWithUpdate`.

> **Note on `ReservationNOs_T_Select`:** despite the name, this SP is a **search/lookup** that lists in‑house reservations by number/room (used by pickers), **not** the number generator. Number generation is done by `UpdateNextDocNoWithUpdate` inside the save SP.

---

### B. Group reservation / block / allotment

Three related mechanisms exist:

**1. Group reservations** — Multiple room reservations share a **`GroupReservationNo`** (e.g. `GOEB005009`). Individual reservations can be joined/split after creation:

| Action (controller) | Service method | SP |
|---|---|---|
| `Reservations/AttachToGroup` (page `5542`) → list candidates | `ReservationHeaderService.SelectReservationListForAttachToGroup` | `ReservationList_T_SelectForAttachToGroup` |
| `Reservations/AttachToGroupSave` | `ReservationHeaderService.AttachToGroupSave` | `Reservation_T_AttachToGroupSave` |
| `Reservations/Detach` / `DetachSave` (page `5543`) | `ReservationHeaderService.DetachSave` | `Reservation_T_Multiple_DetachSave` |

**2. Block dates** — `ReservationBlockDatesController` (Landing / Form / Save / `BlockDatesAvailability`) blocks room inventory for a date range: SPs `ReservationBlockDates_M_Save` and `ReservationBlockDatesAvailability_W_Select` (via `ReservationHeaderEntry`).

**3. Allotments** — a pre‑negotiated block of rooms held for a travel agent/market for a period, managed by **`AllotmentsService`** → `AllotmentEntry`:

| Purpose | Method | SP |
|---|---|---|
| Create allotment (rooms/days/date‑ranges as JSON) | `AllotmentsService.Save` | `Allotment_M_Save` |
| Check allotment availability | `AllotmentsService.CheckAvailability` | `Allotment_T_Select_Availability` |
| Create reservation from an allotment | `AllotmentsService.SaveReservation` | `Reservation_T_Save_New` |
| Edit remaining room balance | `EditAllotmentRoomBalance` | `AllotmentDetails_M_EditRoomBalance` |

An allotment header (`AllotmentHeaders`) carries `AgentId`, `MarketId`, `Name`, `FromDate/ToDate`, `ReservationStatusId`, `AllotmentType` and `ReleasePeriodDays` (auto‑release window). Attaching/removing an allotment to a reservation:

| Action (`ReservationListController`) | Service method | SP |
|---|---|---|
| `AvalableAllotments` / `AttachAllotment` (page `6171`) | `ReservationHeaderService.SelectAvailableAllotments` / `ApplyAllotment` | `Reservation_T_AvailableAllotments` / `Reservation_T_ApplyAllotments` |
| `RemoveAllotment` | `ReservationHeaderService.RemoveAllotment` | `Reservation_T_RemoveAllotments` |

Cancelling a reservation that is attached to an allotment automatically returns its rooms via `Reservation_T_RemoveAllotments` (see *Cancellation* below).

---

### C. Room type & room selection; availability checking logic

- **Room selection at reservation time** is by **room category + room type + meal plan** (a physical room number is usually assigned later at *Room Allocation*).
- **Physical room allocation** happens through `ReservationListController` (page `5500`):
  - `RoomAllocation` / `RoomListForAllocation` — pick a room; view `_RoomAllocationMainOutter`.
  - `SaveReservationWiseRoomsAndAttributes` → `ReservationHeaderService.InsertReservationWiseRoomsAndAttributes` → SP **`ReservationHeaders_T_Save_ReservationHeaderWiseRooms`** (attributes serialized as JSON, Insert/Update operation flag).
  - `SaveQuickRoomAllocation` — one‑click assign/unassign of a single room.

**Availability computation (core logic)** — SP **`RoomAvailability_R_Select @From, @To, @PropertyId`** (wrapped by `RoomAvailability_W_Select` for the booking engine). Verified algorithm:

```
For each night in [From, To):
    total_available(category) = COUNT(RoomDetails
                                       WHERE PropertyId = @PropertyId
                                         AND ConciderForOccupancy = 1
                                         AND IsActive = 1)          -- grouped by RoomCategoryId
    available(category, night) = total_available(category)
                                 − reservations already booked that night
    (optionally include Out-of-order / Blocked Rooms "OBR"
     when SystemSettings code 'SS011' IsEnable = 1)
```

Availability screens:

| Screen | Controller / action | Service → SP |
|---|---|---|
| Room availability grid | `RoomAvailabilityController.Landing / DateWiseRoomAvailabilities` (page `2018`) | `RoomAvailabilityService.Select` → `Room_Availability_M_Select` |
| Availability chart | `AvailabilityChartController.AvailabilityList / AvailabilityListDetails` (page `2019`) | `RoomAvailabilityService.Select_ForChart` → `AvailabilityChart_M_Select`; details → `AvailabilityChartDetail_M_Select` |
| Reservation chart (Gantt) | `ReservationChartController` | `Reservations_M_SelectForReservationChart_ByDateRange`, `RoomDetails_M_SelectForReservationChart`, `CheckRoomAvailability_ForReservationChart` |
| Occupancy forecast | `RoomAvailabilityService` today/forecast methods | `RoomAvailability_Today_Occupancy`, `RoomAvailability_Occupancy_Forecast_HighLevel`, `RoomAvailability_Today_ExpectedArrivals`, `Today_ExpectedDeparture` |

Overbooking guard: `Reservation_T_Save_New` runs a final category‑wise availability check and raises `Sorry, there is an issue in placing the reservation. Category(s) overbooking. (Category Available X, Requested Y)` if any category would be oversold.

---

### D. Rate plan / rate code, meal plan, offers & discounts / promotions / packages

**Rate codes** — `RateCodeHeaderService` → `RateCodeHeaderEntry`:

| Feature | Method | SP |
|---|---|---|
| Save rate code | `Insert` / `Update` | `RateCodeHeaders_M_Save` |
| Rate rules (min/max stay, occupancy, rooms, book‑before days) | `RateRulesSave` | `RateCodeHeaders_M_RateRulesSave` |
| Company‑specific rates | `InsertCompanyWiseRates` | `CompanyWiseRates_T_Save` |
| Copy rates between rate codes | `InsertRateCodeCopy` | `RoomRates_T_RateCodeCopySave` |
| Free‑night offer | `FreeNigthOfferSave` | `RateCodeWiseFreeNights_M_Save` |
| Rates by country (local vs foreign) | `SelectByCounrtyId` | `RateCodeHeaders_T_SelectByContryId` |

Local vs. foreign pricing is driven by the guest country vs. `BookingSettings.LocalCountryId` (`ForeignRateCodeId` / `LocalRateCodeId`). A rate code can be flagged **`IsPromotionApplicable`**, which the save SP uses to auto‑apply eligible promotions.

**Meal plans** — `MealPlanService` → `MealPlanEntry` (`MealPlans_M_Save`, `MealPlans_M_SelectForAvailability`, `Meals_M_SelectForMealAllocation_ByMealPlanId`). Each reservation room stores a `MealPlanId`.

**Promotions / discounts / packages:**

| Feature | Controller action | Service → SP |
|---|---|---|
| Preview applicable promotions | `ReservationList/ApplicablePromotionsPreview` | `ReservationHeaderService.ApplyPromotionsOrDiscounts` (isSave=0) → returns `List<ApplicablePromotionAndDiscount>` |
| Apply promotions/discounts | `ReservationList/ApplyPromotionsOrDiscounts` | `ReservationWiseAppliedPromotions_Save` |
| Read applied promotions | `SelectAppliedPromotionsAndDiscounts` | `ReservationWiseAppliedPromotions_Select` |
| Discount authorisation | — | `Discount_SelectAuthorizedUsersToApproveDiscounts`, `Discount_SelectApplicablePromotions` |
| Packages | package master + reservation `PackageHeaderId` | `PackageHeaders_M_Save`, `PackageDetails_M_Save`; default via `BookingSettings.DefaultPackageId` |

The save SP `Reservation_T_Save_New` reads applied promotions (including promo free‑nights) and stores `ApplicablePromotions` / `PromoCode` on the reservation.

---

### E. Deposits / advance payment

There are **two** deposit paths.

**1. In‑house (cashier‑posted) advance** — `AdvancePaymentService` → `AdvancePaymentEntry`:

| Purpose | Method | SP |
|---|---|---|
| Post advance to folio | `Save` | `Advance_Payment_T_Save` |
| Cancel/reverse advance | `SaveCancelAdvance` | `Advance_Payment_Cancellation_T_Save` |
| Advance charge config | `GetAdvancePaymentCharges` | `AdvancedPyment_Charges_T_Select` |
| Advance refund popup | `Reservations/AdvancePaymentRefundPopup` | view `_AdvancePaymentRefundPopup` |

The advance is posted as a folio credit (`DRCR = 'C'`) using `BookingSettings.ChargeCodeAdvancedPayments` / `AdvancedPayment_ChargeCodeId`.

**2. Online advance request / payment link** — guest pays via the Sampath Internet Payment Gateway (IPG):

| Step | Controller / action | Service → SP |
|---|---|---|
| Create request | `ReservationList/RequestOnlineAdvance` → `SaveRequestOnlineAdvance` | `ReservationHeaderService.SaveRequestOnlineAdvance` + `SaveAdvanceRequestOnlineEmail` → `AdvanceRequestOnline_T_SendEmail`; template in `AdvanceRequestOnline` table (Uuid, DocumentNo, amounts, `PaymentMode`) |
| Guest opens payment page | `Advance/Payment(id=Uuid)` | `ReservationHeaderService.AdvanceRequestSelectByUuid` → delegates to `SampathIPGController.PaymentRequest` |
| Gateway callback | `Advance/Response(reqid)` | parses gateway response (statusCode, card details) → `ReservationHeaderService.AdvanceResponseSave`; `00`/`0` = success → generates invoice + redirect to Receipt, otherwise `Advance/PaymentError` |
| Receipt / e‑mail | `Advance/Receipt(id=Uuid)` | `AdvanceRequestSelectByUuid`; async `EmailSender.SendEmail` confirmation |

Alternative link mechanism (`AdvancePaymentEntry`): `SaveAdvancePaymentLink` → `OnlineAdvancePayment_Insert`, retrieved by `OnlineAdvancePayment_SelectBy_Uuid`, response saved by `OnlineAdvancePaymentLink_Payment_Update`. Supporting tables: `AdvanceRequestOnline`, `AdvanceRequestOnlineEmails`, `AdvanceRequestOnlinePayment(Response)`, `AdvancePaymentLinks`, `AdvanceRequestHeaders/Details`.

---

### F. Reservation confirmation (status flow & number generation)

**Status flow** — the booking's `StatusId` on `ReservationHeaders` drives the workflow. Verified values from the live `ReservationStatus` table (only these six exist):

| Id | Name | AllocationRequired | ApplicableToOccupancy | AllowInMakeReservation | AllowedToCheckIn | IsTentative | IsNoshow |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 3 | **Confirmed** | ✔ | ✔ | ✔ | ✔ | | |
| 4 | **Tentative** | | | ✔ | | ✔ | |
| 6 | **Waitlisted** | | | ✔ | | | |
| 5 | **Inquiry** | | | ✔ | | | |
| 1 | **Cancelled** | | | | | | |
| 2 | **No-Show** | | | | | | ✔ |

Key rules derived from the columns and `BookingSettings`:
- **Confirmed (3)** is the only status that both counts toward occupancy and is allowed to check in; room rates are written on save.
- **Tentative (4)** — if a reservation is approved as tentative (`IsApproveAsTentative = 1`), `Reservation_T_Save_New` switches the status to `BookingSettings.BookingTentitiveStatusId` and the rate to the tentative default rate code.
- **Cancelled (1)** / **No‑Show (2)** are terminal and do not count toward occupancy or make‑reservation.

Status master maintained by `ReservationStatusController` / `ReservationStatusService` → SP `ReservationStatus_M_Save` / `ReservationStatus_M_Select`.

**Confirmation number & confirmation output:**
- Numbers: `UpdateNextDocNoWithUpdate 'RESNO'` (reservation) and `'GRRESNO'` (group), zero‑padded to `DocumentNumbers.Length` with the per‑property prefix.
- Confirmation document/e‑mail: `ReservationHeaderService.HotelBookingConfirmation` → `Reservation_T_Confirmation_Hotel`; `SendEmailConfirmation` → `Reservation_T_SelectConfirmation_EmailTemplate`; sent from `ReservationList/SendEmails` (page `13045`) via `SaveReservationEmail` (`ReservationEmails_T_SelectToMail`, status updated by `ReservationEmails_M_SentStatusUpdate`).

---

### G. Reservation modification

| Action | Controller | Service → SP |
|---|---|---|
| Single‑page edit | `ReservationList/SinglePageReservationEdit` → `ReservationUpdateNew` | `ReservationHeaderService.ReservationUpdateNew` → `Reservation_T_Update_New` |
| Header update | — | `ReservationHeaderService.Update` → `ReservationHeaders_M_Save` |
| Change stay (extend/shorten) | — | `Reservation_T_ChangeStaySave` |
| Manage room rate | `ManageRoomRate` → `ReservationRoomRateUpdate` | `Reservation_T_RoomRateDetails_Select` / `Reservation_T_RoomRate_Update` |
| Reservation type change (Complimentary / House Use) | `ReservationTypeChange` (page `5522`) → `SaveReservationTypeChange` | `ReservationTypeService.Select` (`ReservationTypes_M_Select`); reasons `ComplimentaryReasons_M_Select_TypeWise`; save via `ReservationHeaderService.ReservationTypeChangeSave` |
| Add rooms / guests | `AddMoreRooms`/`AddNewRoom`, `ManageGuests`/`AddNewGuest`/`RemoveGuest` | `Reservation_T_AddNewRoom`, `Reservation_T_AddNewGuest`, `Reservation_T_RemoveGuest` |
| Stop posting | `Reservations/OpenStopPosting` → `StopPosting` (page `5537`) | `Reservation_T_StopPosting` |

Verified `ReservationTypes` values (live): `1 Complimentary`, `2 House Use`, `4 Driver Quarters`.

---

### H. Reservation cancellation

Screen: `CancelReservationController` (page `5509`).

| # | Stage | Detail |
|---|---|---|
| 1 | User action | Agent opens `CancelReservationByHeaderId` (single) or `CancelReservationByGroupResNo` (whole group), selects a **cancellation reason** and enters a remark. |
| 2 | Submit | `POST CancelReservation/Save(selectedReservation)` → **`CancelReservationService.Save`** (list serialized to JSON) → `CancelReservationEntry.Save` → SP **`CancelReservation_M_Save`** (`@UserId`, `@PropertyId`). |
| 3 | DB change | Per reservation the SP: sets `StatusId = BookingSettings.BookingCancelStatusId` (**Cancelled = 1**); writes `CancelledReservationLog (ReservationHeaderId, CansellationReasonId, Remark, CreatedUserId, PropertyId)`; deletes `ReservationWiseInventoryAllocation`; writes audit via `HotelResWeb_AuditTail_WriteToLog`. |
| 4 | Related modules | If attached to an allotment, rooms are returned via `Reservation_T_RemoveAllotments`; revenue/occupancy summary re‑executed (`Dayend_RevenueAndOccupancySummary_Executions_M_Save`); filtration columns refreshed (`ReservationListFilterationColumns_Insert`). |
| 5 | Integration | A **channel‑manager date range** row is inserted into `CMUpdateRanges (arrival, departure, proccessID='A', updated=0, …)` so freed inventory is pushed back to OTAs. For OTA‑originated bookings there is also `CancelReservationEntry.CancelReservation` → SP `RateTiger_Reservation_API_Cancel`. |
| 6 | Result | Returns `Json("OK")`; the booking disappears from active lists and frees inventory. |

**Cancellation reasons** (live `CancellationReasons`): `1 Flight Cancellation`, `4 Mistake`, `5 Overbooking Situation`, `6 Guest Cancellation`, `7 Other`, `8 OTA Booking Cancellation`, `9 Travel Agent Cancellation`.

**Cancellation policy / charges:** the `CancellationPolicies` table holds **textual policies/terms** (Name, Description, IBE‑display flags) shown on confirmations/IBE — it is **not** a monetary penalty calculator. `CancellationPolicyService` (`CancellationPolicies_M_Save`, `…_Select_ForIBE`) maintains these texts. A parameter‑driven automatic cancellation‑**charge/penalty** amount was **Not found in the project** (searched `CancellationPolicies` schema, `CancelReservation_M_Save`, and cancellation SPs — the save SP stores reason + remark, no penalty computation). Any cancellation charge would be posted manually as a folio charge.

### No‑show process

- No‑Show is status **`2`** (`ReservationStatus.IsNoshow = 1`), configured as `BookingSettings.NoShowStatusId = 2`.
- No‑Show marks a guaranteed reservation whose guest never arrived; like Cancelled it is excluded from occupancy and make‑reservation.
- A dedicated single "mark as no‑show" controller action was **Not found in the project** as a distinct endpoint; No‑Show is applied through the standard status/booking‑settings mechanism (`NoShowStatusId`) and is typically actioned during day‑end/night audit. (Searched Reservation‑area controller actions and `BookingSettings`.)

---

### I. Booking source / channel & channel‑manager integration

**Booking source** is stored on `ReservationHeaders.BookingSourceId` (master `BookingSources`, service `BookingSourceService`). Verified live sources: `1 Email`, `2 Face Book`, `3 Airport Counter`, `4 OTA`, `5 DIRECT CALL`, `6 Walk-in`, `7 TOUR OPERATER`, `8 TRAVEL AGENT`, `9 CO OPERATE COMPANY`, `10 WhatsApp`. `BookingMethod` records the origin channel (`"HTL"` = manual/hotel, `IBE` = internet booking engine, API, etc.).

**Channel manager / OTA (`OTABookingController`)** — the property connects to OTAs through a channel manager (**Staah**, with `Bookingwhizz` and generic `CM*`/RateTiger tables also present). High‑level input/output:

| Direction | Action | Service → SP |
|---|---|---|
| **Inbound** (OTA → PMS) list received bookings | `OTABooking/ReceivedOTABookings` | `ReservationHeaderService.ReceivedOTABookings` → `Staah_ReservationRequests_Select_ReceivedReservations` |
| Inbound: view one booking (raw XML) | `OTABooking/BookingDetailByUuid(uUid)` | `Staah_Select_ReservationRequestDetails_ByXml` |
| **Sync**: bookings pending push into PMS | `OTABooking/PendingOTABookings` | `Staah_PendingReservationsToSync` |
| **Re‑push** a failed booking | `OTABooking/RePushOTABooking(uuid)` | `Staah_ReservationRequestRePush` |
| **Outbound** (PMS → OTA) inventory/availability sync | inserted on create/cancel/update | `CMUpdateRanges` (date ranges to push); `Staah_AvailabilityPush` |

Supporting inbound/outbound tables: `Staah_ReservationRequests`, `CMReservation`, `CMReservationRequest`, `CMReservationRooms`, `CMReservationUpdate(Request)`, `CMReservationCancellationRequest`, `CMUpdateRanges`, `Staah_CMRateCodes`, `STAAH_Mapping_RoomCategories`, `STAAH_Mapping_MealPlans`, `BookingWhizz_M_Reservations_ToSync`. Room‑category and meal‑plan **mapping** tables translate OTA codes to PMS ids. OTA cancellations use `RateTiger_Reservation_API_Cancel`.

---

### J. Flow from reservation → check‑in (hand‑off to Front Office)

Confirmed reservations (status `3`, `IsAllowedToCheckIn = 1`) are handed to Front Office at arrival. The fastest path is **Quick Check‑In** (`QuickCheckInsController`, page `2017`):

| # | Stage | Detail |
|---|---|---|
| 1 | Select arrivals | `QuickCheckIns/SelectForGrid` → `ReservationHeaderService.ReservationQuickCheckInListSelect` → `Reservation_T_QuickCheckin_Select`. |
| 2 | Submit | `POST QuickCheckIns/QuickCheckIn(qCheckIns, CheckInRemark)` → **`ReservationHeaderService.QuickCheckIn`** → `ReservationHeaderEntry` → SP **`Reservation_T_QuickCheckInUpdate`** (`@qCheckIns` JSON, `@CheckInRemark`, `@UserId`, `@PropertyId`). |
| 3 | Validation (in SP) | Requires a room to be allocated and available (`InhouseReservationHeaders_Active_Rooms`), the room's housekeeping status to permit check‑in, and the reservation status `IsAllowedToCheckIn = 1`; otherwise `RAISERROR`. |
| 4 | DB change (hand‑off) | The reservation is **copied from `ReservationHeaders` into the in‑house tables**: `INSERT INTO InhouseReservationHeaders` (setting `CheckedInDate = GETDATE()`, `CheckInRemark`, `CheckedInUserId`), plus `InHouseReservationDetails` and `InHouseReservationProfiles`. From this point the stay is "in house" and drives folio/billing, housekeeping and night audit. |
| 5 | Result | `Json("success")`; the guest now appears on the in‑house/arrivals list. Full check‑in (GRC, documents, keys via `Reservations/KeyRequest` → `DoorLockEvent_T_InsertOrDeleteKeyCode`) is completed from the Front Office screens. |

```
 Reservation life-cycle
 ┌────────────┐  approve tentative   ┌───────────┐
 │ Tentative  │ ───────────────────► │ Confirmed │
 │   (4)      │                      │   (3)     │
 └────────────┘                      └─────┬─────┘
   Inquiry(5) / Waitlisted(6)  ──────►     │ allocate room
                                           ▼
                                    ┌──────────────┐  QuickCheckIn / Reservation_T_QuickCheckInUpdate
                                    │ Room Alloc.  │ ───────────────────────────────────────────────►
                                    └──────────────┘        copies to InhouseReservationHeaders
                                           │
                     cancel ◄──────────────┼──────────────► No-Show (2)  (night audit)
                     Cancelled (1)
                     + CMUpdateRanges push
```

---

## Screens / modules involved

| Screen / view | Controller.Action | Purpose |
|---|---|---|
| `MakeReservation.cshtml` | `Reservations.MakeReservation` | Create reservation (page `6176`) |
| `_RoomAvailability.cshtml` | `ReservationCreation.GetAvailability` | Availability grid at booking |
| `_GuestCreateSearchForm` / `_ExistingGuestProfile` | `ReservationCreation.GetGuestDetails/SearchGuest` | Guest search/create |
| `_RoomAllocationMainOutter` | `ReservationList.RoomAllocation` | Assign physical rooms |
| `_ManageRoomRate` | `ReservationList.ManageRoomRate` | Adjust room rate |
| `RequestOnlineAdvance` / `Advance` views | `ReservationList.RequestOnlineAdvance`, `AdvanceController` | Deposits |
| `_AttachAllotment` / `_ReservationTypeChange` | `ReservationList` | Allotments, comp/house‑use |
| Cancel views (`_Landing`, `_SelectGroupReservationForCancellation`) | `CancelReservationController` | Cancellation |
| `AvailabilityChart` / `ReservationChart` / `RoomAvailability` | respective controllers | Availability & charts |
| `_Grid` (Quick Check‑In) | `QuickCheckIns` | Reservation → check‑in |
| OTA `Index` / `BookingDetails` | `OTABooking` | Channel manager |

## Database / API involvement

**Core tables:** `ReservationHeaders`, `ReservationDetails`, reservation profile/rate tables, `RoomDetails/RoomCategories/RoomTypes`, `RoomRates`, `RateCodeHeaders`, `MealPlans/Meals`, `AllotmentHeaders/AllotmentDetails`, `BookingSettings`, `BookingSources`, `ReservationStatus`, `ReservationTypes`, `CancellationReasons`, `CancelledReservationLog`, `CancellationPolicies`, `DocumentNumbers`, advance tables (`AdvanceRequestOnline`, `AdvancePaymentLinks`, `AdvanceRequestHeaders/Details`), channel‑manager tables (`Staah_*`, `CMReservation*`, `CMUpdateRanges`, `BookingWhizz_*`), and the in‑house hand‑off tables (`InhouseReservationHeaders`, `InHouseReservationDetails`, `InHouseReservationProfiles`).

**Key SPs:** `Reservation_T_Save_New` (create), `Reservation_T_Update_New` (modify), `CancelReservation_M_Save` (cancel), `Reservation_T_QuickCheckInUpdate` (check‑in), `RoomAvailability_R_Select` / `RoomAvailability_W_Select` (availability), `UpdateNextDocNoWithUpdate` (numbering), `Reservation_T_ApplyAllotments`/`RemoveAllotments`, `ReservationWiseAppliedPromotions_Save`, `Advance_Payment_T_Save`, `Reservation_T_Confirmation_Hotel`.

**APIs / integrations:** Sampath IPG (online advance), Staah/Bookingwhizz/RateTiger channel manager, e‑mail confirmations (`EmailSender`).

## Business rules

1. A reservation is always scoped to the logged‑in user's `PropertyId` (multi‑tenant).
2. A room rate must exist for the chosen Category + Type + Meal Plan + dates, or the save is rejected (error `104`) — unless the user approves it as **tentative**.
3. Approving as tentative switches status and rate code to the property's tentative defaults (`BookingSettings`).
4. Category overbooking is blocked at save time; blocked/out‑of‑order rooms count only when `SystemSettings SS011` is enabled.
5. Only **Confirmed** reservations count toward occupancy and may be checked in; only Confirmed writes room‑rate rows.
6. Reservation and group numbers are property‑prefixed, zero‑padded, and issued atomically via `UpdateNextDocNoWithUpdate`.
7. Voucher numbers are checked for duplication unless the user approves the duplicate (`IsApproveVoucherNumberDuplication`).
8. Cancelling/No‑showing frees inventory and pushes a channel‑manager update (`CMUpdateRanges`); allotment rooms are returned automatically.
9. Check‑in physically migrates the record from `ReservationHeaders` to the `Inhouse*` tables.

## Expected result

A saved reservation with a unique reservation number (and group number if grouped), correct status, priced rooms/meal plan, optional advance and applied promotions, visible in reservation lists, availability charts and forecasts, and — once confirmed and allocated — ready for quick check‑in into the in‑house tables.

## Error scenarios

| Trigger | System behaviour |
|---|---|
| No room rate for selection | SP raises `104-No Room Rates for the selected Meal Plan, Room Type & Room Category…` → offered to place as tentative. |
| Category oversold at save | SP raises `Category(s) overbooking (Available X, Requested Y)`; save aborted. |
| Duplicate voucher number | Blocked unless `IsApproveVoucherNumberDuplication = 1`. |
| Missing sales person (when required) | SP raises `Please select a sales person..`. |
| Check‑in without allocated/clean room or status not check‑in‑able | `Reservation_T_QuickCheckInUpdate` raises an error; check‑in refused. |
| Online advance gateway failure | `Advance/Response` returns non‑`00` status → redirect to `Advance/PaymentError`. |
| Generic save error | Controller returns `ERR - <message>` / `Error -<message>`; SQL errors starting `104`/`105` are surfaced verbatim. |

## Related documents

- `00-project-overview.md` — system architecture and module map.
- *(Planned)* check‑in, folio/billing, housekeeping, rate/meal‑plan configuration, and channel‑manager documents — cross‑reference when authored.

---

### "Not found in the project" items

- **Automatic monetary cancellation charge/penalty calculation** — `CancellationPolicies` stores textual terms only; `CancelReservation_M_Save` records reason + remark with no penalty computation. (Searched the table schema and cancellation SPs.)
- **A dedicated "mark as No‑show" controller action** — No‑Show is applied via `BookingSettings.NoShowStatusId` / status master, not a distinct Reservation‑area endpoint. (Searched `ctrl_actions.json` Reservation area and controllers.)
