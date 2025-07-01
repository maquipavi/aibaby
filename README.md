### `README.md`

# AI Baby Generator 👶

![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Inference%20API-yellow)

Uma aplicação web criada com Streamlit que utiliza a API de Inferência da Hugging Face para gerar imagens realistas de como seria um futuro filho(a) em diferentes fases da vida: bebê, criança, adolescente e adulto.

## ✨ Visão Geral


*(Substitua a URL acima por uma captura de tela real do seu aplicativo em execução)*

Este aplicativo oferece uma interface amigável para que os usuários possam visualizar uma progressão de idade gerada por Inteligência Artificial, com base em características como gênero e tom de pele.

### Principais Funcionalidades

-   **Geração por Fases:** Crie imagens para "Bebê", "Criança" e "Adolescente" individualmente.
-   **Progressão Completa:** Gere uma grade 2x2 com todas as fases da vida, de bebê a adulto, com um único clique.
-   **Personalização:** Escolha o gênero (Menino, Menina ou Aleatório) e o tom de pele para guiar a IA.
-   **Entrada Segura de API:** O usuário insere sua própria chave de API da Hugging Face, que não é armazenada ou exposta.
-   **Upload Condicional:** A geração só é habilitada após o upload de duas imagens de referência (simulação visual).
-   **Prompt Engineering Inteligente:** O prompt para a fase "Bebê" foi otimizado para esconder as mãos, evitando artefatos comuns em imagens de IA.
-   **Download da Imagem:** Salve facilmente a imagem gerada (única ou grade) com um clique.

## 🛠️ Como Funciona

A aplicação é construída com **Streamlit**, um framework Python para criar aplicações web de forma rápida. O *backend* de geração de imagens não é local; o aplicativo faz requisições HTTP para a **API de Inferência da Hugging Face**, utilizando o modelo `stabilityai/stable-diffusion-xl-base-1.0`.

> **Nota Importante:** As fotos dos pais que são carregadas **não são enviadas para a IA**. Elas servem apenas como um requisito de interface para habilitar os botões de geração, simulando o comportamento de apps mais complexos. A geração da imagem é baseada **exclusivamente** nos prompts de texto criados a partir das opções selecionadas (gênero, tom de pele, idade).

## 🚀 Instalação e Execução

Siga os passos abaixo para executar o projeto localmente.

### 1. Pré-requisitos

-   [Python 3.8](https://www.python.org/downloads/) ou superior
-   [Git](https://git-scm.com/downloads/)

### 2. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```
*(Substitua pela URL do seu repositório no GitHub)*

### 3. Crie um Ambiente Virtual (Recomendado)

```bash
# Para Windows
python -m venv venv
venv\Scripts\activate

# Para macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Crie o Arquivo `requirements.txt`

Crie um arquivo chamado `requirements.txt` na raiz do projeto com o seguinte conteúdo:

```txt
streamlit
requests
Pillow
```

### 5. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 6. Configuração da API Hugging Face

Para que o aplicativo funcione, você precisa de uma chave de API da Hugging Face e precisa aceitar os termos do modelo Stable Diffusion.

1.  **Obtenha uma Chave de API:**
    -   Crie uma conta (ou faça login) em [Hugging Face](https://huggingface.co/).
    -   Vá para a sua página de tokens: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
    -   Crie um "New token" com a permissão (`Role`) de **`read`**. Copie essa chave.

2.  **Aceite os Termos do Modelo:**
    -   Vá para a página do modelo: [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0).
    -   Leia e aceite os termos para liberar o acesso ao modelo. **Este passo é obrigatório para evitar erros de permissão (Erro 403).**

### 7. Execute a Aplicação

```bash
streamlit run app.py
```

Abra o navegador no endereço local fornecido (geralmente `http://localhost:8501`), cole sua chave de API na barra lateral, carregue as imagens e comece a gerar!

## 📂 Estrutura do Projeto

```
/AI-Baby-Generator
|-- app.py             # O código principal da aplicação Streamlit
|-- requirements.txt   # As dependências do projeto
|-- README.md          # Este arquivo
```

## 👨‍💻 Autor

Desenvolvido com ❤️ por **Engº Paulo Silva**.
