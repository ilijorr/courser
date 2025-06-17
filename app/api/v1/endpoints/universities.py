from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlmodel import Session, select

from enums.university import Country
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

@router.get("/",
            response_model=List[UniversityResponse])
def get_universities_with_filter(
        rel_db: Annotated[Session, Depends(postgres.get_db)],
        country_name: Annotated[str | None, Query(max_length=50)] = None,
       ):
    query = select(UniversityModel)
    if country_name is not None:
        try:
            country = Country(country_name.upper())
            query = query.where(UniversityModel.country == country)
        except ValueError:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="invalid country"
                                )
    universities = rel_db.exec(query).all()
    return [UniversityModel.model_validate(university) 
            for university in universities]

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

@router.delete("/{uni_id}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_university(
        uni_id: Annotated[int, Path(ge=1)],
        rel_db: Annotated[Session, Depends(postgres.get_db)]
        ):
    query = select(UniversityModel).where(UniversityModel.id == uni_id)
    results = rel_db.exec(query)
    
    
