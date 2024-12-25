from fastapi import FastAPI, Form
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.chains import create_tagging_chain
from langchain_core.messages import SystemMessage, HumanMessage

# Carregar variáveis de ambiente
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

# Configurar Groq API
chat = ChatGroq(api_key=groq_api_key)

# Esquema para análise de sentimentos
schema = {
    "properties": {
        "sentiment": {
            "type": "string",
            "enum": ["negative", "neutral", "positive"],
            "description": "Sentimento do texto"
        },
        "reasoning": {
            "type": "string",
            "description": "Explique de forma concisa o porquê usar a ferramenta"
        }
    },
    "required": ["sentiment", "reasoning"]
}


# Configurar FastAPI
app = FastAPI()

# Modelo de entrada
class TextAnalysisRequest(BaseModel):
    text: str

@app.post("/analyze/")
async def analyze_sentiment(request: TextAnalysisRequest):
    """
    Endpoint para analisar sentimentos usando LangChain e Groq API.
    """
    try:
        # Configurar mensagens para análise
        messages = [
            SystemMessage(content="Escreva seu texto aqui para a análise"),
            HumanMessage(content=request.text)
        ]

        # Criar cadeia de análise
        chain = create_tagging_chain(schema=schema, llm=chat)

        # Executar análise
        result = chain.run(messages)

        # Retornar o resultado
        return {"analysis": result}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "Bem-vindo ao backend do Feelfy!"}
