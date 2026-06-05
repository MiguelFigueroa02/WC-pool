from collections import defaultdict
import streamlit as st
from utils.helpers import get_flag_path
from services.validations import (validate_user_id, is_stage_open, validate_user_name)
from services.google_sheets import (get_matches, get_predictions, save_predictions, save_user_info, get_user_info)
from utils.constants import CURRENT_STAGE

st.set_page_config(
    page_title="QuinieLIMS",
    initial_sidebar_state='expanded'
)

st.title("Quiniela Mundial 2026")
st.caption('¡Es hora de jugar! Empieza a incluir tus pronósticos.')
# st.markdown("### Fase de grupos")

matches = get_matches()
matches_by_id = {
    match["match_id"]: match
    for match in matches
}


matches_by_group = defaultdict(list)

st.markdown("---")

st.subheader(
    "😎 Identificación del participante"
)
user_id = st.text_input(
    "Ingresa tu número de celular",
    placeholder="Ejemplo: 4490131313"
)
user_name = st.text_input(
    "¿Cuál es tu nombre?",
    placeholder="Ejemplo: 'Maradona' o 'El_Diego' o 'D10S'"
)

existing_predictions = []
is_valid = False
is_valid, result = validate_user_id(user_id)
is_valid_name, name_result = (
    validate_user_name(
        user_name
    )
)
can_submit_predictions = False
if is_valid:
    existing_predictions = get_predictions(
        user_id=result,
        etapa=CURRENT_STAGE
    )
    if (not existing_predictions and is_valid_name):
        if is_stage_open(CURRENT_STAGE):
            can_submit_predictions = True
    # st.write(existing_predictions)
    # st.write(len(existing_predictions))
    if existing_predictions:
        existing_user = get_user_info(result)
        # st.write(existing_user)
        display_name = existing_user['user_name']
        st.success(f"👤 Bienvenido {display_name}")
        st.info('Tu quiniela ya había sido registrada')
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

st.markdown("---")

st.subheader(
    f"⚽ Pronósticos - {CURRENT_STAGE.replace('_', ' ').title()}"
)
if can_submit_predictions:
    submit = st.button("Enviar Quiniela")
else:
    submit = False

if submit:
    if not is_valid_name:
        st.error(name_result)
    elif not is_stage_open(CURRENT_STAGE):
        st.error("La fase de grupos ya se encuentra cerrada.")
    else:
        predictions = []

        for match in matches:

            selection = st.session_state.get(
                f"match_{match['match_id']}"
            )

            if selection is None:
                continue
            elif selection == match["local"]:
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
        existing_user = get_user_info(result)

        if len(predictions) == len(matches):
            save_predictions(predictions)
            if not existing_user:
                save_user_info(result,name_result)
                st.success("Predicciones registradas correctamente")
        else:
            st.error("Debes seleccionar todos los partidos antes de enviar tu quiniela.")
            
    
if (
    is_valid
    and not existing_predictions
    and not is_stage_open(CURRENT_STAGE)
):
        st.warning(
            "La fase de grupos ya se encuentra cerrada."
        )

if can_submit_predictions:

    for match in matches:
        matches_by_group[match["grupo"]].append(match)

    groups = sorted(matches_by_group.keys())
    # st.write(st.session_state.get("match_1"))

    tabs = st.tabs([f"Grupo {group}" for group in groups])

    for tab, group in zip(tabs, groups):

        with tab:
            st.write('Elige un resultado por partido: ')
            for match in matches_by_group[group]:
                flex = st.container(horizontal=True, horizontal_alignment="center", vertical_alignment='center', width='stretch')
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.image(
                        get_flag_path(match["local"]),
                        width=40
                    )
                with col2:
                    st.write("VS")
                with col3:
                    st.image(
                        get_flag_path(match["visitante"]),
                        width=40
                    )
                st.segmented_control(
                    f"{match['fecha']}. Partido: {match['match_id']}:",
                    [
                        match['local'],
                        "Empate",
                        match['visitante']
                    ],
                    key=f"match_{match['match_id']}",
                    default=None
                )
            