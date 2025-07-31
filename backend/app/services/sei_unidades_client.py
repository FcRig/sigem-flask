from __future__ import annotations

from dataclasses import dataclass
from os import getenv
from typing import List

import logging

import requests


logger = logging.getLogger(__name__)


@dataclass
class Unidade:
    """Representa uma unidade organizacional no SEI.

    Cada unidade possui um identificador (id_unidade), uma sigla e uma
    descrição completa. Estes atributos são utilizados nas chamadas
    aos serviços do SEI/SEI-Broker.
    """

    id_unidade: str
    sigla: str
    descricao: str

    def __str__(self) -> str:  # pragma: no cover - conveniência
        return f"{self.sigla} - {self.descricao}"


def listar_unidades_usuario(token: str | None = None) -> List[Unidade]:
    """Retorna a lista de unidades disponíveis para o usuário atual.

    Esta função utiliza as variáveis de ambiente `SEI_BROKER_URL`,
    `SEI_BROKER_USER` e `SEI_BROKER_PASSWORD` para se conectar ao
    broker do SEI. Caso a variável `SEI_MOCK_DATA` esteja definida
    como ``true`` (insensível a caixa), um conjunto de unidades
    fictícias é retornado para facilitar o desenvolvimento sem
    dependência de um servidor externo.
    """
    # Retornar unidades fictícias se especificado
    if getenv("SEI_MOCK_DATA", "false").lower() == "true":
        logger.debug("Retornando unidades mockadas")
        return [
            Unidade(id_unidade="1", sigla="GAB", descricao="Gabinete da Presidência"),
            Unidade(id_unidade="2", sigla="TEC", descricao="Departamento de Tecnologia"),
            Unidade(id_unidade="3", sigla="ADM", descricao="Diretoria Administrativa"),
        ]

    broker_url = getenv("SEI_BROKER_URL")
    user = getenv("SEI_BROKER_USER")
    password = getenv("SEI_BROKER_PASSWORD")
    if not broker_url:
        logger.warning("SEI_BROKER_URL não configurada; retornando lista vazia")
        return []

    endpoint = f"{broker_url.rstrip('/')}/service/tarefas/listar-unidades"
    headers = {"Content-Type": "application/json"}
    params: dict[str, str] = {}
    auth: tuple[str, str] | None = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    elif user and password:
        auth = (user, password)

    try:
        logger.debug("Realizando requisição GET para %s", endpoint)
        response = requests.get(endpoint, headers=headers, params=params, auth=auth, timeout=15)
        response.raise_for_status()
        data = response.json()
        unidades: list[Unidade] = []
        for item in data.get("unidades", []):
            unidades.append(
                Unidade(
                    id_unidade=str(item.get("idUnidade") or item.get("id_unidade")),
                    sigla=str(item.get("sigla")),
                    descricao=str(item.get("descricao")),
                )
            )
        logger.debug("Unidades retornadas: %d", len(unidades))
        return unidades
    except Exception as exc:  # noqa: BLE001
        logger.exception("Erro ao consultar unidades do SEI: %s", exc)
        return []
