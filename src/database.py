import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

class Database:
    def __init__(self, credentials_path="credenciais.json"):
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, self.scope)
        self.client = gspread.authorize(self.creds)
        self.planilha = self.client.open("DB_Sistema_Qualidade")

    def buscar_dados_completos(self, numero_op):
        
        try:
            aba_ops = self.planilha.worksheet("ordens_producao")
            op_encontrada = next((op for op in aba_ops.get_all_records() if str(op['numero_op']) == str(numero_op)), None)
            
            if not op_encontrada:
                return None

            aba_pecas = self.planilha.worksheet("cadastro_pecas")
            peca_dados = next((p for p in aba_pecas.get_all_records() if p['id_peca'] == op_encontrada['id_peca']), None)
            
            if peca_dados:
               
                return {**op_encontrada, **peca_dados}
            return None
        except Exception as e:
            print(f"Erro ao acessar banco de dados: {e}")
            return None

    def salvar_log(self, dados_linha):
        """
        Salva uma nova linha na aba log_inspecoes.
        dados_linha: lista com os valores na ordem das colunas da planilha
        """
        try:
            aba_logs = self.planilha.worksheet("log_inspecoes")
            aba_logs.append_row(dados_linha)
            return True
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            return False

    def obter_historico_recente(self, quantidade=30):
        """Retorna os últimos registros para o relatório de turno."""
        try:
            return self.planilha.worksheet("log_inspecoes").get_all_records()[-quantidade:]
        except:

            return []
