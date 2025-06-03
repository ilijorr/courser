from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlmodel import Session

from rel_db import postgres
from schemas.university import UniversityCreate, UniversityResponse
from models.university import University as UniversityModel

router = APIRouter(
        prefix="/universities",
        tags=["universities"],
        dependencies=[]
        )

@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=UniversityResponse)
def create_university(
        university: UniversityCreate,
        rel_db: Annotated[Session, Depends(postgres.get_db)]):
    uni_model = UniversityModel(**university.model_dump())
    rel_db.add(uni_model)
    try:
        rel_db.commit()
    except Exception:
        rel_db.rollback()
        raise
    rel_db.refresh(uni_model)
    return UniversityResponse.model_validate(uni_model)

@router.get("/{uni_id}", 
            response_model=UniversityResponse)
def get_university(
        uni_id: Annotated[int, Path(ge=1)],
        rel_db: Annotated[Session, Depends(postgres.get_db)]):
    db_model = rel_db.get(UniversityModel, uni_id)
    if db_model is None:
        raise HTTPException(
                status_code=404,
                detail="University not found")
    return UniversityResponse.model_validate(db_model)

@router.put("/{uni_id}",
            response_model=UniversityResponse,
            status_code=status.HTTP_200_OK)
def update_university(
        uni_id: Annotated[int, Path(ge=1)],
        university: UniversityCreate,
        rel_db: Annotated[Session, Depends(postgres.get_db)]):
    db_model = rel_db.get(UniversityModel, uni_id)
    if db_model is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="university not found")

    update_data = university.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_model, field, value)

    rel_db.add(db_model)
    rel_db.commit()
    rel_db.refresh(db_model)
    return UniversityResponse.model_validate(db_model)
