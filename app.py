# app.py
# Studio Gaetani – Colf/Badanti Cedolino & Costi (2026)
# Streamlit single-file app with password gate + calcoli cedolino (ore, festività, straordinari, ferie, contributi)
# NOTE: impostare la password in .streamlit/secrets.toml (consigliato) oppure come variabile d'ambiente GAETANI_APP_PASSWORD

from __future__ import annotations
import os
import hashlib
import hmac
from dataclasses import dataclass
import streamlit as st

APP_TITLE = "Studio Gaetani – Cedolino Colf (automatico)"

# -----------------------------
# Security helpers (simple password gate)
# -----------------------------
def _hash_password(password: str, salt: str) -> str:
    """PBKDF2-HMAC-SHA256; returns hex string."""
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000)
    return dk.hex()

def verify_password(plain: str, salt: str, expected_hex: str) -> bool:
    got = _hash_password(plain, salt)
    return hmac.compare_digest(got, expected_hex)

def password_gate() -> bool:
    """
    Password access:
      - secrets: st.secrets["auth"]["salt"] and st.secrets["auth"]["password_hash"]
      - OR env: GAETANI_APP_PASSWORD (plain, fallback) — not recommended for production.
    """
    st.set_page_config(page_title=APP_TITLE, layout="centered")
    st.title(APP_TITLE)

    auth_cfg = st.secrets.get("auth", None)
    if auth_cfg and "salt" in auth_cfg and "password_hash" in auth_cfg:
        salt = str(auth_cfg["salt"])
        expected = str(auth_cfg["password_hash"]).lower().strip()
        mode = "hashed"
    else:
        expected = os.getenv("GAETANI_APP_PASSWORD", "")
        salt = ""
        mode = "plain_env"

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    with st.form("login"):
        st.subheader("Accesso riservato")
        pwd = st.text_input("Password", type="password")
        ok = st.form_submit_button("Entra")

    if ok:
        if mode == "hashed":
            if verify_password(pwd, salt, expected):
                st.session_state.authenticated = True
                st.success("Accesso effettuato.")
                st.rerun()
            else:
                st.error("Password errata.")
        else:
            if pwd and pwd == expected:
                st.session_state.authenticated = True
                st.success("Accesso effettuato.")
                st.rerun()
            else:
                st.error("Password errata o non configurata. Imposta GAETANI_APP_PASSWORD o secrets.toml.")

    st.caption("© Studio Gaetani – uso interno / clienti dello Studio.")
    return False

# -----------------------------
# Domain model
# -----------------------------
@dataclass
class ContributionParams:
    # 2026 default (fascia fino a 24 ore sett. e retribuzione oraria <= soglia)
    soglia_oraria_fascia1: float = 9.61
    inps_ti_totale_h: float = 1.70
    inps_ti_lav_h: float = 0.43
    inps_td_totale_h: float = 1.82
    inps_td_lav_h: float = 0.43
    cassa_totale_h: float = 0.06
    cassa_lav_h: float = 0.02

@dataclass
class PayrollInputs:
    mese: int
    anno: int
    tipo_contratto: str  # "TI" or "TD"
    ore_mese: float
    paga_oraria_lorda: float | None  # if None, compute from net target
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
    paga_oraria_lorda: float
    paga_oraria_netta: float
    costo_orario_datore: float
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

# -----------------------------
# Calculation
# -----------------------------
def compute_gross_from_net_target(net_h: float, tipo: str, p: ContributionParams) -> tuple[float, float, float, str]:
    """
    Calcolo inverso (stima):
      net_h = gross_h - inps_lav_h - cassa_lav_h
    Valido entro la fascia contributiva impostata. Se gross supera la soglia, avvisa.
    """
    tipo = tipo.upper().strip()
    if tipo not in ("TI", "TD"):
        tipo = "TD"

    inps_lav_h = p.inps_td_lav_h if tipo == "TD" else p.inps_ti_lav_h
    inps_tot_h = p.inps_td_totale_h if tipo == "TD" else p.inps_ti_totale_h

    gross_h = max(0.0, net_h + inps_lav_h + p.cassa_lav_h)

    inps_dat_h = max(0.0, inps_tot_h - inps_lav_h)
    cassa_dat_h = max(0.0, p.cassa_totale_h - p.cassa_lav_h)
    costo_orario = gross_h + inps_dat_h + cassa_dat_h

    warning = ""
    if gross_h > p.soglia_oraria_fascia1:
        warning = (
            "ATTENZIONE: la paga oraria lorda calcolata supera la soglia della fascia 1 "
            f"(> {p.soglia_oraria_fascia1:.2f} €/h). In tal caso i contributi INPS orari possono cambiare: "
            "aggiorna i parametri contributivi secondo la fascia corretta."
        )

    return gross_h, net_h, costo_orario, warning

def compute_payroll(inp: PayrollInputs, p: ContributionParams) -> PayrollResults:
    tipo = inp.tipo_contratto.upper().strip()
    if tipo not in ("TI", "TD"):
        tipo = "TD"

    warning = ""
    if inp.paga_oraria_lorda is None and inp.paga_oraria_netto_target is not None:
        gross_h, net_h_target, costo_orario, warning = compute_gross_from_net_target(inp.paga_oraria_netto_target, tipo, p)
    elif inp.paga_oraria_lorda is not None:
        gross_h = float(inp.paga_oraria_lorda)
        inps_lav_h = p.inps_td_lav_h if tipo == "TD" else p.inps_ti_lav_h
        net_h_target = max(0.0, gross_h - inps_lav_h - p.cassa_lav_h)
        inps_tot_h = p.inps_td_totale_h if tipo == "TD" else p.inps_ti_totale_h
        inps_dat_h = max(0.0, inps_tot_h - inps_lav_h)
        cassa_dat_h = max(0.0, p.cassa_totale_h - p.cassa_lav_h)
        costo_orario = gross_h + inps_dat_h + cassa_dat_h
        if gross_h > p.soglia_oraria_fascia1:
            warning = (
                "ATTENZIONE: la paga oraria lorda supera la soglia della fascia 1 "
                f"(> {p.soglia_oraria_fascia1:.2f} €/h). Verifica la fascia contributiva INPS corretta."
            )
    else:
        gross_h = 0.0
        net_h_target = 0.0
        costo_orario = 0.0

    ore = max(0.0, float(inp.ore_mese))
    fest = max(0, int(inp.n_festivita))

    lordo_base = ore * gross_h
    lordo_festivita = (lordo_base / 26.0) * fest if fest > 0 else 0.0
    lordo_straordinario = max(0.0, inp.ore_straordinario) * gross_h * (1.0 + max(0.0, inp.maggiorazione_straord_pct)/100.0)
    lordo_ferie = max(0.0, inp.ore_ferie) * gross_h
    lordo_indennita = max(0.0, inp.indennita_euro)

    lordo_totale = lordo_base + lordo_festivita + lordo_straordinario + lordo_ferie + lordo_indennita

    ore_fest_equiv = (ore / 26.0) * fest if fest > 0 else 0.0
    ore_contr = ore + max(0.0, inp.ore_ferie) + max(0.0, inp.ore_straordinario) + (ore_fest_equiv if inp.include_festivita_contributi else 0.0)

    inps_tot_h = p.inps_td_totale_h if tipo == "TD" else p.inps_ti_totale_h
    inps_lav_h = p.inps_td_lav_h if tipo == "TD" else p.inps_ti_lav_h
    cassa_tot_h = p.cassa_totale_h
    cassa_lav_h = p.cassa_lav_h

    inps_tot = ore_contr * inps_tot_h
    inps_lav = ore_contr * inps_lav_h
    inps_dat = max(0.0, inps_tot - inps_lav)

    cassa_tot = ore_contr * cassa_tot_h
    cassa_lav = ore_contr * cassa_lav_h
    cassa_dat = max(0.0, cassa_tot - cassa_lav)

    trattenute_varie = max(0.0, inp.trattenute_varie_euro)
    trattenute_tot = inps_lav + cassa_lav + trattenute_varie

    netto = max(0.0, lordo_totale - trattenute_tot)
    costo_datore = lordo_totale + inps_dat + cassa_dat

    ore_contr_trim = ore_contr * 3.0
    vers_inps_trim = ore_contr_trim * inps_tot_h
    vers_cassa_trim = ore_contr_trim * cassa_tot_h
    vers_tot_trim = vers_inps_trim + vers_cassa_trim

    rateo_13a = lordo_totale / 12.0
    tfr = lordo_totale / 13.5

    if warning:
        st.warning(warning)

    return PayrollResults(
        paga_oraria_lorda=gross_h,
        paga_oraria_netta=net_h_target,
        costo_orario_datore=costo_orario,
        ore_festivita_equiv=ore_fest_equiv,
        ore_contributive=ore_contr,
        lordo_base=lordo_base,
        lordo_festivita=lordo_festivita,
        lordo_straordinario=lordo_straordinario,
        lordo_ferie=lordo_ferie,
        lordo_indennita=lordo_indennita,
        lordo_totale=lordo_totale,
        inps_lav=inps_lav,
        cassa_lav=cassa_lav,
        trattenute_varie=trattenute_varie,
        trattenute_tot=trattenute_tot,
        netto=netto,
        inps_datore=inps_dat,
        cassa_datore=cassa_dat,
        costo_datore=costo_datore,
        vers_inps_trim=vers_inps_trim,
        vers_cassa_trim=vers_cassa_trim,
        vers_tot_trim=vers_tot_trim,
        rateo_13a=rateo_13a,
        tfr=tfr,
    )

# -----------------------------
# UI helpers
# -----------------------------
def euro(x: float) -> str:
    return f"€ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    if not password_gate():
        return

    st.divider()
    st.caption("Puoi inserire la paga **lorda** oppure la paga **netta desiderata** per ottenere la lorda calcolata e il costo datore (stima).")

    with st.expander("Parametri contributivi (2026) – modificabili", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            soglia = st.number_input("Soglia fascia 1 (€/h)", value=9.61, step=0.01, format="%.2f")
            cassa_tot = st.number_input("CAS.SA.COLF totale (€/h)", value=0.06, step=0.01, format="%.2f")
            cassa_lav = st.number_input("CAS.SA.COLF lav. (€/h)", value=0.02, step=0.01, format="%.2f")
        with col2:
            inps_ti_tot = st.number_input("INPS TI totale (€/h)", value=1.70, step=0.01, format="%.2f")
            inps_ti_lav = st.number_input("INPS TI lav. (€/h)", value=0.43, step=0.01, format="%.2f")
        with col3:
            inps_td_tot = st.number_input("INPS TD totale (€/h)", value=1.82, step=0.01, format="%.2f")
            inps_td_lav = st.number_input("INPS TD lav. (€/h)", value=0.43, step=0.01, format="%.2f")

        params = ContributionParams(
            soglia_oraria_fascia1=soglia,
            inps_ti_totale_h=inps_ti_tot,
            inps_ti_lav_h=inps_ti_lav,
            inps_td_totale_h=inps_td_tot,
            inps_td_lav_h=inps_td_lav,
            cassa_totale_h=cassa_tot,
            cassa_lav_h=cassa_lav,
        )

    st.subheader("Input cedolino")
    c1, c2, c3 = st.columns(3)
    with c1:
        mese = st.number_input("Mese (1–12)", min_value=1, max_value=12, value=2, step=1)
        anno = st.number_input("Anno", min_value=2020, max_value=2100, value=2026, step=1)
    with c2:
        tipo = st.selectbox("Tipo contratto", ["TD", "TI"], index=0)
        ore_mese = st.number_input("Ore lavorate nel mese", min_value=0.0, value=32.0, step=1.0)
    with c3:
        n_fest = st.number_input("N. festività retribuite nel mese", min_value=0, value=0, step=1)
        inc_fest_contr = st.checkbox("Includi festività nei contributi", value=True)

    st.markdown("### Paga oraria")
    mode = st.radio("Modalità di inserimento", ["Inserisco paga oraria LORDA", "Inserisco paga oraria NETTA desiderata"], horizontal=True)
    if mode == "Inserisco paga oraria LORDA":
        paga_lorda = st.number_input("Paga oraria lorda (€)", min_value=0.0, value=7.01, step=0.01, format="%.2f")
        paga_net_target = None
    else:
        paga_lorda = None
        paga_net_target = st.number_input("Paga oraria netta desiderata (€)", min_value=0.0, value=6.55, step=0.01, format="%.2f")

    st.markdown("### Voci variabili")
    v1, v2, v3 = st.columns(3)
    with v1:
        ore_straord = st.number_input("Ore straordinario", min_value=0.0, value=0.0, step=0.5)
        magg = st.number_input("Maggiorazione straordinario (%)", min_value=0.0, value=25.0, step=1.0)
    with v2:
        ore_ferie = st.number_input("Ore ferie godute retribuite", min_value=0.0, value=0.0, step=0.5)
        indennita = st.number_input("Indennità / altre competenze (€)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    with v3:
        trattenute_varie = st.number_input("Trattenute varie (€)", min_value=0.0, value=0.0, step=1.0, format="%.2f")

    inp = PayrollInputs(
        mese=int(mese),
        anno=int(anno),
        tipo_contratto=tipo,
        ore_mese=float(ore_mese),
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

    st.divider()
    st.subheader("Risultati")

    k1, k2, k3 = st.columns(3)
    k1.metric("Paga oraria lorda", euro(res.paga_oraria_lorda))
    k2.metric("Paga oraria netta (stima)", euro(res.paga_oraria_netta))
    k3.metric("Costo orario datore (stima)", euro(res.costo_orario_datore))

    st.markdown("#### Cedolino – sintesi")
    colA, colB = st.columns(2)
    with colA:
        st.write("**Competenze lorde**")
        st.write(f"- Base: {euro(res.lordo_base)}")
        st.write(f"- Festività: {euro(res.lordo_festivita)}")
        st.write(f"- Straordinario: {euro(res.lordo_straordinario)}")
        st.write(f"- Ferie: {euro(res.lordo_ferie)}")
        st.write(f"- Indennità: {euro(res.lordo_indennita)}")
        st.write(f"**Totale lordo: {euro(res.lordo_totale)}**")
    with colB:
        st.write("**Trattenute**")
        st.write(f"- INPS (lav.): {euro(res.inps_lav)}")
        st.write(f"- CAS.SA.COLF (lav.): {euro(res.cassa_lav)}")
        st.write(f"- Trattenute varie: {euro(res.trattenute_varie)}")
        st.write(f"**Totale trattenute: {euro(res.trattenute_tot)}**")
        st.write(f"### Netto: {euro(res.netto)}")

    st.markdown("#### Datore di lavoro")
    colC, colD = st.columns(2)
    with colC:
        st.write(f"- INPS (datore): {euro(res.inps_datore)}")
        st.write(f"- CAS.SA.COLF (datore): {euro(res.cassa_datore)}")
    with colD:
        st.write(f"### Costo mensile datore: {euro(res.costo_datore)}")

    st.markdown("#### Versamento contributi (stima trimestrale)")
    st.write(f"- INPS trimestre: {euro(res.vers_inps_trim)}")
    st.write(f"- CAS.SA.COLF trimestre: {euro(res.vers_cassa_trim)}")
    st.write(f"**Totale trimestre: {euro(res.vers_tot_trim)}**")

    st.markdown("#### Accantonamenti (facoltativi)")
    st.write(f"- Rateo 13ª (lordo/12): {euro(res.rateo_13a)}")
    st.write(f"- TFR (lordo/13,5): {euro(res.tfr)}")


    st.caption("Nota: i calcoli assumono parametri contributivi orari impostati nella sezione 'Parametri contributivi'. "
               "Se la paga oraria supera la soglia della fascia selezionata o cambia l'orario settimanale, "
               "i contributi possono variare: aggiornare i parametri secondo tabella INPS.")

if __name__ == "__main__":
    main()
# --- INIZIO CODICE TEMPORANEO ---
import streamlit as st
import os
import hashlib

st.divider()
st.subheader("🔧 Generatore Password (Temporaneo)")
nuova_pass = st.text_input("Scrivi qui la password che vuoi usare", type="default")

if st.button("Genera i codici segreti"):
    if nuova_pass:
        salt = os.urandom(16).hex()
        dk = hashlib.pbkdf2_hmac("sha256", nuova_pass.encode("utf-8"), salt.encode("utf-8"), 200_000)
        password_hash = dk.hex()
        
        testo_da_copiare = f"""
[auth]
salt = "{salt}"
password_hash = "{password_hash}"
"""
        st.success("Ecco i tuoi codici! Copiali qui sotto:")
        st.code(testo_da_copiare, language="toml")
        st.warning("⚠️ Dopo aver copiato questi codici nel file secrets.toml, CANCELLA questo pezzo di codice dal file app.py!")
# --- FINE CODICE TEMPORANEO ---