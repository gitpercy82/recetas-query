from app.models.ingrediente import Ingrediente
from app.models.receta import Receta
from app.models.receta_ingrediente import RecetaIngrediente
from app.models.categoria import Categoria
from app.extensions import db

def obtener_ingredientes(categoria_id=None):
    """
    Obtiene ingredientes filtrados por categoría o todos si no se especifica.
    
    Args:
        categoria_id: ID de la categoría para filtrar (opcional)
    
    Returns:
        Lista de ingredientes
    """
    if categoria_id:
        query = (
            db.session.query(Ingrediente)
            .join(RecetaIngrediente, Ingrediente.id == RecetaIngrediente.ingrediente_id)
            .join(Receta, RecetaIngrediente.receta_id == Receta.id)
            .filter(Receta.categoria_id == categoria_id)
            .distinct()
            .all()
        )
    else:
        query = Ingrediente.query.all()
    
    return query

def obtener_ingredientes_con_cantidad(categoria_id=None):
    """
    Obtiene ingredientes con la cantidad de recetas que los usan.
    """
    if categoria_id:
        query = (
            db.session.query(
                Ingrediente,
                db.func.count(RecetaIngrediente.receta_id).label('cantidad_recetas')
            )
            .join(RecetaIngrediente, Ingrediente.id == RecetaIngrediente.ingrediente_id)
            .join(Receta, RecetaIngrediente.receta_id == Receta.id)
            .filter(Receta.categoria_id == categoria_id)
            .group_by(Ingrediente.id)
            .order_by(db.func.count(RecetaIngrediente.receta_id).desc())
            .all()
        )
    else:
        query = (
            db.session.query(
                Ingrediente,
                db.func.count(RecetaIngrediente.receta_id).label('cantidad_recetas')
            )
            .join(RecetaIngrediente, Ingrediente.id == RecetaIngrediente.ingrediente_id)
            .group_by(Ingrediente.id)
            .order_by(db.func.count(RecetaIngrediente.receta_id).desc())
            .all()
        )
    return query