from pydantic import BaseModel, RootModel
from datetime import datetime
from typing import List, Any, Dict


class KnowledgeBaseModel(BaseModel):
    description: str
    knowledgeBaseId: str
    name: str
    status: str
    updatedAt: datetime


class KnowledgeBaseListModel(RootModel[List[KnowledgeBaseModel]]):
    pass


class S3Location(BaseModel):
    uri: str
    type: str


class Content(BaseModel):
    text: str


class KnowledgeBaseRetrievalModel(BaseModel):
    content: Content
    location: Dict[str, Any]
    metadata: Dict[str, Any]
    score: float


class KnowledgeBaseRetrievalListModel(RootModel[List[KnowledgeBaseRetrievalModel]]):
    pass
