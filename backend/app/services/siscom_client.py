import os
import requests


class SiscomClient:
    """Simple client to interact with the SISCOM service."""

    def __init__(self, endpoint: str | None = None):
        self.endpoint = endpoint or os.getenv("SISCOM_ENDPOINT")

    def pesquisar_ai(self, numero: str) -> dict:
        """Search for an Auto de Infracao and return a structured result."""
        response = requests.get(f"{self.endpoint}/{numero}")
        response.raise_for_status()
        payload = response.json() if response.content else {}

        if not payload:
            return {}

        result: dict[str, dict | None] = {
            "infracao": {},
            "veiculo": {},
            "local": {},
            "medicoes": None,
            "equipamento": None,
            "observacoes": payload.get("observacoes"),
        }

        codigo = payload.get("codigoInfracao")
        desc = payload.get("descAbreviadaInfracao")
        if codigo or desc:
            result["infracao"]["codigo_descricao"] = (
                f"{codigo} - {desc}" if codigo and desc else codigo or desc
            )
        result["infracao"]["amparo_legal"] = payload.get("enquadramentoInfracao")
        if payload.get("gravidadeInfracao"):
            result["infracao"]["gravidade"] = payload.get("gravidadeInfracao")
        if payload.get("tipoInfrator"):
            result["infracao"]["tipo_infrator"] = payload.get("tipoInfrator")
        if payload.get("tipoAbordagem"):
            result["infracao"]["tipo_abordagem"] = payload.get("tipoAbordagem")

        estrang = payload.get("veiculoEstrangeiro")
        if estrang is not None:
            result["veiculo"]["emplacamento"] = (
                "Estrangeiro" if str(estrang).lower() == "true" else "Nacional"
            )
        result["veiculo"]["placa"] = payload.get("placa")
        result["veiculo"]["chassi"] = payload.get("chassi")
        result["veiculo"]["renavam"] = payload.get("renavam")
        result["veiculo"]["pais"] = payload.get("pais")
        result["veiculo"]["uf"] = payload.get("ufPlaca")
        result["veiculo"]["marca"] = payload.get("marca")
        result["veiculo"]["outra_marca"] = payload.get("outraMarca")
        result["veiculo"]["modelo"] = payload.get("modelo")
        result["veiculo"]["cor"] = payload.get("cor")
        result["veiculo"]["especie"] = payload.get("descEspecie")
        result["veiculo"]["tipo"] = payload.get("tipo")
        result["veiculo"]["categoria"] = payload.get("categoria")
        result["veiculo"]["tipo_documento"] = payload.get("tipoDocumento")
        result["veiculo"]["numero_documento"] = payload.get("numeroDocumento")
        proprietario = payload.get("nomeCondutor") or payload.get("nomProprietario")
        if proprietario:
            result["veiculo"]["nome_razao_social"] = proprietario
        result["veiculo"]["tipo_composicao"] = payload.get("tipoComposicao")

        municipio = payload.get("municipioInfracao") or {}
        cod = municipio.get("codMunicipio")
        nome = municipio.get("nome")
        uf = municipio.get("UF")
        if cod or nome or uf:
            parts = []
            if cod:
                parts.append(str(cod))
            if nome or uf:
                nomeuf = f"{nome}/{uf}" if nome or uf else ""
                if cod:
                    parts.append(nomeuf)
                else:
                    parts = [nomeuf]
            result["local"]["codigo_municipio_uf"] = " - ".join(parts)
        result["local"]["rodovia"] = payload.get("brInfracao")
        if payload.get("kmInfracao") is not None:
            result["local"]["km"] = str(payload.get("kmInfracao"))
        result["local"]["sentido"] = payload.get("sentidoVia")
        data_hora = payload.get("dataHoraInfracao")
        if data_hora:
            result["local"]["data_hora"] = data_hora

        return result
