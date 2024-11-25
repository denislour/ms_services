from uuid import UUID
from sanic import Blueprint, Request
from sanic.response import json
from application.use_cases.comment.create_comment import CreateComment
from application.use_cases.comment.delete_comment import DeleteComment
from application.use_cases.comment.get_post_comments import GetPostComments
from core.dependencies import get_uow

bp = Blueprint("comments", url_prefix="/comments")

@bp.post("/<post_id:uuid>")
async def create_comment(request: Request, post_id: UUID):
    data = request.json
    
    async with get_uow() as uow:
        use_case = CreateComment(uow)
        comment = await use_case.execute(
            post_id=post_id,
            content=data["content"],
            author=data["author"]
        )
        
        return json({
            "id": str(comment.id),
            "post_id": str(comment.post_id),
            "content": comment.content,
            "author": comment.author,
            "created_at": str(comment.created_at),
            "updated_at": str(comment.updated_at) if comment.updated_at else None
        })

@bp.get("/<post_id:uuid>")
async def get_comments(request: Request, post_id: UUID):
    async with get_uow() as uow:
        use_case = GetPostComments(uow)
        comments = await use_case.execute(post_id)
        
        return json({
            "comments": [
                {
                    "id": str(comment.id),
                    "post_id": str(comment.post_id),
                    "content": comment.content,
                    "author": comment.author,
                    "created_at": str(comment.created_at),
                    "updated_at": str(comment.updated_at) if comment.updated_at else None
                }
                for comment in comments
            ]
        })

@bp.delete("/<comment_id:uuid>")
async def delete_comment(request: Request, comment_id: UUID):
    async with get_uow() as uow:
        use_case = DeleteComment(uow)
        await use_case.execute(comment_id)
        return json({"message": "Comment deleted"})
