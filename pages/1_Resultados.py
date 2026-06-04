import streamlit as st
from services.google_sheets import (get_matches, get_results)


st.title("Resultados Oficiales")


matches = get_matches()
results = get_results()

matches_by_id = {
    match["match_id"]: match
    for match in matches
}

for match_id, result in results.items():

    match = matches_by_id[int(match_id)]
    
    if result == 'LOCAL':
        winner = match["local"]
    
    elif result == 'EMPATE':
        winner = "Empate"

    elif result == 'VISITANTE':
        winner = match["visitante"]

    st.write(
        f'{match["local"]} vs '
        f'{match["visitante"]}'
    )
    st.success(
        f'Resultado: {winner}'
    )

    st.divider()