import gradio as gr
import joblib
import pandas as pd

# Load models
model = joblib.load('model.joblib')
mlb = joblib.load('mlb.joblib')
le_type = joblib.load('le_type.joblib')
le_source = joblib.load('le_source.joblib')
le_rating = joblib.load('le_rating.joblib')


def predict(Episodes, Type, Source, Rating, Rank, Popularity, Favorites, Members, Genres):
    try:
        # ── Validate all fields are filled ──────────────────────────────
        missing = []
        if Episodes  is None: missing.append("Episodes")
        if not Type:          missing.append("Type")
        if not Source:        missing.append("Source")
        if not Rating:        missing.append("Age Rating")
        if Rank       is None: missing.append("Rank")
        if Popularity is None: missing.append("Popularity")
        if Favorites  is None: missing.append("Favorites")
        if Members    is None: missing.append("Members")
        if not Genres:         missing.append("Genres (select at least one)")

        if missing:
            return f"⚠️ Please fill in: {', '.join(missing)}"

        # ── Encode categoricals ─────────────────────────────────────────
        Type_enc   = le_type.transform([Type])[0]
        Source_enc = le_source.transform([Source])[0]
        Rating_enc = le_rating.transform([Rating])[0]

        genre_encoded = mlb.transform([Genres])

        base_data = pd.DataFrame(
            [[Type_enc, int(Episodes), Source_enc, Rating_enc,
              int(Rank), int(Popularity), int(Members), int(Favorites)]],
            columns=['Type', 'Episodes', 'Source', 'Rating',
                     'Rank', 'Popularity', 'Members', 'Favorites']
        )

        genre_df   = pd.DataFrame(genre_encoded, columns=mlb.classes_)
        final_data = pd.concat([base_data, genre_df], axis=1)

        for col in model.feature_names_in_:
            if col not in final_data.columns:
                final_data[col] = 0

        final_data = final_data[model.feature_names_in_]
        prediction = model.predict(final_data)

        score = round(float(prediction[0]), 2)
        stars = "★" * int(score) + "☆" * (10 - int(score))
        return f"⭐ Predicted Score: {score} / 10\n{stars[:10]}"

    except Exception as e:
        import traceback
        return f"❌ Error: {traceback.format_exc()}"


# ── Custom CSS ────────────────────────────────────────────────────────────────
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Nunito:wght@400;600;700&display=swap');

/* ── Root palette ── */
:root {
  --night:    #0b0c1a;
  --deepblue: #0f1130;
  --panel:    #13162b;
  --border:   #2a2f5e;
  --accent:   #e84cbe;
  --gold:     #f7c94b;
  --cyan:     #4de8e8;
  --text:     #e8eaf6;
  --muted:    #7b83b8;
  --glow:     rgba(232,76,190,0.45);
}

/* ── Base ── */
body, .gradio-container {
  background: var(--night) !important;
  font-family: 'Nunito', sans-serif !important;
  color: var(--text) !important;
  min-height: 100vh;
}

/* ── Animated starfield background ── */
.gradio-container::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.8) 0%, transparent 100%),
    radial-gradient(1px 1px at 25% 60%, rgba(255,255,255,0.6) 0%, transparent 100%),
    radial-gradient(1px 1px at 40% 10%, rgba(255,255,255,0.9) 0%, transparent 100%),
    radial-gradient(1px 1px at 55% 75%, rgba(255,255,255,0.7) 0%, transparent 100%),
    radial-gradient(1px 1px at 70% 35%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(1px 1px at 85% 55%, rgba(255,255,255,0.8) 0%, transparent 100%),
    radial-gradient(1px 1px at 15% 85%, rgba(255,255,255,0.6) 0%, transparent 100%),
    radial-gradient(1px 1px at 90% 10%, rgba(255,255,255,0.9) 0%, transparent 100%),
    radial-gradient(1px 1px at 60% 90%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 35% 45%, rgba(247,201,75,0.7) 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 80% 80%, rgba(77,232,232,0.5) 0%, transparent 100%),
    radial-gradient(2px 2px at 5% 50%, rgba(232,76,190,0.6) 0%, transparent 100%);
  pointer-events: none;
  z-index: 0;
  animation: twinkle 6s ease-in-out infinite alternate;
}

@keyframes twinkle {
  0%   { opacity: 0.6; }
  100% { opacity: 1; }
}

/* ── Hero banner ── */
#hero-banner {
  position: relative;
  width: 100%;
  margin-bottom: 0;
  border-radius: 20px 20px 0 0;
  overflow: hidden;
  background:
    linear-gradient(180deg, transparent 30%, var(--night) 100%),
    url('https://www.livemint.com/lm-img/img/2026/01/09/600x338/jjk_3_1767965678392_1767965690487.jpg') center/cover no-repeat;
  min-height: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding: 32px 24px 28px;
}

#hero-banner::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(11,12,26,0.55) 0%, rgba(232,76,190,0.12) 100%);
  pointer-events: none;
}

.hero-title {
  font-family: 'Cinzel Decorative', cursive !important;
  font-size: clamp(1.8rem, 4vw, 3rem) !important;
  font-weight: 700 !important;
  background: linear-gradient(90deg, var(--gold), var(--accent), var(--cyan));
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  text-align: center;
  letter-spacing: 2px;
  text-shadow: none;
  position: relative;
  z-index: 1;
  margin-bottom: 8px !important;
  line-height: 1.2;
}

.hero-sub {
  color: rgba(232,234,246,0.85) !important;
  font-size: 1rem !important;
  text-align: center;
  position: relative;
  z-index: 1;
  letter-spacing: 1px;
  font-weight: 600;
  margin-bottom: 0 !important;
}

/* ── Decorative sakura row ── */
#sakura-strip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 10px 0 4px;
  font-size: 1.4rem;
  letter-spacing: 4px;
  color: var(--accent);
  opacity: 0.75;
}

/* ── Section cards ── */
.card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px !important;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.04);
  transition: border-color 0.3s;
}

.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent), var(--cyan), var(--gold));
  opacity: 0.7;
}

.card:hover {
  border-color: var(--accent);
}

/* ── Section labels ── */
.section-label {
  font-family: 'Cinzel Decorative', cursive !important;
  font-size: 0.75rem !important;
  letter-spacing: 3px !important;
  color: var(--accent) !important;
  text-transform: uppercase;
  margin-bottom: 16px !important;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--accent), transparent);
  opacity: 0.4;
}

/* ── Inputs ── */
.gradio-container input[type=number],
.gradio-container input[type=text],
.gradio-container select,
.gradio-container textarea,
label.svelte-1b6s6ui span,
.block.svelte-1b6s6ui {
  background: #0d0f22 !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 10px !important;
  font-family: 'Nunito', sans-serif !important;
}

.gradio-container input:focus,
.gradio-container select:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px var(--glow) !important;
  outline: none !important;
}

label span {
  color: var(--muted) !important;
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* ── Predict button ── */
#predict-btn {
  background: linear-gradient(135deg, #c2185b, var(--accent), #7b1fa2) !important;
  border: none !important;
  border-radius: 50px !important;
  color: #fff !important;
  font-family: 'Cinzel Decorative', cursive !important;
  font-size: 1rem !important;
  letter-spacing: 2px !important;
  padding: 16px 40px !important;
  cursor: pointer !important;
  box-shadow: 0 0 24px var(--glow), 0 4px 16px rgba(0,0,0,0.5) !important;
  transition: transform 0.2s, box-shadow 0.2s !important;
  width: 100%;
  margin-top: 8px !important;
  position: relative;
  overflow: hidden;
}

#predict-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.12), transparent);
  border-radius: 50px;
}

#predict-btn:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 0 40px var(--glow), 0 8px 32px rgba(0,0,0,0.6) !important;
}

#predict-btn:active {
  transform: scale(0.98) !important;
}

/* ── Output box ── */
#output-box textarea {
  background: linear-gradient(135deg, #0d0f22, #1a0d2e) !important;
  border: 1px solid var(--gold) !important;
  border-radius: 14px !important;
  color: var(--gold) !important;
  font-size: 1.4rem !important;
  font-weight: 700 !important;
  text-align: center !important;
  font-family: 'Nunito', sans-serif !important;
  box-shadow: 0 0 20px rgba(247,201,75,0.2) !important;
  padding: 20px !important;
  min-height: 90px !important;
}

/* ── Genre checkboxes ── */
.gradio-container .wrap.svelte-1ixg7ch {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.gradio-container input[type=checkbox] + span {
  background: #0d0f22 !important;
  border: 1px solid var(--border) !important;
  border-radius: 20px !important;
  padding: 4px 14px !important;
  font-size: 0.78rem !important;
  color: var(--muted) !important;
  cursor: pointer;
  transition: all 0.2s;
}

.gradio-container input[type=checkbox]:checked + span {
  background: linear-gradient(135deg, rgba(232,76,190,0.3), rgba(77,232,232,0.2)) !important;
  border-color: var(--accent) !important;
  color: var(--cyan) !important;
  box-shadow: 0 0 8px var(--glow);
}

/* ── Anime character panels ── */
#char-panels {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 0;
}

.char-card {
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  aspect-ratio: 16/9;
  border: 1px solid var(--border);
  transition: transform 0.3s, box-shadow 0.3s;
}

.char-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 8px 32px rgba(232,76,190,0.35);
  border-color: var(--accent);
}

.char-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  display: block;
  image-rendering: auto;
}

.char-card .overlay {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(0deg, rgba(11,12,26,0.95) 0%, transparent 100%);
  padding: 16px 10px 10px;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--gold);
  letter-spacing: 1px;
  text-transform: uppercase;
}

/* ── Footer ── */
#footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.78rem;
  padding: 20px 0 8px;
  letter-spacing: 1px;
}

/* ── Utility ── */
.gap-row { margin-bottom: 16px !important; }
.full-width { width: 100% !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--night); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
"""

# ── Layout ─────────────────────────────────────────────────────────────────
with gr.Blocks(css=custom_css, theme=gr.themes.Base()) as demo:

    # ── Hero banner ──
    gr.HTML("""
    <div id="hero-banner">
      <p class="hero-title">🎌 Anime Score Oracle</p>
      <p class="hero-sub">✦ Machine Learning · Anime Analytics · Score Prediction ✦</p>
    </div>
    <div id="sakura-strip">🌸 ✦ 🌸 ✦ 🌸 ✦ 🌸 ✦ 🌸</div>
    """)

    # ── Character image panels ──
    gr.HTML("""
    <div id="char-panels">
      <div class="char-card">
        <img src="https://images.saymedia-content.com/.image/ar_4:3%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:eco%2Cw_1200/MTc2MjkyMDU2MDI0MDk3OTY1/attack-on-titan-analysis-the-culture-of-complacency.jpg" alt="Attack on Titan" loading="lazy"/>
        <div class="overlay">🗡 Action</div>
      </div>
      <div class="char-card">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQoB_o2qrfugem6XxFIf4zoA6rCwKK0OHT8w&s" alt="Romance anime" loading="lazy"/>
        <div class="overlay">🌸 Romance</div>
      </div>
      <div class="char-card">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwviVW9uLqTH5gAZ14350ewVRSO7xw-vvqhg&s" alt="Fantasy anime" loading="lazy"/>
        <div class="overlay">✨ Fantasy</div>
      </div>
    </div>
    """)

    # ── Form ──
    with gr.Row(equal_height=False):

        # Left column — anime metadata
        with gr.Column(scale=1, elem_classes=["card"]):
            gr.HTML('<div class="section-label">📋 Anime Metadata</div>')
            Episodes   = gr.Number(label="Episodes", value=None, precision=0, minimum=1, maximum=3000)
            Type       = gr.Dropdown(
                ['Movie', 'Music', 'ONA', 'OVA', 'Special', 'TV'],
                label="Type", value=None
            )
            Source     = gr.Dropdown([
                '4-koma manga', 'Book', 'Card game', 'Digital manga', 'Game',
                'Light novel', 'Manga', 'Music', 'Novel', 'Original', 'Other',
                'Picture book', 'Radio', 'Visual novel', 'Web manga'
            ], label="Source", value=None)
            Rating     = gr.Dropdown([
                'G - All Ages', 'PG - Children', 'PG-13 - Teens 13 or older',
                'R - 17+ (violence & profanity)',
                'R+ - Intended for Mature Audiences', 'Rx - Hentai'
            ], label="Age Rating", value=None)

        # Right column — popularity stats
        with gr.Column(scale=1, elem_classes=["card"]):
            gr.HTML('<div class="section-label">📊 Popularity Stats</div>')
            Rank       = gr.Number(label="Rank (lower = better, e.g. 1 = top, 15000 = obscure)", value=None, precision=0, minimum=1)
            Popularity = gr.Number(label="Popularity (e.g. 1 = most popular, 17000 = least)",    value=None, precision=0, minimum=1)
            Favorites  = gr.Number(label="Favorites (total users who favourited it)",             value=None, precision=0, minimum=0)
            Members    = gr.Number(label="Members (total users with it in their list)",           value=None, precision=0, minimum=0)

    # Genre picker
    with gr.Row():
        with gr.Column(elem_classes=["card"]):
            gr.HTML('<div class="section-label">🎭 Select Genres</div>')
            Genres = gr.CheckboxGroup(
                list(mlb.classes_),
                label="",
                value=[]
            )

    # Predict button + output
    with gr.Row():
        with gr.Column(elem_classes=["card"]):
            gr.HTML('<div class="section-label">🔮 Oracle Prediction</div>')
            output = gr.Textbox(
                label="Predicted Score",
                elem_id="output-box",
                lines=2,
                interactive=False,
                placeholder="Your anime's score will appear here…"
            )
            btn = gr.Button("🌸 Predict Score", elem_id="predict-btn")

    btn.click(
        predict,
        inputs=[Episodes, Type, Source, Rating, Rank, Popularity,
                Favorites, Members, Genres],
        outputs=output
    )

    # Footer
    gr.HTML("""
    <div id="footer">
      🌸 Anime Score Oracle · Powered by ML · Made with ❤️ for Otaku worldwide 🌸
    </div>
    """)

demo.launch()
