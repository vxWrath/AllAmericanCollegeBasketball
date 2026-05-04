# All American College Basketball — Project Goals

## What This Is

**All American College Basketball** is a single-player college basketball dynasty simulator. You play as a head coach, not an owner. You start at a struggling Tier 6 program with bad facilities, weak recruits, and low expectations. Through recruiting, player development, and sustained winning, you build the program up, earn job offers from better schools, and climb conference tiers until you're at a blue-blood Tier 1 program winning national championships.

It is a **career simulator**, not a single-season game. The arc spans many seasons and multiple schools.

---

## The Core Loop

```
Recruit → Sim Season → Conference Tournament → National Playoff → Offseason → Repeat
```

### Preseason
- Review returning roster (graduating seniors, incoming freshmen)
- Finalize recruiting decisions
- Invest budget into program upgrades
- Review updated team ratings and conference outlook

### Regular Season (~30 games)
- Simulate games one at a time or in bulk
- Track standings, rankings, and recruiting pipeline simultaneously
- **Recruiting runs live during the season** — wins attract prospects, losses hurt interest
- Manage the transfer portal: players may request transfers mid-season due to low playing time

### Postseason
- **Conference Tournament** — all teams qualify, seeded by regular season record
- **National Championship Playoff (NCP)** — 64-team field (auto bids + at-large); the March Madness equivalent
- **Secondary Championship Playoff (SCP)** — 32-team consolation bracket (NIT equivalent)

### Offseason
1. Seniors graduate, roster spots open
2. Transfer portal opens — players leave and arrive
3. Recruit freshmen to fill the class
4. Apply program upgrades
5. Receive (and consider) job offers from other programs

---

## Key Systems

### Recruiting
The heart of the game. Each offseason a pool of prospects is generated with a position, an estimated star rating (★–★★★★★), and a list of interested programs. You spend a fixed budget of **recruiting points** on:
- Scouting (reveals a prospect's true rating)
- Sending an offer
- Making a home visit (significant boost)
- Hosting an official visit (strongest tool available)

Elite recruits receive multiple offers and weigh factors like prestige tier, facilities, conference strength, recent win %, NCP appearances, and coaching reputation. You can't pursue everyone — choices matter.

### Transfer Portal
A percentage of underclassmen enter the portal each offseason (higher if they had low playing time). Portal players commit faster than freshmen but have less long-term upside. Elite programs poach from weaker ones. Keeping your roster deep and giving minutes to backups reduces portal attrition.

### Program Upgrades
Upgrades belong to the school, not the coach. They persist after you leave but build your reputation.

| Upgrade | Effect |
|---|---|
| Practice Facility (Lvl 1–3) | Improves player development rate per season |
| Arena Expansion (Lvl 1–3) | Home-court advantage bonus; boosts recruiting visits |
| Recruiting Budget (Lvl 1–3) | More recruiting points per season |
| Academic Reputation (Lvl 1–3) | Attracts high-GPA recruits; reduces portal losses |
| Scouting Network (Lvl 1–3) | Reveals prospect ratings more accurately, earlier |

### Player Attributes
Players have per-position weighted attributes: **inside shot, outside shot, interior defense, perimeter defense, athleticism, playmaking, rebounding**. These combine into an overall rating and evolve each season through development.

### Conference Tiers (1–6)
Programs belong to a conference tier. Tier 1 is blue-blood territory; Tier 6 is obscure low-majors. Tier determines recruiting ceilings, schedule strength, and available job offers. Realignment happens over time.

---

## Technology Stack

| Layer | Choice |
|---|---|
| Backend language | Python |
| Backend framework | BlackSheep |
| Frontend | Svelte |
| Database | PostgreSQL |
| Containerization | Docker |
| Cloud host | Hetzner |

---

## Version 1 Scope

V1 is a **working single-player dynasty mode** with a real web UI.

### In Scope
- Full game loop: recruit → season → postseason → offseason → repeat
- A playable web UI in Svelte (no terminal interface)
- Single-player — one coach, one career, one team
- Working season simulation (all ~30 games, conference tournament, NCP, SCP)
- Simple recruiting system (signing prospects/transfers before the season)

### Out of Scope for V1
- News outlets / social media
- In-depth recruiting (program upgrades, offers, NIL, boosts, pipelines etc)
- Job offers, coach upgrades
- Conference relocation (if staying on one team for awhile)

---

## Learning Goals (Engineering)

This rebuild is also a deliberate exercise in professional software engineering practices. The goals below are equally important as shipping the game.

### CI/CD Pipeline (GitHub Actions)
- Lint and type-check every PR with **ruff** and **pylance**
- Build and push Docker images in CI (not locally)
- Block merges to `main` if CI fails (branch protection rules)

### Environment Promotion: dev → QA → prod
- **dev** — local developer environment; Docker Compose; `.env.dev` secrets
- **QA** — deployed on Hetzner; mirrors prod config; used for integration testing and sanity-checking before release
- **prod** — live environment on Hetzner; deployed only via a tagged release or manual promotion from QA

Each environment has its own:
- PostgreSQL database (no shared state between envs)
- Docker image tag (`dev`, `qa`, `latest`/version tag)
- Secret set managed separately (not committed to the repo)

### Secrets Management
- Secrets stored per-environment (never hardcoded or committed)
- GitHub Actions secrets scoped by environment (`dev`, `qa`, `prod`)
- Local dev uses `.env` files (gitignored); a `.env.example` documents required vars

### Docker
- Multi-stage `Dockerfile` (build stage + lean runtime stage)
- `docker-compose.yml` for local dev (app + Postgres)
- CI builds and tags images automatically
- Images pushed to a container registry (e.g., GitHub Container Registry or Docker Hub)

### Code Quality
- **ruff** for linting and formatting (replaces black + flake8)
- **pylance** for static type checking (strict mode target)
- Pre-commit hooks locally to catch issues before push
- All game logic covered by unit tests; simulation results verified by integration tests

### Branching Strategy
```
main           ← always deployable to prod; protected
  └── qa       ← reflects what's deployed to QA
        └── dev/feature-* ← all development work
```
PRs go from feature branches → `main` (or a develop branch). A promotion workflow deploys `main` → QA → prod.

---

## Design Philosophy (Unchanged from Original)

- **Look**: Retro Bowl — clean, minimal, everything visible at a glance
- **Depth**: NCAA 2K / College Football Game — recruiting, development, program-building, and job moves all matter
- **Feel**: You always understand what's happening and why. No hidden systems, no unexplained numbers

Simplicity wins every design decision. The core loop must be satisfying on its own before any feature is layered on top.

---

## Success Criteria

The project is in a good state when:
- [ ] A new developer can clone the repo, run `docker compose up`, and have a working dev environment in under 5 minutes
- [ ] Every PR triggers linting, type checking, and tests automatically
- [ ] Deploying to QA or prod requires no manual file editing — only a tag or button
- [ ] Dev, QA, and prod each have independent databases and secrets with no cross-contamination
- [ ] A full dynasty season can be played from start to finish in the web UI without errors
