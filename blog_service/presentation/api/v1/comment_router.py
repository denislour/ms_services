from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from application.ports.unit_of_work import UnitOfWork
from infrastructure.sqlite3.unit_of_work import SQLiteUnitOfWork
from presentation.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/comments", tags=["comments"])

async def get_uow() -> UnitOfWork:
    return SQLiteUnitOfWork()

@router.post("/{post_id}", response_model=CommentResponse)
async def create_comment(
    post_id: UUID,
    comment_data: CommentCreate,
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow as uow:
        # Check if post exists
        post = await uow.posts.get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Create comment
        comment = await uow.comments.add(
            Comment(
                id=uuid4(),
                post_id=post_id,
                content=comment_data.content,
                author=comment_data.author,
                created_at=datetime.utcnow()
            )
        )
        await uow.commit()
        return comment

@router.get("/{post_id}", response_model=List[CommentResponse])
async def get_comments(
    post_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow as uow:
        comments = await uow.comments.get_by_post(post_id)
        return comments

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: UUID,
    uow: UnitOfWork = Depends(get_uow)
):
    async with uow as uow:
        await uow.comments.delete(comment_id)
        await uow.commit()
        return {"message": "Comment deleted"}
