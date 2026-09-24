// =============================================================================
// TYPES: Zaves Simulacija Spominskih Sistemov
// Koncept: Zaves je svetovna pripoved — mehanizem razvrščanja žarkov/telegramov
// =============================================================================

// --- Core Types ---

export type TelegramKind = 'korpus' | 'rez' | 'svet' | 'šum' | '∂';
export type CategoryKey = 'epizodicni' | 'semanticni' | 'proceduralni' | 'priming' | 'delovni';

// --- Telegram Interface ---
export interface Telegram {
  id: number;
  text: string;
  kind: TelegramKind;
  novelty: number; // 0-1: novost (rez 62: dopamin je δ)
  age: number;    // starost v delovnem spominu (v korakih aging intervala)
  named: boolean; // ali je bil poimenovan (T5, rez 63: klik = čudenje kot dejanje)
  rep: number;    // število ponovitev
  goal?: boolean; // ciljni žarek (∂) - nagrajujoče kodiranje
}

// --- Category Interface (iz CAT v originalni kodi) ---
export interface Category {
  label: string;           // EPISODIČNI, SEMANTIČNI, itd.
  desc: string;            // opis
  color: string;           // Tailwind CSS classes
}

// --- Application State ---
export interface LogEntry {
  id: number;
  msg: string;
  tone: string; // Tailwind text color class
}

export interface FlashState {
  cat: CategoryKey;
  timestamp: number;
}

export interface AppState {
  utrujenost: number;      // 0-100: pozornostna vrata
  cudenje: number;        // 0-100: novostni detektor
  nagrada: boolean;        // δ (dopamin) - rez 62
  running: boolean;        // ali teče tok telegramov
  wm: Telegram[];          // delovni spomin (odprta ∂, kapaciteta 4)
  stored: Record<CategoryKey, string[]>; // shramba: epizodicni, semanticni, proceduralni, priming
  log: LogEntry[];        // dnevnik klasifikacij
  flash?: FlashState;     // animacija ob klasifikaciji
}

// --- Configuration Constants ---
export interface Config {
  TELEGRAM_INTERVAL: number;  // ms: interval pridobivanja novih telegramov
  AGING_INTERVAL: number;      // ms: interval staranja v WM
  WM_CAPACITY: number;        // kapaciteta delovnega spomina (Zeigarnik: ~4)
  CRITICAL_THRESHOLD: number; // prag za epizodični (novOdkrita >= 0.45)
  DOPAMIN_BOOST: number;       // dopamin bonus (rez 62: δ = 0.3)
  TMR_EFFECT: number;          // TMR ojačitev med spanjem (Rudoy 2009)
}

// --- Zaves Interface (konceptualni layer) ---
// Zaves = meja med svetom (telegrami) in zavestjo (spominski sistemi)
export interface ZavesFilter {
  shouldEnterWM: (currentWmLength: number) => boolean;
  classify: (telegram: Telegram, state: Pick<AppState, 'utrujenost' | 'cudenje' | 'nagrada'>) => CategoryKey;
  ageTelegram: (telegram: Telegram) => Telegram;
  shouldDie: (telegram: Telegram) => boolean; // ugaša ne-poenovljene
}

// --- Event Types ---
export type TelegramEvent = 
  | { type: 'ADD_TELEGRAM'; payload: Telegram }
  | { type: 'NAME_TELEGRAM'; payload: Telegram }
  | { type: 'AGE_TELEGRAMS' }
  | { type: 'SLEEP' }
  | { type: 'TOGGLE_RUNNING' }
  | { type: 'SET_UTRUJENOST'; payload: number }
  | { type: 'SET_CUDENJE'; payload: number }
  | { type: 'TOGGLE_NAGRADA' };
