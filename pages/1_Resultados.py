import streamlit as st
from services.google_sheets import (get_matches, get_results)
from utils.helpers import get_flag_path


st.title("Resultados Oficiales")


matches = get_matches()
results = get_results()
# st.write(results)

matches_by_id = {
    match["match_id"]: match
    for match in matches
}

grouped_matches = {}

for match in matches:
    group = match["grupo"]
    if group not in grouped_matches:
        grouped_matches[group] = []
    
    grouped_matches[group].append(match)


for group in sorted(grouped_matches.keys()):
    st.subheader(
        f"🏟️ Grupo {group}"
    )
    for match in grouped_matches[group]:
        result = results.get(
            match["match_id"]
        )
        # st.write(result)
        if result:
            if result == 'LOCAL':
                winner = match["local"]

            elif result == 'EMPATE':
                winner = "Empate"

            elif result == 'VISITANTE':
                winner = match["visitante"]
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(
                get_flag_path(match["local"]),
                width=40
            )
        with col2:
            st.write(
                f'{match["local"]} vs '
                f'{match["visitante"]}'
            )
        with col3:
            st.image(
                get_flag_path(match["visitante"]),
                width=40
            )
        if result:
            st.success(
                f'🏁 {winner}'
            )
        else:
            st.write('')
            
        st.divider()
