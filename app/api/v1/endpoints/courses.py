from typing import Annotated, List

from langchain_core.documents import Document
from schemas.course import CourseCreate, CourseRelational
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from langchain_core.vectorstores import VectorStore

from rel_db import postgres
from vec_db import pinecone
from models import Course as CourseModel

router = APIRouter(
        prefix = "/courses",
        tags=["courses"],
        dependencies=[]
        )

def to_document(course: CourseCreate) -> Document:
    fields_to_exclude = set(CourseRelational.model_fields.keys())
    data = course.model_dump(exclude=fields_to_exclude)
    data["id"] = str(data["id"])
    return Document(
            page_content=data.pop("description"),
            metadata=data
            )

@router.post("/",
             status_code=status.HTTP_201_CREATED)
async def create_course(
        course: CourseCreate,
        rel_db: Annotated[Session, Depends(postgres.get_db)],
        vec_db: Annotated[VectorStore, Depends(pinecone.get_db)]
        ):
    rel_db.add(CourseModel(**course.model_dump()))
    rel_db.commit()
    await vec_db.aadd_documents([to_document(course)])
    return course.id

@router.post("/batch",
             status_code=status.HTTP_201_CREATED)
async def create_course_batch(
        courses: List[CourseCreate],
        rel_db: Annotated[Session, Depends(postgres.get_db)],
        vec_db: Annotated[VectorStore, Depends(pinecone.get_db)]
        ):
    rel_db.add_all([CourseModel(**course.model_dump()) for course in courses])
    rel_db.commit()
    await vec_db.aadd_documents([to_document(course) for course in courses])
    return [course.id for course in courses]
