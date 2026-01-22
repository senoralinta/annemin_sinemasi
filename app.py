import streamlit as st
import whisper
import yt_dlp
import os
import datetime
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Annemin Sineması", page_icon="🎬", layout="centered")

# --- ŞIK GÖRÜNÜM VE KALP EFEKTİ (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { color: #E50914; text-align: center; font-family: 'Segoe UI', sans-serif; font-weight: bold; }
    .stTextInput > div > div > input { background-color: #262730; color: white; border-radius: 12px; border: 1px solid #E50914; }
    .stButton > button { background-color: #E50914; color: white; width: 100%; border-radius: 25px; font-weight: bold; border: none; height: 3em; }
    footer {visibility: hidden;}
    
    /* Kar tanelerini kalbe dönüştüren sihirli kod */
    [data-testid="stSnow"] {
        display: none;
    }
    .heart {
        position: fixed;
        top: -10%;
        color: #E50914;
        font-size: 20px;
        font-family: Arial;
        text-shadow: 0 0 5px rgba(0,0,0,0.5);
        user-select: none;
        z-index: 1000;
        pointer-events: none;
        animation-name: hearts-fall;
        animation-duration: 5s;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
    }
    @keyframes hearts-fall {
        0% { top: -10%; transform: translateX(0); }
        100% { top: 100%; transform: translateX(100px); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- KALP YAĞDIRMA FONKSİYONU ---
def kalpleri_yagdir():
    # HTML ve JavaScript ile ekrana kalpler saçıyoruz
    heart_html = """
    <script>
    function createHeart() {
        const heart = document.createElement('div');
        heart.innerText = '❤️';
        heart.classList.add('heart');
        heart.style.left = Math.random() * 100 + 'vw';
        heart.style.animationDuration = Math.random() * 2 + 3 + 's';
        document.body.appendChild(heart);
        setTimeout(() => { heart.remove(); }, 5000);
    }
    setInterval(createHeart, 300);
    </script>
    """
    st.markdown(heart_html, unsafe_allow_html=True)

# --- BAŞLANGIÇ EKRANI FONKSİYONU ---
def show_welcome_screen():
    kalpleri_yagdir() # Kar yerine gerçek kalp yağdırıyoruz
    st.markdown("<div style='height: 200px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1>Hoşgeldin Annişimm! ❤️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.5em; color: white;'>Senin için özel hazırlandı...</p>", unsafe_allow_html=True)
    
    time.sleep(5)
    st.session_state.welcome_shown = True
    st.rerun()

# --- ANA FONKSİYONLAR ---
@st.cache_resource
def model_yukle():
    return whisper.load_model("base")

def video_bilgisi_al(url):
    ydl_opts = {'format': 'best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

# --- UYGULAMA AKIŞI ---
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    show_welcome_screen()
else:
    st.markdown("<h1>🎬 Annemin Sineması</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Dizi linkini aşağıya yapıştır anneciğim.</p>", unsafe_allow_html=True)

    dizi_linki = st.text_input("Dizi Linki:", placeholder="https://...")

    if dizi_linki:
        try:
            with st.spinner('Anneciğim hazırlıyorum...'):
                video_info = video_bilgisi_al(dizi_linki)
                st.video(dizi_linki)
                
                if st.button("Türkçe Altyazıları Hazırla"):
                    model = model_yukle()
                    result = model.transcribe(dizi_linki)
                    for segment in result['segments']:
                        start_time = str(datetime.timedelta(seconds=int(segment['start'])))
                        st.write(f"⏱️ **{start_time}** : {segment['text']}")
        except Exception as e:
            st.error("Bir sorun oluştu. Lütfen başka bir link dene.")

st.markdown("<br><br><p style='text-align: center; color: #888888;'>Senin için sevgiyle ❤️</p>", unsafe_allow_html=True)
