from pathlib import Path

from blacksheep import Application
from rodi import Container

from services import get_logger, is_production
from website.state import State

logger = get_logger("main")


def configure_application() -> Application:
    state = State()

    container = Container()
    container.register(State, instance=state)

    app = Application(services=container, show_error_details=not is_production())
    state.set_app(app)

    app.serve_files(Path(__file__).parent / "static", root_path="static", discovery=True)

    return app


app = configure_application()


@app.on_start
async def startup() -> None:
    state = app.services.resolve(State)
    await state.connect()


@app.on_stop
async def shutdown() -> None:
    state = app.services.resolve(State)
    await state.close()
