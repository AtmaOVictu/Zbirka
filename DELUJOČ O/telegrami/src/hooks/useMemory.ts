// =============================================================================
// USE MEMORY HOOK: Upravljanje stanja spominskih sistemov
// Koncept: Zaves + Delovni Spomin + Shramba = Celoten sistem
// (A4: Implicitni korak - vse operacije v enem koraku)
// =============================================================================

import { useState, useEffect, useCallback, useRef } from 'react';
import { Telegram, AppState, CategoryKey, LogEntry, FlashState } from '../types';
import { CONFIG, CATEGORIES, TELEGRAM_POOL, REFS } from '../utils/constants';
import { classifyWithReason, createTelegram } from '../utils/classify';
import { isWMFull, getOverflowTelegram, shouldDie, ageAllTelegrams } from '../utils/age';
import { consolidateMemory, createSleepLogMessage } from '../utils/consolidate';
import { Zaves } from '../utils/zaves';

// --- Initial State ---
const initialStored: Record<CategoryKey, string[]> = {
  epizodicni: [],
  semanticni: [],
  proceduralni: [],
  priming: [],
  delovni: [],
};

const initialState: AppState = {
  utrujenost: 30,
  cudenje: 60,
  nagrada: false,
  running: true,
  wm: [],
  stored: initialStored,
  log: [],
  flash: undefined,
};

// --- Helper: Generate Log ID (A3: Drugi izvod - idempotentno) ---
let logIdCounter = 0;
const nextLogId = () => ++logIdCounter;

// --- Main Hook ---
export const useMemory = () => {
  const [state, setState] = useState<AppState>(initialState);
  const wmRef = useRef<Telegram[]>([]); // For closure-safe access
  const tidRef = useRef(0); // Globalni ID counter (A6: Protokol pred delom)

  // Sync refs with state
  useEffect(() => {
    wmRef.current = state.wm;
  }, [state.wm]);

  // --- Helper Functions ---

  /**
   * Dodaj log vnos (A1: Obseg pred - ekspliciten)
   */
  const pushLog = useCallback((
    msg: string,
    tone: string = 'text-zinc-600'
  ) => {
    setState((prev) => ({
      ...prev,
      log: [
        { id: nextLogId(), msg, tone },
        ...prev.log.slice(0, 39), // Keep last 40 entries
      ],
    }));
  }, []);

  /**
   * Ustvari novi telegram (A7: Sintaksa pred - preverjeno)
   */
  const newTelegram = useCallback((): Telegram => {
    const randomIndex = Math.floor(Math.random() * TELEGRAM_POOL.length);
    const template = TELEGRAM_POOL[randomIndex];
    return {
      id: ++tidRef.current,
      ...template,
      age: 0,
      named: false,
      rep: 0,
    };
  }, []);

  /**
   * Poimenuj telegram (T5, rez 63: klik = čudenje kot dejanje)
   */
  const nameTelegram = useCallback((telegram: Telegram) => {
    setState((prev) => {
      // A4: Implicitni korak - vse v enem setState
      const { utrujenost, cudenje, nagrada } = prev;
      const pozornost = (100 - utrujenost) / 100;
      const dopamin = nagrada && telegram.goal ? CONFIG.DOPAMIN_BOOST : 0;
      const novOdkrita = telegram.novelty * (cudenje / 100) * pozornost + dopamin;

      // Razvrsti
      const { category, reason } = classifyWithReason(
        telegram,
        utrujenost,
        cudenje,
        nagrada
      );

      // Odstrani iz WM
      const newWm = prev.wm.filter((t) => t.id !== telegram.id);

      // Dodaj v ustrezno kategorijo
      const newStored = {
        ...prev.stored,
        [category]: [...prev.stored[category], telegram.text],
      };

      // Flash animacija
      const flash: FlashState = { cat: category, timestamp: Date.now() };

      // Log
      pushLog(`"${telegram.text}" → ${CATEGORIES[category].label} (${reason})`, 
        category === 'epizodicni' ? 'text-amber-700' :
        category === 'proceduralni' ? 'text-emerald-700' :
        'text-sky-700'
      );

      return {
        ...prev,
        wm: newWm,
        stored: newStored,
        flash,
      };
    });
  }, [pushLog]);

  /**
   * Spanje: Konsolidacija (Rudoy 2009)
   */
  const sleep = useCallback(() => {
    setState((prev) => {
      if (prev.wm.length === 0) {
        pushLog('Ni telegramov v delovnem spominu — spanje brez učinka', 'text-zinc-500');
        return prev;
      }

      const { newStored, namedCount } = consolidateMemory(
        prev.wm,
        prev.stored
      );
      const restCount = prev.wm.length - namedCount;

      pushLog(
        createSleepLogMessage(namedCount, restCount),
        'text-fuchsia-700'
      );

      return {
        ...prev,
        running: false,
        wm: [],
        stored: newStored,
      };
    });
  }, [pushLog]);

  /**
   * Staranje telegramov v WM (A2: Vrnitev pred - konzistentno stanje)
   */
  const ageTelegrams = useCallback(() => {
    setState((prev) => {
      const { survived, died } = ageAllTelegrams(prev.wm);

      // Ne-poenovljeni, ki so ugasnili → PRIMING
      if (died.length > 0) {
        const newPriming = [...prev.stored.priming, ...died.map((t) => t.text)];
        died.forEach((t) => {
          pushLog(
            `"${t.text}" — ugasnil brez zaznamka → PRIMING (telegram, ki je padel med utrujenostjo)`,
            'text-zinc-400'
          );
        });

        return {
          ...prev,
          wm: survived,
          stored: {
            ...prev.stored,
            priming: newPriming,
          },
        };
      }

      return {
        ...prev,
        wm: survived,
      };
    });
  }, [pushLog]);

  /**
   * Dodaj nov telegram v WM (A5: Praznina z odprtjem)
   */
  const addTelegram = useCallback(() => {
    setState((prev) => {
      const telegram = newTelegram();
      let nextWm = [...prev.wm, telegram];
      let newPriming = [...prev.stored.priming];
      let logMsg: string | null = null;

      // Preveri kapaciteto WM (Zeigarnik: ~4)
      if (nextWm.length > CONFIG.WM_CAPACITY) {
        const [drop, ...rest] = nextWm;
        newPriming = [...prev.stored.priming, drop.text];
        nextWm = rest;
        logMsg = `"${drop.text}" — presežek delovnega spomina → PRIMING (implicitno; H.M. je pokazal: sistem deluje brez zavesti)`;
      }

      // Log overflow
      if (logMsg) {
        pushLog(logMsg, 'text-zinc-500');
      }

      return {
        ...prev,
        wm: nextWm,
        stored: {
          ...prev.stored,
          priming: newPriming,
        },
      };
    });
  }, [newTelegram, pushLog]);

  // --- Effects ---

  // Tok novih telegramov (A7: Sintaksa pred - intervali so konfigurabilni)
  useEffect(() => {
    if (!state.running) return;

    const interval = setInterval(() => {
      addTelegram();
    }, CONFIG.TELEGRAM_INTERVAL);

    return () => clearInterval(interval);
  }, [state.running, addTelegram]);

  // Staranje v WM
  useEffect(() => {
    if (!state.running) return;

    const interval = setInterval(() => {
      ageTelegrams();
    }, CONFIG.AGING_INTERVAL);

    return () => clearInterval(interval);
  }, [state.running, ageTelegrams]);

  // --- Computed Values ---
  const totalStored = Object.values(state.stored).reduce(
    (acc, curr) => acc + curr.length,
    0
  );

  // --- Public API ---
  return {
    state,
    setUtrujenost: (value: number) => setState((prev) => ({ ...prev, utrujenost: value })),
    setCudenje: (value: number) => setState((prev) => ({ ...prev, cudenje: value })),
    toggleNagrada: () => setState((prev) => ({ ...prev, nagrada: !prev.nagrada })),
    toggleRunning: () => setState((prev) => ({ ...prev, running: !prev.running })),
    nameTelegram,
    sleep,
    totalStored,
    pushLog,
    newTelegram,
    // Zaves methods
    zaves: {
      nextId: () => ++tidRef.current,
      resetId: () => { tidRef.current = 0; },
    },
  };
};

export type UseMemoryReturn = ReturnType<typeof useMemory>;
