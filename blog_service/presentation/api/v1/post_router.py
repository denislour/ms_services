from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from domain.entities.post import Post
from domain.value_objects.post_status import PostStatus
from presentation.schemas.post_schema import PostCreate, PostUpdate, PostResponse
from core.dependencies import (
    get_create_post_use_case,
    get_get_post_use_case,
    get_list_posts_use_case,
    get_update_post_use_case,
    get_delete_post_use_case,
    get_change_post_status_use_case
)
from application.use_cases.post.create_post import CreatePostUseCase
from application.use_cases.post.get_post import GetPostUseCase
from application.use_cases.post.list_posts import ListPostsUseCase
from application.use_cases.post.update_post import UpdatePostUseCase
from application.use_cases.post.delete_post import DeletePostUseCase
from application.use_cases.post.change_post_status import ChangePostStatusUseCase

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    use_case: CreatePostUseCase = Depends(get_create_post_use_case)
) -> Post:
    return await use_case.execute(post.title, post.content, post.author)

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    use_case: GetPostUseCase = Depends(get_get_post_use_case)
) -> Post:
    post = await use_case.execute(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/", response_model=List[PostResponse])
async def list_posts(
    use_case: ListPostsUseCase = Depends(get_list_posts_use_case)
) -> List[Post]:
    return await use_case.execute()

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post: PostUpdate,
    use_case: UpdatePostUseCase = Depends(get_update_post_use_case)
) -> Post:
    updated_post = await use_case.execute(post_id, post.title, post.content, post.author)
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    use_case: DeletePostUseCase = Depends(get_delete_post_use_case)
):
    deleted = await use_case.execute(post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")

@router.post("/{post_id}/publish", response_model=PostResponse)
async def publish_post(
    post_id: int,
    use_case: ChangePostStatusUseCase = Depends(get_change_post_status_use_case)
) -> Post:
    post = await use_case.execute(post_id, PostStatus.PUBLISHED)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/{post_id}/archive", response_model=PostResponse)
async def archive_post(
    post_id: int,
    use_case: ChangePostStatusUseCase = Depends(get_change_post_status_use_case)
) -> Post:
    post = await use_case.execute(post_id, PostStatus.ARCHIVED)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
