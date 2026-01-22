import streamlit as st
import whisper
import yt_dlp
import datetime
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Annemin Sineması", page_icon="🎬")

# --- KALP YAĞDIRMA VE TASARIM (TEK PARÇA) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { color: #E50914; text-align: center; font-family: sans-serif; }
    
    /* Kalp Yağmuru Efekti */
    .heart {
        position: fixed;
        top: -10%;
        font-size: 24px;
        z-index: 9999;
        user-select: none;
        pointer-events: none;
        animation: fall 5s linear infinite;
    }
    @keyframes fall {
        0% { transform: translateY(-10vh) translateX(0); }
        100% { transform: translateY(110vh) translateX(50px); }
    }
    </style>
    
    <script>
    function createHeart() {
        const heart = document.createElement('div');
        heart.innerHTML = '❤️';
        heart.className = 'heart';
        heart.style.left = Math.random() * 100 + 'vw';
        heart.style.animationDuration = (Math.random() * 3 + 2) + 's';
        document.body.appendChild(heart);
        setTimeout(() => { heart.remove(); }, 5000);
    }
    // Kalp yağdırma sıklığı
    setInterval(createHeart, 200);
    </script>
    """, unsafe_allow_html=True)

# --- ANA SİSTEM ---
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    # HOŞGELDİN EKRANI
    st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1>Hoşgeldin Annişimmm! ❤️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.5em;'>Senin için özel hazırlandı...</p>", unsafe_allow_html=True)
    
    time.sleep(5)
    st.session_state.welcome_shown = True
    st.rerun()
else:
    # ANA UYGULAMA
    st.markdown("<h1>🎬 Annemin Sineması</h1>", unsafe_allow_html=True)
    
    dizi_linki = st.text_input("Dizi Linkini Yapıştır Anneciğim:", placeholder="https://...")

    if dizi_linki:
        try:
            with st.spinner('Dizi hazırlanıyor...'):
                ydl_opts = {'format': 'best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(dizi_linki, download=False)
                    video_url = info['url']
                
                st.video(video_url)
                
                if st.button("Türkçe Altyazı Oluştur"):
                    st.warning("Bu işlem videonun uzunluğuna göre vakit alabilir...")
                    model = whisper.load_model("base")
                    result = model.transcribe(video_url)
                    for seg in result['segments']:
                        t = str(datetime.timedelta(seconds=int(seg['start'])))
                        st.write(f"⏱️ **{t}**: {seg['text']}")
        except:
            st.error("Bu linki açamadım annişimm, başka bir tane dener misin?")
