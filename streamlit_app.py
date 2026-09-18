import requests
import streamlit as st

# <-- TUTAJ WKLEJ SWÓJ ADRES Z CLOUD RUN
API_URL = "https://polish-reviews-api-706649204585.europe-west1.run.app/predict"

st.set_page_config(
    page_title="Polish Reviews Rating Predictor", page_icon="⭐️"
)

st.title("⭐️ Polish Product Reviews Rating Predictor")
st.markdown(
    "Wpisz treść opinii w języku polskim, aby oszacować ocenę gwiazdkową"
    " (1-5)."
)

review_text = st.text_area(
    "Treść recenzji:",
    placeholder=(
        "np. Słuchawki grają rewelacyjnie, bas jest głęboki i bateria"
        " trzyma 2 dni!"
    ),
    height=120,
)

if st.button("Oceń recenzję"):
  if len(review_text.strip()) < 3:
    st.warning("Wpisz dłuższą opinię (min. 3 znaki).")
  else:
    with st.spinner("Model analizuje opinię..."):
      try:
        resp = requests.post(API_URL, json={"text": review_text}, timeout=10)
        if resp.status_code == 200:
          data = resp.json()
          rating = int(data["predicted_rating"])
          scores = data["confidence_scores"]

          # Gwiazdki
          st.success(f"Przewidywana ocena: **{rating} / 5** {'⭐️' * rating}")

          # Wykres progów
          st.write("Prawdopodobieństwa przekroczenia progów ocen:")
          chart_data = {
              "Ocena > 1": scores[0],
              "Ocena > 2": scores[1],
              "Ocena > 3": scores[2],
              "Ocena > 4": scores[3],
          }
          st.bar_chart(chart_data)
        else:
          st.error(f"Błąd API: {resp.status_code}")
      except Exception as e:
        st.error(f"Nie udało się połączyć z API: {e}")
