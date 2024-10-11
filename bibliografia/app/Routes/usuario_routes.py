from app.Models.usuario import Usuario
from app import db
from werkzeug.security import generate_password_hash, check_password_hash 
from flask import Blueprint, request, flash, redirect, url_for, render_template, logging, session
import os

bp = Blueprint('usuario', __name__)

@bp.route('/home')
def index():
    return render_template('guavata.html')

@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        print(request.form)
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        rol = request.form.get('rol')
        print(contraseña)
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contraseña=contraseña,
            rol=rol, 
        )
        
        try:
            print("Intentando guardar usuario en la base de datos...")
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario registrado con éxito.')
            return redirect(url_for('usuario.login'))
        except Exception as e:
            db.session.rollback()  
            print(f"Error al registrar el usuario: {str(e)}")  
            flash(f'Error al registrar el usuario: {str(e)}')
            return redirect(url_for('usuario.registro'))

    return render_template('Usuarios/registro.html')


@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        usuario = Usuario.query.filter_by(correo=correo, contraseña=contraseña).first()

        if usuario is None:
            flash('Usuario no encontrado. Por favor, regístrate antes de iniciar sesión.')
            return redirect(url_for('usuario.login'))
        
        
        session['usuario_id'] = usuario.id
        session['rol'] = usuario.rol
        
        if usuario.rol == 'Administrador':
            return redirect(url_for('usuario.admin_dashboard'))  
        else:
            return redirect(url_for('usuario.index'))


    return render_template('Usuarios/login.html')

@bp.route('/logout')
def logout():
    session.clear() 
    flash('Sesión cerrada.')
    return redirect(url_for('usuario.login'))

@bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')