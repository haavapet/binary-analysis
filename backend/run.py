from uvicorn import run as run_server


def start() -> None:
    """Launched with `poetry run start` at root level"""
    run_server("app.controller:app", host="0.0.0.0", port=8000, reload=True)
