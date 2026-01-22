import streamlit as st
import whisper
import yt_dlp
import os
import datetime
import time # sleep fonksiyonu için

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Annemin Sineması", page_icon="🎬", layout="centered")

# --- ŞIK GÖRÜNÜM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { color: #E50914; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: bold; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border-radius: 12px; border: 1px solid #E50914; padding: 10px; }
    .stButton > button { background-color: #E50914; color: white; width: 100%; border-radius: 25px; font-weight: bold; border: none; height: 3em; }
    .stButton > button:hover { background-color: #ff1f1f; color: white; border: 1px solid white; }
    footer {visibility: hidden;}
    .css-1d391kg {padding-top: 2rem;} /* Üst boşluğu ayarla */
    </style>
    """, unsafe_allow_html=True)

# --- BAŞLANGIÇ EKRANI FONKSİYONU ---
def show_welcome_screen():
    st.empty() # Tüm içeriği temizle
    st.markdown("<h1 style='text-align: center; color: #E50914; font-size: 3em;'>Hoşgeldinn Annişimm! ❤️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.5em; color: white;'>Bu senin özel sinema salonun...</p>", unsafe_allow_html=True)
    
    # Kırmızı kalplerin yağdığı efekt
    st.snow() 
    
    time.sleep(3) # 3 saniye bekle
    st.experimental_rerun() # Sayfayı yenileyerek ana uygulamayı yükle (kalpler durur)

# --- ANA FONKSİYONLAR ---
@st.cache_resource
def model_yukle():
    return whisper.load_model("base")

def video_bilgisi_al(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

# --- UYGULAMA AKIŞI ---
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    show_welcome_screen()
    st.session_state.welcome_shown = True
else:
    # Ana uygulama içeriği
    st.markdown("<h1>🎬 Annemin Sineması</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center; font-size: 1.2em;'>İzlemek istediğin Kore, Çin, Japon, Hint veya istediğin dizinin linkini aşağıya yapıştır, senin için hemen Türkçe altyazı hazırlayayım.</p>", unsafe_allow_html=True)

    st.divider()
    dizi_linki = st.text_input("Dizi Linkini Buraya Yapıştır Anneciğim:", placeholder="Örn: https://dizisitesi.com/harika-dizi-bolum-1")

    if dizi_linki:
        try:
            # Video bilgilerini çekmeye çalışıyoruz
            with st.spinner('Anneciğim, diziyi senin için hazırlıyorum...'):
                video_info = video_bilgisi_al(dizi_linki)
                st.success(f"Dizi Bulundu: {video_info.get('title', 'İyi Seyirler!')}")
                
                # Videoyu en yüksek kalitede gösteriyoruz (Orijinal ses)
                st.video(dizi_linki)
                
                st.divider()
                st.subheader("📝 Altyazı Ayarları")
                
                if st.button("Türkçe Altyazıları Hazırla"):
                    model = model_yukle()
                    
                    with st.status("Yapay zeka sesleri analiz ediyor ve çeviriyor...", expanded=True) as status:
                        st.write("Ses dosyası okunuyor...")
                        result = model.transcribe(dizi_linki)
                        status.update(label="Çeviri Tamamlandı!", state="complete", expanded=False)
                    
                    st.markdown("### 🇹🇷 Türkçe Altyazı Takibi")
                    # Altyazıları zaman damgalarıyla birlikte listeleyelim
                    for segment in result['segments']:
                        # Saniyeyi 00:00:00 formatına çevir
                        start_time = str(datetime.timedelta(seconds=int(segment['start'])))
                        st.write(f"⏱️ **{start_time}** : {segment['text']}")
                        
        except Exception as e:
            st.error("Bir sorun oluştu annişim. Bu sitedeki videoları şu an açamıyorum.")
            st.info("İpucu: Linkin doğru olduğundan veya başka bir sitedeki linki denemekten emin ol.")

    # --- ALT BİLGİ ---
    st.markdown("<br><br><p style='text-align: center; color: #888888; font-style: italic;'>Senin için sevgiyle, özel olarak hazırlandı ❤️</p>", unsafe_allow_html=True)