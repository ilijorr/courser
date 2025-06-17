from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session
from uuid import UUID
from testconf import *

PATH_PREFIX = "/v1/courses"
"""
def test_post(client: TestClient, rel_session: Session):
    
        #1. stavim neki univerzitet u bazu
        #2. testiram
    
    id = post_test_unis(rel_session)[0]

    assert id == 1

    response = client.post(
            PATH_PREFIX,
            json={
                "uni_id": id,
                "is_summer": True,
                "name": "Mathematics",
                "category": get_random_category()
                }
            )
    data = response.json()

    assert isinstance(data["id"], UUID)
    assert response.status_code == status.HTTP_201_CREATED

def test_post_bad_args(client: TestClient, rel_session: Session):
    pass

def test_post_batch(client: TestClient, rel_session: Session):
    pass

def test_post_batch_empty(client: TestClient, rel_session: Session):
    pass

def test_get(client: TestClient, rel_session: Session):
    pass

def test_get_unexsitent(client: TestClient, rel_session: Session):
    pass

def test_get_for_uni(client: TestClient, rel_session: Session):
    pass

def test_get_for_uni_unexistent(client: TestClient, rel_session: Session):
    pass

def test_put(client: TestClient, rel_session: Session):
    pass

def test_put_bad_args(client: TestClient, rel_session: Session):
    pass
"""
