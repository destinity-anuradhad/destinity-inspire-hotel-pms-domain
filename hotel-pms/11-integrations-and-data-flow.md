# Integrations and Data Flow

> Scienter HotelERP — Destinity Inspire Front Office. Cross-cutting document: external systems the PMS talks to.
> Every controller, service, `*Entry` method, stored procedure, table, connection string and appSetting named below was read from the actual source code / `Web.config` and, where possible, verified against the live `HotelResWeb_Browns` database. Secrets (passwords, tokens, SAS signatures) are **redacted**; non-secret endpoints/hostnames are shown verbatim. Where something could not be confirmed it is marked **"Not found in the project"** with a note on where it was checked.

---

## Purpose

The PMS is a **modular monolith** but it does not run alone. It exchanges data with payment gateways, channel managers/OTAs, a fiscal printer, SMS/email/WhatsApp providers, a reporting server, cloud storage, a central SSO service, a separate POS/inventory database, a passport-scan database and (via stored procedures) a message queue. This document catalogues each integration: **purpose, direction, trigger, endpoints/config, request/response shape, tables & SPs, and failure handling.**

## Configuration source of truth

All endpoints and connection strings live in **`Scienter.HotelERP.FrontOffice.WebUIMvc\Web.config`** (`<connectionStrings>` and `<appSettings>`). Values are environment-switched by commenting/uncommenting blocks (local `10.4.1.180`, LAN `192.168.10.139`, prod Azure `jwh-pms-db-prod...database.windows.net`). Connection strings read in code via `Configs.GetConnectionSting("<name>")`; appSettings via `Configs.GetAppSettingValue/GetAppSettingBoolValue("<key>")`.

**Connection strings (verified `Web.config` lines 8–13):**

| Name | Target DB | Used for |
|---|---|---|
| `SqlServer2016ConnectionString` | `HotelResWeb_<Property>` (Browns) | Main per-property PMS DB (default connection) |
| `CentralAccessDbConnectionString` | `CentralAccessDB` | Central SSO / cross-property users; also fiscal-printer records |
| `SqlServer2016Inventory` | `Categlog_vrV2` | POS/inventory DB (stock locations, venues, day-end GL/kitchen push) |
| `SqlServer2016POS` | `{0}/{1}/{2}/{3}` **template** | Dynamic per-property POS connection (built at runtime) |
| `PassportDbConnection` | `HotelResWeb_PassportScan` | Passport/NIC scan storage |

---

## Integration landscape (ASCII)

```
                                   ┌──────────────────────────────────────────┐
   OTA / Channel Managers          │        DESTINITY INSPIRE FRONT OFFICE     │        Central platform
 ┌───────────────────────┐  XML/API│         (ASP.NET MVC 5 monolith)          │  ┌────────────────────────┐
 │ Staah · Bookingwhizz  │────────▶│                                          │◀─│ Central SSO            │
 │ RateTiger · AxisRooms │◀────────│  Controllers ─ Services ─ *Entry ─ SPs   │  │ login.inspire.         │
 │  (OTABookingController)│ avail/  │                                          │  │  destinity.lk /        │
 └───────────────────────┘ rates   │   ┌────────────────┐  ┌──────────────┐   │  │ central-api...         │
                                    │   │ HotelResWeb_   │  │ CentralAccess│   │  │ (AutoLoginController)  │
 ┌───────────────────────┐  REST    │   │  <Property> DB │  │   DB         │   │  └────────────────────────┘
 │ Sampath IPG           │◀────────▶│   └────────────────┘  └──────────────┘   │
 │ sampath.paycorp.lk    │  (advance│                                          │  ┌────────────────────────┐
 │ (SampathIPGController) │  payment)│   RabbitMQ_* SPs ─▶ (queue, external     │  │ SSRS Report Server     │
 └───────────────────────┘          │                     consumer)            │─▶│ 10.4.1.180:8080/       │
                                    │                                          │  │  ReportServer          │
 ┌───────────────────────┐  browser │   FiscalPrinter_* SPs ─▶ JSON            │  └────────────────────────┘
 │ Fiscal printer /      │◀─POST────│                                          │
 │ DeviceHub localhost:  │  (from    │   AzureBlobStorage ──▶ Azure Blob        │  ┌────────────────────────┐
 │  1304 / 1302          │  _Layout) │                        (documents/images)│─▶│ Azure Blob (scienter)  │
 └───────────────────────┘          │                                          │  └────────────────────────┘
                                    │   Posting_InHouse_T_Save ◀── POS bill     │
 ┌───────────────────────┐  poll DB │                                          │  ┌────────────────────────┐
 │ SMS (Mobitel SOAP /   │◀─────────│   ReservationSMS ─▶ SMSSender service    │  │ Categlog_vrV2 (POS DB) │
 │  Dialog HTTP fallback)│          │   DocumentToDeliver ─▶ email/WhatsApp/   │◀─│ SqlServer2016Inventory │
 │ SMSSender.exe         │          │                        vButler           │  └────────────────────────┘
 └───────────────────────┘          │   SavePassport ─▶ HotelResWeb_PassportScan│
                                    │   SignalR client ($.connection.          │  ┌────────────────────────┐
 ┌───────────────────────┐          │     notificationHub) — server hub        │  │ HotelResWeb_PassportScan│
 │ Guest app "vButler"   │◀─────────│     currently commented out              │  └────────────────────────┘
 │ 10.4.1.180:6069       │  invite  │                                          │
 └───────────────────────┘          └──────────────────────────────────────────┘
```

---

## 1. Payment gateway — Sampath IPG (Internet Payment Gateway)

| Attribute | Detail |
|---|---|
| **Purpose** | Online advance/deposit card payments for reservations (guest pays a payment link) |
| **Direction** | Outbound (PMS → gateway) to raise the payment page; Inbound (gateway callback → PMS) for the result |
| **Trigger** | Reservation "Request Online Advance" → guest opens the link → `Advance/Payment` flow |
| **Controllers** | `Controllers/SampathIPGController.cs` (root) and `Areas/Administration/Controllers/SampathIPGController.cs` |
| **Config keys** | `serviceEndpoint = https://sampath.paycorp.lk/rest/service/proxy`; `authToken`, `hmacSecret` (**secrets redacted**); `clientIdLKR = 14003501`, `clientIdUSD = 14003502`; `returnUrl = https://localhost:44328/advance/response`; `saaSReturnUrl = https://localhost:44328/saas/paymentresponse` (`Web.config` 81–89) |
| **Request/response** | REST call to paycorp with client id + amount + currency + return URL → gateway returns a hosted payment-page URL; callback carries txn reference, response code/text, card details, settlement date |
| **Tables/SPs** | Advance-payment side: `AdvanceRequestOnline*`, `AdvancePaymentLinks`; SPs prefixed `AdvanceRequestOnline_T_*` / `OnlineAdvancePayment*`. (See `05-cashiering-and-finance-process.md` for advances.) |
| **Failure handling** | On gateway/exception the flow logs and redirects to `LoginPortalUrl`; no automatic retry loop in the controller |

> **Status caveat.** The core `PaymentRequest`/`PaymentResponse` logic in `SampathIPGController` is **largely commented out** in this checkout (the active `proceed`/response paths redirect rather than call paycorp). The **configuration and merchant IDs are present and live**, so the integration is wired but the request/response handlers are disabled/stubbed here. Verified by reading both controller files.

---

## 2. Channel Managers & OTAs — Staah, Bookingwhizz, RateTiger, AxisRooms

| Attribute | Detail |
|---|---|
| **Purpose** | Receive OTA/channel bookings into the PMS (inbound); push availability & rates back to channels (outbound) |
| **Direction** | Bidirectional |
| **Trigger** | Inbound: channel posts a booking (XML/API) into the request tables. Outbound: reservation create/update/cancel flags a range for the next availability/rate push |
| **Controller** | `Areas/Reservation/Controllers/OTABookingController.cs` — `PendingOTABookings`, `ReceivedOTABookings`, `BookingDetailByUuid`, `RePushOTABooking` (manual re-push) |
| **Domain** | `Common.Domain/OTABooking.cs` (VoucherNo, Arrival/Departure, Uuid, RequestXml, ChannelName…) |
| **Endpoints/config** | The channel **API endpoints/credentials are NOT in `Web.config`** — the inbound receiver/outbound pusher runs outside this MVC app (a separate service/job). **Not found in the project (endpoints/credentials).** |
| **Tables/SPs (verified counts in live DB)** | **Staah — 24 SPs** (`Staah_ReservationRequests_Select_ReceivedReservations`, `Staah_PendingReservationsToSync`, `Staah_ReservationRequestRePush`, `Staah_AvailabilityPush`, `Staah_Select_ReservationRequestDetails_ByXml`, `Staah_T_Reservation/GuestProfile/Stay_Data_Select` …). **Bookingwhizz — 11 SPs**. **Generic CM / RateTiger / AxisRooms — 12 `CM_*` SPs** (`CM_RateTiger_Reservation_API_Save/Update/Cancel`, `CM_RateTiger_Update_All_Availability/Rates`, `CM_AxisRooms_*`). Staging tables `CMReservation*` (9). Mapping tables `STAAH_Mapping_RoomCategories`, `STAAH_Mapping_MealPlans`. |
| **Failure handling & retry** | Failed inbound bookings remain pending in the Staah request tables; **manual retry** via the OTA Booking "Re-Push" button (`Staah_ReservationRequestRePush`). Automatic retry/scheduling is done by the external worker — **Not found in the project (MVC side)**. |
| **Data sync** | Availability/rate deltas are queued (per-property update ranges) and pushed by `Staah_AvailabilityPush` / `CM_RateTiger_Update_All_*`. |

---

## 3. Fiscal printer / DeviceHub

| Attribute | Detail |
|---|---|
| **Purpose** | Print tax-compliant fiscal invoices/receipts (Sri Lanka fiscal device) |
| **Direction** | Outbound — the **browser** posts the fiscal JSON to a **local device service** |
| **Trigger** | Cashier prints a folio invoice / posting / currency-encashment / laundry bill; direct-print flags decide auto-print |
| **Config keys** | `FiscalPrinterURL = http://localhost:1304/`; `DirectPrintURL = http://localhost:1302/`; `IsDirectPrint`, `IsCurrencyEncashmentDirectPrint`, `IsLaundryDirectPrint`, `IsPCPostingDirectPrint` (all `= 1`) (`Web.config` 100–106) |
| **Where wired** | The URL is read in `Views/Shared/_Layout.cshtml` — the client JS POSTs the generated fiscal JSON to `localhost:1304`. This is why the device runs on the **cashier's own machine** (localhost). |
| **Service/data** | `FiscalPrinterService` builds/stores the payload via `FiscalPrinterEntry` → SPs **`FiscalPrinter_DirectPrint`** and **`FiscalPrinter_FolioInvoice`** (2 SPs verified in DB). The service also exposes `PrintRequest`, `SaveFiscalPrinterResponse`, `PrintResultsByFiscalCode`, `SelectFiscalPrinter_VoidPostingJson`, `SelectFiscalPrinter_VoidFolioInvoiceJson`. |
| **Request/response** | PMS emits a `FiscalPrinter` JSON (invoice lines, taxes, totals, guest/room, UUID); the device returns a **fiscal code**, which is stored back against the request. |
| **Failure handling** | Response/fiscal code stored for audit; no explicit retry/backoff loop in code (device expected always-on at localhost). |

> The dedicated `Scienter.HotelERP.FrontOffice.DeviceHub` **project is not present in this checkout** (only the URL/consumer side is). **Not found in the project (DeviceHub project source).**

---

## 4. SMS — Mobitel (SOAP) with Dialog (HTTP) fallback

| Attribute | Detail |
|---|---|
| **Purpose** | Send guest SMS (confirmations/notifications) |
| **Direction** | Outbound |
| **Trigger** | The PMS inserts rows into the `ReservationSMS` table; a **separate console service** dispatches them |
| **Project** | `Scienter.HotelERP.FrontOffice.SMSSender` — `Program.cs` runs an **infinite loop, polling every 2 s** |
| **Provider** | **Mobitel bulk SMS SOAP** web reference `lk.mobitel.msmsent` (`SendMobitelSMS(mobileNo, message, propertyCode, account_no, username, password, send_id)`); credentials come from the SMS row itself. **Dialog HTTP fallback**: `https://richcommunication.dialog.lk/api/sms/inline/send?...&from=PizzahuT` (`DialogSMSGateway`, appears to be a test/legacy path). |
| **Data flow** | `ReservationSMSService().SelectToSent()` → send each → `UpdateStatus()` sets `IsSMSsent` + `Response`. |
| **Failure handling & retry** | Mobitel error codes (`camp_key`, `201`–`228`) → failure; the row stays unsent and is **retried on the next 2-second cycle** (effectively infinite retry until it succeeds or is cleared). Exceptions are caught per row and logged to console. |

---

## 5. Email

| Attribute | Detail |
|---|---|
| **Purpose** | Send emails (advance-payment request/response templates, and queued documents) |
| **Direction** | Outbound (SMTP) |
| **Config keys** | `emailHost = smtp.gmail.com`, `emailPort = 587`, `emailSSL = true`, `emailUsername = scienter.hotels@gmail.com`, `emailPassword` (**secret redacted**), `emailSendFromEmail`, `emailSendEmailDisplayName = Advance Payment`, `emailCc`, `emailBcc`, and master flag `IsMailEnabled = 0` (`Web.config` 49, 73–83) |
| **Controllers** | `Controllers/EmailTemplateController.cs` renders advance-request/response/offline email templates. |
| **Note** | `IsMailEnabled = 0` in this config (email dispatch off here). The dedicated **`BEMailSender` project is not present in this checkout** — the actual SMTP send worker is external. **Not found in the project (BEMailSender source).** |

---

## 6. Document delivery — Email / WhatsApp / vButler guest app

| Attribute | Detail |
|---|---|
| **Purpose** | Deliver guest documents (confirmations, bills, invitations) via a chosen channel |
| **Direction** | Outbound |
| **Trigger** | User picks a document type + sending method on a reservation/folio |
| **Controller** | `Controllers/DocumentDeliveryController.cs` — `GetDocumentTypes`, `GetDocumentSendingMethods`, `SaveDocumentToDeliver` |
| **Service/data** | `DocumentSendService` → `DocumentSendEntry`. SPs: `HKDocumentTypes_Select`, `HK_Select_DocumentSendingMethods`, `HK_Save_DocumentToDeliver`; for the guest app, `GuestPortal_Save_VButlerInvitationToDeliver`. The service branches on `ReservationType == "vButler"`. |
| **vButler config** | `VButlerImageUploadUrl = http://10.4.1.180:6069/api/upload/document`, `VButlerAPIBaseUrl = http://10.4.1.180:6069/attachments/` (`Web.config` 108–109) |
| **WhatsApp** | Offered as a *sending method* option in data, but **no WhatsApp API endpoint/config or dispatch code exists in this checkout** — the document is only **queued**. **Not found in the project (WhatsApp send implementation).** |
| **Failure handling** | Documents are saved to a delivery queue; the actual send/retry is performed by an external worker. |

---

## 7. SSRS reporting server

| Attribute | Detail |
|---|---|
| **Purpose** | Generate operational/financial reports (PDF/Excel/HTML) |
| **Direction** | Outbound (PMS → SSRS SOAP `ReportExecution2005`) |
| **Config keys** | `ReportServer = http://10.4.1.180:8080/ReportServer`; `SSRSReportsFolder = Front Office Reports Server Projects`; `ReportSourceConStr = Data Source=10.4.1.180;Initial Catalog=HotelResWeb_Browns`; `ReportServerUserName = Administrator`; `ReportAppBaseUrl = http://jwh-pms-app-tes/ReportServer/`; `ReportWidth/ReportHeight` (`Web.config` 70, 90–91, 95–98) |
| **Web reference** | `ReportDownloader/Web References/SSRSExecution/ReportExecution2005.wsdl` + generated `Reference.cs` (SOAP proxy). The `ReportDownloader` console project executes/downloads reports. |
| **Data flow** | Report name + parameters → SSRS renders against the per-property source DB → returned to the ReportViewer / downloaded. |
| **Failure handling** | Server/param errors surface in the ReportViewer; no retry in code. |

---

## 8. Azure Blob storage

| Attribute | Detail |
|---|---|
| **Purpose** | Store uploaded documents/images (guest photos, scans, attachments) |
| **Direction** | Outbound (upload) |
| **Project/class** | `Scienter.HotelERP.Common.AzureUtility/AzureBlobStorage.cs` (`AzureBlobUploader.UploadBase64Image(...)` using `CloudBlobClient`/`CloudBlobContainer` from a SAS URL) |
| **Config keys** | `FilesUploadTo = LocalStorage` (switch: `AzureBlobStorage` \| `LocalStorage`); `LocalStorage` = base64-encoded **Azure Blob SAS URL** for container `scienter` on `az900sachith.blob.core.windows.net` (**SAS signature redacted**); `ManagedIdentityClientId = 0` (managed identity off, SAS-based) (`Web.config` 39–42) |
| **Data flow** | Base64 file → `UploadBase64Image` → blob at `.../scienter/<dir>/<guid>.<ext>` → returned URI stored in the PMS DB. |
| **Failure handling** | Exceptions bubble to the caller; no explicit retry. |

> The confirmed graph edge `Utilities — Common.Utility → calls → Azure Blob Storage` (`GRAPH_REPORT.md`) corroborates this.

---

## 9. Central SSO — login.inspire.destinity.lk / CentralAccessDB

| Attribute | Detail |
|---|---|
| **Purpose** | Single sign-on across properties/modules; resolves which tenant DB the user gets |
| **Direction** | Outbound (PMS calls the central API to validate a token) |
| **Trigger** | User arrives with a token from the central portal (auto-login), or logs in locally when central login is off |
| **Config keys** | `IsCentralLoginEnabled = 1`; `LoginPortalUrl = http://login.inspire.destinity.lk/`; `CentralAccessApi = http://central-api.inspire.destinity.lk/`; SaaS: `SaasModule = true`, `LoginDb = DestinityHorizon_Saas`, `SaasServer = 161.97.175.199\SQL2019MP`, `Username`/`Password` (**secrets redacted**) (`Web.config` 48, 55–62) |
| **Controllers** | `Controllers/AutoLoginController.cs` (central token exchange → sets `SessionObjects.CentralLoggedUser`, maps tenant DB), `Controllers/SaasLoginController.cs` (local login/logout) |
| **DB** | `CentralAccessDB` (`CentralAccessDbConnectionString`); central user/module-access tables |
| **Data flow** | Token → central API validate → user + property + tenant DB creds → session established → BaseController enforces login per action. |
| **Failure handling** | On error the session is abandoned and the user is redirected to `LoginPortalUrl`; the code distinguishes auth/subscription/db error codes. A recent fix (commit `2b416cf`) hardened AutoLogin when the `Referer` header is absent. |

---

## 10. POS / Inventory DB — Categlog_vrV2

| Attribute | Detail |
|---|---|
| **Purpose** | External F&B/POS & inventory catalogue; the PMS reads a few things from it and pushes day-end data to it |
| **Direction** | Bidirectional (mostly PMS-initiated reads; day-end writes) |
| **Connection** | `SqlServer2016Inventory` → `Categlog_vrV2` (`Web.config` 12); dynamic per-property `SqlServer2016POS` template (11) |
| **Where used (verified)** | `ModulePostingEntry.SelectStockLocation` → `StockLocations_M_Select`; `ReservationHeaderEntry` venue combo → `SELECT code, description FROM Location_Ref`; `DayEndEntry` → `DayEndGL_Posting`, `POS_spInsertKitchenIssues` |
| **Inbound POS bill** | The restaurant POS calls `Administration/POSApi/SaveInHousePOSAPIPosting` → `Posting_InHouse_T_Save` to bill an order to a room. See `07-fnb-and-outlet-process.md` for the full flow. |
| **Not covered** | POS-internal catalogue/menu/recipe/stock logic — **Not found in the project (separate `Categlog_vrV2` DB)**. |

---

## 11. Passport / NIC scan DB — HotelResWeb_PassportScan

| Attribute | Detail |
|---|---|
| **Purpose** | Store scanned passport/NIC images centrally |
| **Direction** | Outbound (PMS writes/reads) |
| **Connection** | `PassportDbConnection` → `HotelResWeb_PassportScan` (`Web.config` 13) |
| **Code** | `DocumentService.SavePassportDocument(...)` → `DocumentEntry` (passport-scan DB). Flag `IsPassportHubURL = 0`. |
| **Note** | An external passport-hub scan device path is toggled by `IsPassportHubURL` (0 here); the hub device endpoint itself is **Not found in the project (config)**. |

---

## 12. RabbitMQ message queue

| Attribute | Detail |
|---|---|
| **Purpose** | Asynchronous propagation of guest/folio events to downstream consumers |
| **Direction** | Outbound producer (via SPs) → external consumer |
| **Trigger** | Guest check-in/out/room-change, folio changes, room status |
| **Tables/SPs (verified in live DB — 15 `RabbitMQ_*` SPs)** | `RabbitMQ_GuestCheckIn`, `RabbitMQ_GuestCheckOut`, `RabbitMQ_GuestRoomChange`, `RabbitMQ_RoomStatus`, `RabbitMQ_FolioDetails`, `RabbitMQ_FolioDetails_WithLineItems`, `RabbitMQ_PendingLogs_Select`, `RabbitMQ_PendingLogs_Update`, `RabbitMQ_ActionFailures_Update` (+ `_Old`/`_Dev`/`_Backup` variants). |
| **Failure handling & retry** | The queue design keeps **pending logs** and **action failures** in DB (`RabbitMQ_PendingLogs_*`, `RabbitMQ_ActionFailures_Update`) so unprocessed/failed messages can be re-selected and retried by the consumer. |
| **Note** | The **broker connection and producer/consumer process are not in this MVC checkout** — only the SP layer. The actual AMQP client is external (e.g., a `DayEndSummaryExecution`/worker service). **Not found in the project (broker client code).** |

---

## 13. Real-time — SignalR

| Attribute | Detail |
|---|---|
| **Purpose** | Push dashboard/guest-portal notifications to the browser in real time |
| **Direction** | Bidirectional (server hub ↔ browser) |
| **Client** | `Views/Shared/_Layout.cshtml` and dashboard views reference `$.connection.notificationHub` (SignalR JS client, `Microsoft.AspNet.SignalR 2.x`) |
| **Server hub** | `WebUIMvc/Models/Hubs/NotificationHub.cs` **exists but its entire body is commented out** (the intended implementation used `SqlDependency` on `GuestPortal_W_Select_Notification`). So the server-side hub is **currently disabled**. |
| **What is active** | Service-hub style notifications appear to be handled via DB + the `ServiceHub*` stack instead: `ServiceHubController` (Administration & Reservation areas), `ServiceHubService`/`ServicehubJobService`, tables `ServiceHubActivityLog`, `ServiceHubJobDetails`. |
| **Status** | SignalR client is wired; **the server `NotificationHub` is commented out** — verified by reading the file. |

---

## Not found in the project (explicit)

| Looked for | Where checked | Result |
|---|---|---|
| **Door-lock control** (unlock/lock commands, real-time lock sync, card-encoder API, lock endpoint/credentials) | `Web.config`, controllers/services, DB (`%DoorLock%` = **2 SPs `DoorLockEvent_T_Save` / `DoorLockEvent_T_InsertOrDeleteKeyCode`**, 4 `DoorLock*` tables) | **Only key-code generation/logging exists** (`DoorLockEvent*`); there is **no external door-lock system control integration** — Not found in the project |
| **Accounting/GL system integration** (QuickBooks/Xero/Tally/SAP export) | `Web.config`, code, DB | GL is **internal only** (day-end GL SPs push into `Categlog_vrV2` via `DayEndGL_Posting`); no external accounting-system connector — Not found in the project |
| **Channel-manager API endpoints/credentials** | `Web.config`, code | Not present (external worker) — Not found in the project |
| **WhatsApp send implementation** | code/config | Only a queued "sending method"; no dispatcher — Not found in the project |
| **DeviceHub / BEMailSender / IPG project source** | solution folder | These projects are **not in this checkout** (only their config/consumers) — Not found in the project |

---

## Cross-cutting failure-handling summary

- **DB-side:** posting/day-end SPs wrap work in `BEGIN TRY…CATCH`, roll back, log to `GEN_ErrTable`, and re-raise (see `05`/`07`).
- **Queue durability:** RabbitMQ pending/failed logs persist in DB for reprocessing.
- **SMS:** infinite 2-second retry loop until sent.
- **OTA:** manual re-push of failed bookings.
- **SSO/IPG:** redirect to central login on failure.
- **Fiscal/SSRS/Azure:** best-effort; results/URIs stored; no explicit retry loops.

## Related documents

- `07-fnb-and-outlet-process.md` — POS API (`Posting_InHouse_T_Save`) and `Categlog_vrV2` details.
- `05-cashiering-and-finance-process.md` — advances (IPG), fiscal invoice printing, day-end GL.
- `03-reservation-process.md` — OTA/channel bookings entering reservations.
- `12-database-and-technical-architecture.md` — multi-DB, connection strings, multi-tenant SaaS.
- `00-project-overview.md` — solution projects and overall architecture.
