# 09 — User Roles & Permissions

> **Module:** `Areas/UserAccess` + enforcement in `WebUIMvc/Controllers/BaseController.cs`
> **Product:** Scienter HotelERP — Destinity Inspire / Destinity Horizon Front Office
> **Scope:** who can log in, which menus/screens they see, which actions (view/add/edit/delete) they may perform, which properties and reports they can reach, and how the system enforces all of this on every request.

---

## Purpose

The PMS holds sensitive commercial and financial data (rates, folios, discounts, day-end). The **UserAccess** module defines *who is allowed to do what*. It provides:

- **Users** — login accounts (linked to an employee).
- **Roles** — named job profiles (Front Office Cashier, Revenue Manager…) that bundle a default set of screen permissions.
- **Role → page permissions** — for each role, which pages are allowed and at what level (Select / Insert / Update / Delete).
- **User → role assignment** — which role(s) a user has.
- **User-wise individual access** — per-user overrides on top of role defaults.
- **User-wise properties** — which hotels a user may operate in (multi-property).
- **User-wise report access** — which reports a user may run.

**Business meaning:** a Front Office Agent can create and view reservations but cannot delete rate configuration or run financial reports; a Cashier can post and settle but cannot change tax setup; only Finance/Admin can run day-end. All of this is expressed as data in the tables below and enforced automatically — not written into each screen by hand.

---

## Relevant users / departments

| Who | Responsibility |
|---|---|
| **System Administrator** (`Admin`, `Property IT`, `HO IT`) | Create users/roles, map role→pages, grant individual access, assign properties & reports. |
| **Department heads / Managers** | Request access levels for their staff. |
| **Every user** | Subject to the permission model on every page and action; may change own password. |

---

## The permission model (data model)

The model is **multi-layered**. All tables were verified live in `HotelResWeb_Browns` (row counts shown).

```
                         ┌──────────────┐
                         │   UserRoles  │  (25 rows — job profiles)
                         └──────┬───────┘
              role defaults     │
        ┌───────────────────────┴─────────────────────────┐
        ▼                                                  ▼
┌────────────────────┐                        ┌──────────────────────┐
│ UserRoleWisePages  │  5,969 rows            │     UserWiseRoles     │ 282 rows
│ RoleId, PageId,    │  (role → page grants)  │  UserId → RoleId      │
│ IsAllowInsert/     │                        └──────────┬───────────┘
│ Update/Delete/     │                                   │ assigns role to user
│ Select             │                                   ▼
└────────────────────┘                        ┌──────────────────────┐
        ▲                                      │        Users         │ 129 rows
        │ overridden per-user by               │  Id, EmployeeId,     │
        ▼                                      │  Username, Password, │
┌──────────────────────────┐                  │  Salt, IsActive,     │
│ UserWiseIndividualAccess │ 1,030 rows       │  IsLocked, Guid      │
│ UserId, PageId,          │                  └──────────┬───────────┘
│ IsAllowInsert/Update/    │                             │ also scoped by
│ Delete/Select            │                             ▼
└──────────────────────────┘          ┌───────────────────────────────┐
                                       │ UserWiseProperties  136 rows  │ (hotels a user may open)
                                       │ UserWiseReportAccess 5,046 rows│ (reports a user may run)
                                       └───────────────────────────────┘
```

### Tables (verified columns)

| Table | Rows (live) | Key columns | Meaning |
|---|---|---|---|
| `Users` | 129 | `Id, EmployeeId, Username, Password, Salt, IsActive, IsLocked, Guid` | Login accounts. Password is salted/hashed (`Password` + `Salt`); linked to an `Employee`. |
| `UserRoles` | 25 | `Id, Name, IsActive, CreatedUserId, CreatedDateTime, LastUpdatedUserId, LastUpdatedDateTime` | Named role/job profiles. |
| `UserRoleWisePages` | 5,969 | `Id, RoleId, MainNavigationId, PageId, IsAllowInsert, IsAllowUpdate, IsAllowDelete, IsAllowSelect` | **The role permission matrix** — one row per (role, page) with four boolean rights. |
| `UserWiseIndividualAccess` | 1,030 | `Id, UserId, MainNavigationId, PageId, IsAllowInsert, IsAllowUpdate, IsAllowDelete, IsAllowSelect` | **Per-user overrides** — same shape as above, keyed by `UserId`. This is what the runtime check actually reads. |
| `UserWiseRoles` | 282 | `Id, UserId, RoleId, IsActive` | Assigns role(s) to a user (a user may hold more than one). |
| `UserWiseProperties` | 136 | `Id, UserId, PropertyId, IsActive` | Which properties (hotels) a user may open. |
| `UserWiseReportAccess` | 5,046 | `Id, UserId, ReportId, …` | Which reports a user may run. |
| `UserWisePageAndReportAccessLog` | — | `UserId, PageId, PageURL, AccessType, AccessStatus` | **Audit** of every page/report access attempt (granted or denied). |
| `UserWiseAccessLog` | — | `UserId, IPAddress, MechineName, DateTime, IsLoggedIn` | Login / logout audit. |

> **The four rights** everywhere are `IsAllowInsert / IsAllowUpdate / IsAllowDelete / IsAllowSelect`, checked at runtime with the codes **`I` / `U` / `D` / `S`**.

---

## How a page/action is authorized (the enforcement mechanism)

Authorization is enforced by a **custom MVC authorization attribute**, not by scattered `if` checks. This is the single most important fact in this document.

### 1. The attribute — `UserWisePageAccess`

Defined in **`Scienter.HotelERP.FrontOffice.WebUIMvc/Controllers/BaseController.cs`** (class `UserWisePageAccess : CustomAuthorizeAttribute : AuthorizeAttribute`).

Every controller action is decorated with a `PageId` and a permission letter. Example from `Areas/Administration/Controllers/RoomTypesController.cs` (verified):

```csharp
[UserWisePageAccess(41, "S")]  public ActionResult Landing() ...      // view
[UserWisePageAccess(41, "S")]  public PartialViewResult Grid() ...    // view grid
[UserWisePageAccess(41, "I")]  public ActionResult Form() ...         // create
[UserWisePageAccess(41, "U")]  public PartialViewResult Edit(int id)  // update
[UserWisePageAccess(41, "D")]  public PartialViewResult Delete(int id)// delete
```

Here `41` is the **PageId** of the "Room Types" screen; the letter is the required right. The same PageId therefore protects all of a screen's actions, differentiated by S/I/U/D.

### 2. What happens on every request (`OnAuthorization`)

```
1. Is SessionObjects.LoggedUser null?
        └─ yes → redirect to LoginPortalUrl (not authenticated)   [BaseController.cs:349]
2. userId = SessionObjects.LoggedUser.Id
3. IsCentralLoginEnabled?
     ├─ YES (SaaS/SSO): call CentralAccessApi
     │      GET api/user/validateaccess?token&userId&pageId&SwitchedPropertyId
     │      → granted only if HttpCode "200" AND Description "Access granted."   [BaseController.cs:381-388]
     └─ NO (local): Result = UserWiseIndividualAccessService()
                        .GetAccessPermission(userId, pageId, permission, altPages) [BaseController.cs:393]
4. Result == false ?
     ├─ AJAX request → HTTP 403 + JSON { Message, Error:"Unauthorized" }  [BaseController.cs:421-436]
     └─ non-AJAX     → throw UnauthorizedAccessException                  [BaseController.cs:442]
5. Log the attempt: SaveUserWisePageAndReportAccess(userId, pageId, url, "P", Result)  [BaseController.cs:447]
```

### 3. The actual permission decision (the SP)

`UserWiseIndividualAccessService.GetAccessPermission()` → `UserWiseIndividualAccessEntry.GetAccessPermission()` (verified in `Scienter.HotelERP.Common.Data/UserWiseIndividualAccessEntry.cs:64-72`) calls:

```
Stored procedure:  UserAccess_M_AccessPermission
Parameters:        @UserId, @PageId, @Right ('S'/'I'/'U'/'D'), @AltPages (JSON array)
Returns:           bit (true = allowed)
```

**Business meaning:** the runtime check reads the effective right for `(user, page, action)`. The `@AltPages` parameter lets one screen accept permission from an alternative page id (used where a screen is reachable from more than one menu). The individual-access table (`UserWiseIndividualAccess`) is the effective source consulted; role defaults (`UserRoleWisePages`) are propagated into it when a role is assigned/edited.

### 4. Report access — `UserWiseReportAccess` attribute

A second attribute (same file, class `UserWiseReportAccess`) protects report pages. It:
1. Resolves the `PageId` from the URL via `GetPageIdByUrl()` → SP `UserWiseIndividualReportAccess_M_Select_ByUrl` (or `Central_UserWiseIndividualReportAccess_M_Select_ByUrl` in SSO mode).
2. Checks `GetAccessPermission(userId, pageId, "S", altPages)`.
3. Denies with 403 / `UnauthorizedAccessException` and logs the attempt.

### 5. Session / login state — `SessionObjects`

Defined in `Scienter.HotelERP.Common.Domain/SessionObjects.cs`. Authorization-relevant items cached in session:

| Session property | Type | Role in auth |
|---|---|---|
| `LoggedUser` | `User` | The authenticated user (`Id`, `Username`, `LoggedProperty`). If null → not logged in. |
| `CentralLoggedUser` | `Central_UserWiseModuleLogin` | SSO identity (UserId, PropertyId, ModuleId, SessionID) used for central `validateaccess` calls. |
| `UserWiseNavigations` | `List<NavigationMain>` | The permission-filtered menu (see below). |
| `FOSettings` / `SystemSettingsWiseProperties` | settings | Property operating parameters loaded at login. |

Central token validation happens in `BaseController.CheckTokenValidity()` (validates the `TokenName` cookie against `CentralAccessApi api/user/validate`) and, in the `BaseController` constructor, `api/user/checkusersession` — an `HttpCode "301"` there means the session expired and the user is redirected to the login portal.

---

## How the menu is filtered by permission

The mega-menu the user sees is itself permission-driven, so a user never sees links they cannot open.

- **Navigation tables (verified live):** `Admin_Nav_MainNavigations` (top-level menus — e.g. *Admin*, *Res. | Front Desk*, *Reports*, *BI Engine*, *Housekeeping*, *Cashier's Desk*), `Admin_Nav_MainNavigationWiseAreas`, `Admin_Nav_AreasWisePages`, and `Admin_Navigations` (**165 rows** — the leaf pages, each with `Area`, `Controller`, `Action`, `Icon`).
- **Build:** `Admin_NavigationService.SelectMegaMenu()` (local) / `SelectMegaMenuCentral()` (SSO) returns a `List<NavigationMain>` where each `NavigationMain → NavigationArea → NavigationPages` node carries an `Access` boolean computed from the user's permissions. The result is cached in `SessionObjects.UserWiseNavigations`.
- **PageId linkage:** the `PageId` used in `[UserWisePageAccess(pageId, …)]` corresponds to a navigation page id, tying the menu, the permission tables, and the attribute together.

---

## Actual roles in the live system (verified)

Queried from `UserRoles` (IsActive = 1) in `HotelResWeb_Browns` — **these are the real role names configured for this hotel chain**, not examples:

| Id | Role name | Typical hotel function |
|---|---|---|
| 1 | **Admin** | Full system administrator. |
| 3 | **Property IT** | Property-level IT / superuser. |
| 10 | **HO IT** | Head-office IT. |
| 8 | **General Manager** | Oversight / dashboards / approvals. |
| 9 | **Front Office Manager** | FO operations management. |
| 11 | **Front Office Executive** | Senior front-desk operations. |
| 13 | **Front Office Agent** | Reception — reservations, check-in/out. |
| 17 | **Front Office Cashier** | Guest folio posting & settlement. |
| 25 | **Cashier** | Cashiering. |
| 4 | **Chief Cashier** | Cashiering supervision. |
| 18 | **Night/Income Auditor** | Night audit / day-end / income audit. |
| 5 | **Reservation Executive** | Reservations desk. |
| 6 | **Revenue Manager** | Rates, seasons, revenue configuration. |
| 12 | **Sales Manager** | Companies, markets, segments, sales. |
| 14 | **Finance Controller** | Finance oversight. |
| 15 | **Supervisor-Receivable** | Accounts receivable (city ledger). |
| 16 | **Supervisor-Payable** | Accounts payable. |
| 19 | **Executive HouseKeeper** | Housekeeping management. |
| 20 | **HouseKeeping Supervisor** | Housekeeping supervision. |
| 21 | **Executive Chef** | Kitchen / F&B. |
| 22 | **Animation** | Guest activities. |
| 23 | **SPA** | Spa operations. |
| 1031–1033 | UAT User / praveen | Test/UAT accounts (non-production personas). |

This maps cleanly onto the "typical hotel roles" (Admin, Front Office, Reservation, Cashier, Accounts, Housekeeping, POS/Restaurant, Manager, Owner) — the live chain simply uses more granular titles.

---

## Per-role screen mapping — why there is no static matrix

**The role → screen matrix is data-driven, not defined in source code.** There is no C# file that says "Cashier can see screens X, Y, Z". Instead:

- Each `(RoleId, PageId)` grant lives as a **row in `UserRoleWisePages`** with its four rights, and each `(UserId, PageId)` override lives in `UserWiseIndividualAccess`.
- These are edited at runtime through the **UserRoleWisePages** and **UserWiseIndividualAccesses** screens (see controllers below). Adding a menu page or changing a role's access is a data change, applied instantly — no redeployment.

**Verified proof it is data-driven** — distinct pages granted per role (live query on `UserRoleWisePages` joined to `UserRoles`):

| Role | Distinct pages granted |
|---|---|
| Admin | 329 |
| Cashier | 327 |
| Property IT | 324 |
| HO IT | 320 |
| Front Office Manager | 280 |
| Revenue Manager | 276 |
| Finance Controller | 266 |
| Reservation Executive | 261 |
| Front Office Executive | 258 |
| Front Office Agent | 257 |
| Front Office Cashier | 239 |

So `Admin`/`Property IT`/`HO IT` are near-total-access; operational roles get a scoped subset aligned to their job (an FO Agent ~257 pages, a Cashier heavy on posting/settlement screens, etc.). Because this is stored data, **the authoritative per-role permission set is obtained by querying `UserRoleWisePages`/`UserWiseIndividualAccess`**, e.g.:

```sql
-- All pages + rights for a role
SELECT p.PageId, p.IsAllowSelect, p.IsAllowInsert, p.IsAllowUpdate, p.IsAllowDelete
FROM UserRoleWisePages p
JOIN UserRoles r ON r.Id = p.RoleId
WHERE r.Name = 'Front Office Cashier';
```

---

## UserAccess controllers (administration of the model)

All in `Areas/UserAccess/Controllers/`. Each action is itself protected by `[UserWisePageAccess(pageId, …)]`.

| Controller | Key actions | Service | Table(s) / SP |
|---|---|---|---|
| `UsersController` | `Landing, Grid, SelectForGrid, Form, Edit, Delete, Print, Save, changepassword, Update, UpdateOwnPassword, UsersCombo` | `UserService` (+ `Central_UsersService` for SSO) | `Users`; SPs `User_M_Save`, `Users_M_Delete`, `User_M_Select_ByUserName`. Passwords stored with `Salt`. |
| `UserRolesController` | `Landing, Grid, Form, Edit, Delete, Print, Save, SelectForGrid, UserRolesCombo` | `UserRoleService` | `UserRoles`; `UserRoles_M_Save`, `UserRoles_M_Delete`. |
| `UserRoleWisePagesController` | `Landing, SelectNavigationMain, SaveUserRoleWisePages, UserRoleWisePagesSelect` | `UserRoleWisePageService` | `UserRoleWisePages`; `UserRoleWisePages_M_Save`. **This is the screen that maps a role to its allowed pages/rights.** |
| `UserWiseIndividualAccessesController` | `Landing, SelectNavigationMain, SaveUserWiseIndividualAccess, UserWiseIndividualAccessSelect` | `UserWiseIndividualAccessService` | `UserWiseIndividualAccess`; `UserWiseIndividualAccess_M_Save`. **Per-user overrides.** |
| `UserWiseRolesController` | `Landing, Form, Insert, LoadUserWiseRoles` | `UserWiseRoleService` | `UserWiseRoles`; `UserWiseRoles_M_Save`. **Assign role(s) to a user.** |
| `UserWisePropertiesController` | `Landing, Form, Insert, LoadUserWiseProperties` | `UserWisePropertyService` | `UserWiseProperties`; `UserWiseProperty_M_Save`. **Which hotels a user may open.** |
| `UserWiseReportAccessController` | `Index, SelectReportPages, Save, SelectPagesByUser` | `UserWiseReportAccessService` | `UserWiseReportAccess`; `UserWiseReportsAccess_M_Save`. **Which reports a user may run.** |

---

## Sensitive actions requiring special permission

Because permissions are page + right (S/I/U/D) based, **sensitive operations are protected by dedicating a page id (and often a distinct right) to them**. A user can be allowed to *view* a folio but denied the *right* to void/discount on it. Verified mechanisms and evidence:

| Sensitive action | How it is gated | Evidence |
|---|---|---|
| **Discount** | Posting-discount actions carry their own `PageId`/right; posting handled by SP family `GL_POSTING_FO_DISCOUNT`, `GL_POSTING_FO_EXTRA_POSTINGS_DISCOUNT`. | Cashiering controllers + discount SPs. |
| **Void posting** | Separate action/right; SPs `ExtraPostings_T_Void`, `ExtraPosting_T_Void_ByDocumentNo`. Fiscal void re-issued via `BaseController.FiscalPrinter_VoidPosting`. | `BaseController.cs`, void SPs. |
| **Rebate / allowance** | SPs `GL_POSTING_FO_REBATE`, `GL_POSTING_FO_EXTRA_POSTINGS_REBATE`, `DirectRebate`. | rebate SP family. |
| **Refund** | SP `GL_POSTING_FO_ADVANCE_REFUND`. | advance-refund SP. |
| **Day-end / night audit** | Restricted to Night/Income Auditor / Finance / Admin roles via page permission; SPs `DayEnd_CompleteDayEnd`, `DayEnd_UpdateHotelDate`. | day-end SP family + role mapping. |
| **Rate override** | Rate-change action gated by page right; SP `Reservation_T_RoomRate_Update_SpPara`. | reservation rate-update SP. |
| **Password reset / user management** | `UsersController` actions guarded by their PageId; `UpdateOwnPassword` is self-service (no admin right needed), `Update`/`Save` require the Users-page rights. | `UsersController`. |
| **Cashier login verification** | `Login/CashierLoginVerify` + `ValidatePasswordOnPopup` re-authenticate before sensitive cashier actions. | `_Root/LoginController`. |

Additionally, the **`SensitivityLevels`** master (live rows: *Normal / Medium / High*) and **`SeverityLevels`** classify records/complaints by sensitivity — used to flag data that should be handled by higher-privileged users (configured in Administration, doc 08).

---

## Step-by-step: granting a new front-desk user access

```
1. USER ACTION      Admin opens UserAccess → Users → Form, creates the login
                    (Username, Password[+Salt], linked EmployeeId).           → Users
2. SYSTEM VALIDATION UsersController.Save is guarded by [UserWisePageAccess(Users-pageId,"I")];
                    duplicate username checked via User_M_Select_ByUserName.
3. ASSIGN ROLE      Admin opens UserWiseRoles → assigns e.g. "Front Office Agent".→ UserWiseRoles
4. ASSIGN PROPERTY  Admin opens UserWiseProperties → ticks the hotel(s).        → UserWiseProperties
5. (OPTIONAL) OVERRIDE  UserWiseIndividualAccesses → fine-tune specific page rights → UserWiseIndividualAccess
6. RESULT           On next login SessionObjects.LoggedUser is set; the mega-menu
                    (UserWiseNavigations) shows only permitted pages; every action
                    is checked by UserAccess_M_AccessPermission and logged to
                    UserWisePageAndReportAccessLog.
```

---

## Business rules

1. **Deny by default:** if no grant exists for `(user, page, right)`, `UserAccess_M_AccessPermission` returns false and the action is blocked.
2. **Individual access overrides role:** `UserWiseIndividualAccess` (keyed by UserId) is the effective source read at runtime; role grants seed it.
3. **Four rights per page:** view (`S`) is independent of add/edit/delete (`I`/`U`/`D`) — a user can see without changing.
4. **Property scoping:** users only operate in properties listed in `UserWiseProperties`; SSO adds `SwitchedPropertyId` to the access check.
5. **Report access is separate:** running a report needs a `UserWiseReportAccess` grant, checked by the `UserWiseReportAccess` attribute.
6. **All access attempts are audited:** every check (granted or denied) writes to `UserWisePageAndReportAccessLog`; logins to `UserWiseAccessLog`.
7. **Account controls:** `Users.IsActive` and `Users.IsLocked` disable/lock accounts independently of role grants.
8. **SSO vs local:** when `IsCentralLoginEnabled` is true, both authentication and authorization delegate to `CentralAccessApi` (Central SSO); otherwise they resolve locally against the property DB.

---

## Expected result

A user logs in, sees only the menus and reports they are entitled to, can perform only the actions their role/individual grants permit, only within their assigned properties, and every attempt is recorded for audit. Sensitive financial actions (discount, void, rebate, refund, day-end, rate override) require the specific page-right and are therefore restricted to Finance/Manager/Auditor/Admin roles by configuration.

## Error scenarios

| Scenario | System response |
|---|---|
| Not logged in / session expired | Redirect to `LoginPortalUrl`; SSO returns `301` on `checkusersession`. |
| Action not permitted (AJAX) | HTTP **403** + JSON `{ Message: "You don't have permission to … !", Error: "Unauthorized" }`. |
| Action not permitted (full page) | `UnauthorizedAccessException` thrown → error page. |
| Report not permitted | `UserWiseReportAccess` attribute denies with 403 / exception. |
| Locked / inactive account | `Users.IsLocked` / `IsActive` prevent login regardless of grants. |
| Property not assigned | Access check fails on `SwitchedPropertyId`; user cannot open that hotel. |

## "Not found in the project" items

- **`AuditTrial*` tables in the main property DB** — not present in `HotelResWeb_Browns` (verified `sys.tables` query returned none). The application-level audit trail (`AuditTrialService` / `AuditTrialController`) targets the separate **`HotelResWeb_AuditTail`** DB (referenced in `AuditTrailEntry.cs`), the secondary sink per the Research Pack. Verified access-audit tables that *do* exist here are `UserWisePageAndReportAccessLog` and `UserWiseAccessLog`.
- **A static per-role screen matrix** — does not exist in source code; the mapping is data in `UserRoleWisePages` / `UserWiseIndividualAccess` (explained above rather than invented).

## Related documents

- `08-admin-and-configuration-process.md` — the Administration screens these permissions protect
- `00-project-overview.md` — architecture, SSO, multi-property model
- `05-cashiering-and-finance-process.md` — sensitive posting/void/rebate/refund actions
- `12-database-and-technical-architecture.md` — DB, SP naming, session handling
