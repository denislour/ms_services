from uuid import UUID
from sanic import Blueprint, Request
from sanic.response import json
from application.use_cases.post.create_post_with_comments import CreatePostWithComments
from application.use_cases.post.delete_post import DeletePost
from application.use_cases.post.get_post import GetPost
from application.use_cases.post.list_posts import ListPosts
from application.use_cases.post.update_post import UpdatePost
from presentation.schemas.post_schema import PostCreate, PostUpdate
from core.dependencies import get_uow

bp = Blueprint("posts", url_prefix="/posts")

@bp.post("/")
async def create_post(request: Request):
    data = request.json
    post_data = PostCreate(**data)
    comments_data = data.pop("comments", [])
    
    async with get_uow() as uow:
        use_case = CreatePostWithComments(uow)
        post, comments = await use_case.execute(
            title=post_data.title,
            content=post_data.content,
            author=post_data.author,
            comments_data=comments_data
        )
        
        return json({
            "post": {
                "id": str(post.id),
                "title": post.title,
                "content": post.content,
                "author": post.author,
                "created_at": str(post.created_at),
                "updated_at": str(post.updated_at) if post.updated_at else None
            },
            "comments": [
                {
                    "id": str(comment.id),
                    "content": comment.content,
                    "author": comment.author,
                    "created_at": str(comment.created_at)
                }
                for comment in comments
            ]
        })

@bp.get("/<post_id:uuid>")
async def get_post(request: Request, post_id: UUID):
    async with get_uow() as uow:
        use_case = GetPost(uow)
        post = await use_case.execute(post_id)
        
        if not post:
            return json({"error": "Post not found"}, status=404)
        
        return json({
            "id": str(post.id),
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "created_at": str(post.created_at),
            "updated_at": str(post.updated_at) if post.updated_at else None,
            "comments": [
                {
                    "id": str(comment.id),
                    "content": comment.content,
                    "author": comment.author,
                    "created_at": str(comment.created_at)
                }
                for comment in post.comments
            ]
        })

@bp.get("/")
async def list_posts(request: Request):
    async with get_uow() as uow:
        use_case = ListPosts(uow)
        posts = await use_case.execute()
        
        return json({
            "posts": [
                {
                    "id": str(post.id),
                    "title": post.title,
                    "content": post.content,
                    "author": post.author,
                    "created_at": str(post.created_at),
                    "updated_at": str(post.updated_at) if post.updated_at else None,
                    "comments_count": len(post.comments)
                }
                for post in posts
            ]
        })

@bp.put("/<post_id:uuid>")
async def update_post(request: Request, post_id: UUID):
    data = request.json
    update_data = PostUpdate(**data)
    
    async with get_uow() as uow:
        use_case = UpdatePost(uow)
        post = await use_case.execute(
            post_id=post_id,
            title=update_data.title,
            content=update_data.content
        )
        
        if not post:
            return json({"error": "Post not found"}, status=404)
            
        return json({
            "id": str(post.id),
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "created_at": str(post.created_at),
            "updated_at": str(post.updated_at)
        })

@bp.delete("/<post_id:uuid>")
async def delete_post(request: Request, post_id: UUID):
    async with get_uow() as uow:
        use_case = DeletePost(uow)
        await use_case.execute(post_id)
        return json({"message": "Post deleted"})
