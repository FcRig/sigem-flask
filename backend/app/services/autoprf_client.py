import requests
from datetime import datetime
import re


class AutoPRFClient:
    """Simple client to interact with the AutoPRF HTTP API."""

    BASE_URL = "https://auto.prf.gov.br/api"

    def __init__(self, jwt_token: str | None = None):
        self.jwt_token = jwt_token or ""

    def login(self, cpf: str, password: str, token: str) -> str:
        """ Autentica no sistema AutoPRF e retorna o token JWT da sessão."""   
             
        payload = {
            "ip": "0.0.0.0",
            "usuario": cpf,
            "senha": password,
            "token": token,
        }

        try:
            response = requests.post(f"{self.BASE_URL}/auth/login", json=payload)
            response.raise_for_status()

            jwt = response.text.strip()
            if not jwt or len(jwt) < 20:
                raise ValueError("Token JWT ausente ou inválido.")

            self.jwt_token = jwt
            return jwt

        except requests.HTTPError as e:
            print(f"[AutoPRF] Erro HTTP na autenticação: {e} - Status: {response.status_code}")
            print(f"Resposta do servidor: {response.text}")
            raise

        except Exception as e:
            print(f"[AutoPRF] Erro inesperado no login: {e}")
            raise


    def pesquisa_auto_infracao(self, numero: str) -> dict:
        """Return data about an Auto de Infracao in the same structure used by the frontend."""
        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        # First request retrieves the page information so we can obtain the
        # identifier of the auto de infração
        response = requests.get(
            f"{self.BASE_URL}/auto-infracao/page",
            params={"numero": numero},
            headers=headers,
        )
        response.raise_for_status()
        data = response.json() if response.content else {}        
        
        item = (data.get("items") or [{}])[0]

        auto_id = item.get("id")
        id_processo = item.get("idProcesso")

        result = {
            "id": auto_id,
            "idProcesso": id_processo,
            "infracao": {},
            "veiculo": {},
            "local": {},
            "medicoes": {},
            "equipamento": {},
            "observacoes": None,
        }

        if not auto_id:
            # If we could not find the identifier we return an empty result
            return result

        # Fetch full details for the auto using its id
        response = requests.get(
            f"{self.BASE_URL}/auto-infracao/{auto_id}",
            headers=headers,
        )
        response.raise_for_status()
        item = response.json() if response.content else {}
        if not item:
            return result

        # Informacoes da infracao
        infracao = item.get("infracao", {})
        codigo = infracao.get("codigo")
        descricao = infracao.get("descricao")
        if codigo or descricao:
            result["infracao"]["codigo_descricao"] = (
                f"{codigo} - {descricao}" if codigo else descricao
            )
        result["infracao"]["amparo_legal"] = infracao.get("amparoLegal")
        gravidade = (infracao.get("valorBase") or {}).get("gravidade")
        if gravidade:
            result["infracao"]["gravidade"] = gravidade
        if infracao.get("tipoInfrator"):
            result["infracao"]["tipo_infrator"] = infracao.get("tipoInfrator")
        result["infracao"]["tipo_abordagem"] = (
            "Com Abordagem" if item.get("comAbordagem") else "Sem Abordagem"
        )

        # Veiculo
        veiculo = item.get("veiculo", {})
        result["veiculo"]["emplacamento"] = veiculo.get("emplacamento")
        result["veiculo"]["placa"] = veiculo.get("placa")
        result["veiculo"]["renavam"] = veiculo.get("renavam")
        result["veiculo"]["chassi"] = veiculo.get("chassi")
        result["veiculo"]["pais"] = veiculo.get("pais")
        result["veiculo"]["uf"] = veiculo.get("uf")
        result["veiculo"]["marca"] = (veiculo.get("marca") or {}).get("nome")
        result["veiculo"]["modelo"] = veiculo.get("modelo")
        result["veiculo"]["cor"] = veiculo.get("cor")
        result["veiculo"]["especie"] = veiculo.get("especie")
        result["veiculo"]["tipo"] = veiculo.get("tipo")
        result["veiculo"]["categoria"] = veiculo.get("categoria")
        result["veiculo"]["tipo_composicao"] = veiculo.get("tipoComposicao")

        envolvidos = item.get("envolvidos") or []
        proprietario = next(
            (e for e in envolvidos if "Propriet\u00e1rio" in e.get("tiposEnvolvimento", [])),
            None,
        )
        if proprietario:
            doc = (proprietario.get("documentos") or [{}])[0]
            result["veiculo"]["tipo_documento"] = doc.get("tipoDocumento")
            result["veiculo"]["numero_documento"] = doc.get("numero")
            result["veiculo"]["nome_razao_social"] = proprietario.get("nome")

        # Localizacao
        local = item.get("local", {})
        municipio = local.get("municipio") or {}
        cod = municipio.get("codigoMunicipioRenainf")
        nome = municipio.get("nome")
        uf = municipio.get("uf")
        if cod or nome or uf:
            if cod:
                result["local"]["codigo_municipio_uf"] = f"{cod} - {nome}/{uf}" if nome or uf else str(cod)
            else:
                result["local"]["codigo_municipio_uf"] = f"{nome}/{uf}" if nome or uf else None
        result["local"]["rodovia"] = (local.get("rodovia") or {}).get("sigla")
        km = local.get("km")
        result["local"]["km"] = str(km) if km is not None else None
        result["local"]["sentido"] = local.get("sentido")
        data_hora = item.get("dataHoraLocal") or item.get("dataHora")
        if data_hora:
            try:
                dt = datetime.fromisoformat(data_hora)
                result["local"]["data_hora"] = dt.strftime("%d/%m/%Y %H:%M:%S")
            except ValueError:
                result["local"]["data_hora"] = data_hora

        # Campo medições
        medicao = item.get("medicao") or {}
        result["medicoes"]["tipo"] = infracao.get("medicao")
        result["medicoes"]["comprovacao"] = medicao.get("comprovadoPor")
        itens = medicao.get("itensMedidos") or []
        if itens:
            med = itens[0]
            result["medicoes"]["realizada"] = med.get("medicaoReal")
            result["medicoes"]["considerada"] = med.get("medicaoConsiderada")
            result["medicoes"]["limite"] = med.get("limitePermitido")
            result["medicoes"]["excesso"] = med.get("excesso")

        equipamento = medicao.get("equipamentoMedicao") or {}
        result["equipamento"]["numero"] = equipamento.get("numeroSerie")
        result["equipamento"]["descricao"] = equipamento.get("descricao")
        result["equipamento"]["marca"] = equipamento.get("marca")
        result["equipamento"]["modelo"] = equipamento.get("modelo")

        result["observacoes"] = item.get("observacao")
        return result

    def get_envolvidos(self, auto_id: int | str) -> list:
        """Return the list of people/vehicles involved in a given Auto de Infracao."""
        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        response = requests.get(
            f"{self.BASE_URL}/auto-infracao/env/{auto_id}",
            headers=headers,
        )
        response.raise_for_status()
        data = response.json() if response.content else []
        for env in data:
            numero = env.get("numeroDocumento")
            tipo = (env.get("tipoDocumento") or "").upper()
            if numero and "CNPJ" in tipo:
                digits = re.sub(r"\D", "", str(numero))
                if len(digits) < 14:
                    env["numeroDocumento"] = digits.zfill(14)
        return data

    def solicitar_cancelamento(self, numero_auto: str, payload: dict) -> dict:
        """Submit a cancelamento request for a given Auto de Infracao."""        
        
        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"

        # Access the auto page so the service can locate the process
        resp = requests.get(
            f"{self.BASE_URL}/auto-infracao/page",
            params={"numero": numero_auto},
            headers=headers,
        )
        resp.raise_for_status()

        resp = requests.post(
            f"{self.BASE_URL}/solicitacao/CANCELAMENTO/lote",
            json=payload,
            headers=headers,
        )
        print(resp)
        resp.raise_for_status()
        return resp.json() if resp.content else True

    def historico(self, id_processo: int | str) -> list:
        """Return the list of status updates for a given processo."""

        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"

        resp = requests.get(
            f"{self.BASE_URL}/auto-infracao/{id_processo}/historico",
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json() if resp.content else []

    def anexar_documento_processo(
        self, id_processo: int | str, file_bytes: bytes, filename: str
    ) -> bool:
        """Envia um PDF e o anexa ao processo informado."""

        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"

        # Recupera dados atuais do processo (e anexos existentes)
        resp = requests.get(
            f"{self.BASE_URL}/anexar-documento-processo/{id_processo}",
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json() if resp.content else {}

        arquivos = data.get("arquivos") or []

        # Envia o arquivo para criação do temporário
        upload_headers = {
            "Content-Type": "application/pdf",
            "Referer": "https://auto.prf.gov.br/",
        }
        if self.jwt_token:
            upload_headers["Authorization"] = f"Bearer {self.jwt_token}"

        resp = requests.post(
            f"{self.BASE_URL}/arquivo/temp",
            data=file_bytes,
            headers=upload_headers,
        )
        resp.raise_for_status()
        nome_temp = resp.text.strip()

        arquivos.append(
            {
                "tipo": "OFICIO",
                "extensao": "PDF",
                "dataHora": datetime.utcnow().isoformat(),
                "tamanhoArquivo": len(file_bytes),
                "nomeArquivoTemp": nome_temp,
                "file": {},
            }
        )

        payload = data
        payload["arquivos"] = arquivos

        resp = requests.put(
            f"{self.BASE_URL}/anexar-documento-processo/{id_processo}",
            json=payload,
            headers=headers,
        )
        resp.raise_for_status()

        if resp.content:
            try:
                result = resp.json()
                if isinstance(result, bool):
                    return result
                return bool(result.get("ok", True))
            except Exception:
                pass
        return True
