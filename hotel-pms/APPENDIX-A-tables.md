# Appendix A — Complete Table Catalog

> **Every one of the 895 tables** in `HotelResWeb_Browns`, grouped by the module that owns it. Column and row counts are from the live database. Tables flagged **backup/variant** are dated snapshots, history, or `_bk`/`BeforeRemoval` twins — not the canonical live table.

> Source of truth for names/counts: `sys.tables` / `sys.columns` / `sys.partitions`. Business purpose is documented for the key tables; group descriptions cover the rest. See [README](README.md).

## Module summary

| Module | Tables | Detail doc |
|---|---:|---|
| Reservations | 87 | [03-reservation-process.md](03-reservation-process.md) |
| Front Office — In-house & Check-in/out | 11 | [04-check-in-check-out-process.md](04-check-in-check-out-process.md) |
| Front Office — Guest Profiles | 22 | [02-front-office-process.md](02-front-office-process.md) |
| Rooms & Housekeeping | 80 | [06-rooms-and-housekeeping-process.md](06-rooms-and-housekeeping-process.md) |
| Cashiering, Folio & Day-End | 177 | [05-cashiering-and-finance-process.md](05-cashiering-and-finance-process.md) |
| F&B / Profit Centres | 51 | [07-fnb-and-outlet-process.md](07-fnb-and-outlet-process.md) |
| Spa & Meal Reservations | 27 | [01-complete-hotel-process.md](01-complete-hotel-process.md) |
| Guest Portal | 72 | [02-front-office-process.md](02-front-office-process.md) |
| Administration & Configuration | 112 | [08-admin-and-configuration-process.md](08-admin-and-configuration-process.md) |
| Users & Access | 14 | [09-user-roles-and-permissions.md](09-user-roles-and-permissions.md) |
| Reporting & Analytics | 18 | [10-reports-and-business-information.md](10-reports-and-business-information.md) |
| Integrations & Notifications | 69 | [11-integrations-and-data-flow.md](11-integrations-and-data-flow.md) |
| Maintenance & Service | 37 | [06-rooms-and-housekeeping-process.md](06-rooms-and-housekeeping-process.md) |
| System / Framework | 59 | [12-database-and-technical-architecture.md](12-database-and-technical-architecture.md) |
| Other / Uncategorized | 59 | [12-database-and-technical-architecture.md](12-database-and-technical-architecture.md) |
| **Total** | **895** | |

## Reservations — 87 tables

*Bookings and their lifecycle up to check-in: reservation headers/details, rates, meal plans, deposits, groups, channels.*  ·  Detail: [03-reservation-process.md](03-reservation-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `Allotment_M_Save_Params` | 18 | 976 |  |
| `AllotmentDetails` | 8 | 1,325 |  |
| `AllotmentHeaders` | 20 | 160 |  |
| `AllotmentReconcileUpdate_Log` | 10 | 0 |  |
| `CancelledReservationLog` | 7 | 95,632 |  |
| `ChangeStay_Log` | 10 | 1,782 |  |
| `DiscountDetails` | 8 | 0 |  |
| `DiscountHeader` | 26 | 0 |  |
| `EventReservationDetails` | 12 | 0 |  |
| `EventReservations` | 12 | 0 |  |
| `FutureReservationInsert` | 6 | 634 |  |
| `FutureReservationInsert_CalmResort` | 6 | 453 |  |
| `FutureReservationInsert_DickwelaResort` | 6 | 603 |  |
| `FutureReservationInsert_Paradise` | 6 | 780 |  |
| `MemeberWiseReservationDetails` | 7 | 0 |  |
| `PackageCategories` | 2 | 0 |  |
| `PackageDetails` | 17 | 37 |  |
| `PackageHeaders` | 13 | 1 |  |
| `PackageHeadersWiseProperties` | 2 | 19 |  |
| `RateCodeCopyDetails` | 10 | 18 |  |
| `RateCodeHeaders` | 31 | 138 |  |
| `RateCodeHeadersWiseProperties` | 2 | 1,380 |  |
| `RateCodeHeadersWisePropertiesLog` | 2 | 1,095 |  |
| `RateCodeWiseFreeNights` | 8 | 0 |  |
| `RatePallets` | 13 | 0 |  |
| `Reservation_Common_SchedulePosting_Insert_Param` | 5 | 21 |  |
| `Reservation_RoomRate_BeforeAndAfterCheckInOrDayEnd` | 12 | 495,544 |  |
| `Reservation_T_RoomRate_Update_SpPara` | 6 | 114,619 |  |
| `Reservation_T_Save_Steps` | 5 | 0 |  |
| `ReservationActivityLog` | 8 | 5,379 |  |
| `ReservationAlerts` | 8 | 13,870 |  |
| `ReservationAlertsWiseProcess` | 7 | 95,713 |  |
| `ReservationBlockDates` | 9 | 0 |  |
| `ReservationCategories` | 8 | 4 |  |
| `ReservationChartLegend` | 3 | 6 |  |
| `ReservationChartUpdateLog` | 6 | 0 |  |
| `ReservationCheckinDate_ConverionRate` | 7 | 96,257 |  |
| `ReservationConfirmationSetups` | 6 | 0 |  |
| `ReservationDetails` | 31 | 284,932 | Per-room lines of a reservation |
| `ReservationDetails_181224` | 30 | 74,260 | _backup/variant_ |
| `ReservationDetails_2025_05_02` | 30 | 149,707 | _backup/variant_ |
| `ReservationDetails_BeforeComplimentaryChange` | 28 | 0 |  |
| `ReservationDetails_BeforeUpdateNewlyAddedColumns` | 27 | 0 |  |
| `ReservationDetails_JKG0000268` | 23 | 0 | _backup/variant_ |
| `ReservationDetails_StayChange_Log` | 35 | 2,040 |  |
| `ReservationDocument` | 15 | 37,711 |  |
| `ReservationEmails` | 18 | 3,260 |  |
| `ReservationEmails_History` | 15 | 0 | _backup/variant_ |
| `ReservationEmailWiseMailDetails` | 4 | 0 |  |
| `ReservationEmailWiseParameters` | 4 | 16,867 |  |
| `ReservationHeaders` | 61 | 114,640 |  |
| `ReservationHeaders_GuestProfileMissing_20220608` | 57 | 0 | _backup/variant_ |
| `ReservationHeaders_JKG0000268` | 57 | 0 | _backup/variant_ |
| `ReservationIBEPayments` | 15 | 0 |  |
| `ReservationList_SearchKeyword_temp` | 4 | 0 |  |
| `ReservationListFilterationColumns` | 35 | 141,407 |  |
| `ReservationListForGuestGroup_T_Update_Params` | 5 | 15,840 |  |
| `ReservationListSortingColumns` | 5 | 0 |  |
| `ReservationNotes` | 13 | 29 |  |
| `ReservationNoteTypes` | 5 | 1 |  |
| `ReservationPostingSettings` | 5 | 3,306,906 |  |
| `ReservationProfiles` | 5 | 117,026 |  |
| `ReservationProfiles_Duplicate_JWL_JSA` | 5 | 0 |  |
| `ReservationProfiles_Duplicated` | 5 | 4,599 |  |
| `ReservationReminderStatus` | 3 | 0 |  |
| `ReservationRoomAllocations` | 8 | 0 |  |
| `ReservationRoomRateChangeLog` | 15 | 441,101 |  |
| `ReservationSMSes` | 12 | 0 |  |
| `ReservationStatus` | 15 | 6 |  |
| `ReservationTraces` | 9 | 10,306 |  |
| `ReservationTracesWiseDates` | 11 | 17,478 |  |
| `ReservationTraceWiseDepartments` | 4 | 13,406 |  |
| `ReservationTypeLog` | 10 | 6,331 |  |
| `ReservationTypes` | 9 | 3 |  |
| `ReservationWiseAccommodationChargeCategories` | 5 | 9 |  |
| `ReservationWiseAllocationAttributes` | 9 | 164 |  |
| `ReservationWiseAppliedPromotions` | 12 | 14 |  |
| `ReservationWiseInventoryAllocation` | 6 | 719 |  |
| `ReservationWiseReceiptReportParam_Source` | 14 | 110,940 |  |
| `ReservationWiseReservationRelatedReceipt` | 22 | 1,326,568 |  |
| `ReservationWiseReservationRelatedReceiptParams` | 5 | 6,208,870 |  |
| `ReservationWiseRevenueSummary` | 46 | 326,528 |  |
| `Seasons` | 11 | 10 |  |
| `SeasonsWiseProperties` | 3 | 79 |  |
| `SeasonsWiseProperties_Exist` | 2 | 0 |  |
| `SeasonsWisePropertiesLog` | 3 | 159 |  |
| `tempInHouseReservationDetails` | 3 | 0 |  |

## Front Office — In-house & Check-in/out — 11 tables

*The in-house guest and arrival/departure: in-house reservation copies, check-in/out, walk-in, no-show.*  ·  Detail: [04-check-in-check-out-process.md](04-check-in-check-out-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `ArrivalMealTimes` | 7 | 0 |  |
| `CheckedOutReservationDetails` | 31 | 251,808 |  |
| `CheckedOutReservationDetails_BeforeUpdateNewlyAddedColumns` | 27 | 0 |  |
| `CheckedOutReservationHeaders` | 61 | 95,573 | Header archived after check-out |
| `CheckedOutReservationProfiles` | 5 | 135,041 |  |
| `InHouseReservationDetails` | 31 | 3,916 |  |
| `InHouseReservationDetails_BeforeComplimentaryChange` | 28 | 9,915,745 |  |
| `InHouseReservationDetails_BeforeUpdateNewlyAddedColumns` | 27 | 0 |  |
| `InHouseReservationDetails_StayChange_Log` | 35 | 36,897 |  |
| `InhouseReservationHeaders` | 61 | 350 | Header for a checked-in (in-house) stay |
| `InHouseReservationProfiles` | 5 | 547 |  |

## Front Office — Guest Profiles — 22 tables

*Guest master data: profiles, identity documents, history, preferences.*  ·  Detail: [02-front-office-process.md](02-front-office-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `Alergic` | 11 | 0 |  |
| `Allergies` | 2 | 0 |  |
| `FinalSelectGuestProfiles` | 27 | 0 |  |
| `GuestActivityLog` | 8 | 0 |  |
| `GuestAlergic` | 9 | 0 |  |
| `GuestComplainWiseAssignees` | 16 | 0 |  |
| `GuestMaster` | 76 | 0 |  |
| `GuestMessages` | 12 | 0 |  |
| `GuestNoteTypes` | 8 | 0 |  |
| `GuestPreferences` | 10 | 0 |  |
| `GuestProfiles` | 34 | 390,261 | Guest master profile |
| `GuestProfiles_BackupBeforeDelete` | 32 | 0 | _backup/variant_ |
| `GuestProfiles_Search` | 19 | 401,077 |  |
| `GuestProfiles_Search_BackupBeforeDelete` | 15 | 0 | _backup/variant_ |
| `GuestProfileTypes` | 6 | 5 |  |
| `GuestProfileWiseAllergies` | 7 | 133 |  |
| `GuestProfileWiseCommunicationDetails` | 9 | 798,855 |  |
| `GuestProfileWiseCommunicationDetails_BackupBeforeDelete` | 9 | 0 | _backup/variant_ |
| `GuestProfileWiseCommunicationDetails_BeforeDelete` | 9 | 1,590 | _backup/variant_ |
| `GuestProfileWiseGuestSignature` | 4 | 2 |  |
| `MissingReferenceGuestProfilesSatutaionMissing` | 3 | 0 |  |
| `ScanedPassport` | 6 | 0 |  |

## Rooms & Housekeeping — 80 tables

*Physical rooms and their readiness: room master, room status, cleaning, inspection, out-of-order.*  ·  Detail: [06-rooms-and-housekeeping-process.md](06-rooms-and-housekeeping-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `BedTypes` | 8 | 4 |  |
| `BedTypeWiseProperties` | 2 | 3 |  |
| `Floors` | 10 | 33 |  |
| `FloorsWiseProperties` | 2 | 9 |  |
| `FutureRoomCategoryUpdateBackup` | 6 | 44 | _backup/variant_ |
| `HK_AppNotifications` | 15 | 5 |  |
| `HK_AppNotifications_Viewed` | 15 | 79,305 |  |
| `HK_GuestProfile_UpdateWithAllergies_Params` | 5 | 427 |  |
| `HK_HouseKeeping_Status_Update_Log` | 7 | 35,162 |  |
| `HK_NHKM_AdditionalHouseKeepingTasks` | 11 | 3 |  |
| `HK_NHKM_CommonAreas` | 11 | 4 |  |
| `HK_NHKM_CommonAreaStatuses` | 11 | 3 |  |
| `HK_NHKM_HotelDateWiseRoomBoyAttendance` | 13 | 50 |  |
| `HK_NHKM_LinenManualChangeEntries` | 9 | 1 |  |
| `HK_NHKM_RoomWiseRoomBoyWiseAddtionalHouseKeepingTasks` | 4 | 8 |  |
| `HK_OutstandingStatementPreview` | 7 | 9 |  |
| `HK_OutstandingStatementPreview_Log` | 8 | 4 |  |
| `HK_TaskReportSavedRecords` | 43 | 27 |  |
| `HKCheckListItems` | 4 | 29 |  |
| `HKDocuments` | 28 | 70 |  |
| `HKDocumentSendingMethods` | 5 | 2 |  |
| `HKDocumentsWiseParameters` | 4 | 467 |  |
| `HKDocumentTypes` | 7 | 8 |  |
| `HKQueueReservations` | 13 | 0 |  |
| `HKQueueReservations_Log` | 15 | 0 |  |
| `HKRoomBoyWiseRoomChecklistProgress` | 20 | 151 |  |
| `HKRoomBoyWiseRoomChecklistProgress_Log` | 20 | 455 |  |
| `HKRoomCategoryWiseCheckListItemWithDefaultValues` | 10 | 174 |  |
| `HKSettings` | 15 | 12 |  |
| `Housekeeping_CleaningPatterns` | 4 | 2 |  |
| `HouseKeeping_ProcessWiseStatusChanges` | 7 | 11 |  |
| `Housekeeping_RoomWiseRoomBoys` | 11 | 78 |  |
| `Housekeeping_RoomWiseRoomBoys_Log` | 11 | 199,472 |  |
| `Housekeeping_SupervisorWiseRooms` | 9 | 38 |  |
| `Housekeeping_SupervisorWiseRooms_Log` | 11 | 25,621 |  |
| `HouseKeepingStatus` | 14 | 14 |  |
| `HouseKeepingStatusUpdate_Log` | 7 | 1,202,061 |  |
| `HouseKeepingStatusUpdate_TXN` | 6 | 671,535 |  |
| `OutOfOrderReasons` | 8 | 34 |  |
| `OutOfOrderTXN` | 13 | 1,429 |  |
| `RoomAllocationAttributes` | 4 | 3 |  |
| `RoomAllocationCategotyWise_AtHotel_WebApi` | 5 | 0 |  |
| `RoomAreas` | 10 | 39 |  |
| `RoomAreasWiseProperties` | 2 | 11 |  |
| `RoomAvailability` | 6 | 0 |  |
| `RoomBillDetails` | 8 | 477,464 |  |
| `RoomBillHeader` | 12 | 107,861 |  |
| `RoomBillWiseTaxes` | 8 | 1,308,815 |  |
| `RoomBoyDetails` | 10 | 20 |  |
| `RoomBoyDetailWiseProperties` | 2 | 0 |  |
| `RoomCategories` | 30 | 91 | Room category master |
| `RoomCategoriesWiseProperties` | 2 | 11 |  |
| `RoomCategoriesWiseRoomDetails` | 7 | 0 |  |
| `RoomCategoriesWiseRoomTypes` | 3 | 75 |  |
| `RoomCategoryUpdateBackup` | 6 | 597 | _backup/variant_ |
| `RoomChangeLogs` | 12 | 6,760 |  |
| `RoomChangeReasons` | 6 | 4 |  |
| `RoomCleaningScedule` | 7 | 0 |  |
| `RoomCleaningTypes` | 8 | 3 |  |
| `RoomDetails` | 30 | 1,087 | Room master — physical rooms |
| `RoomDetailsWiseProperties` | 2 | 650 |  |
| `RoomDetailWiseRoomFeatures` | 4 | 92 |  |
| `RoomFeatures` | 9 | 1 |  |
| `RoomInspectionDetails` | 15 | 123 |  |
| `RoomInspectionTimes` | 8 | 32 |  |
| `RoomKeyCode` | 6 | 0 |  |
| `RoomRate_MinimumRateRestriction` | 10 | 0 |  |
| `RoomRates` | 16 | 10,381,848 |  |
| `RoomRates2` | 16 | 0 |  |
| `RoomRates_PromotionSettings` | 16 | 9 |  |
| `RoomRatesWiseProperties` | 2 | 0 |  |
| `RoomRef` | 21 | 0 |  |
| `RoomStatus` | 16 | 31 | Unified room-status master (FO + housekeeping statuses) |
| `RoomStatus_araliya` | 14 | 0 |  |
| `RoomStatusCategory` | 6 | 5 |  |
| `RoomTypes` | 20 | 48 | Room type master |
| `RoomTypesWiseProperties` | 2 | 4 |  |
| `RoomWiseInventoryItems` | 9 | 0 |  |
| `STAAH_Mapping_RoomCategories` | 8 | 68 |  |
| `tempReportOccupancyByRoomNightsForDashboard` | 5 | 54 |  |

## Cashiering, Folio & Day-End — 177 tables

*The money: folios, postings, taxes, bills, settlements, advances, credit/debit notes, and the nightly day-end.*  ·  Detail: [05-cashiering-and-finance-process.md](05-cashiering-and-finance-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `AdvanceMigration_Inserted_20211204` | 6 | 0 | _backup/variant_ |
| `AdvanceMigration_NotInserted__20211204` | 4 | 0 | _backup/variant_ |
| `AdvancePaymentLinks` | 28 | 0 | Online advance payment link (IPG) |
| `AdvanceRequestDetails` | 6 | 0 | Advance/deposit request lines |
| `AdvanceRequestHeaders` | 10 | 0 | Advance/deposit request header |
| `AdvanceRequestOnline` | 28 | 0 |  |
| `AdvanceRequestOnline_History` | 26 | 0 | _backup/variant_ |
| `AdvanceRequestOnlineEmails` | 19 | 0 |  |
| `AdvanceRequestOnlinePayment` | 16 | 0 |  |
| `AdvanceRequestOnlinePaymentResponse` | 41 | 0 |  |
| `AdvanceRequestOnlinePaymentResponseTransactionSearches` | 5 | 0 |  |
| `AdvanceRequestResponses` | 8 | 0 |  |
| `BillHeader` | 47 | 0 | Finalised bill/invoice header |
| `BillSettlementDetails` | 23 | 113,844 | How a bill was settled (payment lines) |
| `BillSettlementDetails_11062025` | 22 | 1 | _backup/variant_ |
| `BillSettlementDetails_AgentCorrected_20220325` | 20 | 0 | _backup/variant_ |
| `BillToRoomLog` | 3 | 0 | Log of charges routed/transferred to a room |
| `BillTrans` | 43 | 0 |  |
| `CashierwiseOutlet` | 3 | 0 |  |
| `ChargeCodes` | 12 | 18 |  |
| `CityLedgerLog` | 10 | 13,482 |  |
| `CreditAndDebitNotesDetails` | 31 | 0 |  |
| `CreditAndDebitNotesSettlements` | 11 | 0 |  |
| `CreditAndDebitNotesWiseTaxes` | 10 | 0 |  |
| `CreditOrDebit_FolioDetails` | 33 | 30 |  |
| `CreditOrDebit_FoliowiseTaxDetails` | 14 | 75 |  |
| `CreditOrDebit_txnTaxes` | 9 | 78 |  |
| `CurrencyEncashment` | 22 | 7,176 |  |
| `CurrencyEncashmentVoid` | 22 | 82 |  |
| `DayEnd_CompleteDayEnd_SP_ExecutionSteps` | 6 | 148,623 | Ordered list of day-end execution steps |
| `Dayend_GL_BillSettlementDetails` | 38 | 112,857 |  |
| `Dayend_GL_ExtraPostingDetails` | 39 | 229,236 |  |
| `Dayend_GL_ExtraPostingDetailWiseTaxes` | 16 | 641,898 |  |
| `Dayend_GL_ExtraPostingSettlements` | 19 | 228,643 |  |
| `Dayend_MealWiseMealAllocation_Log` | 10 | 740,236 |  |
| `Dayend_RevenueAndOccupancySummary_Executions` | 10 | 132,849 |  |
| `DayEnd_T_VerifiedRoomRate` | 17 | 0 |  |
| `DayEnd_UpdateHotelDate_History` | 8 | 0 | _backup/variant_ |
| `DayEndCompleteTime` | 12 | 5,569 |  |
| `DayEndCompleteTimeWithUniqueId` | 6 | 0 |  |
| `DayEndCurrencyConversion` | 9 | 8,907,052 |  |
| `DayEndDayEndStepCompletion` | 8 | 0 |  |
| `DayEndDayEndStepCompletion_History` | 10 | 28,017 | _backup/variant_ |
| `DayEndDayEndStepCompletion_History_20240306` | 10 | 0 | _backup/variant_ |
| `DayEndGLPostingBlocks` | 6 | 0 |  |
| `DayEndRoomPickup` | 14 | 174,491 |  |
| `DayEndRoomStatus` | 7 | 5,260,287 |  |
| `DayEndSummary` | 61 | 10,058 | Frozen day-end revenue/occupancy summary |
| `DayEndSummaryGuestLedger` | 26 | 382,626 | Frozen guest-ledger snapshot from day-end |
| `DayEndSummaryGuestLedger_01122024` | 26 | 35,052 | _backup/variant_ |
| `DayEndSummaryGuestLedger_AiAgents` | 29 | 0 | _backup/variant_ |
| `DayEndSummaryGuestLedger_Base_060820224` | 26 | 954 |  |
| `DowntimeReportPendingFoliosSchedules` | 4 | 0 |  |
| `DowntimeReportPendingFoliosSchedules_4hoursTimeLapseEmailSends` | 5 | 0 |  |
| `Duplicate_Advances_ADV0000307` | 25 | 0 |  |
| `ExtraPosting_T_Void_ByDocumentNo_SP_Para` | 5 | 1,519 |  |
| `ExtraPostingDetails` | 32 | 229,893 |  |
| `ExtraPostingDetails_20230317` | 30 | 0 | _backup/variant_ |
| `ExtraPostingDetails_BeforeUpdate` | 32 | 0 |  |
| `ExtraPostingDetails_BySachith_test` | 30 | 0 | _backup/variant_ |
| `ExtraPostingDetails_History` | 32 | 0 | _backup/variant_ |
| `ExtraPostingDetails_R2R_Transfered` | 35 | 23,663 | _backup/variant_ |
| `ExtraPostingDetailWiseTaxes` | 10 | 643,680 |  |
| `ExtraPostingDetailWiseTaxes_History` | 10 | 0 | _backup/variant_ |
| `ExtraPostings_T_Void_SP_Para` | 5 | 2,184 |  |
| `ExtraPostingSettlements` | 13 | 229,285 |  |
| `ExtraPostingSettlements_History` | 13 | 0 | _backup/variant_ |
| `ExtraPostingSettlements_LaterSettlements` | 11 | 0 |  |
| `FOGuestLedger` | 18 | 0 |  |
| `Folio_TransferLog` | 14 | 52,400 |  |
| `FolioCreation_TempDate` | 3 | 0 |  |
| `FolioDetailMissedFolioWiseTaxDetails` | 16 | 34 |  |
| `FolioDetails` | 31 | 4,402 | Individual charge/payment lines on a folio |
| `FolioDetails_24082025` | 31 | 2 | _backup/variant_ |
| `FolioDetails_BeforeInsertFolio` | 31 | 15,388 | _backup/variant_ |
| `FolioDetails_BeforeRemoval` | 31 | 5,073 | _backup/variant_ |
| `FolioDetails_bk` | 24 | 0 | _backup/variant_ |
| `FolioDetails_FolioRemoval_Deleted` | 26 | 0 | _backup/variant_ |
| `FolioDetails_JKG0000268` | 24 | 0 | _backup/variant_ |
| `FolioDetails_JLK0016654` | 24 | 0 | _backup/variant_ |
| `FolioDetails_R2R_Transfered` | 33 | 131,879 | _backup/variant_ |
| `FolioDetails_StayChange_Log` | 36 | 376,779 |  |
| `FolioDetails_TEMP_20220309` | 24 | 0 | _backup/variant_ |
| `FolioDetailsBeforeDelete` | 31 | 4 | _backup/variant_ |
| `FolioDetailsHistory` | 31 | 477,469 | _backup/variant_ |
| `FolioDetailsHistory280383` | 31 | 1 | _backup/variant_ |
| `FolioDetailsMigrationCorrection` | 5 | 0 | _backup/variant_ |
| `FolioDetailsWiseDiscounts` | 14 | 0 |  |
| `FolioHeader` | 12 | 405 | Guest bill (folio) header — one running account per stay |
| `FolioHeader_BeforeRemoval` | 14 | 1,011 | _backup/variant_ |
| `FolioHeader_FolioRemoval_Deleted` | 12 | 0 | _backup/variant_ |
| `FolioHeader_JKG0000268` | 12 | 0 | _backup/variant_ |
| `FolioHeader_R2R_Transfered` | 14 | 86,611 | _backup/variant_ |
| `FolioHeaderHistory` | 12 | 107,863 | _backup/variant_ |
| `FolioInvoiceNameChangeHistory` | 8 | 333 | _backup/variant_ |
| `FolioManagementSideButtons` | 12 | 19 |  |
| `FolioWiseDiscount` | 9 | 0 |  |
| `FolioWisePostingBreakUp` | 22 | 866,267 | Detailed posting break-up per folio (used by day-end room posting) |
| `folioWisePostingBreakUP_05_03_2023_13` | 22 | 0 | _backup/variant_ |
| `FolioWisePostingBreakUp_Backup2023_04_26` | 22 | 0 | _backup/variant_ |
| `FolioWisePostingBreakUp_BeforeDayend` | 13 | 0 |  |
| `FolioWisePostingBreakUpTemp` | 10 | 0 |  |
| `FolioWisePostingBreakUpWiseTax` | 15 | 688,745 |  |
| `FoliowiseTaxDetails` | 16 | 12,432 | Tax lines calculated per folio charge |
| `FoliowiseTaxDetails_03042019` | 9 | 0 | _backup/variant_ |
| `FoliowiseTaxDetails_2025_01_20` | 16 | 8,798 | _backup/variant_ |
| `FoliowiseTaxDetails_BeforeInsertFolio` | 16 | 0 | _backup/variant_ |
| `FoliowiseTaxDetails_BeforeRemoval` | 18 | 13,382 | _backup/variant_ |
| `FoliowiseTaxDetails_FolioRemoval_Deleted` | 14 | 0 | _backup/variant_ |
| `FoliowiseTaxDetails_JKG0000268` | 13 | 0 | _backup/variant_ |
| `FoliowiseTaxDetails_R2R_Transfered` | 17 | 374,142 | _backup/variant_ |
| `FoliowiseTaxDetails_StayChange_Log` | 21 | 1,129,872 |  |
| `FoliowiseTaxDetails_TEMP_20220309` | 13 | 0 | _backup/variant_ |
| `FolioWiseTaxDetailsBeforeDelete` | 16 | 8 | _backup/variant_ |
| `FoliowiseTaxDetailsHistory` | 16 | 1,308,841 | _backup/variant_ |
| `FolioWiseTaxDetailsHistory280383` | 16 | 3 | _backup/variant_ |
| `FoliowiseTaxDetailsHistoryJKG0011659` | 14 | 0 | _backup/variant_ |
| `GL_Posting_Detail_Log` | 11 | 11,146 |  |
| `GL_POSTING_ErrTable` | 9 | 1,964 |  |
| `GL_Posting_SP_List` | 3 | 23 |  |
| `GL_Posting_SP_ReCall_Log` | 7 | 0 |  |
| `GL_Posting_Summary_Log` | 10 | 0 |  |
| `InvoicePrintCopies` | 7 | 0 |  |
| `ManuallyAddedDayEndCompleteTime` | 5 | 0 |  |
| `MemeberWiseBillSettlementDetails` | 24 | 0 |  |
| `MissingReferenceFolioDetailRoomIdMissings` | 4 | 0 |  |
| `MissingReferenceFolioHeaderFolioCompanyMissings` | 4 | 0 |  |
| `MissingReferenceFolioHeaderRoomIdMissings` | 4 | 0 |  |
| `ModuleCategories` | 6 | 0 |  |
| `ModuleCategoryWiseItem` | 8 | 0 |  |
| `ModuleCategoryWiseTXN` | 12 | 0 |  |
| `PaymentGateWaySettings` | 46 | 0 |  |
| `PaymentTypes` | 20 | 13 |  |
| `PendingBills` | 7 | 0 |  |
| `Posting_InHouse_T_Save_GeneratedDocumentNos` | 7 | 96,353 |  |
| `Posting_InHouse_T_Save_SP_Para` | 7 | 215,592 |  |
| `PostingCategories` | 10 | 15 |  |
| `PostingCategoryWiseProperties` | 2 | 5 |  |
| `PostingData_Log` | 9 | 0 |  |
| `PostingRhythms` | 8 | 4 |  |
| `PostingTypes` | 20 | 101 |  |
| `PostingTypesWiseCurrency` | 5 | 400 |  |
| `PostingTypesWiseCurrencyOld` | 5 | 0 |  |
| `PostingTypeWiseProperties` | 2 | 165 |  |
| `ProfitCenterWiseDocumentNo` | 6 | 7 |  |
| `Receipt_Details` | 5 | 0 |  |
| `Receipt_Header` | 10 | 0 |  |
| `ReservaqtionAmoutWithTaxBeforeModify` | 12 | 0 |  |
| `Save_Folio_SP_Para` | 7 | 94,254 |  |
| `Save_MultipleFolio_Para` | 6 | 72 |  |
| `SchedulePostingDetails` | 25 | 2,583 |  |
| `SchedulePostingDetailWiseTaxes` | 10 | 7,727 |  |
| `TaxGroupDetailDeleteLog` | 3 | 0 |  |
| `TaxGroupDetails` | 9 | 118 |  |
| `TaxGroupDetails_23092024` | 9 | 23 | _backup/variant_ |
| `TaxGroupDetails_Base` | 9 | 23 |  |
| `TaxGroupDetailsWiseProperties` | 2 | 3 |  |
| `TaxGroups` | 11 | 61 | Bundles of tax types applied together |
| `TaxGroups_23092024` | 11 | 9 | _backup/variant_ |
| `TaxGroupWiseProperties` | 2 | 12 |  |
| `TaxRemovalPolicies` | 4 | 3 |  |
| `TaxRemovedFolioWiseTaxDetailItems` | 12 | 88 |  |
| `TaxRemovedFoliowiseTaxDetails` | 21 | 143 |  |
| `TaxTypes` | 16 | 6 | Tax type master (VAT, SC, SSCL, TDL) |
| `TaxTypeWiseProperties` | 2 | 3 |  |
| `temp_Folio_T_ItemSplit` | 5 | 98 |  |
| `Void_CityLedgerLog` | 12 | 144 |  |
| `VoidBillHeader` | 82 | 0 |  |
| `VoidBillSettlementDetails` | 23 | 1,309 |  |
| `VoidBillTrans` | 28 | 0 |  |
| `VoidExtraPostingDetails` | 34 | 1,900 |  |
| `VoidExtraPostingDetailWiseTaxes` | 10 | 5,547 |  |
| `VoidExtraPostingSettlements` | 12 | 1,861 |  |
| `VoidFolioDetailsHistory` | 31 | 6,314 | _backup/variant_ |
| `VoidFolioHeaderHistory` | 14 | 1,183 | _backup/variant_ |
| `VoidFoliowiseTaxDetailsHistory` | 16 | 17,200 | _backup/variant_ |
| `VoidPayTrans` | 14 | 0 |  |

## F&B / Profit Centres — 51 tables

*Outlets/profit centres and posting their sales to guest folios.*  ·  Detail: [07-fnb-and-outlet-process.md](07-fnb-and-outlet-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `CategoryComNameWise` | 3 | 0 |  |
| `CategoryWiseKI` | 3 | 0 |  |
| `Core_ProfitCenterChargePrices` | 15 | 0 |  |
| `Core_ProfitCenterChargeType` | 11 | 0 |  |
| `Core_ProfitCenterItemCategories` | 10 | 0 |  |
| `Core_ProfitCenterItems` | 11 | 0 |  |
| `Core_ProfitCenterPackageDetail` | 11 | 0 |  |
| `Core_ProfitCenterPackageHeader` | 12 | 0 |  |
| `Core_ProfitCenters` | 13 | 0 | Outlet/profit-centre master |
| `Core_ProfitCenterTransactionDetail` | 14 | 0 |  |
| `Core_ProfitCenterTransactionHeader` | 12 | 0 | (unused parallel schema — 0 rows) |
| `Core_ProfitCenterTransactionPayment` | 7 | 0 |  |
| `Core_ProfitCenterTransactionTax` | 8 | 0 |  |
| `ItemBreakDown` | 7 | 0 |  |
| `ItemCategory` | 4 | 6 |  |
| `ItemCategory_History` | 5 | 0 | _backup/variant_ |
| `itemWiseKotRemarks` | 9 | 0 |  |
| `KDSSettings` | 17 | 0 |  |
| `KDSummaryDetails` | 4 | 0 |  |
| `KitchenQueue` | 29 | 0 |  |
| `MenuItem` | 8 | 0 |  |
| `MenuItemImages` | 6 | 0 |  |
| `MenuItemInfo` | 6 | 0 |  |
| `MenuItems` | 4 | 0 |  |
| `MenuItemsWiseKitchenDispllaySetup` | 9 | 0 |  |
| `MenuItemWiseAlternatives` | 9 | 0 |  |
| `MenuItemWiseAlternatives_History` | 10 | 0 | _backup/variant_ |
| `OutletWisePrinters` | 3 | 0 |  |
| `OutletWisePrinterType` | 6 | 0 |  |
| `ProfitCenter_ChargeTypes` | 10 | 4 |  |
| `ProfitCenter_ItemCategories` | 10 | 4 |  |
| `ProfitCenter_ItemPriceTypes` | 5 | 2 |  |
| `ProfitCenter_Items` | 11 | 142 |  |
| `ProfitCenter_ItemWiseCategoryWiseChargeTypeWisePricing` | 8 | 10 |  |
| `ProfitCenter_Patterns` | 10 | 0 |  |
| `ProfitCenter_txnDetails` | 11 | 9 |  |
| `ProfitCenter_txnHeader` | 13 | 7 |  |
| `ProfitCenter_txnPayments` | 6 | 3 |  |
| `ProfitCenter_txnTaxes` | 8 | 27 |  |
| `ProfitCenters` | 11 | 46 |  |
| `Profitroom_BookingConfirmAudit` | 8 | 11,532 |  |
| `Profitroom_BookingProcessLog` | 13 | 519 |  |
| `Profitroom_BookingStage` | 14 | 116,064 |  |
| `Profitroom_CompanyMapping` | 7 | 109 |  |
| `Profitroom_HotelMapping` | 6 | 5 |  |
| `Profitroom_OutboundAvailabilityXml` | 14 | 44,652 |  |
| `ProfitRoom_PmsRateUpdateTracking` | 6 | 0 |  |
| `Profitroom_PostingMapping` | 11 | 74 |  |
| `Profitroom_RateCodeMapping` | 11 | 60 |  |
| `Profitroom_RoomMapping` | 11 | 24 |  |
| `Profitroom_TypeMapping` | 7 | 0 |  |

## Spa & Meal Reservations — 27 tables

*Spa and meal reservations and their scheduling/posting.*  ·  Detail: [01-complete-hotel-process.md](01-complete-hotel-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `Core_SpaBed` | 9 | 0 |  |
| `Core_SpaBedOutOfOrder` | 13 | 0 |  |
| `Core_SpaDailyTimeSlotConfig` | 8 | 0 |  |
| `Core_SpaReservationBillSettlement` | 15 | 0 |  |
| `Core_SpaReservationDetails` | 24 | 0 |  |
| `Core_SpaReservationDetailWiseTax` | 8 | 0 |  |
| `Core_SpaReservationHeader` | 25 | 0 |  |
| `Core_SpaReservationPosting` | 18 | 0 |  |
| `Core_SpaReservationWiseTherapists` | 5 | 0 |  |
| `Core_SpaReservationWiseTimeSlots` | 6 | 0 |  |
| `Core_SpaTimeSlotTemplate` | 5 | 0 |  |
| `MealDeal_CatRef` | 3 | 0 |  |
| `MealPlanRef` | 16 | 0 |  |
| `MealPlans` | 23 | 60 |  |
| `MealPlans_123` | 23 | 1 |  |
| `MealPlansWiseProperties` | 2 | 0 |  |
| `MealPlanWiseArrivalDepartureMealPlanWiseApplicableMeals` | 8 | 480 |  |
| `MealPlanWiseArrivalDepartureMeals` | 4 | 55 |  |
| `MealReservationAdvanceRequestHeaders` | 10 | 0 |  |
| `MealReservationAdvanceRequestResponses` | 8 | 0 |  |
| `MealReservations` | 30 | 187 |  |
| `MealReservationWiseAdvancePayments` | 19 | 132 |  |
| `Meals` | 7 | 5 |  |
| `MealTimes` | 9 | 0 |  |
| `MealWiseMealAllocation` | 7 | 188 |  |
| `MealWiseMealAllocation_Log` | 9 | 144 |  |
| `MealWiseRates` | 5 | 0 |  |

## Guest Portal — 72 tables

*Guest self-service portal requests (housekeeping, laundry, services, complaints).*  ·  Detail: [02-front-office-process.md](02-front-office-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `GuestPortal_A_UserDetails_Update_Params` | 22 | 175 |  |
| `GuestPortal_ActionTypes` | 5 | 41 |  |
| `GuestPortal_AdvancePaymentPercentages` | 4 | 6 |  |
| `GuestPortal_AdvancePaymentRequests` | 29 | 0 |  |
| `GuestPortal_Allergies` | 3 | 10 |  |
| `GuestPortal_API_EmailSend_Logs` | 15 | 0 |  |
| `GuestPortal_CheckInValidation` | 8 | 8 |  |
| `GuestPortal_Documents` | 9 | 72 |  |
| `GuestPortal_EmailSettings` | 24 | 0 |  |
| `GuestPortal_EmailTemplateContent` | 35 | 3 |  |
| `GuestPortal_EmailTemplateTypes` | 4 | 66 |  |
| `GuestPortal_ErrorLogs` | 4 | 60 |  |
| `GuestPortal_FeedbackAnswers` | 8 | 135 |  |
| `GuestPortal_FeedbackCategories` | 6 | 6 |  |
| `GuestPortal_FeedbackQuestionTypes` | 12 | 31 |  |
| `GuestPortal_FeedbackRates` | 8 | 5 |  |
| `GuestPortal_FolioDetails_Settlements` | 25 | 0 |  |
| `GuestPortal_FolioHeader_Settlements` | 20 | 0 |  |
| `GuestPortal_FoliowiseTaxDetails_Settlements` | 15 | 0 |  |
| `GuestPortal_GRC` | 18 | 0 |  |
| `GuestPortal_GuestComplaintActionTypes` | 3 | 0 |  |
| `GuestPortal_GuestComplaints` | 18 | 18 |  |
| `GuestPortal_GuestComplaintTypes` | 8 | 0 |  |
| `GuestPortal_GuestComplaintWiseActions` | 8 | 0 |  |
| `GuestPortal_GuestNotifications` | 15 | 49 |  |
| `GuestPortal_GuestNotificationTypes` | 3 | 1 |  |
| `GuestPortal_GuestPortal_A_SavePOSOrder_Para` | 7 | 34 |  |
| `GuestPortal_GuestProfileWiseAllergies` | 5 | 23 |  |
| `GuestPortal_GuestProfileWiseMealPreferences` | 5 | 12 |  |
| `GuestPortal_HotelPromotions` | 12 | 5 |  |
| `GuestPortal_LaundryDetails` | 18 | 62 |  |
| `GuestPortal_LaundryHeaders` | 13 | 36 |  |
| `GuestPortal_Logins` | 27 | 217 |  |
| `GuestPortal_Logins_Logs` | 7 | 0 |  |
| `GuestPortal_MealPreferences` | 3 | 11 |  |
| `GuestPortal_MobilePOSDocuments` | 5 | 142 |  |
| `GuestPortal_MobilePOSSendDocument_Logs` | 13 | 143 |  |
| `GuestPortal_Notifications` | 25 | 390 |  |
| `GuestPortal_Pages` | 14 | 34 |  |
| `GuestPortal_Pages_2025_11_14` | 13 | 34 | _backup/variant_ |
| `GuestPortal_Pages_Old` | 13 | 0 | _backup/variant_ |
| `GuestPortal_PaymentGateWaySettings` | 46 | 1 |  |
| `GuestPortal_PaymentResponses` | 37 | 0 |  |
| `GuestPortal_POS_SendDocumentLogs` | 13 | 0 |  |
| `GuestPortal_POSCategories` | 11 | 0 |  |
| `GuestPortal_POSItems` | 61 | 0 |  |
| `GuestPortal_POSItemWiseImages` | 5 | 0 |  |
| `GuestPortal_POSOrderDetail` | 7 | 7 |  |
| `GuestPortal_POSOrderHeader` | 14 | 7 |  |
| `GuestPortal_POSOrderHeaderWiseStatuses` | 6 | 0 |  |
| `GuestPortal_Posting` | 23 | 0 |  |
| `GuestPortal_Preferences` | 10 | 0 |  |
| `GuestPortal_ProcessWiseEmailSMSSettings` | 7 | 8 |  |
| `GuestPortal_PropertySettings` | 35 | 3 |  |
| `GuestPortal_QrCodes` | 15 | 25 |  |
| `GuestPortal_QuickCheckInUpdate_Params` | 7 | 11 |  |
| `GuestPortal_ReportSettings` | 9 | 0 |  |
| `GuestPortal_RequestTypes` | 13 | 37 |  |
| `GuestPortal_RequestWiseActions` | 10 | 139 |  |
| `GuestPortal_RoomRequest` | 16 | 39 |  |
| `GuestPortal_RoomRequestActionTypes` | 3 | 0 |  |
| `GuestPortal_RoomRequestWiseActions` | 8 | 0 |  |
| `GuestPortal_ServiceInformationDetails` | 3 | 4 |  |
| `GuestPortal_ServiceInformationHeaders` | 5 | 5 |  |
| `GuestPortal_SettleBillParams` | 12 | 0 |  |
| `GuestPortal_StayChangeRequest` | 29 | 0 |  |
| `GuestPortal_T_AdvanceRequestOnline_Save_Params` | 19 | 0 |  |
| `GuestPortal_Transports` | 22 | 5 |  |
| `GuestPortal_TransportTypes` | 3 | 0 |  |
| `GuestPortal_VButlerInvitations` | 20 | 306 |  |
| `GuestPortal_VisitPlaces` | 10 | 7 |  |
| `GuestPortal_WakeupCalls` | 14 | 4 |  |

## Administration & Configuration — 112 tables

*Master/reference configuration used by every other module.*  ·  Detail: [08-admin-and-configuration-process.md](08-admin-and-configuration-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `Attributes` | 3 | 3 |  |
| `BOBSegments` | 8 | 6 |  |
| `BOBSegments_Log` | 10 | 3 |  |
| `BOBSegmentWisePMSSegments` | 8 | 9 |  |
| `BOBSegmentWisePMSSegments_Log` | 6 | 21 |  |
| `BookingSettings` | 32 | 12 |  |
| `BookingSourceDetails` | 7 | 0 |  |
| `BookingSources` | 10 | 10 |  |
| `CancellationPolicies` | 14 | 41 |  |
| `CancellationReasons` | 7 | 7 |  |
| `Colors` | 6 | 18 |  |
| `CommunicationTypes` | 3 | 4 |  |
| `Companies` | 50 | 1,220 |  |
| `Companies_Approvals` | 55 | 1,796 |  |
| `Companies_Approvals_Base` | 55 | 323 |  |
| `CompaniesWiseProperties` | 2 | 1 |  |
| `CompanyActivityLog` | 9 | 4,940 |  |
| `CompanyCategories` | 3 | 0 |  |
| `CompanyEmailTemplates` | 3 | 1 |  |
| `CompanyProfileTypes` | 9 | 11 |  |
| `CompanyProfileTypeWiseSegments` | 5 | 0 |  |
| `CompanyWiseContact` | 8 | 5 |  |
| `CompanyWiseContactDetails` | 15 | 0 |  |
| `CompanyWiseConversion` | 7 | 0 |  |
| `CompanyWiseMarkets` | 8 | 98 |  |
| `CompanyWiseRateCodes` | 8 | 158 |  |
| `CompanyWiseRateCodes1` | 8 | 0 |  |
| `CompanyWiseRates` | 11 | 9 |  |
| `CompanyWiseRepresentative` | 13 | 0 |  |
| `CompanyWiseSegments` | 8 | 18 |  |
| `ComplimentaryReasons` | 6 | 11 |  |
| `CompReasons` | 2 | 0 |  |
| `Countries` | 18 | 251 |  |
| `Countries_Araliya` | 18 | 252 |  |
| `Country` | 17 | 0 |  |
| `CRM_CampaignDetails` | 7 | 0 |  |
| `CRM_CampaignHeaders` | 9 | 0 |  |
| `CRM_DynamicSearch` | 10 | 0 |  |
| `CRM_EmailTemplate` | 10 | 0 |  |
| `CRM_Menues` | 6 | 0 |  |
| `CRM_W_Paras` | 4 | 0 |  |
| `Currencies` | 12 | 156 |  |
| `CurrencyConversion` | 8 | 1,848 |  |
| `CurrencyConversionHistory` | 10 | 7,893 | _backup/variant_ |
| `Departments` | 12 | 68 |  |
| `Designations` | 8 | 40 |  |
| `Employees` | 10 | 21 |  |
| `EmployeesWiseProperties` | 2 | 0 |  |
| `ExtensionGroups` | 8 | 42 |  |
| `Extensions` | 10 | 67 |  |
| `Extensions_Base` | 10 | 0 |  |
| `FOSettings` | 77 | 12 |  |
| `FrontOfficeInventory` | 11 | 2 |  |
| `FrontOfficeInventoryWiseProperties` | 2 | 0 |  |
| `FrontOfficeNotifications` | 9 | 3 |  |
| `FrontOfficeRoomStatus` | 13 | 5 |  |
| `FrontOfficeRoomStatusWiseProperties` | 2 | 0 |  |
| `FrontOfficeStatusWiseHouseKeepingStatus` | 4 | 12 |  |
| `Genders` | 4 | 3 |  |
| `GuestPaymentModes` | 7 | 4 |  |
| `InventoryItems` | 8 | 0 |  |
| `InventoryItemsWiseProperties` | 2 | 0 |  |
| `Languages` | 8 | 4 |  |
| `Laundry_txnDetails` | 10 | 10,568 |  |
| `Laundry_txnHeader` | 12 | 1,876 |  |
| `Laundry_txnPayments` | 5 | 1,871 |  |
| `Laundry_txnTaxes` | 7 | 31,704 |  |
| `LaundryChargeTypes` | 9 | 3 |  |
| `LaundryItemCategories` | 10 | 6 |  |
| `LaundryItemPriceTypes` | 4 | 2 |  |
| `LaundryItems` | 9 | 155 |  |
| `LaundryItemWiseCategoryWiseChargeTypeWisePricing` | 8 | 1,503 |  |
| `LaundryPatterns` | 9 | 3 |  |
| `LaundryWisePosting_M_Save_SP_Para_temp` | 11 | 0 |  |
| `Markets` | 11 | 72 |  |
| `MarketWiseProperties` | 3 | 456 |  |
| `MarketWisePropertiesLog` | 3 | 504 |  |
| `Nationalities` | 10 | 195 |  |
| `NationalityTemp` | 1 | 0 |  |
| `PaymentModes` | 26 | 95 |  |
| `PaymentModes_23July2025` | 26 | 90 |  |
| `PaymentModeWiseProperties` | 3 | 157 |  |
| `PaymentModeWiseProperties_23July2025` | 3 | 181 |  |
| `PaymentModeWisePropertiesLog` | 3 | 4 |  |
| `PMSSegments_BudgetAllocation` | 13 | 16 |  |
| `PMSSegments_BudgetAllocation_Log` | 14 | 10 |  |
| `ProfileStatus` | 9 | 4 |  |
| `Properties` | 41 | 12 |  |
| `PropertyLogos` | 2 | 20 |  |
| `PropertyLogos_Stehani` | 2 | 0 |  |
| `PropertyWiseBankDetails` | 10 | 24 |  |
| `PropertyWiseChargeTypesWiseCurrencies` | 4 | 4 |  |
| `PropertyWiseCompanyCreditPostingControl` | 6 | 10 |  |
| `Regions` | 7 | 5 |  |
| `SalesCallCategories` | 7 | 0 |  |
| `SalesStaffCategories` | 8 | 0 |  |
| `Salutations` | 3 | 11 |  |
| `Segments` | 9 | 32 |  |
| `SegmentWiseCancellationPolicy` | 4 | 17 |  |
| `StaffCategories` | 11 | 18 |  |
| `StaffDetails` | 13 | 393 |  |
| `StaffDetailsWiseProperties` | 2 | 0 |  |
| `SubRegions` | 8 | 23 |  |
| `TransferLocations` | 10 | 0 |  |
| `TransferModes` | 10 | 6 |  |
| `TransferTypes` | 11 | 32 |  |
| `TransferTypeWiseAttributes` | 4 | 20 |  |
| `TransportAttributes` | 6 | 17 |  |
| `TransportDetails` | 9 | 70 |  |
| `TransportHeaders` | 14 | 16 |  |
| `VIPLevels` | 10 | 12 |  |
| `VisitPurposes` | 10 | 8 |  |

## Users & Access — 14 tables

*Users, roles, and page/report permissions (with the central SSO store).*  ·  Detail: [09-user-roles-and-permissions.md](09-user-roles-and-permissions.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `billUserLog` | 5 | 0 |  |
| `SensitivityLevels` | 4 | 3 |  |
| `UserRoles` | 7 | 25 | Role master (25 roles) |
| `UserRoleWisePages` | 12 | 5,969 | Role → page permission mapping |
| `Users` | 12 | 129 |  |
| `UserWiseAccessLog` | 6 | 33 |  |
| `UserWiseDepartments` | 7 | 1 |  |
| `UserWiseIndividualAccess` | 12 | 1,030 | User-specific page permission overrides |
| `UserWisePageAndReportAccessLog` | 7 | 9,186,387 |  |
| `UserWiseProperties` | 8 | 136 |  |
| `UserWiseQuickNavigationAreas` | 5 | 36 |  |
| `UserWiseQuickNavigationPages` | 5 | 53 |  |
| `UserWiseReportAccess` | 3 | 5,046 |  |
| `UserWiseRoles` | 8 | 282 |  |

## Reporting & Analytics — 18 tables

*Reporting and analytics/dashboard data sources.*  ·  Detail: [10-reports-and-business-information.md](10-reports-and-business-information.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `Budget` | 10 | 0 |  |
| `BudgetAllocationCategories` | 3 | 12 |  |
| `BudgetAllocations` | 11 | 0 |  |
| `BudgetAllocations_Log` | 13 | 0 |  |
| `DashboardAPI_ColorCodes` | 2 | 8 |  |
| `DashboardAPI_CommonFormat` | 50 | 103 |  |
| `DashboardAPI_CommonFormat_bkup` | 50 | 99 |  |
| `DashboardAPI_Menues` | 8 | 35 |  |
| `DashboardAPI_Menues_bkup` | 8 | 33 |  |
| `OccupancyPropertyConfig` | 19 | 12 |  |
| `Report_Common_Occupancy_Data` | 21 | 334,678 |  |
| `ReportDetails` | 56 | 219 |  |
| `ReportPrintCopyLog` | 8 | 450 |  |
| `ReportProperties` | 32 | 18 |  |
| `ReportProperties_Temp` | 31 | 11 |  |
| `Reports_Common_OccupancySummary` | 19 | 10,674 |  |
| `ReportsHotelStatistics` | 28 | 39 |  |
| `tmpReportProperties` | 32 | 2 |  |

## Integrations & Notifications — 69 tables

*External systems and messaging: channel managers, payment gateway, SMS/email/WhatsApp, RabbitMQ, notifications.*  ·  Detail: [11-integrations-and-data-flow.md](11-integrations-and-data-flow.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `AlertProcesses` | 6 | 41 |  |
| `AlertTypes` | 11 | 9 |  |
| `BookingWhizz_M_GuestProfiles_ToSync` | 9 | 107,838 |  |
| `BookingWhizz_M_Reservations_ToSync` | 9 | 3,494,937 |  |
| `BookingWhizz_M_Stay_ToSync` | 9 | 0 |  |
| `ChannelManagerSettings` | 12 | 1 |  |
| `CMAvailabilityResponses` | 5 | 0 |  |
| `CMOTA` | 4 | 0 |  |
| `CMReservation` | 17 | 0 |  |
| `CMReservation_Log` | 17 | 0 |  |
| `CMReservationCancellationRequest` | 5 | 0 |  |
| `CMReservationRequest` | 5 | 0 |  |
| `CMReservationRooms` | 14 | 0 |  |
| `CMReservationRooms_Log` | 14 | 0 |  |
| `CMReservationUpdate` | 17 | 0 |  |
| `CMReservationUpdateRequest` | 5 | 0 |  |
| `CMReservationUpdateRooms` | 13 | 0 |  |
| `CMUpdateRanges` | 8 | 102,392 |  |
| `DirectPrint_CreateDocument_Requests` | 11 | 0 |  |
| `DocumentCategories` | 5 | 3 |  |
| `DocumentNumbers` | 6 | 471 |  |
| `DocumentNumbers_23092024` | 6 | 83 | _backup/variant_ |
| `DocumentProcess` | 3 | 2 |  |
| `DocumentProcessWiseDocument` | 9 | 6 |  |
| `DoorLockEvent` | 26 | 0 |  |
| `DoorLockEvent_KeyCodeEncorders` | 3 | 0 |  |
| `DoorLockEvent_Log` | 27 | 0 |  |
| `DoorLockEventDelete` | 22 | 0 |  |
| `EmailLog` | 11 | 0 |  |
| `EmailSettings` | 17 | 17 |  |
| `EmailTypes` | 6 | 2 |  |
| `IBE_ADMIN_Bookings` | 18 | 2 |  |
| `IBE_ADMIN_Facilities` | 5 | 12 |  |
| `IBE_ADMIN_FaqItems` | 5 | 9 |  |
| `IBE_ADMIN_HeroSlides` | 6 | 5 |  |
| `IBE_ADMIN_Offers` | 10 | 3 |  |
| `IBE_ADMIN_PolicyGroups` | 6 | 13 |  |
| `IBE_ADMIN_RoomImages` | 6 | 14 |  |
| `IBE_ADMIN_Rooms` | 11 | 5 |  |
| `IBE_ADMIN_SiteSettings` | 18 | 1 |  |
| `IBE_ADMIN_Users` | 8 | 1 |  |
| `IBESliderImages` | 11 | 0 |  |
| `Mobile_ControlLog` | 9 | 0 |  |
| `Mobile_ErrorLog` | 9 | 0 |  |
| `Mobile_MessageLog` | 9 | 0 |  |
| `mobileErrExceptions` | 5 | 0 |  |
| `MobileOutletWisePrinters` | 6 | 0 |  |
| `Notification_EmailSettings` | 7 | 0 |  |
| `Notification_Parameters` | 5 | 0 |  |
| `Notification_ParameterValues` | 20 | 0 |  |
| `Notification_Template_Schedule` | 8 | 0 |  |
| `Notification_Template_Types` | 9 | 0 |  |
| `Notification_Templates` | 8 | 0 |  |
| `PrinterSetup` | 9 | 1 |  |
| `PrinterSetup_History` | 10 | 0 | _backup/variant_ |
| `PrintingCategory` | 3 | 0 |  |
| `RabbitMQ_ActionFailures` | 5 | 0 |  |
| `RabbitMQ_ActionLogs` | 12 | 20,296 |  |
| `ServiceJobs_Emails` | 9 | 18 |  |
| `Staah_AvailabilityPush` | 10 | 3,085,162 |  |
| `Staah_CMProperties` | 8 | 0 |  |
| `Staah_CMRateCodes` | 8 | 0 |  |
| `Staah_Companies` | 6 | 13 |  |
| `Staah_DefaultSettings` | 11 | 37 |  |
| `Staah_ReservationRequests` | 15 | 29,216 |  |
| `Staah_WholeVillaCategoryWiseRoomCategories` | 5 | 0 |  |
| `StaahRateMappings` | 12 | 706 |  |
| `StaahTemp` | 2 | 0 |  |
| `WhatsApp_Outbox` | 8 | 0 |  |

## Maintenance & Service — 37 tables

*Engineering/maintenance jobs, assets, activities, complaints, lost & found.*  ·  Detail: [06-rooms-and-housekeeping-process.md](06-rooms-and-housekeeping-process.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `Activities` | 7 | 0 |  |
| `ActivityWiseMaintenanceTypes` | 8 | 0 |  |
| `Assests` | 11 | 0 |  |
| `AssestTypes` | 7 | 0 |  |
| `AssetWiseMaintenanceTypes` | 9 | 0 |  |
| `ComplainAssignees` | 6 | 0 |  |
| `ComplainCategories` | 4 | 20 |  |
| `ComplainLog` | 11 | 0 |  |
| `Complains` | 11 | 0 |  |
| `ComplainTypes` | 10 | 20 |  |
| `DamageRequest` | 18 | 0 |  |
| `DamageRequestApproval` | 9 | 0 |  |
| `DamageRequestApproval_History` | 10 | 0 | _backup/variant_ |
| `DamageRequestHeader` | 8 | 0 |  |
| `DamageRequestHeader_History` | 8 | 0 | _backup/variant_ |
| `JobExecutionRegistry` | 27 | 0 |  |
| `Jobs` | 15 | 0 |  |
| `JobStatus` | 7 | 0 |  |
| `JobType` | 6 | 0 |  |
| `JobWiseNotes` | 10 | 0 |  |
| `JobWiseStaffAllocation` | 7 | 0 |  |
| `Location` | 19 | 3 |  |
| `Location_Ref_old` | 29 | 0 |  |
| `Locations_old` | 3 | 0 |  |
| `LostAndFound` | 26 | 448 |  |
| `LostAndFoundActions` | 7 | 6 |  |
| `LostAndFoundLocations` | 8 | 6 |  |
| `LostAndFoundRelatedImages` | 5 | 600 |  |
| `LostAndFoundTypes` | 7 | 4 |  |
| `MaintenanceSettings` | 3 | 0 |  |
| `MaintenanceTypes` | 7 | 0 |  |
| `PreventiveMaintananceScedule` | 12 | 0 |  |
| `PreventiveMaintenanceSceduleWiseStaffAllocation` | 7 | 0 |  |
| `ProductionCenters` | 7 | 0 |  |
| `ProductionLevel` | 5 | 0 |  |
| `SeverityLevels` | 4 | 3 |  |
| `Tracess` | 10 | 14 |  |

## System / Framework — 59 tables

*Framework/plumbing: migrations, navigation/menu, generic helpers, staging/temp.*  ·  Detail: [12-database-and-technical-architecture.md](12-database-and-technical-architecture.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `__CMPropertiesMigrationsHistory` | 2 | 6 | _backup/variant_ |
| `__EFMigrationsHistory` | 2 | 3 | _backup/variant_ |
| `ActionButtons` | 4 | 9 |  |
| `ActionTemplate` | 4 | 8 |  |
| `Admin_CheckCategoryWiseAvailability_PreventOverbooking` | 5 | 47 |  |
| `Admin_ExtraPostingIssues` | 2 | 0 |  |
| `Admin_Folio_RatesUpdated` | 1 | 0 |  |
| `Admin_LockedTransactions` | 20 | 70,744 |  |
| `Admin_LongRunningTransactionsDoNotKill` | 2 | 0 |  |
| `Admin_MissingFoliosHeaders_Created_Log` | 6 | 22 |  |
| `Admin_Nav_AreasWisePages` | 10 | 412 |  |
| `Admin_Nav_AreasWisePages2` | 9 | 322 |  |
| `Admin_Nav_AreasWisePages_HotelSigiriya` | 10 | 0 |  |
| `Admin_Nav_MainNavigations` | 8 | 10 |  |
| `Admin_Nav_MainNavigations_Original` | 7 | 0 |  |
| `Admin_Nav_MainNavigationWiseAreas` | 9 | 50 |  |
| `Admin_Nav_MainNavigationWiseAreas_Original` | 9 | 0 |  |
| `Admin_Navigations` | 9 | 165 |  |
| `Admin_SummaryStatExecutions` | 5 | 5,957 |  |
| `Admin_tbaEmails` | 3 | 1,595 |  |
| `Admin_TempFolioDuplicates_Details` | 25 | 0 |  |
| `Admin_TempFolioDuplicates_Taxes` | 13 | 0 |  |
| `CacheSignals` | 3 | 0 |  |
| `CallTxn` | 15 | 0 |  |
| `DaysOfWeek` | 2 | 14 |  |
| `GEN_ErrTable` | 8 | 131,424 |  |
| `Migration_ReservationHeaders_Dolphin` | 61 | 4,925 | _backup/variant_ |
| `Migration_ReservationHeaders_Sigiriya` | 61 | 11,651 | _backup/variant_ |
| `Migration_ReservationHeaders_Thaala` | 61 | 2,935 | _backup/variant_ |
| `Temp_DayEnd_FrontOffice_Check` | 6 | 0 |  |
| `Temp_DayEnd_PseudoRoom_Check` | 7 | 0 |  |
| `Temp_DayEnd_RoomRates_Check` | 15 | 0 |  |
| `Temp_Insert_Folio` | 6 | 0 |  |
| `Temp_Report_RevenueDetails` | 3 | 221 |  |
| `TempBeforeUUidUpdate` | 4 | 2,504 |  |
| `TempBillCharges` | 4 | 0 |  |
| `TempCheckedOut` | 6 | 1 |  |
| `TempDiscounts` | 4 | 1,168 |  |
| `TempEdenFutureReservations` | 27 | 634 |  |
| `TempForeCast` | 4 | 0 |  |
| `TempFutureReservationInsert_DickwelaResort` | 27 | 603 |  |
| `TempGuestDetail` | 9 | 0 |  |
| `TempInhouseSelect` | 70 | 0 |  |
| `TempInvNo` | 1 | 0 |  |
| `TempParadiseFutureReservations` | 27 | 780 |  |
| `TempRemovedReservations` | 1 | 0 |  |
| `TempResDetail` | 4 | 0 |  |
| `TempReservationHeaders` | 53 | 0 |  |
| `TempReservationRooms_Res_SaveSP` | 17 | 0 |  |
| `TempReservationRoomsAll_Res_SaveSP` | 17 | 0 |  |
| `TempReservationSaveParameters` | 11 | 0 |  |
| `TempReservationSaveParametersNew` | 11 | 79,715 |  |
| `TempReservationSaveParametersNew_20231204` | 11 | 0 | _backup/variant_ |
| `TempReservationsCalmResort` | 27 | 0 |  |
| `TempReservationsRevealResort` | 27 | 453 |  |
| `TempResHeader` | 16 | 0 |  |
| `TempTable` | 3 | 397 |  |
| `TempTaxTypesToRemove` | 5 | 39 |  |
| `TmpSetMenuItems` | 19 | 0 |  |

## Other / Uncategorized — 59 tables

*Objects that did not match a domain rule — review individually.*  ·  Detail: [12-database-and-technical-architecture.md](12-database-and-technical-architecture.md)

| Table | Cols | Rows | Notes |
|---|---:|---:|---|
| `BEFOREDELETE` | 32 | 0 |  |
| `Check_IsExistsDuplicate_DocumentNo_BeforeInsert` | 6 | 96,193 | _backup/variant_ |
| `Core_ProfitroomRatePushLog` | 16 | 6,554 |  |
| `Core_Therapist` | 9 | 0 |  |
| `Core_TimeSlotMaster` | 5 | 56 |  |
| `FullCottage` | 6 | 3 |  |
| `HistoryKitchenQueue` | 29 | 0 | _backup/variant_ |
| `KithchenDisplay` | 38 | 0 |  |
| `LinenChangeLogs` | 7 | 7 |  |
| `LockedOrders` | 5 | 0 |  |
| `Months` | 2 | 12 |  |
| `NewPropertyLogos` | 3 | 4 |  |
| `Notes` | 13 | 0 |  |
| `orderType` | 3 | 6 |  |
| `PayTrans` | 11 | 0 |  |
| `PendingKOT` | 8 | 0 |  |
| `Preferences` | 8 | 0 |  |
| `PriorityLevels` | 7 | 0 |  |
| `ReasonsDetails` | 8 | 0 |  |
| `Remarks` | 5 | 205,139 |  |
| `RemarkTypes` | 4 | 3 |  |
| `ResDetail` | 31 | 0 |  |
| `roomrates123` | 16 | 0 |  |
| `SamanVilla` | 1 | 0 |  |
| `SeatNumberWiseOrderDetails` | 11 | 0 |  |
| `ServiceActions` | 10 | 7 |  |
| `ServiceCategories` | 10 | 8 |  |
| `ServiceJobHistory` | 7 | 27 | _backup/variant_ |
| `ServiceJobs` | 26 | 5 |  |
| `ServiceLocations` | 8 | 1,071 |  |
| `ServiceTypes` | 9 | 15 |  |
| `SideButtons` | 17 | 96 |  |
| `STAAH_Mapping_MealPlans` | 6 | 25 |  |
| `Statuses` | 4 | 0 |  |
| `StayChange_ProcessTimeConsum_Log` | 11 | 3,697 |  |
| `StayChangeReasons` | 13 | 10 |  |
| `sysdiagrams` | 5 | 0 |  |
| `SystemSettings` | 6 | 580 | Key-value feature-flag / parameter catalog (per property) |
| `SystemSettings_23092024` | 6 | 50 | _backup/variant_ |
| `tableIndexing` | 4 | 0 |  |
| `Tables` | 8 | 2 |  |
| `tableSyncStatus` | 3 | 0 |  |
| `TableWiseColumnType` | 2 | 0 |  |
| `TelMonEvent` | 20 | 291,542 |  |
| `TelMonEventDelete` | 21 | 0 |  |
| `TelMonLog` | 1 | 0 |  |
| `TEMP_AllotmentDetails` | 5 | 0 |  |
| `tempJson` | 1 | 0 |  |
| `tempMenuDisplaySetup` | 7 | 0 |  |
| `Test_table_for_room_posting_removable` | 3 | 0 |  |
| `TestOTA` | 2 | 0 |  |
| `tmpFerdeen` | 9 | 0 |  |
| `trmp` | 9 | 0 |  |
| `UploadedPassportDocumentDetails` | 22 | 2 |  |
| `VersionNew` | 4 | 2 |  |
| `VoucherDetails` | 18 | 0 |  |
| `WakeupTxnLog` | 8 | 0 |  |
| `WStations` | 29 | 1 |  |
| `Years` | 2 | 71 |  |

