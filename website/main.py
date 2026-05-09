from pathlib import Path

from blacksheep import Application
from rodi import Container

from services import get_logger, is_production
from website.errors import configure_error_handlers
from website.state import State
from website.templating import configure_templating

logger = get_logger("main")


def configure_application() -> Application:
    state = State()

    container = Container()
    container.register(State, instance=state)

    app = Application(services=container, show_error_details=not is_production())
    state.set_app(app)

    app.serve_files(Path(__file__).parent / "static", root_path="static", discovery=True)

    configure_error_handlers(app)
    configure_templating(app)

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
