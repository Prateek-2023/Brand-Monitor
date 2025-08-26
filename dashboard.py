import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("tweets_sentiment_detailed.csv")

st.set_page_config(page_title="Brand Perception Monitor", layout="wide")
st.title("📊 Brand Perception Monitor")
st.markdown("---")

if df.empty:
    st.error("❌ No tweets found in the data.")
    st.stop()

positive_count = (df['sentiment'] == "Positive").sum()
negative_count = (df['sentiment'] == "Negative").sum()
neutral_count = (df['sentiment'] == "Neutral").sum()

st.markdown(f"### 😃 {positive_count} 👍 | 😐 {neutral_count} 😶 | 😠 {negative_count} 👎")
st.markdown("---")

if positive_count > negative_count:
    st.success("🌟 Overall Sentiment: **Great job! Your audience loves you.**")
elif positive_count == negative_count:
    st.warning("⚖️ Overall Sentiment: **Stagnant perception – Push harder to grow.**")
else:
    st.error("🚨 Overall Sentiment: **Something's off – Address concerns immediately.**")

st.markdown("---")

st.subheader("📈 Common Topics (Word Cloud)")
words = " ".join(df['tweet'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(words)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

st.markdown("---")

quotes = {
    "Positive": "🌈 *People love what you're doing!*",
    "Negative": "💢 *Concerns are rising – time to act.*",
    "Neutral": "🧭 *Factual or mixed mentions – stay alert.*"
}

for sentiment in ["Positive", "Negative", "Neutral"]:
    count = (df['sentiment'] == sentiment).sum()
    st.subheader(f"{sentiment} Tweets ({count})")
    st.markdown(quotes[sentiment])

    filtered = df[df['sentiment'] == sentiment]
    if filtered.empty:
        st.info("No tweets found.")
    else:
        for _, row in filtered.iterrows():
            tweet = row["tweet"]
            if len(tweet) > 250:
                tweet = tweet[:250] + "..."
            st.markdown(f'''
            > 🕒 {row["date_time"]}
            > 💬 {tweet}
            > 👤 {row["username"]}
            ''')
    st.markdown("---")
