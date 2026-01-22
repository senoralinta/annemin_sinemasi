import streamlit as st
import streamlit.components.v1 as components
import whisper
import yt_dlp
import datetime
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Annemin Sineması", page_icon="🎬")

# --- KALP YAĞDIRMA FONKSİYONU ---
def kalpleri_yagdir():
    # JavaScript'in Streamlit içinde çalışması için height=0 yerine görünür alan verdik
    heart_code = """
    <div id='hearts-container'></div>
    <style>
        body { margin: 0; overflow: hidden; }
        .heart {
            position: fixed;
            top: -10vh;
            font-size: 30px;
            user-select: none;
            pointer-events: none;
            animation: fall 5s linear forwards;
            z-index: 9999;
        }
        @keyframes fall {
            to {
                transform: translateY(110vh) translateX(80px);
                opacity: 0;
            }
        }
    </style>
    <script>
        function createHeart() {
            const heart = document.createElement('div');
            heart.innerHTML = '❤️';
            heart.className = 'heart';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.animationDuration = (Math.random() * 2 + 3) + 's';
            document.body.appendChild(heart);
            setTimeout(() => { heart.remove(); }, 6000);
        }
        // Kalplerin yoğunluğunu buradan ayarlayabilirsin (200ms)
        setInterval(createHeart, 200);
    </script>
    """
    components.html(heart_code, height=200) # Kalplerin çıkış noktası için alan

# --- STİL AYARLARI ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h1 { color: #E50914 !important; text-align: center; font-weight: bold; }
    .stTextInput input { border-radius: 15px !important; border: 2px solid #E50914 !important; }
    .stButton>button { background-color: #E50914; color: white; border-radius: 20px; width: 100%; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- ANA SİSTEM ---
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    kalpleri_yagdir() # Kalpler burada başlıyor
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1>Hoşgeldin Annişimm! ❤️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.5em;'>Senin için özel hazırlandı bal annemm...</p>", unsafe_allow_html=True)
    
    time.sleep(6) 
    st.session_state.welcome_shown = True
    st.rerun()
else:
    st.markdown("<h1>🎬 Annemin Sineması</h1>", unsafe_allow_html=True)
    
    dizi_linki = st.text_input("Dizi Linkini Yapıştır Annemmm:", placeholder="Buraya linki ekle...")

    if dizi_linki:
        try:
            with st.spinner('Anneciğim dizi hazırlanıyor...'):
                ydl_opts = {'format': 'best', 'quiet': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(dizi_linki, download=False)
                    video_url = info['url']
                
                st.video(video_url)
                
                if st.button("Türkçe Altyazı Oluştur"):
                    st.info("AI Çeviri Başladı... Lütfen bekle annişim.")
                    model = whisper.load_model("base")
                    result = model.transcribe(video_url)
                    for seg in result['segments']:
                        t = str(datetime.timedelta(seconds=int(seg['start'])))
                        st.write(f"⏱️ **{t}**: {seg['text']}")
        except:
            st.error("Dizi açılırken bir hata oldu annişim, lütfen linki kontrol et.")
