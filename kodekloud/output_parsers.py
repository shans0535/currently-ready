from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import OpenAI
from typing import List
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.output_parsers import JsonOutputParser
import json
import os
# ------- CSV parser imports

from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.output_parsers.list import ListOutputParser
from langchain.output_parsers import CommaSeparatedListOutputParser
import os

# --------- json parser imports
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.output_parsers.list import ListOutputParser
from langchain_core.output_parsers import JsonOutputParser
import json
import os
from dotenv import load_dotenv
load_dotenv()
llm = OpenAI()

prompt = PromptTemplate(
    template="List 3 countries in {continent} and their capitals",
    input_variables=["continent"]
)

print(llm.invoke(input=prompt.format(continent="Asia")))

# ----------------- CSV parser-------------------

llm = OpenAI()
prompt = PromptTemplate(
    template="List 3 {things}",
    input_variables=["things"])
print(llm.invoke(input=prompt.format(
    things="countries that play cricket in world cup")))

output_parser = CommaSeparatedListOutputParser()
format_instructions = output_parser.get_format_instructions()
print(format_instructions)


# --------------- JSON parser -------------------
llm = OpenAI()
prompt = PromptTemplate(
    template="List 3 countries in {continent} and their capitals",
    input_variables=["continent"])

print(llm.invoke(input=prompt.format(continent="Asia")))
output_parser = JsonOutputParser()
format_instructions = output_parser.get_format_instructions()
print(format_instructions)

prompt = PromptTemplate(
    template="List 3 countries in {continent} and their capitals\n{format_instructions}",
    input_variables=["continent"],
    partial_variables={"format_instructions": format_instructions})
final_prompt = prompt.format(continent="North America")
print(final_prompt)
output = llm.invoke(input=final_prompt)
print(output)
countries = output_parser.parse(output)
print(json.dumps(countries))
type(countries)

# ---------------- Pydantic parser ----------------

model = OpenAI()


class Ticket(BaseModel):
    date: str = Field(description="show date")
    time: str = Field()
    theater: str = Field()
    count: int = Field()
    movie: str = Field()


parser = PydanticOutputParser(pydantic_object=Ticket)

ticket_template = '''
Book us a moview ticket for two this Friday at 6:00 PM.
Choose any theater, it doesn't matter. SEnd the confirmation by emial.
Our preferred movie is : {query}
Format instructions:
{format_instructions}
'''

prompt = PromptTemplate(
    template=ticket_template,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

input = prompt.format_prompt(query="Interstellar")
print(input.to_string)

output = model.invoke(input.to_string())

output

reservation = parser.parse(output)
