from app.Models.categorias import Categoria
from app import db
from flask import Blueprint, request, redirect, url_for, render_template, current_app
from app.Models.categorias import Categoria
import os




bp = Blueprint('categorias', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/categorias/ admin')
def index():
    data= Categoria.query.all()
    return render_template('categorias/index.html')



@bp.route('/categorias/index_cliente')
def index_cliente():
    db.session.remove()
    data= Categoria.query.all()
    return render_template('categorias/index_cliente.html', data=data)

@bp.route('/categorias/add', methods=['POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        if 'imagen' not in request.files:
            return "No se ha selccionada ninguna imagen", 400
        file= request.files['imagen']
        if file.filename == '':
            return "Nombre de archivo vacio", 400
        if file and allowed_file(file.filename):
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
                filepath = os.path.join(upload_folder, file.filename)
                file.save(filepath)
                new_categoria = Categoria(nombre=nombre, descripcion=descripcion, imagen=filepath)
                db.session.add(new_categoria)
                db.session.commit()
                return redirect(url_for('categorias.index'))
            return render_template('categorias/add.html')

@bp.route('/categorias/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
       categoria.nombre = request.form['nombre']
       categoria.descripcion = request.form['descripcion']
       
       
    if 'imagen' in request.files['imagen']:
        file= request.files['imagen']
        if file and allowed_file(file.filename):
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
                filepath = os.path.join(upload_folder, file.filename)
                file.save(filepath)
                categoria.imagen = filepath
                db.session.commit()
                return redirect(url_for('categorias.index'))
            return render_template('categorias/edit.html', categoria=categoria)
        
@bp.route('/categorias/delete/<int:id>')
def delete(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categorias.index'))

@bp.route('/sitiosturisticos')
def sitiosturisticos():
    return render_template('sitiosturisticos.html')


@bp.route("/historia")
def historia():
    return render_template("historia.html")

@bp.route("/deportes")
def deportes():
    return render_template("deportes.html")

@bp.route("/mapageneral")
def mapageneral():
    return render_template("mapageneral.html")

@bp.route("/guavata")
def guavata():
    return render_template("guavata.html")

@bp.route("/eventos")
def eventos():
    return render_template("eventos.html")

