from typing import Annotated, Any, Dict, List
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from langchain_pinecone import PineconeVectorStore

from core.settings import PineconeSettings, SettingsFactory
from enums.course import CourseCategory
from vec_db import pinecone


router = APIRouter(
        prefix = "/search",
        tags=["search"],
        )

"""
fetch response looks like:
    {
            'namespace': 'example-namespace',  
            'usage': {'readUnits': 1},
            'vectors': {
                'id-1':
                    {
                    'id': 'id-1',
                    'values': [0.568879, 0.632687092, 0.856837332, ...]
                    },
                'id-2':
                {
                    'id': 'id-2',
                    'values': [0.00891787093, 0.581895, 0.315718859, ...]
                    }
                }
    } 
"""
def fetch_response_to_vectors (
        response: Dict[str, Any]
        ) -> List[List[float]] :
    vector_dict = response.get('vectors', {})
    if not isinstance(vector_dict, Dict):
        raise ValueError(
                "Response dict must have a field 'vectors'"
                )

    vectors = []
    for vector_data in vector_dict.values():
        if not isinstance(vector_data, Dict):
            raise ValueError(
                    "Each vector entry must be a dictionary"
                    )
        vector = vector_data.get('values')
        if not isinstance(vector, List):
            raise ValueError(
                    "vector values are not a list"
                    )

        if not all(isinstance(x, (float, int)) for x in vector):
            raise ValueError(
                    "not all vector values are float/int"
                    )
        vectors.append(vector)

    return vectors

async def find_similair(
        vec_db: PineconeVectorStore,
        id_category_dict: Dict[UUID, CourseCategory],
        uni_id: int,
        is_summer: bool,
        index_name: str = "courser",
        count: int = 10
        ) -> Dict[UUID, List[UUID]]:
    settings = SettingsFactory.create(PineconeSettings)
    index = vec_db.get_pinecone_index(index_name, pinecone_api_key=settings.api_key)

    fetch_response = index.fetch(ids=[str(id) for id in id_category_dict.keys()])
    vectors = fetch_response_to_vectors(fetch_response.to_dict())

    results = {}

    for course_id, vector in zip(id_category_dict.keys(), vectors):
        filters = {
                "uni_id": uni_id,
                "is_summer": is_summer,
                "category": id_category_dict[course_id].value
                }
        
        similair_docs = vec_db.asimilarity_search_by_vector(
                embedding=vector,
                k=count,
                filter=filters
                )
        
        if not isinstance(similair_docs, List):
            raise TypeError(
                    f"similair docs is not a list, it is {type(similair_docs)}"
                    )
        similair_ids = [UUID(doc.metadata["id"]) for doc in similair_docs]
        results[course_id] = similair_ids

    return results

@router.post("/{uni_id}",
             status_code=status.HTTP_200_OK,
             response_model=Dict[UUID, List[UUID]])
async def search_by_uni(
            vec_db: Annotated[PineconeVectorStore, Depends(pinecone.get_db)],
            id_category_dict: Annotated[Dict[UUID, CourseCategory], Body(...)],
            is_summer: Annotated[bool, Query(...)],
            uni_id: Annotated[int, Path(...)]
            ):
    try:
        return await find_similair(
                vec_db, id_category_dict, is_summer=is_summer, uni_id=uni_id
                )
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e
                )

