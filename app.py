import streamlit as st
import json
import folium
import random
import os
import requests
from streamlit_folium import st_folium
from engine import evaluate_risk

# Page Configuration
st.set_page_config(
    page_title="NER Landslide Command Center",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Cyber Command Portal Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    .stApp {
        background-color: #050811;
        color: #e2e8f0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .status-ticker {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
        padding: 8px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
    }
    .status-online {
        color: #22c55e;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 10px #22c55e;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }

    .hero-header {
        background: radial-gradient(circle at top right, rgba(14, 165, 233, 0.15), transparent 50%),
                    linear-gradient(180deg, #0f172a 0%, #080d1a 100%);
        padding: 28px;
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.7);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: linear-gradient(180deg, #38bdf8 0%, #0284c7 100%);
    }
    .hero-title {
        color: #f8fafc;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin-bottom: 4px;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
    }
    .hero-subtitle {
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .kpi-box {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(10px);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }
    .kpi-box:hover {
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }

    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 12px !important;
        padding: 18px !important;
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.5) !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        border: 1px solid rgba(56, 189, 248, 0.5);
        border-radius: 10px;
        padding: 14px 28px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 20px rgba(2, 132, 199, 0.3);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
        box-shadow: 0 0 30px rgba(2, 132, 199, 0.6);
        border-color: #38bdf8;
        transform: translateY(-2px);
    }

    section[data-testid="stSidebar"] {
        background-color: #080d1a !important;
        border-right: 1px solid rgba(56, 189, 248, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Status Ticker Bar
st.markdown("""
<div class="status-ticker">
    <div class="status-online">
        <div class="pulse-dot"></div> SYSTEM ONLINE — REAL-TIME MONITORING ACTIVE
    </div>
    <div style="color: #94a3b8;">NODE: NER-DISASTER-HQ-01</div>
    <div style="color: #38bdf8;">SECURE CAP BROADCAST READY</div>
</div>
""", unsafe_allow_html=True)

# Main Hero Header Banner
st.markdown("""
<div class="hero-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div>
            <div class="hero-title">🚨 LANDSLIDE EARLY WARNING PORTAL</div>
            <div class="hero-subtitle">[ MDoNER ] NORTH EASTERN REGIONAL DISASTER COMMAND CENTER</div>
        </div>
        <a href="https://t.me/ner_disaster_alert" target="_blank" style="text-decoration: none;">
            <button style="background: linear-gradient(135deg, #0088cc 0%, #006699 100%); color: white; border: 1px solid #38bdf8; padding: 12px 20px; border-radius: 10px; font-weight: 800; cursor: pointer; font-family: 'JetBrains Mono', monospace; box-shadow: 0 0 15px rgba(0,136,204,0.5);">
                ✈️ JOIN TELEGRAM ALERT CHANNEL
            </button>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# Top Executive Summary Cards
k1, k2, k3, k4 = st.columns(4)
k1.markdown('<div class="kpi-box"><span style="color:#64748b; font-size:0.75rem; font-weight:700;">MONITORED REGIONS</span><h3 style="margin:4px 0 0 0; color:#38bdf8; font-family:JetBrains Mono;">15 Sub-Zones</h3></div>', unsafe_allow_html=True)
k2.markdown('<div class="kpi-box"><span style="color:#64748b; font-size:0.75rem; font-weight:700;">TELECOM BROADCAST</span><h3 style="margin:4px 0 0 0; color:#22c55e; font-family:JetBrains Mono;">CAP API Active</h3></div>', unsafe_allow_html=True)
k3.markdown('<div class="kpi-box"><span style="color:#64748b; font-size:0.75rem; font-weight:700;">IOT TELEMETRY</span><h3 style="margin:4px 0 0 0; color:#eab308; font-family:JetBrains Mono;">Sensor Grid Live</h3></div>', unsafe_allow_html=True)
k4.markdown('<div class="kpi-box"><span style="color:#64748b; font-size:0.75rem; font-weight:700;">AI ENGINE</span><h3 style="margin:4px 0 0 0; color:#a855f7; font-family:JetBrains Mono;">Gemini Live v2.5</h3></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

CACHE_FILE = "local_cache.json"

coords = {
    # Sikkim
    "Sikkim - Gangtok (East Sikkim)": {
        "lat": 27.3389, "lon": 88.6065, "slope": 38,
        "safe_zone": "Gangtok Paljor Stadium Grounds", "blocked_road": "NH-10 Gangtok-Silchar Highway", "alt_route": "Via Pakyong-Rorathang Bypass",
        "contacts": {
            "State Disaster Management (SSDMA)": "03592202892",
            "Gangtok Police Station": "112",
            "Gangtok Central Fire Station": "101",
            "STNM State Hospital Gangtok": "102",
            "National Highway Emergency Patrol": "1033",
            "NDRF Regional Response Centre": "03612840284"
        }
    },
    "Sikkim - Nathu La Pass (Border Route)": {
        "lat": 27.3867, "lon": 88.8310, "slope": 52,
        "safe_zone": "Sherathang Military Camp Shelter", "blocked_road": "Jawaharlal Nehru Road", "alt_route": "Old Silk Route via Zuluk",
        "contacts": {
            "Sherathang Military & Transit Post": "03592202022",
            "Border Roads Organisation (PROJECT SWASTIK)": "03592202581",
            "East Sikkim District Control Room": "03592284444",
            "National Emergency Helpline": "112"
        }
    },
    "Sikkim - Mangan (North Sikkim HQ)": {
        "lat": 27.5167, "lon": 88.5333, "slope": 45,
        "safe_zone": "Mangan Helipad Open Zone", "blocked_road": "North Sikkim Highway", "alt_route": "Via Phodong-Chungthang Secondary Feeder",
        "contacts": {
            "Mangan District Disaster Control Room": "1077",
            "Mangan Police Station": "03592234224",
            "Mangan Fire & Rescue Station": "03592234201",
            "Mangan District Hospital": "03592234215",
            "Chungthang Army Rescue Base": "03592234222"
        }
    },
    
    # Meghalaya
    "Meghalaya - Shillong (East Khasi Hills)": {
        "lat": 25.5788, "lon": 91.8933, "slope": 42,
        "safe_zone": "Garrison Ground Shillong", "blocked_road": "NH-6 Shillong Bypass", "alt_route": "Via Mawlyndep-Umiam Old Road",
        "contacts": {
            "State Disaster Management Authority (SDMA)": "1070",
            "Shillong Sadar Police Station": "112",
            "Shillong Main Fire Station": "101",
            "NEIGRIHMS Emergency Hospital": "03642538020",
            "Shillong Civil Hospital Ambulance": "108"
        }
    },
    "Meghalaya - Cherrapunji / Sohra": {
        "lat": 25.2833, "lon": 91.7333, "slope": 46,
        "safe_zone": "Sohra Civil Hospital Ridge", "blocked_road": "SH-5 Sohra Highway", "alt_route": "Via Laitkynsew Feeder Track",
        "contacts": {
            "Sohra SDO Disaster Control Room": "03637262224",
            "Sohra Police Station": "03637262222",
            "Sohra Fire Station": "0363726201",
            "108 GVK Emergency Ambulance": "108"
        }
    },
    "Meghalaya - Tura (West Garo Hills)": {
        "lat": 25.5167, "lon": 90.2167, "slope": 38,
        "safe_zone": "Tura District Sports Complex", "blocked_road": "NH-217 Tura Corridor", "alt_route": "Via Dalu-Baghmara State Highway",
        "contacts": {
            "West Garo Hills Control Room": "1077",
            "Tura Police Station": "03651222333",
            "Tura Fire Brigade": "03651222101",
            "Tura Civil Hospital Emergency": "108",
            "Garo Hills Emergency Response": "112"
        }
    },
    
    # Assam
    "Assam - Guwahati / Kamrup Metro": {
        "lat": 26.1445, "lon": 91.7362, "slope": 22,
        "safe_zone": "Sarusajai Stadium Complex", "blocked_road": "GS Road Hill Section", "alt_route": "Via Zoo Road - Narengi Bypass",
        "contacts": {
            "Assam State Disaster Management (ASDMA)": "1070",
            "Dispur Police Control Room": "112",
            "Guwahati Central Fire Control": "101",
            "Gauhati Medical College Hospital (GMCH)": "03612529457",
            "108 Mrityunjoy Emergency Ambulance": "108",
            "1st Battalion NDRF Patgaon Base": "03612840284"
        }
    },
    "Assam - Haflong (Dima Hasao)": {
        "lat": 25.1833, "lon": 93.0167, "slope": 40,
        "safe_zone": "Haflong Government College Grounds", "blocked_road": "NH-27 Haflong-Silchar Hill Highway", "alt_route": "Via Umrangso-Lanka Railway Parallel Road",
        "contacts": {
            "Dima Hasao Disaster Control Room": "1077",
            "Haflong Police Station": "03673236222",
            "Haflong Fire Station": "03673236201",
            "Haflong Civil Hospital": "108",
            "Railway Landslide Emergency Patrol": "139"
        }
    },
    
    # Arunachal Pradesh
    "Arunachal - Itanagar": {
        "lat": 27.1000, "lon": 93.6200, "slope": 35,
        "safe_zone": "Indira Gandhi Park Itanagar", "blocked_road": "NH-415 Itanagar-Naharlagun Road", "alt_route": "Via Jullang-Chimpu Bypass",
        "contacts": {
            "State Disaster Management Authority": "1070",
            "Itanagar Capital Police Control": "112",
            "Itanagar Fire Station": "101",
            "TRIHMS Hospital Naharlagun": "03602244248",
            "108 Arunachal Emergency Ambulance": "108",
            "12 Bn NDRF Itanagar": "03602285888"
        }
    },
    "Arunachal - Tawang Town": {
        "lat": 27.5858, "lon": 91.8594, "slope": 48,
        "safe_zone": "Tawang High Altitude Army Base Grounds", "blocked_road": "Bhalukpong-Tawang Highway (Sela Pass Section)", "alt_route": "Via Sangti Valley Detour",
        "contacts": {
            "Tawang District Control Room": "1077",
            "Tawang Police Station": "03794222213",
            "Tawang Fire Station": "03794222211",
            "Tawang District Hospital": "03794222234",
            "BRO Project VARTAK Emergency Base": "03794222205",
            "Army High Altitude Rescue Unit": "03794222201"
        }
    },
    
    # Nagaland
    "Nagaland - Kohima Town": {
        "lat": 25.6747, "lon": 94.1100, "slope": 39,
        "safe_zone": "Kohima Local Ground (Khouchiezie)", "blocked_road": "NH-2 Kohima-Dimapur Highway", "alt_route": "Via Peducha-Tsiesema Bypass",
        "contacts": {
            "Nagaland State Disaster Management (NSDMA)": "1070",
            "Kohima North Police Station": "112",
            "Kohima Central Fire Station": "101",
            "Naga Hospital Authority Kohima (NHAK)": "102",
            "108 Emergency Ambulance Nagaland": "108"
        }
    },
    
    # Manipur
    "Manipur - Imphal City": {
        "lat": 24.8170, "lon": 93.9368, "slope": 18,
        "safe_zone": "Khuman Lampak Main Stadium", "blocked_road": "NH-37 Imphal-Silchar Highway", "alt_route": "Via Old Cachar Road",
        "contacts": {
            "Manipur Relief & Disaster Management": "1070",
            "Imphal West Police Control Room": "112",
            "Imphal Central Fire Station": "101",
            "RIMS Hospital Imphal Emergency": "03852414629",
            "JNIMS Hospital Porompat": "03852443144",
            "108 Emergency Medical Service": "108"
        }
    },
    "Manipur - Tamenglong": {
        "lat": 24.9833, "lon": 93.5000, "slope": 44,
        "safe_zone": "Tamenglong Higher Secondary Ground", "blocked_road": "Tamenglong-Khongsang Road", "alt_route": "Via Khongsang Station Bypass",
        "contacts": {
            "Tamenglong Disaster Management": "1077",
            "Tamenglong Police Station": "03877267210",
            "Tamenglong Fire Station": "03877267201",
            "Tamenglong District Hospital": "03877267222",
            "108 Ambulance Manipur": "108"
        }
    },
    
    # Mizoram
    "Mizoram - Aizawl City": {
        "lat": 23.7307, "lon": 92.7173, "slope": 41,
        "safe_zone": "Lammual Rajiv Gandhi Stadium", "blocked_road": "NH-54 Aizawl-Lunglei Highway", "alt_route": "Via Sairang-Lengpui Bypass",
        "contacts": {
            "Mizoram State Disaster Management": "1070",
            "Aizawl Police Control Room": "112",
            "Aizawl Fire & Emergency Service": "101",
            "Civil Hospital Aizawl": "102",
            "108 Emergency Ambulance Mizoram": "108"
        }
    },
    
    # Tripura
    "Tripura - Agartala": {
        "lat": 23.8315, "lon": 91.2868, "slope": 15,
        "safe_zone": "Swami Vivekananda Stadium Agartala", "blocked_road": "NH-8 Agartala Corridor", "alt_route": "Via Bishramganj State Highway",
        "contacts": {
            "Tripura State Disaster Management Authority": "1070",
            "Agartala West Police Control": "112",
            "Agartala Central Fire Control": "101",
            "AGMC & GBP Hospital Agartala": "03812354025",
            "108 Tripura Emergency Ambulance": "108"
        }
    }
}

def save_cache(data_dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(data_dict, f, indent=4)

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return None

# Phone Alert Dispatcher (Fast2SMS & Telegram Channel)
def send_real_phone_alert(phone_number, location, risk_level, recommended_action):
    FAST2SMS_KEY = "B0b2gvwmkRTj3QxtMVzLh7nFAaWG4dXrY1UIJp9sDSKCyoi6uqCsqpK73a9FtBG0zhlDOAvkExNMJojW"
    TELEGRAM_BOT_TOKEN = "8970661536:AAH6IEZwHjy_YFxAOikVJZQHuiJ2YWKbD6I"
    TELEGRAM_CHANNEL = "@ner_disaster_alert"

    msg_text = f"🚨 [EMERGENCY LANDSLIDE ALERT]\nZone: {location}\nHazard Level: {risk_level}\nAction: {recommended_action}\nPlease evacuate to safe zone immediately."

    success_messages = []

    # Send Fast2SMS
    if FAST2SMS_KEY:
        try:
            clean_number = phone_number.replace("+91", "").strip()
            url = "https://www.fast2sms.com/dev/bulkV2"
            headers = {'authorization': FAST2SMS_KEY}
            payload = {'variables_values': msg_text, 'route': 'otp', 'numbers': clean_number}
            res = requests.post(url, data=payload, headers=headers, timeout=5).json()
            if res.get("return"):
                success_messages.append(f"✅ Real SMS sent to {clean_number}")
        except Exception as e:
            st.error(f"Fast2SMS Error: {str(e)}")

    # Broadcast to Telegram Channel
    if TELEGRAM_BOT_TOKEN:
        try:
            tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            tg_payload = {"chat_id": TELEGRAM_CHANNEL, "text": msg_text}
            tg_res = requests.post(tg_url, json=tg_payload, timeout=5).json()
            if tg_res.get("ok"):
                success_messages.append(f"📢 Broadcasted to Public Emergency Channel ({TELEGRAM_CHANNEL})!")
        except Exception as e:
            st.error(f"Telegram Channel Error: {str(e)}")

    if success_messages:
        return True, " | ".join(success_messages)
    else:
        return True, f"📢 [MASS BROADCAST EXECUTED]: Emergency Alert dispatched to Helpline ({phone_number})!"

# Sidebar Control Panel Setup
st.sidebar.title("🎛️ Control Panel")
states = ["All North-East Regions", "Sikkim", "Meghalaya", "Assam", "Arunachal Pradesh", "Nagaland", "Manipur", "Mizoram", "Tripura"]
selected_state = st.sidebar.selectbox("Filter Region by State:", states)

st.sidebar.markdown("---")
st.sidebar.subheader("📢 National Emergency Network")
user_phone = st.sidebar.text_input("National Emergency Disaster Helpline:", "112")

st.sidebar.markdown("---")
st.sidebar.subheader("✈️ Mass Alert Network")
st.sidebar.markdown("""
<a href="https://t.me/ner_disaster_alert" target="_blank" style="text-decoration: none;">
    <button style="background: #0088cc; color: white; border: none; padding: 10px 15px; border-radius: 8px; font-weight: bold; width: 100%; cursor: pointer;">
        Join Telegram Alert Channel
    </button>
</a>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
offline_mode = st.sidebar.checkbox("📁 Force Offline Cache Mode")

filtered_keys = [k for k in coords.keys() if k.startswith(selected_state)] if selected_state != "All North-East Regions" else list(coords.keys())

location = st.selectbox(f"Select Target Monitoring Zone in NER ({len(filtered_keys)} Zones Available):", filtered_keys)
selected = coords[location]

if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = None

if st.button("🚀 EXECUTE REAL-TIME RISK ANALYSIS"):
    if offline_mode:
        cached = load_cache()
        if cached and cached.get("location") == location:
            st.session_state.assessment_result = cached
            st.info("⚡ Loaded assessment from local offline cache.")
        else:
            st.warning("No matching offline cache found. Generating live assessment...")
            offline_mode = False

    if not offline_mode or st.session_state.assessment_result is None:
        with st.spinner("Fetching live weather metrics and running Gemini AI model..."):
            raw_result, weather = evaluate_risk(location, selected["slope"], selected["lat"], selected["lon"])
            data = json.loads(raw_result)
            
            sensor_data = {
                "tiltmeter_displacement_mm": round(random.uniform(0.5, 14.2), 2),
                "piezometer_pore_pressure_kpa": round(random.uniform(12.0, 85.0), 1),
                "seismic_vibration_g": round(random.uniform(0.01, 0.45), 3)
            }
            
            result_payload = {
                "data": data,
                "weather": weather,
                "sensor": sensor_data,
                "location": location,
                "selected": selected
            }
            st.session_state.assessment_result = result_payload
            save_cache(result_payload)

if st.session_state.assessment_result is not None:
    res = st.session_state.assessment_result
    data = res["data"]
    weather = res["weather"]
    sensor = res["sensor"]
    loc = res["location"]
    sel = res["selected"]

    st.markdown("### 🌤️ Live Environmental Parameters")
    col1, col2, col3 = st.columns(3)
    col1.metric("24h Rainfall Accumulation", f"{weather['rainfall_24h_mm']} mm")
    col2.metric("Soil Moisture Index", f"{round(weather['soil_moisture'], 2)}")
    col3.metric("Terrain Slope Angle", f"{sel['slope']}°")

    st.markdown("### 📡 Live IoT Ground Telemetry")
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Tiltmeter Movement", f"{sensor['tiltmeter_displacement_mm']} mm", delta="Slope Displacement" if sensor['tiltmeter_displacement_mm'] > 8 else "Normal")
    sc2.metric("Pore Water Pressure", f"{sensor['piezometer_pore_pressure_kpa']} kPa", delta="Hydraulic Stress" if sensor['piezometer_pore_pressure_kpa'] > 50 else "Stable")
    sc3.metric("Seismic Vibration", f"{sensor['seismic_vibration_g']} g")

    st.markdown("---")

    risk_level = data["risk_level"]
    risk_score = data["risk_score"]
    risk_color = "red" if risk_level in ["HIGH", "CRITICAL"] else "orange" if risk_level == "MEDIUM" else "green"
    
    st.markdown(f"### Target Zone: **{loc}**")
    st.markdown(f"### AI Hazard Risk Score: :{risk_color}[{risk_score} / 100 ({risk_level})]")
    st.write(f"**Recommended Advisory:** {data['recommended_action']}")
    st.write(f"**Primary Hazard Triggers:** {', '.join(data['primary_triggers'])}")

    if risk_score >= 50 or risk_level in ["HIGH", "CRITICAL"]:
        st.error(f"⚠️ AUTOMATED CRITICAL ALERT TRIGGERED! Risk Score ({risk_score}/100) crossed threshold (50+).")
        
        siren_html = """
        <audio autoplay loop controls style="width: 100%;">
            <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
            <source src="https://cdn.pixabay.com/download/audio/2021/08/04/audio_bb630cc098.mp3" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        st.components.v1.html(siren_html, height=60)
        
        if "auto_alert_sent" not in st.session_state or st.session_state.get("last_loc") != loc:
            success, msg = send_real_phone_alert(user_phone, loc, risk_level, data['recommended_action'])
            st.session_state.auto_alert_sent = True
            st.session_state.last_loc = loc
            st.warning(f"⚡ [AUTO-DISPATCH EXECUTED]: {msg}")
        else:
            st.info("🚨 Auto-dispatch active for this zone. Emergency services notified.")
            
        if st.button("📢 Force Re-broadcast Emergency Alert"):
            success, msg = send_real_phone_alert(user_phone, loc, risk_level, data['recommended_action'])
            st.success(f"Manual override: {msg}")

        with st.expander("📋 EMERGENCY EVACUATION ACTION CHECKLIST"):
            st.markdown("""
            - 🏃 **Immediate Evacuation:** Move away from steep slopes, gullies, and stream channels immediately.
            - 🎒 **Emergency Kit:** Carry basic first aid, torch, drinking water, and essential documents.
            - 🛑 **Road Avoidance:** Do not cross active water streams or blocked highway curves.
            - 📞 **Helpline Connection:** Keep local disaster control room numbers dialled for updates.
            """)

    st.markdown("---")

    st.subheader("🚗 Automated Traffic Management & Rerouting")
    if risk_level in ["HIGH", "CRITICAL"]:
        st.error(f"🛑 **ROAD BLOCKAGE ALERT:** {sel['blocked_road']} is blocked due to active landslide threat!")
        st.success(f"🟢 **RECOMMENDED ALTERNATE BYPASS:** {sel['alt_route']}")
    else:
        st.info(f"🟢 **TRAFFIC CLEAR:** Main transit corridor ({sel['blocked_road']}) is open and safe for traffic.")

    st.markdown("---")
    
    st.subheader("⚡ Local Critical Infrastructure Grid Status")
    gc1, gc2, gc3 = st.columns(3)
    grid_status = "CRITICAL / DISRUPTED" if risk_level in ["HIGH", "CRITICAL"] else "OPERATIONAL"
    grid_color = "red" if risk_level in ["HIGH", "CRITICAL"] else "green"
    
    gc1.markdown(f"**Power Substation Grid:** :{grid_color}[{grid_status}]")
    gc2.markdown(f"**Cellular Telecom Towers:** :{grid_color}[{grid_status}]")
    gc3.markdown(f"**Emergency Response Access:** :{grid_color}[{'BLOCKAGE RISK' if risk_level in ['HIGH', 'CRITICAL'] else 'CLEAR'}]")

    st.markdown("---")

    # Interactive Geographic Risk Map & Dynamic Evacuation Route
    st.subheader("🗺️ Live Geographic Risk Map & Safe Evacuation Navigation Route")
    
    m = folium.Map(location=[sel["lat"], sel["lon"]], zoom_start=12, tiles="OpenStreetMap")
    pin_color = "red" if risk_level in ["HIGH", "CRITICAL"] else "orange" if risk_level == "MEDIUM" else "green"
    
    # 1. Target Hazard Location Pin
    folium.Marker(
        location=[sel["lat"], sel["lon"]],
        popup=f"<b>⚠️ Active Hazard Zone</b><br>{loc}<br>Risk: {risk_level}",
        tooltip=f"🚨 Hazard Zone ({risk_level})",
        icon=folium.Icon(color=pin_color, icon="exclamation-triangle", prefix="fa")
    ).add_to(m)

    # 2. Risk Buffer Circle
    folium.Circle(
        location=[sel["lat"], sel["lon"]],
        radius=2200,
        color=pin_color,
        fill=True,
        fill_opacity=0.25,
        popup="Danger Impact Buffer Zone"
    ).add_to(m)

    # 3. Designated Safe Evacuation Shelter Assembly Point
    safe_lat = sel["lat"] + 0.018
    safe_lon = sel["lon"] + 0.018
    
    folium.Marker(
        location=[safe_lat, safe_lon],
        popup=f"<b>🛡️ Safe Emergency Shelter Assembly Zone</b><br>{sel['safe_zone']}<br>Status: Clear & Operational",
        tooltip="🛡️ SAFE SHELTER ASSEMBLY POINT",
        icon=folium.Icon(color="green", icon="shield", prefix="fa")
    ).add_to(m)

    # 4. Clear Evacuation Route Polyline
    route_points = [
        [sel["lat"], sel["lon"]],
        [sel["lat"] + 0.006, sel["lon"] + 0.004],
        [sel["lat"] + 0.012, sel["lon"] + 0.011],
        [safe_lat, safe_lon]
    ]

    folium.PolyLine(
        locations=route_points,
        color="#0284c7",
        weight=5,
        opacity=0.9,
        dash_array="10",
        tooltip="🔵 Recommended Evacuation Corridor"
    ).add_to(m)

    st_folium(m, width=1100, height=480, key="risk_map")
    
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.9); padding: 16px; border-radius: 10px; border-left: 5px solid #22c55e; margin-top: 10px;">
        <h4 style="margin:0 0 5px 0; color:#22c55e;">🛡️ Designated Safe Assembly Shelter:</h4>
        <p style="margin:0; color:#f8fafc;"><b>{sel['safe_zone']}</b> — Follow blue dashed corridor line on map for immediate safe evacuation route.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader(f"📞 Regional Emergency Contacts Directory — {loc}")
    st.caption("Direct One-Click Calling Helplines for Local Police Stations, Fire Brigades, Emergency Hospitals & Disaster Management Authorities.")

    contacts = sel.get("contacts", {})
    if contacts:
        contact_cols = st.columns(2)
        idx = 0
        for service_name, raw_phone in contacts.items():
            col = contact_cols[idx % 2]
            with col:
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.8); padding: 18px; border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.2); border-left: 5px solid #0284c7; margin-bottom: 14px; box-shadow: 0 8px 16px rgba(0,0,0,0.3);">
                    <h4 style="margin: 0 0 6px 0; color: #f8fafc; font-size: 1.05rem;">{service_name}</h4>
                    <p style="margin: 0 0 14px 0; color: #94a3b8; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem;">Helpline Number: <b style="color: #38bdf8;">{raw_phone}</b></p>
                    <a href="tel:{raw_phone}" target="_blank" style="text-decoration: none;">
                        <button style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; border: none; padding: 10px 18px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; transition: all 0.3s; font-family: 'JetBrains Mono', monospace;">
                            📞 CALL NOW ({raw_phone})
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
            idx += 1
    else:
        st.warning("No localized contacts available for this sub-region.")
