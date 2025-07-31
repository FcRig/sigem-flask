"""Rotas relacionadas à criação de processos no SEI.

Este módulo define uma blueprint que exibe um formulário para
criar um novo processo no SEI e lista as unidades disponíveis para o
usuário selecionar. O comportamento segue o padrão usado pelo
``spidr-engine``.
"""

from __future__ import annotations

from flask import Blueprint, render_template, request, redirect, url_for, flash

from ..services.sei_unidades_client import listar_unidades_usuario, Unidade

# Definir blueprint com prefixo de URL. Isso permitirá acessar as rotas
# deste módulo sob "/processos".
bp = Blueprint("criar_processo", __name__, url_prefix="/processos")


@bp.route("/novo", methods=["GET", "POST"])
def criar_processo() -> str:
    """Exibe o formulário e processa a criação de um novo processo.

    Quando acessado via ``GET`` a função obtém a lista de
    unidades disponíveis para o usuário corrente e a repassa ao
    template.  No ``POST``, a função recolhe os dados enviados
    pelo formulário e realiza as chamadas necessárias para criar o
    processo no SEI (aqui representado apenas por uma mensagem de
    sucesso).  Uma aplicação real deverá implementar a chamada ao
    serviço correspondente do SEI.
    """
    if request.method == "POST":
        unidade_id = request.form.get("unidade_id")
        assunto = request.form.get("assunto")
        especificacao = request.form.get("especificacao")
        if not unidade_id:
            flash("Selecione uma unidade para criar o processo.", "danger")
        else:
            # Aqui iríamos chamar o serviço de inclusão de processo do SEI
            flash(f"Processo criado na unidade {unidade_id} com assunto '{assunto}'.", "success")
            return redirect(url_for("criar_processo.criar_processo"))

    # Para requisições GET (ou em caso de erro de validação), obter a lista
    # de unidades do serviço.  Idealmente deveria ser feito com o
    # contexto do usuário autenticado; aqui está simplificado.
    unidades: list[Unidade] = listar_unidades_usuario()
    return render_template("criar_processo.html", unidades=unidades)
