from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
import httpx
from langchain.chains import LLMChain
from langchain_openai import OpenAI, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv(override=True)

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a {subject} teacher"),
        ("human", "tell me about {concept}")
    ]
)

chain = LLMChain(llm=llm, prompt=prompt)

res = chain.invoke(
    {
        "subject": "Physics",
        "concept": "newtons first law of motion"
    }
)
print(res)


# OpenAI client with SSL disabled
openai_client = OpenAI(
    http_client=httpx.Client(verify=False)
)

# Use the embeddings sub-client
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    client=openai_client.embeddings,   # ✅ important fix
)

print(embeddings.embed_query("Hello, world!"))
