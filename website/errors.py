from blacksheep import Request, Response
from blacksheep.server import Application
from blacksheep.server.responses import html, json, text
from blacksheep.settings.html import html_settings
from essentials.exceptions import AcceptedException

from services import get_logger

__all__ = ["configure_error_handlers"]

logger = get_logger("dashboard.errors")


def is_api_route(request: Request) -> bool:
    return request.url.path.startswith(b"/api/")


async def format_html_error(status: int, title: str, description: str) -> Response:
    content = await html_settings.renderer.render_async(
        "error.jinja",
        {"status": status, "title": title, "description": description},
    )
    return html(content, status=status)


def configure_error_handlers(app: Application) -> None:
    @app.exception_handler(404)
    async def not_found_handler(_: Application, request: Request, __: Exception) -> Response:
        if is_api_route(request):
            return json({"error": {"code": "NOT_FOUND", "message": "Not found"}}, status=404)
        return await format_html_error(
            404, "Not Found", "The page you're looking for doesn't exist."
        )

    @app.exception_handler(500)
    async def not_implemented_handler(_: Application, request: Request, __: Exception) -> Response:
        if is_api_route(request):
            return json(
                {"error": {"code": "SERVER_ERROR", "message": "An unexpected error occurred."}},
                status=500,
            )
        return await format_html_error(
            500, "Server Error", "Something went wrong on our end. Developers have been notified."
        )

    @app.exception_handler(401)
    async def unauthorized_handler(_: Application, request: Request, __: Exception) -> Response:
        if is_api_route(request):
            return json(
                {"error": {"code": "UNAUTHORIZED", "message": "You must be logged in."}}, status=401
            )
        return await format_html_error(
            401, "Unauthorized", "You must be logged in to access this page."
        )

    @app.exception_handler(403)
    async def forbidden_handler(_: Application, request: Request, __: Exception) -> Response:
        if is_api_route(request):
            return json({"error": {"code": "FORBIDDEN", "message": "Access denied."}}, status=403)
        return await format_html_error(
            403, "Forbidden", "You don't have permission to access this."
        )

    @app.exception_handler(AcceptedException)
    async def accepted(*args: object) -> Response:
        return text("Accepted", status=202)
