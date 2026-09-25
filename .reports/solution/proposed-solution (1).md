# Proposed Solution: Meetpu (மீட்பு), an Evidence-to-Relief Pipeline for Disaster Damage Assessment in Tamil Nadu

| Field | Value |
|---|---|
| Prepared | 2026-09-25 |
| Based on | `.reports/2026-09-25_disaster-damage-assessment-tamil-nadu-software-gaps.md` |
| Audience | Solvix'26 hackathon team and judges |
| Scope | Software only; floods, cyclones and coastal hazards |

## 1. Problem

Tamil Nadu and India already have strong pieces of a damage-assessment stack: ISRO satellite flood maps, TN-ALERT and TN-SMART alert apps, TNeGA crop survey apps, a national PDNA framework and PMFBY satellite yield estimation. The weak point is the link between them.

- A satellite map shows where the water was. It does not show which household or building was damaged.
- Alert apps cover the time before the event. Public descriptions show no post-event damage reporting or citizen feedback.
- Field capture depends on officials. Verifiable, geotagged citizen evidence is not confirmed in the official flow.
- Crop loss waits for water to recede and for slow, manual Crop Cutting Experiments.
- After Cyclones Michaung (2023) and Fengal (2024), people protested late or unpaid relief. Tamil Nadu claimed Rs 37,907 crore for Michaung and the Centre approved Rs 276 crore, under 1%.

Part of that funding gap is political. Software can still make claims better evidenced and auditable, and make relief status visible.

## 2. Solution overview

Meetpu is one connected, geotagged damage record that runs from the household report to the relief payment. It plugs into existing government data and does not replace it.

Target gaps from the research report: G1, G3, G4, G6, G7, and partly G9.

### Core flow

1. **Report.** A citizen (User app) or a field staff member (Staff app) submits a photo, GPS position, timestamp and damage type (house, hut, cattle, crop). Both apps are Tamil-first and offline-first; reports sync when the network returns.
2. **Verify.** The system runs automatic checks: EXIF/GPS match, duplicate photo hash, and whether the location falls inside the ISRO/Bhuvan inundation polygon. Field staff receive a queue sorted by confidence and confirm or reject each report on site. A human makes the final decision.
3. **Record.** Each household or asset has one geotagged record with a versioned status history: reported, verified, approved, paid.
4. **Approve and monitor.** Officials in the Management portal review verified cases, approve relief, and see stuck cases per village and district.
5. **Track relief.** The citizen sees the status of their claim by phone number or ration ID and can raise a grievance from the same screen.
6. **Export.** One click in the Management portal produces a PDNA-style report with the full evidence trail (photo, place, time, verifier) for the state's claim to the Centre.

## 3. Portals

The solution has three portals, each for a different user group and device.

| Portal | Users | Platform | Main functions |
|---|---|---|---|
| Management | Government departments and officials (for example TNSDMA, Revenue, district administration) | Website, desktop preferred | Live damage map with flood-layer overlay; review and approve verified cases; relief and payment status; stuck-case and grievance dashboard; user and role management; PDNA-style export and audit trail |
| Staff | Field staff (for example VAOs, revenue and survey staff, assigned volunteers) | Mobile app | Assigned-area task queue; on-site verification of citizen reports; capture of new damage records with photo and GPS; offline mode with sync; crop-loss pre-screen flags for survey priority |
| User | Affected citizens and farmers | Mobile app | Report damage with photo and GPS in Tamil or English; relief status timeline; raise grievance; SMS or WhatsApp notifications |

How the portals connect:

- A User report enters the Staff queue for its area.
- Staff verify on site and mark the case verified or rejected, with evidence.
- Management approves verified cases, monitors progress, and exports claims.
- Status changes flow back to the User app, so the citizen sees each step.

Access control: phone OTP for User and Staff; role-based login for Management (for example state, district and taluk levels), with every action logged.

## 4. Modules

| Module | Portal | Function | Gap addressed |
|---|---|---|---|
| Damage reporting | User, Staff | Tamil and English, offline queue, photo plus GPS capture | G3, G9 |
| Flood-layer overlay | Management, Staff | Import NRSC/Bhuvan SAR inundation layers as GeoJSON; tag each report as inside or outside the water extent | G1 |
| Verification queue | Staff, Management | Rule-based checks plus optional AI photo triage; staff and officials have the final say | G3, G6 |
| Crop pre-screen | Management, Staff | Sentinel-1 SAR flood duration against crop calendar per survey number; flag likely loss to prioritise CCEs | G4 |
| Relief tracker and grievance | User, Management | Status timeline with SMS or WhatsApp notification and a grievance loop | G7 |
| Audit and export | Management | PDNA-compatible fields and an evidence bundle for central claims | G6 |

## 5. Suggested stack

- **Management portal:** React web app (desktop layout), MapLibre for the damage map, tables and charts for dashboards.
- **Staff and User apps:** React Native or Flutter mobile apps, i18n (Tamil and English), local database for the offline queue.
- **Backend:** FastAPI or Node.js, one shared API for all three portals, PostgreSQL with PostGIS, S3-compatible photo storage.
- **Geospatial:** Sentinel-1 via Google Earth Engine or Copernicus; ISRO/Bhuvan layers for the demo.
- **AI (optional):** a small image classifier for damage severity, always overridable by a human.
- **Notifications:** SMS gateway or WhatsApp API.
- **Auth:** phone OTP for User and Staff; role-based login for Management (state, district, taluk, admin).

## 6. Hackathon scope

| Status | Items |
|---|---|
| Build for real | Management web portal (map, approval queue, export), Staff and User mobile apps in Tamil, PostGIS damage record, inundation-polygon check, status tracker |
| Demo data | Michaung (Chennai) or Fengal (Cuddalore) inundation layer with synthetic citizen reports |
| Mock | Payment (status change only); Revenue, TNeGA and PMFBY integration shown as adapter stubs |
| Skip | Custom AI model training; use rule-based severity instead |

## 7. Design principles

- **Integrate, do not replace.** Import NRSC inundation layers and export PDNA-compatible fields.
- **Human in the loop.** AI and rules only prioritise; staff and officials decide.
- **Low connectivity.** Offline-first and Tamil-first, because networks fail in floods.
- **Auditable.** Every status change records who, when and on what evidence.

## 8. Risks and limits

| Risk | Mitigation or note |
|---|---|
| No official Tamil Nadu data access | Demo uses public ISRO layers and synthetic reports; state this openly |
| Fake or duplicate reports | Geo-fence check, photo hash, staff verification |
| Gaps G3, G5, G9 are low-evidence | Verify with a district revenue or TNSDMA contact before the pitch |
| AI models trained on foreign data may not fit Tamil Nadu roof and hut types | Use rule-based severity in the demo; treat AI as untested |
| Crop pre-screen is not a replacement for CCEs | Label it decision support only |
| Payment delays may have causes other than assessment (for example beneficiary lists) | Tracker shows the stage where a case is stuck, without claiming the cause |

This is a hackathon design, not an official assessment. Have it reviewed by disaster management professionals before any real use.

## 9. Pitch summary

Satellites show where the water was. Meetpu shows who lost what, proves it, and follows the rupee to their door.

- **Problem:** Existing tools do not connect satellite data, household damage and relief payment.
- **Solution:** A geotagged evidence-to-relief pipeline with three portals (Management web, Staff and User mobile), citizen reporting, staff verification, a relief tracker and audit export.
- **Value:** Faster and fairer relief for families, a stuck-case view for officials, and evidence that can withstand scrutiny when the state claims funds from the Centre.

## 10. Next steps

1. Confirm low-confidence gaps (G3, G5, G9) with a local official or by reading the CAG report and TNeGA app descriptions in full.
2. Pick the demo event (Michaung or Fengal) and obtain its public inundation layer.
3. Build the User and Staff apps and the verification queue first; add the Management portal, tracker and export next.
4. Prepare judge Q&A, for example with the `presentation-helper` skill.
