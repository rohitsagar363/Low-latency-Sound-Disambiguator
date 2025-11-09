import streamlit as st
import sounddevice as sd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import scipy.signal
import csv, time, matplotlib.pyplot as plt
from datetime import datetime
from tdoa_utils import estimate_angle
from PIL import Image, ImageDraw, ImageFont

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Sound Alert & Direction Detector", page_icon="🔊", layout="wide")
st.title("🎧 Real-Time Sound Alert & Visual Translator")
st.markdown("**Audio-to-Visual System for Deaf Users** - Select sound categories and get visual alerts with images and bold text when sounds are detected!")
st.markdown("Detects sounds like **dog barking**, **baby crying**, **sirens**, and more, showing visual alerts with emojis and bold text.")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    model = hub.load("https://tfhub.dev/google/yamnet/1")
    class_map_path = model.class_map_path().numpy().decode("utf-8")
    class_names = []
    with tf.io.gfile.GFile(class_map_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_names.append(row["display_name"])
    return model, class_names

with st.spinner("Loading YAMNet model..."):
    model, class_names = load_model()
st.success(f"✅ Model loaded with {len(class_names)} classes.")

# ---------------- GLOBAL FLAGS ----------------
stereo_checked = False
stereo_supported = True
event_log = []  # store detections for UI log

# ---------------- AUDIO FUNCTIONS ----------------
def get_audio_chunk(duration=3, sample_rate=16000):
    """Capture one audio chunk; warn only once."""
    global stereo_checked, stereo_supported

    if not stereo_checked:
        stereo_checked = True
        try:
            sd.rec(int(0.5 * sample_rate), samplerate=sample_rate, channels=2, dtype="float32")
            sd.wait()
            st.sidebar.success("🎙️ Stereo mic detected (direction detection active).")
            print("✅ Stereo mic detected (direction detection active).")
        except sd.PortAudioError:
            stereo_supported = False
            st.sidebar.warning("⚠️ Stereo mic not available — using mono mode with simulated stereo.")
            print("⚠️ Stereo mic not available — using mono mode with simulated stereo.")

    if stereo_supported:
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype="float32")
    else:
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait()
    return np.squeeze(audio)

def simulate_stereo(audio, delay_ms=3, sample_rate=16000):
    """Simulate stereo by adding a tiny delay to right channel."""
    if audio.ndim > 1 and audio.shape[1] == 2:
        return audio
    delay = int(sample_rate * delay_ms / 1000)
    left = audio
    right = np.concatenate([np.zeros(delay), audio[:-delay]])
    return np.stack([left, right], axis=1)

def preprocess_audio(audio, original_sr=16000, target_sr=16000):
    if original_sr != target_sr:
        n = round(audio.shape[0] * float(target_sr) / original_sr)
        audio = scipy.signal.resample(audio, n, axis=0)
    return audio

def predict_audio(audio):
    mono = np.mean(audio, axis=1)
    scores, _, _ = model(mono)
    mean_scores = tf.reduce_mean(scores, axis=0)
    i = tf.argmax(mean_scores).numpy()
    return class_names[i], mean_scores[i].numpy()

# ---------------- CATEGORY MAPPINGS ----------------
# Maps categories to visual representations and keywords for matching YAMNet labels
CATEGORY_CONFIG = {
    "Dog Barking": {
        "emoji": "🐕",
        "bold_text": "BOW WOW",
        "keywords": ["dog", "bark", "barking", "baying"],
        "color": "#FF6B6B",
        "description": "Dog barking sound detected"
    },
    "Baby Crying": {
        "emoji": "👶",
        "bold_text": "WAAH WAAH",
        "keywords": ["baby", "infant", "crying", "cry", "wail"],
        "color": "#4ECDC4",
        "description": "Baby crying sound detected"
    },
    "Siren": {
        "emoji": "🚨",
        "bold_text": "WEE WOO",
        "keywords": ["siren", "alarm", "emergency"],
        "color": "#FF4757",
        "description": "Emergency siren detected"
    },
    "Fire Alarm": {
        "emoji": "🔥",
        "bold_text": "BEEP BEEP",
        "keywords": ["fire alarm", "fire", "smoke alarm", "smoke detector"],
        "color": "#FF6348",
        "description": "Fire alarm detected"
    },
    "Thunder": {
        "emoji": "⛈️",
        "bold_text": "BOOM",
        "keywords": ["thunder", "thunderstorm", "lightning"],
        "color": "#5352ED",
        "description": "Thunder sound detected"
    },
    "Car Horn": {
        "emoji": "🚗",
        "bold_text": "HONK HONK",
        "keywords": ["car horn", "horn", "vehicle", "automobile"],
        "color": "#FFA502",
        "description": "Car horn detected"
    },
    "Doorbell": {
        "emoji": "🔔",
        "bold_text": "DING DONG",
        "keywords": ["doorbell", "bell", "chime"],
        "color": "#FFD32A",
        "description": "Doorbell sound detected"
    },
    "Knock": {
        "emoji": "🚪",
        "bold_text": "KNOCK KNOCK",
        "keywords": ["knock", "knocking", "door"],
        "color": "#95A5A6",
        "description": "Knocking sound detected"
    },
    "Phone Ringing": {
        "emoji": "📞",
        "bold_text": "RING RING",
        "keywords": ["phone", "ringing", "ring", "telephone"],
        "color": "#00D2D3",
        "description": "Phone ringing detected"
    },
    "Applause": {
        "emoji": "👏",
        "bold_text": "CLAP CLAP",
        "keywords": ["applause", "clapping", "clap"],
        "color": "#FFD700",
        "description": "Applause detected"
    },
    "Music": {
        "emoji": "🎵",
        "bold_text": "LA LA LA",
        "keywords": ["music", "song", "melody", "tune"],
        "color": "#FF69B4",
        "description": "Music detected"
    },
    "Speech": {
        "emoji": "🗣️",
        "bold_text": "HELLO",
        "keywords": ["speech", "speaking", "talk", "voice", "conversation"],
        "color": "#4834D4",
        "description": "Speech detected"
    }
}

def create_alert_image(category_name, config):
    """Create a visual alert image with emoji and bold text"""
    # Create image with colored background
    img_width, img_height = 500, 400
    # Convert hex color to RGB
    color_hex = config["color"].lstrip('#')
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    # Use light version of color for background
    bg_color = tuple(min(255, c + 50) for c in color_rgb)
    
    img = Image.new('RGB', (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a larger font, fallback to default if not available
    font_size = 60
    try:
        # Try to use a bold font on Linux
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        try:
            # Try macOS font
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                # Try other common Linux fonts
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
    
    # Draw bold text
    text = config["bold_text"]
    
    # Get text size - use textsize for older PIL or textbbox for newer
    try:
        # Newer PIL versions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        # Older PIL versions
        text_width, text_height = draw.textsize(text, font=font)
    
    # Center the text
    x = (img_width - text_width) // 2
    y = (img_height - text_height) // 2 - 50  # Offset upward for emoji space
    
    # Draw text with outline for bold effect
    outline_width = 3
    for adj in range(outline_width):
        for dx in [-adj, adj]:
            for dy in [-adj, adj]:
                draw.text((x + dx, y + dy), text, font=font, fill='black')
    
    # Draw main text in category color
    draw.text((x, y), text, font=font, fill=color_rgb)
    
    # Draw category name below
    category_font_size = 30
    try:
        cat_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", category_font_size)
    except:
        try:
            cat_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", category_font_size)
        except:
            cat_font = ImageFont.load_default()
    
    try:
        cat_bbox = draw.textbbox((0, 0), category_name, font=cat_font)
        cat_width = cat_bbox[2] - cat_bbox[0]
    except:
        cat_width, _ = draw.textsize(category_name, font=cat_font)
    
    cat_x = (img_width - cat_width) // 2
    cat_y = y + text_height + 30
    draw.text((cat_x, cat_y), category_name, font=cat_font, fill=(50, 50, 50))
    
    return img

def match_category(label, selected_categories, category_config):
    """Match detected label to selected categories"""
    label_lower = label.lower()
    for category_name in selected_categories:
        config = category_config[category_name]
        for keyword in config["keywords"]:
            if keyword.lower() in label_lower:
                return category_name, config
    return None, None

# ---------------- SETTINGS ----------------
st.sidebar.header("⚙️ Settings")

# Category selection
st.sidebar.subheader("🎯 Select Categories to Monitor")
available_categories = list(CATEGORY_CONFIG.keys())
selected_categories = st.sidebar.multiselect(
    "Choose sounds to detect and display alerts for:",
    available_categories,
    default=["Dog Barking", "Baby Crying", "Siren", "Fire Alarm"] if len(available_categories) > 0 else []
)

if len(selected_categories) == 0:
    st.sidebar.warning("⚠️ No categories selected. All detections will be shown but no special alerts.")

# Display selected categories with their emojis
if selected_categories:
    st.sidebar.markdown("**Selected categories:**")
    for cat in selected_categories:
        config = CATEGORY_CONFIG[cat]
        st.sidebar.markdown(f"{config['emoji']} {cat}")

st.sidebar.markdown("---")

# Audio settings
st.sidebar.subheader("🎙️ Audio Settings")
duration = st.sidebar.slider("Recording duration (seconds)", 1, 5, 3)
mic_spacing = st.sidebar.number_input("Mic spacing (m)", min_value=0.05, max_value=0.5, value=0.15, step=0.01)
simulate = st.sidebar.checkbox("🎭 Enable Fake Stereo Mode", value=True)
confidence_threshold = st.sidebar.slider("Confidence threshold (%)", 10, 90, 25, 5)
run_btn = st.sidebar.button("🎙️ Start Listening", type="primary")

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1, 2])
log_placeholder = col2.empty()  # detection history
current_output = col1.empty()   # live status

# ---------------- COMPASS PLOT ----------------
def plot_direction(angle):
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    theta = np.deg2rad(angle)
    ax.arrow(theta, 0, 0, 1, width=0.05, color="red")
    ax.set_title(f"Direction: {angle:.1f}°", pad=20)
    st.pyplot(fig)

# ---------------- MAIN LOOP ----------------
if run_btn:
    st.write("🎧 Listening... Press **Stop** in terminal (Ctrl+C) to end.")
    SAMPLE_RATE = 16000

    while True:
        try:
            audio = get_audio_chunk(duration, SAMPLE_RATE)
            if not stereo_supported and simulate:
                audio = simulate_stereo(np.squeeze(audio), delay_ms=np.random.randint(2, 6))
            audio = preprocess_audio(audio, SAMPLE_RATE)

            label, conf = predict_audio(audio)
            angle = estimate_angle(audio, mic_spacing, SAMPLE_RATE)
            timestamp = datetime.now().strftime("%H:%M:%S")

            # Log and print
            log_entry = f"[{timestamp}] 🎵 {label} ({conf*100:.2f}%)"
            if angle is not None:
                log_entry += f" | 🧭 Direction: {angle:.1f}°"
            print(log_entry)
            event_log.insert(0, log_entry)

            # UI output - check if detected label matches selected categories
            matched_category, matched_config = match_category(label, selected_categories, CATEGORY_CONFIG)
            conf_percent = conf * 100
            
            with current_output.container():
                # Always show what was detected
                st.markdown(f"### 🎵 **Detected:** {label}")
                st.markdown(f"**Confidence:** {conf_percent:.2f}%")
                
                # Show visual alert if category is selected, matched, and confidence is above threshold
                if matched_category and matched_config and conf_percent >= confidence_threshold:
                    # Create prominent visual alert
                    st.markdown("---")
                    st.markdown(f"### {matched_config['emoji']} **{matched_category.upper()} DETECTED!**")
                    
                    # Display large emoji and bold text using HTML/CSS for better visibility
                    alert_html = f"""
                    <div style="text-align: center; padding: 20px; background-color: {matched_config['color']}20; border-radius: 10px; border: 3px solid {matched_config['color']};">
                        <div style="font-size: 120px; margin: 10px;">{matched_config['emoji']}</div>
                        <div style="font-size: 60px; font-weight: bold; color: {matched_config['color']}; margin: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                            {matched_config['bold_text']}
                        </div>
                        <div style="font-size: 20px; color: #333; margin-top: 10px;">
                            {matched_config['description']}
                        </div>
                    </div>
                    """
                    st.markdown(alert_html, unsafe_allow_html=True)
                    
                    # Create and display image alert
                    try:
                        alert_img = create_alert_image(matched_category, matched_config)
                        st.image(alert_img, use_container_width=False, width=400)
                    except Exception as e:
                        # If image creation fails, just show the HTML alert
                        pass
                    
                    # Show direction if available
                    if angle is not None:
                        st.markdown(f"🧭 **Direction:** {angle:.1f}°")
                        plot_direction(angle)
                else:
                    # No match to selected categories or low confidence
                    if matched_category and matched_config:
                        # Category matched but confidence too low
                        st.warning(f"⚠️ {matched_category} detected but confidence ({conf_percent:.2f}%) is below threshold ({confidence_threshold}%)")
                    elif selected_categories:
                        # Sound detected but not in selected categories
                        st.info("ℹ️ Sound detected but not in selected categories.")
                    else:
                        # No categories selected
                        st.success("✅ Sound detected. Select categories in sidebar to enable visual alerts.")

            # Show full history
            with log_placeholder.container():
                st.markdown("### 🧾 Detection History (most recent first)")
                for log in event_log[:10]:  # show last 10 detections
                    st.text(log)

            time.sleep(1)

        except KeyboardInterrupt:
            st.warning("🛑 Detection stopped by user.")
            print("🛑 Detection stopped by user.")
            break
