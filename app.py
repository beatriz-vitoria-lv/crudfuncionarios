import os
import re

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "chave-local-desenvolvimento")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://crud_user:crud_password@db:5432/crud_funcionarios",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Funcionario(db.Model):
    __tablename__ = "funcionarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False, index=True)


def somente_digitos(valor):
    return re.sub(r"\D", "", valor or "")


def cpf_valido(cpf):
    cpf = somente_digitos(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for tamanho in (9, 10):
        soma = sum(int(digito) * peso for digito, peso in zip(cpf[:tamanho], range(tamanho + 1, 1, -1)))
        resto = (soma * 10) % 11
        digito = 0 if resto == 10 else resto
        if digito != int(cpf[tamanho]):
            return False
    return True


@app.route("/")
def index():
    funcionarios = Funcionario.query.order_by(Funcionario.nome.asc()).all()
    return render_template("index.html", funcionarios=funcionarios)


@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cpf = somente_digitos(request.form.get("cpf"))
        if not nome or len(nome) > 120:
            flash("Informe um nome válido (até 120 caracteres).", "erro")
        elif not cpf_valido(cpf):
            flash("CPF inválido. Confira os números digitados.", "erro")
        else:
            db.session.add(Funcionario(nome=nome, cpf=cpf))
            try:
                db.session.commit()
                flash("Funcionário cadastrado com sucesso!", "sucesso")
                return redirect(url_for("index"))
            except IntegrityError:
                db.session.rollback()
                flash("Já existe um funcionário cadastrado com esse CPF.", "erro")
    return render_template("editar.html", funcionario=None, titulo="Novo funcionário")


@app.route("/editar/<int:funcionario_id>", methods=["GET", "POST"])
def editar(funcionario_id):
    funcionario = db.get_or_404(Funcionario, funcionario_id)
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cpf = somente_digitos(request.form.get("cpf"))
        if not nome or len(nome) > 120:
            flash("Informe um nome válido (até 120 caracteres).", "erro")
        elif not cpf_valido(cpf):
            flash("CPF inválido. Confira os números digitados.", "erro")
        else:
            funcionario.nome = nome
            funcionario.cpf = cpf
            try:
                db.session.commit()
                flash("Cadastro atualizado com sucesso!", "sucesso")
                return redirect(url_for("index"))
            except IntegrityError:
                db.session.rollback()
                flash("Esse CPF já pertence a outro funcionário.", "erro")
    return render_template("editar.html", funcionario=funcionario, titulo="Editar funcionário")


@app.post("/excluir/<int:funcionario_id>")
def excluir(funcionario_id):
    funcionario = db.get_or_404(Funcionario, funcionario_id)
    db.session.delete(funcionario)
    db.session.commit()
    flash("Funcionário excluído.", "sucesso")
    return redirect(url_for("index"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
