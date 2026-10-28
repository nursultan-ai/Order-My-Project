from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from mysite.config import OLLAMA_URL, OLLAMA_MODEL
from mysite.database.schemas import AIOrderOutputSchema

order_prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            "Ты помогаешь оформлять заказы в интернет-магазине. "
            "Извлеки данные о заказе из текста клиента на русском языке: "
            "- title: краткое название товара (например, 'Свитер'); "
            "- category: подходящая категория (например, 'Одежда', 'Обуви и аксессуары', 'Электроника'); "
            "- price: цена за единицу товара (если не указана в тексте, укажи 9999); "
            "- quantity: количество товара (по умолчанию 1, если не указано иное); "
            "- total_price: общая сумма (price * quantity); "
            "- description: краткое описание товара с деталями из текста (например, размер, цвет)."
        ),
        (
            'human',
            '{text}'
        ),
    ]
)

order_model = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0,
    num_predict=250
)

structured_order_model = order_model.with_structured_output(
    AIOrderOutputSchema,
    method='json_schema'
)

order_chain = order_prompt | structured_order_model