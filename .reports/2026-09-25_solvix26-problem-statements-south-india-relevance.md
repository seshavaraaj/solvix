# Solvix'26 Round 1: Which Problem Statements Matter Most for India and South India

| Field | Value |
|---|---|
| Prepared | 2026-09-25 |
| Topic | Relevance of the 35 Solvix'26 Round 1 problem statements to India, with focus on South India |
| Domain | Applied AI for public good (hackathon problem selection) |
| Constraints | Focus on Tamil Nadu, Kerala, Karnataka, Andhra Pradesh, Telangana, Puducherry; choose one statement for a hackathon build |
| Audience | Solvix'26 team choosing a problem statement |
| File | 2026-09-25_solvix26-problem-statements-south-india-relevance.md |

## Executive Summary

The question is which Solvix'26 Round 1 problem statement gives a student team the best mix of real South Indian need, usable data, buildability and judge appeal. We scored all 35 statements on a weighted rubric. The strongest options are **Sustainable Fishing Support (Sustainability 4)** and **Human-AI Disaster Damage Assessment (Human-AI Collaboration 6)**, both scoring 89/100, followed by **Community Climate-Disaster Preparedness (Sustainability 3)**, **Reducing Wrongful Welfare Rejections (Responsible AI 5)**, **Gig-Work Algorithm Fairness (Responsible AI 1)** and **Municipal Action Mapping (Sustainability 6)**. Each maps to documented, recent, costly problems in the southern states: repeated cyclones and floods, a large coastal fishing economy, a well-documented algorithmic welfare-exclusion case in Telangana, and new gig-worker laws in Karnataka and Telangana. Our top recommendation is Sustainable Fishing Support if the team wants a distinctive idea, or Disaster Damage Assessment if the team wants the safest, highest-impact build.

## Assumptions and Scope

Defaults applied (user accepted all defaults):

- Audience: a hackathon team of about 4 students picking one statement for Solvix'26.
- Team capability: web, mobile and ML through existing APIs and open models; no custom hardware; 24–36 hour build.
- Scoring weights: South India relevance and scale 30%, data availability for a demo 20%, build feasibility 20%, judge appeal and uniqueness 15%, government scheme or policy fit 15%.
- Depth: standard report with a ranking of all statements and a deep dive on the top 5.
- Timeframe: most recent sources available (2023–2026), dates noted.
- Geography: India, weighted toward the five southern states and Puducherry.

Scope notes:

- The PDF lists 5 domains × 7 statements = 35 statements. All 35 are scored.
- The PDF says "AI for Social Impact" is missing from the document. It is out of scope here.
- Scores are the author's judgment based on the evidence cited. They are not an official rubric. Judges at Solvix'26 may weigh things differently.

## Methodology

- Read the Solvix'26 Round 1 Problem Statements PDF (local source [40]).
- Ran about 25 web searches on South Indian conditions for each theme: disasters, fisheries, welfare algorithms, gig-work law, ageing, cyber fraud, urban lakes and flooding, civic grievance apps, e-waste, energy metering, education outcomes, accessibility and Indian-language AI tooling.
- Opened full pages where possible to confirm key numbers. Two news sites (Business Standard, Deccan Herald) blocked full-page fetch; figures from those sources come from search-result extracts and are marked where it matters.
- Scored each statement 1–5 on each criterion, then converted to a score out of 100.

Limitations: no interviews with officials or users; no access to paid databases; some figures come from news reports rather than primary government data.

## Findings

### 1. Disasters are the single largest recurring cost in South India

All five southern states face repeated, high-cost climate disasters.

- Cyclone Michaung (December 2023) caused economic losses in Tamil Nadu estimated at over ₹11,000–12,000 crore, with insured losses only ₹1,500–2,000 crore [1][2]. The gap between economic and insured loss shows how much damage goes unassessed by insurers and must be assessed by the state.
- The Wayanad landslides in Kerala (30 July 2024) killed about 392 people with about 150 missing [3]. Commentators argue short lead times and weak multi-hazard early warning contributed [4].
- Cyclone Montha (October 2025) caused Andhra Pradesh to estimate losses of ₹5,265 crore, later revised upward. Reports give the revised figure as ₹6,355.60 crore or ₹6,384 crore [5][6]. AP ran relief through its Real-Time Governance Society and sent over 3.6 crore alert messages [7].
- Bengaluru has lost most of its lakes to encroachment (730 of 837 urban-district lakes reported as encroached), and 209 flood-prone spots were identified by BBMP [26].
- Heat is a growing hazard. Tamil Nadu declared heatwave a state-specific disaster in November 2024 [38]. Kerala recorded 2024 as its warmest year since 1901 [39].

Relevant statements: Human-AI 6 (Disaster Damage Assessment) and Sustainability 3 (Climate-Disaster Preparedness).

### 2. Small-scale fisheries are a large, stressed livelihood in the south

- Tamil Nadu (6.79 lakh tonnes) and Kerala (6.10 lakh tonnes) are India's second- and third-largest marine fish producers. National landings fell 2% in 2024 and Kerala's fell 4%. CMFRI linked the drop partly to cyclones and heatwave days in AP and Kerala [20].
- Prices swing hard: oil sardine went from ₹350–400/kg in early 2024 to ₹20–30/kg later in the year [20]. This volatility hurts small fishers most.
- INCOIS already publishes daily Potential Fishing Zone (PFZ) advisories for 14 sectors, including Kerala, North and South Tamil Nadu, North and South AP, and Karnataka, in 10 languages including Tamil, Telugu, Malayalam and Kannada. It reaches about 5.5 lakh fishers [18][19].
- Tamil Nadu fishers are repeatedly arrested by the Sri Lankan Navy for crossing the International Maritime Boundary Line (IMBL). One November 2025 incident alone saw 35 arrested and 3 boats seized [21].

Relevant statement: Sustainability 4 (Sustainable Fishing Support).

### 3. Telangana is a global case study for wrongful algorithmic welfare exclusion

- Telangana's Samagra Vedika system merges government databases to decide welfare eligibility. From 2014 to 2019 the state cancelled over 1.86 million food security cards and rejected 142,086 new applications, without notice [8].
- After a Supreme Court-ordered re-verification, 15,471 of 205,734 processed applications were approved, meaning at least 7.5% had been wrongly excluded [8].
- Amnesty International (April 2024) found the entity-resolution approach raises serious human rights concerns [9]. Reports indicate the same technology was used again to issue new ration cards [10].

Relevant statement: Responsible AI 5 (Reducing Wrongful Welfare Rejections).

### 4. South India leads India on gig-worker algorithm law

- Karnataka's Platform-Based Gig Workers (Social Security and Welfare) Act, 2025 was notified on 12 September 2025. It requires algorithmic transparency for decisions affecting working conditions, non-discrimination in automated systems, and written reasons for deactivation [11][12].
- Telangana's Gig and Platform Workers Bill, 2025 also includes algorithmic transparency and covers about 4 lakh workers [13].
- Tamil Nadu set up a Gig Workers Welfare Board expected to register over 1 lakh workers [14].

Bengaluru and Hyderabad are India's gig-platform hubs. A tool that helps workers or regulators check platform decisions has a direct legal hook.

Relevant statement: Responsible AI 1 (Gig-Work Algorithm Fairness).

### 5. South India is ageing fastest, but also most digitally prepared

- Kerala has India's highest share of people aged 60+ (14.4% per SRS 2021; some sources give 16.5%). Tamil Nadu follows at 12.9%, against a national average of about 9% [15][16]. Kerala's share is projected to reach 22.8% within a decade [15].
- Kerala declared itself India's first fully digitally literate state in August 2025 after the Digi Keralam campaign trained about 21 lakh people aged 14+, including people over 100 [17]. Basic literacy does not equal ability to complete complex tasks such as banking or welfare forms, so assisted interfaces are still needed.
- AP has issued about 9.5 lakh UDID disability cards, third highest in India [33].

Relevant statements: Accessibility 7 (Elderly and Low-Literacy Access) and Accessibility 1 (Offline Document Accessibility).

### 6. Cyber fraud, including impersonation calls, is a major South Indian problem

- Indians lost ₹22,845.73 crore to cyber fraud in 2024, up about 206% from ₹7,465.18 crore in 2023 [22].
- Karnataka lost ₹312.5 crore to "digital arrest" scams (fraudsters posing as police on audio or video calls) over three years [23]. Bengaluru alone accounted for ₹1,543 crore of cyber fraud losses by November 2025, about 76% of Karnataka's total [24].
- The searches did not find reliable South India-specific statistics on AI voice cloning. The impersonation-call problem is well documented; the share that uses synthetic voices is not.

Relevant statement: Responsible AI 2 (Voice Cloning and Audio Scams).

### 7. Urban civic and environmental stress is high, but tools already exist

- Chennai (Namma Chennai) and Bengaluru (Namma Bengaluru / Sahaaya 2.0) already run grievance apps [27][28]. A municipal complaint-mapping project competes with these but can add value by merging channels, deduplicating and mapping hotspots.
- Bellandur and Varthur lakes in Bengaluru foam and catch fire, with about 40% of the city's sewage reported to enter Bellandur's catchment [25].

Relevant statements: Sustainability 6 (Municipal Action Mapping) and Sustainability 7 (Lake and River Tipping Points).

### 8. Education and energy themes are real but weaker hooks in the south

- Kerala already trained 80,000 teachers in AI and added AI to its Class 7 ICT textbook [34]. An AI literacy platform (Education 3) is therefore less novel in Kerala.
- ASER 2024 shows Tamil Nadu recovering strongly in arithmetic, while Andhra Pradesh and Telangana declined [35][36]. This supports Education 5 (Equitable Personalised Learning) for AP and Telangana.
- Smart-meter rollout is uneven: Tamil Nadu had installed under 10,000 of about 3 crore sanctioned prepaid smart meters, and Karnataka did not join RDSS [29]. Energy waste reduction (Sustainability 1) therefore lacks the meter data it assumes in much of the south.
- India generated about 12.5 lakh tonnes of e-waste in FY 2023-24 (CPCB) and most is handled informally [32]. The problem is real but mainly concentrated in northern clusters in coverage found.

### 9. Indian-language AI tooling makes accessibility and multilingual builds feasible

AI4Bharat (IIT Madras) and the national Bhashini platform provide open models for translation (IndicTrans2), speech recognition and TTS covering Tamil, Telugu, Kannada and Malayalam [30][31]. This lowers the cost of any solution that needs local-language voice or text.

### 10. Full ranking of all 35 statements

Scores out of 100. R = relevance (30%), D = data (20%), F = feasibility (20%), A = appeal (15%), P = policy fit (15%). Each criterion scored 1–5.

| Rank | Statement | R | D | F | A | P | Score | Main South India hook |
|---|---|---|---|---|---|---|---|---|
| 1 | SUS-4 Sustainable Fishing Support | 5 | 4 | 4 | 5 | 4 | 89 | TN/Kerala fisheries, INCOIS PFZ, IMBL arrests [18][20][21] |
| 1 | HAC-6 Human-AI Disaster Damage Assessment | 5 | 4 | 4 | 4 | 5 | 89 | Michaung, Montha, Wayanad [1][3][5] |
| 3 | SUS-3 Climate-Disaster Preparedness | 5 | 5 | 3 | 3 | 5 | 86 | Floods, cyclones, heat [4][26][38] |
| 4 | REA-5 Wrongful Welfare Rejections | 5 | 3 | 4 | 5 | 4 | 85 | Telangana Samagra Vedika [8][9] |
| 5 | REA-1 Gig-Work Algorithm Fairness | 5 | 2 | 4 | 5 | 5 | 84 | Karnataka and Telangana gig laws [11][13] |
| 5 | SUS-6 Municipal Action Mapping | 5 | 4 | 5 | 2 | 4 | 84 | Chennai, Bengaluru grievance systems [27][28] |
| 7 | ACC-7 Elderly and Low-Literacy Access | 5 | 3 | 4 | 4 | 4 | 82 | Kerala/TN ageing [15][16] |
| 8 | REA-2 Voice Cloning and Audio Scams | 5 | 3 | 3 | 4 | 4 | 78 | Bengaluru cyber fraud [23][24] |
| 9 | ACC-1 Offline Document Accessibility | 4 | 4 | 3 | 4 | 4 | 76 | Indic OCR/TTS available [30] |
| 9 | ACC-6 Govt Accessibility Testing | 3 | 5 | 5 | 2 | 4 | 76 | State e-gov portals |
| 11 | HAC-2 Doctor–CHW Decision Support | 4 | 3 | 3 | 3 | 4 | 69 | Community health worker networks |
| 11 | SUS-7 Lake/River Tipping Points | 4 | 3 | 3 | 4 | 3 | 69 | Bellandur, Varthur [25] |
| 11 | EDU-5 Equitable Personalised Learning | 4 | 3 | 3 | 3 | 4 | 69 | AP/Telangana ASER decline [36] |
| 14 | ACC-4 Educational Video Accessibility | 3 | 4 | 4 | 2 | 3 | 65 | Indic captioning tools [30] |
| 14 | REA-6 Explainable Financial/Legal AI | 3 | 3 | 5 | 2 | 3 | 65 | General |
| 14 | EDU-3 AI Literacy Gap | 3 | 3 | 5 | 2 | 3 | 65 | Kerala already active [34] |
| 17 | HAC-4 Multi-Stakeholder Facilitation | 3 | 3 | 4 | 3 | 3 | 64 | Gram sabha meetings |
| 18 | REA-3 Children's Biometrics Consent | 3 | 2 | 4 | 3 | 4 | 63 | DPDP Rules 2025 [37] |
| 18 | EDU-1 Preventing Cognitive Offloading | 3 | 2 | 4 | 4 | 3 | 63 | General |
| 20 | SUS-1 Energy Waste Reduction | 3 | 3 | 4 | 2 | 3 | 61 | Smart meters stalled in TN [29] |
| 20 | SUS-2 Local Biodiversity Monitoring | 3 | 4 | 3 | 3 | 2 | 61 | Western Ghats |
| 22 | EDU-2 Assessing Genuine Competence | 3 | 2 | 4 | 3 | 3 | 60 | General |
| 23 | SUS-5 E-Waste Worker Protection | 3 | 2 | 3 | 4 | 3 | 59 | Informal sector [32] |
| 24 | HAC-3 Rehab Planning | 3 | 2 | 4 | 3 | 2 | 57 | General |
| 24 | EDU-4 Curriculum Design | 3 | 3 | 3 | 2 | 3 | 57 | General |
| 26 | HAC-1 Social Case Prioritisation | 3 | 2 | 3 | 3 | 3 | 56 | General |
| 26 | HAC-7 Grassroots Advocacy Co-Author | 2 | 3 | 5 | 2 | 2 | 56 | General |
| 26 | ACC-2 Real-Time Captions for Deaf Users | 3 | 3 | 2 | 3 | 3 | 56 | Code-mixed speech |
| 29 | ACC-3 Navigation for Visually Impaired | 3 | 2 | 2 | 4 | 3 | 55 | Hard without hardware |
| 30 | HAC-5 Classroom Co-Pilot | 3 | 2 | 3 | 2 | 3 | 53 | General |
| 31 | REA-4 Property Valuation Fairness | 2 | 3 | 3 | 3 | 2 | 51 | Weak Indian data |
| 31 | REA-7 Privacy-Preserving Personalisation | 2 | 3 | 3 | 2 | 3 | 51 | General |
| 31 | EDU-6 AI Companion Dependency | 2 | 2 | 4 | 3 | 2 | 51 | General |
| 31 | EDU-7 EdAI Governance and Procurement | 2 | 2 | 4 | 2 | 3 | 51 | General |
| 35 | ACC-5 Speech-Impairment Assistant | 2 | 2 | 2 | 4 | 2 | 46 | Needs on-device fine-tuning |

Codes: HAC = Human–AI Collaboration, ACC = Accessibility & Inclusion, REA = Responsible & Ethical AI, SUS = Sustainability, EDU = Education & Future Skills.

### 11. Deep dive on the top 5

#### 11.1 SUS-4 Sustainable Fishing Support (89)

- Why South India: TN and Kerala are the #2 and #3 marine fish producers; Karnataka and AP have long coasts [20]. IMBL arrests are a recurring political issue in Tamil Nadu [21].
- Existing solutions: INCOIS PFZ advisories and the FISH / SAMUDRA apps [18][19]. These give fish-zone maps and hazard alerts but do not combine fuel cost, catch history, regulation and boundary risk into one decision.
- Solution sketch: a Tamil/Malayalam voice-first advisor (WhatsApp or low-end Android) that takes PFZ data, IMD/INCOIS weather and wave forecasts, the annual fishing-ban calendar and the IMBL line. It suggests a trip plan, estimates fuel cost vs. expected catch, and warns before the boat nears the IMBL or a closed zone. Predictions are labelled separately from verified official data, as the statement requires.
- Data for demo: INCOIS PFZ web GIS, INCOIS ocean-state forecasts, public IMBL coordinates, CMFRI landings summaries, simple synthetic catch logs.
- Differentiator: boundary-safety alerts and "don't fish here" advice turn the product against overfishing, which answers the statement's explicit concern.

#### 11.2 HAC-6 Human-AI Disaster Damage Assessment (89)

- Why South India: Michaung, Montha and Wayanad caused thousands of crore in damage in 2023–2025, and states had to assess damage fast to claim central aid [1][5][6].
- Existing solutions: AP's Real-Time Governance Society is an example of state-led tech response [7]. Most field damage enumeration is still manual.
- Solution sketch: volunteers upload geotagged photos and short Tamil/Telugu/Malayalam voice notes. A vision model proposes a damage class (house, road, crop, utility) with confidence. The system asks for missing details. Reviewers approve or override. A live map shows verified vs. AI-only assessments in different colours, and a report exports in a format close to state relief memoranda.
- Data for demo: public disaster imagery datasets (for example xBD), OpenStreetMap, Bhuvan layers, sample images from Chennai 2023 flood coverage.
- Tip: merge SUS-3 preparedness features only if time allows. Keep the core on assessment.

#### 11.3 REA-5 Reducing Wrongful Welfare Rejections (85)

- Why South India: Telangana's Samagra Vedika is an internationally documented case with a Supreme Court-verified wrongful-exclusion rate of at least 7.5% [8][9].
- Solution sketch: a reviewer console that takes an automated eligibility decision and its input records, flags record conflicts (name mismatches, stale land or vehicle records, entity-resolution merges), explains the likely rejection reason in plain Telugu/English, routes high-risk cases to a human officer and logs every correction and appeal.
- Data for demo: synthetic citizen records modelled on the Al Jazeera and Amnesty descriptions. No real personal data should be used.
- Differentiator: strong story, clear ethics fit, directly answers the statement's "never decide from opaque AI alone" requirement.

#### 11.4 REA-1 Gig-Work Algorithm Fairness (84)

- Why South India: Karnataka's 2025 Act and Telangana's 2025 Bill both mandate algorithmic transparency; Tamil Nadu has a gig workers welfare board [11][13][14].
- Solution sketch: a worker-side app that logs trips, pay, ratings and deactivations; an auditor dashboard that detects pay or allocation gaps across worker groups; and a generator for written deactivation challenges that cite the Karnataka Act.
- Data risk: platforms do not share data. Demo must use synthetic or crowdsourced logs. This is the main weakness (data score 2).

#### 11.5 ACC-7 Elderly and Low-Literacy Access (82)

- Why South India: Kerala and Tamil Nadu have India's oldest populations [15][16]. Digital literacy campaigns exist [17] but complex tasks still defeat many older users.
- Solution sketch: a voice-first Tamil/Malayalam assistant for pension, ration and bank tasks, tolerant of slow speech and repeated questions, with a one-tap handover to a human helper (Akshaya centre staff, family member or bank).
- Data for demo: AI4Bharat ASR/TTS, IndicTrans2 [30][31], mock government forms.

## Analysis

- **Pattern 1: disasters and climate dominate.** Three of the top six statements (HAC-6, SUS-3, SUS-4) link to cyclones, floods, heat and ocean conditions. Southern states have large recent losses and strong public data (IMD, INCOIS, Bhuvan). Judges from any Indian background will recognise the need.
- **Pattern 2: South India has unusual legal and case-study hooks for Responsible AI.** Telangana's welfare algorithm and the Karnataka/Telangana gig laws give REA-5 and REA-1 concrete, citable anchors that most other regions lack. The trade-off is data: both demos must use synthetic data.
- **Pattern 3: crowded spaces score lower on appeal.** Municipal complaint mapping (SUS-6) is highly relevant and easy to build, but Chennai and Bengaluru already run grievance apps. Teams choosing it must show clear added value (merging channels, deduplication, hotspot prediction).
- **Pattern 4: some statements assume infrastructure the south does not yet have.** Energy waste reduction assumes smart-meter data, but Tamil Nadu's rollout had barely started and Karnataka is outside RDSS [29].
- **Fishing vs. disaster assessment.** Both score 89. Fishing is more distinctive (fewer teams likely to pick it) and very South India-specific. Disaster assessment is broader, has more public image data and is easier to demo visually. Choose by team strength: geospatial/data team → fishing; computer-vision team → disaster assessment.

## Risks and Uncertainties

| Finding | Confidence | Reason |
|---|---|---|
| 1. Disasters are the largest recurring cost | High | Multiple independent sources and official statements; exact loss figures vary slightly between sources |
| 2. Fisheries are large and stressed | High | CMFRI data via news, INCOIS official pages |
| 3. Telangana welfare exclusion | High | Al Jazeera/Pulitzer investigation read in full; Amnesty corroborates |
| 4. Gig-worker laws | High | Law firm and ILO tracker agree; Telangana status (bill vs. act) may have changed since sources |
| 5. Ageing and digital literacy | Medium | 14.4% vs. 16.5% conflict between sources (SRS vs. other estimates); SRS is more authoritative |
| 6. Cyber fraud | Medium | National figures from Parliament are solid; voice-cloning share unknown |
| 7. Civic and lake stress | Medium | Lake figures come from secondary sources |
| 8. Education and energy | Medium | ASER is reliable; smart-meter data may be out of date |
| 10. Ranking scores | Low–Medium | Author judgment; weights are defaults, not the official judging rubric |

Other risks:

- Montha loss figure: sources report ₹6,355.60 crore and ₹6,384 crore for the revised estimate [5][6]. Full articles could not be fetched to resolve this.
- Kerala's elderly share: 14.4% (SRS 2021) vs. 16.5% (other reports). SRS is the official survey and is preferred.
- Health, legal and financial features in any build must not be presented as professional advice.
- Using real personal data (welfare, gig or fisher records) in a demo would raise privacy issues under the DPDP Act and Rules 2025 [37]. Use synthetic data.

## Recommendations

1. **Pick SUS-4 Sustainable Fishing Support** if the team wants the most distinctive, South India-specific idea with public data (Findings 2, 11.1).
2. **Pick HAC-6 Human-AI Disaster Damage Assessment** if the team is stronger in computer vision and wants the most visual demo (Findings 1, 11.2).
3. **Pick REA-5 Welfare Rejections** if the team wants a strong ethics story and is comfortable building on synthetic data (Findings 3, 11.3).
4. Whatever the choice, build voice-first in at least one South Indian language using AI4Bharat or Bhashini tools. This raises relevance and judge appeal at low cost (Finding 9).
5. Avoid SUS-1, ACC-5 and ACC-3 unless the team has special hardware or data access (Findings 8, 10).
6. Before finalising, check the Solvix'26 official judging criteria and replace the default weights in Finding 10 with them.

## Conclusion Summary

Bottom line: the best Solvix'26 picks for South India are Sustainable Fishing Support and Human-AI Disaster Damage Assessment, with Welfare Rejections as a strong third.

- Cyclones, floods and landslides in Tamil Nadu, Andhra Pradesh and Kerala caused thousands of crores in losses in 2023–2025, so damage assessment and preparedness tools meet a real need (see Findings 1).
- Tamil Nadu and Kerala are India's second and third biggest sea-fishing states, fishers face falling catches, price swings and border arrests, and government fish-zone data is free to use (see Findings 2).
- Telangana's welfare algorithm wrongly cut food support for thousands of families, which makes the welfare-rejection problem very concrete (see Findings 3).
- Karnataka and Telangana passed new gig-worker laws that require platforms to explain their algorithms, but platform data is hard to get (see Findings 4).
- Kerala and Tamil Nadu have India's oldest populations, so simple voice-based help for elderly users is valuable (see Findings 5).
- Cyber fraud losses tripled in 2024, and Bengaluru is a hotspot, but how much involves AI-cloned voices is unknown (see Findings 6).
- Some topics are real but weaker choices: city complaint apps already exist, smart meters are not yet installed in most southern homes, and Kerala already trains teachers in AI (see Findings 7 and 8).

Next step: confirm the official Solvix'26 judging criteria, then choose between fishing and disaster assessment based on whether the team is stronger in data/maps or in image AI.

## Sources

1. Wikipedia, "Cyclone Michaung", accessed 2026-09-25. <https://en.wikipedia.org/wiki/Cyclone_Michaung> (accessed 2026-09-25)
2. Asia Insurance Post, "Cyclone Michaung: Economic and insured losses of Chennai floods will be much less than 2015 event", 2023-12. <https://asiainsurancepost.com/archives/46274> (accessed 2026-09-25)
3. Eos (The Landslide Blog), "The 30 July 2024 Wayanad landslides in Kerala, India", 2024. <https://eos.org/thelandslideblog/wayanad-landslides> (accessed 2026-09-25)
4. Down To Earth, "Wayanad disaster highlights need for multi-hazard early warning systems", 2024-08. <https://www.downtoearth.org.in/climate-change/wayanad-disaster-highlights-need-for-multi-hazard-early-warning-systems> (accessed 2026-09-25)
5. Deccan Herald, "Cyclone Montha aftermath: Andhra Pradesh estimates loss at Rs 5,265 crore", 2025-10. <https://www.deccanherald.com/india/andhra-pradesh/cyclone-montha-aftermath-andhra-pradesh-estimates-loss-at-rs-5265-crore-cm-chandrababu-naidu-3780894> (accessed 2026-09-25)
6. Deccan Herald, "Andhra Pradesh revises Cyclone Montha damage to Rs 6,384 cr, seeks urgent aid of Rs 900 cr", 2025-11. <https://www.deccanherald.com/india/andhra-pradesh/andhra-pradesh-revises-cyclone-montha-damage-to-rs-6384-cr-seeks-urgent-aid-of-rs-900-cr-3792990> (accessed 2026-09-25; full text blocked, figure from search extract)
7. Wikipedia, "Cyclone Montha", accessed 2026-09-25. <https://en.wikipedia.org/wiki/Cyclone_Montha> (accessed 2026-09-25)
8. Tapasya, Kumar Sambhav, Divij Joshi / Al Jazeera, "How an algorithm denied food to thousands of poor in India's Telangana", 2024-01-24. <https://www.aljazeera.com/economy/2024/1/24/how-an-algorithm-denied-food-to-thousands-of-poor-in-indias-telangana> (accessed 2026-09-25)
9. Amnesty International, "Use of Entity Resolution in India: Shining a light on how new forms of automation can deny people access to welfare", 2024-04. <https://www.amnesty.org/en/latest/research/2024/04/entity-resolution-in-indias-welfare-digitalization/> (accessed 2026-09-25)
10. The South First, "Telangana employs same tech to issue new ration cards that deleted 20 lakh names", 2024–2025. <https://thesouthfirst.com/telangana/telangana-employs-same-tech-to-issue-new-ration-cards-that-deleted-20-lakh-names/> (accessed 2026-09-25)
11. DLA Piper, "Karnataka's new platform-based gig worker protection", 2025. <https://knowledge.dlapiper.com/dlapiperknowledge/globalemploymentlatestdevelopments/2025/karnatakas-new-platform-based-gig-worker-protection> (accessed 2026-09-25)
12. ILO Digital Labour Platform Tracker, "Karnataka Platform Based Gig Workers (Social Security and Welfare) Act, 2025", 2025. <https://digitallabour.ilo.org/legislation/karnataka-platform-based-gig-workers-social-security-and-welfare-act-2025> (accessed 2026-09-25)
13. Lexology, "Telangana's Gig Workers Bill 2025: A New Deal for the Digital Workforce", 2025. <https://www.lexology.com/library/detail.aspx?g=f1b60fe1-9f81-46cf-b26a-4a69d9bc8579> (accessed 2026-09-25)
14. Outlook India, "Tamil Nadu Govt Forms Welfare Board to Cater to Gig Workers", 2023. <https://www.outlookindia.com/national/tamil-nadu-govt-forms-welfare-board-to-cater-to-gig-workers-news-339589> (accessed 2026-09-25)
15. Onmanorama, "Ageing Kerala: Study warns elderly population to surge in coming decade", 2025-08-03. <https://www.onmanorama.com/news/kerala/2025/08/03/elderly-population-statistics-study-report-kerala.html> (accessed 2026-09-25)
16. The South First, "Grey wave rising as South India's population ages fast", 2024–2025. <https://thesouthfirst.com/health/grey-wave-rising-as-south-indias-population-ages-fast/> (accessed 2026-09-25)
17. LSGD Kerala, "Digi Keralam: Kerala goes 100% digital", 2025-08. <https://lsgd.kerala.gov.in/en/latest_news/digikeralam-kerala-goes-100-digital/> (accessed 2026-09-25)
18. INCOIS, "Potential Fishing Zone (PFZ) Advisory". <https://incois.gov.in/MarineFisheries/PfzAdvisory> (accessed 2026-09-25)
19. ETV Bharat, "INCOIS FISH App Helps Fishermen Locate Fish, Track Marine Hazards", 2026-09. <https://www.etvbharat.com/en/state/incois-fish-app-helps-fishermen-locate-fish-track-marine-hazards-enn26091107835> (accessed 2026-09-25)
20. Business Standard, "India's marine fish landings drop 2% to 3.47 million tonnes in 2024", 2025-08-04. <https://www.business-standard.com/economy/news/indias-marine-fish-landings-fall-kerala-gujarat-2024-125080401070_1.html> (accessed 2026-09-25; figures from search extract)
21. News On Air, "Sri Lankan Navy arrests 35 Indian fishermen from Tamil Nadu and Karaikal for trespassing", 2025-11. <https://www.newsonair.gov.in/sri-lankan-navy-arrests-35-indian-fishermen-from-tamil-nadu-and-karaikal-for-trespassing> (accessed 2026-09-25)
22. India TV News, "Indians lost over Rs 22,845 crore to cyber fraud in 2024; incidents skyrocket by 206%: Government", 2025-07-22. <https://www.indiatvnews.com/technology/news/indians-lost-over-rs-22-845-crore-to-cyber-fraud-in-2024-incidents-skyrocket-by-206-government-2025-07-22-1000037> (accessed 2026-09-25)
23. Vartha Bharati, "Karnataka lost Rs 312.5 crore in 'digital arrest' scam over three years: Minister", 2025–2026. <https://english.varthabharati.in/karnataka/karnataka-lost-rs-3125-crore-in-digital-arrest-scam-over-three-years-minister> (accessed 2026-09-25)
24. The420.in, "Cyber Fraud Ravages State Capital: Bengaluru Loses ₹4.83 Crore Every Day", 2025. <https://the420.in/bengaluru-cyber-fraud-losses-1543-crore-daily-4-83-crore-2025/> (accessed 2026-09-25)
25. Down To Earth, "Bellandur Lake: a story of toxic froth and fire". <https://www.downtoearth.org.in/environment/bellandur-lake-a-story-of-toxic-froth-and-fire-57139> (accessed 2026-09-25)
26. Insights on India, "Bengaluru Urban Flooding: Causes, Impacts & Sustainable Solutions", 2025-05-21. <https://www.insightsonindia.com/2025/05/21/bengaluru-urban-flooding/> (accessed 2026-09-25)
27. Greater Chennai Corporation, "Namma Chennai" (Google Play listing). <https://play.google.com/store/apps/details?id=com.ceedeev.grivenancev2&hl=en_IN> (accessed 2026-09-25)
28. BBMP, "Namma Bengaluru (Sahaaya 2.0)" (Google Play listing). <https://play.google.com/store/apps/details?id=com.nammabengaluruNew.org&hl=en> (accessed 2026-09-25)
29. Prayas (Energy Group), "Smart Metering in India: A work in progress". <https://energy.prayaspune.org/power-perspectives/smart-metering-in-india-a-work-in-progress> (accessed 2026-09-25)
30. AI4Bharat, IIT Madras, homepage. <https://ai4bharat.iitm.ac.in/> (accessed 2026-09-25)
31. AI4Bharat, "IndicTrans2". <https://ai4bharat.iitm.ac.in/areas/model/NMT/IndicTrans2> (accessed 2026-09-25)
32. Wikipedia, "Electronic waste in India" (cites CPCB data). <https://en.wikipedia.org/wiki/Electronic_waste_in_India> (accessed 2026-09-25)
33. WeCapable, "Disabled Population in India: Data and Facts" (Census 2011, UDID portal figures). <https://wecapable.com/disabled-population-india-data/> (accessed 2026-09-25)
34. IndiaAI, "Kerala launches groundbreaking AI training program for 80,000 school teachers", 2024. <https://indiaai.gov.in/news/kerala-launches-groundbreaking-ai-training-program-for-80-000-school-teachers> (accessed 2026-09-25)
35. The News Minute, "ASER 2024: Tamil Nadu sees recovery in learning, but not to pre-pandemic levels", 2025-01. <https://www.thenewsminute.com/tamil-nadu/aser-2024-tamil-nadu-shows-progress-in-education-but-gaps-remain> (accessed 2026-09-25)
36. Insights on India, "ASER Report 2024 Summary", 2025-01-29. <https://www.insightsonindia.com/2025/01/29/aser-report-2024/> (accessed 2026-09-25)
37. Wikipedia, "Digital Personal Data Protection Rules, 2025". <https://en.wikipedia.org/wiki/Digital_Personal_Data_Protection_Rules,_2025> (accessed 2026-09-25)
38. WRI India, "Mapping a Path for Heat Resilience in Tamil Nadu". <https://wri-india.org/perspectives/mapping-path-heat-resilience-tamil-nadu> (accessed 2026-09-25)
39. Onmanorama, "Why Kerala warmed up like never before in a century in 2024?", 2025-02-15. <https://www.onmanorama.com/news/kerala/2025/02/15/kerala-temperature-heatwave-2024-hottest-year-weather-climate-change.html> (accessed 2026-09-25)
40. Solvix'26, "Round 1 Problem Statements" (PDF provided by user), 2026. Local file, not in repository.
