import asyncio
from fastapi import APIRouter, HTTPException
from urllib3.util.util import reraise
from mysite.chain.ticket_chain import ticket_chain
from mysite.database.schemas import TicketInputSchema, TicketOutputSchema, AnswerInputSchema,AnswerOutputSchema,AIOrderOutputSchema
from langchain_core.exceptions import OutputParserException
from mysite.chain.answer_chain import answer_chain
from mysite.chain.order_chain import order_chain

ai_router = APIRouter(prefix='/ai', tags=['AI Assistant'])


@ai_router.post('/analyze', response_model=TicketOutputSchema)
async def analyze_ticket(ticket: TicketInputSchema):
    text = ticket.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилген')

    try:
        result = await asyncio.wait_for(
            ticket_chain.ainvoke({"text": text}), timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модель тапшырманы аткарганы текшерген жок')

    except OutputParserException:
        raise HTTPException(status_code=500, detail='Моделдин жообу схемага туура келбейт')

    return result

@ai_router.post('/answer', response_model=AnswerOutputSchema)
async def answer_list(answer: AnswerInputSchema):
    text = (answer.text or "").strip()
    facts = (answer.facts or "").strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилген')

    try:
        result = await asyncio.wait_for(
            answer_chain.ainvoke({
                "text": text,
                "facts": facts if facts else "Нет дополнительных сведений от оператора"
            }),
            timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модель тапшырманы аткарганга жетишкен жок')
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Оборачиваем строку в словарь (проверь, как называется поле в твоей AnswerOutputSchema: answer или text)
    return {"answer": result.strip()}



@ai_router.post('/order', response_model=AIOrderOutputSchema)
async def create_ai_order(order: TicketInputSchema):  # Можно использовать TicketInputSchema или OrderInputSchema, так как там только поле text
    text = (order.text or "").strip()

    if not text:
        raise HTTPException(status_code=422, detail='Маалымат туура эмес форматта берилген')

    try:
        result = await asyncio.wait_for(
            order_chain.ainvoke({"text": text}), timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=500, detail='Модель тапшырманы аткарганга жетишкен жок')
    except OutputParserException:
        raise HTTPException(status_code=500, detail='Моделдин жообу схемага туура келбейт')

    return result