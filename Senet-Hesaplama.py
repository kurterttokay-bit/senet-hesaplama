import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Kurter Finans", page_icon="🏦", layout="centered")

st.title("🏦 Kurter Senet Analiz Paneli")
st.markdown("---")

# Giriş Alanları - Ana Ekranda
st.subheader("📊 Hesaplama Parametreleri")
col1, col2 = st.columns(2)

with col1:
    ana_para = st.number_input("Senet Tutarı (₺)", min_value=0.0, value=100000.0, step=1000.0)
    secilen_faiz = st.slider("Yıllık Mevduat Faizi (%)", 1, 100, 53)

with col2:
    vade_tarihi = st.date_input("Vade Bitiş Tarihi", value=datetime(2026, 6, 24))
    st.info("💡 Verileri değiştirdiğinizde grafik anlık güncellenir.")

bugun = datetime.now().date()
kalan_gun = (vade_tarihi - bugun).days

st.markdown("---")

if kalan_gun <= 0:
    st.error("⚠️ Lütfen ileri bir tarih seçin.")
elif ana_para > 0:
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    toplam_tutar = ana_para + faiz_kazanci
    vergi_avantaji = faiz_kazanci * 0.075

    c1, c2, c3 = st.columns(3)
    c1.metric("Vade Sonu", f"{toplam_tutar:,.0f} ₺")
    c2.metric("Kalan Vade", f"{kalan_gun} Gün")
    c3.metric("Net Getiri", f"{faiz_kazanci:,.0f} ₺")

    fig = go.Figure(data=[go.Pie(labels=['Ana Para', 'Kazanç'], values=[ana_para, faiz_kazanci], hole=.4)])
    st.plotly_chart(fig, use_container_width=True)
    
    st.success(f"📈 Vergi Avantajı: Yaklaşık {vergi_avantaji:,.2f} ₺")

# --- KURTER ÖZEL İMZA ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #7f8c8d;'><i>Finance meets Focus</i><br><h4 style='color: #2c3e50;'><b>K U R T E R</b></h4><p>♉ Taurus Discipline</p></div>", unsafe_allow_html=True)
