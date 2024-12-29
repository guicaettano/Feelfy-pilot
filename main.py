import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime

# Configuração da URL do backend
BACKEND_URL = "http://127.0.0.1:8000/analyze/"

# Configurações de tema e estilo
def set_custom_style():
    st.markdown("""
        <style>
        /* Cores personalizadas */
        :root {
            --primary-color: #7B68EE;
            --secondary-color: #4B0082;
            --background-color: #F8F8FF;
            --text-color: #2C2C2C;
        }
        
        /* Estilo do container principal */
        .main {
            padding: 2rem;
            background-color: var(--background-color);
        }
        
        /* Estilo dos cards */
        .stCard {
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            background-color: white;
            margin-bottom: 1.5rem;
        }
        
        /* Estilo dos botões */
        .stButton button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: var(--secondary-color);
            transform: translateY(-2px);
        }
        
        /* Estilo da área de texto */
        .stTextArea textarea {
            border-radius: 10px;
            border: 2px solid #E6E6FA;
            padding: 1rem;
            font-size: 1.1rem;
        }
        
        .stTextArea textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 2px rgba(123, 104, 238, 0.2);
        }
        
        /* Estilo para o upload de arquivo */
        .uploadfile {
            border: 2px dashed var(--primary-color);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Estilo dos títulos */
        h1, h2, h3 {
            font-family: 'Helvetica Neue', sans-serif;
            color: var(--secondary-color);
        }
        
        /* Animações */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
        
        /* Responsividade */
        @media (max-width: 768px) {
            .main {
                padding: 1rem;
            }
            
            h1 {
                font-size: 2em !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def create_sentiment_gauge(score):
    """Cria um gráfico gauge para visualização do sentimento"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [-1, 1], 'tickwidth': 1},
            'bar': {'color': "#7B68EE"},
            'bgcolor': "white",
            'steps': [
                {'range': [-1, -0.3], 'color': "#FFB6C1"},
                {'range': [-0.3, 0.3], 'color': "#E6E6FA"},
                {'range': [0.3, 1], 'color': "#98FB98"}
            ],
        },
        title={'text': "Índice de Sentimento", 'font': {'color': "#4B0082", 'size': 24}}
    ))
    
    fig.update_layout(
        font={'color': "#4B0082", 'family': "Helvetica Neue"},
        paper_bgcolor="white",
        height=300,
        margin=dict(t=100, b=0, l=20, r=20)
    )
    
    return fig

def analyze_text(text):
    """Função para enviar texto para análise na API"""
    try:
        response = requests.post(BACKEND_URL, json={"text": text})
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Erro ao conectar com o servidor: {str(e)}")
        return None

def main():
    # Configurações da página
    st.set_page_config(
        page_title="Feelfy",
        page_icon="💜",
        layout="wide"
    )
    
    # Aplicar estilos personalizados
    set_custom_style()
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 2rem 0;">
                <h1 style="color: #7B68EE; font-size: 3.5em; margin-bottom: 0.5rem;">Feelfy</h1>
                <p style="color: #4B0082; font-size: 1.3em; font-weight: 300;">
                    Transformando textos em insights emocionais
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Container principal
    with st.container():
        # Card de entrada
        st.markdown("""
            <div class="stCard fade-in">
                <h2 style="text-align: center; color: #4B0082; margin-bottom: 1.5rem;">
                    💭 Análise de Sentimento
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Abas para texto e upload
        tab1, tab2 = st.tabs(["📝 Digite o texto", "📁 Upload de arquivo"])
        
        with tab1:
            text_input = st.text_area(
                "",
                placeholder="Digite aqui o texto que você deseja analisar...",
                height=200,
                key="text_input"
            )
            
        with tab2:
            uploaded_file = st.file_uploader(
                "Selecione um arquivo de texto",
                type=["txt"],
                help="Arraste e solte ou clique para selecionar"
            )
            if uploaded_file is not None:
                text_input = uploaded_file.read().decode("utf-8")
                st.success("Arquivo carregado com sucesso!")
                with st.expander("Visualizar conteúdo do arquivo"):
                    st.code(text_input)
        
        # Botão de análise centralizado
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            analyze_button = st.button(" Analisar Sentimento")
        
        if analyze_button:
            if text_input and text_input.strip():
                with st.spinner("Analisando seu texto..."):
                    result = analyze_text(text_input)
                    
                    if result:
                        sentiment_score = result.get("sentiment_score", 0)
                        reasoning = result.get("reasoning", "")
                        
                        # Container para os resultados
                        st.markdown("""
                            <div class="stCard fade-in">
                                <h3 style="text-align: center; color: #4B0082; margin-bottom: 1rem;">
                                    Resultados da Análise
                                </h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Visualização do sentimento
                        st.plotly_chart(
                            create_sentiment_gauge(sentiment_score),
                            use_container_width=True
                        )
                        
                        # Interpretação do resultado
                        if sentiment_score > 0.3:
                            emoji = "🌟"
                            message = "Sentimento muito positivo"
                            color = "#98FB98"
                        elif sentiment_score > 0:
                            emoji = "😊"
                            message = "Sentimento levemente positivo"
                            color = "#E6E6FA"
                        elif sentiment_score > -0.3:
                            emoji = "😐"
                            message = "Sentimento neutro"
                            color = "#E6E6FA"
                        else:
                            emoji = "😔"
                            message = "Sentimento negativo"
                            color = "#FFB6C1"
                        
                        # Exibir resultado e reasoning
                        st.markdown(f"""
                            <div style="text-align: center; padding: 1rem; background-color: {color}; 
                                        border-radius: 10px; margin: 1rem 0;">
                                <h2 style="color: #4B0082;">{emoji} {message}</h2>
                                <p style="color: #4B0082; font-size: 1.1em;">
                                    Score: {sentiment_score:.2f}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if reasoning:
                            st.markdown("""
                                <div class="stCard">
                                    <h4 style="color: #4B0082;">Análise Detalhada</h4>
                                    <p style="color: #2C2C2C;">{}</p>
                                </div>
                            """.format(reasoning), unsafe_allow_html=True)
            else:
                st.warning("⚠️ Por favor, insira um texto ou faça upload de um arquivo para análise.")
    
    # Footer
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0; margin-top: 3rem;">
            <p style="color: #4B0082; font-size: 1em;">
                 Feelfy © {0}
            </p>
        </div>
    """.format(datetime.now().year), unsafe_allow_html=True)

if __name__ == "__main__":
    main()