import streamlit as st

from services.ranking import (
    calculate_ranking
)

col1, col2 = st.columns(2)

st.title("🏆 Ranking")

ranking = calculate_ranking()

with col1:

    st.metric(
        "Participantes",
        len(ranking)
    )

with col2:

    st.metric(
        "Líder",
        ranking[0]["puntos"]
    )

for position, player in enumerate(
    ranking,
    start=1
):
    if position == 1:
        medal = "🥇"

    elif position == 2:
        medal = "🥈"

    elif position == 3:
        medal = "🥉"

    else:
        medal = "🏅"

    col1, col2, col3 = st.columns(
    [1, 3, 1]
)

    with col1:
        st.markdown(
            f"### {medal}"
        )

    with col2:
        st.write(player["usuario_id"])

    with col3:
        st.write(
            f"{player['puntos']} pts"
        )

    st.divider()
    



