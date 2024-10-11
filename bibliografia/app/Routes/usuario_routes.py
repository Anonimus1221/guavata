from app.Models.usuario import Usuario
from flask import Message
from app import db
from app import app
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash 
from flask import Blueprint, request, flash, redirect, url_for, render_template, logging, session
import os

bp = Blueprint('usuario', __name__)

@bp.route('/home')
def index():
    return render_template('guavata.html')

@bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    print("Función recuperar() llamada")  # Añade esta línea
    if request.method == 'POST':
        correo = request.form.get('correo')
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario:
            print("Usuario encontrado:", usuario.nombre)  # Imprime el nombre del usuario
            # Generar el token
            token = generar_token(usuario)
            print("Token generado:", token)
            # Enviar el correo de recuperación
            enviar_email_recuperacion(usuario, token)
            flash('Se ha enviado un correo para restablecer tu contraseña.', 'success')
        else:
            flash('El correo no está registrado en nuestro sistema.', 'warning')
        
        return redirect(url_for('login'))
    
    return render_template('recuperar_contraseña.html')

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    usuario = verificar_token(token)
    if not usuario:
        flash('El enlace de restablecimiento de contraseña no es válido o ha expirado.', 'warning')
        return redirect(url_for('recuperar'))

    if request.method == 'POST':
        nueva_clave = request.form['nueva_clave']
        # Hashear la nueva contraseña
        nueva_clave_hash = generate_password_hash(nueva_clave)
        usuario.clave = nueva_clave_hash
        db.session.commit()
        flash('Tu contraseña ha sido actualizada.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

    # Generar token
def generar_token(usuario):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return s.dumps({'user_id': usuario.id})

# Verificar token
def verificar_token(token, expiration=1800):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token, max_age=expiration)['user_id']
    except:
        return None
    return Usuario.query.get(user_id)

def enviar_email_recuperacion(usuario, token):
    from app import mail
    # Construir la URL para la recuperación de la contraseña
    reset_url = url_for('reset_password', token=token, _external=True)

    print(f'URL de restablecimiento de contraseña: {reset_url}')
    # Crear el mensaje de correo
    msg = Message('Recupera tu contraseña',
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[usuario.correo])
    
    # Definir el cuerpo del mensaje
    msg.body = f'''Hola {usuario.nombre},

Para restablecer tu contraseña, haz clic en el siguiente enlace:

{reset_url}

Si no solicitaste este cambio, simplemente ignora este correo.
'''
    try:
        mail.send(msg)
    except Exception as e:
        print(f'Error al enviar el correo: {e}')

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