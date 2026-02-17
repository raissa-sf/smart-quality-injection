import os
import PyPDF2
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv


load_dotenv()

class AIEngine:
    def __init__(self, model_name="llama-3.1-8b-instant"):
        api_key = os.getenv("GROQ_API_KEY")
        self.chat = ChatGroq(
            temperature=0, 
            groq_api_key=api_key, 
            model_name=model_name
        )

    def extrair_texto_pdf(self, caminho_pdf):
        """Lê o manual técnico e extrai o texto para contexto."""
        try:
            if os.path.exists(caminho_pdf):
                with open(caminho_pdf, "rb") as f:
                    leitor = PyPDF2.PdfReader(f)
                    texto = "".join([p.extract_text() for p in leitor.pages if p.extract_text()])
                    return texto
            return "Manual técnico não encontrado."
        except Exception as e:
            return f"Erro ao ler manual: {e}"

    def gerar_relatorio_turno(self, op, total, reprovas, observacoes):
        """Lógica para o Supervisor de IA resumir a situação da OP."""
        mensagens = [
            SystemMessage(content="""Você é um Engenheiro de Processos Sênior em Injeção Plástica. 
            Analise os logs e gere um resumo executivo:
            1.  **Status Quantitativo**: Calcule a % de refugo.
            2.  **Diagnóstico**: Identifique se os defeitos são recorrentes ou isolados.
            3.  **Diretriz para o Próximo Turno**: Liste 2 ações preventivas baseadas nos problemas relatados (ex: verificar refrigeração, limpar bico, ajustar contrapressão).
            
            Seja direto, use jargões técnicos (ex: rechupe, queima, ciclo, purga) e mantenha tom de urgência se as reprovas forem > 5%."""),
            HumanMessage(content=f"DADOS DA OP {op}:\nInspeções: {total}\nReprovações: {reprovas}\nLogs de Observação: {observacoes}")
        ]
        return self.chat.invoke(mensagens).content

    def consultar_manual(self, pergunta, contexto_pdf):
        """Responde dúvidas técnicas baseadas no texto do PDF."""
        mensagens = [
            SystemMessage(content=f"""Você é o Assistente Técnico da Fábrica. 
            Responda APENAS com base no manual fornecido: {contexto_pdf[:15000]} 
            (limitado aos primeiros 15k caracteres para estabilidade).
            
            Regras:
            - Se a informação não estiver no manual, diga: 'Informação não localizada no manual técnico'.
            - Use listas para procedimentos de segurança ou parâmetros de máquina.
            - Mantenha a resposta curta e objetiva para leitura rápida em tablets/celulares."""),
            HumanMessage(content=pergunta)
        ]

        return self.chat.invoke(mensagens).content
