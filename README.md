# Courser

Courser is a web app which uses AI to make applying to Erasmus+ student exchange program easier.

## TODO

Backend:
- [x] basic testing
- [ ] rag-related testing
- [ ] fix formatting
- [ ] expand models
- [ ] implement authorization

Frontend:
- [ ] create webapp
- [ ] test webapp

Building:
- [ ] put everything in docker
      


## Running

### Prerequisites

You need a PostgreSQL base, an embedding model and a Pinecone index with valid dimensions for your embedding model.
In the root folder, create a `.env` file and place all the environmental variables the app needs. They are going to be listed here when the development is finished, but you can check [the settings file](./app/core/settings.py) for any variable you need.

Requirements are in the `app/requirements.txt` file, so [create a virtual environment](https://fastapi.tiangolo.com/virtual-environments/#create-a-virtual-environment), [activate it](https://fastapi.tiangolo.com/virtual-environments/#activate-the-virtual-environment), and run `pip install -r app/requirements.txt`.

The app is still in development, but you run it as you would for any FastAPI app, `fastapi dev app/main.py`

## Docs

To learn about the endpoints, check out the generated docs on [127.0.0.1:8000/docs], if running locally.
