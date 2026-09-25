import { createContext, useCallback, useContext, useState, type ReactNode } from 'react'

// Tamil strings are a first draft; a native speaker should review them before any real use.
const en = {
  appName: 'Meetpu',
  tagline: 'Satellites show where the water was. We show who lost what.',
  portal: 'Management portal',
  mockNotice: 'Demo build: OTP, SMS, payment and Revenue integrations are mocked. Seeded reports are synthetic.',
  'nav.map': 'Map',
  'nav.queue': 'Approval queue',
  'nav.stuck': 'Stuck cases',
  logout: 'Log out',
  login: 'Log in',
  username: 'Username',
  password: 'Password',
  loginHint: 'Demo login: collector / meetpu123',
  loginFailed: 'Wrong username or password',

  'status.reported': 'Reported',
  'status.verified': 'Verified',
  'status.rejected': 'Rejected',
  'status.approved': 'Approved',
  'status.paid': 'Paid',

  'flag.outside_flood_extent': 'Outside flood extent',
  'flag.gps_mismatch': 'Photo GPS mismatch',
  'flag.duplicate_photo': 'Duplicate photo',
  'flag.outside_event_window': 'Outside event dates',
  'flag.no_photo': 'No photo',
  'flag.no_exif_gps': 'No photo GPS',
  'flag.no_flood_layer': 'No flood layer',

  'asset.house': 'House',
  'asset.hut': 'Hut',
  'asset.cattle': 'Cattle',
  'asset.crop': 'Crop',
  'asset.boat': 'Boat',
  'asset.shop': 'Shop',
  'asset.other': 'Other',

  'damage.fully_damaged': 'Fully damaged',
  'damage.partially_damaged': 'Partially damaged',
  'damage.washed_away': 'Washed away',
  'damage.submerged': 'Submerged',
  'damage.dead': 'Dead',
  'damage.other': 'Other',

  approve: 'Approve',
  reject: 'Reject',
  pay: 'Release payment (mock)',
  note: 'Note',
  notePlaceholder: 'Reason or remarks',
  noteRequired: 'A note is required to reject',
  amount: 'Amount (₹)',
  confirm: 'Confirm',
  cancel: 'Cancel',
  back: 'Back',
  openCase: 'Open case',

  confidence: 'Confidence',
  flags: 'Flags',
  noFlags: 'No flags',
  district: 'District',
  allDistricts: 'All districts',
  taluk: 'Taluk',
  village: 'Village',
  asset: 'Asset',
  damage: 'Damage',
  severity: 'Severity',
  description: 'Description',
  reporter: 'Reporter',
  reportedAt: 'Reported',
  capturedAt: 'Photo taken',
  location: 'Location',
  photoGps: 'Photo GPS',
  inFlood: 'Inside flood extent',
  outFlood: 'Outside flood extent',
  unknownFlood: 'No flood layer',
  evidence: 'Evidence photo',
  noPhoto: 'No photo uploaded',
  history: 'Status history',
  grievances: 'Grievances',
  noGrievances: 'No grievances',
  paymentRef: 'Payment ref',
  status: 'Status',
  age: 'In stage',
  actions: 'Actions',
  synthetic: 'Synthetic',
  by: 'by',

  total: 'Total reports',
  flagged: 'Flagged',
  flaggedOnly: 'Flagged only',
  openGrievances: 'Open grievances',
  floodLayer: 'Flood extent',
  selectReport: 'Click a report on the map to see details.',
  reports: 'Reports',

  'tab.verified': 'Awaiting approval',
  'tab.approved': 'Awaiting payment',
  'tab.reported': 'Awaiting field verification',
  fieldOnly: 'Field staff verify these on site using the mobile app.',
  noRows: 'Nothing here right now.',

  exportPdna: 'Export PDNA CSV',
  exportNote: 'Approved and paid cases with evidence links. PDNA-style, not an official format.',
  stuckTitle: 'Where cases are stuck',
  stuckAfter: 'Stuck after',
  stuckCount: 'Stuck',
  oldest: 'Oldest',
  byArea: 'By area',
  overdue: 'Most overdue cases',
  noneStuck: 'No stuck cases.',
  hoursShort: 'h',
  daysShort: 'd',

  loading: 'Loading…',
  error: 'Something went wrong',
  retry: 'Retry',
}

type Key = keyof typeof en

const ta: Record<Key, string> = {
  appName: 'மீட்பு',
  tagline: 'செயற்கைக்கோள்கள் நீர் எங்கே இருந்தது என்று காட்டுகின்றன. யார் எதை இழந்தார் என்று நாங்கள் காட்டுகிறோம்.',
  portal: 'மேலாண்மைத் தளம்',
  mockNotice:
    'மாதிரிப் பதிப்பு: OTP, SMS, பணப் பரிமாற்றம், வருவாய்த் துறை இணைப்புகள் போலியானவை. பதிவேற்றப்பட்ட புகார்கள் மாதிரித் தரவு.',
  'nav.map': 'வரைபடம்',
  'nav.queue': 'ஒப்புதல் வரிசை',
  'nav.stuck': 'நிலுவை வழக்குகள்',
  logout: 'வெளியேறு',
  login: 'உள்நுழை',
  username: 'பயனர் பெயர்',
  password: 'கடவுச்சொல்',
  loginHint: 'மாதிரி உள்நுழைவு: collector / meetpu123',
  loginFailed: 'பயனர் பெயர் அல்லது கடவுச்சொல் தவறு',

  'status.reported': 'புகாரளிக்கப்பட்டது',
  'status.verified': 'சரிபார்க்கப்பட்டது',
  'status.rejected': 'நிராகரிக்கப்பட்டது',
  'status.approved': 'அங்கீகரிக்கப்பட்டது',
  'status.paid': 'தொகை வழங்கப்பட்டது',

  'flag.outside_flood_extent': 'வெள்ளப் பகுதிக்கு வெளியே',
  'flag.gps_mismatch': 'புகைப்பட இருப்பிட முரண்பாடு',
  'flag.duplicate_photo': 'நகல் புகைப்படம்',
  'flag.outside_event_window': 'நிகழ்வு நாட்களுக்கு வெளியே',
  'flag.no_photo': 'புகைப்படம் இல்லை',
  'flag.no_exif_gps': 'புகைப்பட இருப்பிடம் இல்லை',
  'flag.no_flood_layer': 'வெள்ள அடுக்கு இல்லை',

  'asset.house': 'வீடு',
  'asset.hut': 'குடிசை',
  'asset.cattle': 'கால்நடை',
  'asset.crop': 'பயிர்',
  'asset.boat': 'படகு',
  'asset.shop': 'கடை',
  'asset.other': 'மற்றவை',

  'damage.fully_damaged': 'முழுமையாகச் சேதம்',
  'damage.partially_damaged': 'பகுதியளவு சேதம்',
  'damage.washed_away': 'அடித்துச் செல்லப்பட்டது',
  'damage.submerged': 'நீரில் மூழ்கியது',
  'damage.dead': 'இறப்பு',
  'damage.other': 'மற்றவை',

  approve: 'அங்கீகரி',
  reject: 'நிராகரி',
  pay: 'தொகை விடுவி (மாதிரி)',
  note: 'குறிப்பு',
  notePlaceholder: 'காரணம் அல்லது கருத்து',
  noteRequired: 'நிராகரிக்கக் குறிப்பு அவசியம்',
  amount: 'தொகை (₹)',
  confirm: 'உறுதிசெய்',
  cancel: 'ரத்துசெய்',
  back: 'பின்செல்',
  openCase: 'வழக்கைத் திற',

  confidence: 'நம்பக மதிப்பு',
  flags: 'எச்சரிக்கைகள்',
  noFlags: 'எச்சரிக்கை இல்லை',
  district: 'மாவட்டம்',
  allDistricts: 'அனைத்து மாவட்டங்கள்',
  taluk: 'வட்டம்',
  village: 'கிராமம்',
  asset: 'சொத்து',
  damage: 'சேதம்',
  severity: 'தீவிரம்',
  description: 'விவரம்',
  reporter: 'புகார்தாரர்',
  reportedAt: 'புகார் நேரம்',
  capturedAt: 'புகைப்பட நேரம்',
  location: 'இருப்பிடம்',
  photoGps: 'புகைப்பட இருப்பிடம்',
  inFlood: 'வெள்ளப் பகுதிக்குள்',
  outFlood: 'வெள்ளப் பகுதிக்கு வெளியே',
  unknownFlood: 'வெள்ள அடுக்கு இல்லை',
  evidence: 'ஆதாரப் புகைப்படம்',
  noPhoto: 'புகைப்படம் பதிவேற்றப்படவில்லை',
  history: 'நிலை வரலாறு',
  grievances: 'குறைகள்',
  noGrievances: 'குறைகள் இல்லை',
  paymentRef: 'பரிவர்த்தனை எண்',
  status: 'நிலை',
  age: 'இந்த நிலையில்',
  actions: 'செயல்கள்',
  synthetic: 'மாதிரி',
  by: 'செய்தவர்',

  total: 'மொத்தப் புகார்கள்',
  flagged: 'எச்சரிக்கை உள்ளவை',
  flaggedOnly: 'எச்சரிக்கை உள்ளவை மட்டும்',
  openGrievances: 'திறந்த குறைகள்',
  floodLayer: 'வெள்ளப் பரப்பு',
  selectReport: 'விவரங்களைக் காண வரைபடத்தில் ஒரு புகாரைத் தேர்ந்தெடுக்கவும்.',
  reports: 'புகார்கள்',

  'tab.verified': 'ஒப்புதலுக்குக் காத்திருப்பவை',
  'tab.approved': 'தொகைக்குக் காத்திருப்பவை',
  'tab.reported': 'களச் சரிபார்ப்புக்குக் காத்திருப்பவை',
  fieldOnly: 'இவற்றைக் களப் பணியாளர்கள் கைபேசிச் செயலி மூலம் நேரில் சரிபார்க்கின்றனர்.',
  noRows: 'தற்போது எதுவும் இல்லை.',

  exportPdna: 'PDNA CSV ஏற்றுமதி',
  exportNote: 'ஆதார இணைப்புகளுடன் அங்கீகரிக்கப்பட்ட, தொகை வழங்கப்பட்ட வழக்குகள். PDNA வடிவத்தை ஒத்தது; அதிகாரப்பூர்வ வடிவம் அல்ல.',
  stuckTitle: 'வழக்குகள் எங்கே தேங்கியுள்ளன',
  stuckAfter: 'நிலுவை வரம்பு',
  stuckCount: 'நிலுவை',
  oldest: 'மிகப் பழையது',
  byArea: 'பகுதி வாரியாக',
  overdue: 'மிகத் தாமதமான வழக்குகள்',
  noneStuck: 'நிலுவை வழக்குகள் இல்லை.',
  hoursShort: 'மணி',
  daysShort: 'நாள்',

  loading: 'ஏற்றுகிறது…',
  error: 'ஏதோ தவறு நடந்தது',
  retry: 'மீண்டும் முயல்',
}

export type Lang = 'en' | 'ta'
const dicts: Record<Lang, Record<Key, string>> = { en, ta }
const LANG_KEY = 'meetpu.lang'

function initialLang(): Lang {
  try {
    return localStorage.getItem(LANG_KEY) === 'ta' ? 'ta' : 'en'
  } catch {
    return 'en'
  }
}

interface I18n {
  lang: Lang
  setLang: (l: Lang) => void
  t: (key: string) => string
}

const Ctx = createContext<I18n | null>(null)

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(initialLang)
  const setLang = useCallback((l: Lang) => {
    setLangState(l)
    try {
      localStorage.setItem(LANG_KEY, l)
    } catch {
      /* ignore */
    }
  }, [])
  const t = useCallback(
    (key: string) => dicts[lang][key as Key] ?? en[key as Key] ?? key,
    [lang],
  )
  return <Ctx.Provider value={{ lang, setLang, t }}>{children}</Ctx.Provider>
}

export function useI18n(): I18n {
  const v = useContext(Ctx)
  if (!v) throw new Error('useI18n outside I18nProvider')
  return v
}
