import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(
       api_key=os.getenv("GROQ_API_KEY", "")
   )

# Page Configuration
st.set_page_config(
    page_title="BubbleWash Laundry",
    page_icon="🧺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Modern & Clean Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background */
    .stApp {
        background: linear-gradient(to bottom right, #e0f2fe, #fae8ff, #fef3c7);
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container */
    .main .block-container {
        padding: 1.5rem 1rem;
        max-width: 900px;
    }
    
    /* Header */
    .custom-header {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    .custom-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .custom-header p {
        color: #6b7280;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Info cards */
    .info-cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .info-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .info-card .icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .info-card .title {
        font-size: 0.75rem;
        color: #6b7280;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }
    
    .info-card .value {
        font-size: 0.875rem;
        color: #1f2937;
        font-weight: 600;
    }
    
    /* Messages area */
    .messages-area {
        margin-bottom: 1rem;
        min-height: 200px;
    }
    
    /* Messages */
    .message {
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message.user {
        flex-direction: row-reverse;
    }
    
    .message-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .user .message-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .bot .message-avatar {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .message-content {
        max-width: 70%;
        padding: 0.875rem 1.125rem;
        border-radius: 16px;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .user .message-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .bot .message-content {
        background: #f3f4f6;
        color: #1f2937;
        border-bottom-left-radius: 4px;
    }
    
    /* Input field */
    .stTextInput > div > div > input {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.875rem 1rem;
        font-size: 0.95rem;
        transition: all 0.2s;
        background: white;
        color: #1f2937 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Remove label */
    .stTextInput > label {
        display: none;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1rem;
        font-size: 0.95rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.4);
        margin-top: 0.75rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 8px -1px rgba(102, 126, 234, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 1rem;
        color: #9ca3af;
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Quick actions */
    .quick-actions {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }
    
    .quick-action {
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #4b5563;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .quick-action:hover {
        background: #e5e7eb;
        border-color: #d1d5db;
    }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """
Kamu adalah chatbot resmi BubbleWash Laundry.
Gunakan bahasa Indonesia yang sopan, ramah, jelas, dan profesional.
Jawaban harus konsisten dengan data di bawah ini.

========================
INFORMASI TOKO
========================
Nama Usaha: BubbleWash Laundry
Alamat: Pedurungan Village No. 12A Blok A, Semarang
Hari Operasional: Senin – Minggu
Jam Operasional: 08.00 – 21.00 WIB

Layanan Pickup & Delivery:
- Tersedia (antar jemput ke rumah pelanggan)
- Tarif mengikuti pricelist pickup & delivery

========================
PRICELIST DROP TO OUTLET (KILOAN)
========================

Cuci Komplit:
- Express: Rp 20.000/kg
- One Day: Rp 15.000/kg
- Regular: Rp 10.000/kg

Cuci Lipat:
- Express: Rp 15.000/kg
- One Day: Rp 10.000/kg
- Regular: Rp 7.000/kg

Setrika:
- Express: Rp 12.000/kg
- One Day: Rp 10.000/kg
- Regular: Rp 7.000/kg

========================
PRICELIST PICKUP & DELIVERY (KILOAN)
========================

Cuci Komplit:
- Express: Rp 25.000/kg
- One Day: Rp 18.000/kg
- Regular: Rp 12.000/kg

Cuci Lipat:
- Express: Rp 20.000/kg
- One Day: Rp 12.000/kg
- Regular: Rp 10.000/kg

Setrika:
- Express: Rp 15.000/kg
- One Day: Rp 12.000/kg
- Regular: Rp 10.000/kg

========================
PRICELIST PREMIUM CARE & LAINNYA
========================

(Data lengkap sesuai pricelist)

========================
ATURAN JAWABAN
========================
- Jawab hanya berdasarkan data BubbleWash Laundry
- Jika pertanyaan di luar layanan laundry, jawab sopan bahwa chatbot hanya melayani informasi BubbleWash Laundry
- Jangan mengarang harga atau layanan
"""

# Header
st.markdown("""
<div class="custom-header">
    <div style="font-size: 3rem;">🧺</div>
    <h1>BubbleWash Laundry</h1>
    <p>Asisten Virtual untuk Layanan Laundry Anda</p>
</div>
""", unsafe_allow_html=True)

# Info Cards
st.markdown("""
<div class="info-cards">
    <div class="info-card">
        <div class="icon">📍</div>
        <div class="title">LOKASI</div>
        <div class="value">Pedurungan, Semarang</div>
    </div>
    <div class="info-card">
        <div class="icon">⏰</div>
        <div class="title">JAM BUKA</div>
        <div class="value">08.00 - 21.00 WIB</div>
    </div>
    <div class="info-card">
        <div class="icon">🚚</div>
        <div class="title">LAYANAN</div>
        <div class="value">Pickup & Delivery</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display messages directly (no box)
if len(st.session_state.chat) > 0:
    for role, msg in st.session_state.chat:
        if role == "Anda":
            st.markdown(f"""
            <div class="message user">
                <div class="message-avatar">👤</div>
                <div class="message-content">{msg}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message bot">
                <div class="message-avatar">🤖</div>
                <div class="message-content">{msg}</div>
            </div>
            """, unsafe_allow_html=True)

# Quick actions (suggested questions)
if len(st.session_state.chat) == 0:
    st.markdown("""
    <div class="quick-actions">
        <div class="quick-action">💰 Berapa harga cuci kilat?</div>
        <div class="quick-action">🚚 Apakah ada layanan antar jemput?</div>
        <div class="quick-action">⏱️ Berapa lama proses cuci?</div>
        <div class="quick-action">👔 Harga cuci jas berapa?</div>
    </div>
    """, unsafe_allow_html=True)

# Input area - vertical layout (input on top, button below)
user_input = st.text_input(
    "input",
    key="user_input",
    placeholder="Contoh: Berapa harga cuci komplit 5kg?",
    label_visibility="collapsed"
)

send_clicked = st.button("✈️ Kirim Pesan")

if send_clicked and user_input.strip():
        try:
            # Add user message
            st.session_state.chat.append(("Anda", user_input))
            
            # Call Groq API
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=500,
            )
            
            response_text = chat_completion.choices[0].message.content
            st.session_state.chat.append(("BubbleWash", response_text))
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {str(e)}")