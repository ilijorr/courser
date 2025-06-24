from typing import Annotated, List, Tuple
from uuid import UUID
from langchain_core.documents import Document
from sqlalchemy.exc import NoResultFound
from enums.course import CourseCategory
from schemas.course import Course, CourseCreate, CourseRelational
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status, Query
from sqlmodel import Session, select
from langchain_core.vectorstores import VectorStore

from rel_db import postgres
from vec_db import pinecone
from models import Course as CourseModel

router = APIRouter(
        prefix = "/courses",
        tags=["courses"],
        dependencies=[]
        )

def to_document(course: Course) -> Tuple[Document, str]:
    fields_to_exclude = set(CourseRelational.model_fields.keys())
    data = course.model_dump(exclude=fields_to_exclude)
    id_str = str(data.pop("id"))
    return Document(
            page_content=data.pop("description"),
            metadata=data
            ), id_str

@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=UUID)
async def create_course(
        course: CourseCreate,
        rel_db: Annotated[Session, Depends(postgres.get_db)],
        vec_db: Annotated[VectorStore, Depends(pinecone.get_db)]
        ):
    course = Course(**course.model_dump())
    rel_db.add(CourseModel(**course.model_dump()))

    try:
        doc, id = to_document(course)
        await vec_db.aadd_documents([doc], ids=[id])
    except Exception as e:
        rel_db.rollback()
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"error while upserting vector to db, {e}"
                )

    try:
        rel_db.commit()
    except Exception as e:
        rel_db.rollback()
        vec_db.delete(ids=[id])
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"error while inserting into relational db"
                )
    return course.id

@router.post("/batch",
             status_code=status.HTTP_201_CREATED,
             response_model=List[UUID])
async def create_course_batch(
        courses_without_id: Annotated[List[CourseCreate], Body(...)],
        rel_db: Annotated[Session, Depends(postgres.get_db)],
        vec_db: Annotated[VectorStore, Depends(pinecone.get_db)]
        ):
    try:
        courses = [Course(**course.model_dump()) for course in courses_without_id]
        rel_db.add_all([CourseModel(**course.model_dump()) for course in courses])
        rel_db.commit()
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"error while inserting into relational db, {e}"
                )
    try:
        documents, ids = map(list, zip(*[to_document(course) for course in courses]))
        await vec_db.aadd_documents(documents, ids=ids)
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"error while upserting to vecdb, {e}"
                )
    return [course.id for course in courses]

@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=List[CourseModel])
async def get_courses(
        rel_db: Annotated[Session, Depends(postgres.get_db)],
        uni_id: Annotated[int | None, Query(ge=1)] = None,
        is_summer: Annotated[bool | None, Query()] = None,
        category: Annotated[CourseCategory | None, Query()] = None,
        ):
    query = select(CourseModel)
    if uni_id is not None:
        query = query.where(CourseModel.uni_id == uni_id)
    if is_summer is not None:
        query = query.where(CourseModel.is_summer == is_summer)
    if category is not None:
        query = query.where(CourseModel.category == category)

    try:
        courses = rel_db.exec(query).all()
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"db error, {e}"
                )

    return courses

@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=CourseModel)
async def get_course(
        id: Annotated[UUID, Path()],
        rel_db: Annotated[Session, Depends(postgres.get_db)],
        ):
    query = select(CourseModel).where(CourseModel.id == id)
    try:
        course_model = rel_db.exec(query).one()
    except Exception as e:
        return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"id not found, {e}"
                )
    return course_model

@router.get("/university/{uni_id}",
            response_model=List[CourseModel])
async def get_courses_for_university(
        uni_id: Annotated[int, Path(..., ge=1)],
        rel_db: Annotated[Session, Depends(postgres.get_db)]
        ):
    query = select(CourseModel).where(CourseModel.uni_id == uni_id)
    try:
        courses = rel_db.exec(query).all()
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"db error, {e}"
                )
    return courses

@router.put("/{id}",
            status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def put_course():
    return None

@router.delete("/{id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
        id: Annotated[UUID, Path(...)],
        rel_db: Annotated[Session, Depends(postgres.get_db)],
        vec_db: Annotated[VectorStore, Depends(pinecone.get_db)]
        ):
    query = select(CourseModel).where(CourseModel.id == id)
    success = await vec_db.adelete([str(id)])
    if success is False:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"course not found"
                )
    try:
        course = rel_db.exec(query).one()
        rel_db.delete(course)
        rel_db.commit()
    except NoResultFound as e:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"course not found, \n {e}"
                )
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"relational db error, \n {e}"
                )
    return None
