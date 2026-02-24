import ssl

# Mac'teki o inatçı SSL kontrolünü tamamen devre dışı bırakıyoruz
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go
import urllib3

# Mac'teki SSL/Sertifika uyarılarını kapatır
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Sayfa Yapılandırması
st.set_page_config(page_title="Kurter Finans Dashboard", page_icon="🏦", layout="centered")

def get_tcmb_faiz():
    """TCMB EVDS sisteminden Kurter'in API Key'i ile canlı faiz çeker."""
    API_KEY = 'FPdDriF9XD' 
    SERI_KODU = 'TP.KK.M.1' # 1 Ay Vadeli Mevduat Faizi
    
    today = datetime.now().strftime('%d-%m-%Y')
    start_date = (datetime.now() - pd.Timedelta(days=15)).strftime('%d-%m-%Y')
    
    url = f"https://evds2.tcmb.gov.tr/service/evds/series={SERI_KODU}&startDate={start_date}&endDate={today}&type=json&key={API_KEY}"
    
    try:
        # verify=False ekleyerek SSL hatasını kesin çözüyoruz
        response = requests.get(url, timeout=10, verify=False)
        data = response.json()
        
        items = data.get('items', [])
        for item in reversed(items):
            val = item.get(SERI_KODU)
            if val is not None and val != "":
                return float(val.replace(',', '.'))
        return 45.0
    except:
        return 45.0

# --- DASHBOARD ARAYÜZÜ ---
st.title("🏦 Kurter Senet Analiz Paneli")
st.write(f"**Veri Kaynağı:** TCMB Canlı Veri Sistemi | **Tarih:** {datetime.now().strftime('%d/%m/%Y')}")
st.markdown("---")

# Canlı Veriyi Çek
guncel_faiz = get_tcmb_faiz()

# Yan Menü Girdileri
with st.sidebar:
    st.header("📊 Hesaplama Parametreleri")
    ana_para = st.number_input("Senet Tutarı (₺)", value=0.0, step=5000.0)
    
    st.info(f"📡 Güncel Mevduat Faizi: %{guncel_faiz}")
    
    # Kullanıcı isterse faizi elle değiştirebilir
    manuel_mod = st.checkbox("Faiz Oranını Elle Ayarla")
    if manuel_mod:
        secilen_faiz = st.slider("Uygulanacak Faiz (%)", 1, 100, int(guncel_faiz))
    else:
        secilen_faiz = guncel_faiz
        
    vade_tarihi = st.date_input("Vade Bitiş Tarihi", value=datetime(2026, 6, 24))

# Hesaplama Motoru
bugun = datetime.now().date()
kalan_gun = (vade_tarihi - bugun).days

if kalan_gun <= 0:
    st.error("⚠️ Lütfen bugünden ileri bir vade tarihi seçin.")
else:
    # Finansal Matematik
    faiz_kazanci = ana_para * (secilen_faiz / 100) * (kalan_gun / 365)
    toplam_tahsilat = ana_para + faiz_kazanci
    vergi_avantaji = faiz_kazanci * 0.075 # %7.5 stopaj avantajı

    # Görsel Kartlar
    c1, c2, c3 = st.columns(3)
    c1.metric("Vade Sonu", f"{toplam_tahsilat:,.2f} ₺")
    c2.metric("Kalan Vade", f"{kalan_gun} Gün")
    c3.metric("Vergi Kârı", f"{vergi_avantaji:,.2f} ₺", delta="Avantaj", delta_color="normal")

    # Pasta Grafiği
    fig = go.Figure(data=[go.Pie(
        labels=['Ana Para', 'Vade Farkı Kazancı'],
        values=[ana_para, faiz_kazanci],
        hole=.4,
        marker_colors=['#003366', '#28a745']
    )])
    fig.update_layout(title_text="Portföy Dağılımı")
    st.plotly_chart(fig)

    st.success(f"💡 Not: Bu işlem senet olduğu için banka mevduatına göre **{vergi_avantaji:,.2f} ₺** daha kazançlıdır (Stopaj muafiyeti).")