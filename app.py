# app.py
# GAETANI & PARTNERS Consulting – Cedolino Colf/Badanti (2026)
# Versione 2.0 – Aggiornata con tutte le fasce contributive INPS 2026

from __future__ import annotations
from dataclasses import dataclass, field
import streamlit as st

APP_TITLE = "Gaetani & Partners – Cedolino Lavoro Domestico 2026"

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Mulish:wght@300;400;500;600;700&display=swap');

    /* ── Reset & base ── */
    html, body, [data-testid="stAppViewContainer"] {
        background: #F0F3F8 !important;
        font-family: 'Mulish', sans-serif !important;
    }
    [data-testid="stSidebar"] { display: none; }

    /* ── Header brand ── */
    .gp-header {
        background: linear-gradient(135deg, #14213D 0%, #1D3461 60%, #14213D 100%);
        border-radius: 0 0 0 0;
        padding: 36px 48px 28px;
        margin: -1rem -1rem 0 -1rem;
        position: relative;
        overflow: hidden;
    }
    .gp-header::before {
        content: '';
        position: absolute;
        top: -30px; right: -30px;
        width: 220px; height: 220px;
        background: radial-gradient(circle, rgba(196,160,72,0.18) 0%, transparent 70%);
        border-radius: 50%;
    }
    .gp-header::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #C4A048, #E8CC7A, #C4A048, transparent);
    }
    .gp-logo-row {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 6px;
    }
    .gp-logo-icon {
        width: 48px; height: 48px;
        background: linear-gradient(135deg, #C4A048, #E8CC7A);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 15px rgba(196,160,72,0.4);
        flex-shrink: 0;
    }
    .gp-firm-name {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        letter-spacing: 0.5px;
        line-height: 1.1;
    }
    .gp-firm-tagline {
        font-size: 11px !important;
        color: #C4A048 !important;
        letter-spacing: 2.5px !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
        font-family: 'Mulish', sans-serif !important;
    }
    .gp-app-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 19px !important;
        font-weight: 400 !important;
        font-style: italic !important;
        color: rgba(240,243,248,0.85) !important;
        margin-top: 6px !important;
    }
    .gp-pill {
        display: inline-block;
        background: rgba(196,160,72,0.2);
        border: 1px solid rgba(196,160,72,0.5);
        color: #E8CC7A;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 20px;
        margin-left: 8px;
        vertical-align: middle;
    }

    /* ── Section titles ── */
    .gp-section-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #14213D !important;
        border-left: 3px solid #C4A048;
        padding-left: 14px !important;
        margin: 28px 0 14px 0 !important;
    }
    .gp-section-sub {
        font-family: 'Mulish', sans-serif !important;
        font-size: 11px !important;
        letter-spacing: 1.8px !important;
        text-transform: uppercase !important;
        color: #7A8CA8 !important;
        font-weight: 700 !important;
        margin-bottom: 20px !important;
    }

    /* ── Cards ── */
    .gp-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 24px 28px;
        box-shadow: 0 1px 3px rgba(20,33,61,0.06), 0 4px 16px rgba(20,33,61,0.04);
        margin-bottom: 16px;
        border: 1px solid rgba(20,33,61,0.07);
    }
    .gp-card-title {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #14213D !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 14px !important;
        padding-bottom: 10px !important;
        border-bottom: 1px solid #EEF1F7 !important;
    }
    .gp-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        font-size: 14px;
        color: #3D4F6B;
        border-bottom: 1px dashed rgba(20,33,61,0.07);
    }
    .gp-row:last-child { border-bottom: none; }
    .gp-row-label { font-weight: 400; }
    .gp-row-value { font-weight: 600; font-family: 'Mulish', sans-serif; }
    .gp-row-total {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 6px;
        font-size: 15px;
        font-weight: 700;
        color: #14213D;
        border-top: 2px solid #14213D;
        margin-top: 6px;
    }
    .gp-netto {
        background: linear-gradient(135deg, #14213D, #1D3461);
        border-radius: 10px;
        padding: 16px 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 12px;
    }
    .gp-netto-label {
        color: rgba(255,255,255,0.75);
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
    .gp-netto-value {
        color: #E8CC7A;
        font-size: 22px;
        font-weight: 700;
        font-family: 'Cormorant Garamond', serif;
    }
    .gp-kpi-row {
        display: flex; gap: 14px; margin-bottom: 20px; flex-wrap: wrap;
    }
    .gp-kpi {
        flex: 1; min-width: 140px;
        background: #FFFFFF;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(20,33,61,0.06), 0 4px 12px rgba(20,33,61,0.03);
        border: 1px solid rgba(20,33,61,0.07);
        text-align: center;
    }
    .gp-kpi-label {
        font-size: 10px;
        color: #7A8CA8;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .gp-kpi-value {
        font-family: 'Cormorant Garamond', serif;
        font-size: 22px;
        font-weight: 700;
        color: #14213D;
    }
    .gp-kpi-sub {
        font-size: 10px;
        color: #7A8CA8;
        margin-top: 3px;
    }
    .gp-kpi-gold .gp-kpi-value { color: #9A7A28; }
    .gp-kpi-accent .gp-kpi-value { color: #1D6A3E; }

    /* ── Fascia badge ── */
    .gp-fascia {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .gp-fascia-1 { background: #EDF7F0; color: #1D6A3E; border: 1px solid #9DD4B1; }
    .gp-fascia-2 { background: #FFF8E7; color: #9A6A00; border: 1px solid #F0D070; }
    .gp-fascia-3 { background: #FEF0EE; color: #B03020; border: 1px solid #F4AAAA; }
    .gp-fascia-4 { background: #EEF0FF; color: #3040B0; border: 1px solid #AABBF0; }

    /* ── Warning/info boxes ── */
    .gp-warning {
        background: #FFF8E7;
        border-left: 4px solid #C4A048;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        font-size: 13px;
        color: #7A5A00;
        margin: 10px 0;
    }
    .gp-error {
        background: #FEF0EE;
        border-left: 4px solid #CC3020;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        font-size: 13px;
        color: #9A2010;
        margin: 10px 0;
    }
    .gp-info {
        background: #EEF4FF;
        border-left: 4px solid #3D7ACC;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        font-size: 13px;
        color: #1A3A6E;
        margin: 10px 0;
    }

    /* ── Divider ── */
    .gp-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(196,160,72,0.4), transparent);
        margin: 28px 0;
    }

    /* ── Login card ── */
    .gp-login-wrap {
        max-width: 420px;
        margin: 60px auto 0;
    }
    .gp-login-icon {
        text-align: center;
        font-size: 40px;
        margin-bottom: 10px;
    }
    .gp-login-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 22px;
        font-weight: 600;
        color: #14213D;
        text-align: center;
        margin-bottom: 4px;
    }
    .gp-login-sub {
        font-size: 12px;
        color: #7A8CA8;
        text-align: center;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 24px;
    }

    /* ── Footer ── */
    .gp-footer {
        text-align: center;
        padding: 28px 0 12px;
        font-size: 11px;
        color: #A0AABB;
        letter-spacing: 0.5px;
    }
    .gp-footer strong { color: #7A8CA8; }

    /* ── Streamlit overrides ── */
    [data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 1px solid rgba(20,33,61,0.09) !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0 4px 20px rgba(20,33,61,0.06) !important;
    }
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #14213D, #1D3461) !important;
        color: #E8CC7A !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Mulish', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        font-size: 13px !important;
        padding: 10px 28px !important;
        text-transform: uppercase !important;
        transition: all 0.2s !important;
    }
    div[data-testid="stButton"] > button:hover {
        box-shadow: 0 4px 16px rgba(20,33,61,0.3) !important;
        transform: translateY(-1px) !important;
    }
    label[data-testid="stWidgetLabel"] p {
        font-family: 'Mulish', sans-serif !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #3D4F6B !important;
        letter-spacing: 0.3px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    [data-testid="stSelectbox"] select {
        border-color: #D4DCE8 !important;
        border-radius: 7px !important;
        font-family: 'Mulish', sans-serif !important;
    }
    [data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid rgba(20,33,61,0.08) !important;
        border-radius: 10px !important;
    }
    [data-testid="stRadio"] label p {
        font-size: 13px !important;
        font-weight: 500 !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }
    div[data-testid="stCheckbox"] label p {
        font-size: 13px !important;
        font-weight: 500 !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 700 !important;
        font-size: 26px !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER HTML
# ─────────────────────────────────────────────────────────────────────────────
def euro(x: float) -> str:
    return f"€\u00a0{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def card_row(label: str, value: str, bold: bool = False) -> str:
    cls = "gp-row-total" if bold else "gp-row"
    return f'<div class="{cls}"><span class="gp-row-label">{label}</span><span class="gp-row-value">{value}</span></div>'

def card(title: str, rows_html: str) -> str:
    return f'<div class="gp-card"><div class="gp-card-title">{title}</div>{rows_html}</div>'

def netto_box(value: str) -> str:
    return f'<div class="gp-netto"><span class="gp-netto-label">Netto in busta</span><span class="gp-netto-value">{value}</span></div>'

def kpi(label: str, value: str, sub: str = "", extra_cls: str = "") -> str:
    return f'<div class="gp-kpi {extra_cls}"><div class="gp-kpi-label">{label}</div><div class="gp-kpi-value">{value}</div><div class="gp-kpi-sub">{sub}</div></div>'

def badge_fascia(n: int) -> str:
    desc = {1: "Fascia 1 (≤ €9,61/h)", 2: "Fascia 2 (€9,61–€11,70/h)", 3: "Fascia 3 (> €11,70/h)", 4: "Fascia 4 (> 24h/sett)"}
    return f'<span class="gp-fascia gp-fascia-{n}">{desc.get(n, f"Fascia {n}")}</span>'

def info_box(msg: str, tipo: str = "info") -> str:
    return f'<div class="gp-{tipo}">{msg}</div>'


# ─────────────────────────────────────────────────────────────────────────────
# PASSWORD GATE
# ─────────────────────────────────────────────────────────────────────────────
def get_password() -> str:
    """
    Legge la password da Streamlit Secrets se disponibile,
    altrimenti usa il default di fallback.
    Configurazione Secrets (share.streamlit.io → Edit secrets):
        [auth]
        password = "LatuaPasswordSicura!"
    """
    try:
        return st.secrets["auth"]["password"]
    except Exception:
        return "GaetaniPartners2026"  # Fallback locale – cambiare in produzione


def password_gate() -> bool:
    st.set_page_config(
        page_title=APP_TITLE,
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_css()
    _render_header(show_anno=False)

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown('<div class="gp-login-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="gp-login-icon">🔒</div>', unsafe_allow_html=True)
    st.markdown('<div class="gp-login-title">Accesso riservato</div>', unsafe_allow_html=True)
    st.markdown('<div class="gp-login-sub">Area clienti Studio</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        pwd = st.text_input("Password", type="password", placeholder="Inserire la password di accesso")
        ok = st.form_submit_button("Entra →")

    if ok:
        if pwd == get_password():
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.markdown(info_box("⛔  Password non corretta. Contattare lo Studio.", "error"), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="gp-footer">© 2026 <strong>Gaetani & Partners Consulting</strong> · Uso riservato ai clienti dello Studio</div>', unsafe_allow_html=True)
    return False


def _render_header(show_anno: bool = True):
    anno_pill = '<span class="gp-pill">2026</span>' if show_anno else ''
    st.markdown(f"""
    <div class="gp-header">
        <div class="gp-logo-row">
            <div class="gp-logo-icon">⚖</div>
            <div>
                <div class="gp-firm-name">Gaetani &amp; Partners{anno_pill}</div>
                <div class="gp-firm-tagline">Consulting · Consulenza Tributaria &amp; Pianificazione Fiscale</div>
            </div>
        </div>
        <div class="gp-app-title">Gestione Cedolino Lavoro Domestico — Colf · Badanti · Baby-sitter</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DOMAIN MODEL
# ─────────────────────────────────────────────────────────────────────────────
MESI = ["Gennaio","Febbraio","Marzo","Aprile","Maggio","Giugno",
        "Luglio","Agosto","Settembre","Ottobre","Novembre","Dicembre"]

LIVELLI_NON_CONV: dict[str, float] = {
    "A – €6,51/h":  6.51,
    "AS – €6,76/h": 6.76,
    "B – €7,01/h":  7.01,
    "BS – €7,45/h": 7.45,
    "C – €7,86/h":  7.86,
    "CS – €8,30/h": 8.30,
    "D – €9,57/h":  9.57,
    "DS – €9,97/h": 9.97,
}
LIVELLI_CONV: dict[str, float] = {
    "A – €908,10/mese":    908.10,
    "AS – €958,55/mese":   958.55,
    "B – €983,16/mese":    983.16,
    "BS – €1.053,39/mese": 1053.39,
    "C – €1.123,63/mese":  1123.63,
    "CS – €1.193,84/mese": 1193.84,
    "D – €1.404,51+ind./mese": 1404.51 + 207.69,
    "DS – €1.474,73+ind./mese": 1474.73 + 207.69,
}


@dataclass
class ContributionParams:
    # Soglie fascia (retrib. effettiva oraria)
    soglia_fascia1: float = 9.61
    soglia_fascia2: float = 11.70
    soglia_ore_fascia4: float = 24.0  # >24h/sett → fascia 4

    # TI (Tempo Indeterminato) – CON quota CUAF
    ti_f1_tot: float = 1.70;  ti_f1_lav: float = 0.43
    ti_f2_tot: float = 1.92;  ti_f2_lav: float = 0.48
    ti_f3_tot: float = 2.34;  ti_f3_lav: float = 0.59
    ti_f4_tot: float = 1.24;  ti_f4_lav: float = 0.31  # >24h/sett

    # TD (Tempo Determinato) – include addiz. NASpI 1,40%
    td_f1_tot: float = 1.82;  td_f1_lav: float = 0.43
    td_f2_tot: float = 2.05;  td_f2_lav: float = 0.48
    td_f3_tot: float = 2.50;  td_f3_lav: float = 0.59
    td_f4_tot: float = 1.32;  td_f4_lav: float = 0.31  # >24h/sett

    # CAS.SA.COLF (tutti i rapporti)
    cassa_tot: float = 0.06;  cassa_lav: float = 0.02

    # Deducibilità / detrazione per datore
    deduzione_inps_max: float = 1549.37
    detrazione_badante_max: float = 2100.00


@dataclass
class PayrollInputs:
    mese: int
    anno: int
    tipo_contratto: str          # "TI" | "TD"
    convivente: bool
    ore_mese: float
    ore_settimanali: float       # per determinare fascia 4
    livello_ccnl_key: str
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
class PayrollResults:
    fascia_inps: int
    retrib_eff_h: float
    paga_oraria_lorda: float
    paga_oraria_netta: float
    costo_orario_datore: float
    inps_tot_h_usata: float
    inps_lav_h_usata: float
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
    warning_ccnl: str
    warning_fascia: str


# ─────────────────────────────────────────────────────────────────────────────
# CALCOLI
# ─────────────────────────────────────────────────────────────────────────────
def get_fascia(ore_settimanali: float, retrib_eff_h: float, p: ContributionParams) -> int:
    """
    Determina la fascia contributiva INPS.
    Fascia 4 (flat) se ore_settimanali > 24, indipendente dalla retribuzione.
    Altrimenti fascia 1/2/3 in base alla retribuzione effettiva oraria.
    """
    if ore_settimanali > p.soglia_ore_fascia4:
        return 4
    if retrib_eff_h <= p.soglia_fascia1:
        return 1
    elif retrib_eff_h <= p.soglia_fascia2:
        return 2
    else:
        return 3


def get_rates(fascia: int, tipo: str, p: ContributionParams) -> tuple[float, float]:
    """Restituisce (inps_tot_h, inps_lav_h) per la fascia e tipo contratto."""
    tipo = tipo.upper()
    mapping = {
        ("TI", 1): (p.ti_f1_tot, p.ti_f1_lav),
        ("TI", 2): (p.ti_f2_tot, p.ti_f2_lav),
        ("TI", 3): (p.ti_f3_tot, p.ti_f3_lav),
        ("TI", 4): (p.ti_f4_tot, p.ti_f4_lav),
        ("TD", 1): (p.td_f1_tot, p.td_f1_lav),
        ("TD", 2): (p.td_f2_tot, p.td_f2_lav),
        ("TD", 3): (p.td_f3_tot, p.td_f3_lav),
        ("TD", 4): (p.td_f4_tot, p.td_f4_lav),
    }
    return mapping.get((tipo, fascia), (p.td_f1_tot, p.td_f1_lav))


def compute_gross_from_net(net_h: float, ore_sett: float, tipo: str, p: ContributionParams) -> tuple[float, int, float]:
    """Calcola lordo da netto target. Restituisce (gross_h, fascia, retrib_eff_h)."""
    tipo = tipo.upper()
    # Stima iniziale: fascia 1
    for _ in range(5):  # iterazione per convergenza fascia
        gross_h_est = net_h + p.td_f1_lav + p.cassa_lav
        retrib_eff = gross_h_est * (13 / 12)
        fascia = get_fascia(ore_sett, retrib_eff, p)
        _, lav_h = get_rates(fascia, tipo, p)
        gross_h_est = net_h + lav_h + p.cassa_lav
    gross_h = max(0.0, gross_h_est)
    retrib_eff = gross_h * (13 / 12)
    fascia = get_fascia(ore_sett, retrib_eff, p)
    return gross_h, fascia, retrib_eff


def compute_payroll(inp: PayrollInputs, p: ContributionParams) -> PayrollResults:
    tipo = inp.tipo_contratto.upper().strip()
    if tipo not in ("TI", "TD"):
        tipo = "TD"

    ore_sett = max(0.0, float(inp.ore_settimanali))
    warning_fascia = ""
    warning_ccnl = ""

    # ── Determina paga oraria lorda ──
    if inp.paga_oraria_lorda is not None:
        gross_h = max(0.0, float(inp.paga_oraria_lorda))
        retrib_eff_h = gross_h * (13 / 12)
        fascia = get_fascia(ore_sett, retrib_eff_h, p)
        inps_tot_h, inps_lav_h = get_rates(fascia, tipo, p)
        inps_dat_h = max(0.0, inps_tot_h - inps_lav_h)
        cassa_dat_h = max(0.0, p.cassa_tot - p.cassa_lav)
        net_h = max(0.0, gross_h - inps_lav_h - p.cassa_lav)
        costo_orario = gross_h + inps_dat_h + cassa_dat_h
    elif inp.paga_oraria_netto_target is not None:
        gross_h, fascia, retrib_eff_h = compute_gross_from_net(
            float(inp.paga_oraria_netto_target), ore_sett, tipo, p)
        inps_tot_h, inps_lav_h = get_rates(fascia, tipo, p)
        inps_dat_h = max(0.0, inps_tot_h - inps_lav_h)
        cassa_dat_h = max(0.0, p.cassa_tot - p.cassa_lav)
        net_h = float(inp.paga_oraria_netto_target)
        costo_orario = gross_h + inps_dat_h + cassa_dat_h
    else:
        gross_h = net_h = costo_orario = retrib_eff_h = 0.0
        fascia = 1
        inps_tot_h = inps_lav_h = 0.0

    # ── Verifica minimo CCNL ──
    if inp.livello_ccnl_key:
        if inp.convivente:
            minimo_mensile = LIVELLI_CONV.get(inp.livello_ccnl_key, 0.0)
            if minimo_mensile > 0 and inp.ore_mese > 0:
                minimo_h_equiv = minimo_mensile / max(1, inp.ore_mese)
                if gross_h < minimo_h_equiv * 0.999:
                    warning_ccnl = (
                        f"⚠️ La paga oraria equivalente ({euro(gross_h)}/h) è inferiore al minimo "
                        f"CCNL 2026 per il livello selezionato ({euro(minimo_h_equiv)}/h equiv. da €{minimo_mensile:,.2f}/mese)."
                    )
        else:
            minimo_h = LIVELLI_NON_CONV.get(inp.livello_ccnl_key, 0.0)
            if minimo_h > 0 and gross_h < minimo_h * 0.999:
                warning_ccnl = (
                    f"⚠️ La paga oraria lorda ({euro(gross_h)}/h) è inferiore al minimo "
                    f"CCNL 2026 per il livello selezionato ({euro(minimo_h)}/h)."
                )

    if fascia >= 2 and ore_sett <= p.soglia_ore_fascia4:
        warning_fascia = (
            f"ℹ️ La retribuzione effettiva oraria ({euro(retrib_eff_h)}/h, include rateo 13ª) "
            f"supera la soglia della Fascia 1 (€{p.soglia_fascia1}). "
            f"Applicata automaticamente la Fascia {fascia}."
        )

    # ── Competenze lorde ──
    ore = max(0.0, float(inp.ore_mese))
    fest = max(0, int(inp.n_festivita))
    lordo_base = ore * gross_h
    lordo_festivita = (lordo_base / 26.0) * fest if fest > 0 else 0.0
    lordo_straordinario = max(0.0, inp.ore_straordinario) * gross_h * (1.0 + max(0.0, inp.maggiorazione_straord_pct) / 100.0)
    lordo_ferie = max(0.0, inp.ore_ferie) * gross_h
    lordo_indennita = max(0.0, inp.indennita_euro)
    lordo_totale = lordo_base + lordo_festivita + lordo_straordinario + lordo_ferie + lordo_indennita

    # ── Ore contributive ──
    ore_fest_equiv = (ore / 26.0) * fest if fest > 0 else 0.0
    ore_contr = (ore
                 + max(0.0, inp.ore_ferie)
                 + max(0.0, inp.ore_straordinario)
                 + (ore_fest_equiv if inp.include_festivita_contributi else 0.0))

    # ── Contributi ──
    inps_tot = ore_contr * inps_tot_h
    inps_lav = ore_contr * inps_lav_h
    inps_dat = max(0.0, inps_tot - inps_lav)

    cassa_tot_val = ore_contr * p.cassa_tot
    cassa_lav_val = ore_contr * p.cassa_lav
    cassa_dat_val = max(0.0, cassa_tot_val - cassa_lav_val)

    trattenute_varie = max(0.0, inp.trattenute_varie_euro)
    trattenute_tot = inps_lav + cassa_lav_val + trattenute_varie
    netto = max(0.0, lordo_totale - trattenute_tot)
    costo_datore = lordo_totale + inps_dat + cassa_dat_val

    # ── Versamenti trimestrali ──
    ore_contr_trim = ore_contr * 3.0
    vers_inps_trim = ore_contr_trim * inps_tot_h
    vers_cassa_trim = ore_contr_trim * p.cassa_tot
    vers_tot_trim = vers_inps_trim + vers_cassa_trim

    # ── Accantonamenti ──
    rateo_13a = lordo_totale / 12.0
    tfr = lordo_totale / 13.5

    return PayrollResults(
        fascia_inps=fascia,
        retrib_eff_h=retrib_eff_h,
        paga_oraria_lorda=gross_h,
        paga_oraria_netta=net_h,
        costo_orario_datore=costo_orario,
        inps_tot_h_usata=inps_tot_h,
        inps_lav_h_usata=inps_lav_h,
        ore_contributive=ore_contr,
        lordo_base=lordo_base,
        lordo_festivita=lordo_festivita,
        lordo_straordinario=lordo_straordinario,
        lordo_ferie=lordo_ferie,
        lordo_indennita=lordo_indennita,
        lordo_totale=lordo_totale,
        inps_lav=inps_lav,
        cassa_lav=cassa_lav_val,
        trattenute_varie=trattenute_varie,
        trattenute_tot=trattenute_tot,
        netto=netto,
        inps_datore=inps_dat,
        cassa_datore=cassa_dat_val,
        costo_datore=costo_datore,
        vers_inps_trim=vers_inps_trim,
        vers_cassa_trim=vers_cassa_trim,
        vers_tot_trim=vers_tot_trim,
        rateo_13a=rateo_13a,
        tfr=tfr,
        warning_ccnl=warning_ccnl,
        warning_fascia=warning_fascia,
    )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN UI
# ─────────────────────────────────────────────────────────────────────────────
def main():
    if not password_gate():
        return

    _render_header(show_anno=True)

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    # ── Nota introduttiva ──
    st.markdown(info_box(
        "ℹ️ <strong>Nota normativa:</strong> L'app applica automaticamente le tabelle contributive INPS 2026 "
        "(Circ. n. 9/2026) su tutte e quattro le fasce, inclusa la <em>Fascia 4 flat</em> per orari superiori a 24h/settimana. "
        "La fascia viene determinata sulla <em>retribuzione effettiva oraria</em> che include il rateo tredicesima (×13/12), "
        "come previsto dalla normativa. Il datore di lavoro domestico <strong>non è sostituto d'imposta</strong>: "
        "nessuna ritenuta IRPEF viene applicata in busta paga."
    ), unsafe_allow_html=True)

    # ── Parametri contributivi (avanzato) ──
    # Inizializza con defaults; saranno sovrascritti se l'utente apre l'expander
    _p = ContributionParams()
    # Pre-carica i widget con session_state defaults per raccogliere eventuali modifiche
    with st.expander("⚙️  Parametri contributivi 2026 — modifica solo se necessario", expanded=False):
        st.markdown('<p class="gp-section-sub">Valori da Circolare INPS n. 9 del 03/02/2026</p>', unsafe_allow_html=True)
        _t1, _t2 = st.tabs(["Fasce 1–3 (<24h/sett)", "Fascia 4 (>24h/sett) · CAS.SA"])
        with _t1:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.caption("**Fascia 1** ≤ €9,61/h")
                ti_f1_tot = st.number_input("TI totale", value=1.70, step=0.01, format="%.2f", key="ti_f1t")
                ti_f1_lav = st.number_input("TI lav.", value=0.43, step=0.01, format="%.2f", key="ti_f1l")
                td_f1_tot = st.number_input("TD totale", value=1.82, step=0.01, format="%.2f", key="td_f1t")
                td_f1_lav = st.number_input("TD lav.", value=0.43, step=0.01, format="%.2f", key="td_f1l")
                soglia_f1 = st.number_input("Soglia fascia 1 (€/h)", value=9.61, step=0.01, format="%.2f", key="sf1")
            with c2:
                st.caption("**Fascia 2** €9,61–€11,70/h")
                ti_f2_tot = st.number_input("TI totale", value=1.92, step=0.01, format="%.2f", key="ti_f2t")
                ti_f2_lav = st.number_input("TI lav.", value=0.48, step=0.01, format="%.2f", key="ti_f2l")
                td_f2_tot = st.number_input("TD totale", value=2.05, step=0.01, format="%.2f", key="td_f2t")
                td_f2_lav = st.number_input("TD lav.", value=0.48, step=0.01, format="%.2f", key="td_f2l")
                soglia_f2 = st.number_input("Soglia fascia 2 (€/h)", value=11.70, step=0.01, format="%.2f", key="sf2")
            with c3:
                st.caption("**Fascia 3** > €11,70/h")
                ti_f3_tot = st.number_input("TI totale", value=2.34, step=0.01, format="%.2f", key="ti_f3t")
                ti_f3_lav = st.number_input("TI lav.", value=0.59, step=0.01, format="%.2f", key="ti_f3l")
                td_f3_tot = st.number_input("TD totale", value=2.50, step=0.01, format="%.2f", key="td_f3t")
                td_f3_lav = st.number_input("TD lav.", value=0.59, step=0.01, format="%.2f", key="td_f3l")
        with _t2:
            c4, c5 = st.columns(2)
            with c4:
                st.caption("**Fascia 4** > 24h/sett (flat, indip. da retrib.)")
                ti_f4_tot = st.number_input("TI totale", value=1.24, step=0.01, format="%.2f", key="ti_f4t")
                ti_f4_lav = st.number_input("TI lav.", value=0.31, step=0.01, format="%.2f", key="ti_f4l")
                td_f4_tot = st.number_input("TD totale", value=1.32, step=0.01, format="%.2f", key="td_f4t")
                td_f4_lav = st.number_input("TD lav.", value=0.31, step=0.01, format="%.2f", key="td_f4l")
            with c5:
                st.caption("**CAS.SA.COLF** (tutti i rapporti)")
                cassa_tot = st.number_input("Totale (€/h)", value=0.06, step=0.01, format="%.2f", key="cst")
                cassa_lav = st.number_input("Lavoratore (€/h)", value=0.02, step=0.01, format="%.2f", key="csl")

        _p = ContributionParams(
            soglia_fascia1=soglia_f1, soglia_fascia2=soglia_f2,
            ti_f1_tot=ti_f1_tot, ti_f1_lav=ti_f1_lav,
            ti_f2_tot=ti_f2_tot, ti_f2_lav=ti_f2_lav,
            ti_f3_tot=ti_f3_tot, ti_f3_lav=ti_f3_lav,
            ti_f4_tot=ti_f4_tot, ti_f4_lav=ti_f4_lav,
            td_f1_tot=td_f1_tot, td_f1_lav=td_f1_lav,
            td_f2_tot=td_f2_tot, td_f2_lav=td_f2_lav,
            td_f3_tot=td_f3_tot, td_f3_lav=td_f3_lav,
            td_f4_tot=td_f4_tot, td_f4_lav=td_f4_lav,
            cassa_tot=cassa_tot, cassa_lav=cassa_lav,
        )

    params = _p

    # ─── INPUT PRINCIPALE ───
    st.markdown('<p class="gp-section-title">Dati del rapporto di lavoro</p>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        mese_sel = st.selectbox("Mese di riferimento", MESI, index=1)
        mese = MESI.index(mese_sel) + 1
        anno = st.number_input("Anno", min_value=2020, max_value=2100, value=2026, step=1)
    with col_b:
        tipo = st.selectbox("Tipo contratto", ["TD – Tempo Determinato", "TI – Tempo Indeterminato"], index=0)
        tipo_code = tipo[:2]
        convivente = st.checkbox("Lavoratore/trice convivente", value=False)
    with col_c:
        ore_mese = st.number_input("Ore lavorate nel mese", min_value=0.0, value=32.0, step=1.0)
        ore_sett = st.number_input("Ore settimanali (per fascia INPS)", min_value=0.0, value=8.0, step=1.0,
                                   help="Se > 24h/settimana si applica la Fascia 4 flat, indipendentemente dalla retribuzione.")

    col_d, col_e = st.columns([1, 1])
    with col_d:
        livelli = LIVELLI_CONV if convivente else LIVELLI_NON_CONV
        livello_keys = list(livelli.keys())
        default_idx = 2  # livello B
        livello_sel = st.selectbox("Livello CCNL", livello_keys, index=default_idx,
                                   help="L'app verifica che la paga non sia inferiore al minimo contrattuale.")
    with col_e:
        n_fest = st.number_input("N. festività retribuite nel mese", min_value=0, value=0, step=1)
        inc_fest_contr = st.checkbox("Includi festività nelle ore contributive", value=True)

    # ─── PAGA ORARIA ───
    st.markdown('<p class="gp-section-title">Paga oraria</p>', unsafe_allow_html=True)
    mode = st.radio(
        "Modalità di inserimento",
        ["Inserisco la paga oraria LORDA", "Inserisco la paga oraria NETTA desiderata (calcolo lordo automatico)"],
        horizontal=True
    )
    c_paga1, c_paga2 = st.columns([1, 2])
    with c_paga1:
        if mode == "Inserisco la paga oraria LORDA":
            min_ccnl = livelli.get(livello_sel, 7.01) if not convivente else 7.01
            paga_lorda = st.number_input("Paga oraria lorda (€)", min_value=0.0,
                                         value=float(min_ccnl if not convivente else 7.01),
                                         step=0.01, format="%.2f")
            paga_net_target = None
        else:
            paga_lorda = None
            paga_net_target = st.number_input("Paga oraria netta desiderata (€)", min_value=0.0,
                                               value=6.55, step=0.01, format="%.2f")

    # ─── VOCI VARIABILI ───
    st.markdown('<p class="gp-section-title">Voci variabili del mese</p>', unsafe_allow_html=True)
    v1, v2, v3 = st.columns(3)
    with v1:
        ore_straord = st.number_input("Ore straordinario", min_value=0.0, value=0.0, step=0.5)
        magg = st.number_input("Maggiorazione straordinario (%)", min_value=0.0, value=25.0, step=1.0)
    with v2:
        ore_ferie = st.number_input("Ore ferie godute retribuite", min_value=0.0, value=0.0, step=0.5)
        indennita = st.number_input("Indennità / altre competenze (€)", min_value=0.0, value=0.0,
                                    step=1.0, format="%.2f")
    with v3:
        trattenute_varie = st.number_input("Trattenute varie (€)", min_value=0.0, value=0.0,
                                           step=1.0, format="%.2f")
        st.caption("Es. anticipi, quote associative su richiesta lavoratore")

    # ─── CALCOLO ───
    inp = PayrollInputs(
        mese=mese, anno=anno,
        tipo_contratto=tipo_code,
        convivente=convivente,
        ore_mese=float(ore_mese),
        ore_settimanali=float(ore_sett),
        livello_ccnl_key=livello_sel,
        paga_oraria_lorda=paga_lorda,
        paga_oraria_netto_target=paga_net_target,
        n_festivita=int(n_fest),
        include_festivita_contributi=bool(inc_fest_contr),
        ore_straordinario=float(ore_straord),
        maggiorazione_straord_pct=float(magg),
        ore_ferie=float(ore_ferie),
        indennita_euro=float(indennita),
        trattenute_varie_euro=float(trattenute_varie),
    )
    res = compute_payroll(inp, params)

    # ─── AVVISI ───
    if res.warning_ccnl:
        st.markdown(info_box(res.warning_ccnl, "error"), unsafe_allow_html=True)
    if res.warning_fascia:
        st.markdown(info_box(res.warning_fascia, "warning"), unsafe_allow_html=True)

    st.markdown('<div class="gp-divider"></div>', unsafe_allow_html=True)

    # ─── RISULTATI ───
    st.markdown(f'<p class="gp-section-title">Cedolino — {mese_sel} {anno}</p>', unsafe_allow_html=True)

    # KPI row
    fascia_badge = badge_fascia(res.fascia_inps)
    st.markdown(f"""
    <div class="gp-kpi-row">
        {kpi("Paga oraria lorda", euro(res.paga_oraria_lorda), f"Ret. eff. {euro(res.retrib_eff_h)}/h · {fascia_badge}")}
        {kpi("Paga oraria netta", euro(res.paga_oraria_netta), "stima (no IRPEF)")}
        {kpi("Costo orario datore", euro(res.costo_orario_datore), "lordo + contrib. datore", "gp-kpi-gold")}
        {kpi("Netto mensile", euro(res.netto), "importo da corrispondere", "gp-kpi-accent")}
        {kpi("Costo mensile datore", euro(res.costo_datore), "tot. onere employeur")}
    </div>
    """, unsafe_allow_html=True)

    # ─── Due colonne: cedolino lavoratore + datore ───
    col_sx, col_dx = st.columns([1, 1])

    with col_sx:
        rows = (
            card_row("Base (ore × paga lorda)", euro(res.lordo_base))
            + card_row("Festività", euro(res.lordo_festivita))
            + card_row("Straordinario", euro(res.lordo_straordinario))
            + card_row("Ferie retribuite", euro(res.lordo_ferie))
            + card_row("Indennità / altre competenze", euro(res.lordo_indennita))
            + card_row("Totale lordo", euro(res.lordo_totale), bold=True)
            + "<br>"
            + card_row(f"INPS lavoratore ({euro(res.inps_lav_h_usata)}/h)", euro(res.inps_lav))
            + card_row("CAS.SA.COLF lavoratore (€0,02/h)", euro(res.cassa_lav))
            + card_row("Trattenute varie", euro(res.trattenute_varie))
            + card_row("Totale trattenute", euro(res.trattenute_tot), bold=True)
        )
        st.markdown(card("Competenze e trattenute lavoratore", rows), unsafe_allow_html=True)
        st.markdown(netto_box(euro(res.netto)), unsafe_allow_html=True)

        ore_info = f"Ore contributive: {res.ore_contributive:.1f}h · Fascia {res.fascia_inps} {tipo_code}"
        st.markdown(info_box(f"ℹ️ {ore_info} · INPS tot. {euro(res.inps_tot_h_usata)}/h", "info"),
                    unsafe_allow_html=True)

    with col_dx:
        rows2 = (
            card_row("Lordo totale (a carico datore)", euro(res.lordo_totale))
            + card_row(f"INPS datore ({euro(res.inps_tot_h_usata - res.inps_lav_h_usata)}/h)", euro(res.inps_datore))
            + card_row("CAS.SA.COLF datore (€0,04/h)", euro(res.cassa_datore))
            + card_row("Costo mensile datore", euro(res.costo_datore), bold=True)
        )
        st.markdown(card("Oneri datore di lavoro", rows2), unsafe_allow_html=True)

        rows3 = (
            card_row("INPS (versamento trimestrale)", euro(res.vers_inps_trim))
            + card_row("CAS.SA.COLF (trimestrale)", euro(res.vers_cassa_trim))
            + card_row("Totale versamento trimestrale", euro(res.vers_tot_trim), bold=True)
        )
        st.markdown(card("Versamenti contributivi — stima trimestrale", rows3), unsafe_allow_html=True)

        rows4 = (
            card_row("Rateo 13ª mensilità (lordo ÷ 12)", euro(res.rateo_13a))
            + card_row("Rateo TFR (lordo ÷ 13,5)", euro(res.tfr))
            + card_row("Totale accantonamenti mensili", euro(res.rateo_13a + res.tfr), bold=True)
        )
        st.markdown(card("Accantonamenti (da stanziare mensilmente)", rows4), unsafe_allow_html=True)

    # ─── Nota fiscale per il datore ───
    st.markdown('<div class="gp-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="gp-section-title">Note fiscali per il datore di lavoro</p>', unsafe_allow_html=True)

    col_note1, col_note2 = st.columns(2)
    with col_note1:
        st.markdown(info_box(
            f"<strong>Deduzione INPS (art. 10 TUIR):</strong> I contributi INPS versati sono deducibili dal "
            f"reddito complessivo fino a <strong>€ {params.deduzione_inps_max:,.2f}/anno</strong>. "
            f"I contributi trimestrali stimati per questo mese sono {euro(res.vers_inps_trim / 3)} "
            f"({euro(res.vers_inps_trim)} sul trimestre).", "info"
        ), unsafe_allow_html=True)
    with col_note2:
        st.markdown(info_box(
            f"<strong>Detrazione badante (art. 15 TUIR):</strong> Se il lavoratore assiste un familiare "
            f"non autosufficiente (certificato ASL/INPS), il datore ha diritto a una detrazione IRPEF "
            f"del 19% su un massimo di <strong>€ {params.detrazione_badante_max:,.2f}/anno</strong> "
            f"(reddito ≤ €40.000). Contattare lo Studio per la verifica dei requisiti.", "info"
        ), unsafe_allow_html=True)

    st.markdown(info_box(
        "<strong>Scadenze versamento contributi 2026 (solo PagoPA/portale INPS):</strong> "
        "10 aprile (I trim.) · 10 luglio (II trim.) · 10 ottobre (III trim.) · 10 gennaio 2027 (IV trim.). "
        "⚠️ Dal 2026 <em>non sono più accettati bollettini cartacei</em> (salvo datori ≥ 76 anni, deroga temporanea).",
        "warning"
    ), unsafe_allow_html=True)

    # ─── Footer ───
    st.markdown('<div class="gp-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="gp-footer">
        <strong>Gaetani &amp; Partners Consulting</strong> · Consulenza Tributaria &amp; Pianificazione Fiscale<br>
        I calcoli sono elaborati su parametri contributivi INPS 2026 (Circ. n. 9/2026) e CCNL Lavoro Domestico in vigore.<br>
        Il documento non sostituisce la consulenza professionale. Per assistenza contattare lo Studio.<br><br>
        © 2026 Gaetani &amp; Partners · Uso riservato ai clienti dello Studio
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
