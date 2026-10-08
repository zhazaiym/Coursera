from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore

BASE_DIR = Path(__file__).resolve().parent
loaders = TextLoader(str(BASE_DIR / 'nn'), encoding='utf-8')
document = loaders.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=40
)

chunks = text_splitter.split_documents(document)

embeddings = GoogleGenerativeAIEmbeddings(
    model='gemini-embedding-001'
)

vectors_store = InMemoryVectorStore.from_documents(chunks, embeddings)

prompt = ChatPromptTemplate(
    [
        (
            'system',
            "Ты онлайн менеджер сайта Coursera. "
            "Твоя задача помогать пользователям находить подходящие курсы. "
            "При ответе сначала обязательно посмотри Базу Знаний: "
            "База знаний: {nn}. "
            "Отвечай только на основе информации из Базы Знаний. "
            "Не придумывай курсы, цены, продолжительность, уровни "
            "и другую информацию которой нет в Базе Знаний. "
            "Если пользователь указал название курса, уровень, цену "
            "или продолжительность, учитывай эти условия. "
            "Каждый курс перечисляй только один раз. "
            "Не повторяй один и тот же курс. "
            "Если подходящего курса нет в Базе Знаний, напиши "
            "что подходящий курс не найден. "
            "Если в Базе Знаний нет ответа на вопрос, напиши "
            "что не знаешь. "
            "Отвечай коротко, понятно и вежливо. "
            "Отвечай на языке пользователя."
        ),
        (
            'human',
            '{content}'
        )
    ]
)

model = ChatGoogleGenerativeAI(
    model='gemini-3.8-flash'
)

chain = prompt | model | StrOutputParser()


def search_answer(question: str):
    new_document = vectors_store.similarity_search(question, k=1)
    final_answer = chain.invoke({
        'content': question,
        'nn': new_document
    })
    final_answer = final_answer.replace('\n', ' ')
    final_answer = final_answer.replace('*', '')
    final_answer = ' '.join(final_answer.split())

    return final_answer