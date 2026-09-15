from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import app.groups.models as members
from app.database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()
members.Base.metadata.create_all(bind=engine)

class Members(BaseModel):
    id: int
    name: str
    discord: str
    birthdate: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/members/{member_id}")
async def read_members(member_id: int, db: db_dependency):
    result = db.query(members.Members).filter(members.Members.id == member_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Member not found")
    return result


@app.post("/members/")
async def create_member(member: Members, db: db_dependency):
    db_member = members.Members(
        id=member.id,
        name=member.name,
        discord=member.discord,
        birthdate=member.birthdate
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member