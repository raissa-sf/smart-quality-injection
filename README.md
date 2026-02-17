# 🏭 Sistema Inteligente de Controle de Qualidade - Injeção Plástica
**Autor:** Raissa Santos Feitosa  
**GitHub:** [raissa-sf](https://github.com/raissa-sf)  
**LinkedIn:** [Raissa Santos Feitosa](https://www.linkedin.com/in/raissa-santos-feitosa-73485b1a3/)


![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![AI](https://img.shields.io/badge/AI-Groq_%7C_Llama_3-f54e00?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets)
![Status](https://img.shields.io/badge/Status-Protótipo%20Funcional-green?style=for-the-badge)

> **Uma estação de inspeção digital para o chão de fábrica, substituindo formulários de papel por uma interface web responsiva integrada a uma camada de Inteligência Artificial.**

---

## 📸 Visão Geral

O sistema digitaliza o processo de qualidade, garantindo integridade dos dados e fornecendo suporte técnico em tempo real via IA.

| Identificação e Login | Padrão Visual e Inspeção |
|:---:|:---:|
| <img src="assets/tela_inicial.png" width="400"> | <img src="assets/padrao_visual.png" width="400"> |
| *Controle de acesso* | *Imagem de referência peça padrão* |

---

## 🚀 Funcionalidades Principais

### 1. Gestão de Turno e Operadores
- **Persistência Inteligente:** Sistema mantém o operador logado mesmo após recarregar a página (F5), recuperando o estado via URL params.
- **Troca Rápida:** Fluxo simplificado para troca de turno sem perda de dados.

### 2. Inspeção Técnica Digital
- **Metrologia Validada:** O operador insere a medida e o sistema compara instantaneamente com a Cota Nominal e Tolerâncias (+/-).
    - ✅ **Verde:** Aprovado.
    - 🚫 **Vermelho:** Reprovado (Bloqueia erros grosseiros).
- **Checklist Visual:** Pontos de verificação estética parametrizados por OP.
- **Padrão Visual:** Exibe a imagem de referência da peça (buscada no Drive/Nuvem) para comparação.


| Checklist | Validação Reprovada |
|:---:|:---:|
| <img src="assets/checkbox_marcado.png" width="400"> | <img src="assets/resumo_inspecao.png" width="400"> |

### 3. Assistente IA (Groq + Llama 3) 🤖
Utiliza a **Groq Cloud** para inferência em ultra-baixa latência:
- **RAG Técnico:** Chatbot que consulta o PDF do Manual de Processos e tira dúvidas do operador em milissegundos.
- **Passagem de Turno:** A IA lê as últimas inspeções no Google Sheets e gera um resumo executivo para o supervisor.
  
| Chatbot Técnico | Relatório de Turno (IA) | Chatbot Técnico (Sem alucinar)
|:---:|:---:| :---:|
| <img src="assets/assistente_ia.png" width="400"> | <img src="assets/passagem_turno.png" width="400"> |  <img src="assets/assistente_ia_alucinacao.png" width="400"> | 

### 4. Banco de Dados em Nuvem (Google Sheets) 📊
- **Zero Infraestrutura:** Não requer servidores SQL complexos.
- **Tempo Real:** Assim que o operador clica em "Salvar", a linha aparece na planilha do gestor.
- **Integração:** Permite criar Dashboards no Power BI ou Looker Studio conectados diretamente à planilha.
---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.13
* **Frontend:** [Streamlit](https://streamlit.io/) (Interface Web Data-Driven).
* **Inteligência Artificial:** Groq API + Meta Llama 3 (Para inferência em tempo real).
* **Database:** Google Sheets API (via `gspread` ou `streamlit-google-oauth`).
* **Processamento de Arquivos:** PyPDF2 / LangChain (Leitura de manuais técnicos).
* **Estilização:** CSS Customizado para melhorar a UX nativa do Streamlit.

---

## 📈 Impacto de Negócio

1.  **Redução de Erros:** Bloqueia o salvamento de medições fora da tolerância sem justificativa.
2.  **Padronização:** Garante que todos os operadores sigam o mesmo checklist visual, independente do turno.
3.  **Agilidade:** O supervisor recebe um resumo gerado por IA em segundos, eliminando a análise manual de pilhas de papel no final do dia.

---

## 📂 Estrutura do Projeto

```text
smart-quality-injection/
├─ config/               # (Opcional) Configurações gerais
├─ data/
│  ├─ manual_processo.pdf  # Base de conhecimento da IA (RAG)
│  └─ credenciais.json     # (Ignorado no Git)
├─ src/
│  ├─ ai_engine.py         # Lógica da IA (Groq + RAG)
│  ├─ database.py          # Conexão com Google Sheets API
│  └─ utils.py             # Funções auxiliares e CSS
├─ assets/                 # Imagens para o README
├─ .streamlit/
│  └─ secrets.toml         # Chaves de API (Ignorado no Git)
├─ app.py                  # Script principal da aplicação
├─ requirements.txt
└─ README.md
```
## ⚙️ Como Executar Localmente

Siga os passos abaixo para rodar a aplicação na sua máquina:

1. **Clone o repositório**
   ```bash
   git clone https://github.com/raissa-sf/smart-quality-injection.git
   cd smart-quality-injection

2. **Crie um ambiente virtual (Opcional, mas recomendado)**
   ```bash
   python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt

4. **Configure as Credenciais (Veja abaixo)**

 ## 🔐 Configuração das Credenciais

Este projeto utiliza chaves de API que não são compartilhadas no repositório. Para executar localmente, siga os passos:

1. Na raiz do projeto, crie uma pasta chamada `.streamlit`.
2. Dentro dela, crie um arquivo chamado `secrets.toml`.
3. Cole o seguinte modelo e preencha com suas próprias credenciais:

```toml
# .streamlit/secrets.toml

# 1. Chave da Groq Cloud (Para a IA)
[GROQ_API]
key = "gsk_SUA_CHAVE_DA_GROQ_AQUI"

# 2. Credenciais do Google Sheets (Para o Banco de Dados)
# Baixe o JSON da sua Service Account no Google Cloud Console e preencha abaixo:
[connections.gsheets]
type = "service_account"
project_id = "seu-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "seu-email@exemplo.com"
client_id = "..."
auth_uri = "[https://accounts.google.com/o/oauth2/auth](https://accounts.google.com/o/oauth2/auth)"
token_uri = "[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)"
auth_provider_x509_cert_url = "[https://www.googleapis.com/oauth2/v1/certs](https://www.googleapis.com/oauth2/v1/certs)"
client_x509_cert_url = "..."
```
5. **Execute a aplicação**
 ```bash
   streamlit run app.py
```
## 📞 Contato
Gostou do projeto ou tem alguma dúvida? Entre em contato!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/raissa-santos-feitosa-73485b1a3/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:raissa.feitosa06@gmail.com)
