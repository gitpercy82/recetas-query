from flask import jsonify, request
from app.models.ingrediente import Ingrediente
from app.models.receta import Receta
from app.models.receta_ingrediente import RecetaIngrediente
from app.extensions import db, appbuilder


@appbuilder.app.route('/api/ingredientes', methods=['GET'])
def api_ingredientes():
    """
    API endpoint para obtener ingredientes.
    
    Query params:
        - categoria_id: Filtrar por categoría (opcional)
    """
    categoria_id = request.args.get('categoria_id', type=int)
    
    if categoria_id:
        ingredientes = (
            db.session.query(Ingrediente)
            .join(RecetaIngrediente, Ingrediente.id == RecetaIngrediente.ingrediente_id)
            .join(Receta, RecetaIngrediente.receta_id == Receta.id)
            .filter(Receta.categoria_id == categoria_id)
            .distinct()
            .all()
        )
    else:
        ingredientes = Ingrediente.query.all()
    
    # Serializar resultados
    resultado = [
        {
            'id': ing.id,
            'nombre': ing.nombre,
            'unidad': ing.unidad if hasattr(ing, 'unidad') else None
        }
        for ing in ingredientes
    ]
    
    return jsonify({
        'ingredientes': resultado,
        'total': len(resultado),
        'categoria_id': categoria_id
    })