from flask import Blueprint, render_template, request, redirect, url_for

from . import db
from .models import (
    Usuario,
    Categoria,
    Anuncio,
    Pergunta,
    Compra,
    ListaFavoritos,
    Favorito
)


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/usuarios")
def usuarios():
    usuarios = Usuario.query.all()

    return render_template(
        "usuarios.html",
        usuarios=usuarios
    )


@bp.route("/categorias")
def categorias():
    categorias = Categoria.query.all()

    return render_template(
        "categorias.html",
        categorias=categorias
    )


@bp.route("/anuncios")
def anuncios():
    anuncios = Anuncio.query.all()

    return render_template(
        "anuncios.html",
        anuncios=anuncios
    )


@bp.route("/anuncios/novo", methods=["GET", "POST"])
def novo_anuncio():

    if request.method == "POST":

        anuncio = Anuncio(
            titulo=request.form["titulo"],
            descricao=request.form["descricao"],
            preco=float(request.form["preco"]),
            estoque=int(request.form["estoque"]),
            usuario_id=int(request.form["usuario_id"]),
            categoria_id=int(request.form["categoria_id"])
        )

        db.session.add(anuncio)
        db.session.commit()

        return redirect(
            url_for("main.anuncios")
        )

    return render_template(
        "form_anuncio.html",
        usuarios=Usuario.query.all(),
        categorias=Categoria.query.all()
    )


@bp.route("/perguntas")
def perguntas():
    perguntas = Pergunta.query.all()

    return render_template(
        "perguntas.html",
        perguntas=perguntas
    )


@bp.route("/compras")
def compras():
    compras = Compra.query.all()

    return render_template(
        "compras.html",
        compras=compras
    )


@bp.route("/favoritos")
def favoritos():

    listas = ListaFavoritos.query.all()
    favoritos = Favorito.query.all()

    return render_template(
        "favoritos.html",
        listas=listas,
        favoritos=favoritos
    )


@bp.route("/relatorios")
def relatorios():

    vendas = Compra.query.join(Anuncio).all()
    compras = Compra.query.all()

    return render_template(
        "relatorios.html",
        vendas=vendas,
        compras=compras
    )