import boto3
from typing import List
from models.models import KnowledgeBaseListModel, KnowledgeBaseModel, KnowledgeBaseRetrievalListModel
from pydantic import RootModel


def get_client(client_type: str) -> boto3.client:
    boto3_session = boto3.session.Session()
    return boto3_session.client(client_type)


def list_kbs() -> List[KnowledgeBaseModel]:
    boto3_session = boto3.session.Session()
    bedrock_agent_client = get_client('bedrock-agent')
    kb_list = bedrock_agent_client.list_knowledge_bases()
    kb_list_model: KnowledgeBaseListModel = []
    if 'knowledgeBaseSummaries' in kb_list:
        kb_list_model = KnowledgeBaseListModel.parse_obj(kb_list['knowledgeBaseSummaries'])

    for kb in kb_list_model.root:
        print(kb)

    return kb_list_model.root


def query_kb(kb_id: str, query: str):
    if not kb_id:
        raise AttributeError('kb_id is required')
    if not query:
        raise AttributeError('query is required')

    bedrock_agent_client = get_client('bedrock-agent-runtime')
    bedrock_agent_response = bedrock_agent_client.retrieve(
        knowledgeBaseId=kb_id,
        #nextToken='string',
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': 5,
                'overrideSearchType': 'HYBRID'
            }
        },
        retrievalQuery={
            'text': query
        }
    )

    retrieval_response_list: KnowledgeBaseRetrievalListModel = []

    if 'retrievalResults' in bedrock_agent_response:
        retrieval_response_list = KnowledgeBaseRetrievalListModel.parse_obj(bedrock_agent_response['retrievalResults'])

    for item in retrieval_response_list.root:
        print(item)

