from collections import defaultdict

import streamlit as st

from services.google_sheets import (get_matches, save_predictions)

st.title("Quiniela Mundial 2026")

matches = get_matches()

matches_by_group = defaultdict(list)

for match in matches:
    matches_by_group[match["grupo"]].append(match)

groups = sorted(matches_by_group.keys())

tabs = st.tabs([f"Grupo {group}" for group in groups])

user_id = st.text_input(
    "Ingresa tu identificador",
    placeholder="Ejemplo: JUAN_001"
)

submit = st.button("Enviar Quiniela")

if submit:

    predictions = []

    for match in matches:

        selection = st.session_state.get(
            f"match_{match['match_id']}"
        )

        if selection == match["local"]:
            prediction = "LOCAL"

        elif selection == "Empate":
            prediction = "EMPATE"

        else:
            prediction = "VISITANTE"

        predictions.append(
            {
                "usuario_id": user_id,
                "etapa": match["etapa"],
                "match_id": match["match_id"],
                "prediccion": prediction
            }
        )

    # st.write(predictions)
    save_predictions(predictions)
    st.success("Predicciones registradas correctamente")


for tab, group in zip(tabs, groups):

    with tab:

        for match in matches_by_group[group]:
            st.write(match["fecha"])
            st.write(
                f'{match["local"]} vs {match["visitante"]}'
            )
            st.radio(
                "Selecciona un resultado",
                [
                    match['local'],
                    "Empate",
                    match['visitante']
                ],
                key=f"match_{match['match_id']}"
            )
            
