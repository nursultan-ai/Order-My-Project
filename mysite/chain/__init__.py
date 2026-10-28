from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from mysite.config import OLLAMA_URL, OLLAMA_MODEL
from mysite.database.schemas import TicketInputSchema, TicketOutputSchema

ChatPromptTemplate.from_messages(
    [
        (
            'system',
            "Ты помогаешь оператору службы доставки разбирать обращения. "
            "Кратко опиши проблему на русском языке в answer. "
            "Не "
        )
    ]
)