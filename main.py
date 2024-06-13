from fastapi import FastAPI
from src.router import user, discussion, comment, like
from src.db.session import engine
from src.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.user_router, prefix="/users", tags=["users"])
app.include_router(discussion.discussion_router, prefix="/discussions", tags=["discussions"])
app.include_router(comment.comment_router, prefix="/comments", tags=["comments"])
app.include_router(like.like_router, prefix="/likes", tags=["likes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
