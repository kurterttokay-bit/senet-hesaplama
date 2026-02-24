import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Sayfa Konfigürasyonu
st.set_page_config(page_title="Kurter Finans | Pro", page_icon="📈", layout="centered")

# Özel CSS ile Arayüzü Şıklaştıralım
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    div[data-testid="stMetricValue"] { color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Kurter Finans Analiz")
st.markdown("<p style='color: #64748b;'>Stratejik Senet ve Mevduat Karşılaştırma Paneli</p>", unsafe_allow_html=True)
st.markdown("---")

# Giriş Alanları
st.subheader("⚙️ Parametreler")
col1, col2 = st.columns(2)

with col1:
    ana_para = st.number_input("Senet Tutarı (₺)", min_value=0.0, value=100000.0, step=1000.0)
    secilen_faiz = st.slider("Yıllık Mevduat Faizi (%)", 1, 100, 53)

with col2:
    vade_tarihi = st.date_input("Vade Bitiş Tarihi", value=datetime(2026, 6, 24))
    st.info("💡 Verileri değiştirdiğinizde grafik ve hesaplamalar anlık güncellenir.")

# Hesaplamalar
bugun = datetime.now().date()
kalan_gun = (vade_tarihi - bugun).days

if kalan_gun <= 0:
    st.error("⚠️ Lütfen ileri bir tarih seçin.")
elif ana_para > 0:
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    toplam_tutar = ana_para + faiz_kazanci
    vergi_avantaji = faiz_kazanci * 0.075

    st.markdown("---")
    
    # Metrik Kartları
    c1, c2, c3 = st.columns(3)
    c1.metric("Vade Sonu Toplam", f"{toplam_tutar:,.0f} ₺")
    c2.metric("Kalan Vade", f"{kalan_gun} Gün")
    c3.metric("Net Faiz Getirisi", f"{faiz_kazanci:,.0f} ₺", delta=f"{vergi_avantaji:,.0f} ₺ Vergi Avantajı", delta_color="normal")

    # Modern Donut Grafik (Plotly Custom)
    fig = go.Figure(data=[go.Pie(
        labels=['Ana Sermaye', 'Net Kazanç'], 
        values=[ana_para, faiz_kazanci], 
        hole=.6,
        marker=dict(colors=['#1e3a8a', '#fbbf24']), # Lacivert ve Altın
        textinfo='percent+label'
    )])
    
    fig.update_layout(
        title=dict(text="Sermaye Projeksiyonu", x=0.5, font=dict(size=18)),
        annotations=[dict(text=f'₺{toplam_tutar:,.0f}', x=0.5, y=0.5, font_size=16, showarrow=False)],
        showlegend=False,
        height=450,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
        <div style="background-color: #eff6ff; padding: 15px; border-left: 5px solid #1e3a8a; border-radius: 5px;">
            <p style="margin: 0; color: #1e3a8a;"><b>Finansal Not:</b> Bu senet vadesine kadar bankada tutulursa, 
            stopaj muafiyeti sayesinde yaklaşık <b>{vergi_avantaji:,.2f} ₺</b> ek kazanç elde edilmiş olur.</p>
        </div>
    """, unsafe_allow_html=True)

# --- KURTER ÖZEL İMZA ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style='text-align: center;'>
        <p style='color: #94a3b8; font-style: italic; margin-bottom: 0;'>Strategic Wealth Management</p>
        <h3 style='color: #1e3a8a; margin-top: 5px; letter-spacing: 2px;'><b>K U R T E R</b></h3>
        <p style='color: #fbbf24; font-weight: bold;'>♉ TAURUS DISCIPLINE</p>
    </div>
    """, unsafe_allow_html=True)
