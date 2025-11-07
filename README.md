# Pesquisa Varinha Mágica - Dashboard de Análise

Este projeto é um **dashboard interativo**, construído em **Python** com a biblioteca **Panel**, para analisar e visualizar os dados da pesquisa:

> “Se você tivesse uma varinha mágica, o que você faria para melhorar o seu ambiente de trabalho?”

O dashboard apresenta os dados em *boxes* categorizados, permitindo a **filtragem por setor** e fornecendo um **resumo visual das respostas mais comuns**.

---

## 📁 Estrutura do Projeto

```
.
├── dashboard.py       # Script principal da aplicação que executa o dashboard
├── dados.csv          # Dados brutos da pesquisa (necessário para executar)
├── codebook.csv       # "Dicionário" que mapeia categorias e descrições
├── requirements.txt   # Dependências Python do projeto
└── README.md          # Este arquivo
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python **3.8+**
- Os arquivos `dados.csv` e `codebook.csv` devem estar na mesma pasta que o `dashboard.py`.

---

### 1️⃣ Instalação

Clone este repositório para a sua máquina local:

```bash
git clone https://github.com/lidianycs/Dashboard-Varinha
cd seu-repositorio
```

Crie e ative um ambiente virtual (recomendado):

```bash
# Windows
python -m venv venv
.venv\Scripts\Activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Instale as dependências Python:

```bash
pip install -r requirements.txt
```
---

### 2️⃣ Executar o Dashboard

Com o ambiente virtual ativo e as dependências instaladas, execute:

```bash
python dashboard.py
```

O script iniciará um **servidor local** e abrirá automaticamente o dashboard no navegador, geralmente em:

👉 http://localhost:5006

Para parar o servidor, volte ao terminal e pressione `CTRL+C`.

---

## 🧾 Formato dos Dados

### `dados.csv`
- **Separador:** ponto e vírgula (`;`)
- **Colunas obrigatórias:**
  - `response_id` → Identificador único da resposta  
  - `setor` → Categoria de setor (usado para filtro)  
  - `label` → Categoria-fator (ex.: `Projeto - Tamanho médio da equipe`)

### `codebook.csv`
- **Separador:** ponto e vírgula (`;`)
- **Colunas obrigatórias:**
  - `category` → Nome da categoria  
  - `factor` → Nome do fator  
  - `description` → Texto a ser exibido no resumo

---

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Contato

Lidiany Cerqueira
lidianycs@gmail.com
