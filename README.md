# Destinity Inspire — Hotel PMS Domain Documentation

Complete operational and technical documentation for the **Scienter HotelERP / Destinity Inspire** Front Office Property Management System (PMS).

Every document is grounded strictly in the actual source code and the live `HotelResWeb_Browns` database — nothing is invented, and unconfirmable items are explicitly marked **"Not found in the project"**.

> **System in one line:** an ASP.NET **MVC 5** multi-tenant hotel PMS (C# · SQL Server 2019 · **895 tables · ~2,890 stored procedures**) covering Reservations, Front Office, Housekeeping, Cashiering, F&B posting, Administration, Reporting and Night Audit for Sri-Lankan hotel chains.

## Contents

All documentation lives in [`hotel-pms/`](hotel-pms/). Start with the full index and reading paths:

➡️ **[hotel-pms/README.md](hotel-pms/README.md)** — document index, role-based reading order, and executive summaries.

### Highlights
| Area | Document |
|---|---|
| Project overview & tech stack | [00-project-overview.md](hotel-pms/00-project-overview.md) |
| End-to-end hotel process | [01-complete-hotel-process.md](hotel-pms/01-complete-hotel-process.md) |
| Whole-system flow | [SYSTEM-WIDE-FLOW.md](hotel-pms/SYSTEM-WIDE-FLOW.md) |
| Database & technical architecture | [12-database-and-technical-architecture.md](hotel-pms/12-database-and-technical-architecture.md) |
| Full table catalog (895) | [APPENDIX-A-tables.md](hotel-pms/APPENDIX-A-tables.md) |
| Full stored-procedure catalog (~2,890) | [APPENDIX-B-stored-procedures.md](hotel-pms/APPENDIX-B-stored-procedures.md) |
| Known issues & improvements | [15-known-issues-and-improvement-suggestions.md](hotel-pms/15-known-issues-and-improvement-suggestions.md) |
| Documentation gaps | [DOCUMENTATION-GAPS.md](hotel-pms/DOCUMENTATION-GAPS.md) |

## Notes
- Secrets (passwords, tokens, SAS signatures) are **redacted** throughout; only non-secret endpoints/hostnames appear.
- Research scratch (raw object-name lists, generator script, shared pack) is under [`hotel-pms/_research/`](hotel-pms/_research/) and is not part of the deliverable.
