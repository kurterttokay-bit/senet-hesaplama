import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go
import urllib3

# SSL hatalarını sustur
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="Kurter Finans Dashboard", page_icon="🏦", layout="centered")

def get_tcmb_faiz():
    """TCMB EVDS sisteminden canlı faiz çeker."""
    API_KEY = 'FPdDriF9XD' 
    SERI_KODU = 'TP.KK.M.1'
    
    # Tarihi 30 gün geriden başlatarak veri gelmesini garantiye alalım
    today = datetime.now().strftime('%d-%m-%Y')
    start_date = (datetime.now() - pd.Timedelta(days=30)).strftime('%d-%m-%Y')
    
    url = f"https://evds2.tcmb.gov.tr/service/evds/series={SERI_KODU}&startDate={start_date}&endDate={today}&type=json&key={API_KEY}"
    
    try:
        response = requests.get(url, timeout=15, verify=False)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            for item in reversed(items):
                val = item.get(SERI_KODU)
                if val is not None and val != "":
                    return float(val.replace(',', '.'))
            return 45.0
        else:
            st.error(f"TCMB Bağlantı Sorunu: Kod {response.status_code}")
            return 45.0
    except Exception as e:
        st.error(f"Veri Çekme Hatası: {str(e)}")
        return 45.0

# --- DASHBOARD ARAYÜZÜ ---
st.title("🏦 Kurter Senet Analiz Paneli")
st.markdown("---")

guncel_faiz = get_tcmb_faiz()

with st.sidebar:
    st.header("📊 Parametreler")
    ana_para = st.number_input("Senet Tutarı (₺)", min_value=0.0, value=0.0, step=5000.0)
    
    st.info(f"📡 TCMB Canlı Faiz: %{guncel_faiz}")
    
    manuel_mod = st.checkbox("Faiz Oranını Elle Ayarla")
    secilen_faiz = st.slider("Uygulanacak Faiz (%)", 1, 100, int(guncel_faiz)) if manuel_mod else guncel_faiz
    vade_tarihi = st.date_input("Vade Bitiş Tarihi", value=datetime(2026, 6, 24))

bugun = datetime.now().date()
kalan_gun = (vade_tarihi - bugun).days

if kalan_gun <= 0:
    st.error("⚠️ Lütfen ileri bir tarih seçin.")
elif ana_para > 0:
    # Hesaplama mantığı
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    vergi_avantaji = faiz_kazanci * 0.075 # %7.5 stopaj avantajı varsayımı

    c1, c2, c3 = st.columns(3)
    c1.metric("Vade Sonu", f"{ana_para + faiz_kazanci:,.2f} ₺")
    c2.metric("Kalan Vade", f"{kalan_gun} Gün")
    c3.metric("Vergi Kârı", f"{vergi_avantaji:,.2f} ₺")

    # Grafik
    fig = go.Figure(data=[go.Pie(labels=['Ana Para', 'Kazanç'], values=[ana_para, faiz_kazanci], hole=.4)])
    fig.update_layout(title_text="Yatırım Dağılımı")
    st.plotly_chart(fig)
else:
    st.warning("👈 Hesaplamaya başlamak için sol menüden senet tutarını girin.")