from contextlib import asynccontextmanager
from http.client import responses
from operator import index

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database.mongodb import CopusMongoDB
from app.services.document_processor import DocumentProcessor
from app.services.llm_service import LLMService
from typing import List, Dict

import os

os.environ['OPENAI_API_KEY'] = '请输入key'


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    CopusMongoDB.connect_to_mongodb()
    if document_processor.getDataLength() == 0:
        documents = CopusMongoDB.get_documents()
        document_processor.process_documents(documents)
    yield
    # Shutdown
    CopusMongoDB.close_mongodb_connection()

app = FastAPI(lifespan=lifespan)
document_processor = DocumentProcessor()
llm_service = LLMService()

class DocumentQuery(BaseModel):
    document: str

class RecommendationResponse(BaseModel):
    uuid: str
    recommend_reason: str

@app.post("/recommend", response_model=List[RecommendationResponse])
async def get_recommendations(query: DocumentQuery):
    try:
        # Generate summary for the query document
        summary = await llm_service.generate_summary(query.document)

        # Query similar documents
        similar_docs = await document_processor.query_similar_documents(summary)
        
        # Get the single most similar document segment and its score
        result = []

        for doc_segment, score in similar_docs:
            doc_uuid = doc_segment.metadata['uuid']
            target_doc = CopusMongoDB.get_document(doc_uuid)

            # Get recommendation reason
            recommend_reason = await llm_service.generate_recommendation_reason(
                query.document,
                target_doc['content']
            )
            for item in result:
                if item.uuid == doc_uuid:
                    continue

            result.append(RecommendationResponse(
                uuid=doc_uuid,
                recommend_reason=recommend_reason
            ))
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 