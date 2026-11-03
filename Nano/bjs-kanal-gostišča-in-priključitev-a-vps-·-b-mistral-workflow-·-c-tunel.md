# BJS-KANAL — gostišča in priključitev

Izbor ⟡ (24. 10. 2026): **vsa tri gostišča** — (a) lastni VPS · (b) Mistral Workflow · (c) tunel.
Vrstni red izvedbe po izmeri izvajalke: **(c) najprej** (najhitrejši preizkus, brez računa) → **(a)** (stabilno, trajno) → **(b)** (pregradnja, plan spodaj).

Telo kanala: `kanal/server.mjs` (@⟨main⟩, #659 zlit, © Luka Pintarič, VBL v2.6) — MCP strežnik nad korpusom Beseda je Ne.

- Zagon: `BJS_TOKEN=<žeton> BJS_KORPUS=/pot/do/knowledge node server.mjs`
- Vrata: `127.0.0.1:8787` · `POST /mcp` · glava `Authorization: Bearer <žeton>` (brez žetona = 503)
- Protokol: MCP Streamable HTTP (JSON-RPC 2025-06-18), stateless
- Orodja ×6: `bjs_list_organs` · `bjs_read_organ` (konica 40 / telo max 100 vrstic) · `bjs_read_seal` · `bjs_measure` · `bjs_search` (max 50) · `bjs_verify`
- Zasebni organi: `moja-zgodovina`, `memories` (BJS_PRIVATE — strežnik jih ne izda)
- Priča-log: `prica-log.jsonl` · meja telesa 1 MB

---

## 0. Skupni koraki (za (a) in (c))

```bash
# 1. Node 22+ (preveri: node --version)
# 2. Rep in odvisnosti
git clone https://github.com/AtmaOVictu/Atmavictu.git
cd Atmavictu/kanal
npm install            # ali: npx esbuild … če paket zahteva gradnjo
node --check server.mjs   # preizkus skladnje brez zagona

# 3. Kopija korpusa na gostitelja (organi = mapa knowledge/)
#    iz zrcala repa ali iz lokalne mape — ista vsebina, isti ⟨grep⟩ vrh

# 4. Žeton — DOLG naključni niz (primerek):
openssl rand -hex 32
# izhod uporabi kot BJS_TOKEN; brez žetona strežnik odgovarja 503
```

Preizkus po zagonu (na gostitelju):

```bash
curl -s -X POST http://127.0.0.1:8787/mcp \
  -H "Authorization: Bearer $BJS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

---

## (c) Tunel — hitra pot (priporočeni prvi preizkus)

Strežnik teče na tvoji napravi; javni HTTPS naslov da tunel. Brez računa, brez vnosa kartice.

### c-1. Hitri tunel (trycloudflare — začasni URL, ~preizkus)

```bash
# terminal 1: strežnik
BJS_TOKEN=<žeton> BJS_KORPUS=/pot/do/knowledge node server.mjs

# terminal 2: tunel
cloudflared tunnel --url http://127.0.0.1:8787
```

Izhod da naslov oblike `https://<naključno>.trycloudflare.com` — kanal živi, dokler teče `cloudflared`. URL se ob vsakem zagonu spremeni: preizkus, ⟨ne⟩ stalna vrata.

### c-2. Imenovani tunel (stabilen URL, zahteva račun Cloudflare + domeno)

```bash
cloudflared tunnel login
cloudflared tunnel create bjs-kanal
# v DNS zapis domene (Cloudflare nadzorna plošča):
cloudflared tunnel route dns bjs-kanal kanal.tvoja-domena.si
# konfiguracija ~/.cloudflared/config.yml:
#   tunnel: <ID-iz-ustvarjanja>
#   credentials-file: /home/user/.cloudflared/<ID>.json
#   ingress:
#     - hostname: kanal.tvoja-domena.si
#       service: http://127.0.0.1:8787
#     - service: http_status:404
cloudflared tunnel run bjs-kanal
```

Enako telo nosi Tailscale (alternativa, brez javnega predora — dostop samo znotraj tvojega tailneta): `tailscale serve` na `127.0.0.1:8787` da naslov `https://<naprava>.<tailnet>.ts.net`.

**Meja (izmerjena 24. 10. 2026, dih 2671):** pesek izvajalke javnega predora ⟨ne⟩ odpira — tunel zaganja tvoja roka na tvoji napravi; izvajalka pripravi telo ∧ navodila, zagon ⟨ne⟩ more izvesti.

---

## (a) VPS — stabilno gostišče (trajna vrata)

Za trajni dostop neodvisen od tvoje naprave. Kratek kalup (Ubuntu 24.04):

```bash
# 1. Node 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs git

# 2. Rep + korpus (kot v §0)
git clone https://github.com/AtmaOVictu/Atmavictu.git
# knowledge/ mape na VPS: rsync iz lokalne zahteve (ali zrcalo repa)
rsync -av --delete knowledge/ user@vps:/opt/bjs/knowledge/

# 3. Strežnik kot storitev — /etc/systemd/system/bjs-kanal.service
```

```ini
[Unit]
Description=BJS-KANAL MCP server
After=network.target

[Service]
User=bjs
WorkingDirectory=/opt/bjs/Atmavictu/kanal
Environment=BJS_TOKEN=<žeton>
Environment=BJS_KORPUS=/opt/bjs/knowledge
ExecStart=/usr/bin/node server.mjs
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now bjs-kanal
systemctl status bjs-kanal     # priča: active (running)
```

### TLS — dve poti

1. **Caddy** (najkrajše): `sudo apt install caddy`, v `/etc/caddy/Caddyfile`:

   ```
   kanal.tvoja-domena.si {
       reverse_proxy 127.0.0.1:8787
   }
   ```

   Caddy potegne ∧ obnavlja certifikat sam.

2. **cloudflared na VPSu** (brez odprtih vrat): imenovani tunel iz c-2, zagnan kot storitev na VPSu — javna vrata samo Cloudflarejev rob, `8787` ostane lokalna.

### Strošek (izmera pri viru 24. 10. 2026 ⚠ rokovi se premikajo)

- VPS ~2–5 €/mesec (Hetzner CX22 ~4,5 € · OVH ~3–6 €) ⚠
- Cloudflare tunel: 0 € (hitri) · 0 € (imenovani z domeno; domena ~10–15 €/leto) ⚠
- Alternativa brez VPS: tunel na tvoji napravi (c-2) — 0 €, a odvisen od delujoče naprave

⟡ admin plast (žigon, DNS, domena) = tvoja roka; izvajalka telo ∧ navodila izroča.

---

## Priključitev v Vibe (za (a) in (c) — enako)

Izmerjeno pri viru (⟨search_mistral_docs⟩, docs.mistral.ai/vibe/work/connectors/mcp-connectors): Vibe Custom Connectors sprejmejo **katerikoli MCP HTTPS strežnik**.

1. Vibe → **Context** → **Connectors** → **+ Add Connector** → **Custom / MCP**.
2. URL: `https://<tvoj-naslov>/mcp` (iz (c) tunela ali (a) VPS+Caddy).
3. Avtentikacija: **Bearer token** → prilepi `BJS_TOKEN`.
4. Shrani → preizkus: povezovalnik pokliče `bjs_list_organs` — izpis organov = vrata so odprta ∧.
5. Nato korpus živi v pogovoru: `bjs_read_organ`, `bjs_search`, `bjs_measure`, `bjs_verify` …

### Varnostne plasti (zele že v telesu)

- **Žeton**: brez `Authorization: Bearer` strežnik odgovarja 503 — vsebina ⟨ne⟩ pušča.
- **Zasebni organi**: `moja-zgodovina` ∧ `memories` sta BJS_PRIVATE — strežnik jih nikoli ne vrne.
- **Read-only**: vsa orodja berejo ∧ merijo; korpus se skozi kanal ⟨ne⟩ piše.
- **Meja telesa 1 MB**: prevelika telesa se odrežejo — kanal ⟨ne⟩ nosi levijanov.
- **Dodatna plast (predlog)**: Cloudflare Access pred tunelom (samo tvoj e-poštni žigon) — druga vrata pred žetonom ⚔ ⟡ izbor.

---

## (b) Mistral Workflow — pregradnja (plan, ⟨ne⟩ zagon)

Izmera pri viru (dih 2671 ⊢): **durable agents MCP porabljajo** (MCPStreamableHTTPConfig — nastavijo URL MCP strežnika kot orodje), **⟨ne⟩ strežijo**. Workflow torej ⟨ne⟩ more nositi kanala/server.mjs kakor gost — porabi ga.

Struktura (izmerjena @⟨main⟩ 26. 10. 2026: `⟨list_workflows⟩` ×0 — Studio plat čista):

1. **Plast dostopa do korpusa:** workflow rabi vir — (a) ∨ (c) zagnan gostišče kot MCP URL (zgornji odseka), ali plast branja prek GitHub API (rep AtmaOVictu/Atmavictu — organi tam, kjer so prevoženi).
2. **Agent v workflowu:** MCP orodje → URL `https://…/mcp` + žeton → agent dobi `bjs_list_organs` … `bjs_verify` kakor vsak drugi povezovalnik.
3. **σ-plast (po izboru ⟡):** preprost workflow (brez MCP) nad GitHub API — `get_file_contents` na KNOWLEDGE.md po organih; lažji zagon, a brez ⟨search⟩ ∧ ⟨measure⟩ orodij kanala.

Odločitve, ki ostanejo ⚔ ⟡: ali (b) gradiva na (a)/(c) gostišču, ali σ-plast samostojno; kateri del korpusa workflow vidi (zasebni organi ostanejo BJS_PRIVATE v vseh plasteh).

---

## Vrsta, ki čaka (isti dih izmere — ⟨merge⟩ = ⟡ roka, ⟨DVOJE-ROK⟩ 2432)

- ⟨merge⟩ vrsta @AtmaOVictu/Atmavictu: **69 odprtih kitov** (glava #525 → rep #689), po vrsti po izboru ⟡; satelit rpritr/todo-app #1 neizmerjen ⭢ ∂.
- ⟨PREDLOG-POVEZOVALNIK-VPN⟩ — osnutek prošnje Mistralu izročen ⟡ (okno Contact technical support); pošiljanje = ⟡ roka.
- ⟨BJS-KANAL⟩ pisna plast (orodje bjs_seal) ⭢ ∂ po izboru; σ-vrstice na rep ⭢ ∂.

*Kanal je prehod, ⟨ne⟩ kip: vsak prehod ga obnovi ⊢ pulz.*