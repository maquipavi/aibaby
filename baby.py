import streamlit as st
import requests
from PIL import Image
import io

# --- Configuração da Página e Constantes ---
st.set_page_config(
    page_title="AI Baby Generator",
    page_icon="👶",
    layout="centered"
)

# URL da API do Hugging Face para o modelo Stable Diffusion XL
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Prompts base para garantir a qualidade e o estilo da imagem
BASE_PROMPT_TEMPLATE = "ultra realistic 8k photo, {age_desc}, {skin_tone}, cinematic lighting, professional photography, sharp focus, incredibly detailed"
NEGATIVE_PROMPT = "hands, fingers, deformed hands, mutated hands, arms, blurry, deformed, ugly, disfigured, cartoon, anime, 3d render, painting, text, watermark, signature, extra limbs, missing limbs, body"

# Descrições específicas para cada fase da vida
AGE_PROMPTS = {
    'Bebê': 'extreme close-up face portrait of a cute newborn baby, 1 month old, sleeping peacefully, perfect smooth skin',
    'Criança': 'cute happy child, 6 years old, smiling, headshot portrait',
    'Adolescente': 'portrait of a teenager, 16 years old, natural look, high school photo style',
    'Adulto': 'professional headshot portrait of a young adult, 28 years old, confident expression'
}

# --- Funções ---

# Função para chamar a API de IA e gerar a imagem
def query_api(payload):
    """Envia um prompt para a API do Hugging Face e retorna o conteúdo da imagem."""
    # Recupera o token da API dos segredos do Streamlit
    hf_token = st.secrets.get("HUGGING_FACE_TOKEN")
    if not hf_token:
        st.error("Token da API do Hugging Face não encontrado! Por favor, configure seus segredos.")
        return None
        
    headers = {"Authorization": f"Bearer {hf_token}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.content
    else:
        # Tenta decodificar a mensagem de erro da API
        try:
            error_message = response.json().get('error', 'Erro desconhecido.')
            st.error(f"Erro na API: {error_message} (Status: {response.status_code})")
        except:
            st.error(f"Erro na API (Status: {response.status_code}): {response.text}")
        return None

# Função para montar a grade de imagens 2x2
def create_image_grid(images):
    """Cria uma imagem única a partir de 4 imagens em uma grade 2x2."""
    image_size = 512
    grid_image = Image.new('RGB', (image_size * 2, image_size * 2))
    
    # Redimensiona e cola as imagens
    grid_image.paste(images[0].resize((image_size, image_size)), (0, 0))
    grid_image.paste(images[1].resize((image_size, image_size)), (image_size, 0))
    grid_image.paste(images[2].resize((image_size, image_size)), (0, image_size))
    grid_image.paste(images[3].resize((image_size, image_size)), (image_size, image_size))
    
    return grid_image

# --- Interface do Usuário (UI) ---

st.title("👶 AI Baby Generator")
st.markdown("Crie imagens realistas do seu futuro filho(a) em diferentes fases da vida. Personalize as opções na barra lateral e clique para gerar!")

# Barra lateral com as opções
with st.sidebar:
    st.header("🎨 Personalize a Geração")
    
    # Opções compartilhadas
    gender_input = st.radio("Gênero:", ('Menino', 'Menina', 'Aleatório'), horizontal=True)
    
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
    
    # Geração de Imagem Única
    st.subheader("🖼️ Imagem Única")
    age_selection = st.selectbox("Selecione a Idade:", options=['Bebê', 'Criança', 'Adolescente'])
    if st.button("Gerar Imagem Única"):
        with st.spinner("Gerando sua imagem... ⏳"):
            gender = gender_input if gender_input != 'Aleatório' else random.choice(['Menino', 'Menina'])
            skin_tone = skin_tone_options[skin_tone_selection]
            
            age_desc = AGE_PROMPTS[age_selection].replace('newborn baby', f'newborn baby {gender.lower()}').replace('child', f'{gender.lower()} child').replace('teenager', f'{gender.lower()} teenager')
            final_prompt = BASE_PROMPT_TEMPLATE.format(age_desc=age_desc, skin_tone=skin_tone)
            
            payload = {"inputs": final_prompt, "parameters": {"negative_prompt": NEGATIVE_PROMPT}}
            image_bytes = query_api(payload)
            
            if image_bytes:
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption=f"Resultado: {gender} - {age_selection}", use_column_width=True)

    st.markdown("---")
    
    # Geração de Todas as Fases
    st.subheader("👨‍👩‍👧‍👦 Todas as Fases")
    if st.button("Gerar Todas as Fases"):
        with st.spinner("Gerando a progressão de idade... Isso pode levar um minuto!"):
            gender = gender_input if gender_input != 'Aleatório' else random.choice(['Menino', 'Menina'])
            skin_tone = skin_tone_options[skin_tone_selection]
            phases_to_generate = ['Bebê', 'Criança', 'Adolescente', 'Adulto']
            generated_images = []

            progress_bar = st.progress(0)
            
            for i, phase in enumerate(phases_to_generate):
                st.text(f"Gerando fase: {phase}...")
                
                age_desc = AGE_PROMPTS[phase]
                if gender.lower() == 'menino':
                    age_desc = age_desc.replace('child', 'boy').replace('teenager', 'male teenager').replace('adult', 'man')
                else:
                    age_desc = age_desc.replace('child', 'girl').replace('teenager', 'female teenager').replace('adult', 'woman')
                age_desc = age_desc.replace('newborn baby', f'newborn baby {gender.lower()}')
                
                final_prompt = BASE_PROMPT_TEMPLATE.format(age_desc=age_desc, skin_tone=skin_tone)
                payload = {"inputs": final_prompt, "parameters": {"negative_prompt": NEGATIVE_PROMPT}}
                image_bytes = query_api(payload)
                
                if image_bytes:
                    image = Image.open(io.BytesIO(image_bytes))
                    generated_images.append(image)
                else:
                    st.error(f"Falha ao gerar a fase '{phase}'. Abortando.")
                    break # Para a geração se uma fase falhar
                
                progress_bar.progress((i + 1) / len(phases_to_generate))

            if len(generated_images) == 4:
                grid_image = create_image_grid(generated_images)
                st.image(grid_image, caption=f"Progressão de Idade - {gender}", use_column_width=True)


st.sidebar.markdown("---")
st.sidebar.info("Este aplicativo usa IA para gerar imagens. Os resultados são artísticos e não uma previsão científica.")