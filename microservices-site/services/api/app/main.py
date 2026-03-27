from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .db import Base, SessionLocal, engine
from .models import Item


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class ItemRead(BaseModel):
    id: int
    name: str
    description: str | None


@contextmanager
def get_db_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Catalog API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/items", response_model=list[ItemRead])
def list_items() -> list[ItemRead]:
    with get_db_session() as session:
        results = session.execute(select(Item)).scalars().all()
        return [ItemRead(id=item.id, name=item.name, description=item.description) for item in results]


@app.post("/items", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate) -> ItemRead:
    with get_db_session() as session:
        try:
            item = Item(name=payload.name, description=payload.description)
            session.add(item)
            session.commit()
            session.refresh(item)
            return ItemRead(id=item.id, name=item.name, description=item.description)
        except SQLAlchemyError as exc:
            session.rollback()
            raise HTTPException(status_code=500, detail="Database error") from exc
