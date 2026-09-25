# Meetpu management portal (React + Vite + MapLibre)

Web portal for district officials: map of reports over the flood extent, approval queue, case detail with evidence and status history, stuck-case dashboard, and PDNA-style CSV export. English and Tamil.

## Run locally

Start the API first (see `backend/README.md`), then:

```bash
cd management-web
npm install
cp .env.example .env.local      # VITE_API_URL, default http://localhost:8000
npm run dev                     # http://localhost:5173
```

Demo login: `collector` / `meetpu123`.

## Build

```bash
npm run build                   # output in dist/
```

`VITE_API_URL` is read at build time. On Render, set it on the `meetpu-portal` static site to the API's public URL and redeploy.

## Notes

- Basemap: OpenFreeMap Positron vector tiles (no API key).
- Tamil strings in `src/i18n.tsx` are a first draft. Have a native speaker review them.
- Photos load from `/reports/{uuid}/photo`. The UUID in the URL is the access control, so treat these links as sensitive.
