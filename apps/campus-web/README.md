# Campus Web MVP

First-phase Web workbench for Hermes Campus Agent.

## Run Locally

```bash
cd apps/campus-web
npm install
npm run dev
```

Open `http://localhost:3000`.

If another local app already owns port 3000:

```bash
npm run dev -- --hostname 127.0.0.1 --port 3010
```

## Verification

```bash
npm run type-check
npm run lint
npm run build
npm run e2e
```

Run `type-check` and `build` sequentially. Next.js generates `.next/types` during build, so running them in parallel can create transient type-generation races.

`npm run e2e` expects the app to be running at `http://127.0.0.1:3010`.

## Current Scope

- Role-aware workbench for teaching administrator and teacher workflows.
- Local fixture-backed campus knowledge Q&A.
- Visible source citations and evidence abstention.
- Reviewable draft generation.
- Teaching task ledger.
- Local `HermesBridge` interface with deterministic implementation.

## Explicitly Not Included

- Real school data.
- Real student, staff, grade, disciplinary, psychological, personnel, or financial data.
- Business-system write operations.
- Automatic notice publication, approval, or high-stakes decision making.
- Production authentication or authorization.
