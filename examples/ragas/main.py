from langchain_community.document_loaders import DirectoryLoader,WebBaseLoader
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import logging

logging.basicConfig(level=logging.DEBUG)

directory_loader = DirectoryLoader("documents")
#web_loader = WebBaseLoader(web_path="https://www.itau.com.br/download-file/v2/d/42787847-4cf6-4461-94a5-40ed237dca33/ce5914f9-490e-ff22-bb08-646c7c9fd86c?origin=1")

documents = directory_loader.load()


for document in documents:
    document.metadata['filename'] = document.metadata['source']


# generator with openai models
generator_llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
critic_llm = ChatOpenAI(model="gpt-4o")
embeddings = OpenAIEmbeddings()

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings
)

# generate testset
testset = generator.generate_with_langchain_docs(documents, test_size=10, distributions={simple: 0.5, reasoning: 0.25, multi_context: 0.25})

testset.to_pandas()