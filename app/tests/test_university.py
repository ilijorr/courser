from fastapi import status
from fastapi.testclient import TestClient
from testconf import *

import random

PATH_PREFIX = "/v1/universities"

def test_post(client: TestClient):
    name = "Univerzitet u Novom Sadu"
    country = "Serbia"

    response = client.post(
            PATH_PREFIX + "/",
            json={
                "name": name,
                "country": country
                }
            )
    
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] > 0
    assert data["name"] == name
    assert data["country"] == country

def test_post_bad_args(client: TestClient):
    response_codes = []
    ###################################################################
    response = client.post(
            PATH_PREFIX + "/",
            json = {}
            )
    response_codes.append(response.status_code)
    ###################################################################
    response = client.post(
            PATH_PREFIX + "/",
            json = {"name": "some name"}
            )

    response_codes.append(response.status_code)
    ###################################################################
    response = client.post(
            PATH_PREFIX + "/",
            json = {"country": "some country"}
            )

    response_codes.append(response.status_code)
    ###################################################################
    response = client.post(
            PATH_PREFIX + "/",
            json = {"name":5}
            )

    response_codes.append(response.status_code)
    ###################################################################

    assert all(
            code == status.HTTP_422_UNPROCESSABLE_ENTITY for code in response_codes
            )

def test_post_invalid_country(client: TestClient):
    name = "Tokyo University"
    country = "Japan"

    response = client.post(
            PATH_PREFIX + "/",
            json={
                "name": name,
                "country": country
                }
            )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

def test_get(client: TestClient):
    name = "Univerzitet u Novom Sadu"
    country = "Serbia"

    response = client.post(
            PATH_PREFIX + "/",
            json={
                "name": name,
                "country": country
                }
            )

    id = response.json()["id"]
    
    response = client.get(
            PATH_PREFIX + "/" + str(id)
            )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == name
    assert response.json()["country"] == country

def test_get_unexistent(client: TestClient):
    response = client.get(
            PATH_PREFIX + "/1"
            )

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_bad_args(client: TestClient):
    response = client.get(
            PATH_PREFIX + "/asdf"
            )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.get(
            PATH_PREFIX + "/"
            )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

def test_put(client:TestClient):
    name = "Univerzitet u Novom Sadu"
    country = "Serbia"

    response = client.post(
            PATH_PREFIX + "/",
            json={
                "name": name,
                "country": country
                }
            )

    id = response.json()["id"]

    new_name = "somename"
    new_country = "Croatia"
    response = client.put(
            PATH_PREFIX + "/" + str(id),
            json={
                "name": new_name,
                "country": new_country
                }
            )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == new_name
    assert data["country"] == new_country

def test_put_unexistent(client: TestClient):
    id = random.randint(1,100)
    response = client.put(
            PATH_PREFIX + "/" + str(id),
            json={
                "name": "asd",
                "country": "Serbia"
                }
            )

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_put_empty(client: TestClient):
    name = "Univerzitet u Novom Sadu"
    country = "Serbia"

    response = client.post(
            PATH_PREFIX + "/",
            json={
                "name": name,
                "country": country
                }
            )

    id = response.json()["id"]

    new_country = "Croatia"
    response = client.put(
            PATH_PREFIX + "/" + str(id),
            json={
                "name": "",
                "country": new_country
                }
            )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    new_name = "somename"
    response = client.put(
            PATH_PREFIX + "/" + str(id),
            json={
                "name": new_name,
                "country": ""
                }
            )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
