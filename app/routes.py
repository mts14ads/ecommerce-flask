from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Usuario, Categoria, Anuncio, Pergunta, Compra, ListaFavoritos, Favorito

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

# USUÁRIOS
@main.route("/usuarios")
def usuarios():
    return render_template("usuarios.html", registros=Usuario.query.order_by(Usuario.id.desc()).all())

@main.route("/usuarios/novo", methods=["GET", "POST"])
def usuario_novo():
    if request.method == "POST":
        registro = Usuario(
            nome=request.form["nome"],
            email=request.form["email"],
            senha=request.form["senha"]
        )
        db.session.add(registro)
        db.session.commit()
        flash("Usuário cadastrado com sucesso.")
        return redirect(url_for("main.usuarios"))
    return render_template("usuario_form.html", registro=None)

@main.route("/usuarios/<int:id>/editar", methods=["GET", "POST"])
def usuario_editar(id):
    registro = Usuario.query.get_or_404(id)
    if request.method == "POST":
        registro.nome = request.form["nome"]
        registro.email = request.form["email"]
        registro.senha = request.form["senha"]
        db.session.commit()
        flash("Usuário alterado com sucesso.")
        return redirect(url_for("main.usuarios"))
    return render_template("usuario_form.html", registro=registro)

@main.route("/usuarios/<int:id>/excluir", methods=["POST"])
def usuario_excluir(id):
    registro = Usuario.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    flash("Usuário excluído com sucesso.")
    return redirect(url_for("main.usuarios"))

# CATEGORIAS
@main.route("/categorias")
def categorias():
    return render_template("categorias.html", registros=Categoria.query.order_by(Categoria.id.desc()).all())

@main.route("/categorias/novo", methods=["GET", "POST"])
def categoria_novo():
    if request.method == "POST":
        registro = Categoria(nome=request.form["nome"], descricao=request.form["descricao"])
        db.session.add(registro)
        db.session.commit()
        flash("Categoria cadastrada com sucesso.")
        return redirect(url_for("main.categorias"))
    return render_template("categoria_form.html", registro=None)

@main.route("/categorias/<int:id>/editar", methods=["GET", "POST"])
def categoria_editar(id):
    registro = Categoria.query.get_or_404(id)
    if request.method == "POST":
        registro.nome = request.form["nome"]
        registro.descricao = request.form["descricao"]
        db.session.commit()
        flash("Categoria alterada com sucesso.")
        return redirect(url_for("main.categorias"))
    return render_template("categoria_form.html", registro=registro)

@main.route("/categorias/<int:id>/excluir", methods=["POST"])
def categoria_excluir(id):
    registro = Categoria.query.get_or_404(id)
    if registro.anuncios:
        flash("Não é possível excluir uma categoria que possui anúncios.")
    else:
        db.session.delete(registro)
        db.session.commit()
        flash("Categoria excluída com sucesso.")
    return redirect(url_for("main.categorias"))

# ANÚNCIOS
@main.route("/anuncios")
def anuncios():
    return render_template("anuncios.html", registros=Anuncio.query.order_by(Anuncio.id.desc()).all())

@main.route("/anuncios/novo", methods=["GET", "POST"])
def anuncio_novo():
    if request.method == "POST":
        registro = Anuncio(
            titulo=request.form["titulo"],
            descricao=request.form["descricao"],
            preco=float(request.form["preco"]),
            estoque=int(request.form["estoque"]),
            usuario_id=int(request.form["usuario_id"]),
            categoria_id=int(request.form["categoria_id"])
        )
        db.session.add(registro)
        db.session.commit()
        flash("Anúncio cadastrado com sucesso.")
        return redirect(url_for("main.anuncios"))
    return render_template("anuncio_form.html", registro=None, usuarios=Usuario.query.all(), categorias=Categoria.query.all())

@main.route("/anuncios/<int:id>/editar", methods=["GET", "POST"])
def anuncio_editar(id):
    registro = Anuncio.query.get_or_404(id)
    if request.method == "POST":
        registro.titulo = request.form["titulo"]
        registro.descricao = request.form["descricao"]
        registro.preco = float(request.form["preco"])
        registro.estoque = int(request.form["estoque"])
        registro.usuario_id = int(request.form["usuario_id"])
        registro.categoria_id = int(request.form["categoria_id"])
        db.session.commit()
        flash("Anúncio alterado com sucesso.")
        return redirect(url_for("main.anuncios"))
    return render_template("anuncio_form.html", registro=registro, usuarios=Usuario.query.all(), categorias=Categoria.query.all())

@main.route("/anuncios/<int:id>/excluir", methods=["POST"])
def anuncio_excluir(id):
    registro = Anuncio.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    flash("Anúncio excluído com sucesso.")
    return redirect(url_for("main.anuncios"))

# PERGUNTAS
@main.route("/perguntas")
def perguntas():
    return render_template("perguntas.html", registros=Pergunta.query.order_by(Pergunta.id.desc()).all())

@main.route("/perguntas/novo", methods=["GET", "POST"])
def pergunta_novo():
    if request.method == "POST":
        registro = Pergunta(
            texto=request.form["texto"],
            resposta=request.form["resposta"],
            usuario_id=int(request.form["usuario_id"]),
            anuncio_id=int(request.form["anuncio_id"])
        )
        db.session.add(registro)
        db.session.commit()
        flash("Pergunta cadastrada com sucesso.")
        return redirect(url_for("main.perguntas"))
    return render_template("pergunta_form.html", registro=None, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@main.route("/perguntas/<int:id>/editar", methods=["GET", "POST"])
def pergunta_editar(id):
    registro = Pergunta.query.get_or_404(id)
    if request.method == "POST":
        registro.texto = request.form["texto"]
        registro.resposta = request.form["resposta"]
        registro.usuario_id = int(request.form["usuario_id"])
        registro.anuncio_id = int(request.form["anuncio_id"])
        db.session.commit()
        flash("Pergunta alterada com sucesso.")
        return redirect(url_for("main.perguntas"))
    return render_template("pergunta_form.html", registro=registro, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@main.route("/perguntas/<int:id>/excluir", methods=["POST"])
def pergunta_excluir(id):
    registro = Pergunta.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    flash("Pergunta excluída com sucesso.")
    return redirect(url_for("main.perguntas"))

# COMPRAS
@main.route("/compras")
def compras():
    return render_template("compras.html", registros=Compra.query.order_by(Compra.id.desc()).all())

@main.route("/compras/novo", methods=["GET", "POST"])
def compra_novo():
    if request.method == "POST":
        registro = Compra(
            quantidade=int(request.form["quantidade"]),
            valor_unitario=float(request.form["valor_unitario"]),
            comprador_id=int(request.form["comprador_id"]),
            anuncio_id=int(request.form["anuncio_id"])
        )
        db.session.add(registro)
        db.session.commit()
        flash("Compra cadastrada com sucesso.")
        return redirect(url_for("main.compras"))
    return render_template("compra_form.html", registro=None, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@main.route("/compras/<int:id>/editar", methods=["GET", "POST"])
def compra_editar(id):
    registro = Compra.query.get_or_404(id)
    if request.method == "POST":
        registro.quantidade = int(request.form["quantidade"])
        registro.valor_unitario = float(request.form["valor_unitario"])
        registro.comprador_id = int(request.form["comprador_id"])
        registro.anuncio_id = int(request.form["anuncio_id"])
        db.session.commit()
        flash("Compra alterada com sucesso.")
        return redirect(url_for("main.compras"))
    return render_template("compra_form.html", registro=registro, usuarios=Usuario.query.all(), anuncios=Anuncio.query.all())

@main.route("/compras/<int:id>/excluir", methods=["POST"])
def compra_excluir(id):
    registro = Compra.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    flash("Compra excluída com sucesso.")
    return redirect(url_for("main.compras"))

# LISTAS DE FAVORITOS
@main.route("/favoritos")
def favoritos():
    listas = ListaFavoritos.query.order_by(ListaFavoritos.id.desc()).all()
    itens = Favorito.query.order_by(Favorito.id.desc()).all()
    return render_template("favoritos.html", listas=listas, itens=itens)

@main.route("/favoritos/listas/novo", methods=["GET", "POST"])
def lista_nova():
    if request.method == "POST":
        registro = ListaFavoritos(nome=request.form["nome"], usuario_id=int(request.form["usuario_id"]))
        db.session.add(registro)
        db.session.commit()
        flash("Lista de favoritos cadastrada com sucesso.")
        return redirect(url_for("main.favoritos"))
    return render_template("lista_form.html", registro=None, usuarios=Usuario.query.all())

@main.route("/favoritos/listas/<int:id>/editar", methods=["GET", "POST"])
def lista_editar(id):
    registro = ListaFavoritos.query.get_or_404(id)
    if request.method == "POST":
        registro.nome = request.form["nome"]
        registro.usuario_id = int(request.form["usuario_id"])
        db.session.commit()
        flash("Lista alterada com sucesso.")
        return redirect(url_for("main.favoritos"))
    return render_template("lista_form.html", registro=registro, usuarios=Usuario.query.all())

@main.route("/favoritos/listas/<int:id>/excluir", methods=["POST"])
def lista_excluir(id):
    registro = ListaFavoritos.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    flash("Lista excluída com sucesso.")
    return redirect(url_for("main.favoritos"))

@main.route("/favoritos/itens/novo", methods=["GET", "POST"])
def favorito_novo():
    if request.method == "POST":
        registro = Favorito(lista_id=int(request.form["lista_id"]), anuncio_id=int(request.form["anuncio_id"]))
        db.session.add(registro)
        db.session.commit()
        flash("Favorito cadastrado com sucesso.")
        return redirect(url_for("main.favoritos"))
    return render_template("favorito_form.html", registro=None, listas=ListaFavoritos.query.all(), anuncios=Anuncio.query.all())

@main.route("/favoritos/itens/<int:id>/editar", methods=["GET", "POST"])
def favorito_editar(id):
    registro = Favorito.query.get_or_404(id)
    if request.method == "POST":
        registro.lista_id = int(request.form["lista_id"])
        registro.anuncio_id = int(request.form["anuncio_id"])
        db.session.commit()
        flash("Favorito alterado com sucesso.")
        return redirect(url_for("main.favoritos"))
    return render_template("favorito_form.html", registro=registro, listas=ListaFavoritos.query.all(), anuncios=Anuncio.query.all())

@main.route("/favoritos/itens/<int:id>/excluir", methods=["POST"])
def favorito_excluir(id):
    registro = Favorito.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()
    flash("Favorito excluído com sucesso.")
    return redirect(url_for("main.favoritos"))

# RELATÓRIOS
@main.route("/relatorios")
def relatorios():
    vendas = db.session.query(Compra).join(Anuncio).order_by(Compra.id.desc()).all()
    compras = Compra.query.order_by(Compra.id.desc()).all()
    return render_template("relatorios.html", vendas=vendas, compras=compras)
