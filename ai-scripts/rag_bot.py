import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = "knowledge.txt"
if not os.path.exists(file_path):
    print(f"Ошибка: Файл {file_path} не найден!")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
chunks = text_splitter.create_documents([text])
print(f"Текст разбит на {len(chunks)} частей.")

embeddings = OllamaEmbeddings(model="llama3.2:3b")
vector_store = Chroma.from_documents(chunks, embeddings, collection_name="my_knowledge")

retriever = vector_store.as_retriever(search_kwargs={"k": 2})
llm = ChatOllama(model="llama3.2:3b", temperature=0.1)

prompt_template = '''
Ответь на вопрос, используя ТОЛЬКО контекст ниже.
Если в контексте нет ответа, скажи: "В предоставленных данных нет такой информации".

Контекст:
{context}

Вопрос: {question}
Ответ:'''

prompt = ChatPromptTemplate.from_template(prompt_template)

question = "Где работал Алексей Петров?"
print(f"\nВопрос: {question}")

docs = retriever.invoke(question)
context = "\n\n".join([doc.page_content for doc in docs])

chain = prompt | llm
response = chain.invoke({"context": context, "question": question})
print(f"Ответ: {response.content}")
