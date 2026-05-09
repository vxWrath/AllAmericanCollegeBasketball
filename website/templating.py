from blacksheep.server import Application
from blacksheep.server.rendering.jinja2 import JinjaRenderer
from blacksheep.settings.html import html_settings
from jinja2 import FileSystemLoader

from services import is_production


def configure_templating(app: Application) -> None:
    renderer = JinjaRenderer(
        loader=FileSystemLoader(searchpath="website/templates"),
        debug=not is_production(),
        enable_async=True,
    )
    html_settings.use(renderer)

    helpers = {
        "get_copyright": "Copyright © 2026 All American College Basketball.",
        "STATIC_PATH": "/static",
    }

    renderer.env.globals.update(helpers)
