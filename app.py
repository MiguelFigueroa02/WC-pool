from collections import defaultdict
import streamlit as st
from services.validations import (validate_user_id, is_stage_open)
from services.google_sheets import (get_matches, get_predictions, save_predictions, get_results)

st.set_page_config(
    page_title="QuinieLIMS",
    initial_sidebar_state='expanded'
)

st.title("Quiniela Mundial 2026")

matches = get_matches()
matches_by_id = {
    match["match_id"]: match
    for match in matches
}

results = get_results()
# st.write(results)


matches_by_group = defaultdict(list)

for match in matches:
    matches_by_group[match["grupo"]].append(match)

groups = sorted(matches_by_group.keys())

tabs = st.tabs([f"Grupo {group}" for group in groups])

user_id = st.text_input(
    "Ingresa tu número de celular",
    placeholder="Ejemplo: 4490131313"
)
existing_predictions = []
is_valid = False
is_valid, result = validate_user_id(user_id)
if is_valid:
    existing_predictions = get_predictions(
        user_id=result,
        etapa='fase_de_grupos'
    )
    # st.write(existing_predictions)
    # st.write(len(existing_predictions))
    if existing_predictions:
        st.info('Ya existe una quiniela registrada para este número.')
        # st.write(existing_predictions)
        st.subheader("Tus predicciones registradas")
        for prediction in existing_predictions:
            match = matches_by_id[
                prediction["match_id"]
            ]
            if prediction["prediccion"] == "LOCAL":
                selected = match["local"]
            elif prediction["prediccion"] == "EMPATE":
                selected = "Empate"
            elif prediction["prediccion"] == "VISITANTE":
                selected = match["visitante"]

            st.write(
                 f'{match["local"]} vs '
                 f'{match["visitante"]}'
            )
            st.write(
                f'✅ {selected}'
            )

            st.divider()

has_predictions = bool(existing_predictions)
st.write(has_predictions)
if is_valid and not has_predictions:
    submit = st.button("Enviar Quiniela")
else:
    submit = False

if submit:
    if not is_stage_open("fase_de_grupos"):
        st.error("La fase de grupos ya se encuentra cerrada.")
    else:
        predictions = []

        for match in matches:

            selection = st.session_state.get(
                f"match_{match['match_id']}"
            )

            if selection == match["local"]:
                prediction = "LOCAL"

            elif selection == "Empate":
                prediction = "EMPATE"

            elif selection == match["visitante"]:
                prediction = "VISITANTE"

            predictions.append(
                {
                    "usuario_id": result,
                    "etapa": match["etapa"],
                    "match_id": match["match_id"],
                    "prediccion": prediction
                }
            )
        is_valid = False
        submit = False
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
            
