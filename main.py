from models import MoodEntry, User
from schemas import MoodCreate, MoodUpdate

from typing import Annotated

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from schemas import UserCreate, UserUpdate

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import User
from schemas import UserCreate

from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from schemas import UserCreate
from models import User
from database import get_session

from typing import Annotated

from fastapi import (
    FastAPI, Depends, HTTPException, Query, Response
)
from sqlmodel import Session, select

from database import get_session
from models import User, JournalEntry
from schemas import JournalCreate, JournalUpdate

app = FastAPI(title="SoulSync API")


@app.post("/users", status_code=201)
def create_user(
    data: UserCreate,
    session: Annotated[Session, Depends(get_session)]
):
    user = User(
        name=data.name,
        email=data.email
    )

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists"
        )

    session.refresh(user)

    return user

from fastapi import Query

@app.get("/users", status_code=200)
def get_users(
    session: Annotated[Session, Depends(get_session)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    statement = (
        select(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
    )

    users = session.exec(statement).all()

    return users



@app.get("/users/{user_id}", status_code=200)
def get_user(
    user_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.patch("/users/{user_id}", status_code=200)
def update_user(
    user_id: int,
    data: UserUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    update_data = data.model_dump(exclude_unset=True)

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=422,
            detail="Name and email cannot be null"
        )

    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Update conflicts with a database constraint"
        )

    session.refresh(user)

    return user


from fastapi import Response

@app.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    user = session.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    session.delete(user)
    session.commit()

    return Response(status_code=204)


@app.post("/moods", status_code=201)
def create_mood(
    data: MoodCreate,
    session: Annotated[Session, Depends(get_session)]
):
    user = session.get(User, data.user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    mood = MoodEntry(
        user_id=data.user_id,
        mood=data.mood,
        note=data.note
    )

    session.add(mood)
    session.commit()
    session.refresh(mood)

    return mood


@app.get("/moods", status_code=200)
def get_moods(
    session: Annotated[Session, Depends(get_session)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    statement = (
        select(MoodEntry)
        .order_by(MoodEntry.id)
        .offset(skip)
        .limit(limit)
    )

    moods = session.exec(statement).all()

    return moods

@app.get("/moods/{mood_id}", status_code=200)
def get_mood(
    mood_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    mood = session.get(MoodEntry, mood_id)

    if mood is None:
        raise HTTPException(
            status_code=404,
            detail="Mood not found"
        )

    return mood


@app.patch("/moods/{mood_id}", status_code=200)
def update_mood(
    mood_id: int,
    data: MoodUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    mood = session.get(MoodEntry, mood_id)

    if mood is None:
        raise HTTPException(
            status_code=404,
            detail="Mood not found"
        )

    update_data = data.model_dump(exclude_unset=True)

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=422,
            detail="Mood fields cannot be null"
        )

    for key, value in update_data.items():
        setattr(mood, key, value)

    session.add(mood)
    session.commit()
    session.refresh(mood)

    return mood


@app.delete("/moods/{mood_id}", status_code=204)
def delete_mood(
    mood_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    mood = session.get(MoodEntry, mood_id)

    if mood is None:
        raise HTTPException(
            status_code=404,
            detail="Mood not found"
        )

    session.delete(mood)
    session.commit()

    return Response(status_code=204)

@app.post("/journals", status_code=201)
def create_journal(
    data: JournalCreate,
    session: Annotated[Session, Depends(get_session)]
):
    user = session.get(User, data.user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    journal = JournalEntry(
        user_id=data.user_id,
        title=data.title,
        content=data.content
    )

    session.add(journal)
    session.commit()
    session.refresh(journal)

    return journal

@app.get("/journals", status_code=200)
def get_journals(
    session: Annotated[Session, Depends(get_session)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
):
    statement = (
        select(JournalEntry)
        .order_by(JournalEntry.id)
        .offset(skip)
        .limit(limit)
    )

    return session.exec(statement).all()

@app.get("/journals/{journal_id}", status_code=200)
def get_journal(
    journal_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    journal = session.get(JournalEntry, journal_id)

    if journal is None:
        raise HTTPException(
            status_code=404,
            detail="Journal not found"
        )

    return journal  


@app.patch("/journals/{journal_id}", status_code=200)
def update_journal(
    journal_id: int,
    data: JournalUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    journal = session.get(JournalEntry, journal_id)

    if journal is None:
        raise HTTPException(
            status_code=404,
            detail="Journal not found"
        )

    updates = data.model_dump(exclude_unset=True)

    if any(value is None for value in updates.values()):
        raise HTTPException(
            status_code=422,
            detail="Journal fields cannot be null"
        )

    for key, value in updates.items():
        setattr(journal, key, value)

    session.commit()
    session.refresh(journal)

    return journal

@app.delete("/journals/{journal_id}", status_code=204)
def delete_journal(
    journal_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    journal = session.get(JournalEntry, journal_id)

    if journal is None:
        raise HTTPException(
            status_code=404,
            detail="Journal not found"
        )

    session.delete(journal)
    session.commit()

    return Response(status_code=204)