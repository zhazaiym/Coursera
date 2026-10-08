from fastapi import APIRouter
from mysite.database.schema import ChainInputSchema, ChainOutSchema
from mysite.chain.ai_search import search_answer

chain_router = APIRouter(prefix="/chain",tags=["Chain"])


@chain_router.post("/", response_model=ChainOutSchema)
async def ask_question(data: ChainInputSchema):
    answer = search_answer(data.text)

    return {
        "answer": answer
    }