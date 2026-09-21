# Appendix B — Complete Stored Procedure Catalog

> **Every one of the 2890 stored procedures** in `HotelResWeb_Browns`, grouped by module, then by name prefix. Type tag: **M**=Master/config · **T**=Transaction · **R**=Report/read · **W**=Wide report · (blank)=other. **backup/variant** marks `_OLD`/`_Dev`/`_OPT`/`_NEW`/`test`/dated twins — not the canonical procedure.

> Source of truth: `sys.procedures`. See [README](README.md) and [12-database-and-technical-architecture](12-database-and-technical-architecture.md) for the naming convention.

## Module summary

| Module | Stored procedures | Detail doc |
|---|---:|---|
| Reservations | 327 | [03-reservation-process.md](03-reservation-process.md) |
| Front Office — In-house & Check-in/out | 39 | [04-check-in-check-out-process.md](04-check-in-check-out-process.md) |
| Front Office — Guest Profiles | 67 | [02-front-office-process.md](02-front-office-process.md) |
| Rooms & Housekeeping | 229 | [06-rooms-and-housekeeping-process.md](06-rooms-and-housekeeping-process.md) |
| Cashiering, Folio & Day-End | 345 | [05-cashiering-and-finance-process.md](05-cashiering-and-finance-process.md) |
| F&B / Profit Centres | 81 | [07-fnb-and-outlet-process.md](07-fnb-and-outlet-process.md) |
| Spa & Meal Reservations | 34 | [01-complete-hotel-process.md](01-complete-hotel-process.md) |
| Guest Portal | 268 | [02-front-office-process.md](02-front-office-process.md) |
| Administration & Configuration | 393 | [08-admin-and-configuration-process.md](08-admin-and-configuration-process.md) |
| Users & Access | 42 | [09-user-roles-and-permissions.md](09-user-roles-and-permissions.md) |
| Reporting & Analytics | 636 | [10-reports-and-business-information.md](10-reports-and-business-information.md) |
| Integrations & Notifications | 152 | [11-integrations-and-data-flow.md](11-integrations-and-data-flow.md) |
| Maintenance & Service | 115 | [06-rooms-and-housekeeping-process.md](06-rooms-and-housekeeping-process.md) |
| System / Framework | 75 | [12-database-and-technical-architecture.md](12-database-and-technical-architecture.md) |
| Other / Uncategorized | 87 | [12-database-and-technical-architecture.md](12-database-and-technical-architecture.md) |
| **Total** | **2890** | |

## Reservations — 327 stored procedures

*Bookings and their lifecycle up to check-in: reservation headers/details, rates, meal plans, deposits, groups, channels.*  ·  Detail: [03-reservation-process.md](03-reservation-process.md)

#### `Allotment_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Allotment_M_AgentWiseMarketWiseChart` | M |  |
| `Allotment_M_Delete` | M |  |
| `Allotment_M_Save` | M |  |
| `Allotment_M_Select` | M |  |
| `Allotment_M_Select_ById` | M |  |

#### `EventReservation_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `EventReservation_M_Select` | M |  |
| `EventReservation_T_Select` | T |  |
| `EventReservation_T_SelectByVenueAndDate` | T |  |

#### `EventReservations_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `EventReservations_M_Delete` | M |  |
| `EventReservations_M_Save` | M |  |
| `EventReservations_M_Search` | M |  |
| `EventReservations_M_Select` | M |  |
| `EventReservations_M_SelectById` | M |  |

#### `FutureReservations_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `FutureReservations_MasterFiles_Save` | · |  |
| `FutureReservations_Save` | · |  |
| `FutureReservations_Save_NEW` | · | _backup/variant_ |
| `FutureReservations_Save_WithMultipleRoomTypeIds` | · |  |
| `FutureReservations_Save_WithSingleRoomTypeId` | · |  |
| `FutureReservations_UpdateGroupReservationNos` | · |  |

#### `PackageDetails_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PackageDetails_M_Delete` | M |  |
| `PackageDetails_M_Save` | M |  |
| `PackageDetails_M_Select` | M |  |
| `PackageDetails_M_Select_ByHeaderId` | M |  |
| `PackageDetails_M_Select_ById` | M |  |
| `PackageDetails_M_Select_ForGrid` | M |  |

#### `PackageHeaders_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PackageHeaders_M_Delete` | M |  |
| `PackageHeaders_M_Save` | M |  |
| `PackageHeaders_M_Select` | M |  |
| `PackageHeaders_M_Select_ById` | M |  |
| `PackageHeaders_M_Select_ForGrid` | M |  |
| `PackageHeaders_M_SelectByPackageCategoryId` | M |  |

#### `RateCodeHeaders_*` — 9

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RateCodeHeaders_M_Delete` | M |  |
| `RateCodeHeaders_M_RateRulesSave` | M |  |
| `RateCodeHeaders_M_Save` | M |  |
| `RateCodeHeaders_M_Select` | M |  |
| `RateCodeHeaders_M_Select_ById` | M |  |
| `RateCodeHeaders_M_Select_dev` | M |  |
| `RateCodeHeaders_M_Select_ForGrid` | M |  |
| `RateCodeHeaders_T_SelectByContryId` | T |  |
| `RateCodeHeaders_T_SelectByContryId_20211120` | T | _backup/variant_ |

#### `Reservation_*` — 128

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Reservation_Advancepayment_T_Select` | T |  |
| `Reservation_API_GetGroupReservationReservationNo` | · |  |
| `Reservation_API_GetReferencenNo` | · |  |
| `Reservation_API_GetReferenceNo` | · |  |
| `Reservation_API_GetReservationNo` | · |  |
| `Reservation_API_GetReservationUuid` | · |  |
| `Reservation_Common_SchedulePosting_Insert` | · |  |
| `Reservation_IBE_Payment_Save` | · |  |
| `Reservation_IBE_Payment_Select` | · |  |
| `Reservation_IBE_Payment_Update` | · |  |
| `Reservation_R_ArrivalList` | R |  |
| `Reservation_R_DepartureList` | R |  |
| `Reservation_R_GuestArrivalAlphabetically` | R |  |
| `Reservation_R_GuestDepartureAlphabetically` | R |  |
| `Reservation_R_HouseStatusSummary` | R |  |
| `Reservation_R_InformationSummary` | R |  |
| `Reservation_R_InHouseMealPlanSubReport` | R |  |
| `Reservation_R_InHouseRoomSummary` | R |  |
| `Reservation_R_InHouseRoomSummaryWiseComplementory` | R |  |
| `Reservation_R_InHouseRoomSummaryWiseCountries` | R |  |
| `Reservation_R_InHouseRoomSummaryWiseMealPlan` | R |  |
| `Reservation_R_InHouseRoomSummaryWiseRoomCategory` | R |  |
| `Reservation_R_ReservationDetailsWithRoomRates` | R |  |
| `Reservation_R_RoomSalesList` | R |  |
| `Reservation_R_RoomTypeWiseForeCast` | R |  |
| `Reservation_R_SelectResNoByHeaderId` | R |  |
| `Reservation_RoomAllocation_CheckDummyRoomAllocated` | · |  |
| `Reservation_T_ActivityLog_Insert` | T |  |
| `Reservation_T_AddNewGuest` | T |  |
| `Reservation_T_AddNewRoom` | T |  |
| `Reservation_T_AddNewRoom_BeforePublishOn20240221` | T |  |
| `Reservation_T_AddNewRoom_Exist` | T |  |
| `Reservation_T_AdvanceRequest_ExisitingPayments` | T |  |
| `Reservation_T_AdvanceRequest_Save` | T |  |
| `Reservation_T_AdvanceRequest_Select` | T |  |
| `Reservation_T_AdvanceRequest_SelectByDocNo` | T |  |
| `Reservation_T_AdvanceRequest_SelectByUuid` | T |  |
| `Reservation_T_AdvanceRequest_Update` | T |  |
| `Reservation_T_ApplyAllotments` | T |  |
| `Reservation_T_AttachToGroupSave` | T |  |
| `Reservation_T_AvailableAllotments` | T |  |
| `Reservation_T_BookingRemark_Update` | T |  |
| `Reservation_T_ChangeChargeCategory` | T |  |
| `Reservation_T_ChangeStaySave` | T |  |
| `Reservation_T_ChangeStaySave_20250709` | T | _backup/variant_ |
| `Reservation_T_ChangeStaySave_Back20250514` | T |  |
| `Reservation_T_ChangeStaySave_Browns` | T |  |
| `Reservation_T_ChangeStaySave_DEV` | T |  |
| `Reservation_T_ChangeStaySave_dev100` | T |  |
| `Reservation_T_ChangeStaySave_ForReservationLevel` | T |  |
| `Reservation_T_ChangeStaySave_OLD` | T | _backup/variant_ |
| `Reservation_T_ChangeStaySave_reverse10072025` | T |  |
| `Reservation_T_Confirmation_Hotel` | T |  |
| `Reservation_T_Confirmation_Hotel_TEST` | T |  |
| `Reservation_T_DetachSave` | T |  |
| `Reservation_T_FolioCreation` | T |  |
| `Reservation_T_FolioCreation_2026_01_05_Before_vButler_Onlive` | T | _backup/variant_ |
| `Reservation_T_FolioManageDetail_Select` | T |  |
| `Reservation_T_FolioManageDetail_Update` | T |  |
| `Reservation_T_FolioManageDetail_Update_20210907` | T | _backup/variant_ |
| `Reservation_T_FolioRemoval` | T |  |
| `Reservation_T_FolioWisePostingBreakUp_ByDate` | T |  |
| `Reservation_T_FolioWisePostingBreakUp_ByDate_back20260316` | T |  |
| `Reservation_T_FolioWisePostingBreakUp_ByDate_ForMissedPackageId` | T |  |
| `Reservation_T_FolioWisePostingBreakUp_Save` | T |  |
| `Reservation_T_FolioWisePostingBreakUp_Save_back20260316` | T |  |
| `Reservation_T_FolioWisePostingBreakUp_Save_History` | T | _backup/variant_ |
| `Reservation_T_FolioWisePostingBreakUp_Save_History_back20260316` | T | _backup/variant_ |
| `Reservation_T_InhouseSelect` | T |  |
| `Reservation_T_LockFolio` | T |  |
| `Reservation_T_Multiple_DetachSave` | T |  |
| `Reservation_T_ProcessTraces_Select` | T |  |
| `Reservation_T_ProcessTraces_Update` | T |  |
| `Reservation_T_QuickCheckin_Select` | T |  |
| `Reservation_T_QuickCheckin_Select_20230225` | T | _backup/variant_ |
| `Reservation_T_QuickCheckInUpdate` | T |  |
| `Reservation_T_QuickCheckInUpdate_11-11-2024` | T |  |
| `Reservation_T_QuickCheckInUpdate_20230222` | T | _backup/variant_ |
| `Reservation_T_QuickCheckInUpdate_2026_01_05_Before_vButler_Onlive` | T | _backup/variant_ |
| `Reservation_T_QuickCheckInUpdate_Aravinda` | T |  |
| `Reservation_T_QuickCheckInUpdate_Old` | T | _backup/variant_ |
| `Reservation_T_QuickCheckInUpdate_Optimized` | T |  |
| `Reservation_T_QuickCheckInValidation` | T |  |
| `Reservation_T_QuickCheckOutSelect` | T |  |
| `Reservation_T_QuickCheckOutUpdate` | T |  |
| `Reservation_T_QuickCheckOutUpdate_2026_01_05_Before_vButler_Onlive` | T | _backup/variant_ |
| `Reservation_T_QuickCheckOutUpdate_Dev` | T | _backup/variant_ |
| `Reservation_T_QuickCheckOutUpdate_OLD` | T | _backup/variant_ |
| `Reservation_T_RemoveAllotments` | T |  |
| `Reservation_T_RemoveGuest` | T |  |
| `Reservation_T_RoomAllocation_GroupBooking` | T |  |
| `Reservation_T_RoomRate_Update` | T |  |
| `Reservation_T_RoomRate_Update_Old` | T | _backup/variant_ |
| `Reservation_T_RoomRateDetails_Select` | T |  |
| `Reservation_T_Save` | T |  |
| `Reservation_T_Save_ForVouchers` | T |  |
| `Reservation_T_Save_Hotel` | T |  |
| `Reservation_T_Save_New` | T | _backup/variant_ |
| `Reservation_T_Save_New_back20250216` | T |  |
| `Reservation_T_Save_New_BeforePublishOn20240221` | T |  |
| `Reservation_T_Save_New_ProfitRoom` | T |  |
| `Reservation_T_Save_New_WithSinglePromotion` | T |  |
| `Reservation_T_SaveRoomInventory` | T |  |
| `Reservation_T_SaveRoomInventory_20200917` | T | _backup/variant_ |
| `Reservation_T_Select_ActivityDetailByTrailId` | T |  |
| `Reservation_T_Select_ActivityDetailByTrailId_Browns` | T |  |
| `Reservation_T_Select_ActivityLog` | T |  |
| `Reservation_T_Select_ActivityLog_Browns` | T |  |
| `Reservation_T_Select_ByReservationNo` | T |  |
| `Reservation_T_Select_ExistingChange` | T |  |
| `Reservation_T_Select_NonRefundedAdvancePayments` | T |  |
| `Reservation_T_SelectAllReservationsInTheSameGroup` | T |  |
| `Reservation_T_SelectComplementryDates` | T |  |
| `Reservation_T_SelectConfirmation` | T |  |
| `Reservation_T_SelectConfirmation_EmailTemplate` | T |  |
| `Reservation_T_SelectRoomsforReservationRoomAllocation` | T |  |
| `Reservation_T_SelectRoomsforReservationRoomAllocation_20220225` | T | _backup/variant_ |
| `Reservation_T_SelectRoomsforReservationRoomAllocation_Dev` | T | _backup/variant_ |
| `Reservation_T_SelectRoomsforReservationRoomChange` | T |  |
| `Reservation_T_SelectRoomTypeWiseNoOfRooms` | T |  |
| `Reservation_T_StopPosting` | T |  |
| `Reservation_T_Update` | T |  |
| `Reservation_T_Update_New` | T | _backup/variant_ |
| `Reservation_T_Update_New_back20250516` | T |  |
| `Reservation_T_Update_New_Backup20241211` | T | _backup/variant_ |
| `Reservation_T_Update_New_dev` | T |  |
| `Reservation_T_UpdateRatesOnConfirm` | T |  |
| `Reservation_T_UpdateReservationChart` | T |  |

#### `ReservationCategories_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationCategories_M_Delete` | M |  |
| `ReservationCategories_M_Save` | M |  |
| `ReservationCategories_M_Search` | M |  |
| `ReservationCategories_M_Select` | M |  |
| `ReservationCategories_M_Select_Adtive` | M |  |
| `ReservationCategories_M_SelectById` | M |  |

#### `ReservationDetails_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationDetails_M_SelectByVoucherNo` | M |  |
| `ReservationDetails_M_SelectForSendEmail` | M |  |
| `ReservationDetails_SelectForSearch` | · |  |
| `ReservationDetails_T_ForReservationHeaderId` | T |  |

#### `ReservationDocument_*` — 9

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationDocument_InsertReservationReceipt` | · |  |
| `ReservationDocument_M_Delete` | M |  |
| `ReservationDocument_M_Save` | M |  |
| `ReservationDocument_M_Save_2026_08_12` | M | _backup/variant_ |
| `ReservationDocument_M_Select_ByReservationHeaderId` | M |  |
| `ReservationDocument_MarkUploadedToOBS` | · |  |
| `ReservationDocument_Select_ById` | · |  |
| `ReservationDocument_SelectObsUrlsByReservationHeaderId` | · |  |
| `ReservationDocument_ToUploadToOBS` | · |  |

#### `ReservationEmails_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationEmails_M_Save` | M |  |
| `ReservationEmails_M_SentStatusUpdate` | M |  |
| `ReservationEmails_T_SelectToMail` | T |  |

#### `ReservationHeaders_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationHeaders_M_Select` | M |  |
| `ReservationHeaders_M_Select_ForGrid` | M |  |
| `ReservationHeaders_T_Save_ReservationHeaderWiseRooms` | T |  |
| `ReservationHeaders_T_Select` | T |  |
| `ReservationHeaders_T_SelectById` | T |  |
| `ReservationHeaders_T_SelectReservationForSchedule` | T |  |

#### `ReservationList_*` — 15

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationList_DataTable_Test` | · | _backup/variant_ |
| `ReservationList_T_Select` | T |  |
| `ReservationList_T_Select_20240412` | T | _backup/variant_ |
| `ReservationList_T_Select_AdvanceSearch` | T |  |
| `ReservationList_T_Select_AdvanceSearch_2026_01_30` | T | _backup/variant_ |
| `ReservationList_T_Select_AdvanceSearch_GroupReservations` | T |  |
| `ReservationList_T_Select_AdvanceSearch_TEST` | T |  |
| `ReservationList_T_Select_Dev` | T | _backup/variant_ |
| `ReservationList_T_Select_DynamicFilteration` | T |  |
| `ReservationList_T_Select_New` | T | _backup/variant_ |
| `ReservationList_T_Select_Old` | T | _backup/variant_ |
| `ReservationList_T_Select_Piyumi` | T |  |
| `ReservationList_T_Select_WithFilterations` | T |  |
| `ReservationList_T_SelectForAttachToGroup` | T |  |
| `ReservationList_T_SelectForGuestProfile` | T |  |

#### `ReservationListForGuestGroup_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationListForGuestGroup_T_Select` | T |  |
| `ReservationListForGuestGroup_T_Update` | T |  |
| `ReservationListForGuestGroup_T_Update_Optimises` | T |  |

#### `ReservationNOs_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationNOs_T_Select` | T |  |
| `ReservationNOs_T_Select_Back20260120` | T |  |
| `ReservationNOs_T_Select_ById` | T |  |
| `ReservationNOs_T_Select_ById_new` | T |  |
| `ReservationNOs_T_Select_dev` | T |  |
| `ReservationNOs_T_Select_Dev_20250417` | T | _backup/variant_ |
| `ReservationNOs_T_Select_old` | T |  |

#### `ReservationNotes_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationNotes_M_Delete` | M |  |
| `ReservationNotes_T_Save` | T |  |
| `ReservationNotes_T_Select` | T |  |
| `ReservationNotes_T_SelectNoteForCurrentDate` | T |  |

#### `Reservations_*` — 21

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Reservations_M_SelectForReservationChart` | M |  |
| `Reservations_M_SelectForReservationChart_ByDateRange` | M |  |
| `Reservations_R_MealPlanForGuestInhouse` | R |  |
| `Reservations_R_SelectPrintCopies` | R |  |
| `Reservations_Save_Dolphin` | · |  |
| `Reservations_Select_ByHeaderId` | · |  |
| `Reservations_SelectGuestsByReservationHeaderId` | · |  |
| `Reservations_SelectGuestsByReservationHeaderId_2026_08_12` | · | _backup/variant_ |
| `Reservations_T_CheckFreeNights` | T |  |
| `Reservations_T_CheckOutList` | T |  |
| `Reservations_T_CheckOutList_dev` | T |  |
| `Reservations_T_ReservationTypeChange` | T |  |
| `Reservations_T_ReservationTypeChange_BeforeHUActivation` | T |  |
| `Reservations_T_ReservationTypeChange_dev` | T |  |
| `Reservations_T_ReservationTypeChangeSelectById` | T |  |
| `Reservations_T_SELECT_For_AdvancedPaymentList` | T |  |
| `Reservations_T_Select_For_Grid` | T |  |
| `Reservations_T_Select_For_GuestDetails` | T |  |
| `Reservations_T_Select_For_SchedulePosting` | T |  |
| `Reservations_T_Select_WithInHouseReservationsAndReservations` | T |  |
| `Reservations_T_UpdateNoShow` | T |  |

#### `ReservationStatus_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationStatus_M_Delete` | M |  |
| `ReservationStatus_M_Save` | M |  |
| `ReservationStatus_M_Select` | M |  |
| `ReservationStatus_M_Select_ById` | M |  |
| `ReservationStatus_M_Select_ForGrid` | M |  |

#### `ReservationTraces_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationTraces_M_Delete` | M |  |
| `ReservationTraces_M_Save` | M |  |
| `ReservationTraces_M_Select` | M |  |
| `ReservationTraces_M_SelectById` | M |  |
| `ReservationTraces_T_SelectReservationRemindTraceForCurrentDate` | T |  |
| `ReservationTraces_T_UpdateRemark` | T |  |

#### `ReservationWise_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ReservationWise_InsertReservationRelatedReceiptsFromSource` | · |  |
| `ReservationWise_Receipts_MarkDownloaded` | · |  |
| `ReservationWise_ReceiptsToDownload` | · |  |

#### `Seasons_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Seasons_M_Delete` | M |  |
| `Seasons_M_Save` | M |  |
| `Seasons_M_Select` | M |  |
| `Seasons_M_SelectBy_Id` | M |  |

#### `Select_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Select_AttachedMemeberDetail_ByReservationHeaderId` | · |  |
| `Select_GroupReservationsToDetach` | · |  |
| `Select_MealReservationAdvanveDocNo` | · |  |
| `Select_ReservationWiseReservationRelatedDocumentDownload` | · |  |

#### Other Reservations procedures — 59

| Stored procedure | Type | Notes |
|---|:--:|---|
| `AllocatedRoomsForGroupReservation_T_Update` | T |  |
| `AllotmentDetails_Reconcile_Update` | · |  |
| `Attach_MemeberDetail_ByReservationHeaderId` | · |  |
| `CancelReservation_M_Save` | M |  |
| `ChangeStay_M_Select` | M |  |
| `CheckOut_ReservationHeaders_T_Select` | T |  |
| `CheckOutReservationList_M_Reinstate` | M |  |
| `CheckRoomAvailability_ForReservationChart` | · |  |
| `ComplementaryReservation_R_Select` | R |  |
| `Detach_AttachedMemeberDetail_ByReservationHeaderId` | · |  |
| `Discounts_M_Select_ById` | M |  |
| `EventReservationDetail_M_Delete` | M |  |
| `EventReservationDetails_M_Save` | M |  |
| `ExistingReservationList_M_Select` | M |  |
| `ExpectedArrivals_ReservationHeaders_T_Select` | T |  |
| `ExpectedDeparture_ReservationHeaders_T_Select` | T |  |
| `GroupReservationNo_M_Select` | M |  |
| `ProformaInvoice_M_SelectBySingleOrGroupReservation` | M |  |
| `RateCodeWiseFreeNights_M_Save` | M |  |
| `RateCodeWiseFreeNights_Select_ById` | · |  |
| `Rates_T_SelectForReservationChart` | T |  |
| `Remarks_Select_ByReservationHeaderId` | · |  |
| `ReservationAlert_T_Delete` | T |  |
| `ReservationAlert_T_Save` | T |  |
| `ReservationAlerts_T_Select` | T |  |
| `ReservationAlerts_T_Select_ById` | T |  |
| `ReservationBlockDates_M_Save` | M |  |
| `ReservationBlockDates_T_Save` | T |  |
| `ReservationBlockDatesAvailability_W_Select` | W |  |
| `ReservationChartLegend_M_Select` | M |  |
| `ReservationEmailWiseMailDetails_M_SelectByCode` | M |  |
| `ReservationEmailWiseParameters_T_SelectToMailById` | T |  |
| `ReservationListFilterationColumns_Insert` | · |  |
| `ReservationListFilterMethod_M_Select` | M |  |
| `ReservationListForAttachAllotment_T_Select` | T |  |
| `ReservationListForGRC_T_Select` | T |  |
| `ReservationListForGuestInformation_T_Select` | T |  |
| `ReservationListForGuestInformation_T_Select_Optimized` | T |  |
| `ReservationListForPrintCopy` | · |  |
| `ReservationListForSingleGuest_T_Select` | T |  |
| `ReservationListSortingColumns_M_Select` | M |  |
| `ReservationNoteFor_Select` | · |  |
| `ReservationNoteType_M_Select` | M |  |
| `ReservationNumbers_M_SelectById` | M |  |
| `ReservationNumbers_M_SelectByType` | M |  |
| `ReservationPostingSettings_M_Select_ById` | M |  |
| `ReservationReminder_M_SelectReservationReminderStatus` | M |  |
| `ReservationReminderStatus_M_Save` | M |  |
| `ReservationReminderStatus_M_Update` | M |  |
| `ReservationTypes_M_Select` | M |  |
| `ReservationWithoutGroup_T_Confirmation_Hotel` | T |  |
| `Rpt_GuestReservationRepiters` | · |  |
| `Rpt_GuestReservationRepiters_OLD_20250305` | · | _backup/variant_ |
| `Season_M_Select_ForGrid` | M |  |
| `SelectCancelReservationsReservationNo` | · |  |
| `SelectCheckedOutGuestDetailsByReservationNo` | · |  |
| `SelectFutureReservationsReservationNo` | · |  |
| `SelectGuestComplainByReservationNo` | · |  |
| `SelectInHouseGuestDetailsByReservationNo` | · |  |

## Front Office — In-house & Check-in/out — 39 stored procedures

*The in-house guest and arrival/departure: in-house reservation copies, check-in/out, walk-in, no-show.*  ·  Detail: [04-check-in-check-out-process.md](04-check-in-check-out-process.md)

#### `Getthesearrived_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Getthesearrived` | · |  |
| `Getthesearrived_new` | · |  |
| `Getthesearrived_old` | · |  |

#### `InHouse_*` — 9

| Stored procedure | Type | Notes |
|---|:--:|---|
| `InHouse_ReservationHeaders_Select` | · |  |
| `InHouse_ReservationHeaders_T_Select` | T |  |
| `InHouse_ReservationHeaders_T_Select_BeforeOptimize` | T |  |
| `InHouse_ReservationHeaders_T_Select_BeforePublishOn20240221` | T |  |
| `InHouse_ReservationHeaders_T_Select_Sachith20220301` | T |  |
| `InHouse_ReservationHeaders_T_SelectForAttachToGroup` | T |  |
| `InHouse_RoomDetails_T_Select` | T |  |
| `InHouse_RoomDetails_T_Select_1` | T |  |
| `InHouse_RoomDetails_T_Select_Dev` | T | _backup/variant_ |

#### `InhouseReservationList_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `InhouseReservationList_T_Select_AdvanceSearch` | T |  |
| `InhouseReservationList_T_Select_AdvanceSearch2` | T |  |
| `InhouseReservationList_T_Select_AdvanceSearch_Dev` | T | _backup/variant_ |
| `InhouseReservationList_T_Select_AdvanceSearch_GroupReservations` | T |  |

#### `InhouseReservationSummary_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `InhouseReservationSummary_CountryWise` | · |  |
| `InhouseReservationSummary_FolioWise` | · |  |
| `InhouseReservationSummary_MealPlanWise` | · |  |
| `InhouseReservationSummary_RoomCategoryWise` | · |  |

#### Other Front Office — In-house & Check-in/out procedures — 19

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CheckedOutReservationHeader_M_SelectReservationNo` | M |  |
| `CheckedOutReservationList_T_Select_AdvanceSearch` | T |  |
| `CheckedOutReservationList_T_Select_AdvanceSearch_GroupReservations` | T |  |
| `Getthesearrivals` | · |  |
| `Getthesearrivals_20250818` | · | _backup/variant_ |
| `GettheseDeparted` | · |  |
| `GettheseDepartures` | · |  |
| `GettheseExpectedarrivals` | · |  |
| `GettheseExpectedDepartures` | · |  |
| `Inhouse_Reservations_T_Select_For_SchedulePosting` | T |  |
| `InhouseReservation_T_FolioCreation` | T |  |
| `InhouseReservation_T_SelectRoomsforReservationRoomChange` | T |  |
| `InHouseReservationDetail_T_ChangeRoom` | T |  |
| `InHouseReservationDetail_T_ChangeRoom_Old` | T | _backup/variant_ |
| `InhouseReservationHeaders_Active_Rooms` | · |  |
| `InHouseReservationHeaders_T_Select_ByReservationId` | T |  |
| `InHouseReservationHeaders_T_Select_ForRoomChange` | T |  |
| `InHouseReservationList_M_Reinstate` | M |  |
| `InHouseReservationList_M_Reinstate_Back20241111` | M |  |

## Front Office — Guest Profiles — 67 stored procedures

*Guest master data: profiles, identity documents, history, preferences.*  ·  Detail: [02-front-office-process.md](02-front-office-process.md)

#### `Guest_*` — 10

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Guest_Alergies_M_Delete` | M |  |
| `Guest_Alergies_M_Save` | M |  |
| `Guest_Alergies_M_Select` | M |  |
| `Guest_Communication_Details_M_Delete` | M |  |
| `Guest_Communication_Details_M_Save` | M |  |
| `Guest_Communication_Details_M_Select` | M |  |
| `Guest_Notes_M_Delete` | M |  |
| `Guest_Preferences_M_Delete` | M |  |
| `Guest_Preferences_M_Save` | M |  |
| `Guest_Preferences_M_Select` | M |  |

#### `GuestProfile_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `GuestProfile_M_SaveForMember_Api` | M |  |
| `GuestProfile_M_SaveForMember_Api_Test` | M | _backup/variant_ |
| `GuestProfile_M_Select_By_ReservationHeaderId` | M |  |
| `GuestProfile_M_Select_ByReservationNo` | M |  |
| `GuestProfile_R_Select_BY_Country` | R |  |
| `GuestProfile_T_ActivityLog_Insert` | T |  |
| `GuestProfile_T_Select_ActivityLog` | T |  |

#### `GuestProfiles_*` — 14

| Stored procedure | Type | Notes |
|---|:--:|---|
| `GuestProfiles_M_Delete` | M |  |
| `GuestProfiles_M_Save` | M |  |
| `GuestProfiles_M_Save_FromNewReservation` | M |  |
| `GuestProfiles_M_Save_OnReservationCreation` | M |  |
| `GuestProfiles_M_Select` | M |  |
| `GuestProfiles_M_Select_ById` | M |  |
| `GuestProfiles_M_Select_ForCurrencyEnchashment` | M |  |
| `GuestProfiles_M_Select_ForGrid` | M |  |
| `GuestProfiles_M_SelectFolioDetailsByGuest` | M |  |
| `GuestProfiles_M_SelectInHouseGuest` | M |  |
| `GuestProfiles_M_SelectReservationsByGuest` | M |  |
| `GuestProfiles_SelectMembers_Popup` | · |  |
| `GuestProfiles_T_Search` | T |  |
| `GuestProfiles_T_Search_Test` | T | _backup/variant_ |

#### `Guests_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Guests_T_Select_ByReservationId` | T |  |
| `Guests_T_Select_ByRoomId` | T |  |
| `Guests_T_SelectByReservationId` | T |  |

#### `PassportDocumentDetails_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PassportDocumentDetails_M_Save` | M |  |
| `PassportDocumentDetails_M_Save_2026_08_12` | M | _backup/variant_ |
| `PassportDocumentDetails_M_Save_BeforeUpdate_PassportScaanner_2024_05_29` | M | _backup/variant_ |

#### `Widgets_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Widgets_GuestHistory_Select_Financials` | · | _backup/variant_ |
| `Widgets_GuestHistory_Select_Preferences` | · | _backup/variant_ |
| `Widgets_GuestHistory_Select_Stays` | · | _backup/variant_ |

#### Other Front Office — Guest Profiles procedures — 27

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Alergies_M_Select` | M |  |
| `DailyGuestRoomNightForecastAnalysis` | · |  |
| `GuestComplainCategories_T_Select` | T |  |
| `GuestComplainWiseAssignees_M_Select` | M |  |
| `GuestComplainWiseAssignees_Save` | · |  |
| `GuestInspectedDetails_Update` | · |  |
| `GuestMessage_M_Delete` | M |  |
| `GuestMessage_M_Save` | M |  |
| `GuestMessages_M_Select_ForGrid` | M |  |
| `GuestMessages_M_UpdateIsDelivered` | M |  |
| `GuestName_M_Select` | M |  |
| `GuestNote_M_Select` | M |  |
| `GuestNotes_M_Save` | M |  |
| `GuestProfileDuplicate_Remove` | · |  |
| `GuestProfileMerge_M_Select` | M |  |
| `GuestProfileMerge_T_Save` | T |  |
| `GuestProfileTypes_M_Select` | M |  |
| `GuestProfileWiseAllergies_Update` | · |  |
| `GuestProfileWiseAllergies_Update_2026_01_05_Before_vButler_Onlive` | · | _backup/variant_ |
| `HeadCountWiseGuestProfile_Creation` | · |  |
| `Inquery_GuestNightsInformation` | · |  |
| `Rpt_GuestPoliceReports` | · |  |
| `ScanedPassport_M_Save` | M |  |
| `ScanedPassport_M_Select` | M |  |
| `SelectGuestComplainWiseAssignees` | · |  |
| `SelectGuestInquiryDetails` | · |  |
| `SelectIsMainGuest` | · |  |

## Rooms & Housekeeping — 229 stored procedures

*Physical rooms and their readiness: room master, room status, cleaning, inspection, out-of-order.*  ·  Detail: [06-rooms-and-housekeeping-process.md](06-rooms-and-housekeeping-process.md)

#### `BedTypes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `BedTypes_M_Delete` | M |  |
| `BedTypes_M_Save` | M |  |
| `BedTypes_M_Select` | M |  |
| `BedTypes_M_Select_ById` | M |  |
| `BedTypes_M_Select_ForGrid` | M |  |

#### `Floors_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Floors_M_Delete` | M |  |
| `Floors_M_Save` | M |  |
| `Floors_M_Select` | M |  |
| `Floors_M_Select_ByDisplayOrder` | M |  |
| `Floors_M_Select_ById` | M |  |
| `Floors_M_Select_ByIndex` | M |  |
| `Floors_M_Select_ForGrid` | M |  |

#### `HK_*` — 55

| Stored procedure | Type | Notes |
|---|:--:|---|
| `HK_AddReservationToQueue` | · |  |
| `HK_ChangeQueuePriorityState` | · |  |
| `HK_Countries_M_SelectForAPI` | M |  |
| `HK_DashboardFigures_SelectForDisplay` | · |  |
| `HK_DirectPrint_AvoidDuplicatePrint_M_Select` | M |  |
| `HK_DirectPrint_CreateDocument_M_Select` | M |  |
| `HK_DocumentsToDownload` | · |  |
| `HK_DocumentsToDownload_UpdateStatus` | · |  |
| `HK_DocumentsToWhatappOrEmail` | · |  |
| `HK_DocumentsToWhatappOrEmail_UpdateStatus` | · |  |
| `HK_Floors_M_Select` | M |  |
| `HK_FrontOfficeRoomStatus_M_Select` | M |  |
| `HK_FrontOfficeStatusWiseHouseKeepingStatus_Select` | · |  |
| `HK_GuestProfile_UpdateWithAllergies` | · |  |
| `HK_GuestProfiles_DeleteSharerByGuestProfileId` | · |  |
| `HK_GuestProfiles_SelectByReservationHeaderId` | · |  |
| `HK_GuestProfiles_SelectPredefinedAllergies` | · |  |
| `HK_GuestProfiles_SelectPredefinedAllergies_2026_01_05_Before_vButler_Onlive` | · | _backup/variant_ |
| `HK_GuestService_Status_Update` | · |  |
| `HK_HouseKeeping_Status_Update` | · |  |
| `HK_HouseKeeping_Status_Update_Common` | · |  |
| `HK_HouseKeepingRoomStatus_M_Select` | M |  |
| `HK_HouseKeepingStatus_M_Select` | M |  |
| `HK_InhouseReservations_Select` | · |  |
| `HK_Nationalities_M_SelectForAPI` | M |  |
| `HK_NHKM_CommonArea_UpdateStatusByRoomBoy` | · |  |
| `HK_NHKM_CommonAreaStatuses_Select` | · |  |
| `HK_OutstandingStatementPreview_Save` | · |  |
| `HK_QueueReservationDetails_SelectByReservationHeaderId` | · |  |
| `HK_QuickCheckin_Select` | · |  |
| `HK_QuickCheckOut_Select` | · |  |
| `HK_RemoveReservationsFromQueue` | · |  |
| `HK_ReservationPriority_Select` | · |  |
| `HK_ReservationQueueNotificationSMS_Send` | · |  |
| `HK_Reservations_SelectToQueue` | · |  |
| `HK_RoomBoyChangesByRoomIdAndRoomBoyId` | · |  |
| `HK_RoomBoyWiseRoomChecklistProgress_T_SelectByRoomBoyId` | T |  |
| `HK_RoomBoyWiseRoomChecklistProgress_T_Update` | T |  |
| `HK_RoomCategories_M_Select` | M |  |
| `HK_RoomFeatures_M_Select` | M |  |
| `HK_Salutations_M_SelectForAPI` | M |  |
| `HK_Save_DocumentsToSend` | · |  |
| `HK_Save_DocumentToDeliver` | · |  |
| `HK_Select_DocumentSendingMethods` | · |  |
| `HK_Select_DocumentTypes` | · |  |
| `HK_Select_PendingDocuments` | · |  |
| `HK_Select_RoomBoyChecklist_ByRoomBoyIdAndRoomId` | · |  |
| `HK_Select_RoomWiseCheckListItems` | · |  |
| `HK_Select_SupervisorWiseVacantCleanRoomingList` | · |  |
| `HK_SelectAppNotifications` | · |  |
| `HK_SelectGuestsByReservationHeaderId` | · |  |
| `HK_SelectHotelPolicies` | · |  |
| `HK_ServiceRoomStatus_M_Select` | M |  |
| `HK_StatusWise_RoomDetails_Select` | · |  |
| `HK_StatusWise_RoomDetails_Select_20250305` | · | _backup/variant_ |

#### `HouseKeeping_*` — 19

| Stored procedure | Type | Notes |
|---|:--:|---|
| `HouseKeeping_FrontOfficeStatusWiseHouseKeepingStatus` | · |  |
| `HouseKeeping_M_SaveRoomWiseRoomBoys` | M |  |
| `HouseKeeping_M_SaveSupervisorWiseRooms` | M |  |
| `HouseKeeping_M_Select_DateWise` | M |  |
| `HouseKeeping_M_SelectRoomWiseRoomBoys_ByRoomBoyId` | M |  |
| `HouseKeeping_M_SelectSupervisorWiseAssignedRooms` | M |  |
| `HouseKeeping_ProcessWiseStatusChanges_Update` | · |  |
| `HouseKeeping_ProcessWiseStatusChanges_Update_Old` | · | _backup/variant_ |
| `HouseKeeping_RoomStatus_CategoryWise` | · |  |
| `HouseKeeping_RoomStatus_Delete` | · |  |
| `HouseKeeping_RoomStatus_Save` | · |  |
| `HouseKeeping_RoomStatus_Select` | · |  |
| `HouseKeeping_RoomStatus_Select_ByCategory` | · |  |
| `HouseKeeping_RoomStatus_Select_ById` | · |  |
| `HouseKeeping_Select_ForGrid` | · |  |
| `HouseKeeping_Select_RoomStatusCategory_ByID` | · |  |
| `HouseKeeping_Status_Select` | · |  |
| `HouseKeeping_Txn` | · |  |
| `HouseKeeping_UpdateRoomStatus` | · |  |

#### `HouseKeepingStatus_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `HouseKeepingStatus_M_Delete` | M |  |
| `HouseKeepingStatus_M_Save` | M |  |
| `HouseKeepingStatus_M_Select` | M |  |
| `HouseKeepingStatus_M_Select_ById` | M |  |
| `HouseKeepingStatus_M_Select_ForGrid` | M |  |

#### `OutofOrderReasons_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `OutofOrderReasons_M_Delete` | M |  |
| `OutofOrderReasons_M_Save` | M |  |
| `OutofOrderReasons_M_Select` | M |  |
| `OutofOrderReasons_M_Select_ById` | M |  |

#### `OutofOrderTxn_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `OutofOrderTxn_M_Delete` | M |  |
| `OutofOrderTxn_M_Select` | M |  |
| `OutofOrderTxn_M_Select_ById` | M |  |

#### `RoomAreas_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomAreas_M_Delete` | M |  |
| `RoomAreas_M_Save` | M |  |
| `RoomAreas_M_Select` | M |  |
| `RoomAreas_M_Select_ById` | M |  |
| `RoomAreas_M_Select_ForGrid` | M |  |

#### `RoomAvailability_*` — 28

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomAvailability_Occupancy_Forecast` | · |  |
| `RoomAvailability_Occupancy_Forecast_Common` | · |  |
| `RoomAvailability_Occupancy_Forecast_Common_Parameterized` | · |  |
| `RoomAvailability_Occupancy_Forecast_Common_TEST` | · |  |
| `RoomAvailability_Occupancy_Forecast_Common_yy` | · |  |
| `RoomAvailability_Occupancy_Forecast_Parameterized` | · |  |
| `RoomAvailability_R_Select` | R |  |
| `RoomAvailability_R_Select_20200919` | R | _backup/variant_ |
| `RoomAvailability_R_Select_20210410` | R | _backup/variant_ |
| `RoomAvailability_R_Select_20221125` | R | _backup/variant_ |
| `RoomAvailability_R_Select_back20250514` | R |  |
| `RoomAvailability_R_Select_BeforeOptimized` | R |  |
| `RoomAvailability_R_Select_ForManageReservationList` | R |  |
| `RoomAvailability_R_Select_ForManageReservationList_20221125` | R | _backup/variant_ |
| `RoomAvailability_R_Select_ForManageReservationList_Browns` | R |  |
| `RoomAvailability_R_Select_ForManageReservationList_Test` | R | _backup/variant_ |
| `RoomAvailability_R_Select_ForManageReservationList_TEST2` | R |  |
| `RoomAvailability_R_Select_Modified` | R |  |
| `RoomAvailability_Today_ArrivedStayOversDeparted` | · |  |
| `RoomAvailability_Today_ExpectedArrivals` | · |  |
| `RoomAvailability_Today_Occupancy` | · |  |
| `RoomAvailability_Today_Occupancy_Parameterized` | · |  |
| `RoomAvailability_W_PreventOverbook` | W |  |
| `RoomAvailability_W_PreventOverbook_11/11` | W |  |
| `RoomAvailability_W_PreventOverbook_MailStehani` | W |  |
| `RoomAvailability_W_Select` | W |  |
| `RoomAvailability_W_Select_20200918` | W | _backup/variant_ |
| `RoomAvailability_W_Select_20200919` | W | _backup/variant_ |

#### `RoomBoyDetails_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomBoyDetails_M_Delete` | M |  |
| `RoomBoyDetails_M_Save` | M |  |
| `RoomBoyDetails_M_Select` | M |  |
| `RoomBoyDetails_M_Select_ById` | M |  |

#### `RoomCategories_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomCategories_M_Delete` | M |  |
| `RoomCategories_M_Save` | M |  |
| `RoomCategories_M_Select` | M |  |
| `RoomCategories_M_Select_ById` | M |  |
| `RoomCategories_M_Select_ForGrid` | M |  |
| `RoomCategories_M_SelectForAvailability` | M |  |

#### `RoomDetails_*` — 9

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomDetails_M_Delete` | M |  |
| `RoomDetails_M_Save` | M |  |
| `RoomDetails_M_Select` | M |  |
| `RoomDetails_M_Select_ByCategoryId` | M |  |
| `RoomDetails_M_Select_ById` | M |  |
| `RoomDetails_M_Select_ForGrid` | M |  |
| `RoomDetails_M_SelectForReservationChart` | M |  |
| `RoomDetails_M_SelectInHouseRooms` | M |  |
| `RoomDetails_M_SelectInHouseRoomsForRToRTransfer` | M |  |

#### `RoomDetailsM_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomDetailsM_SelectForReport` | · |  |
| `RoomDetailsM_SelectForReport_TEST` | · |  |
| `RoomDetailsM_SelectForReportModified` | · |  |

#### `RoomFeatures_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomFeatures_M_Delete` | M |  |
| `RoomFeatures_M_Save` | M |  |
| `RoomFeatures_M_Select_ForGrid` | M |  |
| `RoomFeatures_M_SelectById` | M |  |

#### `RoomInspectionDetails_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomInspectionDetails_M_Delete` | M |  |
| `RoomInspectionDetails_M_Select` | M |  |
| `RoomInspectionDetails_T_Save` | T |  |

#### `RoomRate_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomRate_MinimumRateRestriction_T_Select` | T |  |
| `RoomRate_MinimumRateRestriction_T_Select_ForReservationHeaderId` | T |  |
| `RoomRate_MinimumRateRestriction_T_SelectByPickupDate` | T |  |
| `RoomRate_MinimumRateRestriction_T_SelectByReservationDate` | T |  |
| `RoomRate_T_SelectOnMealPlanAndRoomTypeChange` | T |  |

#### `RoomRates_*` — 9

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomRates_M_ModifyNOTUSE` | M |  |
| `RoomRates_M_Save` | M |  |
| `RoomRates_M_SaveNOTUSE` | M |  |
| `RoomRates_M_Select` | M |  |
| `RoomRates_M_Select_ById` | M |  |
| `RoomRates_M_SelectForDateRange` | M |  |
| `RoomRates_R_Grid` | R |  |
| `RoomRates_T_RateCodeCopySave` | T |  |
| `RoomRates_W_SelectForBooking` | W |  |

#### `RoomTypes_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomTypes_M_Delete` | M |  |
| `RoomTypes_M_Save` | M |  |
| `RoomTypes_M_Select` | M |  |
| `RoomTypes_M_Select_ById` | M |  |
| `RoomTypes_M_Select_ForGrid` | M |  |
| `RoomTypes_M_SelectForAddRoom` | M |  |
| `RoomTypes_M_SelectForAvailability` | M |  |

#### `RoomWiseInventoryItems_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RoomWiseInventoryItems_M_Delete` | M |  |
| `RoomWiseInventoryItems_M_Select` | M |  |
| `RoomWiseInventoryItems_M_Select_ByRoomId` | M |  |
| `RoomWiseInventoryItems_M_Select_ForGrid` | M |  |

#### `Select_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Select_Common_RoomStatusChart` | · |  |
| `Select_M_RoomList` | M |  |
| `Select_M_RoomListAndRoomStatus` | M |  |
| `Select_M_RoomListAndRoomStatus_byDate` | M |  |
| `Select_M_RoomListAndRoomStatus_byFloorId` | M |  |
| `Select_M_RoomListAndRoomStatus_byRoomCategoryId` | M |  |

#### Other Rooms & Housekeeping procedures — 38

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Checkout_RoomDetails_T_Select` | T |  |
| `DailyRoomAvailability_R_Select` | R |  |
| `GetAllRoomsDetails` | · |  |
| `GetRoomAllocationLog` | · |  |
| `HKDocumentTypes_Select` | · |  |
| `HKSettings_Select` | · |  |
| `HKSettings_Update` | · |  |
| `HouseKeepingStatusHistory_Select` | · | _backup/variant_ |
| `Inquery_RoomNightsInformation` | · |  |
| `Inquery_RoomPickupsInformation` | · |  |
| `InspectionTime_M_Select` | M |  |
| `MiniDashboard_Select_VacantRoomForCard` | · |  |
| `OutOfOrder_T_RoomWise_QuickDelete` | T |  |
| `OutOfOrder_T_Select_RoomWise` | T |  |
| `OutOfOrderReasons_M_Select_ForGrid` | M |  |
| `OutOfOrderTXN_M_Insert` | M |  |
| `OutOfOrderTxn_Select_ForGrid` | · |  |
| `Room_Availability_M_Insert` | M |  |
| `Room_Availability_M_Select` | M |  |
| `RoomAllocationAttributes_M_Select` | M |  |
| `RoomAvailabilitySummary_for_Email` | · |  |
| `RoomBoys_M_Select` | M |  |
| `RoomCategoriesWiseRoomTypes_W_Select` | W |  |
| `RoomChange_R_Select` | R |  |
| `RoomChangeReason_M_Select` | M |  |
| `RoomChargeMissedReservations_Select` | · |  |
| `RoomDetailsWiseKeyCode_M_Select` | M |  |
| `RoomInspection_T_Select_ForUpdate` | T |  |
| `RoomInspectionTimes_M_Select` | M |  |
| `RoomInventory_T_Delete` | T |  |
| `RoomInventory_T_ReservationWiseAllocation` | T |  |
| `RoomInventoryItems_T_SelectAvailable` | T |  |
| `RoomStatusCategory_M_Select` | M |  |
| `RoomStatusCategory_M_SelectBy_QueryStringValue` | M |  |
| `RoomWiseInventoryitems_M_Save` | M |  |
| `RoomWiseInventoryitems_M_Select_ById` | M |  |
| `RptInHousePaidRooms` | · |  |
| `SelectRoomStatus` | · |  |

## Cashiering, Folio & Day-End — 345 stored procedures

*The money: folios, postings, taxes, bills, settlements, advances, credit/debit notes, and the nightly day-end.*  ·  Detail: [05-cashiering-and-finance-process.md](05-cashiering-and-finance-process.md)

#### `Advance_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Advance_Payment_Cancellation_T_Save` | T |  |
| `Advance_Payment_T_Save` | T |  |
| `Advance_Payment_T_Save_back20260626` | T |  |

#### `AdvanceRequestOnline_*` — 12

| Stored procedure | Type | Notes |
|---|:--:|---|
| `AdvanceRequestOnline_T_Delete` | T |  |
| `AdvanceRequestOnline_T_ReSendEmail` | T |  |
| `AdvanceRequestOnline_T_Save` | T |  |
| `AdvanceRequestOnline_T_Select` | T |  |
| `AdvanceRequestOnline_T_SelectBankDetailsByUuid` | T |  |
| `AdvanceRequestOnline_T_SelectByUuid` | T |  |
| `AdvanceRequestOnline_T_SelectByUuid_20240105` | T | _backup/variant_ |
| `AdvanceRequestOnline_T_SelectByUuid_Validation` | T |  |
| `AdvanceRequestOnline_T_SelectPropertyDetails` | T |  |
| `AdvanceRequestOnline_T_SelectRoomDetailsByUuid` | T |  |
| `AdvanceRequestOnline_T_SendEmail` | T |  |
| `AdvanceRequestOnline_T_SendEmail_2024_01_11` | T | _backup/variant_ |

#### `AdvanceRequestOnlinePayment_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `AdvanceRequestOnlinePayment_T_Save` | T |  |
| `AdvanceRequestOnlinePayment_T_Save_2024-01-07` | T |  |
| `AdvanceRequestOnlinePayment_T_Save_20240105` | T | _backup/variant_ |

#### `AdvanceRequestOnlinePaymentResponse_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `AdvanceRequestOnlinePaymentResponse_T_Save` | T |  |
| `AdvanceRequestOnlinePaymentResponse_T_Save_2024_01_09` | T | _backup/variant_ |
| `AdvanceRequestOnlinePaymentResponse_T_SelectTransactionSearch` | T |  |
| `AdvanceRequestOnlinePaymentResponse_T_UpdateTransactionSearch` | T |  |

#### `CalculateFolioChargersToBill_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CalculateFolioChargersToBill` | · |  |
| `CalculateFolioChargersToBill_dev` | · |  |
| `CalculateFolioChargersToBill_dev100` | · |  |

#### `ChargeCodes_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ChargeCodes_M_Delete` | M |  |
| `ChargeCodes_M_Save` | M |  |
| `ChargeCodes_M_Select` | M |  |
| `ChargeCodes_M_Select_ById` | M |  |
| `ChargeCodes_M_Select_ForGrid` | M |  |
| `ChargeCodes_T_Select_Discountable` | T |  |

#### `ChargeTypes_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ChargeTypes_M_Delete` | M |  |
| `ChargeTypes_M_Select` | M |  |
| `ChargeTypes_M_Select_ForGrid` | M |  |

#### `CreditOrDebitNote_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CreditOrDebitNote_BillSettlementDetails_Select_ByReservationNoOrInvoiceNo` | · |  |
| `CreditOrDebitNote_InvoiceNoWiseDetails_Save` | · |  |
| `CreditOrDebitNote_InvoiceNoWiseDetails_Save_OLDON18062025` | · |  |
| `CreditOrDebitNote_SettledFolioDetails_Select_ByInvoiceNo` | · |  |

#### `Dayend_*` — 12

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Dayend_ChangeConvertionOn_FirstNight` | · |  |
| `Dayend_Extraposting_MoveToHistory` | · | _backup/variant_ |
| `Dayend_GL_ExtraPosting_Save` | · |  |
| `Dayend_GL_ExtraPosting_Save20250131` | · |  |
| `Dayend_GL_ExtraPosting_Save_back20250107` | · |  |
| `Dayend_GL_ExtraPosting_Save_back20260212` | · |  |
| `Dayend_GL_MainBillSettlementDetails_Save` | · |  |
| `Dayend_RevenueAndOccupancySummary_Executions_M_Save` | M |  |
| `Dayend_RevenueAndOccupancySummary_Executions_M_Save_BackUp20250408` | M |  |
| `Dayend_RevenueAndOccupancySummary_Executions_M_Save_ByStayPeriod` | M |  |
| `Dayend_RevenueAndOccupancySummary_Executions_M_Save_ByStayPeriod_Parameterized` | M |  |
| `Dayend_RevenueAndOccupancySummary_Executions_M_Save_Parameterized` | M |  |

#### `DayEnd_*` — 25

| Stored procedure | Type | Notes |
|---|:--:|---|
| `DayEnd_CompleteDayEnd` | · |  |
| `DayEnd_CompleteDayEnd_back20260316` | · |  |
| `DayEnd_DayEndDayEndStepCompletion_Check` | · |  |
| `DayEnd_DayEndDayEndStepCompletion_Insert` | · |  |
| `DayEnd_FrontOffice_Check` | · |  |
| `DayEnd_PseudoRoom_Check` | · |  |
| `DayEnd_RoomPickup_M_Save` | M |  |
| `DayEnd_RoomRates_Check` | · |  |
| `DayEnd_RoomStatus_M_Save` | M |  |
| `DayEnd_Summary_M_Save` | M |  |
| `DayEnd_Summary_M_Save_Dev` | M | _backup/variant_ |
| `DayEnd_SummaryGuestLedger_M_Save` | M |  |
| `DayEnd_SummaryGuestLedger_M_Save_20240131` | M | _backup/variant_ |
| `DayEnd_SummaryGuestLedger_M_Save_2025-12-17` | M |  |
| `DayEnd_SummaryGuestLedger_M_Save_Ai_Agent` | M |  |
| `DayEnd_SummaryGuestLedger_M_Save_Back20250121` | M |  |
| `DayEnd_SummaryGuestLedger_M_Save_back20250811_new` | M |  |
| `DayEnd_SummaryGuestLedger_M_Save_Back20250815` | M |  |
| `DayEnd_SummaryGuestLedger_M_Save_back20251202` | M |  |
| `DayEnd_SummaryGuestLedger_M_Save_dev` | M |  |
| `DayEnd_SummaryGuestLedger_M_Save_For_RunManully` | M |  |
| `DayEnd_SummaryGuestLedger_M_Save_ForReservation` | M |  |
| `DayEnd_UpdateHotelDate` | · |  |
| `DayEnd_UpdateHotelDate BUP` | · |  |
| `DayEnd_UpdateHotelDate_Old` | · | _backup/variant_ |

#### `DayEndSummary_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `DayEndSummary_InhouseRevenueMissMatch` | · |  |
| `DayEndSummary_InhouseRevenueMissMatch_Send_Mail` | · |  |
| `DayEndSummary_InhouseRevenueMissMatch_Send_Mail_dev` | · |  |

#### `DirectRebate_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `DirectRebate` | · |  |
| `DirectRebate_20250206` | · | _backup/variant_ |
| `DirectRebate_back20240527` | · |  |
| `DirectRebate_back20240827` | · |  |

#### `ExtraPosting_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ExtraPosting_T_Void_ByDocumentNo` | T |  |
| `ExtraPosting_T_Void_ByDocumentNo_Back20250429` | T |  |
| `ExtraPosting_T_Void_ByDocumentNo_DEV` | T |  |

#### `ExtraPostings_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ExtraPostings_T_Select_CurrentDate` | T |  |
| `ExtraPostings_T_Void` | T |  |
| `ExtraPostings_T_Void_back20260728` | T |  |
| `ExtraPostings_T_Void_Dev` | T | _backup/variant_ |

#### `ExtraPostingSettlements_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ExtraPostingSettlements_LaterSettlements_T_SelectTaxDetailsByExtraPostingId` | T |  |
| `ExtraPostingSettlements_LaterSettlements_T_SelectToSettle` | T |  |
| `ExtraPostingSettlements_LaterSettlements_T_Settle` | T |  |

#### `Folio_*` — 15

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Folio_PostUnbilled_POS_Bills` | · |  |
| `Folio_T_CalculateTaxTaxGroupWise` | T |  |
| `Folio_T_Group_RoomToRoomTransfer` | T |  |
| `Folio_T_ItemSplit` | T |  |
| `Folio_T_ItemSplit_BeforePublishOn20240221` | T |  |
| `Folio_T_LineItemRoomToRoomTransfer` | T |  |
| `Folio_T_RoomToRoomTransfer` | T |  |
| `Folio_T_RoomToRoomTransfer_Back2024_12_20` | T |  |
| `Folio_T_RoomToRoomTransfer_Back20250210` | T |  |
| `Folio_T_RoomToRoomTransfer_back20250717` | T |  |
| `Folio_T_RoomToRoomTransfer_Browns` | T |  |
| `Folio_T_RoomToRoomTransfer_Dev` | T | _backup/variant_ |
| `Folio_T_RoomToRoomTransferOLD` | T |  |
| `Folio_TaxDiffereceCorrection` | · |  |
| `Folio_U_CreateFolioHeaderIfNotExists` | · |  |

#### `FolioChargers_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `FolioChargers_T_Cancel_Discount` | T |  |
| `FolioChargers_T_Save_Discount` | T |  |
| `FolioChargers_T_Select` | T |  |
| `FolioChargers_T_Select_By_TransferedFolioId` | T |  |
| `FolioChargers_T_Select_ById` | T |  |
| `FolioChargers_T_Select_dev` | T |  |
| `FolioChargers_T_Select_For_Discount` | T |  |

#### `GL_*` — 94

| Stored procedure | Type | Notes |
|---|:--:|---|
| `GL_InsertGLPostings_Job` | · |  |
| `GL_POSTING_BAN_ADVANCE_RECEIVED_RESERVATION_CREDITCARD` | · |  |
| `GL_POSTING_BAN_ADVANCE_RECEIVED_RESERVATION_GENERAL` | · |  |
| `GL_POSTING_BAN_EXTRA_POSTINGS` | · |  |
| `GL_POSTING_BAN_FUNCTION_CHARGE` | · |  |
| `GL_POSTING_BAN_MAIN_BILL_SETTLEMENT` | · |  |
| `GL_POSTING_BAN_MAIN_BILL_SETTLEMENT_HISTORY` | · |  |
| `GL_POSTING_COMMON_SP` | · |  |
| `GL_POSTING_COMMON_SP_POST_BACKDATE` | · |  |
| `GL_POSTING_COMMON_SP_POST_BACKDATE_ALL_PROPERTIES` | · |  |
| `GL_POSTING_FE_RESTAURANT_COMPLEMENTARY` | · |  |
| `GL_POSTING_FE_RESTAURANT_COMPLEMENTARY_EXECUTIVE` | · |  |
| `GL_POSTING_FE_RESTAURANT_COMPLEMENTARY_GENERAL` | · |  |
| `GL_POSTING_FE_RESTAURANT_COMPLEMENTARY_GENERAL_OPT` | · | _backup/variant_ |
| `GL_POSTING_FE_RESTAURANT_COMPLEMENTARY_ITEMCATEGORY` | · |  |
| `GL_POSTING_FE_RESTAURANT_SALE` | · |  |
| `GL_POSTING_FE_RESTAURANT_SALE_CREDIT` | · |  |
| `GL_POSTING_FE_RESTAURANT_SALE_CREDIT_OPT` | · | _backup/variant_ |
| `GL_POSTING_FE_RESTAURANT_SALE_CREDITCARD` | · |  |
| `GL_POSTING_FE_RESTAURANT_SALE_CREDITCARD_OPT` | · | _backup/variant_ |
| `GL_POSTING_FE_RESTAURANT_SALE_GENERAL` | · |  |
| `GL_POSTING_FE_RESTAURANT_SALE_GENERAL_OPT` | · | _backup/variant_ |
| `GL_POSTING_FE_RESTAURANT_SALE_ITEMCATEGORY` | · |  |
| `GL_POSTING_FE_RESTAURANT_SALE_OPT` | · | _backup/variant_ |
| `GL_POSTING_FO_ADVANCE_CANCEL_MEAL_RESERVATION_CREDITCARD` | · |  |
| `GL_POSTING_FO_ADVANCE_CANCEL_MEAL_RESERVATION_CREDITCARD_OPT` | · | _backup/variant_ |
| `GL_POSTING_FO_ADVANCE_CANCEL_MEAL_RESERVATION_GENERAL` | · |  |
| `GL_POSTING_FO_ADVANCE_CANCEL_MEAL_RESERVATION_GENERAL_OPT` | · | _backup/variant_ |
| `GL_POSTING_FO_ADVANCE_RECEIVED` | · |  |
| `GL_POSTING_FO_ADVANCE_RECEIVED_INHOUSE` | · |  |
| `GL_POSTING_FO_ADVANCE_RECEIVED_INHOUSE_CREDITCARD` | · |  |
| `GL_POSTING_FO_ADVANCE_RECEIVED_INHOUSE_GENERAL` | · |  |
| `GL_POSTING_FO_ADVANCE_RECEIVED_MEAL_RESERVATION_CREDITCARD` | · |  |
| `GL_POSTING_FO_ADVANCE_RECEIVED_MEAL_RESERVATION_CREDITCARD_OPT` | · | _backup/variant_ |
| `GL_POSTING_FO_ADVANCE_RECEIVED_MEAL_RESERVATION_GENERAL` | · |  |
| `GL_POSTING_FO_ADVANCE_RECEIVED_MEAL_RESERVATION_GENERAL_OPT` | · | _backup/variant_ |
| `GL_POSTING_FO_ADVANCE_RECEIVED_RESERVATION` | · |  |
| `GL_POSTING_FO_ADVANCE_RECEIVED_RESERVATION_CREDITCARD` | · |  |
| `GL_POSTING_FO_ADVANCE_RECEIVED_RESERVATION_GENERAL` | · |  |
| `GL_POSTING_FO_ADVANCE_REFUND` | · |  |
| `GL_POSTING_FO_ADVANCE_REFUND_INHOUSE` | · |  |
| `GL_POSTING_FO_ADVANCE_REFUND_RESERVATION` | · |  |
| `GL_POSTING_FO_ADVANCE_TRANSFER` | · |  |
| `GL_POSTING_FO_CURRENCY_ENCASHMENT` | · |  |
| `GL_POSTING_FO_CURRENCY_ENCASHMENT_OPT` | · | _backup/variant_ |
| `GL_POSTING_FO_DISCOUNT` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_CREDITNOTE` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_CREDITNOTE_LINEITEM` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_CREDITNOTE_OPT` | · | _backup/variant_ |
| `GL_POSTING_FO_EXTRA_POSTINGS_DEBITNOTE` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_DEBITNOTE_LINEITEM` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_DEBITNOTE_OPT` | · | _backup/variant_ |
| `GL_POSTING_FO_EXTRA_POSTINGS_DISCOUNT` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_REBATE` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_SALE` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_SALE_CREDIT` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_SALE_CREDITCARD` | · |  |
| `GL_POSTING_FO_EXTRA_POSTINGS_SALE_GENERAL` | · |  |
| `GL_POSTING_FO_MAIN_BILL_SETTLEMENT` | · |  |
| `GL_POSTING_FO_MISC_SALE` | · |  |
| `GL_POSTING_FO_MISC_SETTLEMENT` | · |  |
| `GL_POSTING_FO_REBATE` | · |  |
| `GL_POSTING_FO_REGEN_ROOM_CHARGE` | · |  |
| `GL_POSTING_FO_ROOM_CHARGE` | · |  |
| `GL_POSTING_FO_ROOM_CHARGE_ROOMCATEGORY` | · |  |
| `GL_POSTING_FO_SALE` | · |  |
| `GL_POSTING_FO_SETTLEMENT` | · |  |
| `GL_POSTING_INSERT_SP` | · |  |
| `GL_POSTING_INVENTORY_KITCHEN_ISSUE_POST` | · |  |
| `GL_POSTING_NEW_COMMON_SP` | · | _backup/variant_ |
| `GL_POSTING_NEW_COMMON_SP_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_ROOM_ADVANCE` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_ROOM_ADVANCE_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_ROOM_ADVANCE_REFUND` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_ROOM_ADVANCE_REFUND_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_ROOM_ADVANCE_TRANSFER` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_ROOM_ADVANCE_TRANSFER_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SALE` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SALE_DISCOUNT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SALE_DISCOUNT_31052024` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SALE_DISCOUNT_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SALE_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SALE_REBATE` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SALE_REBATE_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SETTLEMENT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SETTLEMENT_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SETTLEMENT_REBATE` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_EXTRA_POSTINGS_SETTLEMENT_REBATE_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_MAIN_BILL_SETTLEMENT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_MAIN_BILL_SETTLEMENT_OPT` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_ROOM_CHARGE` | · | _backup/variant_ |
| `GL_POSTING_NEW_FO_ROOM_CHARGE_OPT` | · | _backup/variant_ |
| `GL_POSTING_ReSPCall` | · |  |

#### `ModuleCategories_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ModuleCategories_M_Delete` | M |  |
| `ModuleCategories_M_Save` | M |  |
| `ModuleCategories_M_Select` | M |  |
| `ModuleCategories_M_Select_ById` | M |  |
| `ModuleCategories_M_Select_ForGrid` | M |  |

#### `OnlineAdvancePayment_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `OnlineAdvancePayment_Delete` | · |  |
| `OnlineAdvancePayment_Insert` | · |  |
| `OnlineAdvancePayment_Select` | · |  |
| `OnlineAdvancePayment_SelectBy_Uuid` | · |  |
| `OnlineAdvancePayment_SelectLink_ForEmail` | · |  |

#### `PaymentTypes_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PaymentTypes_M_Delete` | M |  |
| `PaymentTypes_M_Save` | M |  |
| `PaymentTypes_M_Select` | M |  |

#### `Posting_*` — 10

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Posting_Bill_Advance_Copy` | · |  |
| `Posting_Bill_Payments` | · |  |
| `Posting_Bill_Payments_Advance_Copy` | · |  |
| `Posting_Bill_Preview` | · |  |
| `Posting_Bill_Preview_06102025` | · | _backup/variant_ |
| `Posting_BillType_T_Select` | T |  |
| `Posting_InHouse_T_Save` | T |  |
| `Posting_SelectDocumentNos` | · |  |
| `Posting_Taxes_Bill` | · |  |
| `Posting_WalkIn_T_Save` | T |  |

#### `PostingCategories_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PostingCategories_M_Delete` | M |  |
| `PostingCategories_M_Save` | M |  |
| `PostingCategories_M_Select` | M |  |
| `PostingCategories_M_Select_ById` | M |  |
| `PostingCategories_M_Select_ForGrid` | M |  |

#### `PostingRhythms_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PostingRhythms_M_Select` | M |  |
| `PostingRhythms_M_Select_ById` | M |  |
| `PostingRhythms_M_Select_ForGrid` | M |  |

#### `PostingTypes_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PostingTypes_M_Delete` | M |  |
| `PostingTypes_M_Save` | M |  |
| `PostingTypes_M_Select` | M |  |
| `PostingTypes_M_Select_ById` | M |  |
| `PostingTypes_M_Select_ForGrid` | M |  |
| `PostingTypes_Price_T_Select` | T |  |

#### `Save_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Save_Folio` | · |  |
| `Save_Folio_DEV` | · |  |
| `Save_Folio_Test` | · | _backup/variant_ |
| `Save_Folio_TestTest` | · | _backup/variant_ |
| `Save_MultipleFolio` | · |  |
| `Save_TaxRemoval` | · |  |

#### `Select_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Select_FolioTotal` | · |  |
| `Select_LaundryInvoiceTaxes` | · |  |
| `Select_M_TaxGroupDetails` | M |  |
| `Select_MembersToSettleBills` | · |  |
| `Select_PaymentType_For_CompanySettlement` | · |  |
| `Select_ProfitCenterInvoiceTaxes` | · |  |

#### `TaxGroupDetails_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `TaxGroupDetails_M_Delete` | M |  |
| `TaxGroupDetails_M_Save` | M |  |
| `TaxGroupDetails_M_Select` | M |  |
| `TaxGroupDetails_M_Select_ById` | M |  |

#### `TaxGroups_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `TaxGroups_M_Delete` | M |  |
| `TaxGroups_M_Save` | M |  |
| `TaxGroups_M_Select` | M |  |
| `TaxGroups_M_Select_ById` | M |  |
| `TaxGroups_M_Select_ForGrid` | M |  |

#### `TaxTypes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `TaxTypes_M_Delete` | M |  |
| `TaxTypes_M_Save` | M |  |
| `TaxTypes_M_Select` | M |  |
| `TaxTypes_M_Select_ById` | M |  |
| `TaxTypes_M_Select_ForGrid` | M |  |

#### Other Cashiering, Folio & Day-End procedures — 74

| Stored procedure | Type | Notes |
|---|:--:|---|
| `AccountCodes_M_Select` | M |  |
| `AdvancedPyment_Charges_T_Select` | T |  |
| `AdvanceRequestOnlinePaymentSelect_DetailsBy_ReservationId` | · |  |
| `AdvanceRequestOnlinePaymentSelect_DetailsBy_ReservationId_2024_01_11` | · | _backup/variant_ |
| `AdvanceRequestOnlineRespond_T_SelectByUuid` | T |  |
| `AdvanceRequestRespondtOnline_T_SendEmail` | T |  |
| `BillPaymentLKR_T_Update` | T |  |
| `CalculateFolioChargersToBillInFC` | · |  |
| `CheckAvailableFolioNumber_T_Select_ByID` | T |  |
| `CreateInvoiceJson_Bridge` | · |  |
| `CreateInvoiceJson_Bridge_New` | · | _backup/variant_ |
| `CreditAndDebitNotes_SelectDocumentNos` | · |  |
| `CreditAndDebitNotesDetails_M_Save` | M |  |
| `CreditAndDebitNotesDetails_M_SelectByResHeaderId` | M |  |
| `CreditNote_R_SelectForReport` | R |  |
| `CreditNote_R_SelectTaxForReport` | R |  |
| `CreditNotes_T_Save` | T |  |
| `CurrencyEncashment_M_Save` | M |  |
| `CurrencyEncashment_T_SelectToVoid` | T |  |
| `CurrencyEncashmentVoid_T_Save` | T |  |
| `DayEndCurrencyConversion_M_Save` | M |  |
| `DayEndRoomRateVerify_T_Save` | T |  |
| `DebitNotes_T_Save` | T |  |
| `DowntimeReportPendingFoliosSchedules_T_4hoursTimeLapseEmailSends` | T |  |
| `FolioDetails_T_Select_ById` | T |  |
| `FolioDiscount_T_Update` | T |  |
| `FolioHeader_T_Select_ByIncoiveNo` | T |  |
| `FolioInvoice_T_ChangeGuestAndCompanyName` | T |  |
| `FolioManagement_InhouseGuestDetails_SelectByReservationHeaderId` | · |  |
| `FolioManagement_InhouseReservationDetails_SelectByReservationHeaderId` | · |  |
| `FolioManagementSideButtons_Select` | · |  |
| `FolioNoExchange_T_Update` | T |  |
| `FolioNumberChange_T_Update` | T |  |
| `FolioNumbers_T_Select_ById` | T |  |
| `FolioSettlementPayments_T_Select` | T |  |
| `FolioSplit_T_Update` | T |  |
| `FolioSplit_T_Update_BeforePublishOn20240221` | T |  |
| `FolioToBill` | · |  |
| `Get_CurrentDayEnd` | · |  |
| `GetOriginal_PostingAmount` | · |  |
| `inhouseReservation_Advancepayment_T_Select` | T |  |
| `Insert_Folio` | · |  |
| `Insert_Folio_Back20241021` | · |  |
| `Invoice_Print_Copy` | · |  |
| `InvoiceDetails_M_SelectForCheckedOutReservations` | M |  |
| `InvoiceNo_T_Select` | T |  |
| `ModuleCategoryWiseItem_M_Select` | M |  |
| `ModuleCategoryWiseItem_M_Select_ById` | M |  |
| `ModuleCategoryWiseItems_M_Save` | M |  |
| `ModuleCategoryWiseItems_M_Select_ForGrid` | M |  |
| `ModuleCategoryWiseTXN_T_Save` | T |  |
| `OnlineAdvancePaymentLink_Payment_Update` | · |  |
| `PaymentGatewaySettings_W_SelectByPropertyId` | W |  |
| `PaymentType_M_Select_for_sync_Oulets` | M |  |
| `PostingRhythm_M_Save` | M |  |
| `PostingRhythm_M_Select_ById` | M |  |
| `PostingRythms_M_Delete` | M |  |
| `PostingRythms_M_Save` | M |  |
| `PostingSettingCategories_M_Save` | M |  |
| `PostingSettingsChargeCodes_M_Select` | M |  |
| `PostingTypewiseCurrency_M_SelecyById` | M |  |
| `ProfitCenterWiseItemCategory_M_Select_ForCombo` | M |  |
| `SelectFolioHeaderHistory` | · | _backup/variant_ |
| `SettledFolioNumbers_T_Select_ById` | T |  |
| `SettledFolios_T_Select_ById` | T |  |
| `SettledFoliosNoList_T_Select_ById` | T |  |
| `TaxCalculations` | · |  |
| `TaxCalculations_Decimal2` | · |  |
| `TaxRemovalPolicies_M_Select` | M |  |
| `TaxUpdate_PlusPlus` | · |  |
| `ValidateExtraPostingGLMappings` | · |  |
| `VoidExtraPosting_Bill_Preview` | · |  |
| `VoidExtraPosting_T_Select_CurrentDate` | T |  |
| `VoidSettledFolios_T_Update` | T |  |

## F&B / Profit Centres — 81 stored procedures

*Outlets/profit centres and posting their sales to guest folios.*  ·  Detail: [07-fnb-and-outlet-process.md](07-fnb-and-outlet-process.md)

#### `ComboItemBreakDown_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ComboItemBreakDown_M_Delete` | M |  |
| `ComboItemBreakDown_M_Save` | M |  |
| `ComboItemBreakDown_M_Select` | M |  |

#### `KDSCategory_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `KDSCategory_M_Delete` | M |  |
| `KDSCategory_M_Save` | M |  |
| `KDSCategory_M_Select` | M |  |

#### `POS_*` — 13

| Stored procedure | Type | Notes |
|---|:--:|---|
| `POS_RoomListArrivals` | · |  |
| `POS_RoomListDepartures` | · |  |
| `POS_RoomListStayOvers` | · |  |
| `POS_spGetMealReservationList` | · |  |
| `POS_spGetRoomCategories` | · |  |
| `POS_spGetRoomDetails` | · |  |
| `POS_spGetRoomDetails_20260116` | · | _backup/variant_ |
| `POS_spGetRoomList` | · |  |
| `POS_spGetRoomList_20260116` | · | _backup/variant_ |
| `POS_spGetRoomPostingDocNo` | · |  |
| `POS_spGetTravelAgent` | · |  |
| `POS_spGetTravelAgents` | · |  |
| `POS_spInsertRoomPosting` | · |  |

#### `ProfitCenter_*` — 14

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ProfitCenter_ChargeType_Select` | · |  |
| `ProfitCenter_InvoiceNumber_Select` | · |  |
| `ProfitCenter_ItemCategories_M_Select_ByProfitCenterId` | M |  |
| `ProfitCenter_ItemCategoryWiseTypeWisePrcing_M_Select` | M |  |
| `ProfitCenter_ItemPriceTypes_M_Select` | M |  |
| `ProfitCenter_ItemWiseCategoryWiseChargeTypeWisePricing_M_SelectByItemId` | M |  |
| `ProfitCenter_M_Delete` | M |  |
| `ProfitCenter_M_Save` | M |  |
| `ProfitCenter_M_Select` | M |  |
| `ProfitCenter_M_Select_ById` | M |  |
| `ProfitCenter_M_Select_ForCombo` | M |  |
| `ProfitCenter_M_Select_ForGrid` | M |  |
| `ProfitCenter_Posting_Bill_Preview` | · |  |
| `ProfitCenter_TaxCalculations` | · |  |

#### `ProfitCenterChargeTypes_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ProfitCenterChargeTypes_M_Delete` | M |  |
| `ProfitCenterChargeTypes_M_Save` | M |  |
| `ProfitCenterChargeTypes_M_Select` | M |  |
| `ProfitCenterChargeTypes_M_Select_ByCategoryId` | M |  |
| `ProfitCenterChargeTypes_M_Select_ById` | M |  |
| `ProfitCenterChargeTypes_M_Select_ByProfitCenterId` | M |  |
| `ProfitCenterChargeTypes_M_Select_ForGrid` | M |  |

#### `ProfitCenterItemCategories_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ProfitCenterItemCategories_M_Delete` | M |  |
| `ProfitCenterItemCategories_M_Save` | M |  |
| `ProfitCenterItemCategories_M_Select` | M |  |
| `ProfitCenterItemCategories_M_Select_ById` | M |  |
| `ProfitCenterItemCategories_M_Select_ForGrid` | M |  |
| `ProfitCenterItemCategories_SelectIdByCategory` | · |  |

#### `ProfitCenterItems_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ProfitCenterItems_M_Delete` | M |  |
| `ProfitCenterItems_M_Save` | M |  |
| `ProfitCenterItems_M_Select` | M |  |
| `ProfitCenterItems_M_Select_ById` | M |  |
| `ProfitCenterItems_M_Select_ByProfitCenterId` | M |  |
| `ProfitCenterItems_M_Select_ForCombo` | M |  |
| `ProfitCenterItems_M_Select_ForGrid` | M |  |

#### `ProfitCenterPatterns_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ProfitCenterPatterns_M_Delete` | M |  |
| `ProfitCenterPatterns_M_Save` | M |  |
| `ProfitCenterPatterns_M_Select` | M |  |
| `ProfitCenterPatterns_M_Select_ById` | M |  |
| `ProfitCenterPatterns_M_Select_ForGrid` | M |  |

#### `RecipeHeader_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RecipeHeader_M_Save` | M |  |
| `RecipeHeader_M_Select` | M |  |
| `RecipeHeader_M_SelectBy_RecipeCode` | M |  |

#### Other F&B / Profit Centres procedures — 20

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ComboSetup_M_Save` | M |  |
| `ComboSetup_Select_for_sync` | · |  |
| `MenuItem_Select_By_ID` | · |  |
| `MenuItemAlternatives_Select_for_sync` | · |  |
| `MenuItemModifiers_Select_for_sync` | · |  |
| `MenuItems_M_Select` | M |  |
| `MenuItemWiseModifiers_M_Save` | M |  |
| `MenuItemWiseModifiers_M_Select` | M |  |
| `PosItemTypes_M_Delete` | M |  |
| `PosItemTypes_M_Save` | M |  |
| `POSItemTypes_M_Select` | M |  |
| `ProfitCenterItemCategoryWiseItem_M_Select_ForCombo` | M |  |
| `ProfitCenterItemPriceTypes_M_Select` | M |  |
| `ProfitCenterReport_Image_Select` | · |  |
| `ProfitCentertemChargeTypeWisePrice_M_Select` | M |  |
| `ProfitcenterWisePosting_M_Save` | M |  |
| `RecipeDetails_M_Save` | M |  |
| `RecipeDetails_M_SelectBy_RecipeCode` | M |  |
| `Select_ProfitCenterInvoicePayments` | · |  |
| `StockLocations_M_Select` | M |  |

## Spa & Meal Reservations — 34 stored procedures

*Spa and meal reservations and their scheduling/posting.*  ·  Detail: [01-complete-hotel-process.md](01-complete-hotel-process.md)

#### `MealPlans_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `MealPlans_M_Delete` | M |  |
| `MealPlans_M_Save` | M |  |
| `MealPlans_M_Select` | M |  |
| `MealPlans_M_Select_ById` | M |  |
| `MealPlans_M_Select_ForGrid` | M |  |
| `MealPlans_M_SelectForAddRoom` | M |  |
| `MealPlans_M_SelectForAvailability` | M |  |

#### `MealReservation_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `MealReservation_T_AdvanceRequest_ExisitingPayments` | T |  |
| `MealReservation_T_AdvanceRequest_Save` | T |  |
| `MealReservation_T_AdvanceRequest_SelectByDocNo` | T |  |
| `MealReservation_T_AdvanceRequest_SelectByUuid` | T |  |
| `MealReservation_T_AdvanceRequest_Update` | T |  |

#### `MealReservations_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `MealReservations_T_Complete` | T |  |
| `MealReservations_T_Save` | T |  |
| `MealReservations_T_Select_ById` | T |  |
| `MealReservations_T_Select_ByReservationNo` | T |  |
| `MealReservations_T_Select_ForGrid` | T |  |
| `MealReservations_T_Select_Json` | T |  |
| `MealReservations_T_Update_Json` | T |  |

#### `MealReservationsAdvance_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `MealReservationsAdvance_T_Cancel` | T |  |
| `MealReservationsAdvance_T_Save` | T |  |
| `MealReservationsAdvance_T_Select` | T |  |
| `MealReservationsAdvance_T_Select_ById` | T |  |

#### `Meals_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Meals_M_Select` | M |  |
| `Meals_M_SelectForMealAllocation` | M |  |
| `Meals_M_SelectForMealAllocation_ByMealPlanId` | M |  |

#### `MealTimes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `MealTimes_M_Delete` | M |  |
| `MealTimes_M_Save` | M |  |
| `MealTimes_M_Select` | M |  |
| `MealTimes_M_Select_ById` | M |  |
| `MealTimes_M_Select_ForGrid` | M |  |

#### Other Spa & Meal Reservations procedures — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `MealPlanWiseArriveAndDepartureFor_M_SelectBy_MealPlanId` | M |  |
| `MealWiseRates_T_Save` | T |  |
| `MealWiseRates_T_Select` | T |  |

## Guest Portal — 268 stored procedures

*Guest self-service portal requests (housekeeping, laundry, services, complaints).*  ·  Detail: [02-front-office-process.md](02-front-office-process.md)

#### `GuestPortal_*` — 268

| Stored procedure | Type | Notes |
|---|:--:|---|
| `GuestPortal_A_AdvancePaymentPercentages_Select` | · |  |
| `GuestPortal_A_Allergies_Select` | · |  |
| `GuestPortal_A_DocumentCategories_Select` | · |  |
| `GuestPortal_A_DocumentProcessWiseDocument_Select` | · |  |
| `GuestPortal_A_ErrorLogs_Save` | · |  |
| `GuestPortal_A_ExtraPosting_BillType_Select` | · |  |
| `GuestPortal_A_FeedbackAnswers_Save` | · |  |
| `GuestPortal_A_FeedbackAnswers_Save_BeforeModify_Jetwing` | · |  |
| `GuestPortal_A_GuestComplaintActionTypes_Select` | · |  |
| `GuestPortal_A_GuestComplaints_Select` | · |  |
| `GuestPortal_A_GuestComplaints_Select_2025_10_15_Old` | · | _backup/variant_ |
| `GuestPortal_A_GuestComplaintWiseActions_ActivityLog` | · |  |
| `GuestPortal_A_GuestComplaintWiseActions_ActivityLog_20241010` | · | _backup/variant_ |
| `GuestPortal_A_GuestNotification_Select` | · |  |
| `GuestPortal_A_GuestNotification_Select_20241010` | · | _backup/variant_ |
| `GuestPortal_A_GuestNotification_WhatsApp_Select` | · |  |
| `GuestPortal_A_GuestNotification_WhatsApp_Update` | · |  |
| `GuestPortal_A_GuestNotifications_Save` | · |  |
| `GuestPortal_A_GuestNotifications_SendEmail` | · |  |
| `GuestPortal_A_GuestNotifications_SendEmail_Old` | · | _backup/variant_ |
| `GuestPortal_A_GuestService_Save` | · |  |
| `GuestPortal_A_GuestService_Select` | · |  |
| `GuestPortal_A_GuestServiceTypes_Select` | · |  |
| `GuestPortal_A_GuestServiceWiseActions_ActivityLog` | · |  |
| `GuestPortal_A_HK_AppNotifications_Save` | · |  |
| `GuestPortal_A_Laundry_Item_Select` | · |  |
| `GuestPortal_A_Laundry_ItemCategory_Select` | · |  |
| `GuestPortal_A_Laundry_ItemCategorywiseChargeTypewisePrice_Select` | · |  |
| `GuestPortal_A_Laundry_ItemCategorywiseChargeTypewisePrice_Select_Dev` | · | _backup/variant_ |
| `GuestPortal_A_Laundry_ItemCategorywiseChargeTypewisePrice_Select_Old` | · | _backup/variant_ |
| `GuestPortal_A_Laundry_ItemChargeTypeWisePrice_M_Select` | M |  |
| `GuestPortal_A_Laundry_LaundryChargeTypes_Select` | · |  |
| `GuestPortal_A_Laundry_Save` | · |  |
| `GuestPortal_A_Laundry_Save_Dev` | · | _backup/variant_ |
| `GuestPortal_A_Laundry_Select` | · |  |
| `GuestPortal_A_LaundryRequest_Save` | · |  |
| `GuestPortal_A_LaundryRequest_Save_Dev` | · | _backup/variant_ |
| `GuestPortal_A_Login_InStaySendEmail` | · |  |
| `GuestPortal_A_Login_InStaySendEmail_Old` | · | _backup/variant_ |
| `GuestPortal_A_Login_PostStaySendEmail` | · |  |
| `GuestPortal_A_Login_PostStaySendEmail_Old` | · | _backup/variant_ |
| `GuestPortal_A_Login_PreArrivalSendEmail` | · |  |
| `GuestPortal_A_Login_PreArrivalSendEmail_20250318` | · | _backup/variant_ |
| `GuestPortal_A_Login_PreArrivalSendEmail_DayEnd` | · |  |
| `GuestPortal_A_Login_PreArrivalSendEmail_Old` | · | _backup/variant_ |
| `GuestPortal_A_Login_PreArrivalSendEmail_TEST` | · |  |
| `GuestPortal_A_MainGuest_Select` | · |  |
| `GuestPortal_A_MealPlans_Select` | · |  |
| `GuestPortal_A_MealPreferences_Select` | · |  |
| `GuestPortal_A_Meals_Select` | · |  |
| `GuestPortal_A_MyStayLogin_Save` | · |  |
| `GuestPortal_A_MyStayLogin_Save_1` | · |  |
| `GuestPortal_A_MyStayLogin_Save_20250317` | · | _backup/variant_ |
| `GuestPortal_A_MyStayLogin_Save_Before_Add_AuditTrail` | · |  |
| `GuestPortal_A_MyStayLogin_Save_New` | · | _backup/variant_ |
| `GuestPortal_A_Notification_Save` | · |  |
| `GuestPortal_A_Notification_Save_Old` | · | _backup/variant_ |
| `GuestPortal_A_Posting_Save` | · |  |
| `GuestPortal_A_Posting_Select_PriceList` | · |  |
| `GuestPortal_A_PostingTypes_Price_T_Select` | T |  |
| `GuestPortal_A_QRRedirect_GetReservationByRoom` | · |  |
| `GuestPortal_A_QRReservationDetails` | · |  |
| `GuestPortal_A_RefillSessionByReservationHeaderId` | · |  |
| `GuestPortal_A_ReservationConfirmation_Image_Select` | · |  |
| `GuestPortal_A_ReservationConfirmation_PreArrivalRequests_SelectById` | · |  |
| `GuestPortal_A_ReservationConfirmation_ReservationChargeDetails` | · |  |
| `GuestPortal_A_ReservationConfirmation_ReservationChargeDetails_1` | · |  |
| `GuestPortal_A_ReservationConfirmation_ReservationChargeDetails_20250317` | · | _backup/variant_ |
| `GuestPortal_A_ReservationConfirmation_SelectedPropertyDetails` | · |  |
| `GuestPortal_A_ReservationConfirmation_SelectedRoomDetails` | · |  |
| `GuestPortal_A_ReservationConfirmation_TermsAndCondition` | · |  |
| `GuestPortal_A_Reservations` | · |  |
| `GuestPortal_A_Reservations_20230517` | · | _backup/variant_ |
| `GuestPortal_A_Reservations_20241010` | · | _backup/variant_ |
| `GuestPortal_A_Reservations_beforegetemail` | · |  |
| `GuestPortal_A_Reservations_BeforeModify_Jetwing` | · |  |
| `GuestPortal_A_Reservations_BeforeModifyJetwing` | · |  |
| `GuestPortal_A_Reservations_Deb` | · |  |
| `GuestPortal_A_Reservations_NEW` | · | _backup/variant_ |
| `GuestPortal_A_ReservationWiseFolioSummary` | · |  |
| `GuestPortal_A_Roomcategories_Select` | · |  |
| `GuestPortal_A_RoomRequest_Save` | · |  |
| `GuestPortal_A_RoomRequest_Save_Dev` | · | _backup/variant_ |
| `GuestPortal_A_RoomRequest_Select` | · |  |
| `GuestPortal_A_RoomRequestActionTypes_Select` | · |  |
| `GuestPortal_A_RoomRequestWiseActions_ActivityLog` | · |  |
| `GuestPortal_A_RoomRequestWiseActions_ActivityLog_20241010` | · | _backup/variant_ |
| `GuestPortal_A_RoomTypes_Select` | · |  |
| `GuestPortal_A_Salutations_Select` | · |  |
| `GuestPortal_A_SavePOSOrder` | · |  |
| `GuestPortal_A_Select_HotelPromotions` | · |  |
| `GuestPortal_A_SelectFeedbackCategories` | · |  |
| `GuestPortal_A_SelectFeedbackQuestionTypes` | · |  |
| `GuestPortal_A_SelectFeedbackRates` | · |  |
| `GuestPortal_A_SelectFolioDetails` | · |  |
| `GuestPortal_A_SelectFolioNos` | · |  |
| `GuestPortal_A_SelectFolioWiseTax` | · |  |
| `GuestPortal_A_SelectLaundryRequest` | · |  |
| `GuestPortal_A_SelectLoggedPropery` | · |  |
| `GuestPortal_A_SelectPages` | · |  |
| `GuestPortal_A_SelectPOSCategories` | · |  |
| `GuestPortal_A_SelectPOSItemsByCategory` | · |  |
| `GuestPortal_A_SelectPOSItemsWiseImages` | · |  |
| `GuestPortal_A_SelectPOSOrder` | · |  |
| `GuestPortal_A_SelectPOSOrder_Old` | · | _backup/variant_ |
| `GuestPortal_A_SelectRoomRequest` | · |  |
| `GuestPortal_A_SendEmail` | · |  |
| `GuestPortal_A_SendEmail_FolioInvoice` | · |  |
| `GuestPortal_A_SendFolioInvoice_ChangedName_20231015` | · | _backup/variant_ |
| `GuestPortal_A_ServiceInformation_Select` | · |  |
| `GuestPortal_A_Sharer_DeleteById` | · |  |
| `GuestPortal_A_Sharer_Select` | · |  |
| `GuestPortal_A_Sharer_SelectById` | · |  |
| `GuestPortal_A_StayChangeRequest_Save` | · |  |
| `GuestPortal_A_StayChangeRequest_Select` | · |  |
| `GuestPortal_A_StayChangeWiseActions_ActivityLog` | · |  |
| `GuestPortal_A_StayChangeWiseActions_ActivityLog_20241010` | · | _backup/variant_ |
| `GuestPortal_A_TermsAndCondition` | · |  |
| `GuestPortal_A_Transports_BookingSummary_RoomDetails_Select` | · |  |
| `GuestPortal_A_Transports_BookingSummary_RoomDetails_Select_1` | · |  |
| `GuestPortal_A_Transports_Save` | · |  |
| `GuestPortal_A_Transports_Save_dev_2026_01_12` | · | _backup/variant_ |
| `GuestPortal_A_Transports_Save_OLD` | · | _backup/variant_ |
| `GuestPortal_A_Transports_Select` | · |  |
| `GuestPortal_A_Transports_Select_OLD` | · | _backup/variant_ |
| `GuestPortal_A_TransportsWiseActions_ActivityLog` | · |  |
| `GuestPortal_A_TransportsWiseActions_ActivityLog_20241010` | · | _backup/variant_ |
| `GuestPortal_A_TransportTypes_Select` | · |  |
| `GuestPortal_A_UpdatePOSOrder` | · |  |
| `GuestPortal_A_UpdatePOSOrderRequest` | · |  |
| `GuestPortal_A_UpdatePOSOrderStatus` | · |  |
| `GuestPortal_A_UserDetails_Update` | · |  |
| `GuestPortal_A_UserDetails_Update_1` | · |  |
| `GuestPortal_A_VerifyLogin` | · |  |
| `GuestPortal_A_VerifyLoginByEmail` | · |  |
| `GuestPortal_A_VerifyLoginByRoom` | · |  |
| `GuestPortal_A_VerifyLoginByUsername` | · |  |
| `GuestPortal_A_VerifyLoginByUuid` | · |  |
| `GuestPortal_A_VisitPlaces_Select` | · |  |
| `GuestPortal_A_WakeupCalls_Delete` | · |  |
| `GuestPortal_A_WakeupCalls_Save` | · |  |
| `GuestPortal_A_WakeupCalls_Select` | · |  |
| `GuestPortal_A_WakeupCallsWiseActions_ActivityLog` | · |  |
| `GuestPortal_API_EmailSend_Logs_Save` | · |  |
| `GuestPortal_API_EmailSettings_Select` | · |  |
| `GuestPortal_API_MobilePOSDocument_Save` | · |  |
| `GuestPortal_API_MobilePOSSendDocument_Logs_Save` | · |  |
| `GuestPortal_API_PropertySettings_Select` | · |  |
| `GuestPortal_FeedbackQuestionTypes_M_Delete` | M |  |
| `GuestPortal_FeedbackQuestionTypes_M_Save` | M |  |
| `GuestPortal_FeedbackQuestionTypes_M_Select` | M |  |
| `GuestPortal_FeedbackQuestionTypes_M_Select_ById` | M |  |
| `GuestPortal_FeedbackQuestionTypes_M_Select_ForGrid` | M |  |
| `GuestPortal_HotelPromotions_Delete` | · |  |
| `GuestPortal_HotelPromotions_Save` | · |  |
| `GuestPortal_HotelPromotions_SelectById` | · |  |
| `GuestPortal_LaundryDetails_M_DeleteById` | M |  |
| `GuestPortal_Logins_T_AuditTail_WriteToLog` | T |  |
| `GuestPortal_M_FeedbackCategories_Delete` | M |  |
| `GuestPortal_M_FeedbackCategories_ForCombo` | M |  |
| `GuestPortal_M_FeedbackCategories_Save` | M |  |
| `GuestPortal_M_FeedbackCategories_Select` | M |  |
| `GuestPortal_M_FeedbackCategories_SelectById` | M |  |
| `GuestPortal_M_FeedbackQuestionTypes_Delete` | M |  |
| `GuestPortal_M_FeedbackQuestionTypes_Save` | M |  |
| `GuestPortal_M_FeedbackQuestionTypes_SaveAdmin` | M |  |
| `GuestPortal_M_FeedbackQuestionTypes_Select` | M |  |
| `GuestPortal_M_FeedbackQuestionTypes_SelectById` | M |  |
| `GuestPortal_M_GroupReservation_Select` | M |  |
| `GuestPortal_M_GuestComplaints_Save` | M |  |
| `GuestPortal_M_GuestComplaints_Select` | M |  |
| `GuestPortal_M_GuestComplaintTypes_Select` | M |  |
| `GuestPortal_M_GuestComplaintTypes_Select_20241010` | M | _backup/variant_ |
| `GuestPortal_M_GuestNotification_Delete` | M |  |
| `GuestPortal_M_GuestNotification_Select` | M |  |
| `GuestPortal_M_GuestNotificationType_Select` | M |  |
| `GuestPortal_M_RequestType_Select` | M |  |
| `GuestPortal_M_RequestTypes_Delete` | M |  |
| `GuestPortal_M_RequestTypes_Save` | M |  |
| `GuestPortal_M_RequestTypes_SelectById` | M |  |
| `GuestPortal_M_SelectFeedbackQuestionTypes` | M |  |
| `GuestPortal_M_SendEmail` | M |  |
| `GuestPortal_M_SendEmail_FolioInvoice_2024_11_08` | M | _backup/variant_ |
| `GuestPortal_M_StayChangeRequest_Change` | M |  |
| `GuestPortal_M_StayChangeRequest_Save` | M |  |
| `GuestPortal_M_StayChangeRequest_Select_ForGrid` | M |  |
| `GuestPortal_Posting_BillType_T_Select` | T |  |
| `GuestPortal_Posting_M_DeleteById` | M |  |
| `GuestPortal_QRImageUrl_M_Save` | M |  |
| `GuestPortal_R_Report_FolioCharges_T_Select` | T |  |
| `GuestPortal_R_ReservationConfirmation_ReservationChargeDetails` | R |  |
| `GuestPortal_Save_VButlerInvitationToDeliver` | · |  |
| `GuestPortal_Select_EmailTemplateDetails` | · |  |
| `GuestPortal_SelectQR_ForAutoLogin` | · |  |
| `GuestPortal_T_AdvancePaymentRequests_Select` | T |  |
| `GuestPortal_T_AdvanceRequestOnline_Save` | T |  |
| `GuestPortal_T_AdvanceRequestOnline_SelectByUuid` | T |  |
| `GuestPortal_T_AdvanceRequestOnline_SelectRoomDetailsByUuid` | T |  |
| `GuestPortal_T_AdvanceRequestOnline_SendEmail` | T |  |
| `GuestPortal_T_AdvanceRequestOnlinePaymentSelect_DetailsBy_ReservationId` | T |  |
| `GuestPortal_T_PreArrivalRequests_SelectById` | T |  |
| `GuestPortal_T_QuickCheckInUpdate` | T |  |
| `GuestPortal_T_QuickCheckInValidation` | T |  |
| `GuestPortal_T_SaveOnlineTxn` | T |  |
| `GuestPortal_T_SaveOnlineTxn_20241010` | T | _backup/variant_ |
| `GuestPortal_T_SelectEmailDetails` | T |  |
| `GuestPortal_T_SelectFolioDetails` | T |  |
| `GuestPortal_T_SelectPaymentGateWaySettings` | T |  |
| `GuestPortal_T_SelectPaymentGateWaySettings_20241010` | T | _backup/variant_ |
| `GuestPortal_T_SettleBill` | T |  |
| `GuestPortal_T_SettleBill_2024_10_28` | T | _backup/variant_ |
| `GuestPortal_W_ActionTypes_Select` | W |  |
| `GuestPortal_W_AdvancePaymentRequests_Select` | W |  |
| `GuestPortal_W_Compliant_DashBoard` | W |  |
| `GuestPortal_W_Compliant_SelectBarChart` | W |  |
| `GuestPortal_W_Compliant_SelectDoughnutChart` | W |  |
| `GuestPortal_W_Compliant_SelectPieChart` | W |  |
| `GuestPortal_W_Feedback_Select_ForGrid` | W |  |
| `GuestPortal_W_Feedback_Select_ForGrid_OLD` | W | _backup/variant_ |
| `GuestPortal_W_Feedback_SelectBarChart` | W |  |
| `GuestPortal_W_Feedback_SelectDoughnutChart` | W |  |
| `GuestPortal_W_Feedback_SelectPieChart` | W |  |
| `GuestPortal_W_FeedbackActions_Save` | W |  |
| `GuestPortal_W_FeedbackActions_Select` | W |  |
| `GuestPortal_W_FeedbackActionTypes_Select` | W |  |
| `GuestPortal_W_FeedbackAnswers_Select` | W |  |
| `GuestPortal_W_FeedbackAnswers_Select_OLD` | W | _backup/variant_ |
| `GuestPortal_W_GRC_Save` | W |  |
| `GuestPortal_W_GuestComplaints_Select_ForGrid` | W |  |
| `GuestPortal_W_GuestComplaintTypes_Select` | W |  |
| `GuestPortal_W_GuestComplaintWiseActions_Save` | W |  |
| `GuestPortal_W_GuestNotifications_SendEmail` | W |  |
| `GuestPortal_W_GuestNotifications_SendEmail_20250317` | W | _backup/variant_ |
| `GuestPortal_W_GuestNotifications_SendEmail_Old` | W | _backup/variant_ |
| `GuestPortal_W_GuestProfiles_SelectByGuestProfileId` | W |  |
| `GuestPortal_W_GuestProfiles_Update` | W |  |
| `GuestPortal_W_GuestService_Select_ForGrid` | W |  |
| `GuestPortal_W_GuestTransports_Select_ForGrid` | W |  |
| `GuestPortal_W_GuestTransports_Select_ForGrid_20241010` | W | _backup/variant_ |
| `GuestPortal_W_HotelPromotion_Delete` | W |  |
| `GuestPortal_W_HotelPromotions_Save` | W |  |
| `GuestPortal_W_HotelPromotions_Select` | W |  |
| `GuestPortal_W_HotelPromotions_SelectById` | W |  |
| `GuestPortal_W_Logins_Save` | W |  |
| `GuestPortal_W_Preferences_SingleR_Update` | W |  |
| `GuestPortal_W_RequestTypes_Select` | W |  |
| `GuestPortal_W_RequestWiseActions_Save` | W |  |
| `GuestPortal_W_RequestWiseActions_Save_20241010` | W | _backup/variant_ |
| `GuestPortal_W_RequestWiseActions_Save_Old` | W | _backup/variant_ |
| `GuestPortal_W_RequestWiseActions_Save_old_2025_11_19` | W | _backup/variant_ |
| `GuestPortal_W_RequestWiseActions_Select` | W |  |
| `GuestPortal_W_RoomRequest_Select` | W |  |
| `GuestPortal_W_RoomRequest_Select_ForGrid` | W |  |
| `GuestPortal_W_RoomRequest_Select_ForGrid_20250319` | W | _backup/variant_ |
| `GuestPortal_W_RoomRequest_Select_ForGrid_Dev_2026_02_09` | W | _backup/variant_ |
| `GuestPortal_W_RoomRequest_Select_ForGrid_old` | W |  |
| `GuestPortal_W_RoomRequestWiseActions_Save` | W |  |
| `GuestPortal_W_Select_GuestNotification` | W |  |
| `GuestPortal_W_Select_HotelPromotions` | W |  |
| `GuestPortal_W_Select_Notification` | W |  |
| `GuestPortal_W_Select_VisitPlaces` | W |  |
| `GuestPortal_W_TransportActivity_Save` | W |  |
| `GuestPortal_W_Update_Notification` | W |  |
| `GuestPortal_W_VisitPlaces_Delete` | W |  |
| `GuestPortal_W_VisitPlaces_Save` | W |  |
| `GuestPortal_W_VisitPlaces_Select` | W |  |
| `GuestPortal_W_VisitPlaces_SelectById` | W |  |
| `GuestPortal_W_WakeupCalls_Select_ForGrid` | W |  |

## Administration & Configuration — 393 stored procedures

*Master/reference configuration used by every other module.*  ·  Detail: [08-admin-and-configuration-process.md](08-admin-and-configuration-process.md)

#### `BOBSegments_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `BOBSegments_M_Delete` | M |  |
| `BOBSegments_M_Save` | M |  |
| `BOBSegments_M_Select` | M |  |
| `BOBSegments_M_Select_ById` | M |  |
| `BOBSegments_M_Select_ForGrid` | M |  |

#### `BOBSegmentWisePMSSegments_*` — 9

| Stored procedure | Type | Notes |
|---|:--:|---|
| `BOBSegmentWisePMSSegments_M_Delete` | M |  |
| `BOBSegmentWisePMSSegments_M_Delete_ByBOBSegmentId` | M |  |
| `BOBSegmentWisePMSSegments_M_Save` | M |  |
| `BOBSegmentWisePMSSegments_M_Select` | M |  |
| `BOBSegmentWisePMSSegments_M_Select_ByBOBSegmentId` | M |  |
| `BOBSegmentWisePMSSegments_M_SelectForGrid` | M |  |
| `BOBSegmentWisePMSSegments_Select` | · |  |
| `BOBSegmentWisePMSSegments_Select_ByBOBSegmentId` | · |  |
| `BOBSegmentWisePMSSegments_SelectForGrid` | · |  |

#### `BookingSources_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `BookingSources_M_Delete` | M |  |
| `BookingSources_M_Save` | M |  |
| `BookingSources_M_Select` | M |  |
| `BookingSources_M_Select_ByCompanyId` | M |  |
| `BookingSources_M_Select_ById` | M |  |
| `BookingSources_M_Select_ForGrid` | M |  |

#### `CancellationPolicies_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CancellationPolicies_M_Delete` | M |  |
| `CancellationPolicies_M_Save` | M |  |
| `CancellationPolicies_M_Select` | M |  |
| `CancellationPolicies_M_Select_ById` | M |  |
| `CancellationPolicies_M_Select_ForGrid` | M |  |
| `CancellationPolicies_M_Select_ForIBE` | M |  |

#### `CommunicationTypes_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CommunicationTypes_M_Delete` | M |  |
| `CommunicationTypes_M_Save` | M |  |
| `CommunicationTypes_M_Select` | M |  |

#### `Companies_*` — 11

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Companies_M_ApproveById` | M |  |
| `Companies_M_ApproveById_back20260716` | M |  |
| `Companies_M_Delete` | M |  |
| `Companies_M_RejectById` | M |  |
| `Companies_M_Save` | M |  |
| `Companies_M_Save_BeforeApproval` | M |  |
| `Companies_M_Select` | M |  |
| `Companies_M_Select_Combo` | M |  |
| `Companies_M_Select_ForGrid` | M |  |
| `Companies_M_SelectApprovals` | M |  |
| `Companies_Select_ById` | · |  |

#### `Company_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Company_T_ActivityLog_Insert` | T |  |
| `Company_T_Select_ActivityLog` | T |  |
| `Company_T_Select_ActivityLog_back20260716` | T |  |
| `Company_T_Select_ActivityLog_BeforeModOn11082025` | T |  |
| `Company_T_Select_ActivityLog_dev` | T |  |

#### `CompanyProfileTypes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CompanyProfileTypes_M_Delete` | M |  |
| `CompanyProfileTypes_M_Save` | M |  |
| `CompanyProfileTypes_M_Select` | M |  |
| `CompanyProfileTypes_M_Select_ById` | M |  |
| `CompanyProfileTypes_M_Select_ForGrid` | M |  |

#### `CompanyWiseContacts_*` — 11

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CompanyWiseContacts_M_Delete` | M |  |
| `CompanyWiseContacts_M_DeleteAll` | M |  |
| `CompanyWiseContacts_M_Save` | M |  |
| `CompanyWiseContacts_M_SaveAll` | M |  |
| `CompanyWiseContacts_M_Select` | M |  |
| `CompanyWiseContacts_M_Select_ByCompany` | M |  |
| `CompanyWiseContacts_M_Select_ById` | M |  |
| `CompanyWiseContacts_M_Select_ByIdAll` | M |  |
| `CompanyWiseContacts_M_Select_ForGrid` | M |  |
| `CompanyWiseContacts_M_Select_ForGridAll` | M |  |
| `CompanyWiseContacts_M_SelectAll` | M |  |

#### `CompanyWiseMarkets_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CompanyWiseMarkets_M_Delete` | M |  |
| `CompanyWiseMarkets_M_Save` | M |  |
| `CompanyWiseMarkets_M_Select` | M |  |
| `CompanyWiseMarkets_M_Select_ByCompanyId` | M |  |
| `CompanyWiseMarkets_M_Select_ById` | M |  |
| `CompanyWiseMarkets_M_Select_ForGrid` | M |  |

#### `CompanyWiseRateCodes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CompanyWiseRateCodes_M_Save` | M |  |
| `CompanyWiseRateCodes_M_Select` | M |  |
| `CompanyWiseRateCodes_M_Select_ByCompanyId` | M |  |
| `CompanyWiseRateCodes_M_Select_ById` | M |  |
| `CompanyWiseRateCodes_M_Select_ForGrid` | M |  |

#### `CompanyWiseSegments_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CompanyWiseSegments_M_Delete` | M |  |
| `CompanyWiseSegments_M_Save` | M |  |
| `CompanyWiseSegments_M_Select` | M |  |
| `CompanyWiseSegments_M_Select_ByCompanyId` | M |  |
| `CompanyWiseSegments_M_Select_ById` | M |  |
| `CompanyWiseSegments_M_Select_ForGrid` | M |  |

#### `Countries_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Countries_M_Delete` | M |  |
| `Countries_M_Save` | M |  |
| `Countries_M_Select` | M |  |
| `Countries_M_Select_ById` | M |  |
| `Countries_M_Select_ForGrid` | M |  |

#### `CRM_*` — 84

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CRM_A_UpdateInvalidProfiles` | · |  |
| `CRM_Dashboard` | · |  |
| `CRM_DyanamicSearch` | · |  |
| `CRM_DyanamicSearch_OLD` | · | _backup/variant_ |
| `CRM_DyanamicSearch_TEST` | · |  |
| `CRM_GuestProfileGenderWise` | · |  |
| `CRM_GuestProfileNationalityWise` | · |  |
| `CRM_Select_Menues` | · |  |
| `CRM_SelectGuestProfileByNationalityId` | · |  |
| `CRM_SelectGuestProfileForRecentBirthdays` | · |  |
| `CRM_SelectGuestProfilesByNationality` | · |  |
| `CRM_SelectValidGuestProfiles` | · |  |
| `CRM_T_DeleteCampaign` | T |  |
| `CRM_T_DeleteEmailTemplate` | T |  |
| `CRM_T_EditEmailTemplateById` | T |  |
| `CRM_T_SaveCampaign` | T |  |
| `CRM_T_SaveEmailTemplate` | T |  |
| `CRM_T_SelectAgents` | T |  |
| `CRM_T_SelectAllGuestProfiles` | T |  |
| `CRM_T_SelectBillSettlements` | T |  |
| `CRM_T_SelectCampaignById` | T |  |
| `CRM_T_SelectCampaignByPropertyId` | T |  |
| `CRM_T_SelectCompleteGuestProfiles` | T |  |
| `CRM_T_SelectCountries` | T |  |
| `CRM_T_SelectCountryWiseProfileForChart` | T |  |
| `CRM_T_SelectCusomerProfilesByYearAndCountryCode` | T |  |
| `CRM_T_SelectCustomerDetailsById` | T |  |
| `CRM_T_SelectCustomerProfileByCountryCode` | T |  |
| `CRM_T_SelectCustomerProfileByCountryCode_Sumamry` | T |  |
| `CRM_T_SelectCustomerProfileByGenderId` | T |  |
| `CRM_T_SelectCustomerProfileByNationalityId` | T |  |
| `CRM_T_SelectCustomerProfileBySeason` | T |  |
| `CRM_T_SelectCustomerProfileBySeasonForChart` | T |  |
| `CRM_T_SelectCustomerProfileByVisitPurposeId` | T |  |
| `CRM_T_SelectCustomerProfileByYear` | T |  |
| `CRM_T_SelectCustomerProfileCountryWise` | T |  |
| `CRM_T_SelectCustomerProfilesByNationality` | T |  |
| `CRM_T_SelectCustomerProfilesByNationalityForChart` | T |  |
| `CRM_T_SelectCustomerProfilesByYearAndNationalityId` | T |  |
| `CRM_T_SelectDyanamicSearch` | T |  |
| `CRM_T_SelectEmailTemplateById` | T |  |
| `CRM_T_SelectEmailTemplateByPropertyId` | T |  |
| `CRM_T_SelectForDashboardStats` | T |  |
| `CRM_T_SelectGenderWiseCustomerProfiles` | T |  |
| `CRM_T_SelectGuestDetailsForSearch` | T |  |
| `CRM_T_SelectInCompleteCustomerProfileCountryWise` | T |  |
| `CRM_T_SelectInCompleteGuestProfiles` | T |  |
| `CRM_T_SelectMarkets` | T |  |
| `CRM_T_SelectMealPlans` | T |  |
| `CRM_T_SelectNationalities` | T |  |
| `CRM_T_SelectPackages` | T |  |
| `CRM_T_SelectProperties` | T |  |
| `CRM_T_SelectRateCodes` | T |  |
| `CRM_T_SelectRoomCategories` | T |  |
| `CRM_T_SelectRooms` | T |  |
| `CRM_T_SelectSalutations` | T |  |
| `CRM_T_SelectSegments` | T |  |
| `CRM_T_SelectVisitPurposes` | T |  |
| `CRM_T_SelectVisitPurposeWiseCustomerProfiles` | T |  |
| `CRM_W_Country_TypeWiseCountByCountryCode` | W |  |
| `CRM_W_Country_TypeWiseCountByYear` | W |  |
| `CRM_W_Country_TypeWiseProfilesByCountryCode` | W |  |
| `CRM_W_Country_TypeWiseProfilesByYear` | W |  |
| `CRM_W_DuplicateEmails_Count` | W |  |
| `CRM_W_DuplicateEmails_Profiles` | W |  |
| `CRM_W_Gender_TypeWiseCountByGenderCode` | W |  |
| `CRM_W_Gender_TypeWiseProfilesByGenderCode` | W |  |
| `CRM_W_GuestProfile_DetailsById` | W |  |
| `CRM_W_GuestProfile_Preference_Summary` | W |  |
| `CRM_W_GuestProfile_PropertyWiseCount` | W |  |
| `CRM_W_GuestProfile_Reservation_Summary` | W |  |
| `CRM_W_GuestProfile_SummaryById` | W |  |
| `CRM_W_GuestProfile_TypeWiseCount` | W |  |
| `CRM_W_GuestProfile_TypeWiseProfiles` | W |  |
| `CRM_W_GuestProfiles_ByPropertyCode` | W |  |
| `CRM_W_InvalidEmail_CountByError` | W |  |
| `CRM_W_MissingProfileInfo_Count` | W |  |
| `CRM_W_MissingProfileInfo_Profiles` | W |  |
| `CRM_W_Nationality_TypeWiseCountByNationalityCode` | W |  |
| `CRM_W_Nationality_TypeWiseProfilesByNationalityCode` | W |  |
| `CRM_W_Property_TypeWiseCountByPropertyCode` | W |  |
| `CRM_W_UpdateGuestProfileDetails` | W |  |
| `CRM_W_VisitPurpose_TypeWiseCountByVisitPurposeId` | W |  |
| `CRM_W_VisitPurpose_TypeWiseProfilesByVisitPurposeId` | W |  |

#### `Currencies_*` — 10

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Currencies_M_Delete` | M |  |
| `Currencies_M_Save` | M |  |
| `Currencies_M_Select` | M |  |
| `Currencies_M_Select_ById` | M |  |
| `Currencies_M_Select_ForGrid` | M |  |
| `Currencies_M_Select_IBEEnable` | M |  |
| `Currencies_M_SelectBaseCurrency` | M |  |
| `Currencies_M_SelectForMultiCurrencySettlement` | M |  |
| `Currencies_M_SelectIsSettlementEnable` | M |  |
| `Currencies_M_SelectRate` | M |  |

#### `CurrencyConversion_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CurrencyConversion_M_Delete` | M |  |
| `CurrencyConversion_M_Save` | M |  |
| `CurrencyConversion_M_Select` | M |  |
| `CurrencyConversion_M_Select_ById` | M |  |
| `CurrencyConversion_M_Select_ForGrid` | M |  |
| `CurrencyConversion_M_Select_ForPosting` | M |  |

#### `Departments_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Departments_M_Delete` | M |  |
| `Departments_M_Save` | M |  |
| `Departments_M_Select` | M |  |
| `Departments_M_Select_ById` | M |  |
| `Departments_M_Select_ForGrid` | M |  |

#### `Designations_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Designations_M_Delete` | M |  |
| `Designations_M_Save` | M |  |
| `Designations_M_Select` | M |  |
| `Designations_M_Select_ById` | M |  |
| `Designations_M_Select_ForGrid` | M |  |

#### `Employees_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Employees_M_Delete` | M |  |
| `Employees_M_Save` | M |  |
| `Employees_M_Select` | M |  |
| `Employees_M_Select_ById` | M |  |
| `Employees_M_Select_ForGrid` | M |  |

#### `ExtensionGroups_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ExtensionGroups_M_Delete` | M |  |
| `ExtensionGroups_M_Save` | M |  |
| `ExtensionGroups_M_Select` | M |  |
| `ExtensionGroups_M_Select_ById` | M |  |
| `ExtensionGroups_M_Select_ForGrid` | M |  |

#### `Extensions_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Extensions_M_Delete` | M |  |
| `Extensions_M_Save` | M |  |
| `Extensions_M_Select` | M |  |
| `Extensions_M_Select_ById` | M |  |
| `Extensions_M_Select_ForGrid` | M |  |

#### `FrontOfficeInventory_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `FrontOfficeInventory_Availability_Forecast` | · |  |
| `FrontOfficeInventory_M_Delete` | M |  |
| `FrontOfficeInventory_M_Save` | M |  |
| `FrontOfficeInventory_M_Search` | M |  |
| `FrontOfficeInventory_M_Select` | M |  |
| `FrontOfficeInventory_M_SelectById` | M |  |

#### `FrontOfficeRoomStatus_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `FrontOfficeRoomStatus_M_Delete` | M |  |
| `FrontOfficeRoomStatus_M_Save` | M |  |
| `FrontOfficeRoomStatus_M_Select` | M |  |
| `FrontOfficeRoomStatus_M_Select_ById` | M |  |
| `FrontOfficeRoomStatus_M_Select_ForGrid` | M |  |

#### `Genders_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Genders_M_Select` | M |  |
| `Genders_M_Select_ById` | M |  |
| `Genders_M_Select_ForGrid` | M |  |

#### `InventoryItems_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `InventoryItems_M_Delete` | M |  |
| `InventoryItems_M_Save` | M |  |
| `InventoryItems_M_Select` | M |  |
| `InventoryItems_M_Select_ById` | M |  |
| `InventoryItems_M_Select_ForGrid` | M |  |

#### `Languages_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Languages_M_Delete` | M |  |
| `Languages_M_Save` | M |  |
| `Languages_M_Select` | M |  |
| `Languages_M_Select_ById` | M |  |
| `Languages_M_Select_ForGrid` | M |  |

#### `LaundryChargeTypes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `LaundryChargeTypes_M_Delete` | M |  |
| `LaundryChargeTypes_M_Save` | M |  |
| `LaundryChargeTypes_M_Select` | M |  |
| `LaundryChargeTypes_M_Select_ById` | M |  |
| `LaundryChargeTypes_M_Select_ForGrid` | M |  |

#### `LaundryItemCategories_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `LaundryItemCategories_M_Delete` | M |  |
| `LaundryItemCategories_M_Save` | M |  |
| `LaundryItemCategories_M_Select` | M |  |
| `LaundryItemCategories_M_Select_ById` | M |  |
| `LaundryItemCategories_M_Select_ForGrid` | M |  |
| `LaundryItemCategories_SelectIdByCategory` | · |  |

#### `LaundryItems_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `LaundryItems_M_Delete` | M |  |
| `LaundryItems_M_Save` | M |  |
| `LaundryItems_M_Select` | M |  |
| `LaundryItems_M_Select_ById` | M |  |
| `LaundryItems_M_Select_ForGrid` | M |  |
| `LaundryItems_M_Select_ForPosting` | M |  |

#### `LaundryPatterns_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `LaundryPatterns_M_Delete` | M |  |
| `LaundryPatterns_M_Save` | M |  |
| `LaundryPatterns_M_Select` | M |  |
| `LaundryPatterns_M_Select_ById` | M |  |
| `LaundryPatterns_M_Select_ForGrid` | M |  |

#### `Markets_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Markets_M_Delete` | M |  |
| `Markets_M_Save` | M |  |
| `Markets_M_Select` | M |  |
| `Markets_M_Select_By_CompanyId` | M |  |
| `Markets_M_Select_ForGrid` | M |  |
| `Markets_M_SelectBy_Id` | M |  |

#### `Nationalities_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Nationalities_M_Delete` | M |  |
| `Nationalities_M_Save` | M |  |
| `Nationalities_M_Select` | M |  |
| `Nationalities_M_Select_ById` | M |  |
| `Nationalities_M_Select_ForGrid` | M |  |

#### `PaymentModes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PaymentModes_M_Delete` | M |  |
| `PaymentModes_M_Save` | M |  |
| `PaymentModes_M_Select` | M |  |
| `PaymentModes_M_Select_ById` | M |  |
| `PaymentModes_M_Select_ForGrid` | M |  |

#### `PMSSegments_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PMSSegments_BudgetAllocation_CopyFromPreviousMonth` | · |  |
| `PMSSegments_BudgetAllocation_Delete` | · |  |
| `PMSSegments_BudgetAllocation_Log_Select` | · |  |
| `PMSSegments_BudgetAllocation_Save` | · |  |
| `PMSSegments_BudgetAllocation_SelectForGrid` | · |  |
| `PMSSegments_BudgetAllocation_SelectForGrid_20260819` | · | _backup/variant_ |
| `PMSSegments_BudgetAllocation_SelectForGrid_WithBOBSegmentNames` | · |  |

#### `ProfileStatus_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ProfileStatus_M_Delete` | M |  |
| `ProfileStatus_M_Save` | M |  |
| `ProfileStatus_M_Select` | M |  |
| `ProfileStatus_M_Select_ById` | M |  |
| `ProfileStatus_M_Select_ForGrid` | M |  |

#### `Properties_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Properties_M_Delete` | M |  |
| `Properties_M_Save` | M |  |
| `Properties_M_Select` | M |  |
| `Properties_T_Select_ById` | T |  |

#### `Regions_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Regions_M_Delete` | M |  |
| `Regions_M_Save` | M |  |
| `Regions_M_Select` | M |  |
| `Regions_M_Select_ById` | M |  |

#### `SalesCallCategories_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `SalesCallCategories_M_Delete` | M |  |
| `SalesCallCategories_M_Save` | M |  |
| `SalesCallCategories_M_Select` | M |  |
| `SalesCallCategories_M_Select_ById` | M |  |
| `SalesCallCategories_M_Select_ForGrid` | M |  |

#### `Segments_*` — 9

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Segments_M_Delete` | M |  |
| `Segments_M_Save` | M |  |
| `Segments_M_Select` | M |  |
| `Segments_M_Select_ByCompanyId` | M |  |
| `Segments_M_Select_ByCompanyId_Stehani20230515` | M |  |
| `Segments_M_Select_ById` | M |  |
| `Segments_M_Select_ForGrid` | M |  |
| `Segments_M_SelectForBOBSegments` | M |  |
| `Segments_SelectForBOBSegments` | · |  |

#### `StaffCategory_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `StaffCategory_M_Delete` | M |  |
| `StaffCategory_M_Save` | M |  |
| `StaffCategory_M_Select` | M |  |
| `StaffCategory_M_Select_ById` | M |  |
| `StaffCategory_M_Select_ForGrid` | M |  |

#### `StaffDetails_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `StaffDetails_M_Delete` | M |  |
| `StaffDetails_M_Save` | M |  |
| `StaffDetails_M_Select` | M |  |
| `StaffDetails_M_Select_ById` | M |  |
| `StaffDetails_M_Select_ForGrid` | M |  |
| `StaffDetails_M_Select_ForReport` | M |  |
| `StaffDetails_M_Select_FrontOfficeOnly` | M |  |

#### `Staffs_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Staffs_M_Select_ByCategoryId` | M |  |
| `Staffs_M_Select_ByJobId` | M |  |
| `Staffs_M_Select_ByPreventiveMaintenanceSceduleId` | M |  |
| `Staffs_M_Select_ByStaffCategory` | M |  |
| `Staffs_Select_ByCode` | · |  |

#### `SubRegions_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `SubRegions_M_Delete` | M |  |
| `SubRegions_M_Save` | M |  |
| `SubRegions_M_Select` | M |  |
| `SubRegions_M_Select_ById` | M |  |

#### `TransferModes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `TransferModes_M_Delete` | M |  |
| `TransferModes_M_Save` | M |  |
| `TransferModes_M_Select` | M |  |
| `TransferModes_M_Select_ById` | M |  |
| `TransferModes_M_Select_ForGrid` | M |  |

#### `TransferTypes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `TransferTypes_M_Delete` | M |  |
| `TransferTypes_M_Save` | M |  |
| `TransferTypes_M_Select` | M |  |
| `TransferTypes_M_Select_ForGrid` | M |  |
| `TransferTypes_M_SelectBy_Id` | M |  |

#### `Transport_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Transport_For_Reservation` | · |  |
| `Transport_T_Delete` | T |  |
| `Transport_T_Save` | T |  |
| `Transport_T_SelectCategoryWise` | T |  |

#### `VIPLevels_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `VIPLevels_M_Delete` | M |  |
| `VIPLevels_M_Save` | M |  |
| `VIPLevels_M_Select` | M |  |
| `VIPLevels_M_Select_ById` | M |  |
| `VIPLevels_M_Select_ForGrid` | M |  |

#### `VisitPurposes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `VisitPurposes_M_Delete` | M |  |
| `VisitPurposes_M_Save` | M |  |
| `VisitPurposes_M_Select` | M |  |
| `VisitPurposes_M_Select_ById` | M |  |
| `VisitPurposes_M_Select_ForGrid` | M |  |

#### Other Administration & Configuration procedures — 44

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Attributes_M_Select` | M |  |
| `BOBSegmentWisePOSSegments_M_Save` | M |  |
| `BookingSettings_M_Select` | M |  |
| `BookingSettings_M_Update` | M |  |
| `CancellationReasons_M_Select` | M |  |
| `Colors_M_Select` | M |  |
| `Colors_M_Select_ById` | M |  |
| `CompanyCategories_M_Select` | M |  |
| `CompanyCategories_M_Select_ById` | M |  |
| `CompanyEmailTemplates_M_Select` | M |  |
| `CompanyWiseConversion_M_Select` | M |  |
| `CompanyWiseRates_T_Save` | T |  |
| `CompanyWiseRepersentative_M_Save` | M |  |
| `CompanyWiseRepresentative_M_Select` | M |  |
| `ComplimentaryReasons_M_Select_TypeWise` | M |  |
| `Currency_M_BaseCurrencySelect` | M |  |
| `CurrencyConversions_M_Save` | M |  |
| `CurrencyEncashement_T_Select` | T |  |
| `DepartmentWiseTraceEmail_T_Save` | T |  |
| `ExtensionGroup_M_Select_ComboBox` | M |  |
| `FOSettings_R_Select` | R |  |
| `FrontOfficeNotifications_M_Update` | M |  |
| `FrontOfficeSettings_M_Select` | M |  |
| `FrontOfficeSettings_M_Update` | M |  |
| `GuestPaymentModes_M_Select` | M |  |
| `Laundry_Posting_Bill_Preview` | · |  |
| `LaundryItemCategoryWiseTypeWisePrcing_M_Select` | M |  |
| `LaundryItemChargeTypeWisePrice_M_Select` | M |  |
| `LaundryItemPriceTypes_M_Select` | M |  |
| `LaundryWisePosting_M_Save` | M |  |
| `LaundryWisePosting_M_Save_Old` | M | _backup/variant_ |
| `Market_M_Select_ByRateCodeHeaderId` | M |  |
| `Property_M_Select` | M |  |
| `Property_T_Select_By_Prefix` | T |  |
| `PropertyGroup_M_Select` | M |  |
| `PropertyGroup_M_Select_UserWise` | M |  |
| `PropertyWisePaymentRequests_M_Save_Saas` | M |  |
| `PropertyWisePaymentResponse_M_Save_Saas` | M |  |
| `PropertyWisePaymentResponse_M_SelectByUuid_Saas` | M |  |
| `Salutations_M_Select` | M |  |
| `Salutations_M_Select_ById` | M |  |
| `TransferTypeWiseAttributes_T_Select_TransferTypeIdWise` | T |  |
| `TransportAttributes_M_Select` | M |  |
| `TransportAttributes_T_Select_TransportHeaderWise` | T |  |

## Users & Access — 42 stored procedures

*Users, roles, and page/report permissions (with the central SSO store).*  ·  Detail: [09-user-roles-and-permissions.md](09-user-roles-and-permissions.md)

#### `User_*` — 10

| Stored procedure | Type | Notes |
|---|:--:|---|
| `User_M_LoginVerify` | M |  |
| `User_M_ResetUserGuid` | M |  |
| `User_M_Save` | M |  |
| `User_M_Select` | M |  |
| `User_M_Select_ByCredentials` | M |  |
| `User_M_Select_ByUserName` | M |  |
| `User_M_Select_ByUserName_Saas` | M |  |
| `User_M_UpdateLoginGuid` | M |  |
| `User_M_UpdateLoginGuid_Saas` | M |  |
| `User_M_VerifyUserByGuid` | M |  |

#### `UserRoles_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `UserRoles_M_Delete` | M |  |
| `UserRoles_M_Save` | M |  |
| `UserRoles_M_Select` | M |  |
| `UserRoles_M_Select_ForGrid` | M |  |

#### `UserRoleWisePages_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `UserRoleWisePages_M_Save` | M |  |
| `UserRoleWisePages_M_Select` | M |  |
| `UserRoleWisePages_M_Select_ById` | M |  |

#### `UserWiseIndividualAccess_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `UserWiseIndividualAccess_M_Save` | M |  |
| `UserWiseIndividualAccess_M_Select` | M |  |
| `UserWiseIndividualAccess_M_Select_ById` | M |  |

#### `UserWiseRoles_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `UserWiseRoles_M_Save` | M |  |
| `UserWiseRoles_M_Select` | M |  |
| `UserWiseRoles_M_Select_ByUserId` | M |  |

#### Other Users & Access procedures — 19

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Central_UpdateNextDocNoWithUpdate` | · |  |
| `Central_User_M_Select_ByUserName` | M |  |
| `EditUserWiseApprovals` | · |  |
| `UserAccess_M_AccessPermission` | M |  |
| `UserAccessLog_T_Save` | T |  |
| `Users_M_Delete` | M |  |
| `Users_M_Select_ById` | M |  |
| `UserWiseIndividualReportAccess_M_Select_ByUrl` | M |  |
| `UserWiseProperties_M_Select` | M |  |
| `UserWiseProperty_M_Save` | M |  |
| `UserWiseProperty_M_Select_ByUserId` | M |  |
| `UserWiseQuickNavigationAreas_T_Save` | T |  |
| `UserWiseQuickNavigationAreas_T_Select` | T |  |
| `UserWiseQuickNavigationPages_T_Save` | T |  |
| `UserWiseQuickNavigationPages_T_Select_ById` | T |  |
| `UserWiseQuickNavigations_SelectForDashboard` | · |  |
| `UserWiseQuickNavigationsAreas_SelectForDashboard` | · |  |
| `UserWiseReportsAccess_M_Save` | M |  |
| `UserWiseReportsAccess_M_SelectPagesByUser` | M |  |

## Reporting & Analytics — 636 stored procedures

*Reporting and analytics/dashboard data sources.*  ·  Detail: [10-reports-and-business-information.md](10-reports-and-business-information.md)

#### `Analysis_*` — 9

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Analysis_DailyGuestRoomNights` | · |  |
| `Analysis_DailyOcupancy` | · |  |
| `Analysis_DailyRoomPickups` | · |  |
| `Analysis_GuestAnalysis` | · |  |
| `Analysis_GuestCountByCountry` | · |  |
| `Analysis_GuestNights` | · |  |
| `Analysis_MonthlyGuestRoomNights` | · |  |
| `Analysis_MonthlyRoomPickups` | · |  |
| `Analysis_RoomNight_GuestNightByCountry` | · |  |

#### `BIDashboard_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `BIDashboard_DailyIncomeFO` | · |  |
| `BIDashboard_DebtorsAgeAnalysis` | · |  |
| `BIDashboard_OntheBookFO` | · |  |

#### `Budget_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Budget_M_Delete` | M |  |
| `Budget_M_Save` | M |  |
| `Budget_M_Select` | M |  |
| `Budget_M_Select_ById` | M |  |
| `Budget_M_Select_ForGrid` | M |  |

#### `Dashboard_*` — 12

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Dashboard_AgentWiseRoomRevenue` | · |  |
| `Dashboard_OccupancyByRoomNights` | · |  |
| `Dashboard_OccupancyByRoomNights_Parameterized` | · |  |
| `Dashboard_OccupancyData` | · |  |
| `Dashboard_OccupancyData2` | · |  |
| `Dashboard_OccupancyData2_Parameterized` | · |  |
| `Dashboard_OccupancyData3` | · |  |
| `Dashboard_OccupancyData3_Parameterized` | · |  |
| `Dashboard_OccupancyData_Parameterized` | · |  |
| `Dashboard_Properties_M_Select` | M |  |
| `Dashboard_TypeWiseOccupancyDetails` | · |  |
| `Dashboard_TypeWiseOccupancyDetails_Parameterized` | · |  |

#### `DashboardAPI_*` — 193

| Stored procedure | Type | Notes |
|---|:--:|---|
| `DashboardAPI_AgentGuestNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_AgentRoomNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_AverageLengthOfStay_Select_Table` | · |  |
| `DashboardAPI_AverageLengthOfStayStatistic_Select_Table` | · |  |
| `DashboardAPI_AverageLengthOfStayStatistic_Select_Table_Copy` | · |  |
| `DashboardAPI_BeverageRevenueYear_Select` | · |  |
| `DashboardAPI_BeverageRevenueYear_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_CommonOccupancySummary_Select` | · |  |
| `DashboardAPI_CommonOccupancySummary_Select_Parameterized` | · |  |
| `DashboardAPI_CountryGuestNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_CountryRoomNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_DailyGuestMovementSummary_ForDashboardAPI_Chart` | · |  |
| `DashboardAPI_DashboardAPI_CommonFormat_M_Select` | M |  |
| `DashboardAPI_DashboardAPI_CommonFormat_M_SelectById` | M |  |
| `DashboardAPI_DashboardBeverageRevenue_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_DashboardFigures_Select` | · |  |
| `DashboardAPI_DashboardFigures_SelectForDisplay` | · |  |
| `DashboardAPI_DashboardFigures_SelectForDisplay_OLD` | · | _backup/variant_ |
| `DashboardAPI_DashboardFoodRevenue_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_DashboardRoomRevenue_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_DashboardTotalRevenue_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_DayArrivalsStayOversDepartures_Select` | · |  |
| `DashboardAPI_FoodCostAnalysis_Select_Dashboard_20240605` | · | _backup/variant_ |
| `DashboardAPI_FoodRevenueYear_Select` | · |  |
| `DashboardAPI_FoodRevenueYear_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_InformationSummaryDetails` | · |  |
| `DashboardAPI_InformationSummaryDetails_Select` | · |  |
| `DashboardAPI_InformationSummaryDetails_Select_Chart` | · |  |
| `DashboardAPI_MenuEngineeringMatrix_Dog_ForDashboardAPI_Chart_20240605` | · | _backup/variant_ |
| `DashboardAPI_MenuEngineeringMatrix_Dogs_ForDashboardAPI_Grid_20240605` | · | _backup/variant_ |
| `DashboardAPI_MenuEngineeringMatrix_Plowhorses_ForDashboardAPI_Chart_20240605` | · | _backup/variant_ |
| `DashboardAPI_MenuEngineeringMatrix_Plowhorses_ForDashboardAPI_Grid_20240605` | · | _backup/variant_ |
| `DashboardAPI_MenuEngineeringMatrix_Puzzles_ForDashboardAPI_Chart_20240605` | · | _backup/variant_ |
| `DashboardAPI_MenuEngineeringMatrix_Puzzles_ForDashboardAPI_Grid_20240605` | · | _backup/variant_ |
| `DashboardAPI_MenuEngineeringMatrix_Stars_ForDashboardAPI_Chart_20240605` | · | _backup/variant_ |
| `DashboardAPI_MenuEngineeringMatrix_Stars_ForDashboardAPI_Grid_20240605` | · | _backup/variant_ |
| `DashboardAPI_MonthlyADR_Select_Chart` | · |  |
| `DashboardAPI_MonthlyADR_Select_Chart_OLD` | · | _backup/variant_ |
| `DashboardAPI_MonthlyARR_Select` | · |  |
| `DashboardAPI_MonthlyARR_Select_Chart` | · |  |
| `DashboardAPI_MonthlyARR_Select_OLD` | · | _backup/variant_ |
| `DashboardAPI_MonthlyGOP_Select_Chart` | · |  |
| `DashboardAPI_MonthlyNOP_Select_Chart` | · |  |
| `DashboardAPI_MonthlyOccupancyData_ForDetailPage` | · |  |
| `DashboardAPI_MonthlyOccupancyData_ForDetailPage_Parameterized` | · |  |
| `DashboardAPI_MonthlyOccupancyData_ForDetailPage_Table` | · |  |
| `DashboardAPI_MonthlyOccupancyData_ForDetailPage_Table_Parameterized` | · |  |
| `DashboardAPI_MonthlyOutletSales_ForDashboardAPI_Chart_20240605` | · | _backup/variant_ |
| `DashboardAPI_MonthlyOutletSales_Select_Chart` | · |  |
| `DashboardAPI_MonthlyOutletSales_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_MonthlyOutletSalesAnalysis_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_MonthlyRevPACAnalysis_Select_Chart` | · |  |
| `DashboardAPI_MonthlyRevPARAnalysis_Select_Chart` | · |  |
| `DashboardAPI_MonthlyRevPARAnalysis_Select_Chart_OLD2` | · |  |
| `DashboardAPI_MonthlyRevPARAnalysis_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_NationalityGuestNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_NationalityRoomNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_OccupancyByRoomNights_Select` | · |  |
| `DashboardAPI_OccupancyByRoomNights_Select_Parameterized` | · |  |
| `DashboardAPI_OccupancyDaily_ForDashboardAPI_Chart` | · |  |
| `DashboardAPI_OccupancyDaily_ForDashboardAPI_Chart_Parameterized` | · |  |
| `DashboardAPI_OccupancyDaily_Select` | · |  |
| `DashboardAPI_OccupancyDaily_Select_Parameterized` | · |  |
| `DashboardAPI_OccupancyData_ForDashboardAPI_Chart` | · |  |
| `DashboardAPI_OccupancyData_ForDashboardAPI_Chart_Parameterized` | · |  |
| `DashboardAPI_OccupancyData_Select` | · |  |
| `DashboardAPI_OccupancyData_Select_Parameterized` | · |  |
| `DashboardAPI_OutletSalesAnalysis_OutletSalesMixChart_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_OutletSalesMix_Select_Chart` | · |  |
| `DashboardAPI_OutletSalesMix_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_OutletSalesMix_Select_Table` | · |  |
| `DashboardAPI_OutletWiseSales_Grid_20240605` | · | _backup/variant_ |
| `DashboardAPI_PaidvsComplimentaryRoomSummary_ForDashboardAPI_Chart` | · |  |
| `DashboardAPI_RateCodeGuestNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_RateCodeRoomNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_RevenueForecast_Select_Chart` | · |  |
| `DashboardAPI_RevenueForecast_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_RevenueForecast_Select_ForDetailPage_Table_Test` | · | _backup/variant_ |
| `DashboardAPI_RevenueManagement_MonthlyADRAnalysis_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_RevenueManagement_MonthlyARRAnalysis_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_RevenueManagement_MonthlyRevPACAnalysis_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_RevenueManagement_Select_Table` | · |  |
| `DashboardAPI_RevenueManagement_Select_Table_OLD` | · | _backup/variant_ |
| `DashboardAPI_RoomAvailability_Occupancy_Forecast` | · |  |
| `DashboardAPI_RoomAvailability_Occupancy_Forecast_Parameterized` | · |  |
| `DashboardAPI_RoomAvailability_Today_ArrivedStayOversDeparted` | · |  |
| `DashboardAPI_RoomCategoryGuestNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_RoomCategoryRoomNightsAnalysis_Select_Chart` | · |  |
| `DashboardAPI_RoomRevenueYear_Select` | · |  |
| `DashboardAPI_RoomRevenueYear_Select_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_AccomodationRevenueForPieChart` | · |  |
| `DashboardAPI_Select_AgentPerfomanceCardFigures` | · |  |
| `DashboardAPI_Select_AvarageLengthOfStayTableSummary` | · |  |
| `DashboardAPI_Select_AverageLengthOfStay` | · |  |
| `DashboardAPI_Select_AverageLengthOfStay_Chart` | · |  |
| `DashboardAPI_Select_AverageLengthOfStay_Chart_TEST2` | · |  |
| `DashboardAPI_Select_AverageLengthOfStay_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_AverageLengthOfStay_Table` | · |  |
| `DashboardAPI_Select_BeverageRevenues_ChartDashboard` | · |  |
| `DashboardAPI_Select_BeverageRevenues_ChartDashboard_OLD` | · | _backup/variant_ |
| `DashboardAPI_Select_CommonDetailsByPage` | · |  |
| `DashboardAPI_Select_CommonOccupancyAnalysisData_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_CommonOccupancyAnalysisData_ForDetailPage_Table_Parameterized` | · |  |
| `DashboardAPI_Select_CountryWiseInhouseGuestCount` | · |  |
| `DashboardAPI_Select_DailyRevenueAccomodationChart` | · |  |
| `DashboardAPI_Select_DailyRevenueFoodIncomeChart` | · |  |
| `DashboardAPI_Select_DailyRevenueOtherIncomeChart` | · |  |
| `DashboardAPI_Select_DailyRevenueReportCharts` | · |  |
| `DashboardAPI_Select_DailyRevenueReportCharts_Bar` | · |  |
| `DashboardAPI_Select_DailyRevenueReportCharts_Pie` | · |  |
| `DashboardAPI_Select_DailyRevenueReportCharts_Pie_ForAccomodation` | · |  |
| `DashboardAPI_Select_DailyRevenueReportCharts_Pie_ForFoodIncome` | · |  |
| `DashboardAPI_Select_F&BRevenues_Chart` | · |  |
| `DashboardAPI_Select_FoodCostingCardFigures` | · |  |
| `DashboardAPI_Select_FoodRevenues_ChartDashboard` | · |  |
| `DashboardAPI_Select_FoodRevenues_ChartDashboard_OLD` | · | _backup/variant_ |
| `DashboardAPI_Select_GOPNOPCardFigures` | · |  |
| `DashboardAPI_Select_GuestNightsForecast_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_GuestNightsStatistics_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_InhouseReservationDetailsByCountryId_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_LastTenDaysOccupancyStatistics_Chart` | · |  |
| `DashboardAPI_Select_LastTenDaysOccupancyStatistics_Chart_Parameterized` | · |  |
| `DashboardAPI_Select_LastTenDaysReservationStatisticsAndAvailableRooms_Chart` | · |  |
| `DashboardAPI_Select_LastTenDaysStatistics` | · |  |
| `DashboardAPI_Select_LastTenDaysStatistics_Chart` | · |  |
| `DashboardAPI_Select_Menues` | · |  |
| `DashboardAPI_Select_MonthlyARRAnalysis_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_MonthlyGuestNightsStatistics_Chart` | · |  |
| `DashboardAPI_Select_MonthlyOccupancyStatistics_Chart` | · |  |
| `DashboardAPI_Select_MonthlyOccupancyStatistics_Chart_Parameterized` | · |  |
| `DashboardAPI_Select_MonthlyOccupancyStatistics_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_MonthlyOccupancyStatistics_ForDetailPage_Table_Parameterized` | · |  |
| `DashboardAPI_Select_MonthlyOccupancyStatisticsForecast_Chart` | · |  |
| `DashboardAPI_Select_MonthlyOccupancyStatisticsForecast_Chart_` | · |  |
| `DashboardAPI_Select_MonthlyOccupancyStatisticsForecast_Chart_OLD` | · | _backup/variant_ |
| `DashboardAPI_Select_MonthlyOccupancyStatisticsForecast_Chart_Parameterized` | · |  |
| `DashboardAPI_Select_MonthlyOccupancyStatisticsForecast_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_MonthlyOccupancyStatisticsForecast_ForDetailPage_Table_Parameterized` | · |  |
| `DashboardAPI_Select_MonthlyRoomNightsStatistics_Chart` | · |  |
| `DashboardAPI_Select_NationalityPerfomanceCardFigures` | · |  |
| `DashboardAPI_Select_Next10DaysCardFigures` | · |  |
| `DashboardAPI_Select_Next10DaysCardFigures_OLD` | · | _backup/variant_ |
| `DashboardAPI_Select_NextTenDaysOccupancyStatistics_Chart` | · |  |
| `DashboardAPI_Select_NextTenDaysOccupancyStatistics_Chart_Parameterized` | · |  |
| `DashboardAPI_Select_NextTenDaysOccupancyStatistics_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_NextTenDaysOccupancyStatistics_ForDetailPage_Table_Parameterized` | · |  |
| `DashboardAPI_Select_NextTenDaysReservationStatisticsAndAvailableRooms_Chart` | · |  |
| `DashboardAPI_Select_NextTenDaysReservationStatisticsAndAvailableRooms_Chart_OLD` | · | _backup/variant_ |
| `DashboardAPI_Select_NextTenDaysReservationStatisticsAndAvailableRooms_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_NextTenDaysStatistics` | · |  |
| `DashboardAPI_Select_NextTenDaysStatistics_Chart` | · |  |
| `DashboardAPI_Select_NextTenDaysStatistics_Chart_OLD` | · | _backup/variant_ |
| `DashboardAPI_Select_NextTenDaysStatistics_COPY` | · |  |
| `DashboardAPI_Select_NextTenDaysStatistics_Table` | · |  |
| `DashboardAPI_Select_OccupancyStatistics` | · |  |
| `DashboardAPI_Select_OccupancyStatistics_Parameterized` | · |  |
| `DashboardAPI_Select_OccupancyStatisticsForecast` | · |  |
| `DashboardAPI_Select_OccupancyStatisticsForecast_Parameterized` | · |  |
| `DashboardAPI_Select_OtherRevenueForBarChart` | · |  |
| `DashboardAPI_Select_OtherRevenues_Chart` | · |  |
| `DashboardAPI_Select_OutletSales_Box_20240605` | · | _backup/variant_ |
| `DashboardAPI_Select_OutletSalesAnalysisCardFigures` | · |  |
| `DashboardAPI_Select_PaxDetails_20240605` | · | _backup/variant_ |
| `DashboardAPI_Select_PropertyOccupancyDetails` | · |  |
| `DashboardAPI_Select_PropertyOccupancyDetails_Parameterized` | · |  |
| `DashboardAPI_Select_RateCodePerfomanceCardFigures` | · |  |
| `DashboardAPI_Select_ReservationStatus_Chart` | · |  |
| `DashboardAPI_Select_ReservationStatus_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_RevenueAnalysisCardFigures` | · |  |
| `DashboardAPI_Select_RevenueAnalysisDashboardCardFigures` | · |  |
| `DashboardAPI_Select_RevenueAnalysisDashboardCardFigures_OLD` | · | _backup/variant_ |
| `DashboardAPI_Select_RevenueManagementCardFigures` | · |  |
| `DashboardAPI_Select_Revenues` | · |  |
| `DashboardAPI_Select_Revenues_Chart` | · |  |
| `DashboardAPI_Select_RoomNightsForecast_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_RoomNightsStatistics_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_RoomRevenues_Chart` | · |  |
| `DashboardAPI_Select_RoomRevenues_ChartDashboard` | · |  |
| `DashboardAPI_Select_RoomRevenues_ChartDashboard_OLD` | · | _backup/variant_ |
| `DashboardAPI_Select_TotalRevenueAnalysis_ForDetailPage_Table` | · |  |
| `DashboardAPI_Select_TotalRevenues_Chart` | · |  |
| `DashboardAPI_Select_TotalRevenues_ChartDashboard` | · |  |
| `DashboardAPI_Select_TotalRevenues_ChartDashboard_OLD` | · | _backup/variant_ |
| `DashboardAPI_Select_YeildManagementCardFigures` | · |  |
| `DashboardAPI_Select_YeildManagementCardFigures_OLD` | · | _backup/variant_ |
| `DashboardAPI_SelectGuestNightsForecast_Chart` | · |  |
| `DashboardAPI_SelectRoomNightsForecast_Chart` | · |  |
| `DashboardAPI_T_SelectCountries` | T |  |
| `DashboardAPI_TotalRevenueYear_Select` | · |  |
| `DashboardAPI_TotalRevenueYear_Select_Dashboard` | · |  |
| `DashboardAPI_TotalRevenueYear_Select_Dashboard_ForAllMonths` | · |  |
| `DashboardAPI_TotalRevenueYear_Select_Dashboard_OLD` | · | _backup/variant_ |
| `DashboardAPI_TotalRevenueYear_Select_ForDetailPage_Table` | · |  |

#### `Report_*` — 285

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Report_AccomodationJurnal` | · |  |
| `Report_AdvanceAndRefundWithOpeningBalance` | · |  |
| `Report_AgentPerformanceSummary` | · |  |
| `Report_AirportDropOff` | · |  |
| `Report_AirportPickup` | · |  |
| `Report_AirportPickupAndDropOff` | · |  |
| `Report_ARR_ADR_RevPar_Analysis` | · |  |
| `Report_ARR_ADR_RevPar_Analysis_New` | · | _backup/variant_ |
| `Report_BankDeposit` | · |  |
| `Report_BillingJurnal` | · |  |
| `Report_BillTypeWiseSales` | · |  |
| `Report_BookingSourceWiseMonthlyAverageOccupancy_WithAndWithoutComplimentaryRoomNights` | · |  |
| `Report_BookingSourceWiseMonthlyAverageOccupancy_WithAndWithoutComplimentaryRoomNights_Parameterized` | · |  |
| `Report_CashEncashment` | · |  |
| `Report_CashierReturnSales` | · |  |
| `Report_Common_Occupancy` | · |  |
| `Report_Common_Occupancy_ForReservation` | · |  |
| `Report_Common_Occupancy_ForReservation_Parameterized` | · |  |
| `Report_Common_Occupancy_Parameterized` | · |  |
| `Report_Common_ReservationDateWiseMealBreakdown` | · |  |
| `Report_Common_ReservationDateWiseMealBreakdown_20250813` | · | _backup/variant_ |
| `Report_Common_RoomStatusChart` | · |  |
| `Report_ComplementaryReservations` | · |  |
| `Report_CumulativeSalesOutletWise` | · |  |
| `Report_CumulativeSalesOutletWise_1` | · |  |
| `Report_CumulativeSummary` | · |  |
| `Report_CumulativeSummaryMonthy` | · |  |
| `Report_CumulativeSummaryYearly` | · |  |
| `Report_CumulativeSummaryYearly_1` | · |  |
| `Report_Currency_Encashment_Details` | · |  |
| `Report_Currency_Encashment_Details_Dev` | · | _backup/variant_ |
| `Report_Currency_Encashment_Receipt` | · |  |
| `Report_CurrencyConvertion` | · |  |
| `Report_CurrencyEncashment_CashierReturnSales` | · |  |
| `Report_DailyArrivalDetail` | · |  |
| `Report_DailyRevenueReport` | · |  |
| `Report_DailyRevenueReport_23032022` | · | _backup/variant_ |
| `Report_DailyRevenueReport_Summary` | · |  |
| `Report_DailyRevenueReport_Summary_Browns` | · |  |
| `Report_DailyRevenueReport_Summary_BudgetAllocation` | · |  |
| `Report_DailyRevenueReport_Summary_TEST` | · |  |
| `Report_DailyRevenueReport_ToCheckGLProcessed` | · |  |
| `Report_Damage_Request` | · |  |
| `Report_DateWise_AvarageLenghtOf_Stay` | · |  |
| `Report_DateWiseRoomTypeWiseReservationCount` | · |  |
| `Report_Day_End_Summary` | · |  |
| `Report_DayEndSummary_CashAndCrd` | · |  |
| `Report_DayEndSummary_EmptyDS` | · |  |
| `Report_DayWiseArrivalOrDepatureSummary` | · |  |
| `Report_DayWiseSalesSummary` | · |  |
| `Report_DeletedItems` | · | _backup/variant_ |
| `Report_Discount` | · |  |
| `Report_DiscountDetails` | · |  |
| `Report_DowntimeReport_PendingFolios` | · |  |
| `Report_FODiscount` | · |  |
| `Report_FolioCharges_T_Select` | T |  |
| `Report_FolioInvoicePayment` | · |  |
| `Report_FolioInvoicePayment_Coral` | · |  |
| `Report_FolioTransferDetails_AllTransactionDetails_ByDateRange` | · |  |
| `Report_FolioTransferDetails_AllTransactionDetails_ByDateRange_dev` | · |  |
| `Report_FolioTransferDetails_ByDateRange` | · |  |
| `Report_FolioTransferDetails_ByDateRange_dev` | · |  |
| `Report_FolioTransferDetails_ByReservation` | · |  |
| `Report_ForecastWeekly` | · |  |
| `Report_Get_GuestLedger` | · |  |
| `Report_GRN_Listing` | · |  |
| `Report_GrossFiguresAnalysis` | · |  |
| `Report_GroupGuest_Registration` | · |  |
| `Report_Guest_Profile_EmailList` | · |  |
| `Report_Guest_Profile_LastVisit` | · |  |
| `Report_Guest_Profile_List` | · |  |
| `Report_Guest_Registration` | · |  |
| `Report_GuestAllergies` | · |  |
| `Report_GuestAllergies_2026_01_05_Before_vButler_Onlive` | · | _backup/variant_ |
| `Report_GuestBalanceAnalysisShortFormat` | · |  |
| `Report_GuestDetails_BirthdayDetails` | · |  |
| `Report_GuestDetails_EmailContactList` | · |  |
| `Report_GuestDetails_VIP` | · |  |
| `Report_GuestDtl_BirthdayArrivalPending` | · |  |
| `Report_GuestinHouse_BirthdayDetails` | · |  |
| `Report_GuestinHouseDayuse` | · |  |
| `Report_GuestLedger` | · |  |
| `Report_GuestWiseMessages` | · |  |
| `Report_HalfHourlySales` | · |  |
| `Report_HourlySalesDayComp` | · |  |
| `Report_HourlySalesOutletComp` | · |  |
| `Report_HourlySalesSummary` | · |  |
| `Report_Housekeeping_RoomWiseRoomBoys` | · |  |
| `Report_Housekeeping_RoomWiseRoomBoys_Old` | · | _backup/variant_ |
| `Report_Housekeeping_RoomWiseRoomBoys_Old_2026_02_20` | · | _backup/variant_ |
| `Report_HouseKeepingStatus` | · |  |
| `Report_HouseKeepingStatus_20250828` | · | _backup/variant_ |
| `Report_Image_Select` | · |  |
| `Report_InformastionSheet_OccupancyCount` | · |  |
| `Report_InformastionSheet_OccupancyCount_20250813` | · | _backup/variant_ |
| `Report_InformastionSheet_OccupancyCount_Back20241016` | · |  |
| `Report_InformastionSheet_OccupancyCount_Parameterized` | · |  |
| `Report_Information_Sheet` | · |  |
| `Report_Information_Sheet_Header` | · |  |
| `Report_InformationSheet` | · |  |
| `Report_InformationSheet_Common` | · |  |
| `Report_InformationSheet_ConvertionRates` | · |  |
| `Report_InformationSheet_ConvertionRates_20250813` | · | _backup/variant_ |
| `Report_InformationSheet_Counts` | · |  |
| `Report_InformationSheet_DaysArrivals` | · |  |
| `Report_InformationSheet_DaysArrivals_ForGroup` | · |  |
| `Report_InformationSheet_DaysArrivals_Group` | · |  |
| `Report_InformationSheet_DaysArrivals_Testing` | · | _backup/variant_ |
| `Report_InformationSheet_DaysDepartures` | · |  |
| `Report_InformationSheet_DaysDepartures_ForGroup` | · |  |
| `Report_InformationSheet_DaysDepartures_Group` | · |  |
| `Report_InformationSheet_MealReservationDetails` | · |  |
| `Report_InformationSheet_StayOvers` | · |  |
| `Report_InformationSheet_StayOvers_ForGroup` | · |  |
| `Report_InformationSheet_StayOvers_Group` | · |  |
| `Report_Invoice_All` | · |  |
| `Report_Invoice_All_DeV` | · |  |
| `Report_InvoiceSettelements` | · |  |
| `Report_InvoiceSettelements_Coral` | · |  |
| `Report_InvoiceTax` | · |  |
| `Report_InvoiceTax_02_06_2020` | · | _backup/variant_ |
| `Report_InvoiceTax_backup27-06-2020` | · | _backup/variant_ |
| `Report_InvoiceTax_Copy` | · |  |
| `Report_InvoiceTax_Coral` | · |  |
| `Report_InvoiceWiseSales` | · |  |
| `Report_ItemConsumption` | · |  |
| `Report_ItemMoving` | · |  |
| `Report_ItemSalesSummaryChanelWise` | · |  |
| `Report_ItemSalesSummaryChanelWise_1` | · |  |
| `Report_LostAndFound` | · |  |
| `Report_LostAndFoundDetails` | · |  |
| `Report_ManagerReport` | · |  |
| `Report_MealCountDetailsByDateRange` | · |  |
| `Report_MealReservationDetails` | · |  |
| `Report_MonthlyAverageOccupancy_WithAndWithoutComplimentaryRoomNights` | · |  |
| `Report_MonthlyAverageOccupancy_WithAndWithoutComplimentaryRoomNights_Parameterized` | · |  |
| `Report_NationalityWiseExtraFandBRevenue` | · |  |
| `Report_NewMiscellaneousBillingSummary` | · |  |
| `Report_OccupancyByPax` | · |  |
| `Report_OccupancyByPax_Old` | · | _backup/variant_ |
| `Report_OccupancyByPax_Parameterized` | · |  |
| `Report_OccupancyByRoomNights` | · |  |
| `Report_OccupancyByRoomNights_dev` | · |  |
| `Report_OccupancyByRoomNights_Jetwing` | · |  |
| `Report_OccupancyByRoomNights_Jetwing_Parameterized` | · |  |
| `Report_OccupancyByRoomNights_Parameterized` | · |  |
| `Report_OccupancyByRoomNights_TEST` | · |  |
| `Report_OnTheBook` | · |  |
| `Report_OnTheBook_20250729` | · | _backup/variant_ |
| `Report_OnTheBook_Browns` | · |  |
| `Report_OnTheBook_Dev` | · | _backup/variant_ |
| `Report_OnTheBook_dev1` | · |  |
| `Report_OnTheBook_dev_20250428` | · | _backup/variant_ |
| `Report_OnTheBook_Exist` | · |  |
| `Report_OnTheBook_OLD` | · | _backup/variant_ |
| `Report_OnTheBook_TEST` | · |  |
| `Report_OutletSalesCashRecon` | · |  |
| `Report_OutOfOrder` | · |  |
| `Report_OutOfOrderRoomDetails` | · |  |
| `Report_OverallHotelPerformance` | · |  |
| `Report_Parameters_byReportName` | · |  |
| `Report_PastSixMonthSalesSummary` | · |  |
| `Report_PaymentPolicies` | · |  |
| `Report_PaymentPolicies_20221125` | · | _backup/variant_ |
| `Report_PaymentPolicies_OLD` | · | _backup/variant_ |
| `Report_PaymentTypeCodeWise` | · |  |
| `Report_PaymentTypeWise` | · |  |
| `Report_PaymentTypeWise_1` | · |  |
| `Report_PaymentTypeWise_20250303` | · | _backup/variant_ |
| `Report_PaymentTypeWise_2025_04_16_BeforeDev` | · | _backup/variant_ |
| `Report_PaymentWiseDetails` | · |  |
| `Report_PaymentWiseSummary` | · |  |
| `Report_PendingReservations` | · |  |
| `Report_PickupDetailsByAgent` | · |  |
| `Report_PickupReservationDetails` | · |  |
| `Report_PickupReservationDetails_New` | · | _backup/variant_ |
| `Report_PickupReservationDetails_old` | · |  |
| `Report_PMSSegments_AccommodationRevenueBudget_Report` | · |  |
| `Report_Posting_Bill_Payments_Summary` | · |  |
| `Report_ProductAnalysis` | · |  |
| `Report_ProductAnalysis_1` | · |  |
| `Report_ProductSoldComparison` | · |  |
| `Report_ProfitCenterWisePostingDetails` | · |  |
| `Report_ProformaInvoice_SelectCharges_ForDetail` | · |  |
| `Report_ProformaInvoice_SelectCharges_ForDetail_New` | · | _backup/variant_ |
| `Report_ProformaInvoice_SelectCharges_ForDetail_New_bACK20260206` | · |  |
| `Report_ProformaInvoice_SelectCharges_ForDetail_New_old` | · |  |
| `Report_ProformaInvoice_SelectCharges_ForDetail_New_Old_2025_12_09` | · | _backup/variant_ |
| `Report_ProformaInvoice_SelectCharges_ForSummary` | · |  |
| `Report_ProformaInvoice_SelectCharges_ForSummary_New` | · | _backup/variant_ |
| `Report_ProformaInvoice_SelectCharges_ForSummary_New_Dev` | · | _backup/variant_ |
| `Report_ProformaInvoice_SelectCharges_ForSummary_New_Old_2025_12_09` | · | _backup/variant_ |
| `Report_ProformaInvoice_SelectCharges_ForSummary_New_TEST` | · |  |
| `Report_ProformaInvoice_SelectDetails` | · |  |
| `Report_ProformaInvoice_SelectDetails_New` | · | _backup/variant_ |
| `Report_PropertyWise_CategoryWiseRoomRevenue_MTD` | · |  |
| `Report_PropertyWise_CategoryWiseRoomRevenue_Today` | · |  |
| `Report_PropertyWise_ProfileTypeWise_RoomNights_MTD` | · |  |
| `Report_PropertyWise_ProfileTypeWise_RoomNights_Today` | · |  |
| `Report_PropertyWise_ProfileTypeWiseRevenue_MTD` | · |  |
| `Report_PropertyWise_ProfileTypeWiseRevenue_Today` | · |  |
| `Report_PropertyWiseAgentRevenueAndOccupancySummary` | · |  |
| `Report_PropertyWiseAgentRevenueAndOccupancySummary_Parameterized` | · |  |
| `Report_PropertyWiseBankDetails_Select` | · |  |
| `Report_PropertyWiseOccupancySummary_MTD` | · |  |
| `Report_PropertyWiseOccupancySummary_MTD_Parameterized` | · |  |
| `Report_PropertyWiseOccupancySummary_Today` | · |  |
| `Report_PropertyWiseOccupancySummary_Today_Parameterized` | · |  |
| `Report_PropertyWiseRoomPickUp_Details` | · |  |
| `Report_Rebate` | · |  |
| `Report_Rebate_Details` | · |  |
| `Report_Rebate_Receipt` | · |  |
| `Report_Rebate_Receipt_TEST` | · |  |
| `Report_RebateDetails` | · |  |
| `Report_ReceipeWiseSales` | · |  |
| `Report_ReservationConfirmation_ReservationChargeDetails` | · |  |
| `Report_ReservationDetailsOfGuestsOnBookingDate` | · |  |
| `Report_ReservationDetailsWithRoomRates` | · |  |
| `Report_ReservationForm_AccommodationDetails` | · |  |
| `Report_ReservationForm_GuestDetails` | · |  |
| `Report_ReservationForm_PaxDetails` | · |  |
| `Report_ReservationForm_PaymentDetails` | · |  |
| `Report_ReservationForm_ReservationDetails` | · |  |
| `Report_ReservationRoomRateChangeLog_Select` | · |  |
| `Report_ReservationWiseFoodRevenueBreakDown_ByMeal` | · |  |
| `Report_RevenueDetails` | · |  |
| `Report_RevenueDetails_Dev` | · | _backup/variant_ |
| `Report_RevenueDetails_Dev1` | · | _backup/variant_ |
| `Report_RevenueDetailsCommon` | · |  |
| `Report_RevenueDetailsCommon_BeforeModificationOn_2022-12-30` | · |  |
| `Report_RevenueDetailsCommon_ForReservation` | · |  |
| `Report_RevenueDetailsCommon_ForReservation_Tax` | · |  |
| `Report_RevenueDetailsCommon_Test` | · | _backup/variant_ |
| `Report_Room_Rate_Details` | · |  |
| `Report_RoomAvailability_Occupancy_Forecast` | · |  |
| `Report_RoomAvailability_Occupancy_Forecast_Parameterized` | · |  |
| `Report_RoomCategoryWiseTourOperatorPerformance` | · |  |
| `Report_RoomChange_Log` | · |  |
| `Report_RoomChangeDetails` | · |  |
| `Report_RoomChangeLogs_Select` | · |  |
| `Report_RoomInvoiceSummary` | · |  |
| `Report_RoomInvoiceSummary_ForAudit` | · |  |
| `Report_RoomInvoiceSummary_ForAudit_Optimized` | · |  |
| `Report_RoomRevDtl` | · |  |
| `Report_RoomRevDtlMP` | · |  |
| `Report_RoomRevDtlRoomCat` | · |  |
| `Report_RoomRevSum` | · |  |
| `Report_RoomSales` | · |  |
| `Report_RoomSales_Test` | · | _backup/variant_ |
| `Report_RoomSalesChat` | · |  |
| `Report_SalesDetails` | · |  |
| `Report_SalesPersonWiseRevenue` | · |  |
| `Report_SalesPersonWiseStatistics` | · |  |
| `Report_SalesSummary` | · |  |
| `Report_SegmentWise_RevenueDetailsWithBudget` | · |  |
| `Report_Select_AllotmentDetails` | · |  |
| `Report_Select_CallTxnByDateRangeWise` | · |  |
| `Report_Select_CallTxnByExtensionCode` | · |  |
| `Report_Select_CallTxnByExtensionGroupWise` | · |  |
| `Report_Select_CallTxnByTelephoneNumberWise` | · |  |
| `Report_Select_CallTxnSummaryByDateRangeWise` | · |  |
| `Report_Select_CallTxnSummaryByExtensionCode` | · |  |
| `Report_Select_CallTxnSummaryByExtensionGroupWise` | · |  |
| `Report_Select_CallTxnSummaryByTelePhoneNumberWise` | · |  |
| `Report_Select_ReportNames` | · |  |
| `Report_Select_ReservationWithinGroup` | · |  |
| `Report_SelectReservationDetailsForSupportingBillPreveiew` | · |  |
| `Report_SPFoodCosting` | · |  |
| `Report_SRN_Listing_Details` | · |  |
| `Report_StockReconciliation` | · |  |
| `Report_StockStatusReport` | · |  |
| `Report_SubRegionWiseCountryList` | · |  |
| `Report_TermsAndCondition` | · |  |
| `Report_TermsAndConditionGRC` | · |  |
| `Report_TermsAndConditionGroupGRC` | · |  |
| `Report_Trace_Log` | · |  |
| `Report_TransportAlerts` | · |  |
| `Report_TransportAll` | · |  |
| `Report_UserChanges_Log` | · |  |
| `Report_VATUploadSchedule` | · |  |
| `Report_Visit_Purpose_Details` | · |  |
| `Report_Void_Currency_Encashment_Details` | · |  |
| `Report_VoidBillListing` | · |  |
| `Report_VoidExtraPosting_Bill_Payments` | · |  |
| `Report_VoidExtraPosting_Taxes_Bill` | · |  |

#### `Reports_*` — 104

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Reports_Advance_Receipt` | · |  |
| `Reports_AdvanceDetails_Reservation` | · |  |
| `Reports_AgentWiseRoomRevenue` | · |  |
| `Reports_AllotmentDetails` | · |  |
| `Reports_AllotmentVsReservations_Details` | · |  |
| `Reports_CancelledReservations` | · |  |
| `Reports_CancelledReservations_ByArrivalDate` | · |  |
| `Reports_CancelledReservations_ByArrivalDate_OTA` | · |  |
| `Reports_CancelledReservations_Dev` | · | _backup/variant_ |
| `Reports_CancelledReservations_Old` | · | _backup/variant_ |
| `Reports_CancelledReservations_OTA` | · |  |
| `Reports_CancelledReservations_TEST` | · |  |
| `Reports_CompanywiseRevenue` | · |  |
| `Reports_CreateDayEndStats` | · |  |
| `Reports_CreateDayEndStats_Job` | · |  |
| `Reports_CreateDayEndStats_Job_SQL` | · |  |
| `Reports_CreateDayEndStats_Reservation` | · |  |
| `Reports_DaywiseRevenue` | · |  |
| `Reports_ExtraPostingBill_detail` | · |  |
| `Reports_GuestArivalAlphabetically` | · |  |
| `Reports_GuestBalanceAnalysis` | · |  |
| `Reports_GuestDeparture` | · |  |
| `Reports_GuestDeparture_StillInhouse` | · |  |
| `Reports_GuestInHouseReservationAgentWise` | · |  |
| `Reports_GuestInHouseReservationCountryWise` | · |  |
| `Reports_GuestInHouseReservationNationaltyWise` | · |  |
| `Reports_HotelStatistics` | · |  |
| `Reports_HotelStatistics_NEW` | · | _backup/variant_ |
| `Reports_HotelStatistics_NEW_Dev` | · | _backup/variant_ |
| `Reports_HotelStatistics_NEW_notuse` | · | _backup/variant_ |
| `Reports_HotelStatistics_NEW_Stehani` | · | _backup/variant_ |
| `Reports_HouseKeepingDiscrepancy` | · |  |
| `Reports_InformationSummary` | · |  |
| `Reports_InformationSummary_Monthly` | · |  |
| `Reports_InHouseGuests` | · |  |
| `Reports_InHouseGuests_Dev` | · | _backup/variant_ |
| `Reports_InHouseGuests_ExistOn20240408` | · |  |
| `Reports_InHouseGuests_new` | · |  |
| `Reports_InHouseGuests_old` | · |  |
| `Reports_InventoryItems` | · |  |
| `Reports_IsComplementryReservation` | · |  |
| `Reports_Laundry_InvoiceBill_Dtl_Copy` | · |  |
| `Reports_Laundry_InvoiceBill_Dtl_Copy_Stehani` | · |  |
| `Reports_Laundry_InvoicePayments_Copy` | · |  |
| `Reports_Laundry_InvoiceTAX_Dtl_Copy` | · |  |
| `Reports_Laundry_InvoiceTotal` | · |  |
| `Reports_LaundryPosting_Details` | · |  |
| `Reports_LaundryPosting_Details_Back` | · |  |
| `Reports_LaundryTEST` | · |  |
| `Reports_ManagerReport` | · |  |
| `Reports_ManagerReport_Old` | · | _backup/variant_ |
| `Reports_ManagerReportSub` | · |  |
| `Reports_ManagerReportSub_Old` | · | _backup/variant_ |
| `Reports_MealForecast` | · |  |
| `Reports_MealForecast_20250813` | · | _backup/variant_ |
| `Reports_MealReservationInvoice` | · |  |
| `Reports_MealReservations` | · |  |
| `Reports_MealReservations_20250813` | · | _backup/variant_ |
| `Reports_MealReservations_ChargeDetails` | · |  |
| `Reports_MealReservations_Details` | · |  |
| `Reports_MealReservationTaxes` | · |  |
| `Reports_MegaSelectForReservationReports` | · |  |
| `Reports_NationalityWiseGuestNights_Actual` | · |  |
| `Reports_OccupancyDaily` | · |  |
| `Reports_OccupancyDaily_Common` | · |  |
| `Reports_OccupancyDaily_Common_Parameterized` | · |  |
| `Reports_OccupancyDaily_OLD` | · | _backup/variant_ |
| `Reports_OccupancyDaily_Parameterized` | · |  |
| `Reports_OutOfOrderRoom_Details` | · |  |
| `Reports_ProfitCenter_InvoiceTotal` | · |  |
| `Reports_ReservationConfirmation_SelectedGuestAndRoomDetails` | · |  |
| `Reports_ReservationConfirmation_SelectedGuestAndRoomDetails_Exist` | · |  |
| `Reports_ReservationConfirmation_SelectedPropertyDetails` | · |  |
| `Reports_ReservationConfirmation_SelectedRoomDetails` | · |  |
| `Reports_ReservationDetails` | · |  |
| `Reports_ReservationDetails_dev` | · |  |
| `Reports_ReservationDetails_ParamNames` | · |  |
| `Reports_ReservationDetailsHistory` | · | _backup/variant_ |
| `Reports_ReservationRoomNight` | · |  |
| `Reports_ReservationRoomNight_2024_1007` | · | _backup/variant_ |
| `Reports_ReservationRoomNight_Actual` | · |  |
| `Reports_ReservationRoomNight_Actual_Dev` | · | _backup/variant_ |
| `Reports_RoomCategoryWise_ForecastSummary` | · |  |
| `Reports_RoomCategoryWise_ForecastSummary_Back20241121` | · |  |
| `Reports_RoomCategoryWise_ForecastSummary_Temp` | · |  |
| `Reports_RoomCategoryWiseforecastSummary` | · |  |
| `Reports_RoomChange_Details` | · |  |
| `Reports_RoomRatesChangeReport` | · |  |
| `Reports_RoomTypeWiseRoomRevenue` | · |  |
| `Reports_Select_Reservations_For_Occupancy` | · |  |
| `Reports_Select_Reservations_For_Occupancy_Browns` | · |  |
| `Reports_Select_Reservations_For_Occupancy_Browns_Parameterized` | · |  |
| `Reports_Select_Reservations_For_Occupancy_Parameterized` | · |  |
| `Reports_Select_Reservations_For_Revenue` | · |  |
| `Reports_Select_Reservations_For_Revenue_TaxBreakup` | · |  |
| `Reports_SelectSchecdulePostingProforma` | · |  |
| `Reports_SupportingBill` | · |  |
| `Reports_SupportingBill_Tax` | · |  |
| `Reports_Tourist_Board_Statistics` | · |  |
| `Reports_UserAccessRole_Details` | · |  |
| `Reports_UserWiseAccess_Details` | · |  |
| `Reports_Void_ExtraPosting_Details` | · |  |
| `Reports_Void_Folio_Details` | · |  |
| `Reports_Void_Folio_Details_UsingVoidBillSettlementDetails` | · |  |

#### Other Reporting & Analytics procedures — 25

| Stored procedure | Type | Notes |
|---|:--:|---|
| `BudgetAllocations_M_Save` | M |  |
| `BudgetAllocations_M_Select` | M |  |
| `DailyRevenueReport` | · |  |
| `DailyRevenueReport_23032022` | · | _backup/variant_ |
| `DashboardFigures_SelectForDashboardAPI` | · |  |
| `DashboardFigures_SelectForDisplay` | · |  |
| `Insert_ReportProperties_PropertyImage` | · |  |
| `ReportAgentsProduction` | · |  |
| `ReportDetails_M_SelectByReportName` | M |  |
| `ReportGuestBirthdayCheckoutReservation` | · |  |
| `ReportGuestBirthdayInhouse` | · |  |
| `ReportGuestBirthdayReservation` | · |  |
| `ReportGuestHistory` | · | _backup/variant_ |
| `ReportHalfHourlySales` | · |  |
| `ReportHalfHourlySales_Dashboard` | · |  |
| `ReportInHouse_ReservationHeaders` | · |  |
| `ReportMarketForecast` | · |  |
| `ReportPrintCopyLog_Insert` | · |  |
| `ReportProductAnalysis` | · |  |
| `ReportRevPAR` | · |  |
| `ReportSegmentStat` | · |  |
| `ReportsInHouseGroupResList_ParamNames` | · |  |
| `ReportsInHouseList_ParamNames` | · |  |
| `ReportsInHouseList_ParamNames_Count` | · |  |
| `Select_CRM_Dashboard` | · |  |

## Integrations & Notifications — 152 stored procedures

*External systems and messaging: channel managers, payment gateway, SMS/email/WhatsApp, RabbitMQ, notifications.*  ·  Detail: [11-integrations-and-data-flow.md](11-integrations-and-data-flow.md)

#### `AlertTypes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `AlertTypes_M_Delete` | M |  |
| `AlertTypes_M_Save` | M |  |
| `AlertTypes_M_Select` | M |  |
| `AlertTypes_M_Select_ById` | M |  |
| `AlertTypes_M_Select_ForGrid` | M |  |

#### `Bookingwhizz_*` — 11

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Bookingwhizz_GuestProfile_T_UpdateResponse` | T |  |
| `Bookingwhizz_GuestProfileUpdate` | · |  |
| `Bookingwhizz_Reservations_T_UpdateResponse` | T |  |
| `Bookingwhizz_ReservationUpdate` | · |  |
| `Bookingwhizz_Stay_T_UpdateResponse` | T |  |
| `Bookingwhizz_T_CRMProperties_Select` | T |  |
| `Bookingwhizz_T_GuestProfile_Select` | T |  |
| `Bookingwhizz_T_Reservation_Select` | T |  |
| `Bookingwhizz_T_Reservation_Select_NotUse_20230310` | T | _backup/variant_ |
| `Bookingwhizz_T_Reservation_Select_TEST` | T |  |
| `Bookingwhizz_T_Stay_Data_Select` | T |  |

#### `CM_*` — 12

| Stored procedure | Type | Notes |
|---|:--:|---|
| `CM_AxisRooms_Availability_Send` | · |  |
| `CM_AxisRooms_Reservation_API_Cancellation` | · |  |
| `CM_AxisRooms_Reservation_API_Save` | · |  |
| `CM_AxisRooms_Reservation_API_Update` | · |  |
| `CM_AxisRooms_RoomRate_By_DateRange` | · |  |
| `CM_AxisRooms_WEBUpdateResult` | · |  |
| `CM_RateTiger_Reservation_API_Cancel` | · |  |
| `CM_RateTiger_Reservation_API_Save` | · |  |
| `CM_RateTiger_Reservation_API_Update` | · |  |
| `CM_RateTiger_ReservationDetails_API_Update` | · |  |
| `CM_RateTiger_Update_All_Availability` | · |  |
| `CM_RateTiger_Update_All_Rates` | · |  |

#### `DocumentProcessWiseDocument_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `DocumentProcessWiseDocument_M_Select_ByDocProcessId` | M |  |
| `DocumentProcessWiseDocument_M_SelectById` | M |  |
| `DocumentProcessWiseDocument_Select_ByDocumentProcessId` | · |  |

#### `IBESliderImages_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `IBESliderImages_M_Delete` | M |  |
| `IBESliderImages_M_Save` | M |  |
| `IBESliderImages_M_Select` | M |  |
| `IBESliderImages_M_Select_ById` | M |  |
| `IBESliderImages_M_Select_ForGrid` | M |  |

#### `Notification_*` — 16

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Notification_Emails_To_Send` | · |  |
| `Notification_Emails_UpdateAsSend` | · |  |
| `Notification_EmailSettings_M_Save` | M |  |
| `Notification_EmailSettings_M_Select` | M |  |
| `Notification_Parameters_M_Delete` | M |  |
| `Notification_Parameters_M_Save` | M |  |
| `Notification_Parameters_M_Select` | M |  |
| `Notification_Template_Schedule_M_Delete` | M |  |
| `Notification_Template_Schedule_M_Save` | M |  |
| `Notification_Template_Schedule_M_Select` | M |  |
| `Notification_Template_Types_M_Delete` | M |  |
| `Notification_Template_Types_M_Save` | M |  |
| `Notification_Template_Types_M_Select` | M |  |
| `Notification_Templates_M_Delete` | M |  |
| `Notification_Templates_M_Save` | M |  |
| `Notification_Templates_M_Select` | M |  |

#### `PrinterSetup_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PrinterSetup_M_Delete` | M |  |
| `PrinterSetup_M_Save` | M |  |
| `PrinterSetup_Select_for_sync` | · |  |

#### `RabbitMQ_*` — 15

| Stored procedure | Type | Notes |
|---|:--:|---|
| `RabbitMQ_ActionFailures_Update` | · |  |
| `RabbitMQ_FolioDetails` | · |  |
| `RabbitMQ_FolioDetails_Backup` | · | _backup/variant_ |
| `RabbitMQ_FolioDetails_WithLineItems` | · |  |
| `RabbitMQ_FolioDetails_WithLineItems_Dev` | · | _backup/variant_ |
| `RabbitMQ_FolioDetails_WithLineItems_OLD` | · | _backup/variant_ |
| `RabbitMQ_GuestCheckIn` | · |  |
| `RabbitMQ_GuestCheckIn_Old` | · | _backup/variant_ |
| `RabbitMQ_GuestCheckOut` | · |  |
| `RabbitMQ_GuestCheckOut_Old` | · | _backup/variant_ |
| `RabbitMQ_GuestRoomChange` | · |  |
| `RabbitMQ_GuestRoomChange_Old` | · | _backup/variant_ |
| `RabbitMQ_PendingLogs_Select` | · |  |
| `RabbitMQ_PendingLogs_Update` | · |  |
| `RabbitMQ_RoomStatus` | · |  |

#### `ServiceHub_*` — 37

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ServiceHub_DepartmentAssignees_M_SelectForCombo` | M |  |
| `ServiceHub_Departments_M_SelectForCombo` | M |  |
| `ServiceHub_InsertDefaulLocations` | · |  |
| `ServiceHub_ReservationDetails_M_SelectyReservationNo` | M |  |
| `ServiceHub_SelectReservationDeatils_ByResLevelAndResNo` | · |  |
| `ServiceHub_ServiceActions_M_Delete` | M |  |
| `ServiceHub_ServiceActions_M_Save` | M |  |
| `ServiceHub_ServiceActions_M_Select_ById` | M |  |
| `ServiceHub_ServiceActions_M_Select_ForGrid` | M |  |
| `ServiceHub_ServiceActions_M_SelectForCombo` | M |  |
| `ServiceHub_ServiceActions_M_SelectForTakenCombo` | M |  |
| `ServiceHub_ServiceCategories_M_Delete` | M |  |
| `ServiceHub_ServiceCategories_M_Save` | M |  |
| `ServiceHub_ServiceCategories_M_Select_ById` | M |  |
| `ServiceHub_ServiceCategories_M_Select_ForGrid` | M |  |
| `ServiceHub_ServiceCategories_M_SelectForCombo` | M |  |
| `ServiceHub_ServiceJob_M_Delete` | M |  |
| `ServiceHub_ServiceJob_M_Save` | M |  |
| `ServiceHub_ServiceJob_M_SelectForActivityLog` | M |  |
| `ServiceHub_ServiceJob_M_SelectForActivityLogByHistoryId` | M | _backup/variant_ |
| `ServiceHub_ServiceJob_M_SelectForTaken` | M |  |
| `ServiceHub_ServiceJob_M_SelectForTakenGrid` | M |  |
| `ServiceHub_ServiceJob_M_SelectReservationNos` | M |  |
| `ServiceHub_ServiceJobs_M_Select_ById` | M |  |
| `ServiceHub_ServiceJobs_M_Select_ForGrid` | M |  |
| `ServiceHub_ServiceJobs_M_Select_ForGrid_OLD` | M | _backup/variant_ |
| `ServiceHub_ServiceJobTaken_M_Save` | M |  |
| `ServiceHub_ServiceLocations_M_Delete` | M |  |
| `ServiceHub_ServiceLocations_M_Save` | M |  |
| `ServiceHub_ServiceLocations_M_Select_ById` | M |  |
| `ServiceHub_ServiceLocations_M_Select_ForGrid` | M |  |
| `ServiceHub_ServiceLocations_M_SelectForCombo` | M |  |
| `ServiceHub_ServiceTypes_M_Delete` | M |  |
| `ServiceHub_ServiceTypes_M_Save` | M |  |
| `ServiceHub_ServiceTypes_M_Select_ById` | M |  |
| `ServiceHub_ServiceTypes_M_Select_ForGrid` | M |  |
| `ServiceHub_ServiceTypes_M_SelectForCombo` | M |  |

#### `Staah_*` — 23

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Staah_AdvancePayment_Cancellation` | · |  |
| `Staah_AdvancePayment_Cancellation_Dev` | · | _backup/variant_ |
| `Staah_Availability_RoomCategories` | · |  |
| `Staah_Availability_RoomRate_Select` | · |  |
| `Staah_Availability_RoomRate_Select_Dev` | · | _backup/variant_ |
| `Staah_Availability_RoomRate_Select_MultiProperty` | · |  |
| `Staah_Availability_RoomRate_Select_MultiProperty_Exist20250408` | · |  |
| `Staah_Availability_RoomRate_Select_MultiProperty_ToTestFullVilla` | · |  |
| `Staah_AvailabilityPush_ForDateRange` | · |  |
| `Staah_AvailabilityPushStatus_Update` | · |  |
| `Staah_AvailabilityUpdateFromPMS` | · |  |
| `Staah_MissedReservation_Select` | · |  |
| `Staah_MissedReservation_Update` | · |  |
| `Staah_PendingReservationsToSync` | · |  |
| `Staah_Reservation_Cancel` | · |  |
| `Staah_Reservation_Save` | · |  |
| `Staah_Reservation_Save_DeliverToPMS` | · |  |
| `Staah_Reservation_Save_DeliverToPMS_Dev` | · | _backup/variant_ |
| `Staah_Reservation_Save_Stehani` | · |  |
| `Staah_Reservation_SelectDeliverToPMS` | · |  |
| `Staah_Reservation_Update` | · |  |
| `Staah_ReservationRequestRePush` | · |  |
| `Staah_Select_ReservationRequestDetails_ByXml` | · |  |

#### `WebApi_*` — 7

| Stored procedure | Type | Notes |
|---|:--:|---|
| `WebApi_RateCodeHeaders_Save` | · |  |
| `WebApi_Reservcation_Select_ToSync_HotelRes` | · |  |
| `WebApi_Reservcation_Update_AsDownloaded` | · |  |
| `WebApi_RoomAvailability` | · |  |
| `WebApi_RoomAvailability_Save` | · |  |
| `WebApi_RoomRates_Save` | · |  |
| `WebApi_Seasons_Save` | · |  |

#### Other Integrations & Notifications procedures — 15

| Stored procedure | Type | Notes |
|---|:--:|---|
| `DirectPrint_AvoidDuplicatePrint` | · |  |
| `DirectPrint_CreateDocument` | · |  |
| `DocumentProcess_M_Select` | M |  |
| `DoorLockEvent_T_InsertOrDeleteKeyCode` | T |  |
| `DoorLockEvent_T_Save` | T |  |
| `EmailLog_SendEmails` | · |  |
| `EmailTypes_M_Select` | M |  |
| `FiscalPrinter_DirectPrint` | · |  |
| `FiscalPrinter_FolioInvoice` | · |  |
| `IBEStayView_M_Select` | M |  |
| `MPEmailSettings_M_Select` | M |  |
| `MPEmailSettings_M_Select_2024_06_17` | M | _backup/variant_ |
| `ServiceJobs_GenerateEmail` | · |  |
| `ServiceJobs_SendEmail` | · |  |
| `usp_SendTextEmail` | · |  |

## Maintenance & Service — 115 stored procedures

*Engineering/maintenance jobs, assets, activities, complaints, lost & found.*  ·  Detail: [06-rooms-and-housekeeping-process.md](06-rooms-and-housekeeping-process.md)

#### `Activities_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Activities_M_Delete` | M |  |
| `Activities_M_Save` | M |  |
| `Activities_M_Select` | M |  |
| `Activities_M_Select_ById` | M |  |
| `Activities_M_Select_ForGrid` | M |  |
| `Activities_T_SelectByMaintenanceId` | T |  |

#### `Assests_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Assests_M_Delete` | M |  |
| `Assests_M_Save` | M |  |
| `Assests_M_Select` | M |  |
| `Assests_M_Select_ById` | M |  |
| `Assests_M_Select_ForGrid` | M |  |

#### `AssestTypes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `AssestTypes_M_Delete` | M |  |
| `AssestTypes_M_Save` | M |  |
| `AssestTypes_M_Select` | M |  |
| `AssestTypes_M_Select_ById` | M |  |
| `AssestTypes_M_Select_ForGrid` | M |  |

#### `AssetWiseMaintenanceTypes_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `AssetWiseMaintenanceTypes_M_Save` | M |  |
| `AssetWiseMaintenanceTypes_M_Select` | M |  |
| `AssetWiseMaintenanceTypes_M_Select_ById` | M |  |

#### `Complain_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Complain_Select` | · |  |
| `Complain_Taken` | · |  |
| `Complain_Update_StatusGrid` | · |  |

#### `ComplainLog_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ComplainLog_M_Select` | M |  |
| `ComplainLog_M_Select_ByUserId` | M |  |
| `ComplainLog_Select_ByCode` | · |  |

#### `Complains_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Complains_M_Delete` | M |  |
| `Complains_M_Select` | M |  |
| `Complains_M_Select_ForGrid` | M |  |
| `Complains_Select_ByCode` | · |  |
| `Complains_Select_ById` | · |  |

#### `ComplainTypes_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ComplainTypes_M_Delete` | M |  |
| `ComplainTypes_M_Save` | M |  |
| `ComplainTypes_M_Select` | M |  |
| `ComplainTypes_M_Select_ById` | M |  |
| `ComplainTypes_M_Select_ForGrid` | M |  |
| `ComplainTypes_T_Select_ByComplainCategoryId` | T |  |

#### `DamageRequest_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `DamageRequest_M_Delete` | M |  |
| `DamageRequest_M_History_By_UserId` | M | _backup/variant_ |
| `DamageRequest_M_Select_DocNo` | M |  |
| `DamageRequest_M_SelectHistory` | M | _backup/variant_ |
| `DamageRequest_M_UnSaved_All` | M |  |

#### `JobWiseNotes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `JobWiseNotes_Delete` | · |  |
| `JobWiseNotes_M_Select_ForGrid` | M |  |
| `JobWiseNotes_Save` | · |  |
| `JobWiseNotes_Select` | · |  |
| `JobWiseNotes_SelectById` | · |  |

#### `Locations_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Locations_Delete` | · |  |
| `Locations_Save` | · |  |
| `Locations_Select` | · |  |
| `Locations_SelectById` | · |  |

#### `LostAndFound_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `LostAndFound_Pending_T_Select` | T |  |
| `LostAndFound_Pending_T_Select_ById` | T |  |
| `LostAndFound_Released_T_Select` | T |  |

#### `LostandFoundActions_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `LostandFoundActions_M_Delete` | M |  |
| `LostandFoundActions_M_Save` | M |  |
| `LostandFoundActions_M_Select` | M |  |
| `LostandFoundActions_M_Select_ById` | M |  |
| `LostandFoundActions_M_Select_ForGrid` | M |  |

#### `LostandFoundItemCategories_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `LostandFoundItemCategories_M_Delete` | M |  |
| `LostandFoundItemCategories_M_Save` | M |  |
| `LostandFoundItemCategories_M_Select` | M |  |
| `LostandFoundItemCategories_M_Select_ById` | M |  |
| `LostandFoundItemCategories_M_Select_ForGrid` | M |  |

#### `Maintenance_*` — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Maintenance_Activity_M_Select` | M |  |
| `Maintenance_Jobs_M_Save` | M |  |
| `Maintenance_Jobs_M_Select` | M |  |
| `Maintenance_Jobs_M_Select_ById` | M |  |
| `Maintenance_Jobs_M_Select_ForGrid` | M |  |
| `Maintenance_JobWiseNotes_M_Save` | M |  |

#### `MaintenanceTypes_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `MaintenanceTypes_M_Delete` | M |  |
| `MaintenanceTypes_M_Save` | M |  |
| `MaintenanceTypes_M_Select` | M |  |
| `MaintenanceTypes_M_Select_ById` | M |  |
| `MaintenanceTypes_M_Select_ForGrid` | M |  |

#### `PreventiveMaintenanceScedule_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `PreventiveMaintenanceScedule_M_Save` | M |  |
| `PreventiveMaintenanceScedule_M_Select` | M |  |
| `PreventiveMaintenanceScedule_M_Select_ForGrid` | M |  |
| `PreventiveMaintenanceScedule_T_SelectById` | T |  |

#### `ProductionCenters_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ProductionCenters_M_Delete` | M |  |
| `ProductionCenters_M_Save` | M |  |
| `ProductionCenters_M_Select` | M |  |
| `ProductionCenters_M_Select_ById` | M |  |
| `ProductionCenters_M_Select_ForGrid` | M |  |

#### `Tracess_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Tracess_M_Delete` | M |  |
| `Tracess_M_Save` | M |  |
| `Tracess_M_Select` | M |  |
| `Tracess_M_Select_ById` | M |  |
| `Tracess_M_Select_ForGrid` | M |  |

#### Other Maintenance & Service procedures — 27

| Stored procedure | Type | Notes |
|---|:--:|---|
| `ActivityWiseMaintenance_M_Select_ByActivityId` | M |  |
| `ActivityWiseMaintenance_T_Select_ByMaintenanceId` | T |  |
| `ActivityWiseMaintenanceType_M_Select` | M |  |
| `ActivityWiseMaintenanceType_M_Select_ForGrid` | M |  |
| `ActivityWiseMaintenanceTypes_M_Save` | M |  |
| `ActivityWiseMaintenanceTypes_M_Select_ById` | M |  |
| `AssetWiseMaintenance_M_Select_ByActivityId` | M |  |
| `AssetWiseMaintenanceType_M_Select_ForGrid` | M |  |
| `Damage_Request_M_Save` | M |  |
| `DamageApproval_M_Save` | M |  |
| `DamageItem_M_Delete` | M |  |
| `Jobs_M_Select_ByPreventiveMaintenanceScedule` | M |  |
| `Jobs_M_Select_ByStaffCategory` | M |  |
| `JobStatus_Select` | · |  |
| `JobTypes_T_Select` | T |  |
| `JobWiseStaffAllocation_M_Select_ByStaffCategory` | M |  |
| `Location_M_Select` | M |  |
| `Location_M_Select_All` | M |  |
| `LostAndFoundActions_M_Select_ForCombo` | M |  |
| `LostAndFoundItem_T_Save` | T |  |
| `LostAndFoundLocations_M_Select_ForCombo` | M |  |
| `LostAndFoundRelatedImages_M_Select_ById` | M |  |
| `LostAndFoundTypes_M_Select_ForCombo` | M |  |
| `MaintenanceSettings_M_Select` | M |  |
| `MaintenanceSettings_M_Update` | M |  |
| `PreventiveMaintenance_M_Select_ById` | M |  |
| `PreventiveMaintenance_M_Select_ByStaffCategory` | M |  |

## System / Framework — 75 stored procedures

*Framework/plumbing: migrations, navigation/menu, generic helpers, staging/temp.*  ·  Detail: [12-database-and-technical-architecture.md](12-database-and-technical-architecture.md)

#### `Admin_*` — 44

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Admin_AddForignKeys` | · |  |
| `Admin_ChangeConvertionOn_Reservation_Checkin` | · |  |
| `Admin_CheckReservationMissingReferences` | · |  |
| `Admin_Classes` | · |  |
| `Admin_ClassFromSQLTable` | · |  |
| `Admin_Common_CurrencyConversion` | · |  |
| `Admin_CorrectFolioRates` | · |  |
| `Admin_CreateMissingGuestProfiles` | · |  |
| `Admin_CreateRevenueHistoryBasedOnGuestLedger` | · | _backup/variant_ |
| `Admin_Delete_TemporyReservations` | · |  |
| `Admin_Folio_RecallValues_DONOTEXEC` | · |  |
| `Admin_FolioCreation_OnMigration` | · | _backup/variant_ |
| `Admin_FolioDetailsCheckWithReservationDates` | · |  |
| `Admin_FOSettings_DayEnd` | · |  |
| `Admin_FOSettings_Web_DayEnd` | · |  |
| `Admin_FOSettings_Web_DayEnd_Pendings` | · |  |
| `Admin_GenerateNotCreatedFolios` | · |  |
| `Admin_jQuery` | · |  |
| `Admin_Kill_LockedTransactions` | · |  |
| `Admin_MissingFoliosHeaders_Create` | · |  |
| `Admin_Navigations_A_Select` | · |  |
| `Admin_Navigations_Mega_Select` | · |  |
| `Admin_Navigations_Mega_Select_For_UserAccess` | · |  |
| `Admin_RecreateFolioTaxMissing` | · |  |
| `Admin_RemoveIncorrectOutOfOrder` | · |  |
| `Admin_RemoveMainGuestProfileDuplicates` | · |  |
| `Admin_RemoveReservation_By_Id` | · |  |
| `Admin_Report` | · |  |
| `Admin_SchedulePosting_To_ExtraPosting` | · |  |
| `Admin_SchedulePosting_To_ExtraPosting_On_Chekin` | · |  |
| `Admin_SchedulePosting_To_ExtraPosting_On_Chekin_Dev` | · | _backup/variant_ |
| `Admin_SP` | · |  |
| `Admin_SummaryStatExecutions_Job` | · |  |
| `Admin_T_LinenChange` | T |  |
| `Admin_T_LinenChange_Dayend` | T |  |
| `Admin_T_LinenChange_Dev` | T | _backup/variant_ |
| `Admin_T_Save_UserWisePagesAndReportsAccess` | T |  |
| `Admin_T_SelectLocalStogates` | T |  |
| `Admin_T_SelectLocalStorage` | T |  |
| `Admin_Tax_Remove` | · |  |
| `Admin_TaxUpdate` | · |  |
| `Admin_TaxUpdate_FutureDates` | · |  |
| `Admin_TaxUpdate_FutureDates_FolioHistory` | · | _backup/variant_ |
| `Admin_ValidateSiteButtonAccess` | · |  |

#### `HotelResWeb_*` — 5

| Stored procedure | Type | Notes |
|---|:--:|---|
| `HotelResWeb_AuditTail_WriteToLog` | · |  |
| `HotelResWeb_AuditTail_WriteToLog_2026-06-22` | · |  |
| `HotelResWeb_AuditTail_WriteToLog_BeforeChange` | · |  |
| `HotelResWeb_AuditTail_WriteToLog_Fixed` | · |  |
| `HotelResWeb_AuditTail_WriteToLog_Old` | · | _backup/variant_ |

#### `MainMenu_*` — 8

| Stored procedure | Type | Notes |
|---|:--:|---|
| `MainMenu_M_Delete` | M |  |
| `MainMenu_M_Save` | M |  |
| `MainMenu_M_Select` | M |  |
| `MainMenu_M_Select_ById` | M |  |
| `MainMenu_M_Select_For_ComboSetup` | M |  |
| `MainMenu_M_Select_for_sync_Oulets` | M |  |
| `MainMenu_Select_For_Price` | · |  |
| `MainMenu_Update_NewPrice` | · |  |

#### `Schedule_*` — 3

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Schedule_posting_Delete` | · |  |
| `Schedule_posting_Delete_All_By_ReservationHeaderList` | · |  |
| `Schedule_posting_Histroy_Select` | · |  |

#### `sp_*` — 9

| Stored procedure | Type | Notes |
|---|:--:|---|
| `sp_alterdiagram` | · |  |
| `sp_creatediagram` | · |  |
| `sp_dropdiagram` | · |  |
| `sp_helpdiagramdefinition` | · |  |
| `sp_helpdiagrams` | · |  |
| `sp_Recover_Dropped_Objects` | · |  |
| `sp_renamediagram` | · |  |
| `sp_ReportPrintCopyLogCount` | · |  |
| `sp_upgraddiagrams` | · |  |

#### Other System / Framework procedures — 6

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Common_Occupancy_Calculation` | · |  |
| `Common_Occupancy_Calculation_Parameterized` | · |  |
| `MainMenuPriceSelectAll` | · |  |
| `PagesForAlert_T_Select` | T |  |
| `SP_ArrivalDetails_withRate` | · |  |
| `SP_CurrencyConvertion_Log` | · |  |

## Other / Uncategorized — 87 stored procedures

*Objects that did not match a domain rule — review individually.*  ·  Detail: [12-database-and-technical-architecture.md](12-database-and-technical-architecture.md)

#### `Category_*` — 4

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Category_M_Delete` | M |  |
| `Category_M_Save` | M |  |
| `Category_M_Select` | M |  |
| `Category_Select_For_Sync` | · |  |

#### `Select_*` — 16

| Stored procedure | Type | Notes |
|---|:--:|---|
| `Select_ActionButtons` | · |  |
| `Select_ActionButtonTemplate` | · |  |
| `Select_ApplicablePromotions` | · |  |
| `Select_ArrivalDepartureStayOvers_ForHK` | · |  |
| `Select_Backend_Mode` | · |  |
| `Select_DiscountTypes` | · |  |
| `Select_ItemBreakDown` | · |  |
| `Select_Itemwise_Printer_Sync` | · |  |
| `Select_LaundryInvoicePayments` | · |  |
| `Select_M_Printers` | M |  |
| `Select_M_SupplierMaster` | M |  |
| `Select_MainMenuWiseModifiers_ByActionId` | · |  |
| `Select_Printer_By_MenuCode` | · |  |
| `Select_TemplateActionButtons` | · |  |
| `Select_ValidationModes` | · |  |
| `Select_WeekDays_M_Save` | M |  |

#### Other Other / Uncategorized procedures — 67

| Stored procedure | Type | Notes |
|---|:--:|---|
| `_ActivityWiseMaintenanceTypes` | · |  |
| `AgentWiseCancellationSummary` | · |  |
| `AllProcess_Kill` | · |  |
| `AuditLogs_Set_Sessions` | · |  |
| `AuditTrail_InsertToHistory` | · | _backup/variant_ |
| `AuditTrial_W_Select` | W |  |
| `AuditTrialProcesses_W_Select` | W |  |
| `AvailabilityChart_M_Select` | M |  |
| `AvailabilityChartDetail_M_Select` | M |  |
| `CalculateMealAllocation` | · |  |
| `CheckIfRecordExists` | · |  |
| `ConfirmationSetup_T_Save` | T |  |
| `ConvertQuery2HTMLTable` | · |  |
| `DefaultMarket_M_Select` | M |  |
| `Destinity_AR_Rpt_AccAge_NOT USE` | · |  |
| `DirectPabx_CreateCommand` | · |  |
| `DROP_TRIGGERS` | · |  |
| `ExistingConfirmationSetup_T_Select` | T |  |
| `FullCottage_M_Select` | M |  |
| `Generate_C#_Class_From_Db` | · |  |
| `Getallrooms` | · |  |
| `GetCancellStatusId` | · |  |
| `GroupPropertySet_M_Select` | M |  |
| `Inquery_ArrivalInformation` | · |  |
| `InsertComplainLog_Close` | · |  |
| `InsertComplainLog_Taken` | · |  |
| `InsertComplains` | · |  |
| `Ishara1` | · |  |
| `IsharaInvoice` | · |  |
| `MonthSelect` | · |  |
| `Notes_M_Select` | M |  |
| `Preference_M_Select` | M |  |
| `RemarkTypes_M_Select` | M |  |
| `RestManageFront_ManageLogs` | · |  |
| `Save_ItemBreakDown` | · |  |
| `Save_schedule_posting` | · |  |
| `SearchAllTables` | · |  |
| `SelectCancellationPolicyList_M_Select` | M |  |
| `SelectComplainCategories` | · |  |
| `SelectComplainListSummary` | · |  |
| `SelectComplains_ById` | · |  |
| `SelectComplainTypes` | · |  |
| `SelectCurrencies` | · |  |
| `SelectSensitivityTypes` | · |  |
| `SelectSeverityLevels` | · |  |
| `SelectStatus` | · |  |
| `SideButtons_M_Select` | M |  |
| `STAAH_Configuration_Mapping` | · |  |
| `StayChangeReason_M_Select` | M |  |
| `Supervisors_M_Select` | M |  |
| `sysmail_Job` | · |  |
| `SystemSettings_M_Save` | M |  |
| `SystemSettings_M_SelectForFeatureRestriction` | M |  |
| `Table_M_Select` | M |  |
| `TelePhoneNumber_M_Select` | M |  |
| `TelMonEvent_T_Save` | T |  |
| `Test_Resercations_M_Select` | M |  |
| `testlaundry` | · |  |
| `TestSSRSMultipleTables` | · |  |
| `Today_ExpectedDeparture` | · |  |
| `UpdateComplains` | · |  |
| `UpdateNextDocNo` | · |  |
| `UpdateNextDocNoWithUpdate` | · |  |
| `UpdateProfile_M_Select` | M |  |
| `Validate_Invoice_Type` | · |  |
| `ValidateRestaurentGLMappings` | · |  |
| `YearSelect` | · |  |

