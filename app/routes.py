from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import generate_password_hash, check_password_hash

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


main = Blueprint("main", __name__)


# ============================================================
# AUTENTICAÇÃO
# ============================================================

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para acessar esta área.")
            return redirect(
                url_for(
                    "main.login",
                    next=request.path
                )
            )

        return view(*args, **kwargs)

    return wrapped


# ============================================================
# PÁGINA INICIAL
# ============================================================

@main.route("/")
def index():
    return render_template("index.html")


# ============================================================
# LOGIN
# ============================================================

@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario and check_password_hash(
            usuario.senha,
            senha
        ):

            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome

            flash("Login realizado com sucesso.")

            return redirect(
                request.args.get("next")
                or url_for("main.index")
            )

        flash("E-mail ou senha inválidos.")

    return render_template("login.html")


# ============================================================
# CADASTRO
# ============================================================

@main.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        usuario_existente = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario_existente:

            flash("Este e-mail já está cadastrado.")

            return render_template(
                "cadastro.html"
            )

        senha_hash = generate_password_hash(
            senha
        )

        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash
        )

        db.session.add(usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso.")

        return redirect(
            url_for("main.login")
        )

    return render_template("cadastro.html")


# ============================================================
# LOGOUT
# ============================================================

@main.route("/logout")
def logout():

    session.clear()

    flash("Sessão encerrada.")

    return redirect(
        url_for("main.index")
    )


# ============================================================
# FUNÇÃO PARA CONVERTER CAMPOS
# ============================================================

def converter_valor(campo, valor):

    campos_inteiros = {
        "estoque",
        "usuario_id",
        "categoria_id",
        "quantidade",
        "comprador_id",
        "anuncio_id",
        "lista_id"
    }

    campos_float = {
        "preco",
        "valor_unitario"
    }

    if campo in campos_inteiros:
        return int(valor)

    if campo in campos_float:
        return float(valor)

    return valor


# ============================================================
# GERADOR DE CRUD
# ============================================================

def criar_crud(
    model,
    nome,
    endpoint,
    campos
):

    # --------------------------------------------------------
    # LISTAGEM
    # --------------------------------------------------------

    def listar():

        registros = model.query.order_by(
            model.id.desc()
        ).all()

        return render_template(
            "crud.html",
            title=nome,
            endpoint=endpoint,
            registros=registros,
            fields=campos
        )

    listar.__name__ = f"{endpoint}_listar"

    main.add_url_rule(
        f"/{endpoint}",
        endpoint=f"{endpoint}_listar",
        view_func=login_required(listar)
    )

    # --------------------------------------------------------
    # NOVO
    # --------------------------------------------------------

    def novo():

        if request.method == "POST":

            dados = {}

            for campo in campos:

                valor = request.form.get(
                    campo,
                    ""
                )

                if (
                    model is Usuario
                    and campo == "senha"
                ):

                    valor = generate_password_hash(
                        valor
                    )

                else:

                    valor = converter_valor(
                        campo,
                        valor
                    )

                dados[campo] = valor

            registro = model(**dados)

            db.session.add(registro)
            db.session.commit()

            flash(
                f"{nome}: registro cadastrado com sucesso."
            )

            return redirect(
                url_for(
                    f"main.{endpoint}_listar"
                )
            )

        return render_template(
            "form.html",
            title=f"Novo {nome}",
            endpoint=endpoint,
            fields=campos,
            values={}
        )

    novo.__name__ = f"{endpoint}_novo"

    main.add_url_rule(
        f"/{endpoint}/novo",
        endpoint=f"{endpoint}_novo",
        view_func=login_required(novo),
        methods=["GET", "POST"]
    )

    # --------------------------------------------------------
    # EDITAR
    # --------------------------------------------------------

    def editar(id):

        registro = model.query.get_or_404(id)

        if request.method == "POST":

            for campo in campos:

                valor = request.form.get(
                    campo,
                    ""
                )

                # Não altera senha se o campo ficar vazio
                if (
                    model is Usuario
                    and campo == "senha"
                    and valor == ""
                ):
                    continue

                if (
                    model is Usuario
                    and campo == "senha"
                ):

                    valor = generate_password_hash(
                        valor
                    )

                else:

                    valor = converter_valor(
                        campo,
                        valor
                    )

                setattr(
                    registro,
                    campo,
                    valor
                )

            db.session.commit()

            flash(
                "Registro atualizado com sucesso."
            )

            return redirect(
                url_for(
                    f"main.{endpoint}_listar"
                )
            )

        valores = {}

        for campo in campos:

            valores[campo] = getattr(
                registro,
                campo
            )

        return render_template(
            "form.html",
            title=f"Editar {nome}",
            endpoint=endpoint,
            fields=campos,
            values=valores
        )

    editar.__name__ = f"{endpoint}_editar"

    main.add_url_rule(
        f"/{endpoint}/<int:id>/editar",
        endpoint=f"{endpoint}_editar",
        view_func=login_required(editar),
        methods=["GET", "POST"]
    )

    # --------------------------------------------------------
    # EXCLUIR
    # --------------------------------------------------------

    def excluir(id):

        registro = model.query.get_or_404(id)

        # Impede excluir o próprio usuário conectado
        if (
            model is Usuario
            and id == session.get("usuario_id")
        ):

            flash(
                "Não é possível excluir o usuário conectado."
            )

            return redirect(
                url_for(
                    f"main.{endpoint}_listar"
                )
            )

        db.session.delete(registro)
        db.session.commit()

        flash(
            "Registro excluído com sucesso."
        )

        return redirect(
            url_for(
                f"main.{endpoint}_listar"
            )
        )

    excluir.__name__ = f"{endpoint}_excluir"

    main.add_url_rule(
        f"/{endpoint}/<int:id>/excluir",
        endpoint=f"{endpoint}_excluir",
        view_func=login_required(excluir),
        methods=["POST"]
    )


# ============================================================
# CRUD DOS USUÁRIOS
# ============================================================

criar_crud(
    Usuario,
    "Usuários",
    "usuarios",
    [
        "nome",
        "email",
        "senha"
    ]
)


# ============================================================
# CRUD DAS CATEGORIAS
# ============================================================

criar_crud(
    Categoria,
    "Categorias",
    "categorias",
    [
        "nome",
        "descricao"
    ]
)


# ============================================================
# CRUD DOS ANÚNCIOS
# ============================================================

criar_crud(
    Anuncio,
    "Anúncios",
    "anuncios",
    [
        "titulo",
        "descricao",
        "preco",
        "estoque",
        "usuario_id",
        "categoria_id"
    ]
)


# ============================================================
# CRUD DAS PERGUNTAS
# ============================================================

criar_crud(
    Pergunta,
    "Perguntas",
    "perguntas",
    [
        "texto",
        "resposta",
        "usuario_id",
        "anuncio_id"
    ]
)


# ============================================================
# CRUD DAS COMPRAS
# ============================================================

criar_crud(
    Compra,
    "Compras",
    "compras",
    [
        "quantidade",
        "valor_unitario",
        "comprador_id",
        "anuncio_id"
    ]
)


# ============================================================
# CRUD DAS LISTAS DE FAVORITOS
# ============================================================

criar_crud(
    ListaFavoritos,
    "Listas de Favoritos",
    "listas-favoritos",
    [
        "nome",
        "usuario_id"
    ]
)


# ============================================================
# CRUD DOS FAVORITOS
# ============================================================

criar_crud(
    Favorito,
    "Favoritos",
    "favoritos",
    [
        "lista_id",
        "anuncio_id"
    ]
)


# ============================================================
# RELATÓRIOS
# ============================================================

@main.route("/relatorios")
@login_required
def relatorios():

    compras = Compra.query.all()

    return render_template(
        "relatorios.html",
        compras=compras
    )