# 🎧 Low-Latency Sound Disambiguator

<div align="center">

> Real-Time Audio Intelligence Dashboard for Sound Awareness

[![Hackathon Track](https://img.shields.io/badge/Track-AI%20for%20Accessibility-blue)](https://github.com/rohitsagar363/Low-latency-Sound-Disambiguator)
[![Edge Intelligence](https://img.shields.io/badge/Technology-Edge%20Intelligence-green)](https://github.com/rohitsagar363/Low-latency-Sound-Disambiguator)

</div>

## 🎯 Mission

Empowering deaf and hearing-impaired individuals with real-time sound awareness through AI-powered visual alerts.

## 🧩 Overview

The **Low-Latency Sound Disambiguator** transforms environmental sounds into instant visual alerts, making the auditory world accessible to everyone. Our system:

- 🎤 **Captures** continuous audio input in real-time
- 🤖 **Analyzes** sounds using Google's YAMNet ML model
- 🧠 **Interprets** context through Ollama (Mistral) AI
- 📊 **Visualizes** alerts through an intuitive dashboard

## 🚨 Use Case Example: Police Siren Detection

<div align="center">

### Without Sound Disambiguator
<img src="/images/before_siren.png" alt="Without System" width="600"/>

*A deaf person unable to hear approaching emergency vehicle sirens*

### With Sound Disambiguator
<img src="/images/with_siren.png" alt="With System" width="600"/>

*Real-time visual alert showing:*
- 🚓 **Detection**: Police siren detected
- 📍 **Direction**: Coming from behind, ~100m away
- 🔊 **Intensity**: High (Emergency vehicle approaching)
- ⚠️ **Action Required**: Move to the side of the road

</div>

## 📊 Dashboard Interface

### 🎯 Live Tab
<img src="/images/live_tab.png" alt="Live Dashboard" width="800"/>

*Real-time monitoring and detection interface*
- Sound classification with confidence levels
- Direction indicator with spatial awareness
- Color-coded alert banner system
- Live AI interpretations of detected sounds

### 📜 History Tab
<img src="/images/history_tab.png" alt="History View" width="800"/>

*Historical data and event tracking*
- Chronological log of detected sounds
- Time-stamped events with classifications
- Filter and search functionality
- Export capabilities for analysis

### 📈 Analytics Tab
<img src="/images/analytics_tab.png" alt="Analytics Dashboard" width="800"/>

*Statistical analysis and insights*
- Sound type distribution charts
- Temporal pattern analysis
- Alert frequency statistics
- Performance metrics visualization

### 🧠 Insights Tab
<img src="/images/insights_tab.png" alt="AI Insights" width="800"/>

*AI-powered interpretation and recommendations*
- Contextual sound interpretations
- Pattern recognition summaries
- Environmental safety scoring
- Actionable safety recommendations

## 🏗️ System Architecture

```mermaid
graph TD
    A[🎤 Microphone Input] --> B[SoundDevice Stream]
    B --> C[YAMNet Model]
    C --> D{Sound Classification}
    D -->|Confidence & Label| E[Live Dashboard]
    D -->|Events| H[Analytics Engine]
    E --> F[Ollama Mistral]
    F --> G[Insights Generation]
    H --> I[Historical Data]
    E --> J[Alert System]
    J -->|Status| K[Visual Indicators]
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style J fill:#fbb,stroke:#333,stroke-width:2px
```

## 🧰 Technology Stack

| Layer | Components | Description |
|-------|------------|-------------|
| 🎨 Frontend | Streamlit, Plotly | Interactive dashboard with real-time updates |
| 🎵 Audio | SoundDevice, NumPy | High-performance audio stream processing |
| 🤖 ML/AI | TensorFlow Hub, YAMNet | Sound classification and analysis |
| 🧠 Intelligence | Ollama (Mistral) | Local LLM for context interpretation |
| 🔄 Processing | Threading, Queue | Concurrent operation handling |
| 📊 Visualization | Plotly, Custom CSS | Dynamic charts and alert banners |

The **Low-Latency Sound Disambiguator** represents an accessible, intelligent, and privacy-respecting approach to real-time audio awareness. It's lightweight, responsive, and extendable — bridging AI, accessibility, and edge computing into one unified platform..png)guator

> Real-Time Audio Intelligence Dashboard for Sound Awareness

[![Hackathon Track](https://img.shields.io/badge/Track-AI%20for%20Accessibility-blue)](https://github.com/rohitsagar363/Low-latency-Sound-Disambiguator)
[![Edge Intelligence](https://img.shields.io/badge/Technology-Edge%20Intelligence-green)](https://github.com/rohitsagar363/Low-latency-Sound-Disambiguator)

## 🧩 Overview

The **Low-Latency Sound Disambiguator** is an innovative real-time audio intelligence system designed to enhance accessibility and sound awareness. This project:

- 🎯 Listens to live microphone input continuously
- 🤖 Utilizes Google's **YAMNet** for precise sound detection
- 🧠 Leverages **Ollama (Mistral)** for intelligent sound interpretation
- 📊 Provides instant visual feedback through an intuitive dashboard

### Core Use Case

> Empowering deaf and hearing-impaired individuals by transforming critical sounds (alarms, sirens, shouts) into clear, real-time visual alerts, enhancing safety and environmental awareness.

## � Use Case Example: Police Siren Detection

<div align="center">

### Without Sound Disambiguator
![Without System](/images/before_siren.png)
*A deaf person unable to hear approaching emergency vehicle sirens*

### With Sound Disambiguator
![With System](/images/with_siren.png)
*Real-time visual alert showing:*
- 🚓 **Detection**: Police siren detected
- 📍 **Direction**: Coming from behind, ~100m away
- 🔊 **Intensity**: High (Emergency vehicle approaching)
- ⚠️ **Action Required**: Move to the side of the road

</div>

> **Note**: Create an `images` directory and add relevant screenshots or mockups of your system in action. The images above are placeholders - replace them with actual screenshots from your application showing the alert system responding to police sirens.

## �🚀 Key Features

| Feature | Description |
|---------|-------------|
| 🔍 Real-time Classification | Advanced sound detection using YAMNet (TensorFlow Hub) |
| ⚡ Low-latency Processing | Efficient streaming with SoundDevice + async queue |
| 🤖 AI Insights | Smart context interpretation via Ollama (Mistral) |
| 📡 Direction Detection | Intelligent stereo microphone utilization with fallback simulation |
| 🚦 Visual Alerts | Smart color-coding system: 🟢 Safe • 🟡 Neutral • 🔴 Alert |
| 📊 Rich Dashboard | Comprehensive view with Live/History/Analytics/Insights tabs |
| 💨 Lightweight Design | Quick local deployment with minimal resource usage |  

## 📊 Dashboard Interface

### 🎯 Live Tab
![Live Dashboard](/images/live_tab.png)
*Real-time monitoring and detection interface*
- Sound classification with confidence levels
- Direction indicator with spatial awareness
- Color-coded alert banner system
- Live AI interpretations of detected sounds

### 📜 History Tab
![History View](/images/history_tab.png)
*Historical data and event tracking*
- Chronological log of detected sounds
- Time-stamped events with classifications
- Filter and search functionality
- Export capabilities for analysis

### 📈 Analytics Tab
![Analytics Dashboard](/images/analytics_tab.png)
*Statistical analysis and insights*
- Sound type distribution charts
- Temporal pattern analysis
- Alert frequency statistics
- Performance metrics visualization

### 🧠 Insights Tab
![AI Insights](/images/insights_tab.png)
*AI-powered interpretation and recommendations*
- Contextual sound interpretations
- Pattern recognition summaries
- Environmental safety scoring
- Actionable safety recommendations

> **📸 Screenshots:** Place your application screenshots in `/images/`:
> - `live_tab.png` - Main monitoring interface
> - `history_tab.png` - Historical data view
> - `analytics_tab.png` - Statistical analysis view
> - `insights_tab.png` - AI interpretation view
> - `before_siren.png` - Use case without system
> - `with_siren.png` - Use case with system active

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[🎤 Microphone Input] --> B[SoundDevice Stream]
    B --> C[YAMNet Model]
    C --> D{Sound Classification}
    D -->|Confidence & Label| E[Live Dashboard]
    D -->|Events| H[Analytics Engine]
    E --> F[Ollama Mistral]
    F --> G[Insights Generation]
    H --> I[Historical Data]
    E --> J[Alert System]
    J -->|Status| K[Visual Indicators]
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style J fill:#fbb,stroke:#333,stroke-width:2px
```

## 🧰 Technology Stack

| Layer | Components | Description |
|-------|------------|-------------|
| 🎨 Frontend | Streamlit, Plotly | Interactive dashboard with real-time updates |
| 🎵 Audio | SoundDevice, NumPy | High-performance audio stream processing |
| 🤖 ML/AI | TensorFlow Hub, YAMNet | Sound classification and analysis |
| 🧠 Intelligence | Ollama (Mistral) | Local LLM for context interpretation |
| 🔄 Processing | Threading, Queue | Concurrent operation handling |
| 📊 Visualization | Plotly, Custom CSS | Dynamic charts and alert banners |

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rohitsagar363/Low-latency-Sound-Disambiguator.git
cd Low-latency-Sound-Disambiguator
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# For Unix/macOS:
source venv/bin/activate
# For Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### Required Packages
```plaintext
streamlit>=1.24.0
tensorflow>=2.12.0
tensorflow_hub>=0.14.0
sounddevice>=0.4.6
numpy>=1.23.5
plotly>=5.15.0
requests>=2.31.0
pandas>=2.0.3
```

### 4. Configure Ollama

1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Start the Ollama service:
```bash
# Pull the Mistral model
ollama pull mistral

# Start the Ollama service
ollama serve
```

### 5. Launch the Dashboard

```bash
streamlit run sound_alert_appv3.py
```

> 🎤 **Note:** Grant microphone access when prompted by your system.
🔊 Grant microphone access when prompted.

## 🧠 System Operation

### Real-time Processing Pipeline

1. **Audio Capture**
   - Continuous streaming in 1.5-second chunks
   - Overlapping segments for smooth analysis
   - Real-time buffer management

2. **Sound Classification**
   - YAMNet model processes each chunk
   - Identifies sound categories and confidence levels
   - Low-latency inference optimization

3. **AI Interpretation**
   - Ollama (Mistral) analyzes classification results
   - Generates contextual two-line summaries
   - Provides human-readable insights

4. **Spatial Analysis**
   - Stereo microphone direction estimation
   - Fallback to simulated positioning
   - Real-time location tracking

5. **Visual Feedback**
   - Dynamic dashboard updates across all tabs
   - Color-coded alert system
   - Historical data tracking and visualization

## 📝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Rohit Sagar** - _Initial work_ - [rohitsagar363](https://github.com/rohitsagar363)

---
<div align="center">
Made with ❤️ for the AI Accessibility Hackathon
</div>

📸 Output Screenshots
🟢 Safe Detection Example

🔴 Alert Detection Example

🧠 AI Insight Summary View

🧩 Demo Flow
Launch the Streamlit app.

Click Start Listening.

Play sounds (e.g., music, speech, alarm) or use your voice.

Watch the live updates, AI summaries, and alert banners appear instantly.

🧭 Future Scope & Enhancements
Area	Next Steps
🔔 IoT Integration	Deploy on Raspberry Pi / ESP32 for edge detection and visual beacons.
🧠 LLM Summarization	Integrate Gemini or GPT-5 for emotion / urgency analysis of sound context.
📡 Multi-Mic Localization	Triangulate sound source direction with a 3-mic array.
🌐 Cloud Dashboard	Push events to Firebase / MQTT for remote monitoring and alerts.
📱 Mobile App Companion	Send push notifications for critical sound events.
🎨 Accessibility Design	Add vibration / haptic feedback and color-blind themes.
🔒 Data Privacy	Fully on-device inference — no audio data leaves the system.
🧾 Analytics Layer	Generate daily summaries and sound frequency heatmaps.

👨‍💻 Team
Team: Udta Buffalo 🦬
Member	Role
Rohith Sagar Karnala
Bhargav
Amal	
Manogna

🏁 Hackathon Demo Highlights
Show real-time sound detection and floating alert banners.

Demonstrate AI-generated summaries from Mistral.

Explain the impact for accessibility and deaf users.

Conclude with your Future Scope roadmap — Edge AI + IoT + LLMs.

🧠 Acknowledgments
Special thanks to:

Google TensorFlow Hub for YAMNet.

Ollama & Mistral for local LLM inference.

Streamlit for rapid dashboard development.

🏁 Summary
🎯 Low-Latency Sound Disambiguator represents an accessible, intelligent, and privacy-respecting approach to real-time audio awareness.
It’s lightweight, responsive, and extendable — bridging AI, accessibility, and edge computing into one unified platform.

