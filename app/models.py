from . import db

class Usuario(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nome=db.Column(db.String(120),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    senha=db.Column(db.String(255),nullable=False)

class Categoria(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nome=db.Column(db.String(100),nullable=False)
    descricao=db.Column(db.String(255))

class Anuncio(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    titulo=db.Column(db.String(150),nullable=False)
    descricao=db.Column(db.Text,nullable=False)
    preco=db.Column(db.Float,nullable=False)
    estoque=db.Column(db.Integer,nullable=False,default=1)
    usuario_id=db.Column(db.Integer,db.ForeignKey("usuario.id"),nullable=False)
    categoria_id=db.Column(db.Integer,db.ForeignKey("categoria.id"),nullable=False)
    usuario=db.relationship("Usuario",backref="anuncios")
    categoria=db.relationship("Categoria",backref="anuncios")

class Pergunta(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    texto=db.Column(db.Text,nullable=False)
    resposta=db.Column(db.Text)
    usuario_id=db.Column(db.Integer,db.ForeignKey("usuario.id"),nullable=False)
    anuncio_id=db.Column(db.Integer,db.ForeignKey("anuncio.id"),nullable=False)
    usuario=db.relationship("Usuario",backref="perguntas")
    anuncio=db.relationship("Anuncio",backref="perguntas")

class Compra(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    quantidade=db.Column(db.Integer,nullable=False)
    valor_unitario=db.Column(db.Float,nullable=False)
    comprador_id=db.Column(db.Integer,db.ForeignKey("usuario.id"),nullable=False)
    anuncio_id=db.Column(db.Integer,db.ForeignKey("anuncio.id"),nullable=False)
    comprador=db.relationship("Usuario",backref="compras")
    anuncio=db.relationship("Anuncio",backref="compras")

class ListaFavoritos(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nome=db.Column(db.String(100),nullable=False)
    usuario_id=db.Column(db.Integer,db.ForeignKey("usuario.id"),nullable=False)
    usuario=db.relationship("Usuario",backref="listas")

class Favorito(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    lista_id=db.Column(db.Integer,db.ForeignKey("lista_favoritos.id"),nullable=False)
    anuncio_id=db.Column(db.Integer,db.ForeignKey("anuncio.id"),nullable=False)
    lista=db.relationship("ListaFavoritos",backref="favoritos")
    anuncio=db.relationship("Anuncio",backref="favoritos")
