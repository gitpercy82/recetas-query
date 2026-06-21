from flask import Flask
from .extensions import appbuilder, db

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    
    with app.app_context():
        appbuilder.init_app(app, db.session)
        
        # Imports de modelos
        from app.models.categoria import Categoria
        from app.models.ingrediente import Ingrediente
        from app.models.receta import Receta
        from app.models.receta_ingrediente import RecetaIngrediente
        
        db.create_all()
        
        # ✅ Imports directos para evitar circular import
        from app.views.categoria_view import CategoriaView
        from app.views.ingrediente_view import IngredienteView
        from app.views.receta_view import RecetaModelView
        from app.views.reportes import ReporteSimpleView
        from app.views.reporte_graficas import ReporteCategoriaView
        
        # Import de API (si existe)
        try:
            from app.api.ingredientes import api_ingredientes
        except ImportError:
            pass
        
        # Registrar vistas
        appbuilder.add_view(
            CategoriaView,
            "Categorías",
            icon="fa-folder-open-o",
            category="Recetas"
        )
        appbuilder.add_view(
            IngredienteView,
            "Ingredientes",
            icon="fa-lemon-o",
            category="Recetas"
        )
        appbuilder.add_view(
            RecetaModelView,
            "Recetas",
            icon="fa-book",
            category="Recetas"
        )
        appbuilder.add_view(
            ReporteSimpleView,
            "Reportes de recetas por categoría",
            icon="fa-file-text-o",
            category="Reportes"
        )
        appbuilder.add_view(
            ReporteCategoriaView,
            "Gráficas por categoría",
            icon="fa-bar-chart",
            category="Reportes"
        )
    
    return app