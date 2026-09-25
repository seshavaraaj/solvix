# Software Gaps in Disaster Damage Assessment: India and Tamil Nadu

| Field | Value |
|---|---|
| Prepared | 2026-09-25 |
| Topic | What is currently lacking in disaster damage assessment (DDA) in India, specifically Tamil Nadu |
| Domain | Disaster management, geospatial and public-sector software |
| Constraints | Software-side solutions only; floods, cyclones and coastal hazards; latest information (mostly 2015–2026) |
| Audience | Solvix'26 hackathon team choosing and scoping a software solution |
| File | 2026-09-25_disaster-damage-assessment-tamil-nadu-software-gaps.md |

## Executive Summary

India and Tamil Nadu already have strong pieces of a damage-assessment stack: ISRO satellite flood maps, a national PDNA framework, state alert apps and government crop-survey apps. The evidence shows the weak point is not "no technology" but the link between pieces: field damage capture, verification, one shared record, and fast, fair payout. Relief protests followed both Cyclone Michaung (2023) and Cyclone Fengal (2024), and the state's Rs 37,907 crore Michaung claim received only Rs 276 crore from the Centre. Public evidence for several specific software gaps is thin or indirect, so this report separates documented facts from reasoned inference and marks confidence for each. The most defensible gap for a software build is an evidence-linked, geotagged, multi-source damage record that connects household and crop reports to satellite layers and relief payment.

## Assumptions and Scope

Defaults applied (user replied "default"):

- Audience: a hackathon team picking a build. Depth: standard.
- Hazards: floods, cyclones, coastal. Tsunami and drought excluded.
- Timeframe: latest available; key events 2015 Chennai floods, 2023 Michaung, 2024 Fengal.
- Sources: primary and official preferred; news used for event detail.
- Saved to `.reports/`; `.gitignore` unchanged.
- Included: recommendations, risks, gap-versus-solution table.

Out of scope: hardware, policy design, funding-formula reform. Where a gap is a policy problem, only the software angle is discussed.

## Methodology

About 17 web searches and 20 page fetches were run on 2026-09-25 (Sources lists what was used). Several key pages returned HTTP 403 (Deccan Herald protest article and editorial, PIB, ScienceDirect, Geospatial World, NDEM homepage) or unreadable content (NIDM PDNA SOP PDF), so their claims rely on search-result summaries and are labelled accordingly. No Tamil Nadu government damage-assessment system documentation, TNeGA app manuals or internal audit was accessed. Because of this, "what is missing" partly comes from inference, not from an official gap analysis. Nothing in this report is an official assessment.

## Findings

### 1. Tamil Nadu and India already have many assessment components

- ISRO's NRSC produced SAR-based flood-inundation maps of the Chennai area for 3, 4, 5 and 7 December 2023 and passed GIS layers to the Tamil Nadu State Remote Sensing Application Centre (TNSAC) and TNSDMA for value addition [1].
- TNSDMA runs TN-ALERT and TN-SMART, a web system that uses forecasts to estimate potential impact and disseminate alerts [2][3]. The Tiruchirappalli district page describes alerts and rainfall information only; it does not mention post-event damage reporting [3].
- TNeGA publishes a "Crop Survey (O)" app for officials to capture field crop details [4]. A separate "Crop Damage Assessment" app for Tamil Nadu also exists on Google Play [5]; its developer and official status could not be verified.
- India has a standard PDNA framework (manual, handbook, SOP) built with NDMA, NIDM and World Bank support [6].
- NRSC also runs a National Database for Emergency Management (NDEM) that hosts event reports [1][7].
- Under PMFBY, satellite-based yield estimation (YES-TECH) has been mandatory at 30% weight for paddy and wheat since Kharif 2023 [8].

Implication: a new tool should integrate with these, not replace them.

### 2. Damage claims and relief remain contested and slow

| Event | Documented fact | Source |
|---|---|---|
| Michaung 2023 | State tentatively estimated Rs 5,060 crore damage; Rs 6,000 per family relief cost Rs 1,486.93 crore, paid via ration shops and bank transfer | [9] |
| Michaung 2023 | CAG-linked report: TN claimed Rs 37,907.21 crore; Union approved Rs 276 crore (under 1%) | [10] |
| Michaung 2023 | Search summary reports intense criticism of "poor handling"; ministers and mayor gheraoed (article not fetched) | [11] |
| Fengal 2024 | Damage counted as 2,416 huts, 721 houses, 963 cattle and 211,139 ha of farm land inundated; extent of crop loss "would be known only after water recedes" | [12] |
| Fengal 2024 | Rs 944.80 crore SDRF released on 2024-12-07 pending central team report | [13] |
| Fengal 2024 | On 2024-12-16, residents of over 14 villages in Cuddalore and Villupuram protested unpaid Rs 2,000 relief; earlier, protesters threw mud at a minister over "poor relief" | [14][15] |

Caution: the funding gap between claimed and approved amounts is largely a political and fiscal matter. Software can only help by making claims more evidence-backed and auditable. Payment delays could have causes other than assessment (for example beneficiary lists); the sources do not say which.

### 3. Historical evidence of weak data infrastructure (2015 Chennai floods)

- CAG called the 2015 floods a "man-made" disaster and the 29,000 cusec Chembarambakkam release "injudicious" [16].
- Per a CAG-related summary, of 219 planned telemetry stations only about a quarter were set up by August 2016, and about 60% of 375 existing stations were non-functional [17]. This figure comes from a search summary; the PDF was not read.
- CAG found TNSDMA held no meeting between March 2013 and March 2017 [17].
- Over 400 lives lost and over 100,000 structures damaged [17].

This is 2015–2018 evidence. Whether the telemetry and coordination problems persist today was not verified.

### 4. Satellite assessment has known limits

- Optical data is blocked by cloud, so SAR is needed in floods [18].
- Flood extent depends on satellite overpass date and coverage [18].
- Maps show water extent, not building-level damage, loss value or which household is affected. Satellite products go to departments; the sources show no automatic path to household-level relief eligibility [1].
- Sources also note high-resolution LiDAR and SAR data can be expensive and need specialist skills [19].

### 5. Crop loss assessment still leans on manual methods

- Crop Cutting Experiments (CCEs) remain the main method; technology-based estimation is only partially implemented [20].
- CCEs are slow, labour-intensive and can carry data uncertainty [20].
- Fengal's crop loss could not be fixed until water receded [12], which suggests waiting-time is a software opportunity (for example SAR flood-duration mapping against crop calendars). This is inference.

### 6. Reported cross-agency data problems (lower confidence)

One secondary source (PubAdmin.Institute, December 2025) states that state–central data interoperability is inconsistent, assessment teams use outdated documentation and have limited digital skills, and agencies sometimes produce conflicting early estimates [19]. It is a general educational site, gives no Tamil Nadu detail and no primary citation. Treat as a hypothesis to validate, not a proven fact.

### 7. Gap list (software side)

| # | Gap | Evidence strength | Basis |
|---|---|---|---|
| G1 | No visible link from satellite flood layers to household/asset-level damage and relief eligibility | Medium | [1][4] |
| G2 | Alert apps cover pre-event; post-event damage reporting and citizen feedback not evident in public TN app descriptions | Medium | [2][3] |
| G3 | Field capture depends on officials; verifiable geotagged citizen evidence not confirmed in official flow | Low–Medium | [4][5][12] |
| G4 | Crop-loss figures wait for water recession and manual CCEs | Medium | [12][20] |
| G5 | One shared, versioned damage record across departments and Centre absent or unverified; conflicting estimates reported | Low | [19] |
| G6 | Claims to Centre poorly backed by auditable evidence trail (inference from 37,907 vs 276 crore outcome) | Low | [10] |
| G7 | Relief payment delays and disputes with no visible tracking or grievance loop | Medium | [14][15] |
| G8 | Sensor and telemetry reliability (historic) | Medium for 2016, unknown now | [17] |
| G9 | Tamil-language, low-connectivity field tools | Not evidenced; assumption | none |

## Analysis

The pattern: Tamil Nadu is data-rich but decision-poor after the event. Satellites give hazard extent; officials give summary counts; payout reaches people late and unevenly. No source shows a single pipeline going from image or citizen photo to verified damage record to payment.

Trade-offs for a builder:

- Satellite-only tools are already provided free by ISRO, so a student copy adds little.
- The unserved layer is the last mile and the audit trail: evidence, dedup, status, grievance.
- Anything that needs official Revenue, TNeGA or PMFBY data will hit access limits; a demo should use open or synthetic data and public ISRO layers.
- AI building-damage models trained on foreign datasets may not transfer to Tamil Nadu roof and hut types. This is an assumption, not tested here.

Conflicts between sources: figures for Michaung differ by design (Rs 5,060 crore tentative estimate, Rs 37,907 crore claim, Rs 276 crore approved). They may reflect different scopes or dates; the sources do not reconcile them.

## Risks and Uncertainties

| Finding | Confidence | Reason |
|---|---|---|
| F1 Existing components (ISRO maps, TN-ALERT, crop apps, PDNA, YES-TECH) | High | Official or government pages and PIB-derived text |
| F2 Relief disputes and delays after Michaung and Fengal | Medium | Multiple news items; several fetches blocked; cause of delay not established |
| F2 Rs 276 crore vs Rs 37,907 crore | Medium | One fetched article; figure from CAG-based reporting; not cross-checked to CAG report |
| F3 2015 telemetry and TNSDMA findings | Medium | Search summaries; 2016–2018 data |
| F4 Satellite limits | Medium | Search summary of NRSC material; not fetched in full |
| F5 CCE reliance | Medium | Academic summary, article paywalled |
| F6 Interoperability and outdated forms | Low | Single secondary source, no Tamil Nadu detail |
| F7 Gap list G3, G5, G6, G9 | Low | Inference or assumption |

Missing data: no Tamil Nadu official post-disaster damage form, no TNeGA/TNSDMA system architecture, no field interviews with VAOs or revenue staff, no public number for share of households missed. Findings should be validated with Tamil Nadu officials before any claim is made to judges as fact.

## Recommendations

1. Frame the build around G1 + G7: geotagged citizen and field reports linked to ISRO/Bhuvan flood layers and a relief-status tracker (Findings 2, 4, 7).
2. Design for integration: import NRSC inundation layers, export in PDNA-compatible fields, assume Tamil and low connectivity (Findings 1, 7).
3. Build an evidence trail: photo, time, location, verifier, status history, to support central claims (Findings 2, 7).
4. Add crop-loss module using SAR inundation duration against crop stage as a pre-screen, clearly marked as decision support, not replacement for CCEs (Findings 5).
5. Use only open and synthetic data for the demo; state limits openly (Risks).
6. Before the pitch, verify G3, G5 and G9 by contacting a district revenue or TNSDMA source, or by reading the CAG report and TNeGA app descriptions in full.
7. Have the design reviewed by disaster management professionals; this report is not an official assessment.

## Conclusion Summary

Tamil Nadu is not short of disaster technology; it is short of a connected, evidence-based way to turn that technology into fast, fair, well-documented damage records and payouts.

- ISRO satellite maps, state alert apps, crop-survey apps and a national needs-assessment framework already exist (see Findings 1).
- After Cyclones Michaung and Fengal, people protested late or unpaid relief, and the Centre approved a tiny share of the state's Michaung claim (see Findings 2).
- Old audits of the 2015 Chennai floods found broken sensors and weak coordination; whether that still holds is unknown (see Findings 3).
- Satellite maps show where water is, not which household or building was hurt (see Findings 4).
- Crop loss still depends on slow manual field experiments and waiting for water to recede (see Findings 5).
- One weak source says agencies use different forms and produce conflicting numbers; this needs checking (see Findings 6).
- The strongest software opportunity is a geotagged evidence-to-relief pipeline that plugs into existing government data (see Findings 7).

Next step: pick the evidence-linked citizen and field reporting tool as the core build and verify the low-confidence gaps with a local official before pitching.

## Sources

1. NRSC/ISRO, "Tamil Nadu Heavy Rains 2023 - Michaung Cyclone" (NDEM report), 2023-12-07. <https://ndem.nrsc.gov.in/documents/Disaster_Document/2023/TN/tncyclone50dsc07122023_0600hrs/tncyclone50dsc07122023_0600hrs_report.pdf> (accessed 2026-09-25; from search summary, not fetched)
2. TNSDMA, "TN-ALERT" listing, Google Play. <https://play.google.com/store/apps/details?id=int_.rimes.tnsmart&hl=en> (accessed 2026-09-25; from search summary)
3. Tiruchirappalli District, "TN-SMART Mobile App", undated. <https://tiruchirappalli.nic.in/revenue-department/tn-smart-mobile-app/> (accessed 2026-09-25)
4. TNeGA, "Crop Survey (O)", Google Play. <https://play.google.com/store/apps/details?id=org.tnega.payiraaivu> (accessed 2026-09-25; search summary)
5. "Crop Damage Assessment", Google Play, developer unverified. <https://play.google.com/store/apps/details?id=app.tnad.cropdamage&hl=en_IN> (accessed 2026-09-25; page not readable)
6. NIDM/NDMA, "Standard Operating Procedures Post Disaster Needs Assessment India", 2019-09. <https://nidm.gov.in/PDF/pubs/sop_pdna.pdf> (accessed 2026-09-25; content not readable, date from metadata; description from search summary)
7. NRSC, "National Database for Emergency Management". <https://ndem.nrsc.gov.in/> (accessed 2026-09-25; page not readable)
8. PIB, "Assessment of Crop Losses through Satellite". <https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2101838&reg=48&lang=2> (accessed 2026-09-25; from search summary; fetch blocked)
9. India TV News / Deccan Chronicle / Deccan Herald, Michaung Rs 6,000 relief reports, 2023-12. <https://www.indiatvnews.com/tamil-nadu/chennai-tamil-nadu-chief-minister-mk-stalin-initiates-rs-6000-flood-relief-cyclone-michaung-affected-families-chennai-tiruvallur-chengelpet-kancheepuram-2023-12-17-907671> (accessed 2026-09-25; search summary)
10. The News Minute, "CAG report says not even half of emergency disaster funds transferred to states", 2026-08-16. <https://www.thenewsminute.com/news/cag-report-says-not-even-half-of-emergency-disaster-fund-transferred-to-states> (accessed 2026-09-25)
11. Deccan Herald, "Michaung exposes our unpreparedness", 2023-12. <https://www.deccanherald.com/opinion/editorial/michaung-exposes-our-unpreparedness-2798468> (accessed 2026-09-25; fetch blocked; search summary only)
12. Search summary of Tamil Nadu Fengal damage figures (news reports incl. All India Radio), 2024-12. <https://www.newsonair.gov.in/cyclone-fengal-causes-widespread-devastation-bringing-heavy-rainfall-and-flooding-in-puducherry-and-tamil-nadu> (accessed 2026-09-25)
13. All India Radio, "Centre approves Rs 944 cr for Tamil Nadu as Cyclone Fengal relief...", 2024-12-07. <https://www.newsonair.gov.in/centre-approves-rs-944-cr-for-tamil-nadu-as-cyclone-fengal-relief-promises-more-funds-after-assessment-report-by-central-team> (accessed 2026-09-25)
14. The Commune, "Residents in Cuddalore and Villupuram protest over unpaid ₹2,000 flood relief after Cyclone Fengal", 2024-12. <https://thecommunemag.com/residents-in-cuddalore-and-villupuram-protest-over-unpaid-%E2%82%B92000-flood-relief-after-cyclone-fengal/> (accessed 2026-09-25; search summary)
15. The Week, "Cyclone Fengal: Irked by 'poor' relief, people throw dirt on TN Minister Ponmudy in Villupuram", 2024-12-03. <https://www.theweek.in/news/india/2024/12/03/cyclone-fengal-poor-relief-ires-public-in-villupuram-throw-dirt-on-tn-minister-ponmudy-authorities.html> (accessed 2026-09-25; search summary)
16. Swarajya, "2015 Chennai Floods Man-Made... CAG Report", 2018-07. <https://swarajyamag.com/insta/2015-chennai-floods-man-made-officials-failed-to-take-proper-steps-to-prevent-damage-cag-report> (accessed 2026-09-25)
17. CAG audit and Chennai floods reports as summarised in search results (CAG Chapter VI Flood Management report; Wikipedia TNSDMA page), 2017–2018. <https://cag.gov.in/uploads/download_audit_report/2016/Chapter_6_Disaster_Management_of_Report_No_4_of_2017_-_Performance_Audit_of_Flood_Management_and_Response.pdf> (accessed 2026-09-25; PDF not read; figures unverified against original)
18. NRSC/NDEM, "Flood Affected Area Atlas of India" and Bhuvan disaster pages. <https://ndem.nrsc.gov.in/documents/downloads/allindia_flood_techdoc.pdf> (accessed 2026-09-25; search summary)
19. PubAdmin.Institute, "Comprehensive Methods for Effective Damage Assessment", 2025-12-07. <https://pubadmin.institute/disaster-management/effective-damage-assessment-methods> (accessed 2026-09-25; secondary source, low reliability)
20. "Can remote sensing-based yield proxies substitute crop cutting experiments in Indian agricultural insurance models?", ScienceDirect, 2026. <https://www.sciencedirect.com/science/article/pii/S2214317326001137> (accessed 2026-09-25; fetch blocked; search summary only)
