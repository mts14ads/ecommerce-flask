from datetime import datetime
from . import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    anuncios = db.relationship(
        "Anuncio",
        backref="proprietario",
        lazy=True
    )

    perguntas = db.relationship(
        "Pergunta",
        backref="autor",
        lazy=True
    )

    compras = db.relationship(
        "Compra",
        backref="comprador",
        lazy=True
    )

    listas_favoritos = db.relationship(
        "ListaFavoritos",
        backref="usuario",
        lazy=True
    )


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.String(255))

    anuncios = db.relationship(
        "Anuncio",
        backref="categoria",
        lazy=True
    )


class Anuncio(db.Model):
    __tablename__ = "anuncios"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=1, nullable=False)
    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id"),
        nullable=False
    )

    perguntas = db.relationship(
        "Pergunta",
        backref="anuncio",
        lazy=True
    )

    compras = db.relationship(
        "Compra",
        backref="anuncio",
        lazy=True
    )

    favoritos = db.relationship(
        "Favorito",
        backref="anuncio",
        lazy=True
    )


class Pergunta(db.Model):
    __tablename__ = "perguntas"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text)
    criada_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    anuncio_id = db.Column(
        db.Integer,
        db.ForeignKey("anuncios.id"),
        nullable=False
    )


class Compra(db.Model):
    __tablename__ = "compras"

    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    valor_unitario = db.Column(
        db.Float,
        nullable=False
    )

    data_compra = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    comprador_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    anuncio_id = db.Column(
        db.Integer,
        db.ForeignKey("anuncios.id"),
        nullable=False
    )


class ListaFavoritos(db.Model):
    __tablename__ = "listas_favoritos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    favoritos = db.relationship(
        "Favorito",
        backref="lista",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Favorito(db.Model):
    __tablename__ = "favoritos"

    id = db.Column(db.Integer, primary_key=True)

    lista_id = db.Column(
        db.Integer,
        db.ForeignKey("listas_favoritos.id"),
        nullable=False
    )

    anuncio_id = db.Column(
        db.Integer,
        db.ForeignKey("anuncios.id"),
        nullable=False
    )