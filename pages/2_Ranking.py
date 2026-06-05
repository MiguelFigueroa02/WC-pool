import streamlit as st
from services.google_sheets import (get_user_info, get_all_users)

from services.ranking import (
    calculate_ranking
)

col1, col2, col3 = st.columns(3)

st.title("🏆 Ranking")

ranking = calculate_ranking()
users = get_all_users()

with col1:

    st.metric(
        "Participantes",
        len(ranking)
    )

with col2:
    leader = users.get(ranking[0]["usuario_id"])
    st.metric(
        "Líder",
        leader["user_name"]
    )

with col3:
    st.metric(
        "Premio acumulado",
        f'$ {len(ranking) * 200}'
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
        # st.write(player["usuario_id"])
        user = get_user_info(player["usuario_id"])
        user = users.get(player["usuario_id"])
        if user:
            display_name = (user["user_name"])
        else:
            display_name = (str(player["usuario_id"]))
        
        st.write(display_name)

    with col3:
        st.write(
            f"{player['puntos']} pts"
        )

    st.divider()
    


