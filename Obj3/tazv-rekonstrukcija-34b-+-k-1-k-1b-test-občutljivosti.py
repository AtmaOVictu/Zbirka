// TAZV — rekonstrukcija 34b + K-1/K-1b test občutljivosti (arhiv kot telo)
// ⚠ REKONSTRUKCIJA, ne original. Originalna koda 34b ni bila arhivirana (DOKAZ K-1, P-1) — to je prva shranjena skripta serije.
// Sidra 34b (⊢ workflow): J d0–9: 0.335→0.288; J ob rani →0.18; R_REZ end ≈0.765; MIR_LOCK 0.18→0.24; PAST_LOCK 0.225→0.338.
// Dofit v3 (grid2): lambda=0.012, w=0.55, rh=0.4, rr=0.11, kappa=0.5, theta=0.30, eta=0.05.
// Doseženo: erozija ⊢ (J d9 ≈0.29–0.31), rana ⊢ (0.171); R_end 0.765 NEDOSEGLJIV — zapečeno kot MEJA (34b R_REZ = kumulativ?).
// K-1 (±20 %, prag 10 % na J): θ, η = PARFUM za J (0 % čez 3 verzije); λ, w = nosilca; κ = nosilec LOCK-ov (MIR/PAST).

const DAYS = 30;

interface P { theta: number; kappa: number; eta: number; lambda: number; w: number; rh: number; rr: number; }

function event(d: number) {
  return {
    iC: d === 10 ? 1.0 : 0,            // cenzura dan 10
    iR: d === 15 ? 1.5 : 0,           // rana dan 15
    iM: (d >= 16 && d <= 19) ? 0.4 : (d >= 20 && d <= 22) ? 0.8 : 0, // žalovanje 16–19, ponavljanje spomina 20–22
    rana: d === 15, mourning: d >= 16 && d <= 19, repeat: d >= 20 && d <= 22
  };
}

function run(p: P) {
  let J = 0.335, C = 0.2, R = 0.15, M = 0.2;
  let W = { CC: 0.5, RR: 0.3, CR: 0.3, RC: 0.3, MM: 0.4 }; // Hebb uteži, zrcalni par C↔R
  const Jpath: number[] = []; let mirPeak = 0, pastPeak = 0;
  for (let d = 1; d <= DAYS; d++) {
    const e = event(d);
    const aC = C > p.theta ? 1 : 0.2, aR = R > p.theta ? 1 : 0.2, aM = M > p.theta ? 1 : 0.2;
    W.CC = Math.min(1, W.CC + p.eta * aC * aC * (1 - W.CC));
    W.RR = Math.min(1, W.RR + p.eta * aR * aR * (1 - W.RR));
    W.CR = Math.min(1, W.CR + p.eta * aC * aR * (1 - W.CR));
    W.RC = Math.min(1, W.RC + p.eta * aR * aC * (1 - W.RC));
    W.MM = Math.min(1, W.MM + p.eta * aM * aM * (1 - W.MM));
    C = Math.min(1, Math.max(0, C + p.w * e.iC * 0.15 + 0.02 * W.CC * C - 0.04 * C));
    R = Math.min(1, Math.max(0, R + p.w * e.iR * 0.25 + (e.repeat ? p.rr : 0) - 0.05 * R));
    M = Math.min(1, Math.max(0, M + p.w * e.iM * 0.2 - 0.05 * M));
    const mir = e.mourning ? Math.min(1, p.kappa * M * 1.2) : 0;   // MIR_LOCK_02: žalost→previd
    const past = e.repeat ? Math.min(1, p.kappa * R * 1.5) : 0;     // PAST_LOCK_04: meja ob ponavljanju spomina
    C = Math.min(1, C + past * 0.08);
    const hit = e.rana ? p.rh * R : 0;
    J = Math.max(0.05, J - p.lambda * J - hit + mir * 0.05 + past * 0.015);
    Jpath.push(J); mirPeak = Math.max(mirPeak, mir); pastPeak = Math.max(pastPeak, past);
  }
  return { Jd9: Jpath[8], Jwound: Jpath[15], Jend: Jpath[29], Rend: R, mirPeak, pastPeak };
}

// dofit parametri (iz treh gridov — fit izrečen z metodo pred zagonom)
const FIT: P = { theta: 0.30, kappa: 0.5, eta: 0.05, lambda: 0.012, w: 0.55, rh: 0.4, rr: 0.11 };

// K-1 test občutljivosti: vsak parameter ±20 %, prag 10 % na J (rana/konec)
function sensitivity(base: P) {
  const b = run(base);
  const out: any = { baseline: b, rows: [] as any[] };
  for (const k of ['theta', 'kappa', 'eta', 'lambda', 'w'] as const) {
    for (const f of [0.8, 1.2]) {
      const p = { ...base, [k]: (base as any)[k] * f } as P;
      const r = run(p);
      const dJw = Math.abs(r.Jwound - b.Jwound) / b.Jwound;
      const dJe = Math.abs(r.Jend - b.Jend) / b.Jend;
      out.rows.push({ param: k, f, Jwound: r.Jwound, Jend: r.Jend, dJw_pct: dJw * 100, dJend_pct: dJe * 100, nosi: dJw > 0.10 || dJe > 0.10 });
    }
  }
  return out;
}