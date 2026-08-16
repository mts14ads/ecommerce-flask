from . import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    anuncios = db.relationship("Anuncio", backref="usuario", lazy=True, cascade="all, delete-orphan")
    perguntas = db.relationship("Pergunta", backref="usuario", lazy=True, cascade="all, delete-orphan")
    compras = db.relationship("Compra", backref="comprador", lazy=True, cascade="all, delete-orphan")
    listas = db.relationship("ListaFavoritos", backref="usuario", lazy=True, cascade="all, delete-orphan")


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))

    anuncios = db.relationship("Anuncio", backref="categoria", lazy=True)


class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=1)
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    perguntas = db.relationship("Pergunta", backref="anuncio", lazy=True, cascade="all, delete-orphan")
    compras = db.relationship("Compra", backref="anuncio", lazy=True, cascade="all, delete-orphan")
    favoritos = db.relationship("Favorito", backref="anuncio", lazy=True, cascade="all, delete-orphan")


class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text)
    criada_em = db.Column(db.DateTime, server_default=db.func.now())
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)


class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.DateTime, server_default=db.func.now())
    comprador_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)


class ListaFavoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    favoritos = db.relationship("Favorito", backref="lista", lazy=True, cascade="all, delete-orphan")


class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lista_id = db.Column(db.Integer, db.ForeignKey("lista_favoritos.id"), nullable=False)
    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)
