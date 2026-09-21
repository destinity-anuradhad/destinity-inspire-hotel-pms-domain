#!/usr/bin/env python3
# Generates APPENDIX-A-tables.md and APPENDIX-B-stored-procedures.md
# 100% coverage: every table + every SP is classified into a module and listed.
import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.dirname(HERE)  # docs/hotel-pms

# ---- Module definitions: label -> doc link -------------------------------
RES     = ("Reservations", "03-reservation-process.md")
FO_STAY = ("Front Office — In-house & Check-in/out", "04-check-in-check-out-process.md")
FO_GST  = ("Front Office — Guest Profiles", "02-front-office-process.md")
HK      = ("Rooms & Housekeeping", "06-rooms-and-housekeeping-process.md")
CASH    = ("Cashiering, Folio & Day-End", "05-cashiering-and-finance-process.md")
FNB     = ("F&B / Profit Centres", "07-fnb-and-outlet-process.md")
SPA     = ("Spa & Meal Reservations", "01-complete-hotel-process.md")
GP      = ("Guest Portal", "02-front-office-process.md")
ADMIN   = ("Administration & Configuration", "08-admin-and-configuration-process.md")
UA      = ("Users & Access", "09-user-roles-and-permissions.md")
REPORT  = ("Reporting & Analytics", "10-reports-and-business-information.md")
INTEG   = ("Integrations & Notifications", "11-integrations-and-data-flow.md")
MAINT   = ("Maintenance & Service", "06-rooms-and-housekeeping-process.md")
SYS     = ("System / Framework", "12-database-and-technical-architecture.md")
OTHER   = ("Other / Uncategorized", "12-database-and-technical-architecture.md")

ORDER = [RES, FO_STAY, FO_GST, HK, CASH, FNB, SPA, GP, ADMIN, UA, REPORT, INTEG, MAINT, SYS, OTHER]

# Short description shown under each module header
MODDESC = {
 RES[0]:  "Bookings and their lifecycle up to check-in: reservation headers/details, rates, meal plans, deposits, groups, channels.",
 FO_STAY[0]: "The in-house guest and arrival/departure: in-house reservation copies, check-in/out, walk-in, no-show.",
 FO_GST[0]: "Guest master data: profiles, identity documents, history, preferences.",
 HK[0]:   "Physical rooms and their readiness: room master, room status, cleaning, inspection, out-of-order.",
 CASH[0]: "The money: folios, postings, taxes, bills, settlements, advances, credit/debit notes, and the nightly day-end.",
 FNB[0]:  "Outlets/profit centres and posting their sales to guest folios.",
 SPA[0]:  "Spa and meal reservations and their scheduling/posting.",
 GP[0]:   "Guest self-service portal requests (housekeeping, laundry, services, complaints).",
 ADMIN[0]:"Master/reference configuration used by every other module.",
 UA[0]:   "Users, roles, and page/report permissions (with the central SSO store).",
 REPORT[0]:"Reporting and analytics/dashboard data sources.",
 INTEG[0]:"External systems and messaging: channel managers, payment gateway, SMS/email/WhatsApp, RabbitMQ, notifications.",
 MAINT[0]:"Engineering/maintenance jobs, assets, activities, complaints, lost & found.",
 SYS[0]:  "Framework/plumbing: migrations, navigation/menu, generic helpers, staging/temp.",
 OTHER[0]:"Objects that did not match a domain rule — review individually.",
}

# ---- Curated one-line purposes for the most important tables --------------
TPURPOSE = {
 "ReservationHeader":"Booking header (dates, source, status, guest link) — core reservation record",
 "ReservationDetails":"Per-room lines of a reservation",
 "InhouseReservationHeaders":"Header for a checked-in (in-house) stay",
 "InhouseReservationDetails":"Per-room lines for an in-house stay",
 "InhouseReservationProfiles":"Guest profile snapshot for the in-house stay",
 "CheckedOutReservationHeaders":"Header archived after check-out",
 "FolioHeader":"Guest bill (folio) header — one running account per stay",
 "FolioDetails":"Individual charge/payment lines on a folio",
 "FolioWisePostingBreakUp":"Detailed posting break-up per folio (used by day-end room posting)",
 "FoliowiseTaxDetails":"Tax lines calculated per folio charge",
 "BillHeader":"Finalised bill/invoice header",
 "BillSettlementDetails":"How a bill was settled (payment lines)",
 "BillToRoomLog":"Log of charges routed/transferred to a room",
 "AdvanceRequestHeaders":"Advance/deposit request header",
 "AdvanceRequestDetails":"Advance/deposit request lines",
 "AdvancePaymentLinks":"Online advance payment link (IPG)",
 "RoomDetails":"Room master — physical rooms",
 "RoomTypes":"Room type master",
 "RoomCategories":"Room category master",
 "RoomStatus":"Unified room-status master (FO + housekeeping statuses)",
 "GuestProfiles":"Guest master profile",
 "TaxTypes":"Tax type master (VAT, SC, SSCL, TDL)",
 "TaxGroups":"Bundles of tax types applied together",
 "DayEndSummary":"Frozen day-end revenue/occupancy summary",
 "DayEndSummaryGuestLedger":"Frozen guest-ledger snapshot from day-end",
 "DayEnd_CompleteDayEnd_SP_ExecutionSteps":"Ordered list of day-end execution steps",
 "SystemSettings":"Key-value feature-flag / parameter catalog (per property)",
 "UserRoles":"Role master (25 roles)",
 "UserRoleWisePages":"Role → page permission mapping",
 "UserWiseIndividualAccess":"User-specific page permission overrides",
 "Core_ProfitCenters":"Outlet/profit-centre master",
 "Core_ProfitCenterTransactionHeader":"(unused parallel schema — 0 rows)",
}

# ---- Classifier ----------------------------------------------------------
PREFIX_RULES = [
 (r'^CheckedOut', FO_STAY),
 (r'^(Inhouse|InHouse)', FO_STAY),
 (r'^(QuickCheck|WalkIn|Walkin|Arrival|Departure|NoShow|ArrivedStay)', FO_STAY),
 (r'^Reservation', RES),
 (r'^Advance', CASH),
 (r'^(Folio|Bill|Void|Credit|Debit|Settlement|Refund|CurrencyEncashment|Encashment)', CASH),
 (r'^(Posting|ExtraPosting|SchedulePosting|ModulePosting|ModuleCategor|FolioWisePosting|ChargeCode|ChargeType|PostingCategor|PostingType|PostingRhythm|ProfitCenterWise|Profit_Center|ProfitCenterWisePosting)', CASH),
 (r'^(DayEnd|Dayend|NightAudit)', CASH),
 (r'^(Tax|Foliowise)', CASH),
 (r'^(GL|GuestLedger|GeneralLedger)', CASH),
 (r'^(PaymentMode|PaymentPolic|GuestPaymentMode)', ADMIN),
 (r'^Payment', CASH),
 (r'^(HouseKeeping|HK|OutOfOrder|OOO|Turndown|Inspection|RoomStatus|RoomCleaning|RoomBoy|SupervisorReview|RoomInspection)', HK),
 (r'^(Room|Floor|Bed|Wing|Block)', HK),
 (r'^(Core_ProfitCenter|ProfitCenter|Profitroom|Profit|POS|Menu|Kitchen|Outlet|StockLocation)', FNB),
 (r'^(Core_Spa|Spa|Therapist|TimeSlot)', SPA),
 (r'^Meal', SPA),
 (r'^(GuestPortal|GuestPotal)', GP),
 (r'^Guest', FO_GST),
 (r'^(Company|Companies|Contact)', ADMIN),
 (r'^(Segment|Market|BookingSource|BookingSetting|Source)', ADMIN),
 (r'^(Rate|Season|Package|Promotion|Offer|Discount|Allotment)', RES),
 (r'^Currenc', ADMIN),
 (r'^(User|Role|Access|Central|Login|Token|Permission|Sensitivity)', UA),
 (r'^(Staah|Bookingwhizz|CM|CMReservation|RateTiger|AxisRooms|OTA|Channel)', INTEG),
 (r'^(RabbitMQ|Notification|Alert|Email|SMS|Whatsapp|WhatsApp|Document|Message|IPG|Sampath|Paycorp|DoorLock|Fiscal|Device|ServiceHub|WebApi|DirectPrint|Print)', INTEG),
 (r'^(Report|Reports|Analysis|Dashboard|Budget|Forecast|Occupancy|Revenue|Statistic)', REPORT),
 (r'^Laundry', ADMIN),
 (r'^(Job|Asset|Activity|Maintenance|Preventive|Production|Location|Complain|LostAndFound|LostFound|Trace|Severity)', MAINT),
 (r'^(Country|Nationalit|Language|Gender|Salutation|VIP|Designation|Department|Staff|Employee|GuestType|ProfileType|ProfileStatus|CommunicationType|CancellationPolic|CancellationReason|Color|Attribute|Transfer|Transport|AlertType|Extension|VisitPurpose)', ADMIN),
 (r'^(GEN|Genral|General|sp|SP|__|EF|Migration|ActionButton|ActionTemplate|Navigation|MegaNav|MainMenu|Admin_|Page|Module|DaysOfWeek)', SYS),
 (r'^(Temp|Tmp)', SYS),
]
INFIX_FALLBACK = [
 (r'(Folio|Bill|Posting|Tax|DayEnd|Advance|Settlement|Ledger|Encashment|Rebate)', CASH),
 (r'(Reservation|Booking)', RES),
 (r'(CheckIn|CheckOut|Inhouse|WalkIn|NoShow)', FO_STAY),
 (r'Guest', FO_GST),
 (r'(Room|HouseKeep|Inspection)', HK),
 (r'(ProfitCenter|POS)', FNB),
 (r'Spa', SPA),
 (r'(Report|Dashboard)', REPORT),
 (r'(Staah|Channel|Notification|RabbitMQ|Email|SMS)', INTEG),
 (r'(User|Access|Role)', UA),
]
# Extra rules (case-insensitive) to catch spelling/case variants + more domains
EXTRA_RULES = [
 (r'^CRM', ADMIN),
 (r'^(IBE|BookingEngine|BookingWhizz)', INTEG),
 (r'^(BOBSegment|PMSSegment|SegmentWise)', ADMIN),
 (r'^(Recipe|Combo|KDS|PosItem|Kitchen|ItemCategory|CategoryWiseKI|CategoryComName|ComboItem|Item)', FNB),
 (r'^(Region|SubRegion)', ADMIN),
 (r'^Propert', ADMIN),
 (r'^(Passport|Scaned|Scanned|ScanPassport|NIC)', FO_GST),
 (r'^(Alerg|Allerg)', FO_GST),
 (r'^Mobile', INTEG),
 (r'^(FOSettings|FrontOfficeSetting|FrontOffice)', ADMIN),
 (r'^(Receipt|Invoice|CreateInvoice|AccountCode|Cashier)', CASH),
 (r'^Getthese', FO_STAY),
 (r'^ChangeStay', RES),
 (r'^(Complimentary|CompReason|Compliment)', ADMIN),
 (r'^(Assest|Asset|Damage|Lostand|LostAndFound|LostFound|Activit)', MAINT),
 (r'^(FrontOfficeInventory|InventoryItem|Inventory)', ADMIN),
 (r'^(SalesCall|Sales)', ADMIN),
 (r'^Countr', ADMIN),
 (r'^(Housekeeping|OutofOrder|Outof)', HK),
 (r'^(Cache|HotelResWeb|Common|CallTxn|GetConnection|Schedule)', SYS),
]
def classify(name):
    for pat, mod in PREFIX_RULES:
        if re.match(pat, name):
            return mod
    for pat, mod in EXTRA_RULES:
        if re.match(pat, name, re.I):
            return mod
    for pat, mod in INFIX_FALLBACK:
        if re.search(pat, name):
            return mod
    return OTHER

VARIANT = re.compile(r'(_OLD$|_OLD_|_Old|_Dev|_OPT|_NEW$|_NEW_|_New\b|_test|_Test|Test$|backup|Backup|_bk$|_bk_|BeforeRemoval|BeforeInsert|BeforeDelete|History|Migration|_R2R|_JKG|_JLK|_AiAgents|_Corrected|_Deleted|_\d{6,8}$|_\d{4}$|_\d{2}_\d{2}_\d{4}|_\d{4}_\d{2}_\d{2})')
def variant_flag(name):
    return "backup/variant" if VARIANT.search(name) else ""

def sp_type(name):
    if '_M_' in name or name.endswith('_M'): return 'M'
    if '_T_' in name or name.endswith('_T'): return 'T'
    if '_R_' in name or name.endswith('_R'): return 'R'
    if '_W_' in name or name.endswith('_W'): return 'W'
    return ''

# ---- Load data -----------------------------------------------------------
tables = []
with open(os.path.join(HERE,"tables_meta.tsv"), encoding="utf-8", errors="ignore") as f:
    for line in f:
        line=line.rstrip("\n")
        if not line.strip(): continue
        parts = line.split("\t")
        if len(parts) < 3: continue
        name = parts[0].strip()
        try: cols=int(parts[1]); rows=int(parts[2])
        except: cols=0; rows=0
        tables.append((name,cols,rows))

procs = []
with open(os.path.join(HERE,"procs_all.txt"), encoding="utf-8", errors="ignore") as f:
    for line in f:
        n=line.strip()
        if n: procs.append(n)

# ---- Group ---------------------------------------------------------------
def group(items):
    g = {m[0]: [] for m in ORDER}
    for it in items:
        name = it if isinstance(it,str) else it[0]
        mod = classify(name)
        g[mod[0]].append(it)
    return g

tg = group(tables)
pg = group(procs)

def fmt_int(n):
    return f"{n:,}"

# ---- Render tables appendix ----------------------------------------------
def render_tables():
    L=[]
    A=L.append
    A("# Appendix A — Complete Table Catalog")
    A("")
    A(f"> **Every one of the {len(tables)} tables** in `HotelResWeb_Browns`, grouped by the module that owns it. "
      "Column and row counts are from the live database. Tables flagged **backup/variant** are dated snapshots, "
      "history, or `_bk`/`BeforeRemoval` twins — not the canonical live table.")
    A("")
    A("> Source of truth for names/counts: `sys.tables` / `sys.columns` / `sys.partitions`. "
      "Business purpose is documented for the key tables; group descriptions cover the rest. See [README](README.md).")
    A("")
    A("## Module summary")
    A("")
    A("| Module | Tables | Detail doc |")
    A("|---|---:|---|")
    for m in ORDER:
        c=len(tg[m[0]])
        if c: A(f"| {m[0]} | {c} | [{m[1]}]({m[1]}) |")
    A(f"| **Total** | **{len(tables)}** | |")
    A("")
    for m in ORDER:
        rows = sorted(tg[m[0]], key=lambda x:x[0].lower())
        if not rows: continue
        A(f"## {m[0]} — {len(rows)} tables")
        A("")
        A(f"*{MODDESC.get(m[0],'')}*  ·  Detail: [{m[1]}]({m[1]})")
        A("")
        A("| Table | Cols | Rows | Notes |")
        A("|---|---:|---:|---|")
        for name,cols,rw in rows:
            note = TPURPOSE.get(name,"")
            vf = variant_flag(name)
            if vf: note = (note+" · " if note else "")+f"_{vf}_"
            A(f"| `{name}` | {cols} | {fmt_int(rw)} | {note} |")
        A("")
    return "\n".join(L)+"\n"

# ---- Render SP appendix --------------------------------------------------
def render_procs():
    L=[]
    A=L.append
    A("# Appendix B — Complete Stored Procedure Catalog")
    A("")
    A(f"> **Every one of the {len(procs)} stored procedures** in `HotelResWeb_Browns`, grouped by module, then by name prefix. "
      "Type tag: **M**=Master/config · **T**=Transaction · **R**=Report/read · **W**=Wide report · (blank)=other. "
      "**backup/variant** marks `_OLD`/`_Dev`/`_OPT`/`_NEW`/`test`/dated twins — not the canonical procedure.")
    A("")
    A("> Source of truth: `sys.procedures`. See [README](README.md) and [12-database-and-technical-architecture](12-database-and-technical-architecture.md) for the naming convention.")
    A("")
    A("## Module summary")
    A("")
    A("| Module | Stored procedures | Detail doc |")
    A("|---|---:|---|")
    for m in ORDER:
        c=len(pg[m[0]])
        if c: A(f"| {m[0]} | {c} | [{m[1]}]({m[1]}) |")
    A(f"| **Total** | **{len(procs)}** | |")
    A("")
    for m in ORDER:
        names = sorted(pg[m[0]], key=lambda s:s.lower())
        if not names: continue
        A(f"## {m[0]} — {len(names)} stored procedures")
        A("")
        A(f"*{MODDESC.get(m[0],'')}*  ·  Detail: [{m[1]}]({m[1]})")
        A("")
        # sub-group by leading token
        buckets={}
        for n in names:
            tok = n.split('_')[0]
            buckets.setdefault(tok,[]).append(n)
        big = {k:v for k,v in buckets.items() if len(v)>=3}
        small = [n for k,v in buckets.items() if len(v)<3 for n in v]
        for tok in sorted(big, key=str.lower):
            vs = sorted(big[tok], key=str.lower)
            A(f"#### `{tok}_*` — {len(vs)}")
            A("")
            A("| Stored procedure | Type | Notes |")
            A("|---|:--:|---|")
            for n in vs:
                vf=variant_flag(n)
                A(f"| `{n}` | {sp_type(n) or '·'} | {('_'+vf+'_') if vf else ''} |")
            A("")
        if small:
            A(f"#### Other {m[0]} procedures — {len(small)}")
            A("")
            A("| Stored procedure | Type | Notes |")
            A("|---|:--:|---|")
            for n in sorted(small, key=str.lower):
                vf=variant_flag(n)
                A(f"| `{n}` | {sp_type(n) or '·'} | {('_'+vf+'_') if vf else ''} |")
            A("")
    return "\n".join(L)+"\n"

with open(os.path.join(OUT,"APPENDIX-A-tables.md"),"w",encoding="utf-8") as f:
    f.write(render_tables())
with open(os.path.join(OUT,"APPENDIX-B-stored-procedures.md"),"w",encoding="utf-8") as f:
    f.write(render_procs())

# ---- Report totals + per-module counts -----------------------------------
print("TABLES total:", len(tables), " listed:", sum(len(v) for v in tg.values()))
print("PROCS  total:", len(procs), " listed:", sum(len(v) for v in pg.values()))
print("Uncategorized tables:", len(tg[OTHER[0]]), " | Uncategorized SPs:", len(pg[OTHER[0]]))
print("--- per module (tables / sps) ---")
for m in ORDER:
    print(f"  {m[0][:38]:38} {len(tg[m[0]]):4}  {len(pg[m[0]]):5}")
