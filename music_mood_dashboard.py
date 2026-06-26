import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Mood Prediction Dashboard",
    page_icon="🎧",
    layout="centered"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("SpotifyFeatures.csv")
    return df

df = load_data()

# ---------------- MOOD CREATION ----------------
def get_mood(row):

    if row["valence"] >= 0.6 and row["energy"] >= 0.6:
        return "Happy 😄"

    elif row["valence"] <= 0.4 and row["energy"] <= 0.4:
        return "Sad 😢"

    elif row["energy"] >= 0.7:
        return "Energetic ⚡"

    else:
        return "Calm 🌿"

df["mood"] = df.apply(get_mood, axis=1)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"]{
    background-color:#0E1117;
}

/* Transparent Header */
[data-testid="stHeader"]{
    background:transparent;
}

/* Hide Streamlit Branding */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

/* Main Area */
.main .block-container{
    max-width:850px;
    padding-top:3rem;
}

/* Title */
.title{
    text-align:center;
    color:#ff4da6;
    font-size:52px;
    font-weight:700;
    margin-bottom:5px;
}

/* Subtitle */
.subtitle{
    text-align:center;
    color:#9ca3af;
    font-size:16px;
    margin-bottom:30px;
}

/* Song Card */
.song-card{
    background:#161B22;
    border-left:5px solid #3b82f6;
    padding:15px;
    border-radius:12px;
    margin-top:12px;
    color:white;
}

/* Result Box */
.result-box{
    background:#161B22;
    padding:20px;
    border-radius:15px;
    margin-top:20px;
    border:1px solid #30363d;
}

/* Button */
.stButton button{
    width:100%;
    height:52px;
    border:none;
    border-radius:10px;
    background:#2563eb;
    color:white;
    font-size:16px;
    font-weight:600;
}

.stButton button:hover{
    background:#1d4ed8;
}

/* Selectbox Label */
label{
    color:white !important;
}

/* Metric */
[data-testid="metric-container"]{
    background:#161B22;
    border-radius:10px;
    padding:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("""
<div class="title">
🎧 AI Mood Prediction Dashboard
</div>

<div class="subtitle">
AI-Powered Music Recommendation System
</div>
""", unsafe_allow_html=True)

# ---------------- METRICS ----------------

col1,col2,col3,col4 = st.columns(4)

col1.metric("Songs", len(df))
col2.metric("Happy", len(df[df["mood"]=="Happy 😄"]))
col3.metric("Sad", len(df[df["mood"]=="Sad 😢"]))
col4.metric("Energetic", len(df[df["mood"]=="Energetic ⚡"]))

st.write("")

# ---------------- INPUT ----------------

mood = st.selectbox(
    "🎭 Select Your Mood",
    ["Happy 😄","Sad 😢","Energetic ⚡","Calm 🌿"]
)

# ---------------- RECOMMEND ----------------

if st.button("🎵 Get Recommendations"):

    recommendations = df[df["mood"] == mood]

    if "popularity" in df.columns:
        recommendations = recommendations.sort_values(
            by="popularity",
            ascending=False
        )

    recommendations = recommendations[
        ["track_name","artist_name"]
    ].drop_duplicates()

    recommendations = recommendations.head(10)

    st.markdown("""
    <div class="result-box">
    <h3 style="color:white;">
    🎶 Recommended Songs
    </h3>
    """, unsafe_allow_html=True)

    for _, row in recommendations.iterrows():

        st.markdown(
            f"""
            <div class="song-card">
            🎵 <b>{row['track_name']}</b><br>
            👤 {row['artist_name']}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<center style="color:#8b949e;">
Built with ❤️ using Streamlit & Spotify Dataset
</center>
""", unsafe_allow_html=True)