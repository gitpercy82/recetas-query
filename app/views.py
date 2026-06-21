from flask import current_app, render_template
from .extensions import appbuilder  # ✅ Agregado

@current_app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )