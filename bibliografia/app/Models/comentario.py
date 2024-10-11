from app import db
class Comentario(db.Model):
    __tablename__ = 'comentarios'  # Cambia _tablename_ a __tablename__
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)