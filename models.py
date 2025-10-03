from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    dispositivos = db.relationship("Dispositivo", backref="categoria", lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class Dispositivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(140), nullable=False)
    serial = db.Column(db.String(140), unique=True, nullable=False)
    status = db.Column(db.String(10), nullable=False, default="ativo")
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'serial': self.serial,
            'status': self.status,
            'categoria_id': self.categoria_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'categoria_nome': self.categoria.nome if self.categoria else None 
        }