import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Sayfa Ayarları
st.set_page_config(page_title="Kurter Finans | Pro", page_icon="🏦", layout="centered")

# CSS: Yazı tipleri ve boşluk ayarları
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&display=swap" rel="stylesheet">
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    h1 { text-align: center; color: #1e293b; font-size: 22px !important; font-weight: 700; margin-bottom: 0.5rem; }
    .signature { font-family: 'Dancing Script', cursive; font-size: 30px; color: #334155; margin-top: 5px; }
    .corporate-text { color: #94a3b8; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin-top: -5px; }
    .stMetric { border: 1px solid #f1f5f9; padding: 5px; border-radius: 10px; }
    div[data-testid="stMetricLabel"] { font-size: 12px !important; }
    div[data-testid="stMetricValue"] { font-size: 18px !important; color: #1e293b; }
    </style>
    """, unsafe_allow_html=True)

st.title("Kurter Finans Analiz")

# Girişler - Slider yerine Number Input (Elle giriş)
c1, c2, c3 = st.columns([1.5, 1, 1.2])
with c1:
    ana_para = st.number_input("Senet (₺)", min_value=0.0, value=100000.0, step=1000.0)
with c2:
    secilen_faiz = st.number_input("Faiz (%)", min_value=1.0, max_value=100.0, value=53.0, step=0.5)
with c3:
    vade_tarihi = st.date_input("Vade", value=datetime(2026, 6, 24))

# Zaman Hesaplama
bugun = datetime.now().date()
kalan_gun = (vade_tarihi - bugun).days

if ana_para > 0 and kalan_gun > 0:
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    toplam_tutar = ana_para + faiz_kazanci
    vergi_avantaji = faiz_kazanci * 0.075

    # Metrikler - Daha küçük ve kompakt
    m1, m2, m3 = st.columns(3)
    m1.metric("Vade Sonu", f"{toplam_tutar:,.0f}")
    m2.metric("Gün", f"{kalan_gun}")
    m3.metric("Net Kâr", f"{faiz_kazanci:,.0f}")

    # Grafik - Kalıcı Yazılar (Inside Label)
    fig = go.Figure(data=[go.Pie(
        labels=['Sermaye', 'Kâr'], 
        values=[ana_para, faiz_kazanci], 
        hole=.7,
        marker=dict(colors=['#334155', '#94a3b8']), # Barut Grisi ve Gümüş
        textinfo='percent+label', # Üzerine gelmeden yüzdeleri gösterir
        textposition='inside',
        insidetextfont=dict(color='white', size=11)
    )])
    
    fig.update_layout(
        height=180, # Daha da küçültüldü
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        annotations=[dict(text=f"₺{toplam_tutar:,.0f}", x=0.5, y=0.5, font_size=14, showarrow=False, font_color="#1e293b")]
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown(f"<p style='text-align: center; color: #64748b; font-size: 11px;'>Vergi Avantajı: {vergi_avantaji:,.0f} ₺</p>", unsafe_allow_html=True)

# --- İMZA BÖLÜMÜ ---
st.markdown(f"""
    <div style='text-align: center; border-top: 1px solid #f1f5f9; margin-top: 5px;'>
        <div class='signature'>Kurter</div>
        <div class='corporate-text'>Strategic Assets & Risk Management</div>
    </div>
    """, unsafe_allow_html=True)
