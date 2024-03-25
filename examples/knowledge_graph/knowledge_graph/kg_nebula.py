import os
import logging
import sys
from typing import List

from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.indices import KnowledgeGraphIndex
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.llms.openai import OpenAI
from llama_index.core.settings import Settings
from llama_index.core.storage import StorageContext
from llama_index.core.schema import Document
from llama_index.core.schema import Node, TextNode
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.web import SimpleWebPageReader
from llama_index.graph_stores.nebula import NebulaGraphStore
from llama_index.core.indices.knowledge_graph.retrievers import KGRetrieverMode
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.core.query_engine import KnowledgeGraphQueryEngine, RetrieverQueryEngine

from llama_index.core.query_engine.retriever_query_engine import (RetrieverQueryEngine)
from llama_index.core.indices.knowledge_graph.retrievers import (KGRetrieverMode, KGTableRetriever,
                                                                 KnowledgeGraphRAGRetriever)

# from llama_index.legacy import SimpleDirectoryReader, KnowledgeGraphIndex
# from llama_index.legacy.graph_stores import SimpleGraphStore
# from llama_index.legacy.llms.openai import OpenAI
# from llama_index.legacy import StorageContext, Document
# from llama_index.legacy.schema import Node, TextNode
# from llama_index.legacy.node_parser import SentenceSplitter
# from llama_index.legacy.readers.web import SimpleWebPageReader
# from llama_index.graph_stores.nebula import NebulaGraphStore
# from llama_index.legacy.indices.knowledge_graph.retrievers import KGRetrieverMode
# from llama_index.legacy.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
# from llama_index.legacy.query_engine import KnowledgeGraphQueryEngine
DEFAULT_URL = "https://pt.wikipedia.org/wiki/Tomb_Raider_(jogo_eletr%C3%B4nico_de_2013)"

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# os.environ["OPENAI_API_KEY"] = "INSERT OPENAI KEY"

# documents = SimpleDirectoryReader(
#     input_dir="datasets"
# ).load_data()


def load_data_from_file(path: str = "Documents") -> List[Document]:
    return SimpleDirectoryReader(path, encoding="utf-8", recursive=True).load_data()


def load_data_from_site(url: str = DEFAULT_URL) -> List[Document]:
    documents = SimpleWebPageReader(html_to_text=True).load_data([url])
    return documents


def split_into_chunks(documents: List[Document]) -> List[TextNode]:
    if not all(isinstance(doc, Document) for doc in documents):
        raise ValueError("documents must be a list of Document")

    nodes = SentenceSplitter().get_nodes_from_documents(documents)
    return nodes


def get_store_context() -> StorageContext:
    os.environ["NEBULA_USER"] = "root"
    os.environ["NEBULA_PASSWORD"] = "nebula"  # replace with your password, by default it is "nebula"
    os.environ["NEBULA_ADDRESS"] = "127.0.0.1:9669"  # assumed we have NebulaGraph 3.5.0 or newer installed locally

    edge_types, rel_prop_names = ["relationship"], ["relationship"]
    tags = ["entity"]

    graph_store = NebulaGraphStore(space_name="tomb_raider",
                                   edge_types=edge_types,
                                   rel_prop_names=rel_prop_names,
                                   tags=tags)

    return StorageContext.from_defaults(graph_store=graph_store)


def build_index(nodes: List[TextNode]) -> KnowledgeGraphIndex:
    # testando forma de construir o index a partir de nodes que são chunks já divididos
    storage_context = get_store_context()

    index = KnowledgeGraphIndex(
        nodes=nodes,
        storage_context=storage_context,
        # callback_manager=callback_manager,
        # show_progress=show_progress,
        # transformations=transformations,
        # service_context=service_context,
        max_triplets_per_chunk=2,
        include_embeddings=True
    )

    # # NOTE: can take a while!
    # #forma tradicional de contruir o index a partir de documentos que ainda serão divididos em nodes
    # index = KnowledgeGraphIndex.from_documents(
    #     documents=nodes,
    #     max_triplets_per_chunk=2,
    #     storage_context=storage_context,
    #     include_embeddings=True,
    #     #transformations=[SentenceSplitter, ]
    # )

    return index


def get_query_engine() -> RetrieverQueryEngine:
    # verificar se essa estratégia de só criar o query engine com o indice já criado funciona
    # referencia = https://github.com/run-llama/llama_index/issues/11034

    # query_engine = KnowledgeGraphQueryEngine(
    #     storage_context=get_store_context(),
    #     llm=OpenAI(temperature=0, model="gpt-3.5-turbo"),
    #     verbose=True,
    #     include_text=False,
    #     response_mode="tree_summarize",
    # )

    graph_rag_retriever = KnowledgeGraphRAGRetriever(
        storage_context=get_store_context(),
        verbose=True,
        retriever_mode="keyword"
    )

    query_engine = RetrieverQueryEngine.from_args(
        graph_rag_retriever,
    )

    return query_engine


llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
# Settings.llm = llm
# Settings.embed_model = OpenAIEmbedding()
# Settings.chunk_size = 2048

# documents = load_data_from_site()  # para carregar do exemplo do Harry Porter localmente use load_data_from_file()
# nodes = split_into_chunks(documents)
# index = build_index(nodes)  # se o banco já estiver populado não é necessário rodar esta linha.

# DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE = PromptTemplate(
#     DEFAULT_QUERY_KEYWORD_EXTRACT_TEMPLATE_TMPL,
#     prompt_type=PromptType.QUERY_KEYWORD_EXTRACT,
# )
logging.debug("Creating query engine")
# query_engine_1 = index.as_query_engine(include_text=False, response_mode="tree_summarize", verbose=True)
# logging.debug("Querying")
# response_1 = query_engine_1.query("Me fale sobre Lara Croft, sempre responda em português brasileiro")
# print(response_1)
logging.debug("Creating query engine 2")
query_engine_2 = get_query_engine()
logging.debug("Querying 2")
response_2 = query_engine_2.query("Me fale sobre Lara Croft, sempre responda em português brasileiro")
print(response_2)
