import streamlit as st
import requests
from PIL import Image
import io
import random

# --- Configuração da Página e Constantes ---
st.set_page_config(
    page_title="AI Baby Generator",
    page_icon="👶",
    layout="wide"
)

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if 'last_image_info' not in st.session_state:
    st.session_state.last_image_info = None

# URL da API do Hugging Face para o modelo Stable Diffusion XL
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Prompts base para garantir a qualidade e o estilo da imagem
BASE_PROMPT_TEMPLATE = "ultra realistic 8k photo, {age_desc}, {skin_tone}, cinematic lighting, professional photography, sharp focus, incredibly detailed"
NEGATIVE_PROMPT = "hands, fingers, deformed hands, mutated hands, arms, blurry, deformed, ugly, disfigured, cartoon, anime, 3d render, painting, text, watermark, signature, extra limbs, missing limbs, body"

# Descrições específicas para cada fase da vida
AGE_PROMPTS = {
    # --- ALTERAÇÃO AQUI ---
    # Adicionado "swaddled in a soft blanket with hands tucked under it" para esconder as mãos
    'Bebê': 'extreme close-up face portrait of a cute newborn baby, 1 month old, sleeping peacefully, swaddled in a soft blanket with hands tucked under it, perfect smooth skin',
    'Criança': 'cute happy child, 6 years old, smiling, headshot portrait',
    'Adolescente': 'portrait of a teenager, 16 years old, natural look, high school photo style',
    'Adulto': 'professional headshot portrait of a young adult, 28 years old, confident expression'
}


# --- Funções ---

def query_api(payload, headers):
    """Envia um prompt para a API do Hugging Face e retorna o conteúdo da imagem."""
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        try:
            error_message = response.json().get('error', 'Erro desconhecido.')
            st.error(f"Erro na API: {error_message} (Status: {response.status_code})")
            if "must be provided" in error_message:
                st.error("Verifique se sua Chave de API está correta e foi inserida na barra lateral.")
            if response.status_code == 403:
                 st.error("Erro 403: Verifique se você aceitou os termos de uso do modelo no site da Hugging Face.")
        except:
            st.error(f"Erro na API (Status: {response.status_code}): {response.text}")
        return None

def create_image_grid(images):
    """Cria uma imagem única a partir de 4 imagens em uma grade 2x2."""
    image_size = 512
    grid_image = Image.new('RGB', (image_size * 2, image_size * 2))
    
    grid_image.paste(images[0].resize((image_size, image_size)), (0, 0))
    grid_image.paste(images[1].resize((image_size, image_size)), (image_size, 0))
    grid_image.paste(images[2].resize((image_size, image_size)), (0, image_size))
    grid_image.paste(images[3].resize((image_size, image_size)), (image_size, image_size))
    
    return grid_image

# --- Interface do Usuário (UI) ---

st.title("👶 AI Baby Generator")
st.markdown("Crie imagens realistas do seu futuro filho(a) em diferentes fases da vida. Siga os passos abaixo.")

# --- Barra lateral com as opções de personalização ---
with st.sidebar:
    st.header("🔑 Configuração da API")
    api_key = st.text_input("Chave da API - AI Baby", type="password", help="Sua chave de API é necessária para gerar as imagens.")
    st.markdown("[Obtenha sua chave de API aqui](https://ai-baby-generator.streamlit.app/)")
    
    if api_key:
        HEADERS = {"Authorization": f"Bearer {api_key}"}
    else:
        HEADERS = None

    st.markdown("---")
    
    st.header("🎨 Personalize a Geração")
    
    gender_input = st.radio(
        "Gênero:", 
        ('Menino', 'Menina', 'Aleatório'), 
        horizontal=True, 
        index=2
    )
    
    skin_tone_options = {
        'Automático': 'beautiful diverse heritage',
        'Muito Claro': 'very light, pale caucasian skin',
        'Claro': 'light, fair caucasian skin',
        'Moreno Claro': 'light brown, mediterranean skin',
        'Moreno Escuro': 'dark brown, south asian skin',
        'Negro': 'deep dark, african skin'
    }
    skin_tone_selection = st.selectbox("Tom de Pele:", options=list(skin_tone_options.keys()))
    
    st.markdown("---")
    
    st.subheader("🖼️ Imagem Única")
    age_selection = st.selectbox("Selecione a Idade:", options=['Bebê', 'Criança', 'Adolescente'])
    
    st.info("Clique nos botões na página principal para gerar a imagem.")
    
    st.markdown("---")
    st.sidebar.info("Este aplicativo usa IA para gerar imagens. Os resultados são artísticos e não uma previsão científica.")


# --- PASSO 1: UPLOAD DE FOTOS (SIMULADO) ---
st.subheader("1. Carregue as Fotos dos Pais")
st.info("ℹ️ **Atenção:** O upload das fotos é necessário para habilitar a geração. **O modelo de IA usa as fotos para gerar o resultado.**")

col1, col2 = st.columns(2)
with col1:
    uploaded_file_1 = st.file_uploader("Pai 1 / Mãe 1", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
    if uploaded_file_1:
        st.image(uploaded_file_1, caption='Pai 1 / Mãe 1', use_column_width=True)

with col2:
    uploaded_file_2 = st.file_uploader("Pai 2 / Mãe 2", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
    if uploaded_file_2:
        st.image(uploaded_file_2, caption='Pai 2 / Mãe 2', use_column_width=True)

st.markdown("---")

api_key_provided = HEADERS is not None
both_images_uploaded = uploaded_file_1 is not None and uploaded_file_2 is not None
ready_to_generate = api_key_provided and both_images_uploaded

# --- PASSO 2: GERAÇÃO ---
st.subheader("2. Gere a Imagem")

if not api_key_provided:
    st.warning("⚠️ Por favor, insira sua chave de API na barra lateral para continuar.")
if not both_images_uploaded:
    st.warning("⚠️ Por favor, carregue as fotos do 'Pai 1 / Mãe 1' e 'Pai 2 / Mãe 2' para habilitar os botões de geração.")

gen_col1, gen_col2 = st.columns(2)
result_placeholder = st.empty()

# Lógica dos botões
with gen_col1:
    if st.button("Gerar Imagem Única", use_container_width=True, disabled=not ready_to_generate):
        with st.spinner("Gerando sua imagem... ⏳"):
            gender = gender_input if gender_input != 'Aleatório' else random.choice(['Menino', 'Menina'])
            skin_tone = skin_tone_options[skin_tone_selection]
            
            age_desc = AGE_PROMPTS[age_selection].replace('newborn baby', f'newborn baby {gender.lower()}').replace('child', f'{gender.lower()} child').replace('teenager', f'{gender.lower()} teenager')
            final_prompt = BASE_PROMPT_TEMPLATE.format(age_desc=age_desc, skin_tone=skin_tone)
            
            payload = {"inputs": final_prompt, "parameters": {"negative_prompt": NEGATIVE_PROMPT}}
            image_bytes = query_api(payload, HEADERS)
            
            if image_bytes:
                image = Image.open(io.BytesIO(image_bytes))
                caption = f"Resultado: {gender} - {age_selection}"
                result_placeholder.image(image, caption=caption, use_column_width=True)
                
                file_name = f"resultado_{gender.lower()}_{age_selection.lower().replace('ê', 'e')}.png"
                st.session_state.last_image_info = {"bytes": image_bytes, "name": file_name}


with gen_col2:
    if st.button("Gerar Todas as Fases", use_container_width=True, type="primary", disabled=not ready_to_generate):
        with st.spinner("Gerando a progressão de idade... Isso pode levar um minuto!"):
            gender = gender_input if gender_input != 'Aleatório' else random.choice(['Menino', 'Menina'])
            skin_tone = skin_tone_options[skin_tone_selection]
            phases_to_generate = ['Bebê', 'Criança', 'Adolescente', 'Adulto']
            generated_images = []

            progress_bar = st.progress(0, text="Iniciando geração...")
            
            for i, phase in enumerate(phases_to_generate):
                progress_bar.progress((i) / len(phases_to_generate), text=f"Gerando fase: {phase}...")
                
                age_desc = AGE_PROMPTS[phase]
                if gender.lower() == 'menino':
                    age_desc = age_desc.replace('child', 'boy').replace('teenager', 'male teenager').replace('adult', 'man')
                else:
                    age_desc = age_desc.replace('child', 'girl').replace('teenager', 'female teenager').replace('adult', 'woman')
                age_desc = age_desc.replace('newborn baby', f'newborn baby {gender.lower()}')
                
                final_prompt = BASE_PROMPT_TEMPLATE.format(age_desc=age_desc, skin_tone=skin_tone)
                payload = {"inputs": final_prompt, "parameters": {"negative_prompt": NEGATIVE_PROMPT}}
                image_bytes = query_api(payload, HEADERS)
                
                if image_bytes:
                    image = Image.open(io.BytesIO(image_bytes))
                    generated_images.append(image)
                else:
                    st.error(f"Falha ao gerar a fase '{phase}'. Abortando.")
                    st.session_state.last_image_info = None
                    progress_bar.empty()
                    break
            
            if len(generated_images) == 4:
                progress_bar.progress(1.0, text="Montando a grade final...")
                grid_image = create_image_grid(generated_images)
                caption = f"Progressão de Idade - {gender}"
                result_placeholder.image(grid_image, caption=caption, use_column_width=True)
                progress_bar.empty()

                buf = io.BytesIO()
                grid_image.save(buf, format="PNG")
                grid_image_bytes = buf.getvalue()
                file_name = f"progressao_idade_{gender.lower()}.png"
                st.session_state.last_image_info = {"bytes": grid_image_bytes, "name": file_name}

st.markdown("---")

# --- PASSO 3 - SALVAR IMAGEM ---
if st.session_state.last_image_info:
    st.subheader("3. Salve sua Criação")
    image_info = st.session_state.last_image_info
    st.download_button(
        label="📥 Salvar Imagem",
        data=image_info["bytes"],
        file_name=image_info["name"],
        mime="image/png",
        use_container_width=True
    )

# --- RODAPÉ PERSONALIZADO ---
st.divider()
st.markdown("<p style='text-align: center;'>Desenvolvido com ❤️ por Engº Paulo Silva</p>", unsafe_allow_html=True)
