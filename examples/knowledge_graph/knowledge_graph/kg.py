import os
import logging
import sys
from llama_index.core import SimpleDirectoryReader, KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from IPython.display import Markdown, display
from llama_index.core import StorageContext
from llama_index.readers.web import SimpleWebPageReader


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#os.environ["OPENAI_API_KEY"] = "INSERT OPENAI KEY"

# documents = SimpleDirectoryReader(
#     input_dir="datasets"
# ).load_data()

documents = SimpleWebPageReader(html_to_text=True).load_data(
    ["https://pt.wikipedia.org/wiki/Tomb_Raider_(jogo_eletr%C3%B4nico_de_2013)"]
)


llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
Settings.llm = llm
Settings.chunk_size = 2048

graph_store = SimpleGraphStore()
storage_context = StorageContext.from_defaults(graph_store=graph_store)

# NOTE: can take a while!
index = KnowledgeGraphIndex.from_documents(
    documents,
    max_triplets_per_chunk=2,
    storage_context=storage_context,
)


query_engine = index.as_query_engine(
    include_text=False, response_mode="tree_summarize"
)
response = query_engine.query(
    "Me fale sobre o Endurance",
)
print(response)