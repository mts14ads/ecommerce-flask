Plataforma de E-commerce - Flask

Projeto desenvolvido para atividade curricular utilizando Python, Flask, Flask-SQLAlchemy e SQLite.

Objetivo

Desenvolver a estrutura inicial de uma plataforma de e-commerce onde usuários podem:

Criar anúncios;
Comprar produtos;
Fazer perguntas em anúncios;
Responder perguntas;
Criar listas de favoritos;
Consultar compras;
Consultar vendas.

Tecnologias
Python
Flask
Flask-SQLAlchemy
SQLite
HTML
Jinja2

Estrutura:
ecommerce-flask/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   └── static/
├── .gitignore
├── requirements.txt
├── run.py
└── README.md

Entidades:
Usuário
Anúncio
Categoria
Pergunta
Compra
ListaFavoritos
Favorito

Rotas principais:
/                   Página inicial
/usuarios           Usuários
/categorias         Categorias
/anuncios           Anúncios
/anuncios/novo      Novo anúncio
/perguntas          Perguntas
/compras            Compras
/favoritos          Favoritos
/relatorios         Relatórios
Como executar

Clone o repositório:

git clone https://github.com/mts14ads/ecommerce-flask.git

Entre na pasta:

cd ecommerce-flask

Crie o ambiente virtual:

python -m venv venv

Ative no Windows:

venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

Execute:

python run.py

Acesse:

http://127.0.0.1:5000/
