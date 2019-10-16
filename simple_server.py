from aiohttp import web
import aiohttp_cors

from app.routes import handle_tn
from app.routes import handle_index 


def setup_app():
  app = web.Application()
  cors = aiohttp_cors.setup(app)
  # Routes
  resource_index = cors.add(app.router.add_resource('/index/{id}'))
  resource_tn = cors.add(app.router.add_resource("/tn"))

  cors_headers = {
    "http://localhost:3000": aiohttp_cors.ResourceOptions(
      allow_credentials=True,
      expose_headers=("X-Custom-Server-Header",),
      allow_headers=("X-Requested-With", "Content-Type"),
      max_age=3600,
    )
  }
  cors.add(resource_tn.add_route("POST", handle_tn), cors_headers)
  cors.add(resource_index.add_route("GET", handle_index), cors_headers)
  return app


if __name__ == '__main__':
  app = setup_app()
  web.run_app(app)

