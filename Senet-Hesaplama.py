import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Sayfa Ayarları - Mobil öncelikli daraltılmış görünüm
st.set_page_config(page_title="Kurter Finans", page_icon="📈", layout="centered")

# Görsel Stil Ayarları (Boşlukları daraltma ve ortalama)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    h1 { text-align: center; color: #1e3a8a; font-size: 24px !important; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Kurter Finans Analiz")

# Giriş ve Sonuçları içiçe geçirerek yerden tasarruf ediyoruz
col1, col2 = st.columns(2)
with col1:
    ana_para = st.number_input("Senet (₺)", min_value=0.0, value=100000.0, step=1000.0)
with col2:
    secilen_faiz = st.number_input("Faiz (%)", min_value=1, max_value=100, value=53)

vade_tarihi = st.date_input("Vade Tarihi", value=datetime(2026, 6, 24))

# Hesaplamalar
bugun = datetime.now().date()
kalan_gun = (vade_tarihi - bugun).days

if kalan_gun <= 0:
    st.error("⚠️ İleri tarih seçin.")
elif ana_para > 0:
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    toplam_tutar = ana_para + faiz_kazanci
    vergi_avantaji = faiz_kazanci * 0.075

    # Metrikleri tek satıra sığdırıyoruz
    m1, m2, m3 = st.columns(3)
    m1.metric("Toplam", f"{toplam_tutar:,.0f}")
    m2.metric("Gün", f"{kalan_gun}")
    m3.metric("Net Kâr", f"{faiz_kazanci:,.0f}")

    # Donut Grafik - Boyutu küçültülmüş
    fig = go.Figure(data=[go.Pie(
        labels=['Sermaye', 'Kazanç'], 
        values=[ana_para, faiz_kazanci], 
        hole=.7,
        marker=dict(colors=['#1e3a8a', '#fbbf24']),
        textinfo='none'
    )])
    
    fig.update_layout(
        height=220, # Yüksekliği ciddi oranda azalttık
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        annotations=[dict(text=f"%{secilen_faiz}", x=0.5, y=0.5, font_size=18, showarrow=False, font_color="#1e3a8a")]
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown(f"<p style='text-align: center; color: #1e3a8a; font-size: 14px;'><b>Vergi Avantajı: {vergi_avantaji:,.2f} ₺</b></p>", unsafe_allow_html=True)

# --- İMZA ---
st.markdown("""
    <div style='text-align: center; border-top: 1px solid #e2e8f0; margin-top: 10px; padding-top: 5px;'>
        <h4 style='color: #1e3a8a; margin: 0; letter-spacing: 2px;'><b>K U R T E R</b></h4>
        <p style='color: #fbbf24; font-size: 12px; margin: 0;'>♉ TAURUS DISCIPLINE</p>
    </div>
    """, unsafe_allow_html=True)
