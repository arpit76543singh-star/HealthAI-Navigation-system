import base64
from io import BytesIO
import qrcode
from urllib.parse import urlencode
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="HealthAI | Smart Healthcare",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
DOCTOR_IMAGE = BASE_DIR / "assets" / "doctor.png"

st.markdown("""
<style>


/* Fit the login page within one screen */

@media (min-width: 801px) {
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.3rem !important;
    }

    div[data-testid="stHorizontalBlock"] {
        align-items: flex-start !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        margin-top: -120px !important;
    }
}






    .hero-title {
        font-size: clamp(32px, 3.2vw, 48px);
        line-height: 1.05;
    }

    .hero-sub {
        font-size: 15px;
        line-height: 1.4;
    }

    .brand {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1px;
}

    .tagline {
        font-size: 11px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 12px;
        border-radius: 18px;
    }

    .stTextInput input {
        min-height: 40px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 40px;
    }
}


@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
      radial-gradient(ellipse at 20% 45%, #06352f 0%, transparent 35%),
      radial-gradient(ellipse at 85% 30%, #062b32 0%, transparent 35%),
      #02080d;
    color: #f5fbfc;
}
html, body, [class*="css"] {font-family: Inter, sans-serif;}
.block-container {max-width:1500px; padding-top:1.4rem;}
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background:transparent;}
h1,h2,h3,h4,p,label {color:#f5fbfc;}

.brand {font-size:32px;font-weight:800;letter-spacing:-1px;}
.brand span {color:#00e5a0;}
.tagline {font-size:13px;color:#a9bec4;margin-top:-6px;}

/* ===== HEALTHAI DOCTOR HOLOGRAM ===== */


/* Doctor image centered inside hologram */
.holo-stage {
    position: relative;
    width: 100%;
    max-width: 420px;
    height: 390px;
    margin: 10px auto 0;
    overflow: hidden;
    isolation: isolate;
}

.doctor-holo {
    position: absolute;
    z-index: 2;
    left: 50%;
    top: 46%;
    transform: translate(-50%, -50%);
    width: 220px;
    height: 260px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: 48% 48% 18% 18%;
    border: 1px solid #00e5ff80;
    background: radial-gradient(
        circle,
        #00e5ff20,
        #03192380 70%
    );
    box-shadow: 0 0 25px #00e5ff30;
}

.doctor-holo img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: contain;
    object-position: center;
    filter: drop-shadow(0 0 10px #00e5ff40);
}

.holo-ring {
    z-index: 3;
    pointer-events: none;
}

.holo-glow {
    z-index: 1;
    pointer-events: none;
}

.medical-symbol {
    z-index: 4;
    pointer-events: none;
}

.holo-caption {
    z-index: 5;
}


.holo-glow {
    position: absolute;
    width: 72%;
    height: 72%;
    left: 14%;
    top: 12%;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        #00e5ff38 0%,
        #00e5a018 38%,
        transparent 72%
    );
    filter: blur(22px);
    animation: holoPulse 3s ease-in-out infinite;
}

.holo-ring {
    position: absolute;
    left: 50%;
    top: 52%;
    border: 1px solid #00e5ff80;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 14px #00e5ff30,
                inset 0 0 12px #00e5ff16;
}

.ring-one {
    width: 270px;
    height: 270px;
    animation: holoRotate 14s linear infinite;
}

.ring-two {
    width: 320px;
    height: 190px;
    border-color: #00e5a080;
    animation: holoRotate 10s linear infinite reverse;
}

.ring-three {
    width: 220px;
    height: 320px;
    border-style: dashed;
    border-color: #39d9ff65;
    animation: holoRotate 18s linear infinite;
}

.medical-symbol {
    position: absolute;
    color: #61f7ff;
    font-size: 27px;
    font-weight: 700;
    text-shadow: 0 0 12px #00e5ff,
                 0 0 25px #00e5ff80;
    animation: holoFloat 3.5s ease-in-out infinite;
}

.symbol-heart {
    left: 13%;
    top: 28%;
}

.symbol-plus {
    right: 13%;
    top: 35%;
    animation-delay: .7s;
}

.symbol-pulse {
    left: 18%;
    bottom: 24%;
    animation-delay: 1.2s;
}

.symbol-cross {
    right: 18%;
    bottom: 27%;
    animation-delay: 1.7s;
}

.holo-caption {
    position: absolute;
    left: 50%;
    bottom: 3px;
    transform: translateX(-50%);
    white-space: nowrap;
    padding: 8px 14px;
    border: 1px solid #00e5ff65;
    border-radius: 30px;
    background: #031923e8;
    color: #91faff;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    box-shadow: 0 0 18px #00e5ff20;
}

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    margin-right: 7px;
    border-radius: 50%;
    background: #00ffc3;
    box-shadow: 0 0 10px #00ffc3;
    animation: holoBlink 1.5s ease-in-out infinite;
}

@keyframes holoPulse {
    0%, 100% {
        opacity: .55;
        transform: scale(.94);
    }
    50% {
        opacity: 1;
        transform: scale(1.06);
    }
}

@keyframes holoRotate {
    from {
        transform: translate(-50%, -50%) rotate(0deg);
    }
    to {
        transform: translate(-50%, -50%) rotate(360deg);
    }
}

@keyframes holoFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-12px);
    }
}

@keyframes holoBlink {
    0%, 100% { opacity: 1; }
    50% { opacity: .35; }
}

@media (prefers-reduced-motion: reduce) {
    .holo-glow,
    .holo-ring,
    .medical-symbol,
    .status-dot {
        animation: none !important;
    }
}


.hero-title {
    font-size:clamp(38px,4vw,62px);
    font-weight:800;
    line-height:1.08;
    letter-spacing:-2px;
}
.hero-title span {
    color:#00e5a0;
    text-shadow:0 0 24px #00e5a055;
}
.hero-sub {
    font-size:18px;
    line-height:1.6;
    color:#bed0d5;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background:linear-gradient(145deg,#062020,#06101a);
    border:1px solid #00bfa0;
    border-radius:24px;
    box-shadow:0 0 24px #00e5a022;
    padding:18px;
}
.stButton>button, .stFormSubmitButton>button {
    min-height:47px;
    border:1px solid #00e5a0;
    border-radius:12px;
    background:linear-gradient(100deg,#00e5a0,#00cbbd,#318cff);
    color:#00140f;
    font-weight:800;
    transition:all .2s ease;
}
.stButton>button:hover, .stFormSubmitButton>button:hover {
    box-shadow:0 0 24px #00e5a066;
    border-color:#65fff0;
    transform:translateY(-2px);
}
.stTextInput input {
    background:#04131b!important;
    color:white!important;
    border:1px solid #24545e!important;
    border-radius:12px!important;
    min-height:46px;
}
.stTextInput input:focus {
    border-color:#00e5a0!important;
    box-shadow:0 0 0 1px #00e5a044!important;
}
div[data-baseweb="tab-list"] {gap:8px;}
button[data-baseweb="tab"] {color:#d5e5e8!important;}
button[data-baseweb="tab"][aria-selected="true"] {
    color:#00150f!important;
    background:linear-gradient(90deg,#00e5a0,#20dce8)!important;
    border-radius:10px;
}
div[data-testid="stMetric"] {
    background:#07191e;
    border:1px solid #14534a;
    border-radius:14px;
    padding:14px;
}
div[data-testid="stMetricValue"] {color:#00e5a0;}
@media(max-width:800px) {
    .block-container {padding-left:1rem;padding-right:1rem;}
    .hero-title {letter-spacing:-1px;}
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ================= LOGIN PAGE =================
if not st.session_state.logged_in:

    # No top navbar and no bottom feature cards on login page.
    st.markdown(
        '<div class="brand">♡ Health<span>AI</span></div>'
        '<div class="tagline">Smart Healthcare • Better Tomorrow</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns(
    [1.0, 0.95],
    gap="large",
    vertical_alignment="top"
)

    with left:
        st.markdown(
            '<div style="color:#3fffc1;font-size:12px;'
            'letter-spacing:2px;font-weight:700">'
            '✦ YOUR DIGITAL HEALTHCARE COMPANION</div>'
            '<div class="hero-title">Your Health,'
            'Our <span>Priority.</span></div>'
            '<div class="hero-sub">AI-Powered Healthcare Assistant<br>'
            'for a Healthier Tomorrow</div>',
            unsafe_allow_html=True,
        )
        st.write("")

        if DOCTOR_IMAGE.exists():
                       st.image(str(DOCTOR_IMAGE), width=356)
        else:
            st.warning(
                "Doctor image missing. Save it at assets/doctor.png"
            )

    with right:
        with st.container(border=True):
            icon_col, title_col = st.columns([0.8, 2.5])

            with icon_col:
                st.markdown(
                    "<div style='font-size:55px;color:#00e5a0'>♡</div>",
                    unsafe_allow_html=True,
                )

            with title_col:
                st.markdown("## Welcome Back")
                st.caption("Sign in to continue your health journey")

            login_tab, signup_tab = st.tabs(["👤 Login", "✚ Sign Up"])

            with login_tab:
                with st.form("login_form"):
                    email = st.text_input(
                        "Email Address",
                        placeholder="you@example.com",
                    )
                    password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Enter your password",
                    )
                    remember = st.checkbox("Remember Me")

                    submitted = st.form_submit_button(
                        "↪  Sign In",
                        use_container_width=True,
                    )

                    if submitted:
                        if not email.strip() or not password:
                            st.error("Enter your email and password.")
                        else:
                            # Demo navigation only, not secure authentication.
                            st.session_state.user_email = email.strip()
                            st.session_state.logged_in = True
                            st.rerun()

                st.caption(
                    "Demo only: credentials are not verified or stored "
                    "in a secure authentication system."
                )

            with signup_tab:
                with st.form("signup_form"):
                    full_name = st.text_input(
                        "Full Name", placeholder="Your full name"
                    )
                    new_email = st.text_input(
                        "Email Address",
                        placeholder="you@example.com",
                        key="signup_email",
                    )
                    new_password = st.text_input(
                        "Create Password",
                        type="password",
                        key="signup_password",
                    )
                    confirm_password = st.text_input(
                        "Confirm Password", type="password"
                    )
                    accepted = st.checkbox(
                        "I agree to the terms and privacy notice."
                    )

                    create = st.form_submit_button(
                        "✚  Create Account",
                        use_container_width=True,
                    )

                    if create:
                        if not full_name.strip() or not new_email.strip() or not new_password:
                            st.error("Please complete all required fields.")
                        elif new_password != confirm_password:
                            st.error("Passwords do not match.")
                        elif not accepted:
                            st.error("Please accept the terms.")
                        else:
                            st.success(
                                "Form validation passed. Account creation "
                                "backend is not connected yet."
                            )

            st.markdown("---")
           

    st.markdown("---")
    st.caption("© 2026 HealthAI. All rights reserved.")

# ================= HOME DASHBOARD =================

   
else:
    st.markdown("""
    <style>
    .block-container {
        max-width: 1600px;
        padding-top: 0.6rem !important;
        padding-bottom: 0.5rem !important;
    }

    .health-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        padding: 12px 18px;
        margin-bottom: 20px;
        border: 1px solid #075064;
        border-radius: 24px;
        background: linear-gradient(100deg, #03121e, #041c2a);
        box-shadow: 0 0 20px #00e5c318;
    }

    .health-brand {
        font-size: 29px;
        font-weight: 800;
        letter-spacing: -1px;
        white-space: nowrap;
    }

    .health-brand span {
        color: #00e5c3;
    }

    .health-tagline {
        font-size: 10px;
        color: #a9c5ce;
        margin-top: -4px;
        white-space: nowrap;
    }

    div[data-testid="stButton"] > button {
        min-height: 43px;
        padding: 5px 7px;
        border-radius: 14px;
        border: 1px solid transparent;
        background: transparent;
        color: #e7f6fa;
        font-size: 13px;
        font-weight: 650;
        white-space: nowrap;
        box-shadow: none;
        transform: none;
    }

    div[data-testid="stButton"] > button:hover {
        border-color: #00e5c3;
        background: #063442;
        color: #45ffe0;
        box-shadow: 0 0 15px #00e5c322;
        transform: none;
    }

    @media(max-width: 1000px) {
        .health-brand { font-size: 23px; }
        div[data-testid="stButton"] > button {
            font-size: 11px;
            white-space: normal;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    nav_title, nav1, nav2, nav3, nav4, nav5, nav_profile = st.columns(
        [2.0, 0.85, 1.25, 1.1, 1.35, 1.55, 0.85],
        gap="small",
        vertical_alignment="center",
    )

    with nav_title:
        st.markdown(
            '<div class="health-brand">♡ Health<span>AI</span></div>'
            '<div class="health-tagline">Smart • Simple • Accessible</div>',
            unsafe_allow_html=True,
        )

    pages = [
        ("🏠 Home", "Home", nav1),
        ("🩺 Acute Disease", "Acute Disease", nav2),
        ("🤖 AI Assistant", "AI Assistant", nav3),
        ("📍 Hospital Finder", "Hospital Finder", nav4),
        ("📅 Book Appointment", "Book Appointment", nav5),
    ]

    for button_label, page_name, col in pages:
        with col:
            if st.button(
                button_label,
                key=f"nav_{page_name}",
                use_container_width=True,
            ):
                st.session_state.active_page = page_name
                st.rerun()

    with nav_profile:
        with st.popover("👤 ▾", use_container_width=True):
            st.markdown("### My Account")
            st.caption(st.session_state.user_email)

            if st.button("👤 My Profile", use_container_width=True):
                st.session_state.active_page = "User Profile"
                st.rerun()

            if st.button("✏️ Edit Profile", use_container_width=True):
                st.session_state.active_page = "Edit Profile"
                st.rerun()

            if st.button("↪ Sign Out", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user_email = ""
                st.rerun()

    active = st.session_state.get("active_page", "Home")


    
    # ================= HOME HERO SECTION =================
    if active == "Home":
        hero_left, hero_right = st.columns(
            [1.15, 0.85],
            gap="large",
            vertical_alignment="center",
        )

        with hero_left:
            st.markdown("""
            <div style="
                display:inline-block;
                padding:8px 14px;
                border:1px solid #087d79;
                border-radius:30px;
                background:#062a30;
                color:#53f5d6;
                font-size:12px;
                font-weight:700;
                letter-spacing:1.5px;
                 margin-top:30px;
                margin-bottom:18px;">
                ✦ AI-POWERED HEALTHCARE
            </div>

            <div class="hero-title">
                Your Health,<br>
                <span>Our Priority.</span>
            </div>

            <div class="hero-sub" style="margin-top:18px;">
                Experience smarter healthcare with AI-powered health
                guidance, healthcare navigation, and easy appointment
                requests — all in one place.
            </div>
            """, unsafe_allow_html=True)

            st.write("")

            action1, action2 = st.columns(2)

            with action1:
                if st.button(
                    "✦ Explore HealthAI",
                    key="hero_explore",
                    use_container_width=True,
                ):
                    st.session_state.active_page = "Acute Disease"
                    st.rerun()

            with action2:
                if st.button(
                    "⌖ Find a Hospital",
                    key="hero_hospital",
                    use_container_width=True,
                ):
                    st.session_state.active_page = "Hospital Finder"
                    st.rerun()

        
        

       
        with hero_right:
            doctor_image_url = (
                DOCTOR_IMAGE.resolve().as_uri()
                if DOCTOR_IMAGE.exists()
                else ""
            )

            st.html(f"""
            <div class="holo-stage">
                <div class="holo-glow"></div>
                <div class="holo-ring ring-one"></div>
                <div class="holo-ring ring-two"></div>
                <div class="holo-ring ring-three"></div>

                <div class="doctor-holo">
                    {"<img src='" + doctor_image_url + "' alt='Doctor' />" if doctor_image_url else "<div class='doctor-placeholder'>🩺</div>"}
                </div>

                <div class="medical-symbol symbol-heart">♡</div>
                <div class="medical-symbol symbol-plus">＋</div>
                <div class="medical-symbol symbol-pulse">⌁</div>
                <div class="medical-symbol symbol-cross">✚</div>

                <div class="holo-caption">
                    <span class="status-dot"></span>
                    AI HEALTHCARE ASSISTANT
                </div>
            </div>
            """)


       
        



    else:
        st.markdown("---")
        st.markdown(
            f'<div class="hero-title">Welcome to <span>HealthAI.</span></div>'
            f'<div class="hero-sub">{active} · Your healthcare workspace</div>',
            unsafe_allow_html=True,
        )


    st.markdown("""
    <style>
    div[data-testid="stImage"] {
        margin-bottom: -25px;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.6rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    div[data-testid="stImage"] {
        margin-bottom: -25px;
    }
    </style>
    """, unsafe_allow_html=True)

    if active == "Home":
        
       
        # =============== HEALTHCARE SERVICES ===============
        st.markdown("""
        <style>
        .services-heading {
            font-size: 27px;
            font-weight: 800;
            color: #f2f8ff;
            margin: 0 0 18px 0;
            padding-left: 15px;
            border-left: 6px solid #00e5c3;
        }

        .service-card {
            height: 154px;
            padding: 17px 14px;
            border: 1px solid #087e91;
            border-radius: 22px;
            background: linear-gradient(145deg, #062a3a, #031622);
            box-shadow: inset 0 0 18px #00d9ff08;
            transition: all .25s ease;
        }

        .service-card:hover {
            border-color: #00f5d0;
            box-shadow: 0 0 22px #00e5c333;
            transform: translateY(-4px);
        }

        .service-icon {
            font-size: 32px;
            color: #00e5c3;
            margin-bottom: 10px;
        }

        .service-title {
            font-size: 16px;
            font-weight: 800;
            color: #f4f9ff;
            margin-bottom: 5px;
        }

        .service-desc {
            color: #c0d4e2;
            font-size: 12px;
            line-height: 1.45;
        }

        .service-card.sos {
            border-color: #f04455;
            background: linear-gradient(145deg, #321b28, #17131f);
            box-shadow: inset 0 0 22px #ff455508;
        }

        .service-card.sos .service-icon {
            color: #ff626b;
        }

        .service-card.sos:hover {
            border-color: #ff626b;
            box-shadow: 0 0 22px #ff455533;
        }

        div[data-testid="stButton"] button {
            border-radius: 18px;
            min-height: 36px;
            font-weight: 700;
            border: 1px solid #087e91;
        }

        div[data-testid="stButton"] button:hover {
            border-color: #00e5c3;
            color: #00e5c3;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div class="services-heading">Healthcare Services</div>',
            unsafe_allow_html=True,
        )

        services = [
            (
                "🩺", "Disease Guidance",
                "Symptoms and warning signs",
                "Acute Disease", False
            ),
            (
                "💬", "AI Assistant",
                "Ask health-related questions",
                "AI Assistant", False
            ),
            (
                "📍", "Hospital Finder",
                "Find nearby hospitals",
                "Hospital Finder", False
            ),
            (
                "📅", "Book Appointment",
                "Consultation request",
                "Book Appointment", False
            ),
            (
                "🚨", "Emergency SOS",
                "Get help in emergency",
                "Emergency SOS", True
            ),
        ]

        card_columns = st.columns(
            [1, 1, 1, 1.15, 1.15],
            gap="small",
        )

        for col, service in zip(card_columns, services):
            emoji, title, desc, destination, is_sos = service

            with col:
                card_class = "service-card sos" if is_sos else "service-card"

                st.markdown(
                    f"""
                    <div class="{card_class}">
                        <div class="service-icon">{emoji}</div>
                        <div class="service-title">{title}</div>
                        <div class="service-desc">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    "➜  Open service",
                    key=f"service_{destination}",
                    use_container_width=True,
                ):
                    if destination == "Emergency SOS":
                        st.warning(
                            "For an immediate emergency in India, "
                            "call 112. Automated SOS messaging is "
                            "not activated by this button."
                        )
                    else:
                        st.session_state.active_page = destination
                        st.rerun()

        st.markdown("""
        <div style="
            margin-top:18px;
            padding:18px 24px;
            border:1px solid #e94455;
            border-radius:22px;
            background:linear-gradient(100deg,#321a27,#171622);
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:16px;
            flex-wrap:wrap;
        ">
            <div>
                <div style="
                    color:#ff8b92;
                    font-size:21px;
                    font-weight:800;
                    margin-bottom:5px;
                ">🛡️ Emergency SOS — Always here for you!</div>
                <div style="color:#f0dfe5;font-size:14px;">
                    In case of emergency, get immediate help.
                </div>
            </div>
           <a href="tel:112" style="
                display:inline-block;
                padding:12px 26px;
                border-radius:30px;
                background:#f04455;
                color:white;
                font-size:16px;
                font-weight:800;
                text-decoration:none;
                white-space:nowrap;
            ">☎ Call 112</a>
        </div>
        """, unsafe_allow_html=True)


    
    
    elif active == "Acute Disease":
        st.subheader("🩺 Acute Disease Guidance")
        st.write("Select a condition to view general care guidance.")

        disease_info = {
            "Fever": {
                "precautions": [
                    "Rest karo aur fluids lete raho.",
                    "Temperature monitor karo.",
                    "Bina medical advice ke antibiotics mat lo."
                ],
                "warning": "Saans lene mein dikkat, confusion, severe headache ya rapidly worsening symptoms hon toh urgent medical help lo."
            },
            "Common Cold": {
                "precautions": [
                    "Rest aur adequate fluids lo.",
                    "Haath regularly wash karo aur doosron ke saath utensils share mat karo.",
                    "Smoke aur doosre irritants se bacho."
                ],
                "warning": "Breathing difficulty, chest pain ya symptoms bahut zyada worsen hon toh medical help lo."
            },
            "Cough": {
                "precautions": [
                    "Fluids lo aur rest karo.",
                    "Smoke aur dust jaise irritants se bacho.",
                    "Cough medicine lene se pehle pharmacist ya clinician se advice lo."
                ],
                "warning": "Breathing difficulty, chest pain ya blood in cough ho toh urgent medical assessment lo."
            },
            "Headache": {
                "precautions": [
                    "Paani piyo aur regular rest lo.",
                    "Screen se breaks lo aur meals skip mat karo.",
                    "Painkillers ko label aur clinician ki advice ke according hi use karo."
                ],
                "warning": "Achanak bahut severe headache, weakness, confusion ya vision/speech changes hon toh emergency care lo."
            },
            "Migraine": {
                "precautions": [
                    "Shaant, dark room mein rest karne ki koshish karo.",
                    "Regular meals, hydration aur sleep maintain karo.",
                    "Known triggers ko note karo."
                ],
                "warning": "Pehli baar severe headache ya unusual neurological symptoms hon toh urgent medical care lo."
            },
            "Diarrhoea": {
                "precautions": [
                    "ORS ko packet instructions ke according prepare karke sip karo.",
                    "Fluids lete raho aur hand hygiene maintain karo.",
                    "Dehydration ke signs par dhyan do."
                ],
                "warning": "Blood in stool, severe abdominal pain, fainting ya dehydration ho toh promptly medical care lo."
            },
            "Vomiting": {
                "precautions": [
                    "Chhote-chhote sips mein fluids ya ORS lo, agar tolerate ho.",
                    "Rest karo aur dehydration ke signs monitor karo.",
                    "Persistent vomiting mein clinician se advice lo."
                ],
                "warning": "Fluids bilkul retain na hon, severe pain, confusion ya blood in vomit ho toh urgent care lo."
            },
            "Sore Throat": {
                "precautions": [
                    "Fluids lo aur rest karo.",
                    "Warm salt-water gargle try kar sakte ho, agar safely gargle kar sakte ho.",
                    "Smoke aur irritants se bacho."
                ],
                "warning": "Breathing ya swallowing mein severe difficulty ho toh emergency help lo."
            },
            "Food Poisoning": {
                "precautions": [
                    "ORS aur fluids se hydration maintain karo.",
                    "Rest karo aur hand hygiene rakho.",
                    "Bina medical advice ke antibiotics mat lo."
                ],
                "warning": "Bloody diarrhoea, severe pain, high fever ya dehydration ho toh prompt medical care lo."
            },
            "Allergic Reaction": {
                "precautions": [
                    "Agar safe ho toh suspected trigger se door ho jao.",
                    "Symptoms ko closely monitor karo.",
                    "Prescribed allergy treatment ko clinician ke instructions ke according use karo."
                ],
                "warning": "Saans lene mein dikkat, tongue/throat swelling ya fainting ho toh emergency services call karo. Prescribed epinephrine auto-injector ho toh instructions ke according use karo."
            }
        }

        disease = st.selectbox(
            "Select a disease or condition",
            ["Select a condition"] + list(disease_info.keys())
        )

        if disease != "Select a condition":
            info = disease_info[disease]

            st.markdown("---")
            st.markdown(f"### 📋 Precautions for {disease}")

            for precaution in info["precautions"]:
                st.markdown(f"- {precaution}")

            st.markdown("### ⚠️ Warning Signs")
            st.warning(info["warning"])

           
            st.caption(
                "Educational guidance only; this is not a diagnosis. "
                "Advice may differ by age and medical history."
            )



    
    
    elif active == "AI Assistant":
        from google import genai
        from google.genai import types

        st.subheader("HealthAI Assistant")
        st.caption(
            "Ask health-related questions in natural language. "
            "You can ask follow-up questions too."
        )

        if "health_chat" not in st.session_state:
            st.session_state.health_chat = []

        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown("**Chat with HealthAI**")
        with col2:
            if st.button("Clear chat", use_container_width=True):
                st.session_state.health_chat = []
                st.rerun()

        for message in st.session_state.health_chat:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input(
            "Ask about symptoms, anaemia, nutrition, or health..."
        )

        if prompt:
            st.session_state.health_chat.append(
                {"role": "user", "content": prompt}
            )

            with st.chat_message("user"):
                st.markdown(prompt)

            system_instruction = """
            You are HealthAI, a careful health education assistant.

            - Answer natural-language questions clearly and helpfully.
            - Support English and Hindi/Hinglish.
            - Use the previous conversation to answer follow-up questions.
            - Explain health topics, symptoms, prevention, nutrition,
              and common medical terms in easy language.
            - Do not claim to diagnose a disease or replace a clinician.
            - Do not invent test results, medical facts, or certainty.
            - For possible emergencies, advise immediate medical help.
              In India, call 112 for emergencies when appropriate.
            - Do not recommend prescription medicines or personalised
              doses without qualified medical supervision.
            - Ask relevant clarifying questions when necessary.
            - Protect privacy; do not request unnecessary personal data.
            - Keep answers organised and understandable.
            - Remind users that online information cannot confirm
              a diagnosis when relevant.
            """

            try:
                client = genai.Client(
                    api_key=st.secrets["GEMINI_API_KEY"]
                )

                conversation = []
                for message in st.session_state.health_chat[-12:]:
                    role = (
                        "model" if message["role"] == "assistant"
                        else "user"
                    )
                    conversation.append(
                        types.Content(
                            role=role,
                            parts=[types.Part(text=message["content"])]
                        )
                    )

                with st.chat_message("assistant"):
                    with st.spinner("HealthAI is thinking..."):
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=conversation,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.4,
                            ),
                        )

                        answer = response.text or (
                            "I couldn't generate a response. "
                            "Please try asking in a different way."
                        )
                        st.markdown(answer)

                st.session_state.health_chat.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception:
                st.error(
                    "HealthAI couldn't connect right now. "
                    "Please try again shortly."
                )

        st.caption(
            "HealthAI provides educational information, not a diagnosis "
            "or a substitute for professional medical care."
        )


    
    
   
   
    elif active == "Hospital Finder":
        from urllib.parse import quote_plus

        st.subheader("🏥 Hospital Finder")
        st.write("Find hospitals by city, PIN code, or current location.")

        search_mode = st.radio(
            "Choose search method",
            ["City / PIN Code", "📍 Use Current Location"],
            horizontal=True,
            key="hospital_search_mode",
        )

        if search_mode == "City / PIN Code":
            with st.form("hospital_search_form"):
                city = st.text_input(
                    "Enter city or PIN code",
                    placeholder="e.g. Lucknow or 226001",
                )
                search_hospitals = st.form_submit_button(
                    "🔍 Find Hospitals",
                    use_container_width=True,
                )

            if search_hospitals:
                location = city.strip()

                if not location:
                    st.warning("Please enter a city or PIN code.")
                else:
                    query = quote_plus(f"hospitals in {location}, India")
                    maps_url = (
                        "https://www.google.com/maps/search/?api=1"
                        f"&query={query}"
                    )
                    st.link_button(
                        "📍 Open Hospitals in Google Maps",
                        maps_url,
                        use_container_width=True,
                    )
        else:
            st.info(
                "Click below to open Google Maps and allow location "
                "access in your browser if prompted."
            )
            current_location_url = (
                "https://www.google.com/maps/search/hospitals/"
                "@?api=1"
            )
            st.link_button(
                "📍 Open Google Maps for Nearby Hospitals",
                current_location_url,
                use_container_width=True,
            )
            st.caption(
                "Google Maps may use your device location if location "
                "services and browser permissions are enabled."
            )

   
    elif active == "Book Appointment":
        import streamlit as st
        from datetime import date, time

        st.subheader("📅 Book Appointment")
        st.caption("Schedule your healthcare consultation with HealthAI.")

        st.markdown("""
        <div style="background:linear-gradient(135deg,#10243A,#164E63);
        padding:22px;border-radius:16px;color:white;">
            <h3 style="margin:0;">Your Health, Our Priority</h3>
            <p>Consultation booking</p>
            <h2 style="color:#67E8F9;margin-bottom:0;">Fee: ₹200</h2>
        </div>
        """, unsafe_allow_html=True)

        st.write("### 👤 Patient Details")

        with st.form("healthai_appointment_form"):
            patient_name = st.text_input("Patient Full Name")
            patient_phone = st.text_input("Mobile Number")
            patient_email = st.text_input("Email (optional)")

            appointment_type = st.radio(
                "Consultation Type",
                ["In-Person Consultation", "Online Consultation"],
                horizontal=True,
            )

            doctor_specialty = st.selectbox(
                "Select Specialist",
                [
                    "General Physician",
                    "Cardiologist",
                    "Dermatologist",
                    "Neurologist",
                    "Other / Not Sure",
                ],
            )

            appointment_date = st.date_input(
                "Preferred Appointment Date",
                min_value=date.today(),
            )

            appointment_time = st.selectbox(
                "Preferred Time",
                [
                    "10:00 AM", "11:00 AM", "12:00 PM",
                    "02:00 PM", "03:00 PM", "04:00 PM",
                ],
            )

            notes = st.text_area(
                "Reason for consultation (optional)"
            )

            submitted = st.form_submit_button(
                "Continue to ₹200 Payment",
                use_container_width=True,
            )

        if submitted:
            if not patient_name.strip():
                st.error("Please enter the patient's name.")
            elif not patient_phone.strip().isdigit() or len(patient_phone.strip()) != 10:
                st.error("Please enter a valid 10-digit mobile number.")
            elif appointment_date < date.today():
                st.error("Please select a valid appointment date.")
            else:
                st.session_state["pending_appointment"] = {
                    "patient_name": patient_name.strip(),
                    "patient_phone": patient_phone.strip(),
                    "patient_email": patient_email.strip(),
                    "appointment_type": appointment_type,
                    "doctor_specialty": doctor_specialty,
                    "appointment_date": str(appointment_date),
                    "appointment_time": appointment_time,
                    "notes": notes.strip(),
                    "amount": 200,
                }
                st.session_state["show_appointment_payment"] = True

           

        if st.session_state.get("show_appointment_payment", False):
            st.divider()
            st.subheader("💳 Pay Consultation Fee — ₹200")

            RECEIVER_UPI_ID = "8381905680@ybl"
            RECEIVER_NAME = "HealthAI"

            upi_params = {
                "pa": RECEIVER_UPI_ID,
                "pn": RECEIVER_NAME,
                "am": "200.00",
                "cu": "INR",
                "tn": "HealthAI Appointment Fee",
            }

            upi_link = "upi://pay?" + urlencode(upi_params)

            st.metric("Total Appointment Fee", "₹200")

            qr_image = qrcode.make(upi_link)
            qr_buffer = BytesIO()
            qr_image.save(qr_buffer, format="PNG")

            st.image(
                qr_buffer.getvalue(),
                caption="Scan using PhonePe or Google Pay",
                width=280,
            )

            st.write("**UPI ID:**", RECEIVER_UPI_ID)

            st.info(
                "Scan the QR code and check that ₹200 is pre-filled. "
                "Verify the recipient before approving payment."
            )

            st.warning(
                "Payment is not automatically verified. "
                "Your appointment remains pending until trusted "
                "payment verification is connected."
            )
        

    st.markdown("---")
    st.caption(
        "HealthAI prototype · No secure authentication, real diagnosis, "
        "hospital API, payment processing or emergency messaging connected."
    )
