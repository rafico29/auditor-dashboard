"""
RADAR DE ALERTAS – CONTRATACIÓN EN SALUD (SECOP)
Dashboard Auditor – Prototipo MVP v3.0 (Mejorado)
Datos híbridos: estructura real SECOP + scores simulados.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Radar de Alertas – Contratación en Salud",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS MEJORADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Source Sans 3', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #1a2a4a 0%, #2c4a7c 100%);
        color: white; padding: 1.2rem 2rem; border-radius: 10px;
        margin-bottom: 1.5rem; text-align: center;
        box-shadow: 0 4px 15px rgba(26,42,74,0.3);
    }
    .main-header h1 { margin: 0; font-size: 1.5rem; font-weight: 700; letter-spacing: 1px; }
    .main-header p { margin: 0.3rem 0 0 0; font-size: 0.85rem; opacity: 0.8; }

    .kpi-card {
        background: white; border-radius: 10px; padding: 0.9rem 1rem;
        text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #2c4a7c; transition: transform 0.2s ease;
    }
    .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.12); }
    .kpi-card.alert { border-top-color: #e74c3c; }
    .kpi-card.warning { border-top-color: #f39c12; }
    .kpi-card.success { border-top-color: #27ae60; }
    .kpi-card.info { border-top-color: #3498db; }
    .kpi-label {
        font-size: 0.72rem; font-weight: 600; color: #5a6a7a;
        text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.2rem;
    }
    .kpi-value { font-size: 1.6rem; font-weight: 700; color: #1a2a4a; line-height: 1.2; }
    .kpi-value.alert { color: #e74c3c; }
    .kpi-value.success { color: #27ae60; }
    .kpi-value.info { color: #3498db; }
    .kpi-delta { font-size: 0.72rem; color: #888; margin-top: 0.15rem; }

    .section-title {
        font-size: 1rem; font-weight: 700; color: #1a2a4a;
        border-left: 4px solid #2c4a7c; padding-left: 0.8rem;
        margin: 1.5rem 0 0.8rem 0;
    }

    .explanation-panel {
        background: #f8fafc; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: 1.2rem;
    }

    .provider-card {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }

    .quality-bar-bg {
        background: #eef2f7; border-radius: 6px; height: 18px;
        margin: 4px 0; overflow: hidden;
    }
    .quality-bar-fill {
        height: 100%; border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 600; color: white;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f4f8 0%, #e8eef5 100%);
    }

    .page-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a2a4a;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #2c4a7c;
    }

    .info-box {
        background: #e8f4f8;
        border-left: 4px solid #3498db;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FUNCIONES DE DATOS
# ─────────────────────────────────────────────
@st.cache_data
def generar_datos(n=600):
    np.random.seed(42)
    random.seed(42)

    departamentos = [
        "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar",
        "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca",
        "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía",
        "Guaviare", "Huila", "La Guajira", "Magdalena", "Meta",
        "Nariño", "Norte de Santander", "Putumayo", "Quindío",
        "Risaralda", "San Andrés", "Santander", "Sucre",
        "Tolima", "Valle del Cauca", "Vaupés", "Vichada", "Bogotá D.C."
    ]

    pesos = np.random.dirichlet(np.ones(len(departamentos)) * 0.5)
    pw = dict(zip(departamentos, pesos))
    for d in ["Bogotá D.C.", "Antioquia", "Valle del Cauca", "Atlántico"]:
        if d in pw: pw[d] *= 3
    total = sum(pw.values())
    pesos_norm = [pw[d] / total for d in departamentos]

    modalidades = ["Contratación Directa", "Licitación Pública", "Selección Abreviada", "Mínima Cuantía", "Concurso de Méritos"]
    tipos_entidad = ["Hospital", "ESE", "IPS", "EPS", "Secretaría de Salud", "Instituto Dptal Salud", "Clínica"]
    objetos = [
        "Suministro de medicamentos e insumos médicos",
        "Prestación de servicios de salud",
        "Mantenimiento de equipos biomédicos",
        "Servicios de aseo y desinfección hospitalaria",
        "Suministro de material médico-quirúrgico",
        "Consultoría en gestión hospitalaria",
        "Transporte asistencial de pacientes",
        "Servicios de alimentación hospitalaria",
        "Adquisición de equipos médicos",
        "Servicios de laboratorio clínico",
        "Servicios de imagenología diagnóstica",
        "Dotación de personal asistencial temporal",
    ]

    proveedores = [f"Prov-{i:03d}" for i in range(80)]

    records = []
    for i in range(n):
        dept = np.random.choice(departamentos, p=pesos_norm)
        modalidad = np.random.choice(modalidades, p=[0.35, 0.15, 0.25, 0.20, 0.05])
        tipo_ent = np.random.choice(tipos_entidad)
        base_valor = np.random.lognormal(mean=7.5, sigma=1.2)
        valor = round(base_valor * 1000, -3)
        valor = max(valor, 5_000_000)
        valor = min(valor, 15_000_000_000)
        fecha = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 900))

        score_base = np.random.beta(2, 5) * 100
        if modalidad == "Contratación Directa":
            score_base += np.random.uniform(5, 20)
        if valor > 3_000_000_000:
            score_base += np.random.uniform(10, 25)
        score = min(round(score_base, 1), 99.5)

        if score >= 70: nivel = "Alto"
        elif score >= 40: nivel = "Medio"
        else: nivel = "Bajo"

        factores = {
            "freq_proveedor": round(np.random.uniform(0, 50), 1),
            "valor_vs_historico": round(np.random.uniform(0, 40), 1),
            "num_oferentes": round(np.random.uniform(0, 25), 1),
            "modalidad_directa": round(np.random.uniform(5, 20) if modalidad == "Contratación Directa" else np.random.uniform(0, 5), 1),
            "variables_macro": round(np.random.uniform(0, 15), 1),
        }
        total_f = sum(factores.values())
        if total_f > 0:
            factores = {k: round(v / total_f * 100, 1) for k, v in factores.items()}

        proveedor = np.random.choice(proveedores[:40] if score >= 40 else proveedores)
        entidad_nombre = f"{tipo_ent} {dept}"
        dias_publicacion = random.randint(0, 45)

        records.append({
            "id_contrato": f"C-{random.randint(1000, 9999)}",
            "fecha": fecha, "anio": fecha.year,
            "mes": fecha.strftime("%b"), "mes_num": fecha.month,
            "departamento": dept,
            "entidad": entidad_nombre,
            "tipo_entidad": tipo_ent,
            "modalidad": modalidad,
            "objeto": np.random.choice(objetos),
            "valor": valor,
            "score_riesgo": score,
            "nivel_riesgo": nivel,
            "proveedor_id": proveedor,
            "contratos_previos_proveedor": random.randint(0, 15),
            "factor_freq_proveedor": factores["freq_proveedor"],
            "factor_valor_historico": factores["valor_vs_historico"],
            "factor_num_oferentes": factores["num_oferentes"],
            "factor_modalidad_directa": factores["modalidad_directa"],
            "factor_variables_macro": factores["variables_macro"],
            "valor_promedio_historico": round(valor * np.random.uniform(0.3, 0.8), -3),
            "num_oferentes": random.randint(1, 8),
            "dias_publicacion": dias_publicacion,
            "calidad_completitud": round(np.random.uniform(50, 100), 1),
            "calidad_consistencia": round(np.random.uniform(40, 100), 1),
            "calidad_oportunidad": round(max(0, 100 - dias_publicacion * 2.5), 1),
            "calidad_estandarizacion": round(np.random.uniform(30, 100), 1),
        })

    df = pd.DataFrame(records)
    df["calidad_datos"] = round(
        df["calidad_completitud"] * 0.30 +
        df["calidad_consistencia"] * 0.25 +
        df["calidad_oportunidad"] * 0.25 +
        df["calidad_estandarizacion"] * 0.20, 1
    )
    return df


@st.cache_data
def get_coords():
    return {
        "Amazonas": {"lat": -1.0, "lon": -71.9}, "Antioquia": {"lat": 6.9, "lon": -75.6},
        "Arauca": {"lat": 7.1, "lon": -70.7}, "Atlántico": {"lat": 10.7, "lon": -75.0},
        "Bolívar": {"lat": 8.6, "lon": -74.0}, "Boyacá": {"lat": 5.9, "lon": -73.4},
        "Caldas": {"lat": 5.3, "lon": -75.5}, "Caquetá": {"lat": 1.5, "lon": -75.6},
        "Casanare": {"lat": 5.3, "lon": -71.3}, "Cauca": {"lat": 2.7, "lon": -76.8},
        "Cesar": {"lat": 9.3, "lon": -73.5}, "Chocó": {"lat": 5.7, "lon": -76.6},
        "Córdoba": {"lat": 8.3, "lon": -75.6}, "Cundinamarca": {"lat": 5.0, "lon": -74.0},
        "Guainía": {"lat": 2.6, "lon": -68.5}, "Guaviare": {"lat": 2.0, "lon": -72.6},
        "Huila": {"lat": 2.5, "lon": -75.5}, "La Guajira": {"lat": 11.4, "lon": -72.4},
        "Magdalena": {"lat": 10.0, "lon": -74.0}, "Meta": {"lat": 3.5, "lon": -73.0},
        "Nariño": {"lat": 1.6, "lon": -77.9}, "Norte de Santander": {"lat": 7.9, "lon": -72.5},
        "Putumayo": {"lat": 0.8, "lon": -76.0}, "Quindío": {"lat": 4.5, "lon": -75.7},
        "Risaralda": {"lat": 5.0, "lon": -75.9}, "San Andrés": {"lat": 12.5, "lon": -81.7},
        "Santander": {"lat": 6.9, "lon": -73.1}, "Sucre": {"lat": 9.0, "lon": -75.4},
        "Tolima": {"lat": 3.9, "lon": -75.2}, "Valle del Cauca": {"lat": 3.8, "lon": -76.5},
        "Vaupés": {"lat": 1.2, "lon": -70.2}, "Vichada": {"lat": 5.0, "lon": -69.0},
        "Bogotá D.C.": {"lat": 4.7, "lon": -74.1},
    }


def fmt_moneda(v):
    if v >= 1_000_000_000: return f"${v/1_000_000_000:,.1f}B"
    elif v >= 1_000_000: return f"${v/1_000_000:,.0f}M"
    else: return f"${v:,.0f}"

def color_riesgo(nivel):
    return {"Alto": "#e74c3c", "Medio": "#f39c12", "Bajo": "#27ae60"}.get(nivel, "#888")

def color_calidad(score):
    if score >= 75: return "#27ae60"
    elif score >= 50: return "#f39c12"
    else: return "#e74c3c"


# ─────────────────────────────────────────────
# CARGAR DATOS
# ─────────────────────────────────────────────
df = generar_datos(n=600)

# ─────────────────────────────────────────────
# SIDEBAR - NAVEGACIÓN Y FILTROS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏥 NAVEGACIÓN")
    page = st.radio(
        "",
        ["📊 Dashboard General", "🔍 Análisis Detallado", "🏢 Proveedores", "📈 Calidad de Datos", "ℹ️ Ayuda"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🔍 Filtros de búsqueda")
    anios = sorted(df["anio"].unique())
    col_anio1, col_anio2 = st.columns(2)
    with col_anio1:
        anio_inicio = st.selectbox("📅 Año Inicio", anios, index=0)
    with col_anio2:
        anio_fin = st.selectbox("📅 Año Fin", anios, index=len(anios)-1)
    periodo = (anio_inicio, anio_fin)
    depts = ["Todos"] + sorted(df["departamento"].unique().tolist())
    dept_sel = st.selectbox("📍 Departamento", depts, index=0)
    mods = ["Todas"] + sorted(df["modalidad"].unique().tolist())
    mod_sel = st.selectbox("📋 Modalidad", mods, index=0)
    niveles = ["Todos", "Alto", "Medio", "Bajo"]
    nivel_sel = st.selectbox("⚠️ Nivel de Riesgo", niveles, index=0)
    calidades = ["Todas", "Alta", "Media", "Baja"]
    calidad_sel = st.selectbox("📊 Calidad de Datos", calidades, index=0)

    st.markdown("---")
    st.markdown("### 📊 Resumen Rápido")
    st.metric("Total Contratos", f"{len(df):,}")
    st.metric("Alertas Totales", f"{len(df[df['score_riesgo'] >= 40]):,}")
    st.metric("Riesgo Alto", f"{len(df[df['nivel_riesgo'] == 'Alto']):,}")

    st.markdown("---")
    st.markdown("<div style='text-align:center;color:#888;font-size:0.75rem;'>Prototipo MVP v3.0<br>Con navegación mejorada<br>3% contratos priorizados</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# APLICAR FILTROS
# ─────────────────────────────────────────────
df_f = df[(df["anio"] >= periodo[0]) & (df["anio"] <= periodo[1])].copy()
if dept_sel != "Todos":
    df_f = df_f[df_f["departamento"] == dept_sel]
if mod_sel != "Todas":
    df_f = df_f[df_f["modalidad"] == mod_sel]
if nivel_sel != "Todos":
    df_f = df_f[df_f["nivel_riesgo"] == nivel_sel]
if calidad_sel != "Todas":
    if calidad_sel == "Alta":
        df_f = df_f[df_f["calidad_datos"] >= 75]
    elif calidad_sel == "Media":
        df_f = df_f[(df_f["calidad_datos"] >= 50) & (df_f["calidad_datos"] < 75)]
    elif calidad_sel == "Baja":
        df_f = df_f[df_f["calidad_datos"] < 50]

# Calcular métricas generales
total_c = len(df_f)
total_alertas = len(df_f[df_f["score_riesgo"] >= 40])
r_alto = len(df_f[df_f["nivel_riesgo"] == "Alto"])
pct_directa = (len(df_f[df_f["modalidad"] == "Contratación Directa"]) / max(total_c, 1) * 100)
ahorro = df_f[df_f["nivel_riesgo"] == "Alto"]["valor"].sum() * 0.12

# Calcular comparación con promedio nacional
pct_alto_filtrado = (r_alto / max(total_c, 1)) * 100
pct_alto_nacional = (len(df[df["nivel_riesgo"] == "Alto"]) / len(df)) * 100
diferencia_pp = pct_alto_filtrado - pct_alto_nacional

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(
    '<div class="main-header">'
    '<h1>🏥 RADAR DE ALERTAS – CONTRATACIÓN EN SALUD (SECOP)</h1>'
    '<p>Sistema de alertas tempranas para contratación pública · Vista Auditor</p>'
    '</div>',
    unsafe_allow_html=True)


# ═════════════════════════════════════════════
# PÁGINA 1: DASHBOARD GENERAL
# ═════════════════════════════════════════════
if page == "📊 Dashboard General":
    st.markdown('<div class="page-title">📊 Dashboard General</div>', unsafe_allow_html=True)

    # KPIs principales
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-label">Contratos Analizados</div><div class="kpi-value">{total_c:,}</div><div class="kpi-delta">Filtros aplicados</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card warning"><div class="kpi-label">Alertas Generadas</div><div class="kpi-value">{total_alertas:,}</div><div class="kpi-delta">{total_alertas/max(total_c,1)*100:.1f}% del total</div></div>', unsafe_allow_html=True)
    with c3:
        # Determinar símbolo, texto, colores y etiqueta según la diferencia con promedio nacional
        # Umbrales ajustados para mejor análisis
        if diferencia_pp > 5:  # Muy por encima (Rojo intenso - CRÍTICO)
            simbolo = "▲▲"
            etiqueta = "Riesgo Crítico"
            texto_comparacion = f"{abs(diferencia_pp):.1f}pp por encima del promedio"
            color_card = "alert"
            color_valor = "#c0392b"  # rojo oscuro
        elif diferencia_pp > 1:  # Arriba (Naranja - ALTO)
            simbolo = "▲"
            etiqueta = "Riesgo Alto"
            texto_comparacion = f"{abs(diferencia_pp):.1f}pp por encima del promedio"
            color_card = "warning"
            color_valor = "#e67e22"  # naranja
        elif diferencia_pp > -1:  # Rango neutro (-1 a +1pp)
            simbolo = "≈"
            etiqueta = "Riesgo Normal"
            texto_comparacion = "Similar al promedio nacional"
            color_card = "info"
            color_valor = "#3498db"  # azul
        elif diferencia_pp > -5:  # Abajo (Amarillo - MODERADO)
            simbolo = "▼"
            etiqueta = "Riesgo Moderado"
            texto_comparacion = f"{abs(diferencia_pp):.1f}pp por debajo del promedio"
            color_card = ""
            color_valor = "#f39c12"  # amarillo
        else:  # Muy por debajo (Verde - BAJO)
            simbolo = "▼▼"
            etiqueta = "Riesgo Bajo"
            texto_comparacion = f"{abs(diferencia_pp):.1f}pp por debajo del promedio"
            color_card = "success"
            color_valor = "#27ae60"  # verde

        st.markdown(f'<div class="kpi-card {color_card}"><div class="kpi-label">{etiqueta}</div><div class="kpi-value" style="color:{color_valor};">{r_alto} {simbolo}</div><div class="kpi-delta">{texto_comparacion}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card info"><div class="kpi-label">Contratación Directa</div><div class="kpi-value info">{pct_directa:.1f}%</div><div class="kpi-delta">Del total analizado</div></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="kpi-card success"><div class="kpi-label">Ahorro Pot. Auditoría</div><div class="kpi-value success">{fmt_moneda(ahorro)}</div><div class="kpi-delta">Est. 12% sobre riesgo alto</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Mapa y Serie Temporal
    col_mapa, col_temp = st.columns([1, 1])

    with col_mapa:
        st.markdown('<div class="section-title">🗺️ Mapa de Riesgo Contractual</div>', unsafe_allow_html=True)
        coords = get_coords()
        ds = df_f.groupby("departamento").agg(
            total=("id_contrato", "count"),
            alertas=("score_riesgo", lambda x: (x >= 40).sum()),
            alto=("nivel_riesgo", lambda x: (x == "Alto").sum()),
            score_prom=("score_riesgo", "mean"),
            valor_total=("valor", "sum"),
        ).reset_index()
        ds["lat"] = ds["departamento"].map(lambda d: coords.get(d, {}).get("lat", 4.5))
        ds["lon"] = ds["departamento"].map(lambda d: coords.get(d, {}).get("lon", -74.0))
        ds["texto"] = ds.apply(lambda r: f"<b>{r['departamento']}</b><br>Contratos: {r['total']}<br>Alertas: {r['alertas']}<br>Riesgo Alto: {r['alto']}<br>Score Prom: {r['score_prom']:.1f}<br>Valor: {fmt_moneda(r['valor_total'])}", axis=1)

        fig_mapa = go.Figure(go.Scattergeo(
            lat=ds["lat"], lon=ds["lon"], text=ds["texto"], hoverinfo="text",
            marker=dict(
                size=ds["alto"].clip(lower=3) * 2 + 8,
                color=ds["score_prom"],
                colorscale=[[0,"#27ae60"],[0.4,"#f1c40f"],[0.7,"#e67e22"],[1.0,"#e74c3c"]],
                cmin=0, cmax=80,
                colorbar=dict(title=dict(text="Score", font=dict(size=10)), thickness=12, len=0.5),
                line=dict(width=1, color="white"), opacity=0.85,
            ),
        ))
        fig_mapa.update_geos(scope="south america", center=dict(lat=4.5, lon=-74.0), projection_scale=5.5, showland=True, landcolor="#f0f4f8", showocean=True, oceancolor="#dce6f0", showcountries=True, countrycolor="#bdc3c7", showframe=False)
        fig_mapa.update_layout(height=420, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor="rgba(0,0,0,0)", geo=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_mapa, use_container_width=True)

    with col_temp:
        st.markdown('<div class="section-title">📅 Alertas por Mes · Contexto Temporal</div>', unsafe_allow_html=True)

        am = df_f[df_f["score_riesgo"] >= 40].groupby(["anio","mes_num","mes"]).size().reset_index(name="alertas").sort_values(["anio","mes_num"])
        am["periodo"] = am["mes"] + " " + am["anio"].astype(str)
        hm = df_f[df_f["nivel_riesgo"]=="Alto"].groupby(["anio","mes_num","mes"]).size().reset_index(name="alto").sort_values(["anio","mes_num"])
        hm["periodo"] = hm["mes"] + " " + hm["anio"].astype(str)

        fig_t = go.Figure()

        # Sombreados contextuales para períodos críticos
        for anio in am["anio"].unique():
            # Fin de vigencia fiscal (Noviembre-Diciembre)
            nov_idx = am[(am["anio"]==anio) & (am["mes_num"]==11)]
            dic_idx = am[(am["anio"]==anio) & (am["mes_num"]==12)]
            if not nov_idx.empty:
                x0 = nov_idx["periodo"].values[0]
                x1 = dic_idx["periodo"].values[0] if not dic_idx.empty else nov_idx["periodo"].values[0]
                fig_t.add_vrect(
                    x0=x0, x1=x1,
                    fillcolor="rgba(241,196,15,0.15)", line_width=0,
                    annotation_text="Cierre fiscal" if anio == am["anio"].min() else "",
                    annotation_position="top left",
                    annotation=dict(font=dict(size=9, color="#b7950b")),
                )

            # Período pre-electoral 2023 (Agosto-Octubre)
            if anio == 2023:
                oct_idx = am[(am["anio"]==2023) & (am["mes_num"].isin([8,9,10]))]
                if not oct_idx.empty:
                    fig_t.add_vrect(
                        x0=oct_idx["periodo"].values[0],
                        x1=oct_idx["periodo"].values[-1],
                        fillcolor="rgba(231,76,60,0.1)", line_width=0,
                        annotation_text="Pre-electoral",
                        annotation_position="top left",
                        annotation=dict(font=dict(size=9, color="#c0392b")),
                    )

            # Período electoral 2024 (Mayo-Junio)
            if anio == 2024:
                may_idx = am[(am["anio"]==2024) & (am["mes_num"].isin([5,6]))]
                if not may_idx.empty:
                    fig_t.add_vrect(
                        x0=may_idx["periodo"].values[0],
                        x1=may_idx["periodo"].values[-1],
                        fillcolor="rgba(155,89,182,0.1)", line_width=0,
                        annotation_text="Electoral",
                        annotation_position="top left",
                        annotation=dict(font=dict(size=9, color="#8e44ad")),
                    )

        # Líneas de datos
        fig_t.add_trace(go.Scatter(x=am["periodo"], y=am["alertas"], mode="lines+markers", name="Total Alertas", line=dict(color="#2c4a7c", width=2.5), marker=dict(size=7), fill="tozeroy", fillcolor="rgba(44,74,124,0.1)"))
        fig_t.add_trace(go.Scatter(x=hm["periodo"], y=hm["alto"], mode="lines+markers", name="Riesgo Alto", line=dict(color="#e74c3c", width=2, dash="dot"), marker=dict(size=6, symbol="diamond")))

        fig_t.update_layout(
            height=420, margin=dict(l=20,r=20,t=30,b=60),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickangle=-45, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor="#eef2f7", title=dict(text="Cantidad", font=dict(size=11))),
            legend=dict(orientation="h", y=1.02, xanchor="right", x=1, font=dict(size=11)),
            hovermode="x unified",
        )
        st.plotly_chart(fig_t, use_container_width=True)

    # Distribución por Modalidad
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Distribución por Modalidad de Contratación</div>', unsafe_allow_html=True)

    md = df_f.groupby("modalidad").agg(
        contratos=("id_contrato","count"),
        alto=("nivel_riesgo", lambda x: (x=="Alto").sum()),
    ).reset_index().sort_values("contratos", ascending=False)

    fig_m = go.Figure()
    fig_m.add_trace(go.Bar(x=md["modalidad"], y=md["contratos"], name="Total", marker_color="#2c4a7c", opacity=0.7))
    fig_m.add_trace(go.Bar(x=md["modalidad"], y=md["alto"], name="Riesgo Alto", marker_color="#e74c3c"))
    fig_m.update_layout(
        height=320, margin=dict(l=20,r=20,t=20,b=80),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        barmode="overlay",
        xaxis=dict(tickangle=-25, tickfont=dict(size=10)),
        yaxis=dict(showgrid=True, gridcolor="#eef2f7"),
        legend=dict(orientation="h", y=1.05, x=0.5, xanchor="center", font=dict(size=11)),
    )
    st.plotly_chart(fig_m, use_container_width=True)

    # Tabla de contratos priorizados
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Top 20 Contratos Priorizados</div>', unsafe_allow_html=True)
    df_top = df_f.sort_values("score_riesgo", ascending=False).head(20).reset_index(drop=True)
    df_disp = df_top[["id_contrato","entidad","departamento","modalidad","valor","nivel_riesgo","score_riesgo"]].copy()
    df_disp["valor"] = df_disp["valor"].apply(fmt_moneda)
    df_disp["score_riesgo"] = df_disp["score_riesgo"].apply(lambda x: f"{x:.1f}%")
    df_disp.columns = ["ID","Entidad","Departamento","Modalidad","Valor","Riesgo","Score"]
    st.dataframe(df_disp, use_container_width=True, height=400, hide_index=True)


# ═════════════════════════════════════════════
# PÁGINA 2: ANÁLISIS DETALLADO
# ═════════════════════════════════════════════
elif page == "🔍 Análisis Detallado":
    st.markdown('<div class="page-title">🔍 Análisis Detallado de Contratos</div>', unsafe_allow_html=True)

    df_top = df_f.sort_values("score_riesgo", ascending=False).head(50).reset_index(drop=True)

    if len(df_top) == 0:
        st.warning("No hay contratos que cumplan con los filtros seleccionados.")
    else:
        ids = df_top["id_contrato"].tolist()
        sel = st.selectbox("🔎 Selecciona un contrato para ver el detalle completo:", ids, index=0)

        if sel:
            c = df_top[df_top["id_contrato"] == sel].iloc[0]

            # Información general del contrato
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(
                    f'<div class="explanation-panel">'
                    f'<h3 style="color:#1a2a4a;margin-top:0;">📄 {c["id_contrato"]}</h3>'
                    f'<p><strong>🏛️ Entidad:</strong> {c["entidad"]}</p>'
                    f'<p><strong>📍 Departamento:</strong> {c["departamento"]}</p>'
                    f'<p><strong>📋 Modalidad:</strong> {c["modalidad"]}</p>'
                    f'<p><strong>📝 Objeto:</strong> {c["objeto"]}</p>'
                    f'<p><strong>💰 Valor:</strong> {fmt_moneda(c["valor"])}</p>'
                    f'<p><strong>📊 Valor Prom. Histórico:</strong> {fmt_moneda(c["valor_promedio_historico"])}</p>'
                    f'<p><strong>👥 No. Oferentes:</strong> {c["num_oferentes"]}</p>'
                    f'<p><strong>🏢 Proveedor:</strong> {c["proveedor_id"]}</p>'
                    f'<p><strong>📅 Contratos previos:</strong> {c["contratos_previos_proveedor"]}</p>'
                    f'</div>', unsafe_allow_html=True)

            with col2:
                # Gauge de riesgo
                sv = c["score_riesgo"]
                nc = color_riesgo(c["nivel_riesgo"])
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number", value=sv,
                    number=dict(suffix="%", font=dict(size=32)),
                    title=dict(text="Score de Riesgo", font=dict(size=16)),
                    gauge=dict(
                        axis=dict(range=[0,100]),
                        bar=dict(color=nc), bgcolor="white",
                        steps=[dict(range=[0,40], color="#e8f5e9"), dict(range=[40,70], color="#fff3e0"), dict(range=[70,100], color="#ffebee")],
                        threshold=dict(line=dict(color="black", width=2), thickness=0.75, value=sv),
                    ),
                ))
                fig_g.update_layout(height=250, margin=dict(l=30,r=30,t=60,b=10), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_g, use_container_width=True)

            # Señales detectadas
            st.markdown("### 🚨 Señales de Alerta Detectadas")
            sobreprecio = (c["valor"] - c["valor_promedio_historico"]) / max(c["valor_promedio_historico"], 1) * 100
            alertas = []
            if sobreprecio > 50:
                alertas.append(("🔴", f"Valor {sobreprecio:.0f}% superior al promedio histórico"))
            if c["contratos_previos_proveedor"] >= 5:
                alertas.append(("🟠", f"Proveedor recurrente ({c['contratos_previos_proveedor']} contratos previos)"))
            if c["modalidad"] == "Contratación Directa":
                alertas.append(("🟠", "Contratación directa sin competencia"))
            if c["num_oferentes"] <= 2:
                alertas.append(("🟡", f"Baja competencia ({c['num_oferentes']} oferentes)"))
            if sobreprecio > 100:
                alertas.append(("🔴", "Incremento no explicado por inflación"))

            if alertas:
                cols = st.columns(len(alertas))
                for idx, (emoji, texto) in enumerate(alertas):
                    with cols[idx]:
                        st.markdown(f"<div style='text-align:center;padding:1rem;background:#fff3cd;border-radius:8px;'><h2>{emoji}</h2><p style='margin:0;'>{texto}</p></div>", unsafe_allow_html=True)
            else:
                st.info("✅ No se detectaron señales de alerta significativas en este contrato.")

            # Factores de riesgo
            st.markdown("### 📊 Factores de Riesgo (Contribución al Score)")
            fd = pd.DataFrame({
                "Factor": ["Frecuencia Proveedor", "Valor vs Histórico", "Nº Oferentes", "Modalidad Directa", "Variables Macro"],
                "Peso": [c["factor_freq_proveedor"], c["factor_valor_historico"], c["factor_num_oferentes"], c["factor_modalidad_directa"], c["factor_variables_macro"]],
            }).sort_values("Peso", ascending=True)

            fig_f = go.Figure(go.Bar(
                y=fd["Factor"], x=fd["Peso"], orientation="h",
                marker=dict(color=["#2c4a7c","#e74c3c","#f39c12","#27ae60","#e67e22"]),
                text=fd["Peso"].apply(lambda x: f"{x:.1f}%"), textposition="outside",
                textfont=dict(size=13, color="#1a2a4a"),
            ))
            fig_f.update_layout(
                height=300, margin=dict(l=10,r=60,t=10,b=10),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#eef2f7", range=[0, max(fd["Peso"])*1.3], title=dict(text="Contribución (%)", font=dict(size=12))),
                yaxis=dict(showgrid=False, tickfont=dict(size=12)), showlegend=False,
            )
            st.plotly_chart(fig_f, use_container_width=True)

            # Comparación con pares
            st.markdown("### 📊 Comparación con Contratos Similares")
            pares = df[(df["tipo_entidad"] == c["tipo_entidad"]) & (df["modalidad"] == c["modalidad"])]
            if len(pares) > 5:
                stats_pares = {
                    "Promedio": pares["valor"].mean(),
                    "Mediana": pares["valor"].median(),
                    "P75": pares["valor"].quantile(0.75),
                    "P95": pares["valor"].quantile(0.95),
                    "Este contrato": c["valor"],
                }

                es_extremo = c["valor"] > pares["valor"].quantile(0.95)
                colores_pares = ["#bdc3c7", "#95a5a6", "#7f8c8d", "#f39c12", "#e74c3c" if es_extremo else "#2c4a7c"]

                fig_p = go.Figure(go.Bar(
                    x=list(stats_pares.keys()),
                    y=list(stats_pares.values()),
                    marker=dict(color=colores_pares),
                    text=[fmt_moneda(v) for v in stats_pares.values()],
                    textposition="outside", textfont=dict(size=11),
                ))
                fig_p.update_layout(
                    height=350, margin=dict(l=10,r=10,t=10,b=60),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(tickangle=-25, tickfont=dict(size=10)),
                    yaxis=dict(showgrid=True, gridcolor="#eef2f7", title=dict(text="Valor ($)", font=dict(size=11))),
                    showlegend=False,
                )
                st.plotly_chart(fig_p, use_container_width=True)

                ratio = c["valor"] / max(pares["valor"].median(), 1)
                if ratio > 2:
                    st.error(f"⚠️ Este contrato vale **{ratio:.1f}x** la mediana de contratos similares ({c['tipo_entidad']}, {c['modalidad']})")
                elif ratio > 1.3:
                    st.warning(f"📊 **{((ratio-1)*100):.0f}%** por encima de la mediana de sus pares")
                else:
                    st.success("✅ Valor dentro del rango esperado para contratos similares")
            else:
                st.info("Insuficientes pares para comparación (mín. 5 contratos similares)")


# ═════════════════════════════════════════════
# PÁGINA 3: PROVEEDORES
# ═════════════════════════════════════════════
elif page == "🏢 Proveedores":
    st.markdown('<div class="page-title">🏢 Análisis de Proveedores</div>', unsafe_allow_html=True)

    # Top proveedores por riesgo
    st.markdown("### 🔝 Proveedores con Mayor Score de Riesgo Promedio")

    prov_stats = df_f.groupby("proveedor_id").agg(
        n_contratos=("id_contrato", "count"),
        score_promedio=("score_riesgo", "mean"),
        valor_total=("valor", "sum"),
        n_entidades=("entidad", "nunique"),
        n_departamentos=("departamento", "nunique"),
        alto_riesgo=("nivel_riesgo", lambda x: (x=="Alto").sum())
    ).reset_index()

    prov_stats = prov_stats[prov_stats["n_contratos"] >= 3].sort_values("score_promedio", ascending=False).head(20)

    col1, col2 = st.columns([1, 1])

    with col1:
        fig_prov = go.Figure(go.Bar(
            x=prov_stats["proveedor_id"],
            y=prov_stats["score_promedio"],
            marker=dict(color=prov_stats["score_promedio"], colorscale="Reds"),
            text=prov_stats["score_promedio"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside"
        ))
        fig_prov.update_layout(
            title="Score Promedio por Proveedor",
            height=400,
            xaxis=dict(tickangle=-45),
            yaxis=dict(title="Score Promedio"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_prov, use_container_width=True)

    with col2:
        fig_contratos = go.Figure(go.Scatter(
            x=prov_stats["n_contratos"],
            y=prov_stats["score_promedio"],
            mode='markers',
            marker=dict(
                size=prov_stats["valor_total"] / 1_000_000,
                color=prov_stats["alto_riesgo"],
                colorscale="Reds",
                showscale=True,
                colorbar=dict(title="Contratos<br>Alto Riesgo")
            ),
            text=prov_stats["proveedor_id"],
            hovertemplate="<b>%{text}</b><br>Contratos: %{x}<br>Score: %{y:.1f}%<extra></extra>"
        ))
        fig_contratos.update_layout(
            title="Contratos vs Riesgo (tamaño = valor total)",
            height=400,
            xaxis=dict(title="Número de Contratos"),
            yaxis=dict(title="Score Promedio"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_contratos, use_container_width=True)

    # Tabla detallada
    st.markdown("### 📋 Tabla Detallada de Proveedores")
    df_prov_display = prov_stats.copy()
    df_prov_display["valor_total"] = df_prov_display["valor_total"].apply(fmt_moneda)
    df_prov_display["score_promedio"] = df_prov_display["score_promedio"].apply(lambda x: f"{x:.1f}%")
    df_prov_display.columns = ["Proveedor", "Contratos", "Score Prom.", "Valor Total", "Entidades", "Departamentos", "Alto Riesgo"]
    st.dataframe(df_prov_display, use_container_width=True, height=400, hide_index=True)

    # Detalle de proveedor específico
    st.markdown("---")
    st.markdown("### 🔍 Detalle de Proveedor Específico")
    prov_sel = st.selectbox("Selecciona un proveedor:", prov_stats["proveedor_id"].tolist())

    if prov_sel:
        contratos_prov = df[df["proveedor_id"] == prov_sel]
        n_entidades = contratos_prov["entidad"].nunique()
        n_contratos = len(contratos_prov)
        valor_total = contratos_prov["valor"].sum()
        n_dptos = contratos_prov["departamento"].nunique()
        score_prom_prov = contratos_prov["score_riesgo"].mean()

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Contratos", n_contratos)
        with col2:
            st.metric("Entidades", n_entidades)
        with col3:
            st.metric("Departamentos", n_dptos)
        with col4:
            st.metric("Valor Acumulado", fmt_moneda(valor_total))
        with col5:
            st.metric("Score Promedio", f"{score_prom_prov:.1f}%")

        # Distribución por entidad
        st.markdown("#### Distribución de Contratos por Entidad")
        ent_dist = contratos_prov.groupby("entidad").size().reset_index(name="n").sort_values("n", ascending=True).tail(10)
        fig_ent = go.Figure(go.Bar(
            y=ent_dist["entidad"],
            x=ent_dist["n"],
            orientation="h",
            marker=dict(color="#2c4a7c"),
            text=ent_dist["n"],
            textposition="outside"
        ))
        fig_ent.update_layout(
            height=300,
            xaxis=dict(title="Número de Contratos"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_ent, use_container_width=True)


# ═════════════════════════════════════════════
# PÁGINA 4: CALIDAD DE DATOS
# ═════════════════════════════════════════════
elif page == "📈 Calidad de Datos":
    st.markdown('<div class="page-title">📈 Índice de Calidad de Datos</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <h4 style="margin-top:0;">ℹ️ Sobre el Índice de Calidad</h4>
    <p>El índice de calidad evalúa la fiabilidad de los datos de contratación en 4 dimensiones:</p>
    <ul>
        <li><strong>Completitud (30%):</strong> Porcentaje de campos obligatorios con información</li>
        <li><strong>Consistencia (25%):</strong> Coherencia entre campos relacionados</li>
        <li><strong>Oportunidad (25%):</strong> Tiempo entre firma y publicación del contrato</li>
        <li><strong>Estandarización (20%):</strong> Uso de formatos y códigos estándar</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # Calidad promedio por entidad
    st.markdown("### 🏛️ Calidad de Datos por Entidad")

    calidad_entidad = df_f.groupby("entidad").agg(
        cal_global=("calidad_datos", "mean"),
        cal_comp=("calidad_completitud", "mean"),
        cal_cons=("calidad_consistencia", "mean"),
        cal_opor=("calidad_oportunidad", "mean"),
        cal_est=("calidad_estandarizacion", "mean"),
        n_contratos=("id_contrato", "count")
    ).reset_index()

    calidad_entidad = calidad_entidad[calidad_entidad["n_contratos"] >= 3].sort_values("cal_global", ascending=True).tail(20)

    col1, col2 = st.columns([1, 1])

    with col1:
        fig_cal_ent = go.Figure(go.Bar(
            y=calidad_entidad["entidad"],
            x=calidad_entidad["cal_global"],
            orientation="h",
            marker=dict(color=calidad_entidad["cal_global"].apply(color_calidad)),
            text=calidad_entidad["cal_global"].apply(lambda x: f"{x:.1f}"),
            textposition="outside"
        ))
        fig_cal_ent.update_layout(
            title="Índice Global de Calidad por Entidad",
            height=500,
            xaxis=dict(title="Índice de Calidad", range=[0, 110]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_cal_ent, use_container_width=True)

    with col2:
        # Distribución general
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=df_f["calidad_datos"],
            nbinsx=20,
            marker=dict(color="#2c4a7c"),
            name="Frecuencia"
        ))
        fig_dist.update_layout(
            title="Distribución del Índice de Calidad",
            height=500,
            xaxis=dict(title="Índice de Calidad"),
            yaxis=dict(title="Frecuencia"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    # Estadísticas generales
    st.markdown("### 📊 Estadísticas Generales de Calidad")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        promedio = df_f["calidad_datos"].mean()
        st.metric("Calidad Promedio", f"{promedio:.1f}/100")
    with col2:
        buenos = len(df_f[df_f["calidad_datos"] >= 75])
        st.metric("Registros Buenos", f"{buenos} ({buenos/len(df_f)*100:.1f}%)")
    with col3:
        medios = len(df_f[(df_f["calidad_datos"] >= 50) & (df_f["calidad_datos"] < 75)])
        st.metric("Registros Medios", f"{medios} ({medios/len(df_f)*100:.1f}%)")
    with col4:
        malos = len(df_f[df_f["calidad_datos"] < 50])
        st.metric("Registros Deficientes", f"{malos} ({malos/len(df_f)*100:.1f}%)")

    # Dimensiones de calidad
    st.markdown("### 📐 Promedio por Dimensión")
    dims = {
        "Completitud": df_f["calidad_completitud"].mean(),
        "Consistencia": df_f["calidad_consistencia"].mean(),
        "Oportunidad": df_f["calidad_oportunidad"].mean(),
        "Estandarización": df_f["calidad_estandarizacion"].mean()
    }

    fig_dims = go.Figure(go.Bar(
        x=list(dims.keys()),
        y=list(dims.values()),
        marker=dict(color=[color_calidad(v) for v in dims.values()]),
        text=[f"{v:.1f}" for v in dims.values()],
        textposition="outside"
    ))
    fig_dims.update_layout(
        height=350,
        yaxis=dict(title="Score Promedio", range=[0, 110]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_dims, use_container_width=True)


# ═════════════════════════════════════════════
# PÁGINA 5: AYUDA
# ═════════════════════════════════════════════
elif page == "ℹ️ Ayuda":
    st.markdown('<div class="page-title">ℹ️ Guía de Uso del Sistema</div>', unsafe_allow_html=True)

    st.markdown("""
    ## 📘 Bienvenido al Radar de Alertas de Contratación en Salud

    ### 🎯 Objetivo del Sistema
    Este dashboard ha sido diseñado para identificar y priorizar contratos de salud pública que presenten
    indicadores de riesgo, facilitando labores de auditoría y control.

    ### 🧭 Navegación

    #### 📊 Dashboard General
    - **Vista panorámica** de todos los contratos analizados
    - **KPIs principales**: contratos analizados, alertas generadas, niveles de riesgo
    - **Mapa interactivo**: distribución geográfica de alertas
    - **Serie temporal**: evolución de alertas en el tiempo
    - **Tabla priorizada**: top 20 contratos con mayor score de riesgo

    #### 🔍 Análisis Detallado
    - **Exploración individual** de cada contrato
    - **Score de riesgo** con indicador gauge
    - **Señales de alerta** detectadas automáticamente
    - **Factores de riesgo** que contribuyen al score
    - **Comparación con pares** de contratos similares

    #### 🏢 Proveedores
    - **Análisis de proveedores** con mayor actividad
    - **Score promedio** por proveedor
    - **Distribución de contratos** entre entidades
    - **Identificación de patrones** de concentración

    #### 📈 Calidad de Datos
    - **Índice de calidad** de la información reportada
    - **4 dimensiones evaluadas**: completitud, consistencia, oportunidad, estandarización
    - **Ranking de entidades** por calidad de reporte
    - **Estadísticas generales** del sistema

    ### 🔍 Filtros Disponibles

    Utiliza los filtros en la barra lateral para refinar tu análisis:

    - **📅 Período**: Rango de años a analizar
    - **📍 Departamento**: Limitar a una región específica
    - **📋 Modalidad**: Tipo de contratación (directa, licitación, etc.)
    - **⚠️ Nivel de Riesgo**: Alto, Medio, Bajo o Todos

    ### 📊 Interpretación del Score de Riesgo

    El score de riesgo (0-100%) se calcula mediante algoritmo que evalúa:

    - 🔴 **70-100% (Alto)**: Revisión prioritaria, múltiples señales de alerta
    - 🟠 **40-70% (Medio)**: Revisión recomendada, algunas señales
    - 🟢 **0-40% (Bajo)**: Dentro de parámetros normales

    ### 🚨 Señales de Alerta Comunes

    - **Sobreprecio**: Valor significativamente superior al histórico
    - **Proveedor recurrente**: Alta concentración en misma entidad
    - **Contratación directa**: Sin proceso competitivo
    - **Baja competencia**: Pocos oferentes en el proceso
    - **Variación no explicada**: Incrementos sin justificación

    ### 💡 Recomendaciones de Uso

    1. **Inicio**: Comienza en el Dashboard General para visión general
    2. **Priorización**: Identifica contratos de alto riesgo en la tabla
    3. **Profundización**: Usa Análisis Detallado para casos específicos
    4. **Patrones**: Revisa Proveedores para detectar concentraciones
    5. **Validación**: Verifica Calidad de Datos antes de conclusiones

    ### 📞 Soporte Técnico

    Para reportar errores o solicitar funcionalidades:
    - 📧 Email: soporte@alertasalud.gov.co
    - 📱 Teléfono: +57 (1) 234-5678

    ### 📌 Versión

    **MVP v3.0** - Dashboard con navegación mejorada y secciones organizadas

    ---

    <div style='background:#fff3cd;padding:1rem;border-radius:8px;'>
    ⚠️ <strong>Nota Importante:</strong> Este es un prototipo con datos simulados para fines de demostración.
    Los scores y alertas no representan situaciones reales de contratación.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#aaa; font-size:0.8rem; padding:1rem 0;">'
    '<strong>Alerta Salud Abierta</strong> · Sistema de Alertas Tempranas para Contratación en Salud<br>'
    'Prototipo MVP v3.0 con navegación mejorada · Universidad Javeriana 2025'
    '</div>', unsafe_allow_html=True)
