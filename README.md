# 🏭 Sistema Inteligente de Controle de Qualidade - Injeção Plástica

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
📁 qualidade-injecao/
│
├── 📁 src/
│   ├── ai_engine.py       # Lógica da IA (RAG e Relatórios)
│   ├── database.py        # Conexão e queries ao banco de dados
│   └── utils.py           # Funções auxiliares 
│
├── 📁 data/
│   ├── manual_processo.pdf  # Base de conhecimento da IA
│
├── 📁 assets/            
├── app.py                 # Aplicação Principal
├── requirements.txt       # Dependências
└── README.md              # Documentação
