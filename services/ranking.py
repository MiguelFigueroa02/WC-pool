from services.google_sheets import (get_all_predictions, get_results)

def calculate_ranking():

    predictions = get_all_predictions()

    results = get_results()

    scores = {}

    for prediction in predictions:

        user_id = str(
            prediction["usuario_id"]
        )

        match_id = int(
            prediction["match_id"]
        )

        predicted_result = (
            prediction["prediccion"]
        )

        official_result = results.get(
            match_id
        )

        if official_result is None:
            continue

        if user_id not in scores:
            scores[user_id] = 0

        if predicted_result == official_result:
            scores[user_id] += 1

    ranking = []

    for user_id, points in scores.items():

        ranking.append(
            {
                "usuario_id": user_id,
                "puntos": points
            }
        )

    ranking.sort(
        key=lambda x: x["puntos"],
        reverse=True
    )

    return ranking