from utils.constants import COUNTRIES


def get_flag_path(country: str) -> str:
    return (
        f"assets/flags/"
        f"{COUNTRIES[country]['flag']}"
    )