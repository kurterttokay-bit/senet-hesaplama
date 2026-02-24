import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Sayfa Ayarları
st.set_page_config(page_title="Kurter Finans | Pro", page_icon="🏦", layout="centered")

# CSS: Hatalı sızıntıları engelleyen ve tasarımı düzelten temiz kod
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .main-title { 
        text-align: center; 
        color: #f8fafc; 
        font-family: 'Inter', sans-serif;
        font-size: 26px; 
        font-weight: 800; 
        letter-spacing: -0.5px;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 20px;
    }
    .signature { font-family: 'Dancing Script', cursive; font-size: 36px; color: #f8fafc; margin-top: 5px; }
    .corporate-text { color: #64748b; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; margin-top: -10px; }
    /* Metrik kutularını koyu temaya uydurma */
    [data-testid="stMetric"] { background-color: #1e293b; border: 1px solid #334155; padding: 10px; border-radius: 10px; }
    [data-testid="stMetricValue"] { color: #f8fafc !important; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

# Başlık Alanı
st.markdown('<div class="main-title">KURTER FINANS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Strategic Asset Analysis</div>', unsafe_allow_html=True)

# Girişler
c1, c2, c3 = st.columns([1.5, 1, 1.2])
with c1:
    ana_para = st.number_input("Ana Para (₺)", min_value=0.0, value=100000.0, step=1000.0)
with c2:
    secilen_faiz = st.number_input("Faiz (%)", min_value=1.0, value=53.0, step=0.5)
with c3:
    vade_tarihi = st.date_input("Vade", value=datetime(2026, 6, 24))

bugun = datetime.now().date()
kalan_gun = (vade_tarihi - bugun).days

if ana_para > 0 and kalan_gun > 0:
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    toplam_tutar = ana_para + faiz_kazanci
    vergi_avantaji = faiz_kazanci * 0.075

    # Metrikler
    m1, m2, m3 = st.columns(3)
    m1.metric("Vade Sonu", f"{toplam_tutar:,.0f}")
    m2.metric("Gün", f"{kalan_gun}")
    m3.metric("Net Kâr", f"{faiz_kazanci:,.0f}")

    # Grafik - Parlak ve Okunaklı Yazılar
    fig = go.Figure(data=[go.Pie(
        labels=['Ana Para', 'Kâr'], 
        values=[ana_para, faiz_kazanci], 
        hole=.7,
        marker=dict(colors=['#334155', '#38bdf8']), # Koyu Gri ve Parlak Mavi
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=14, color='#f8fafc') # Beyaz ve büyük font
    )])
    
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=30, b=30),
        showlegend=False,
        annotations=[dict(text=f"₺{toplam_tutar:,.0f}", x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#f8fafc")]
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f"<p style='text-align: center; color: #94a3b8; font-size: 11px;'>Vergi Avantajı: {vergi_avantaji:,.0f} ₺</p>", unsafe_allow_html=True)

# --- İMZA BÖLÜMÜ (TEMİZLENMİŞ) ---
st.markdown(f"""
    <div style='text-align: center; border-top: 1px solid #334155; margin-top: 20px; padding-top: 10px;'>
        <div class='signature'>Kurter</div>
        <div class='corporate-text'>Strategic Assets & Risk Management</div>
    </div>
    """, unsafe_allow_html=True)
