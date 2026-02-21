import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import kagglehub
import os

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="E-commerce Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CUSTOM CSS  —  Dark industrial theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

:root {
    --bg:      #0d0f14;
    --surface: #161921;
    --border:  #252934;
    --accent1: #f0a500;
    --accent2: #3ecfcf;
    --accent3: #e05c5c;
    --txt:     #dde3f0;
    --muted:   #6b7280;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--txt);
    font-family: 'DM Mono', monospace;
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--txt) !important; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.kpi-grid { display:flex; gap:16px; flex-wrap:wrap; margin-bottom:24px; }
.kpi-card {
    flex:1; min-width:160px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 22px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content:''; position:absolute; top:0; left:0;
    width:4px; height:100%;
    background: var(--accent-color, var(--accent1));
}
.kpi-label { font-size:11px; text-transform:uppercase; letter-spacing:2px; color:var(--muted); margin-bottom:8px; }
.kpi-value { font-family:'Syne',sans-serif; font-size:28px; font-weight:800; color:var(--accent-color, var(--accent1)); }
.kpi-sub   { font-size:11px; color:var(--muted); margin-top:4px; }

.section-title {
    font-family:'Syne',sans-serif;
    font-size:13px; font-weight:700;
    text-transform:uppercase; letter-spacing:3px;
    color:var(--muted);
    border-bottom:1px solid var(--border);
    padding-bottom:8px; margin:28px 0 18px;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap:8px; background:transparent;
    border-bottom:1px solid var(--border);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background:transparent !important;
    color:var(--muted) !important;
    font-family:'Syne',sans-serif;
    font-size:14px; font-weight:600;
    border-radius:6px 6px 0 0; padding:10px 24px;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background:var(--surface) !important;
    color:var(--accent1) !important;
    border-bottom:2px solid var(--accent1) !important;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────
@st.cache_data(show_spinner="Baixando dataset do Kaggle…")
def load_data():
    path = kagglehub.dataset_download("sharmajicoder/e-commerce-sales-dataset")
    files = os.listdir(path)
    csv_file = [f for f in files if f.endswith(".csv")][0]
    df = pd.read_csv(os.path.join(path, csv_file))
    df1 = df.copy().reset_index(drop=True)

    df1['order_date']    = pd.to_datetime(df1['order_date'])
    df1['ship_date']     = pd.to_datetime(df1['ship_date'])
    df1['delivery_date'] = pd.to_datetime(df1['delivery_date'])

    df1['faturamento_bruto']  = df1['quantity'] * df1['unit_price']
    df1['diferenca_absoluta'] = df1['faturamento_bruto'] - df1['total_sales']
    df1['percentual_perda']   = (df1['diferenca_absoluta'] / df1['faturamento_bruto']) * 100

    df1['dias_processamento'] = (df1['ship_date']     - df1['order_date']).dt.days.abs()
    df1['dias_transito']      = (df1['delivery_date'] - df1['ship_date']).dt.days.abs()
    df1['lead_time_total']    = (df1['delivery_date'] - df1['order_date']).dt.days.abs()

    bins   = [-0.01, 0.05, 0.10, 0.20, 0.30, 1.0]
    labels = ['0-5%', '6-10%', '11-20%', '21-30%', '>30%']
    df1['faixa_desconto'] = pd.cut(df1['discount'], bins=bins, labels=labels)

    return df1

df1 = load_data()

# ──────────────────────────────────────────────
# THEME HELPERS
# ──────────────────────────────────────────────
PALETTE = ['#f0a500', '#3ecfcf', '#e05c5c', '#7c6af5', '#5cd98d', '#f07090']
BG      = '#0d0f14'
SURFACE = '#161921'
BORDER  = '#252934'
TEXT    = '#dde3f0'
MUTED   = '#6b7280'


def base_layout(
    height=400,
    title='',
    margin=None,        # pass dict(l=..,r=..,t=..,b=..) to override default
    legend=None,        # pass dict(...) to include legend in layout
    annotations=None,
    **extra,            # any other plotly layout kwargs
):
    """
    Builds a plotly update_layout() dict.
    All conflicting keys (margin, legend, annotations) are handled as
    optional parameters here — never passed twice.
    """
    d = dict(
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(family='DM Mono, monospace', color=TEXT, size=12),
        colorway=PALETTE,
        height=height,
    )

    # margin: use custom if provided, else sensible default
    d['margin'] = margin if margin is not None else dict(l=40, r=20, t=50 if title else 30, b=40)

    # title
    if title:
        d['title'] = dict(text=title, font=dict(color=TEXT, size=14))

    # legend — only added when explicitly requested
    if legend is not None:
        base_leg = dict(bgcolor='rgba(0,0,0,0)', bordercolor=BORDER, font=dict(size=11))
        base_leg.update(legend)
        d['legend'] = base_leg

    # annotations
    if annotations is not None:
        d['annotations'] = annotations

    # any other kwargs (barmode, showlegend, etc.)
    d.update(extra)

    return d


def style_axes(fig):
    ax_style = dict(
        gridcolor=BORDER, linecolor=BORDER, zerolinecolor=BORDER,
        tickfont=dict(color=MUTED, size=11),
        title_font=dict(color=MUTED, size=11),
    )
    for ax in ['xaxis', 'yaxis', 'xaxis2', 'yaxis2']:
        if hasattr(fig.layout, ax):
            getattr(fig.layout, ax).update(ax_style)
    return fig


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📦 E-commerce\n### Sales Analytics")
    st.markdown("---")

    selected_categories = st.multiselect(
        "Categorias",
        options=df1['category'].unique().tolist(),
        default=df1['category'].unique().tolist(),
    )
    selected_payment = st.multiselect(
        "Método de Pagamento",
        options=df1['payment_method'].unique().tolist(),
        default=df1['payment_method'].unique().tolist(),
    )
    selected_status = st.multiselect(
        "Status do Pedido",
        options=df1['order_status'].unique().tolist(),
        default=df1['order_status'].unique().tolist(),
    )
    st.markdown("---")
    st.caption("Dataset: Amazon Sales • 10 000 linhas • Jan–Fev 2026")

# Filtro global
mask = (
    df1['category'].isin(selected_categories) &
    df1['payment_method'].isin(selected_payment) &
    df1['order_status'].isin(selected_status)
)
df = df1[mask].copy()

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.markdown("""
<div style="padding:28px 0 8px;">
  <h1 style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;
             background:linear-gradient(90deg,#f0a500,#3ecfcf);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;">
    E-COMMERCE SALES DASHBOARD
  </h1>
  <p style="color:#6b7280;font-size:13px;margin:6px 0 0;letter-spacing:1px;">
    EXPLORATORY DATA ANALYSIS  ·  HEALTH CHECK  ·  EFICIÊNCIA LOGÍSTICA
  </p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# GLOBAL KPIs
# ──────────────────────────────────────────────
total_rev    = df['total_sales'].sum()
total_bruto  = df['faturamento_bruto'].sum()
total_orders = len(df)
avg_discount = df['discount'].mean()
avg_ship     = df['shipping_cost'].mean()
avg_lead     = df['lead_time_total'].mean()

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card" style="--accent-color:#f0a500">
    <div class="kpi-label">Faturamento Líquido</div>
    <div class="kpi-value">₹{total_rev/1e6:.1f}M</div>
    <div class="kpi-sub">{total_orders:,} pedidos</div>
  </div>
  <div class="kpi-card" style="--accent-color:#e05c5c">
    <div class="kpi-label">Perda por Desconto</div>
    <div class="kpi-value">₹{(total_bruto-total_rev)/1e6:.1f}M</div>
    <div class="kpi-sub">{((total_bruto-total_rev)/total_bruto*100):.1f}% do bruto</div>
  </div>
  <div class="kpi-card" style="--accent-color:#3ecfcf">
    <div class="kpi-label">Desconto Médio</div>
    <div class="kpi-value">{avg_discount*100:.1f}%</div>
    <div class="kpi-sub">sobre o preço unitário</div>
  </div>
  <div class="kpi-card" style="--accent-color:#7c6af5">
    <div class="kpi-label">Frete Médio</div>
    <div class="kpi-value">₹{avg_ship:.0f}</div>
    <div class="kpi-sub">por pedido</div>
  </div>
  <div class="kpi-card" style="--accent-color:#5cd98d">
    <div class="kpi-label">Lead Time Médio</div>
    <div class="kpi-value">{avg_lead:.1f}d</div>
    <div class="kpi-sub">order → entrega</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────
tab1, tab2 = st.tabs([
    "🩺  Health Check de Vendas",
    "🚚  Eficiência Logística",
])

# ══════════════════════════════════════════════
# TAB 1 — HEALTH CHECK DE VENDAS
# ══════════════════════════════════════════════
with tab1:

    # ── Row 1: Concentração Geográfica & Métodos de Pagamento ──
    col_a, col_b = st.columns([1.5, 1])

    with col_a:
        st.markdown('<p class="section-title">Concentração Geográfica — Top 15 Estados</p>', unsafe_allow_html=True)

        geo = (df.groupby('state')['total_sales']
               .sum().sort_values(ascending=False).head(15).reset_index())
        geo['pct'] = geo['total_sales'] / geo['total_sales'].sum() * 100

        fig_geo = go.Figure(go.Bar(
            x=geo['total_sales'], y=geo['state'], orientation='h',
            marker=dict(color=geo['total_sales'],
                        colorscale=[[0,'#253040'],[1,'#f0a500']], showscale=False),
            text=geo['pct'].map(lambda v: f"{v:.1f}%"),
            textposition='outside', textfont=dict(color=MUTED, size=10),
            hovertemplate='<b>%{y}</b><br>Faturamento: ₹%{x:,.0f}<extra></extra>',
        ))
        fig_geo.update_layout(**base_layout(
            height=420,
            legend=dict(),
            xaxis=dict(tickformat='~s', title='Faturamento (₹)'),
            yaxis=dict(autorange='reversed', title=''),
        ))
        style_axes(fig_geo)
        st.plotly_chart(fig_geo, width='stretch')

    with col_b:
        st.markdown('<p class="section-title">Métodos de Pagamento</p>', unsafe_allow_html=True)

        pay = df.groupby('payment_method').agg(
            receita=('total_sales','sum'), pedidos=('order_id','count')
        ).reset_index()

        fig_pay = make_subplots(
            rows=1, cols=2,
            specs=[[{'type':'pie'},{'type':'pie'}]],
            subplot_titles=['% Receita','% Pedidos'],
        )
        for i, col_name in enumerate(['receita','pedidos'], 1):
            fig_pay.add_trace(go.Pie(
                labels=pay['payment_method'], values=pay[col_name],
                hole=0.55,
                marker=dict(colors=PALETTE, line=dict(color=BG, width=2)),
                textinfo='percent',
                hovertemplate='<b>%{label}</b><br>%{percent}<extra></extra>',
            ), row=1, col=i)

        fig_pay.update_layout(**base_layout(
            height=420,
            showlegend=True,
            legend=dict(orientation='h', y=-0.05, x=0.5, xanchor='center'),
        ))
        for ann in fig_pay.layout.annotations:
            ann.font = dict(color=MUTED, size=11)
        st.plotly_chart(fig_pay, width='stretch')

    # ── Row 2: Impacto dos Descontos ──
    st.markdown('<p class="section-title">Impacto dos Descontos no Faturamento</p>', unsafe_allow_html=True)

    col_c, col_d, col_e = st.columns([1.2, 1, 1])

    with col_c:
        fig_scat = px.scatter(
            df.sample(min(2000, len(df)), random_state=42),
            x='discount', y='total_sales', color='category',
            color_discrete_sequence=PALETTE, opacity=0.55,
            labels={'discount':'Desconto','total_sales':'Faturamento Líquido (₹)'},
            title='Dispersão: Desconto × Faturamento',
            hover_data=['state','payment_method'],
        )
        fig_scat.update_traces(marker=dict(size=5))
        fig_scat.update_layout(**base_layout(height=360, legend=dict()))
        style_axes(fig_scat)
        st.plotly_chart(fig_scat, width='stretch')

    with col_d:
        faixa = df.groupby('faixa_desconto', observed=True).agg(
            fat_medio=('total_sales','mean'), pedidos=('order_id','count')
        ).reset_index()

        fig_faixa = go.Figure([go.Bar(
            x=faixa['faixa_desconto'].astype(str), y=faixa['fat_medio'],
            marker_color=PALETTE[:len(faixa)],
            text=faixa['fat_medio'].map(lambda v: f'₹{v/1e3:.1f}K'),
            textposition='outside', textfont=dict(color=TEXT, size=10),
            hovertemplate='Faixa: %{x}<br>Fat. Médio: ₹%{y:,.0f}<extra></extra>',
        )])
        fig_faixa.update_layout(**base_layout(
            height=360, title='Fat. Médio por Faixa de Desconto',
            legend=dict(),
            xaxis_title='Faixa de Desconto',
            yaxis=dict(tickformat='~s', title='Faturamento Médio (₹)'),
        ))
        style_axes(fig_faixa)
        st.plotly_chart(fig_faixa, width='stretch')

    with col_e:
        pareto = (df.groupby(['sub_category','category'])['total_sales']
                  .sum().sort_values(ascending=False).reset_index())
        pareto['cum_pct'] = pareto['total_sales'].cumsum() / pareto['total_sales'].sum() * 100

        fig_pareto = make_subplots(specs=[[{'secondary_y':True}]])
        fig_pareto.add_trace(go.Bar(
            x=pareto['sub_category'], y=pareto['total_sales'],
            marker_color='#f0a500', name='Faturamento', opacity=0.85,
        ), secondary_y=False)
        fig_pareto.add_trace(go.Scatter(
            x=pareto['sub_category'], y=pareto['cum_pct'],
            mode='lines+markers', name='Acumulado %',
            line=dict(color='#e05c5c', width=2), marker=dict(size=5),
        ), secondary_y=True)
        fig_pareto.add_hline(y=80, secondary_y=True,
                             line_dash='dash', line_color='#f07090', line_width=1.5)
        fig_pareto.update_layout(**base_layout(
            height=360, title='Pareto — Subcategorias',
            legend=dict(orientation='h', y=1.1, x=0),
            xaxis_tickangle=30,
        ))
        fig_pareto.update_yaxes(title_text='Faturamento (₹)', tickformat='~s', secondary_y=False,
                                gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=MUTED))
        fig_pareto.update_yaxes(title_text='Acumulado (%)', range=[0,110], secondary_y=True,
                                gridcolor='rgba(0,0,0,0)', tickfont=dict(color='#e05c5c'))
        fig_pareto.update_xaxes(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=MUTED))
        st.plotly_chart(fig_pareto, width='stretch')

    # ── Row 3: Evolução temporal & Status ──
    col_f, col_g = st.columns([1.6, 1])

    with col_f:
        st.markdown('<p class="section-title">Evolução do Faturamento por Categoria</p>', unsafe_allow_html=True)

        ts = df.copy()
        ts['week'] = ts['order_date'].dt.to_period('W').apply(lambda r: r.start_time)
        ts_grp = ts.groupby(['week','category'])['total_sales'].sum().reset_index()

        fig_ts = px.area(
            ts_grp, x='week', y='total_sales', color='category',
            color_discrete_sequence=PALETTE,
            labels={'total_sales':'Faturamento (₹)','week':'Semana','category':'Categoria'},
        )
        fig_ts.update_traces(line=dict(width=1.5))
        fig_ts.update_layout(**base_layout(height=320, legend=dict()))
        style_axes(fig_ts)
        st.plotly_chart(fig_ts, width='stretch')

    with col_g:
        st.markdown('<p class="section-title">Distribuição por Status do Pedido</p>', unsafe_allow_html=True)

        status_df = df.groupby(['order_status','category'])['total_sales'].sum().reset_index()

        fig_status = px.sunburst(
            status_df, path=['order_status','category'], values='total_sales',
            color='order_status', color_discrete_sequence=PALETTE,
        )
        # margin customizado passado DENTRO de base_layout — sem conflito
        fig_status.update_layout(**base_layout(
            height=320,
            margin=dict(l=0, r=0, t=10, b=0),
        ))
        fig_status.update_traces(textfont_color='white', insidetextorientation='auto')
        st.plotly_chart(fig_status, width='stretch')


# ══════════════════════════════════════════════
# TAB 2 — EFICIÊNCIA LOGÍSTICA
# ══════════════════════════════════════════════
with tab2:

    # ── Row 1: Lead Time & Frete por Estado ──
    col_h, col_i = st.columns(2)

    with col_h:
        st.markdown('<p class="section-title">Lead Time Médio por Estado — Top 20</p>', unsafe_allow_html=True)

        lt = (df.groupby('state')['lead_time_total']
              .mean().sort_values().reset_index()
              .rename(columns={'lead_time_total':'lead_time_medio'}))

        n = min(20, len(lt))
        colors = [f'hsl({int(120 - 120*(i/max(n-1,1)))},70%,45%)' for i in range(n)]

        fig_lt = go.Figure(go.Bar(
            x=lt.head(n)['lead_time_medio'], y=lt.head(n)['state'],
            orientation='h', marker_color=colors,
            text=lt.head(n)['lead_time_medio'].map(lambda v: f'{v:.1f}d'),
            textposition='outside', textfont=dict(color=MUTED, size=10),
            hovertemplate='<b>%{y}</b><br>Lead Time: %{x:.1f} dias<extra></extra>',
        ))
        fig_lt.update_layout(**base_layout(
            height=460, legend=dict(),
            xaxis=dict(title='Dias', gridcolor=BORDER),
            yaxis=dict(autorange='reversed', title=''),
        ))
        style_axes(fig_lt)
        st.plotly_chart(fig_lt, width='stretch')

    with col_i:
        st.markdown('<p class="section-title">Frete Médio por Estado — Top 20 (Mais Caro)</p>', unsafe_allow_html=True)

        fr = (df.groupby('state')['shipping_cost']
              .mean().sort_values(ascending=False).head(20).reset_index()
              .rename(columns={'shipping_cost':'frete_medio'}))

        fig_fr = go.Figure(go.Bar(
            x=fr['frete_medio'], y=fr['state'], orientation='h',
            marker=dict(color=fr['frete_medio'],
                        colorscale=[[0,'#253040'],[1,'#e05c5c']], showscale=False),
            text=fr['frete_medio'].map(lambda v: f'₹{v:.0f}'),
            textposition='outside', textfont=dict(color=MUTED, size=10),
            hovertemplate='<b>%{y}</b><br>Frete Médio: ₹%{x:.2f}<extra></extra>',
        ))
        fig_fr.update_layout(**base_layout(
            height=460, legend=dict(),
            xaxis=dict(title='Custo de Frete (₹)', gridcolor=BORDER),
            yaxis=dict(autorange='reversed', title=''),
        ))
        style_axes(fig_fr)
        st.plotly_chart(fig_fr, width='stretch')

    # ── Row 2: Quadrante Frete x Lead Time ──
    st.markdown('<p class="section-title">Mapa de Eficiência: Frete vs Lead Time por Estado</p>', unsafe_allow_html=True)

    quad = df.groupby('state').agg(
        frete_medio=('shipping_cost','mean'),
        lead_time=('lead_time_total','mean'),
        pedidos=('order_id','count'),
        receita=('total_sales','sum'),
    ).reset_index()

    med_frete = quad['frete_medio'].median()
    med_lead  = quad['lead_time'].median()

    def quadrant(row):
        if   row['frete_medio'] <= med_frete and row['lead_time'] <= med_lead: return '✅ Eficiente'
        elif row['frete_medio'] >  med_frete and row['lead_time'] >  med_lead: return '🚨 Problemático'
        elif row['frete_medio'] >  med_frete:                                  return '💸 Frete Caro'
        else:                                                                   return '⏳ Lento'

    quad['quadrante'] = quad.apply(quadrant, axis=1)

    color_map = {
        '✅ Eficiente':    '#5cd98d',
        '🚨 Problemático': '#e05c5c',
        '💸 Frete Caro':   '#f0a500',
        '⏳ Lento':        '#3ecfcf',
    }
    quad_ann = [
        dict(x=quad['frete_medio'].min()*0.98, y=quad['lead_time'].max()*0.97,
             text='⏳ Lento',       showarrow=False, font=dict(color='#3ecfcf', size=11)),
        dict(x=quad['frete_medio'].max(),       y=quad['lead_time'].max()*0.97,
             text='🚨 Problemático',showarrow=False, font=dict(color='#e05c5c', size=11), xanchor='right'),
        dict(x=quad['frete_medio'].min()*0.98, y=quad['lead_time'].min()*0.8,
             text='✅ Eficiente',   showarrow=False, font=dict(color='#5cd98d', size=11)),
        dict(x=quad['frete_medio'].max(),       y=quad['lead_time'].min()*0.8,
             text='💸 Frete Caro',  showarrow=False, font=dict(color='#f0a500', size=11), xanchor='right'),
    ]

    fig_quad = px.scatter(
        quad, x='frete_medio', y='lead_time',
        size='pedidos', color='quadrante',
        color_discrete_map=color_map, hover_name='state',
        hover_data={'pedidos':True,'frete_medio':':.2f','lead_time':':.1f','quadrante':False},
        labels={'frete_medio':'Frete Médio (₹)','lead_time':'Lead Time Médio (dias)'},
        size_max=40,
    )
    fig_quad.add_vline(x=med_frete, line_dash='dash', line_color=MUTED, line_width=1)
    fig_quad.add_hline(y=med_lead,  line_dash='dash', line_color=MUTED, line_width=1)
    fig_quad.update_layout(**base_layout(
        height=460,
        annotations=quad_ann,
        legend=dict(orientation='h', y=-0.12, x=0.5, xanchor='center'),
    ))
    style_axes(fig_quad)
    st.plotly_chart(fig_quad, width='stretch')

    # ── Row 3: Box plots & Heatmap ──
    col_j, col_k = st.columns(2)

    with col_j:
        st.markdown('<p class="section-title">Distribuição do Lead Time por Categoria</p>', unsafe_allow_html=True)

        fig_box = px.box(
            df, x='category', y='lead_time_total', color='category',
            color_discrete_sequence=PALETTE, points='outliers',
            labels={'lead_time_total':'Lead Time (dias)','category':'Categoria'},
        )
        fig_box.update_traces(marker=dict(size=3, opacity=0.4))
        fig_box.update_layout(**base_layout(height=340, legend=dict()))
        style_axes(fig_box)
        st.plotly_chart(fig_box, width='stretch')

    with col_k:
        st.markdown('<p class="section-title">Frete Médio: Categoria × Método de Pagamento</p>', unsafe_allow_html=True)

        heat = df.groupby(['category','payment_method'])['shipping_cost'].mean().reset_index()
        heat_pivot = heat.pivot(index='category', columns='payment_method', values='shipping_cost')

        fig_heat = go.Figure(go.Heatmap(
            z=heat_pivot.values,
            x=heat_pivot.columns.tolist(),
            y=heat_pivot.index.tolist(),
            colorscale=[[0,'#1a3a4a'],[0.5,'#3ecfcf'],[1,'#f0a500']],
            text=[[f'₹{v:.0f}' for v in row] for row in heat_pivot.values],
            texttemplate='%{text}', textfont=dict(size=13, color='white'),
            hovertemplate='%{y} × %{x}<br>Frete: ₹%{z:.2f}<extra></extra>',
            showscale=True,
            colorbar=dict(tickfont=dict(color=MUTED), outlinecolor=BORDER),
        ))
        fig_heat.update_layout(**base_layout(height=340, legend=dict()))
        style_axes(fig_heat)
        st.plotly_chart(fig_heat, width='stretch')

    # ── Row 4: Processamento & Trânsito ──
    col_l, col_m = st.columns(2)

    with col_l:
        st.markdown('<p class="section-title">Processamento vs Trânsito por Categoria</p>', unsafe_allow_html=True)

        proc = df.groupby('category').agg(
            processamento=('dias_processamento','mean'),
            transito=('dias_transito','mean'),
        ).reset_index()

        fig_proc = go.Figure()
        for i, col_name in enumerate(['processamento','transito']):
            fig_proc.add_trace(go.Bar(
                name=col_name.capitalize(), x=proc['category'], y=proc[col_name],
                marker_color=PALETTE[i],
                text=proc[col_name].map(lambda v: f'{v:.1f}d'),
                textposition='auto',
            ))
        fig_proc.update_layout(**base_layout(
            height=340,
            barmode='group',
            legend=dict(orientation='h', y=1.1),
            xaxis_title='Categoria',
            yaxis=dict(title='Dias', gridcolor=BORDER),
        ))
        style_axes(fig_proc)
        st.plotly_chart(fig_proc, width='stretch')

    with col_m:
        st.markdown('<p class="section-title">Top 10 Estados Mais Eficientes (Lead Time)</p>', unsafe_allow_html=True)

        top10 = (df.groupby('state')['lead_time_total']
                 .mean().sort_values().head(10).reset_index())

        fig_top10 = go.Figure(go.Bar(
            x=top10['state'], y=top10['lead_time_total'],
            marker=dict(color=top10['lead_time_total'],
                        colorscale=[[0,'#5cd98d'],[1,'#3ecfcf']], showscale=False),
            text=top10['lead_time_total'].map(lambda v: f'{v:.1f}d'),
            textposition='outside', textfont=dict(color=MUTED, size=10),
        ))
        fig_top10.update_layout(**base_layout(
            height=340, legend=dict(),
            xaxis=dict(title='Estado', tickangle=30),
            yaxis=dict(title='Lead Time (dias)', gridcolor=BORDER),
        ))
        style_axes(fig_top10)
        st.plotly_chart(fig_top10, width='stretch')

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:32px 0 16px;color:#3b4251;font-size:11px;
            border-top:1px solid #252934;margin-top:32px;font-family:'DM Mono',monospace;">
  E-COMMERCE SALES EDA  ·  BUILT WITH STREAMLIT + PLOTLY  ·  DATASET: SHARMAJICODER / KAGGLE
</div>
""", unsafe_allow_html=True)