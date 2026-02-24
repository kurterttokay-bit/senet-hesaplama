import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Kurter Finans | Pro", page_icon="🏦", layout="centered")

# Stil ve İmza Fontu
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
    <style>
    .block-container { padding-top: 1rem; }
    h1 { text-align: center; color: #1e293b; font-size: 24px !important; }
    .signature { font-family: 'Dancing Script', cursive; font-size: 42px; color: #0f172a; margin-top: 5px; }
    .corporate-text { color: #94a3b8; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin-top: -10px; }
    .stMetric { border: 1px solid #f1f5f9; padding: 5px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Kurter Finans Analiz")

c1, c2, c3 = st.columns([1.5, 1, 1.2])
with c1: ana_para = st.number_input("Ana Para (₺)", min_value=0.0, value=100000.0)
with c2: secilen_faiz = st.number_input("Faiz (%)", min_value=1.0, value=53.0)
with c3: vade_tarihi = st.date_input("Vade", value=datetime(2026, 6, 24))

bugun = datetime.now().date()
kalan_gun = (vade_tarihi - bugun).days

if ana_para > 0 and kalan_gun > 0:
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    toplam_tutar = ana_para + faiz_kazanci
    vergi_avantaji = faiz_kazanci * 0.075

    m1, m2, m3 = st.columns(3)
    m1.metric("Vade Sonu", f"{toplam_tutar:,.0f}")
    m2.metric("Gün", f"{kalan_gun}")
    m3.metric("Net Kâr", f"{faiz_kazanci:,.0f}")

    fig = go.Figure(data=[go.Pie(
        labels=['Ana Para', 'Kâr'], 
        values=[ana_para, faiz_kazanci], 
        hole=.7,
        marker=dict(colors=['#1e293b', '#94a3b8']), 
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=12, color='#1e293b')
    )])
    
    fig.update_layout(height=220, margin=dict(l=50, r=50, t=10, b=10), showlegend=False,
                      annotations=[dict(text=f"₺{toplam_tutar:,.0f}", x=0.5, y=0.5, font_size=14, showarrow=False)])
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 11px;'>Vergi Avantajı: {vergi_avantaji:,.0f} ₺</p>", unsafe_allow_html=True)

st.markdown(f"<div style='text-align: center; border-top: 1px solid #f1f5f9; margin-top: 10px;'><div class='signature'>Kurter</div><div class='corporate-text'>Strategic Assets & Risk Management</div></div>", unsafe_allow_html=True)
