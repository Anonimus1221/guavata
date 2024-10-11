from flask import render_template, request, redirect, url_for, flash, Blueprint
from app.Models.comentario import Comentario
from app import db

bp = Blueprint('comentario', __name__)

@bp.route('/enviar_comentario', methods=['GET', 'POST'])
def enviar_comentario():
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')

        # Crea una nueva instancia del modelo comentarios
        nuevo_comentario = Comentario(descripcion=descripcion)

        try:
            # Agrega el nuevo contacto a la base de datos
            db.session.add(nuevo_comentario)
            db.session.commit()
            flash('Comentario enviado correctamente', 'success')
            return redirect(url_for('comentario.enviar_comentario')) # Redirijir al mismo formulario
            
        except Exception as e:
            db.session.rollback() # Si algo sale mal revierte la transaccion
            flash('Error al enviar el comentario.Intenta de nuevo', 'danger')
            print(e)
        return redirect(url_for('comentario.enviar_comentario')) #Redirige de nuevo al mismo formulario
    
    comentarios = Comentario.query.all()
    #Si el metodo es get, simplemente muestra el formulario
    return render_template('comentarios/index.html', comentarios=comentarios)
