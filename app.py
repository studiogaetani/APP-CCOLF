# app.py
# GAETANI & PARTNERS Consulting – Cedolino Lavoro Domestico 2026
# Versione 2.0 – con fix normativi completi (4 fasce INPS, fascia 4 > 24h/sett,
# validazione CCNL, conviventi, retribuzione effettiva per fascia)

from __future__ import annotations
from dataclasses import dataclass, field
import streamlit as st
import datetime
import io

# ─────────────────────────────────────────────
# CONFIGURAZIONE PAGINA (deve essere primo comando st)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Gaetani & Partners – Cedolino Lavoro Domestico",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS PROFESSIONALE – Palette navy / oro
# ─────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }

:root {
    --navy:      #0D1F3C;
    --navy-mid:  #16325A;
    --navy-light:#1E4280;
    --gold:      #C9A84C;
    --gold-light:#E8C96A;
    --cream:     #FAF8F2;
    --white:     #FFFFFF;
    --border:    #D6CCB4;
    --text-dark: #1A1A2E;
    --text-mid:  #4A4A6A;
    --text-light:#7A7A9A;
}

.stApp { background: var(--cream); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 1280px; }

/* ── HEADER ── */
.gp-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 60%, var(--navy-light) 100%);
    padding: 1.8rem 3rem;
    margin: -1rem -1rem 2rem -1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid var(--gold);
    box-shadow: 0 4px 20px rgba(13,31,60,0.3);
}
.gp-header-left h1 {
    font-family: 'Playfair Display', serif;
    color: var(--white);
    font-size: 1.65rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: 0.3px;
}
.gp-header-left p {
    color: var(--gold-light);
    font-size: 0.82rem;
    margin: 0.2rem 0 0 0;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    font-weight: 300;
}
.gp-header-right {
    text-align: right;
    color: rgba(255,255,255,0.55);
    font-size: 0.78rem;
    line-height: 1.7;
}
.gp-header-right strong { color: var(--gold-light); }

/* ── CARD SEZIONE ── */
.gp-section {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(13,31,60,0.06);
}
.gp-section-title {
    font-family: 'Playfair Display', serif;
    color: var(--navy);
    font-size: 1rem;
    font-weight: 600;
    border-left: 3px solid var(--gold);
    padding-left: 0.75rem;
    margin-bottom: 1.2rem;
    letter-spacing: 0.2px;
}
.gp-divider { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }

/* ── METRIC GRID ── */
.gp-metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(155px, 1fr));
    gap: 0.9rem;
    margin: 1rem 0;
}
.gp-metric {
    background: var(--navy);
    border-radius: 4px;
    padding: 1rem 1.1rem;
    text-align: center;
    border-bottom: 3px solid var(--gold);
}
.gp-metric.highlight {
    background: linear-gradient(135deg, var(--navy-mid), var(--navy-light));
    border-bottom-color: var(--gold-light);
}
.gp-metric-label { color: rgba(255,255,255,0.6); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 0.35rem; }
.gp-metric-value { color: var(--gold-light); font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 600; }
.gp-metric-sub { color: rgba(255,255,255,0.4); font-size: 0.67rem; margin-top: 0.2rem; }

/* ── TABELLA CEDOLINO ── */
.ced-table { width: 100%; border-collapse: collapse; font-size: 0.89rem; }
.ced-table th {
    background: var(--navy);
    color: var(--gold-light);
    font-family: 'Playfair Display', serif;
    font-weight: 600;
    padding: 0.6rem 1rem;
    text-align: left;
    font-size: 0.8rem;
    letter-spacing: 0.5px;
}
.ced-table td { padding: 0.5rem 1rem; border-bottom: 1px solid #EDE9DF; color: var(--text-dark); }
.ced-table tr:last-child td { border-bottom: none; }
.ced-table .ced-total td { background: #F2EED8; font-weight: 600; color: var(--navy); border-top: 2px solid var(--gold); }
.ced-table .ced-netto td { background: var(--navy); color: var(--gold-light); font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; border-top: 2px solid var(--gold); }
.ced-table .ced-section-header td { background: #F7F4EC; color: var(--navy); font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.8px; padding: 0.38rem 1rem; }
.amt { text-align: right !important; font-variant-numeric: tabular-nums; }

/* ── BADGE FASCIA ── */
.fascia-badge { display: inline-block; padding: 0.18rem 0.65rem; border-radius: 2px; font-size: 0.73rem; font-weight: 600; letter-spacing: 0.4px; }
.fascia-1 { background: #E8F4E8; color: #1B5E20; border: 1px solid #A5D6A7; }
.fascia-2 { background: #FFF8E1; color: #7A4F00; border: 1px solid #FFE082; }
.fascia-3 { background: #FEE8E8; color: #8B1A1A; border: 1px solid #FFABAB; }
.fascia-4 { background: #E8F0FE; color: #1A4EA8; border: 1px solid #90B4F5; }

/* ── ALERT ── */
.gp-info  { background:#EDF2FF; border-left:3px solid var(--navy-light); padding:0.65rem 1rem; border-radius:0 4px 4px 0; font-size:0.82rem; color:var(--text-mid); margin:0.6rem 0; }
.gp-warn  { background:#FFF8E1; border-left:3px solid var(--gold); padding:0.65rem 1rem; border-radius:0 4px 4px 0; font-size:0.82rem; color:#5A3E00; margin:0.6rem 0; }
.gp-error { background:#FEE8E8; border-left:3px solid #C62828; padding:0.65rem 1rem; border-radius:0 4px 4px 0; font-size:0.82rem; color:#8B1A1A; margin:0.6rem 0; }

/* ── LOGIN ── */
.login-wrap { max-width:400px; margin:3rem auto; background:var(--white); border:1px solid var(--border); border-radius:4px; padding:2.5rem; box-shadow:0 8px 32px rgba(13,31,60,0.13); }
.login-logo { text-align:center; margin-bottom:1.8rem; }
.login-logo h2 { font-family:'Playfair Display', serif; color:var(--navy); font-size:1.5rem; margin:0; }
.login-logo p { color:var(--gold); font-size:0.72rem; letter-spacing:2.5px; text-transform:uppercase; margin:0.25rem 0 0 0; }
.login-divider { width:36px; height:2px; background:var(--gold); margin:0.7rem auto 0; }

/* ── SCADENZE ── */
.scad-grid { display:flex; gap:0.45rem; flex-wrap:wrap; margin:0.4rem 0; }
.scad-chip { background:var(--navy); color:var(--gold-light); padding:0.22rem 0.7rem; border-radius:2px; font-size:0.72rem; font-weight:500; letter-spacing:0.2px; }

/* ── FOOTER ── */
.gp-footer { text-align:center; padding:2rem 1rem; color:var(--text-light); font-size:0.73rem; border-top:1px solid var(--border); margin-top:3rem; letter-spacing:0.2px; line-height:1.8; }
.gp-footer strong { color:var(--navy); }
</style>
"""

# ─────────────────────────────────────────────
# TABELLE NORMATIVE 2026 – data-driven
# Fonte: Circ. INPS n. 9 del 03/02/2026 / Assindatcolf
# ─────────────────────────────────────────────
TABLES_2026: dict = {
    "anno": 2026,
    "fonte": "Circ. INPS n. 9 del 03/02/2026",
    "soglie_fasce": {"fascia1_max": 9.61, "fascia2_max": 11.70},
    "soglia_h_sett_fascia4": 24,
    "contributi": {
        "TI": {
            "F1": {"totale": 1.70, "lav": 0.43},
            "F2": {"totale": 1.92, "lav": 0.48},
            "F3": {"totale": 2.34, "lav": 0.59},
            "F4": {"totale": 1.24, "lav": 0.31},
        },
        "TD": {
            "F1": {"totale": 1.82, "lav": 0.43},
            "F2": {"totale": 2.05, "lav": 0.48},
            "F3": {"totale": 2.50, "lav": 0.59},
            "F4": {"totale": 1.32, "lav": 0.31},
        },
    },
    "cassacolf": {"totale": 0.06, "lav": 0.02},
    "minimi_orari": {
        "A": 6.51, "AS": 6.76, "B": 7.01, "BS": 7.45,
        "C": 7.86, "CS": 8.30, "D": 9.57, "DS": 9.97,
    },
    "minimi_mensili_conviventi": {
        "A": 908.10, "AS": 958.55, "B": 983.16, "BS": 1053.39,
        "C": 1123.63, "CS": 1193.84, "D": 1404.51, "DS": 1474.73,
    },
    "descrizione_livelli": {
        "A":  "A – Mansioni generiche base",
        "AS": "AS – Mansioni generiche specifiche",
        "B":  "B – Colf qualificata / baby-sitter",
        "BS": "BS – Colf esperta / badante base",
        "C":  "C – Badante qualificata",
        "CS": "CS – Badante specializzata",
        "D":  "D – Addetto non autosuff. qualificato",
        "DS": "DS – Addetto non autosuff. esperto",
    },
    "deduzione_inps_max": 1549.37,
    "detrazione_assistenza_max": 2100.00,
    "scadenze_versamento": ["10 Aprile", "10 Luglio", "10 Ottobre", "10 Gen. 2027"],
}

MESI_IT = {
    1: "Gennaio", 2: "Febbraio", 3: "Marzo", 4: "Aprile",
    5: "Maggio", 6: "Giugno", 7: "Luglio", 8: "Agosto",
    9: "Settembre", 10: "Ottobre", 11: "Novembre", 12: "Dicembre",
}

# ─────────────────────────────────────────────
# DOMAIN MODEL
# ─────────────────────────────────────────────
@dataclass
class PayrollInputs:
    mese: int
    anno: int
    tipo_contratto: str
    convivente: bool
    livello_ccnl: str
    ore_mese: float
    ore_settimanali: float
    paga_oraria_lorda: float | None
    paga_oraria_netto_target: float | None
    n_festivita: int
    include_festivita_contributi: bool
    ore_straordinario: float
    maggiorazione_straord_pct: float
    ore_ferie: float
    indennita_euro: float
    trattenute_varie_euro: float

@dataclass
class FasciaInfo:
    codice: str
    inps_tot_h: float
    inps_lav_h: float
    inps_dat_h: float
    retrib_eff_h: float
    label: str

@dataclass
class PayrollResults:
    paga_oraria_lorda: float
    paga_oraria_netta: float
    costo_orario_datore: float
    fascia: FasciaInfo
    ore_festivita_equiv: float
    ore_contributive: float
    lordo_base: float
    lordo_festivita: float
    lordo_straordinario: float
    lordo_ferie: float
    lordo_indennita: float
    lordo_totale: float
    inps_lav: float
    cassa_lav: float
    trattenute_varie: float
    trattenute_tot: float
    netto: float
    inps_datore: float
    cassa_datore: float
    costo_datore: float
    vers_inps_trim: float
    vers_cassa_trim: float
    vers_tot_trim: float
    rateo_13a: float
    tfr: float
    warnings: list[str] = field(default_factory=list)

# ─────────────────────────────────────────────
# CALCOLO
# ─────────────────────────────────────────────
def get_fascia(gross_h: float, ore_sett: float, tipo: str, t: dict) -> FasciaInfo:
    """Determina la fascia contributiva INPS corretta (4 fasce, Circ. 9/2026)."""
    soglie = t["soglie_fasce"]
    contributi = t["contributi"][tipo]

    # Fascia 4: orario settimanale > 24h (flat, indipendente dalla retrib.)
    if ore_sett > t["soglia_h_sett_fascia4"]:
        d = contributi["F4"]
        return FasciaInfo("F4", d["totale"], d["lav"], round(d["totale"] - d["lav"], 4),
                          gross_h, f"Fascia 4 – flat (> {t['soglia_h_sett_fascia4']}h/sett)")

    # Retribuzione effettiva oraria = paga × 13/12 (include rateo 13ª)
    retrib_eff = round(gross_h * 13 / 12, 4)

    if retrib_eff <= soglie["fascia1_max"]:
        d = contributi["F1"]; cod = "F1"
        label = f"Fascia 1 – retrib. eff. ≤ €{soglie['fascia1_max']:.2f}/h"
    elif retrib_eff <= soglie["fascia2_max"]:
        d = contributi["F2"]; cod = "F2"
        label = f"Fascia 2 – retrib. eff. > €{soglie['fascia1_max']:.2f} fino a €{soglie['fascia2_max']:.2f}/h"
    else:
        d = contributi["F3"]; cod = "F3"
        label = f"Fascia 3 – retrib. eff. > €{soglie['fascia2_max']:.2f}/h"

    return FasciaInfo(cod, d["totale"], d["lav"], round(d["totale"] - d["lav"], 4), retrib_eff, label)


def compute_payroll(inp: PayrollInputs, t: dict) -> PayrollResults:
    tipo = inp.tipo_contratto.upper().strip()
    if tipo not in ("TI", "TD"):
        tipo = "TD"
    warnings: list[str] = []
    cassa = t["cassacolf"]

    # 1. Paga lorda
    if inp.paga_oraria_lorda is not None:
        gross_h = float(inp.paga_oraria_lorda)
    elif inp.paga_oraria_netto_target is not None:
        # Stima con fascia 1 (poi la fascia viene ricalcolata)
        f1 = t["contributi"][tipo]["F1"]
        gross_h = max(0.0, inp.paga_oraria_netto_target + f1["lav"] + cassa["lav"])
    else:
        gross_h = 0.0

    # 2. Fascia contributiva (multifascia corretta)
    fascia = get_fascia(gross_h, inp.ore_settimanali, tipo, t)
    inps_lav_h = fascia.inps_lav_h
    inps_dat_h = fascia.inps_dat_h
    cassa_lav_h = cassa["lav"]
    cassa_dat_h = round(cassa["totale"] - cassa["lav"], 4)

    # 3. Netto e costo orario
    net_h = max(0.0, gross_h - inps_lav_h - cassa_lav_h)
    costo_orario = gross_h + inps_dat_h + cassa_dat_h

    # 4. Validazione minimo CCNL
    livello = inp.livello_ccnl
    if inp.convivente:
        min_m = t["minimi_mensili_conviventi"].get(livello, 0.0)
        paga_m = gross_h * inp.ore_mese
        if min_m > 0 and paga_m < min_m:
            warnings.append(
                f"⚠️ Retribuzione mensile equivalente ({euro(paga_m)}) inferiore al minimo CCNL "
                f"Livello {livello} per conviventi ({euro(min_m)}/mese)."
            )
    else:
        min_h = t["minimi_orari"].get(livello, 0.0)
        if min_h > 0 and gross_h < min_h - 0.001:
            warnings.append(
                f"⚠️ Paga oraria lorda ({euro(gross_h)}) inferiore al minimo CCNL "
                f"Livello {livello} ({euro(min_h)}/h). Verificare prima del pagamento."
            )

    # 5. Voci lorde
    ore = max(0.0, float(inp.ore_mese))
    fest = max(0, int(inp.n_festivita))
    lordo_base = ore * gross_h
    lordo_festivita = (lordo_base / 26.0) * fest if fest > 0 else 0.0
    lordo_straordinario = (max(0.0, inp.ore_straordinario) * gross_h
                           * (1.0 + max(0.0, inp.maggiorazione_straord_pct) / 100.0))
    lordo_ferie = max(0.0, inp.ore_ferie) * gross_h
    lordo_indennita = max(0.0, inp.indennita_euro)
    lordo_totale = lordo_base + lordo_festivita + lordo_straordinario + lordo_ferie + lordo_indennita

    # 6. Ore contributive
    ore_fest_equiv = (ore / 26.0) * fest if fest > 0 else 0.0
    ore_contr = (ore + max(0.0, inp.ore_ferie) + max(0.0, inp.ore_straordinario)
                 + (ore_fest_equiv if inp.include_festivita_contributi else 0.0))

    # 7. Contributi mensili
    inps_lav = ore_contr * inps_lav_h
    inps_dat = ore_contr * inps_dat_h
    cassa_lav = ore_contr * cassa_lav_h
    cassa_dat = ore_contr * cassa_dat_h
    trattenute_varie = max(0.0, inp.trattenute_varie_euro)
    trattenute_tot = inps_lav + cassa_lav + trattenute_varie
    netto = max(0.0, lordo_totale - trattenute_tot)
    costo_datore = lordo_totale + inps_dat + cassa_dat

    # 8. Versamento trimestrale
    ore_trim = ore_contr * 3.0
    vers_inps_trim = ore_trim * fascia.inps_tot_h
    vers_cassa_trim = ore_trim * cassa["totale"]
    vers_tot_trim = vers_inps_trim + vers_cassa_trim

    # 9. Accantonamenti
    rateo_13a = lordo_totale / 12.0
    tfr = lordo_totale / 13.5

    return PayrollResults(
        paga_oraria_lorda=gross_h, paga_oraria_netta=net_h, costo_orario_datore=costo_orario,
        fascia=fascia, ore_festivita_equiv=ore_fest_equiv, ore_contributive=ore_contr,
        lordo_base=lordo_base, lordo_festivita=lordo_festivita, lordo_straordinario=lordo_straordinario,
        lordo_ferie=lordo_ferie, lordo_indennita=lordo_indennita, lordo_totale=lordo_totale,
        inps_lav=inps_lav, cassa_lav=cassa_lav, trattenute_varie=trattenute_varie,
        trattenute_tot=trattenute_tot, netto=netto, inps_datore=inps_dat, cassa_datore=cassa_dat,
        costo_datore=costo_datore, vers_inps_trim=vers_inps_trim, vers_cassa_trim=vers_cassa_trim,
        vers_tot_trim=vers_tot_trim, rateo_13a=rateo_13a, tfr=tfr, warnings=warnings,
    )

# ─────────────────────────────────────────────
# HELPERS UI
# ─────────────────────────────────────────────
def euro(x: float) -> str:
    return f"€\u00a0{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def _row(label, val, bold=False, indent=False):
    pre = "&nbsp;&nbsp;&nbsp;" if indent else ""
    s = "font-weight:600;" if bold else ""
    return f"<tr><td style='{s}color:#2A2A4A'>{pre}{label}</td><td class='amt' style='{s}'>{val}</td></tr>"

def _section(label):
    return f"<tr class='ced-section-header'><td colspan='2'>{label}</td></tr>"

def _total(label, val):
    return f"<tr class='ced-total'><td>{label}</td><td class='amt'>{val}</td></tr>"

def _netto(label, val):
    return f"<tr class='ced-netto'><td>{label}</td><td class='amt'>{val}</td></tr>"

def table_html(rows_html: str) -> str:
    return (f"<table class='ced-table'>"
            f"<thead><tr><th>Voce</th><th style='text-align:right'>Importo</th></tr></thead>"
            f"<tbody>{rows_html}</tbody></table>")

def fascia_badge_html(fi: FasciaInfo) -> str:
    cls = {"F1":"fascia-1","F2":"fascia-2","F3":"fascia-3","F4":"fascia-4"}.get(fi.codice,"fascia-1")
    return f"<span class='fascia-badge {cls}'>{fi.codice}</span>&nbsp;{fi.label}"

# ─────────────────────────────────────────────
# GENERAZIONE PDF – RIEPILOGO GESTIONE MENSILE
# ─────────────────────────────────────────────
def genera_pdf_riepilogo(
    inp: PayrollInputs,
    res: PayrollResults,
    nome_lavoratore: str,
    nome_datore: str,
    t: dict,
) -> bytes:
    """Genera il riepilogo gestione mensile in PDF e restituisce i byte pronti per il download."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
    )
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

    # ── Palette colori (identica all'app web) ──
    NAVY      = colors.HexColor("#0D1F3C")
    NAVY_MID  = colors.HexColor("#16325A")
    GOLD      = colors.HexColor("#C9A84C")
    GOLD_LITE = colors.HexColor("#E8C96A")
    CREAM     = colors.HexColor("#FAF8F2")
    BORDER    = colors.HexColor("#D6CCB4")
    SECT_BG   = colors.HexColor("#F7F4EC")
    TOTAL_BG  = colors.HexColor("#F2EED8")
    WHITE     = colors.white
    DARK_TXT  = colors.HexColor("#1A1A2E")
    MID_TXT   = colors.HexColor("#4A4A6A")
    LITE_TXT  = colors.HexColor("#7A7A9A")
    RED_WARN  = colors.HexColor("#8B1A1A")

    buf = io.BytesIO()
    PAGE_W, PAGE_H = A4
    MARGIN = 18 * mm

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=12 * mm, bottomMargin=16 * mm,
        title=f"Riepilogo Gestione Mensile {MESI_IT[inp.mese]} {inp.anno}",
        author="Gaetani & Partners Consulting",
        subject="Riepilogo gestione mensile lavoro domestico",
    )

    # ── Stili tipografici ──
    def sty(name, **kw):
        return ParagraphStyle(name, **kw)

    S = {
        "firm_name": sty("firm_name", fontName="Helvetica-Bold", fontSize=15,
                         textColor=WHITE, alignment=TA_LEFT, leading=18),
        "firm_sub":  sty("firm_sub",  fontName="Helvetica",      fontSize=7.5,
                         textColor=GOLD_LITE, alignment=TA_LEFT, leading=11, spaceAfter=0),
        "header_r":  sty("header_r",  fontName="Helvetica",      fontSize=7,
                         textColor=colors.HexColor("#AABBCC"), alignment=TA_RIGHT, leading=10),
        "section":   sty("section",   fontName="Helvetica-Bold",  fontSize=8,
                         textColor=NAVY, leading=10),
        "label":     sty("label",     fontName="Helvetica",       fontSize=8.5,
                         textColor=DARK_TXT, leading=11),
        "label_ind": sty("label_ind", fontName="Helvetica",       fontSize=8.5,
                         textColor=MID_TXT,  leading=11, leftIndent=8),
        "value":     sty("value",     fontName="Helvetica",       fontSize=8.5,
                         textColor=DARK_TXT, alignment=TA_RIGHT, leading=11),
        "value_b":   sty("value_b",   fontName="Helvetica-Bold",  fontSize=8.5,
                         textColor=NAVY,     alignment=TA_RIGHT, leading=11),
        "total_l":   sty("total_l",   fontName="Helvetica-Bold",  fontSize=9,
                         textColor=NAVY, leading=12),
        "total_v":   sty("total_v",   fontName="Helvetica-Bold",  fontSize=9,
                         textColor=NAVY, alignment=TA_RIGHT, leading=12),
        "netto_l":   sty("netto_l",   fontName="Helvetica-Bold",  fontSize=11,
                         textColor=GOLD_LITE, leading=14),
        "netto_v":   sty("netto_v",   fontName="Helvetica-Bold",  fontSize=11,
                         textColor=GOLD_LITE, alignment=TA_RIGHT, leading=14),
        "kpi_label": sty("kpi_label", fontName="Helvetica",       fontSize=6.5,
                         textColor=colors.HexColor("#AABBCC"), alignment=TA_CENTER,
                         leading=9, spaceAfter=1),
        "kpi_value": sty("kpi_value", fontName="Helvetica-Bold",  fontSize=10,
                         textColor=GOLD_LITE, alignment=TA_CENTER, leading=13),
        "kpi_sub":   sty("kpi_sub",   fontName="Helvetica",       fontSize=6,
                         textColor=colors.HexColor("#7899BB"), alignment=TA_CENTER, leading=8),
        "note":      sty("note",      fontName="Helvetica-Oblique", fontSize=7,
                         textColor=LITE_TXT, leading=9),
        "warn":      sty("warn",      fontName="Helvetica-Bold",  fontSize=7.5,
                         textColor=RED_WARN, leading=10),
        "footer":    sty("footer",    fontName="Helvetica",       fontSize=6.5,
                         textColor=LITE_TXT, alignment=TA_CENTER, leading=9),
        "info_lbl":  sty("info_lbl",  fontName="Helvetica-Bold",  fontSize=8,
                         textColor=MID_TXT, leading=10),
        "info_val":  sty("info_val",  fontName="Helvetica",       fontSize=8,
                         textColor=DARK_TXT, leading=10),
    }

    # ── Helper tabella generica ──
    COL_W = (PAGE_W - 2 * MARGIN)

    def base_style():
        return TableStyle([
            ("BACKGROUND",  (0, 0), (-1, -1), WHITE),
            ("GRID",        (0, 0), (-1, -1), 0.3, BORDER),
            ("LEFTPADDING",  (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING",   (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 3.5),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ])

    def section_row_style(idx):
        return [
            ("BACKGROUND",  (0, idx), (-1, idx), SECT_BG),
            ("SPAN",        (0, idx), (-1, idx)),
            ("TOPPADDING",  (0, idx), (-1, idx), 2.5),
            ("BOTTOMPADDING",(0, idx), (-1, idx), 2.5),
        ]

    def total_row_style(idx):
        return [
            ("BACKGROUND",   (0, idx), (-1, idx), TOTAL_BG),
            ("LINEABOVE",    (0, idx), (-1, idx), 1.2, GOLD),
            ("FONTNAME",     (0, idx), (-1, idx), "Helvetica-Bold"),
        ]

    def netto_row_style(idx):
        return [
            ("BACKGROUND",   (0, idx), (-1, idx), NAVY),
            ("LINEABOVE",    (0, idx), (-1, idx), 1.5, GOLD),
        ]

    # ════════════════════════════════════════
    # COSTRUZIONE DEL DOCUMENTO
    # ════════════════════════════════════════
    story = []

    # ── HEADER BANNER ──
    oggi_str = datetime.date.today().strftime("%d/%m/%Y")
    periodo  = f"{MESI_IT[inp.mese]} {inp.anno}"
    header_data = [[
        Paragraph("Gaetani &amp; Partners Consulting", S["firm_name"]),
        Paragraph(
            f"Riepilogo Gestione Mensile – {periodo}<br/>"
            f"<font size='7' color='#AABBCC'>Elaborato il {oggi_str} | "
            f"Circ. INPS n. 9/2026 · CCNL Lavoro Domestico</font>",
            S["header_r"],
        ),
    ]]
    header_tbl = Table(header_data, colWidths=[COL_W * 0.58, COL_W * 0.42])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), NAVY),
        ("LINEBELOW",   (0, 0), (-1, 0), 2.5, GOLD),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 4 * mm))

    # ── DATI LAVORATORE / DATORE ──
    conv_str = "Sì" if inp.convivente else "No"
    desc_liv  = t["descrizione_livelli"].get(inp.livello_ccnl, inp.livello_ccnl)
    info_data = [
        [
            Paragraph("LAVORATORE", S["info_lbl"]),
            Paragraph(nome_lavoratore or "—", S["info_val"]),
            Paragraph("DATORE DI LAVORO", S["info_lbl"]),
            Paragraph(nome_datore or "—", S["info_val"]),
        ],
        [
            Paragraph("LIVELLO CCNL", S["info_lbl"]),
            Paragraph(desc_liv, S["info_val"]),
            Paragraph("TIPO CONTRATTO", S["info_lbl"]),
            Paragraph(
                f"{'Tempo Indeterminato' if inp.tipo_contratto=='TI' else 'Tempo Determinato'}"
                f" | Convivente: {conv_str}",
                S["info_val"],
            ),
        ],
        [
            Paragraph("PERIODO DI RIFERIMENTO", S["info_lbl"]),
            Paragraph(periodo, S["info_val"]),
            Paragraph("ORE LAVORATE / SETTIMANALI", S["info_lbl"]),
            Paragraph(f"{inp.ore_mese:.1f}h mensili · {inp.ore_settimanali:.1f}h/sett", S["info_val"]),
        ],
    ]
    cw4 = COL_W / 4
    info_tbl = Table(info_data, colWidths=[cw4 * 0.85, cw4 * 1.15, cw4 * 0.85, cw4 * 1.15])
    info_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), CREAM),
        ("BACKGROUND",   (0, 0), (0, -1), colors.HexColor("#EEE9DA")),
        ("BACKGROUND",   (2, 0), (2, -1), colors.HexColor("#EEE9DA")),
        ("GRID",         (0, 0), (-1, -1), 0.3, BORDER),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LINEABOVE",    (0, 0), (-1, 0), 0.6, GOLD),
        ("LINEBELOW",    (0, -1), (-1, -1), 0.6, GOLD),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 4 * mm))

    # ── KPI ORARI (3 box navy) ──
    kpi_data = [[
        [
            Paragraph("PAGA ORARIA LORDA", S["kpi_label"]),
            Paragraph(euro(res.paga_oraria_lorda), S["kpi_value"]),
            Paragraph(f"Livello {inp.livello_ccnl}", S["kpi_sub"]),
        ],
        [
            Paragraph("PAGA ORARIA NETTA", S["kpi_label"]),
            Paragraph(euro(res.paga_oraria_netta), S["kpi_value"]),
            Paragraph("Dopo contributi lavoratore", S["kpi_sub"]),
        ],
        [
            Paragraph("FASCIA INPS", S["kpi_label"]),
            Paragraph(res.fascia.codice, S["kpi_value"]),
            Paragraph(f"{res.fascia.inps_tot_h:.2f}€ tot · {res.fascia.inps_lav_h:.2f}€ lav./h", S["kpi_sub"]),
        ],
        [
            Paragraph("NETTO IN BUSTA", S["kpi_label"]),
            Paragraph(euro(res.netto), S["kpi_value"]),
            Paragraph("Percepito dal lavoratore", S["kpi_sub"]),
        ],
        [
            Paragraph("COSTO MENSILE DATORE", S["kpi_label"]),
            Paragraph(euro(res.costo_datore), S["kpi_value"]),
            Paragraph("Lordo + oneri datore", S["kpi_sub"]),
        ],
    ]]
    # Ogni cella è una sotto-tabella
    kpi_cells = []
    for cell_content in kpi_data[0]:
        inner = Table([[p] for p in cell_content],
                      colWidths=[COL_W / 5 - 3 * mm])
        inner.setStyle(TableStyle([
            ("BACKGROUND",  (0, 0), (-1, -1), NAVY_MID),
            ("LEFTPADDING",  (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING",   (0, 0), (-1, 0), 6),
            ("BOTTOMPADDING",(0, -1), (-1, -1), 6),
            ("TOPPADDING",   (0, 1), (-1, 1), 2),
            ("BOTTOMPADDING",(0, 1), (-1, 1), 2),
            ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ]))
        kpi_cells.append(inner)

    kpi_tbl = Table([kpi_cells], colWidths=[COL_W / 5] * 5, spaceBefore=0)
    kpi_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), NAVY),
        ("LINEBELOW",    (0, 0), (-1, -1), 2, GOLD),
        ("LEFTPADDING",  (0, 0), (-1, -1), 1.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1.5),
        ("TOPPADDING",   (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 1.5),
    ]))
    story.append(kpi_tbl)
    story.append(Spacer(1, 4 * mm))

    # ── WARNINGS ──
    for w in res.warnings:
        story.append(Paragraph(f"⚠ {w}", S["warn"]))
        story.append(Spacer(1, 1.5 * mm))

    # ── CEDOLINO: COMPETENZE + TRATTENUTE (due colonne) ──
    magg_pct = inp.maggiorazione_straord_pct

    def build_cedolino_half(rows_def: list) -> Table:
        """Costruisce mezza tabella cedolino dato un elenco di righe (tipo, label, valore)."""
        data = []
        style_cmds_list = [
            ("BACKGROUND",  (0, 0), (-1, -1), WHITE),
            ("GRID",        (0, 0), (-1, -1), 0.3, BORDER),
            ("LEFTPADDING",  (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING",   (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 3.5),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ]
        for i, (rtype, label, value) in enumerate(rows_def):
            if rtype == "section":
                data.append([Paragraph(label, S["section"]), ""])
                style_cmds_list += [
                    ("BACKGROUND",  (0, i), (-1, i), SECT_BG),
                    ("SPAN",        (0, i), (-1, i)),
                    ("TOPPADDING",  (0, i), (-1, i), 2.5),
                    ("BOTTOMPADDING",(0, i), (-1, i), 2.5),
                ]
            elif rtype == "total":
                data.append([Paragraph(label, S["total_l"]), Paragraph(value, S["total_v"])])
                style_cmds_list += [
                    ("BACKGROUND",   (0, i), (-1, i), TOTAL_BG),
                    ("LINEABOVE",    (0, i), (-1, i), 1.2, GOLD),
                    ("FONTNAME",     (0, i), (-1, i), "Helvetica-Bold"),
                ]
            elif rtype == "netto":
                data.append([Paragraph(label, S["netto_l"]), Paragraph(value, S["netto_v"])])
                style_cmds_list += [
                    ("BACKGROUND",   (0, i), (-1, i), NAVY),
                    ("LINEABOVE",    (0, i), (-1, i), 1.5, GOLD),
                ]
            else:  # normal / indent
                lbl_s = S["label_ind"] if rtype == "indent" else S["label"]
                data.append([Paragraph(label, lbl_s), Paragraph(value, S["value"])])
        half_w = (COL_W - 3 * mm) / 2
        tbl = Table(data, colWidths=[half_w * 0.62, half_w * 0.38])
        tbl.setStyle(TableStyle(style_cmds_list))
        return tbl

    # Definizione righe competenze
    comp_rows = [("section", "COMPETENZE LORDE", "")]
    comp_rows.append(("indent", "Paga base", euro(res.lordo_base)))
    if res.lordo_festivita:
        comp_rows.append(("indent", "Festività retribuite", euro(res.lordo_festivita)))
    if res.lordo_straordinario:
        comp_rows.append(("indent", f"Straordinario (+{magg_pct:.0f}%)", euro(res.lordo_straordinario)))
    if res.lordo_ferie:
        comp_rows.append(("indent", "Ferie retribuite", euro(res.lordo_ferie)))
    if res.lordo_indennita:
        comp_rows.append(("indent", "Indennità / altre competenze", euro(res.lordo_indennita)))
    comp_rows.append(("total", "TOTALE LORDO", euro(res.lordo_totale)))

    # Definizione righe trattenute
    tratt_rows = [("section", "TRATTENUTE A CARICO LAVORATORE", "")]
    tratt_rows.append(("indent", "INPS – quota lavoratore", euro(res.inps_lav)))
    tratt_rows.append(("indent", "CAS.SA.COLF – quota lavoratore", euro(res.cassa_lav)))
    if res.trattenute_varie:
        tratt_rows.append(("indent", "Trattenute varie", euro(res.trattenute_varie)))
    tratt_rows.append(("total",  "TOTALE TRATTENUTE", euro(res.trattenute_tot)))
    tratt_rows.append(("netto",  "NETTO IN BUSTA PAGA", euro(res.netto)))

    # Pareggia lunghezze con righe vuote se necessario
    while len(comp_rows) < len(tratt_rows):
        comp_rows.insert(-1, ("normal", "", ""))
    while len(tratt_rows) < len(comp_rows):
        tratt_rows.insert(-1, ("normal", "", ""))

    tbl_comp  = build_cedolino_half(comp_rows)
    tbl_tratt = build_cedolino_half(tratt_rows)

    ced_outer = Table([[tbl_comp, tbl_tratt]], colWidths=[(COL_W - 3 * mm) / 2] * 2,
                      hAlign="LEFT")
    ced_outer.setStyle(TableStyle([
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("INNERGRID",    (0, 0), (-1, -1), 0, WHITE),
        ("COLPADDING",   (0, 0), (0, -1), 0),
    ]))
    story.append(ced_outer)
    story.append(Spacer(1, 4 * mm))

    # ── COSTI DATORE + ACCANTONAMENTI ──
    costo_reale = res.costo_datore + res.rateo_13a + res.tfr
    dat_rows = [
        ("section", "ONERI DATORE DI LAVORO", ""),
        ("indent",  "Retribuzione lorda erogata",   euro(res.lordo_totale)),
        ("indent",  "INPS – quota datore",           euro(res.inps_datore)),
        ("indent",  "CAS.SA.COLF – quota datore",    euro(res.cassa_datore)),
        ("total",   "COSTO MENSILE DATORE",           euro(res.costo_datore)),
    ]
    acc_rows = [
        ("section", "ACCANTONAMENTI (PRO QUOTA MENSILE)", ""),
        ("indent",  "Rateo 13a mensilita (lordo / 12)", euro(res.rateo_13a)),
        ("indent",  "TFR (lordo / 13,5)",               euro(res.tfr)),
        ("total",   "COSTO REALE MENSILE (c/13a+TFR)",  euro(costo_reale)),
    ]

    tbl_dat = build_cedolino_half(dat_rows)
    tbl_acc = build_cedolino_half(acc_rows)

    dat_outer = Table([[tbl_dat, tbl_acc]], colWidths=[(COL_W - 3 * mm) / 2] * 2)
    dat_outer.setStyle(TableStyle([
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(dat_outer)
    story.append(Spacer(1, 4 * mm))

    # ── VERSAMENTO TRIMESTRALE ──
    vers_data = [
        [Paragraph("VERSAMENTO CONTRIBUTI – STIMA TRIMESTRALE", S["section"]), "", ""],
        [Paragraph("Ore contributive (stima trim.)", S["label_ind"]),
         Paragraph(f"{res.ore_contributive * 3:.1f}h", S["value"]), ""],
        [Paragraph("INPS – totale trimestre",         S["label_ind"]),
         Paragraph(euro(res.vers_inps_trim),           S["value"]), ""],
        [Paragraph("CAS.SA.COLF – totale trimestre",  S["label_ind"]),
         Paragraph(euro(res.vers_cassa_trim),          S["value"]), ""],
        [Paragraph("TOTALE DA VERSARE",               S["total_l"]),
         Paragraph(euro(res.vers_tot_trim),            S["total_v"]), ""],
    ]
    scad_txt = "  ·  ".join(t["scadenze_versamento"])
    vers_data.append([
        Paragraph(f"Scadenze 2026: {scad_txt}", S["note"]), "", ""
    ])

    vers_style_list = [
        ("BACKGROUND",  (0, 0), (-1, -1), WHITE),
        ("GRID",        (0, 0), (-1, -1), 0.3, BORDER),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3.5),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        # section row 0
        ("BACKGROUND",  (0, 0), (-1, 0), SECT_BG),
        ("SPAN",        (0, 0), (-1, 0)),
        ("TOPPADDING",  (0, 0), (-1, 0), 2.5),
        ("BOTTOMPADDING",(0, 0), (-1, 0), 2.5),
        # total row 4
        ("BACKGROUND",   (0, 4), (-1, 4), TOTAL_BG),
        ("LINEABOVE",    (0, 4), (-1, 4), 1.2, GOLD),
        ("FONTNAME",     (0, 4), (-1, 4), "Helvetica-Bold"),
        # span rows
        ("SPAN",        (0, 0), (-1, 0)),
        ("SPAN",        (0, 5), (-1, 5)),
        ("BACKGROUND",  (0, 5), (-1, 5), CREAM),
        ("TOPPADDING",  (0, 5), (-1, 5), 3),
        ("BOTTOMPADDING",(0, 5), (-1, 5), 3),
    ]
    vers_tbl = Table(vers_data, colWidths=[COL_W * 0.5, COL_W * 0.25, COL_W * 0.25])
    vers_tbl.setStyle(TableStyle(vers_style_list))
    story.append(vers_tbl)
    story.append(Spacer(1, 5 * mm))

    # ── NOTA LEGALE + FIRMA ──
    story.append(HRFlowable(width=COL_W, thickness=0.5, color=BORDER))
    story.append(Spacer(1, 3 * mm))

    nota_data = [[
        Paragraph(
            "Nota: il datore di lavoro domestico <b>non è sostituto d'imposta</b>. "
            "L'IRPEF non è trattenuta nel cedolino e viene versata autonomamente dal lavoratore "
            "in sede di dichiarazione dei redditi.<br/>"
            "Calcoli effettuati ai sensi della Circ. INPS n. 9 del 03/02/2026 e del CCNL Lavoro Domestico vigente. "
            "Il presente cedolino ha valore indicativo e non sostituisce la consulenza professionale.",
            S["note"],
        ),
        Paragraph(
            "Firma datore di lavoro<br/><br/><br/>"
            "_______________________________<br/>"
            f"{nome_datore or ''}",
            sty("firma", fontName="Helvetica", fontSize=7.5, textColor=MID_TXT,
                alignment=TA_CENTER, leading=11),
        ),
    ]]
    nota_tbl = Table(nota_data, colWidths=[COL_W * 0.7, COL_W * 0.3])
    nota_tbl.setStyle(TableStyle([
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",(0, 0), (-1, -1), 0),
        ("TOPPADDING",  (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0,0), (-1, -1), 0),
        ("LINEABOVE",   (1, 0), (1, 0), 0.5, BORDER),
    ]))
    story.append(nota_tbl)
    story.append(Spacer(1, 4 * mm))

    # ── FOOTER ──
    story.append(HRFlowable(width=COL_W, thickness=0.5, color=GOLD))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        f"© {datetime.date.today().year} Gaetani &amp; Partners Consulting · "
        "Consulenza Tributaria &amp; Pianificazione Fiscale · Uso riservato",
        S["footer"],
    ))

    # ── Build ──
    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────────
# GENERAZIONE PDF – CEDOLINO PAGA (PER IL LAVORATORE)
# Contiene solo i dati da comunicare al lavoratore:
# contratto, competenze lorde, trattenute, netto da pagare
# ─────────────────────────────────────────────
def genera_pdf_cedolino_lavoratore(
    inp: PayrollInputs,
    res: PayrollResults,
    nome_lavoratore: str,
    nome_datore: str,
    t: dict,
) -> bytes:
    """Genera il cedolino paga per il lavoratore domestico."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
    )
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

    # ── Palette (identica all'app) ──
    NAVY      = colors.HexColor("#0D1F3C")
    NAVY_MID  = colors.HexColor("#16325A")
    GOLD      = colors.HexColor("#C9A84C")
    GOLD_LITE = colors.HexColor("#E8C96A")
    CREAM     = colors.HexColor("#FAF8F2")
    BORDER    = colors.HexColor("#D6CCB4")
    SECT_BG   = colors.HexColor("#F7F4EC")
    TOTAL_BG  = colors.HexColor("#F2EED8")
    WHITE     = colors.white
    DARK_TXT  = colors.HexColor("#1A1A2E")
    MID_TXT   = colors.HexColor("#4A4A6A")
    LITE_TXT  = colors.HexColor("#7A7A9A")
    GREEN_BG  = colors.HexColor("#E8F4E8")
    GREEN_TXT = colors.HexColor("#1B5E20")

    buf = io.BytesIO()
    PAGE_W, PAGE_H = A4
    MARGIN = 20 * mm
    COL_W  = PAGE_W - 2 * MARGIN

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=14 * mm, bottomMargin=18 * mm,
        title=f"Cedolino Paga {MESI_IT[inp.mese]} {inp.anno}",
        author="Gaetani & Partners Consulting",
        subject="Cedolino paga lavoratore domestico",
    )

    def sty(name, **kw):
        return ParagraphStyle(name, **kw)

    S = {
        "firm":    sty("firm",    fontName="Helvetica-Bold", fontSize=14, textColor=WHITE,
                       alignment=TA_LEFT, leading=17),
        "hdr_r":   sty("hdr_r",   fontName="Helvetica",      fontSize=7.5,
                       textColor=GOLD_LITE, alignment=TA_RIGHT, leading=11),
        "title":   sty("title",   fontName="Helvetica-Bold", fontSize=13, textColor=NAVY,
                       alignment=TA_CENTER, leading=16, spaceBefore=4, spaceAfter=4),
        "sub":     sty("sub",     fontName="Helvetica",      fontSize=8.5, textColor=MID_TXT,
                       alignment=TA_CENTER, leading=12, spaceAfter=2),
        "sect":    sty("sect",    fontName="Helvetica-Bold", fontSize=8, textColor=NAVY,
                       leading=10),
        "lbl":     sty("lbl",     fontName="Helvetica",      fontSize=9, textColor=DARK_TXT,
                       leading=11),
        "lbl_i":   sty("lbl_i",   fontName="Helvetica",      fontSize=9, textColor=MID_TXT,
                       leading=11, leftIndent=10),
        "val":     sty("val",     fontName="Helvetica",      fontSize=9, textColor=DARK_TXT,
                       alignment=TA_RIGHT, leading=11),
        "tot_l":   sty("tot_l",   fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY,
                       leading=12),
        "tot_v":   sty("tot_v",   fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY,
                       alignment=TA_RIGHT, leading=12),
        "net_l":   sty("net_l",   fontName="Helvetica-Bold", fontSize=14, textColor=GOLD_LITE,
                       leading=17),
        "net_v":   sty("net_v",   fontName="Helvetica-Bold", fontSize=14, textColor=GOLD_LITE,
                       alignment=TA_RIGHT, leading=17),
        "il":      sty("il",      fontName="Helvetica-Bold", fontSize=7.5, textColor=MID_TXT,
                       leading=10),
        "iv":      sty("iv",      fontName="Helvetica",      fontSize=7.5, textColor=DARK_TXT,
                       leading=10),
        "note":    sty("note",    fontName="Helvetica-Oblique", fontSize=7, textColor=LITE_TXT,
                       leading=9),
        "footer":  sty("footer",  fontName="Helvetica",      fontSize=6.5, textColor=LITE_TXT,
                       alignment=TA_CENTER, leading=9),
        "firma_l": sty("firma_l", fontName="Helvetica",      fontSize=8, textColor=MID_TXT,
                       alignment=TA_CENTER, leading=11),
        "firma_r": sty("firma_r", fontName="Helvetica",      fontSize=8, textColor=MID_TXT,
                       alignment=TA_CENTER, leading=11),
    }

    story = []
    oggi_str = datetime.date.today().strftime("%d/%m/%Y")
    periodo  = f"{MESI_IT[inp.mese]} {inp.anno}"
    tipo_str = "Tempo Indeterminato" if inp.tipo_contratto == "TI" else "Tempo Determinato"
    conv_str = "Convivente" if inp.convivente else "Non convivente"
    desc_liv = t["descrizione_livelli"].get(inp.livello_ccnl, inp.livello_ccnl)

    # ── HEADER ──
    hdr = Table([[
        Paragraph("Gaetani &amp; Partners Consulting", S["firm"]),
        Paragraph(
            f"Cedolino Paga – {periodo}<br/>"
            f"<font size='6.5' color='#AABBCC'>Emesso il {oggi_str}</font>",
            S["hdr_r"],
        ),
    ]], colWidths=[COL_W * 0.58, COL_W * 0.42])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), NAVY),
        ("LINEBELOW",    (0, 0), (-1, 0), 2.5, GOLD),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 5 * mm))

    # ── TITOLO CENTRALE ──
    story.append(Paragraph("CEDOLINO PAGA", S["title"]))
    story.append(Paragraph(f"Periodo: <b>{periodo}</b>", S["sub"]))
    story.append(Spacer(1, 4 * mm))

    # ── DATI LAVORATORE / DATORE ──
    cw = COL_W / 4
    info_data = [
        [Paragraph("LAVORATORE",     S["il"]), Paragraph(nome_lavoratore or "—", S["iv"]),
         Paragraph("DATORE DI LAVORO", S["il"]), Paragraph(nome_datore or "—", S["iv"])],
        [Paragraph("LIVELLO CCNL",   S["il"]), Paragraph(desc_liv, S["iv"]),
         Paragraph("TIPO CONTRATTO", S["il"]),
         Paragraph(f"{tipo_str} · {conv_str}", S["iv"])],
        [Paragraph("ORE NEL MESE",   S["il"]),
         Paragraph(f"{inp.ore_mese:.1f}h  ({inp.ore_settimanali:.1f}h/sett)", S["iv"]),
         Paragraph("PERIODO DI PAY", S["il"]), Paragraph(periodo, S["iv"])],
    ]
    info_tbl = Table(info_data, colWidths=[cw * 0.82, cw * 1.18, cw * 0.82, cw * 1.18])
    info_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), CREAM),
        ("BACKGROUND",   (0, 0), (0, -1), colors.HexColor("#EEE9DA")),
        ("BACKGROUND",   (2, 0), (2, -1), colors.HexColor("#EEE9DA")),
        ("GRID",         (0, 0), (-1, -1), 0.3, BORDER),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LINEABOVE",    (0, 0), (-1, 0), 0.8, GOLD),
        ("LINEBELOW",    (0, -1), (-1, -1), 0.8, GOLD),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 5 * mm))

    # ── CEDOLINO: COMPETENZE ──
    magg_pct = inp.maggiorazione_straord_pct
    comp_rows  = [("sect",  "COMPETENZE LORDE", "")]
    comp_rows += [("ind",   "Paga base", euro(res.lordo_base))]
    if res.lordo_festivita:
        comp_rows += [("ind", "Festività retribuite", euro(res.lordo_festivita))]
    if res.lordo_straordinario:
        comp_rows += [("ind", f"Straordinario (+{magg_pct:.0f}%)", euro(res.lordo_straordinario))]
    if res.lordo_ferie:
        comp_rows += [("ind", "Ferie retribuite", euro(res.lordo_ferie))]
    if res.lordo_indennita:
        comp_rows += [("ind", "Indennità / altre competenze", euro(res.lordo_indennita))]
    comp_rows += [("tot",  "TOTALE LORDO", euro(res.lordo_totale))]

    # ── CEDOLINO: TRATTENUTE ──
    tratt_rows  = [("sect", "TRATTENUTE A CARICO DEL LAVORATORE", "")]
    tratt_rows += [("ind",  "Contributi INPS (quota lavoratore)", euro(res.inps_lav))]
    tratt_rows += [("ind",  "CAS.SA.COLF (quota lavoratore)", euro(res.cassa_lav))]
    if res.trattenute_varie:
        tratt_rows += [("ind", "Altre trattenute", euro(res.trattenute_varie))]
    tratt_rows += [("tot",  "TOTALE TRATTENUTE", euro(res.trattenute_tot))]

    all_rows = comp_rows + [("spacer", "", "")] + tratt_rows

    data_ced = []
    style_ced = [
        ("BACKGROUND",   (0, 0), (-1, -1), WHITE),
        ("GRID",         (0, 0), (-1, -1), 0.3, BORDER),
        ("LEFTPADDING",  (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING",   (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 3.5),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]

    for i, (rtype, label, value) in enumerate(all_rows):
        if rtype == "sect":
            data_ced.append([Paragraph(label, S["sect"]), ""])
            style_ced += [
                ("BACKGROUND",   (0, i), (-1, i), SECT_BG),
                ("SPAN",         (0, i), (-1, i)),
                ("TOPPADDING",   (0, i), (-1, i), 3),
                ("BOTTOMPADDING",(0, i), (-1, i), 3),
            ]
        elif rtype == "tot":
            data_ced.append([Paragraph(label, S["tot_l"]), Paragraph(value, S["tot_v"])])
            style_ced += [
                ("BACKGROUND",  (0, i), (-1, i), TOTAL_BG),
                ("LINEABOVE",   (0, i), (-1, i), 1.2, GOLD),
            ]
        elif rtype == "spacer":
            data_ced.append(["", ""])
            style_ced += [
                ("BACKGROUND",   (0, i), (-1, i), WHITE),
                ("TOPPADDING",   (0, i), (-1, i), 2),
                ("BOTTOMPADDING",(0, i), (-1, i), 2),
                ("GRID",         (0, i), (-1, i), 0, WHITE),
            ]
        else:  # ind / normal
            lbl_s = S["lbl_i"] if rtype == "ind" else S["lbl"]
            data_ced.append([Paragraph(label, lbl_s), Paragraph(value, S["val"])])

    ced_tbl = Table(data_ced, colWidths=[COL_W * 0.65, COL_W * 0.35])
    ced_tbl.setStyle(TableStyle(style_ced))
    story.append(ced_tbl)
    story.append(Spacer(1, 5 * mm))

    # ── NETTO DA PAGARE – box prominente ──
    netto_data = [[
        Paragraph("NETTO DA PAGARE AL LAVORATORE", S["net_l"]),
        Paragraph(euro(res.netto), S["net_v"]),
    ]]
    netto_tbl = Table(netto_data, colWidths=[COL_W * 0.6, COL_W * 0.4])
    netto_tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), NAVY),
        ("LINEABOVE",    (0, 0), (-1, 0), 2.5, GOLD),
        ("LINEBELOW",    (0, 0), (-1, 0), 2.5, GOLD),
        ("LEFTPADDING",  (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING",   (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(netto_tbl)
    story.append(Spacer(1, 7 * mm))

    # ── FIRME ──
    story.append(HRFlowable(width=COL_W, thickness=0.4, color=BORDER))
    story.append(Spacer(1, 4 * mm))

    firme_data = [[
        Paragraph(
            "Firma del datore di lavoro per ricevuta<br/><br/><br/><br/>"
            "_______________________________<br/>"
            f"<font size='7'>{nome_datore or ''}</font>",
            S["firma_l"],
        ),
        Paragraph(
            "Firma del lavoratore per ricevuta<br/><br/><br/><br/>"
            "_______________________________<br/>"
            f"<font size='7'>{nome_lavoratore or ''}</font>",
            S["firma_r"],
        ),
    ]]
    firme_tbl = Table(firme_data, colWidths=[COL_W / 2, COL_W / 2])
    firme_tbl.setStyle(TableStyle([
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING",   (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 0),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(firme_tbl)
    story.append(Spacer(1, 5 * mm))

    # ── NOTA ──
    story.append(HRFlowable(width=COL_W, thickness=0.4, color=BORDER))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "Il datore di lavoro domestico non è sostituto d'imposta: l'IRPEF non è trattenuta "
        "in busta e viene versata autonomamente dal lavoratore. "
        "Contratto applicato: CCNL Lavoro Domestico. "
        f"Fascia contributiva INPS: {res.fascia.codice} – {res.fascia.label}.",
        S["note"],
    ))
    story.append(Spacer(1, 3 * mm))

    # ── FOOTER ──
    story.append(HRFlowable(width=COL_W, thickness=0.5, color=GOLD))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        f"© {datetime.date.today().year} Gaetani &amp; Partners Consulting · "
        "Consulenza Tributaria &amp; Pianificazione Fiscale",
        S["footer"],
    ))

    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────────
# PASSWORD GATE
# ─────────────────────────────────────────────
def get_password() -> str:
    try:
        return st.secrets["auth"]["password"]
    except Exception:
        # ⚠ Cambia qui la password se non usi Streamlit Community Cloud Secrets
        return "GaetaniPartners2026!"

def password_gate() -> bool:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.authenticated:
        return True

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    # Banda header anche nella login
    st.markdown(
        "<div style='background:linear-gradient(135deg,#0D1F3C,#1E4280);"
        "padding:1.2rem 2rem;margin:-1rem -1rem 0;border-bottom:3px solid #C9A84C;'></div>",
        unsafe_allow_html=True
    )

    _, col_c, _ = st.columns([1, 1.3, 1])
    with col_c:
        st.markdown("""
        <div class="login-wrap">
          <div class="login-logo">
            <h2>Gaetani &amp; Partners</h2>
            <p>Consulting</p>
            <div class="login-divider"></div>
          </div>
          <p style="text-align:center;color:#4A4A6A;font-size:0.86rem;margin-bottom:1.5rem;">
            Gestione Lavoro Domestico 2026<br>
            <small style="color:#9A9AB0;">Area riservata – clienti e collaboratori dello Studio</small>
          </p>
        </div>""", unsafe_allow_html=True)

        with st.form("login_form"):
            pwd = st.text_input("Password", type="password", placeholder="Password di accesso")
            ok = st.form_submit_button("Accedi →", use_container_width=True)
        if ok:
            if pwd == get_password():
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.markdown("<div class='gp-error'>🔒 Credenziali non valide. Contattare lo Studio.</div>",
                            unsafe_allow_html=True)

    st.markdown(
        "<div class='gp-footer'>© 2026 <strong>Gaetani &amp; Partners Consulting</strong> – "
        "Uso riservato · Tutti i diritti riservati</div>",
        unsafe_allow_html=True
    )
    return False

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    if not password_gate():
        return

    t = TABLES_2026
    oggi = datetime.date.today()

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="gp-header">
      <div class="gp-header-left">
        <h1>Gaetani &amp; Partners Consulting</h1>
        <p>Cedolino Lavoro Domestico – Sistema di calcolo 2026</p>
      </div>
      <div class="gp-header-right">
        <strong>Circ. INPS n. 9 del 03/02/2026</strong><br>
        CCNL Lavoro Domestico in vigore<br>
        Elaborazione: {oggi.strftime("%d/%m/%Y")}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # SEZ 1 – DATI CONTRATTO
    # ══════════════════════════════════════════════
    st.markdown("<div class='gp-section'>", unsafe_allow_html=True)
    st.markdown("<div class='gp-section-title'>1 · Dati del rapporto di lavoro</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1, 1, 1.2, 1])
    with c1:
        mese = st.selectbox("Mese di riferimento", list(MESI_IT.keys()),
                            format_func=lambda m: MESI_IT[m], index=oggi.month - 1)
        anno = st.number_input("Anno", min_value=2020, max_value=2100, value=oggi.year, step=1)
    with c2:
        tipo_raw = st.selectbox("Tipo contratto",
                                ["TD – Tempo Determinato", "TI – Tempo Indeterminato"])
        tipo_code = "TD" if tipo_raw.startswith("TD") else "TI"
        convivente = st.checkbox("Lavoratore convivente", value=False)
    with c3:
        livello_sel = st.selectbox("Livello CCNL", list(t["descrizione_livelli"].keys()),
                                   format_func=lambda k: t["descrizione_livelli"][k], index=2)
        ore_sett = st.number_input("Ore settimanali contrattualizzate",
                                   min_value=0.0, max_value=54.0, value=8.0, step=0.5,
                                   help="Se > 24h/sett si applica la Fascia 4 INPS (flat)")
    with c4:
        ore_mese = st.number_input("Ore lavorate nel mese", min_value=0.0, value=32.0, step=1.0)
        n_fest = st.number_input("Festività retribuite nel mese", min_value=0, max_value=6, value=0, step=1)
        inc_fest_contr = st.checkbox("Festività nelle ore contributive", value=True)

    if ore_sett > 24:
        st.markdown(
            f"<div class='gp-info'>ℹ️ Con <strong>{ore_sett:.1f}h/sett</strong> si applica la "
            "<strong>Fascia 4 INPS</strong> – contributo flat indipendente dalla retribuzione.</div>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # SEZ 2 – PAGA ORARIA
    # ══════════════════════════════════════════════
    st.markdown("<div class='gp-section'>", unsafe_allow_html=True)
    st.markdown("<div class='gp-section-title'>2 · Paga oraria</div>", unsafe_allow_html=True)

    min_h = t["minimi_orari"].get(livello_sel, 0.0)
    min_m = t["minimi_mensili_conviventi"].get(livello_sel, 0.0)
    if convivente:
        st.markdown(
            f"<div class='gp-info'>Minimo CCNL Livello <strong>{livello_sel}</strong> per conviventi: "
            f"<strong>{euro(min_m)}/mese</strong></div>", unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='gp-info'>Minimo CCNL Livello <strong>{livello_sel}</strong>: "
            f"<strong>{euro(min_h)}/h</strong></div>", unsafe_allow_html=True
        )

    mode = st.radio("Modalità", ["Inserisci paga oraria LORDA",
                                 "Calcola paga lorda da NETTA desiderata"], horizontal=True)
    cp1, cp2 = st.columns([1, 1])
    with cp1:
        if mode.startswith("Inserisci"):
            paga_lorda = st.number_input("Paga oraria lorda (€)", min_value=0.0,
                                         value=float(max(min_h, 7.01)), step=0.01, format="%.2f")
            paga_net_target = None
        else:
            paga_net_target = st.number_input("Paga oraria NETTA desiderata (€)",
                                              min_value=0.0, value=6.55, step=0.01, format="%.2f")
            paga_lorda = None
    with cp2:
        st.markdown("""
        <div class="gp-info" style="margin-top:1.8rem;">
        <strong>Nota IRPEF:</strong> il datore di lavoro domestico <em>non è sostituto d'imposta</em>.
        L'IRPEF non compare nel cedolino: il lavoratore la versa autonomamente in dichiarazione dei redditi.
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # SEZ 3 – VOCI VARIABILI
    # ══════════════════════════════════════════════
    st.markdown("<div class='gp-section'>", unsafe_allow_html=True)
    st.markdown("<div class='gp-section-title'>3 · Voci variabili del mese</div>", unsafe_allow_html=True)

    v1, v2, v3 = st.columns(3)
    with v1:
        ore_straord = st.number_input("Ore di straordinario", min_value=0.0, value=0.0, step=0.5)
        magg = st.number_input("Maggiorazione straordinario (%)", min_value=0.0, value=25.0, step=5.0)
    with v2:
        ore_ferie = st.number_input("Ore ferie godute retribuite", min_value=0.0, value=0.0, step=0.5)
        indennita = st.number_input("Indennità / altre competenze (€)", min_value=0.0, value=0.0,
                                    step=1.0, format="%.2f")
    with v3:
        trattenute_varie = st.number_input("Trattenute varie (€)", min_value=0.0, value=0.0,
                                           step=1.0, format="%.2f")

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # CALCOLO
    # ══════════════════════════════════════════════
    inp = PayrollInputs(
        mese=int(mese), anno=int(anno), tipo_contratto=tipo_code,
        convivente=convivente, livello_ccnl=livello_sel,
        ore_mese=float(ore_mese), ore_settimanali=float(ore_sett),
        paga_oraria_lorda=paga_lorda, paga_oraria_netto_target=paga_net_target,
        n_festivita=int(n_fest), include_festivita_contributi=bool(inc_fest_contr),
        ore_straordinario=float(ore_straord), maggiorazione_straord_pct=float(magg),
        ore_ferie=float(ore_ferie), indennita_euro=float(indennita),
        trattenute_varie_euro=float(trattenute_varie),
    )
    res = compute_payroll(inp, t)

    for w in res.warnings:
        st.markdown(f"<div class='gp-warn'>{w}</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # SEZ 4 – KPI ORARI
    # ══════════════════════════════════════════════
    st.markdown("<div class='gp-section'>", unsafe_allow_html=True)
    st.markdown("<div class='gp-section-title'>4 · Tariffe orarie e costi mensili</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="gp-metric-grid">
      <div class="gp-metric">
        <div class="gp-metric-label">Paga oraria lorda</div>
        <div class="gp-metric-value">{euro(res.paga_oraria_lorda)}</div>
        <div class="gp-metric-sub">Livello {livello_sel} · {tipo_code}</div>
      </div>
      <div class="gp-metric">
        <div class="gp-metric-label">Paga oraria netta</div>
        <div class="gp-metric-value">{euro(res.paga_oraria_netta)}</div>
        <div class="gp-metric-sub">Dopo contributi lavoratore</div>
      </div>
      <div class="gp-metric">
        <div class="gp-metric-label">Costo orario datore</div>
        <div class="gp-metric-value">{euro(res.costo_orario_datore)}</div>
        <div class="gp-metric-sub">Lordo + oneri datore</div>
      </div>
      <div class="gp-metric">
        <div class="gp-metric-label">Fascia INPS</div>
        <div class="gp-metric-value" style="font-size:1.2rem;">{res.fascia.codice}</div>
        <div class="gp-metric-sub">{res.fascia.inps_tot_h:.2f}€ tot · {res.fascia.inps_lav_h:.2f}€ lav. / h</div>
      </div>
      <div class="gp-metric highlight">
        <div class="gp-metric-label">Costo mensile datore</div>
        <div class="gp-metric-value">{euro(res.costo_datore)}</div>
        <div class="gp-metric-sub">Lordo + oneri datore / mese</div>
      </div>
      <div class="gp-metric highlight">
        <div class="gp-metric-label">Netto in busta paga</div>
        <div class="gp-metric-value">{euro(res.netto)}</div>
        <div class="gp-metric-sub">Percepito dal lavoratore</div>
      </div>
    </div>
    <div class="gp-info" style="margin-top:0.3rem; font-size:0.8rem;">
      📊 {fascia_badge_html(res.fascia)}
      &nbsp;|&nbsp; Retribuzione effettiva per fascia (paga × 13/12):
      <strong>{euro(res.fascia.retrib_eff_h)}/h</strong>
      &nbsp;|&nbsp; Ore contributive mese: <strong>{res.ore_contributive:.1f}h</strong>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # SEZ 5 – CEDOLINO
    # ══════════════════════════════════════════════
    st.markdown("<div class='gp-section'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='gp-section-title'>5 · Cedolino – {MESI_IT[inp.mese]} {inp.anno}</div>",
        unsafe_allow_html=True
    )

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        r = (_section("COMPETENZE LORDE")
             + _row("Paga base", euro(res.lordo_base), indent=True)
             + (_row("Festività retribuite", euro(res.lordo_festivita), indent=True) if res.lordo_festivita else "")
             + (_row(f"Straordinario (+{magg:.0f}%)", euro(res.lordo_straordinario), indent=True) if res.lordo_straordinario else "")
             + (_row("Ferie retribuite", euro(res.lordo_ferie), indent=True) if res.lordo_ferie else "")
             + (_row("Indennità / altre competenze", euro(res.lordo_indennita), indent=True) if res.lordo_indennita else "")
             + _total("TOTALE LORDO", euro(res.lordo_totale)))
        st.markdown(table_html(r), unsafe_allow_html=True)

    with col_c2:
        r = (_section("TRATTENUTE A CARICO LAVORATORE")
             + _row("INPS – quota lavoratore", euro(res.inps_lav), indent=True)
             + _row("CAS.SA.COLF – quota lavoratore", euro(res.cassa_lav), indent=True)
             + (_row("Trattenute varie", euro(res.trattenute_varie), indent=True) if res.trattenute_varie else "")
             + _total("TOTALE TRATTENUTE", euro(res.trattenute_tot))
             + _netto("NETTO IN BUSTA PAGA", euro(res.netto)))
        st.markdown(table_html(r), unsafe_allow_html=True)

    st.markdown("<hr class='gp-divider'>", unsafe_allow_html=True)
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        r = (_section("ONERI DATORE DI LAVORO")
             + _row("Retribuzione lorda erogata", euro(res.lordo_totale), indent=True)
             + _row("INPS – quota datore", euro(res.inps_datore), indent=True)
             + _row("CAS.SA.COLF – quota datore", euro(res.cassa_datore), indent=True)
             + _total("COSTO MENSILE DATORE", euro(res.costo_datore)))
        st.markdown(table_html(r), unsafe_allow_html=True)

    with col_d2:
        costo_reale = res.costo_datore + res.rateo_13a + res.tfr
        r = (_section("ACCANTONAMENTI (PRO QUOTA MENSILE)")
             + _row("Rateo 13ª mensilità (lordo ÷ 12)", euro(res.rateo_13a), indent=True)
             + _row("TFR (lordo ÷ 13,5)", euro(res.tfr), indent=True)
             + _total("COSTO REALE MENSILE (c/13ª+TFR)", euro(costo_reale)))
        st.markdown(table_html(r), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # SEZ 5b – GENERA PDF CEDOLINO
    # ══════════════════════════════════════════════
    st.markdown("<div class='gp-section'>", unsafe_allow_html=True)
    st.markdown("<div class='gp-section-title'>📄 Genera documenti PDF</div>",
                unsafe_allow_html=True)

    pdf_c1, pdf_c2 = st.columns([1, 1])
    with pdf_c1:
        nome_lav = st.text_input("Nome e cognome del lavoratore",
                                 placeholder="Es. Maria Rossi", key="pdf_nome_lav")
    with pdf_c2:
        nome_dat = st.text_input("Nome e cognome / Ragione sociale del datore",
                                 placeholder="Es. Mario Bianchi", key="pdf_nome_dat")

    st.markdown(
        "<div class='gp-info' style='font-size:0.8rem;'>ℹ️ I campi nome sono facoltativi ma consigliati "
        "per personalizzare i documenti. Il <strong>Riepilogo Gestione Mensile</strong> è ad uso interno "
        "dello Studio; il <strong>Cedolino Paga</strong> è il documento da consegnare al lavoratore.</div>",
        unsafe_allow_html=True,
    )

    btn_c1, btn_c2 = st.columns(2)

    with btn_c1:
        nome_file_riepilogo = (
            f"riepilogo_gestione_{MESI_IT[inp.mese].lower()}_{inp.anno}"
            f"{'_' + nome_lav.replace(' ','_').lower() if nome_lav else ''}.pdf"
        )
        pdf_riepilogo = genera_pdf_riepilogo(inp, res, nome_lav, nome_dat, t)
        st.download_button(
            label="⬇️  Riepilogo Gestione Mensile",
            data=pdf_riepilogo,
            file_name=nome_file_riepilogo,
            mime="application/pdf",
            use_container_width=True,
            type="secondary",
            help="Documento completo ad uso interno: tutti i costi, contributi, accantonamenti",
        )

    with btn_c2:
        nome_file_cedolino = (
            f"cedolino_paga_{MESI_IT[inp.mese].lower()}_{inp.anno}"
            f"{'_' + nome_lav.replace(' ','_').lower() if nome_lav else ''}.pdf"
        )
        pdf_cedolino = genera_pdf_cedolino_lavoratore(inp, res, nome_lav, nome_dat, t)
        st.download_button(
            label="⬇️  Cedolino Paga (per il lavoratore)",
            data=pdf_cedolino,
            file_name=nome_file_cedolino,
            mime="application/pdf",
            use_container_width=True,
            type="primary",
            help="Documento da consegnare al lavoratore: contratto, lordo, trattenute e netto",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # SEZ 6 – VERSAMENTO TRIMESTRALE
    # ══════════════════════════════════════════════
    st.markdown("<div class='gp-section'>", unsafe_allow_html=True)
    st.markdown("<div class='gp-section-title'>6 · Versamento contributi – stima trimestrale</div>",
                unsafe_allow_html=True)

    ct1, ct2 = st.columns([1.5, 1])
    with ct1:
        r = (_section(f"STIMA TRIMESTRALE (3 mesi × {ore_mese:.0f}h lavorate)")
             + _row("Ore contributive – stima trimestrale", f"{res.ore_contributive * 3:.1f}h", indent=True)
             + _row("INPS totale trimestre", euro(res.vers_inps_trim), indent=True)
             + _row("CAS.SA.COLF totale trimestre", euro(res.vers_cassa_trim), indent=True)
             + _total("TOTALE DA VERSARE", euro(res.vers_tot_trim)))
        st.markdown(table_html(r), unsafe_allow_html=True)

    with ct2:
        chips = "".join(f"<span class='scad-chip'>{s}</span>" for s in t["scadenze_versamento"])
        st.markdown(f"""
        <div style="padding:0.3rem 0;">
          <div style="font-weight:600;color:#0D1F3C;font-size:0.83rem;margin-bottom:0.5rem;">
            Scadenze versamento 2026
          </div>
          <div class="scad-grid">{chips}</div>
          <div class="gp-info" style="margin-top:0.7rem;font-size:0.77rem;">
            Dal 2026 il versamento è <strong>esclusivamente digitale</strong>:<br>
            PagoPA · Portale INPS (SPID/CIE/CNS) · App IO<br>
            <em>I bollettini cartacei non sono più accettati</em>
            (deroga temporanea per datori ≥ 76 anni).
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # SEZ 7 – AGEVOLAZIONI FISCALI
    # ══════════════════════════════════════════════
    st.markdown("<div class='gp-section'>", unsafe_allow_html=True)
    st.markdown("<div class='gp-section-title'>7 · Agevolazioni fiscali per il datore di lavoro</div>",
                unsafe_allow_html=True)

    ca1, ca2 = st.columns(2)
    inps_annuo = res.vers_inps_trim * 4
    deducibile = min(inps_annuo, t["deduzione_inps_max"])

    with ca1:
        st.markdown(f"""
        <div class="gp-metric" style="margin-bottom:0.8rem;">
          <div class="gp-metric-label">Deduzione contributi INPS – Art. 10 TUIR</div>
          <div class="gp-metric-value">{euro(deducibile)}</div>
          <div class="gp-metric-sub">Stima annua deducibile (max €{t['deduzione_inps_max']:,.2f}/anno)</div>
        </div>
        <div class="gp-info" style="font-size:0.79rem;">
          I contributi INPS versati per colf e badanti sono <strong>deducibili dal reddito complessivo</strong>
          fino a <strong>€ 1.549,37/anno</strong> (art. 10, co. 2, TUIR).
          La deduzione riduce direttamente la base imponibile IRPEF del datore.
        </div>""", unsafe_allow_html=True)

    with ca2:
        st.markdown(f"""
        <div class="gp-metric" style="margin-bottom:0.8rem;">
          <div class="gp-metric-label">Detrazione spese badante – Art. 15 TUIR</div>
          <div class="gp-metric-value">{euro(t['detrazione_assistenza_max'])}</div>
          <div class="gp-metric-sub">Detrazione IRPEF 19% – max annuo (reddito ≤ €40.000)</div>
        </div>
        <div class="gp-info" style="font-size:0.79rem;">
          Detrazione del <strong>19%</strong> per spese di assistenza a <strong>persone non autosufficienti</strong>,
          fino a <strong>€ 2.100/anno</strong>. Requisiti: reddito contribuente ≤ €40.000,
          documentazione non autosufficienza (verbale ASL/invalidità).
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # SEZ 8 – PARAMETRI (AVANZATO, sola lettura)
    # ══════════════════════════════════════════════
    with st.expander("⚙️  Tabelle normative 2026 – sola lettura (Circ. INPS n. 9/2026)"):
        st.markdown("<div class='gp-info'>Tabelle pre-caricate dalla Circolare INPS n. 9 del 03/02/2026. "
                    "Aggiornate automaticamente ad ogni nuova versione dell'applicativo. "
                    "Per eventuali variazioni in corso d'anno contattare lo Studio.</div>",
                    unsafe_allow_html=True)

        st.markdown("**Contributi INPS orari 2026**")
        cti, ctd = t["contributi"]["TI"], t["contributi"]["TD"]
        defs = [
            ("F1", f"≤ €{t['soglie_fasce']['fascia1_max']:.2f}/h retrib. eff."),
            ("F2", f"> €{t['soglie_fasce']['fascia1_max']:.2f} fino a €{t['soglie_fasce']['fascia2_max']:.2f}/h eff."),
            ("F3", f"> €{t['soglie_fasce']['fascia2_max']:.2f}/h eff."),
            ("F4", f"> {t['soglia_h_sett_fascia4']}h/sett – flat"),
        ]
        contr_rows = ""
        for cod, cond in defs:
            ti, td = cti[cod], ctd[cod]
            contr_rows += (
                f"<tr><td><strong>{cod}</strong></td><td>{cond}</td>"
                f"<td class='amt'>€ {ti['totale']:.2f}</td><td class='amt'>€ {ti['lav']:.2f}</td>"
                f"<td class='amt'>€ {ti['totale']-ti['lav']:.2f}</td>"
                f"<td class='amt'>€ {td['totale']:.2f}</td><td class='amt'>€ {td['lav']:.2f}</td>"
                f"<td class='amt'>€ {td['totale']-td['lav']:.2f}</td></tr>"
            )
        st.markdown(
            f"<table class='ced-table'>"
            f"<thead><tr><th>Fascia</th><th>Condizione</th>"
            f"<th>TI Totale</th><th>TI Lav.</th><th>TI Dat.</th>"
            f"<th>TD Totale</th><th>TD Lav.</th><th>TD Dat.</th></tr></thead>"
            f"<tbody>{contr_rows}</tbody>"
            f"<tfoot><tr><td colspan='8' style='padding:0.5rem 1rem;color:#666;font-size:0.74rem;'>"
            f"CAS.SA.COLF (tutti i rapporti): totale €0,06/h · lavoratore €0,02/h · datore €0,04/h"
            "</td></tr></tfoot></table>",
            unsafe_allow_html=True
        )

        st.markdown("**Minimi retributivi CCNL – non conviventi (€/ora)**")
        min_rows = "".join(
            f"<tr><td><strong>{k}</strong></td><td>{t['descrizione_livelli'][k]}</td>"
            f"<td class='amt'>{euro(v)}</td>"
            f"<td class='amt'>{euro(t['minimi_mensili_conviventi'][k])}/mese</td></tr>"
            for k, v in t["minimi_orari"].items()
        )
        st.markdown(
            f"<table class='ced-table'><thead><tr><th>Livello</th><th>Descrizione</th>"
            f"<th style='text-align:right'>Min. €/h</th><th style='text-align:right'>Convivente €/mese</th>"
            f"</tr></thead><tbody>{min_rows}</tbody></table>",
            unsafe_allow_html=True
        )

    # ══════════════════════════════════════════════
    # FOOTER
    # ══════════════════════════════════════════════
    st.markdown(f"""
    <div class="gp-footer">
      <strong>Gaetani &amp; Partners Consulting</strong> · Consulenza Tributaria &amp; Pianificazione Fiscale<br>
      I risultati hanno valore indicativo e non sostituiscono la consulenza professionale individuale.<br>
      Fonti: Circ. INPS n. 9/2026 · CCNL Lavoro Domestico · Artt. 10 e 15 TUIR<br><br>
      © {oggi.year} Gaetani &amp; Partners Consulting – Uso riservato · Tutti i diritti riservati
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
