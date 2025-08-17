from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from .models import ShortenedUrl
from .db import engine, get_db
from .service import create_short_link

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.get('/')
async def home():
    return {'message':'welcome to URL Shortner'}

@app.post("/shorten")
async def get_short_link( url : schemas.url, db: AsyncSession = Depends(get_db)):

    short_link = create_short_link(url)
    obj = ShortenedUrl(original_url=url.body, short_link=short_link)
    db.add(obj)
    await db.commit()

    return {"short_link": short_link}


@app.get("/{short_link}")
async def redirect_to_original(short_link: str, db: AsyncSession = Depends(get_db)):
    obj = (
        db.query(ShortenedUrl).filter_by(short_link=short_link).order_by(ShortenedUrl.id.desc()).first()
    )
    if obj is None:
        raise HTTPException(
            status_code=404, detail="link does not exist, couldn't redirect"
        )
    return {"original_url": obj.original_url}
