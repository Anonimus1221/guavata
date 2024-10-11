from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    # Aquí puedes registrar tus blueprints
    from app.Routes import usuario_routes, categorias_routes, comentarios_routes
    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(categorias_routes.bp)
    app.register_blueprint(comentarios_routes.bp)
    
    return app

