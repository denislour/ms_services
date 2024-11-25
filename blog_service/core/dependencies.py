from fastapi import Depends
from core.db_factory import DBFactory
from application.use_cases.post.create_post import CreatePost, CreatePostUseCase
from application.use_cases.post.get_post import GetPost, GetPostUseCase
from application.use_cases.post.list_posts import ListPosts, ListPostsUseCase
from application.use_cases.post.update_post import UpdatePost, UpdatePostUseCase
from application.use_cases.post.delete_post import DeletePost, DeletePostUseCase
from application.use_cases.post.change_post_status import ChangePostStatus, ChangePostStatusUseCase

# Get the repository factory based on current database type
get_post_repository = DBFactory.get_repository_factory()

def get_create_post_use_case(repo=Depends(get_post_repository)) -> CreatePostUseCase:
    return CreatePost(repo)

def get_get_post_use_case(repo=Depends(get_post_repository)) -> GetPostUseCase:
    return GetPost(repo)

def get_list_posts_use_case(repo=Depends(get_post_repository)) -> ListPostsUseCase:
    return ListPosts(repo)

def get_update_post_use_case(repo=Depends(get_post_repository)) -> UpdatePostUseCase:
    return UpdatePost(repo)

def get_delete_post_use_case(repo=Depends(get_post_repository)) -> DeletePostUseCase:
    return DeletePost(repo)

def get_change_post_status_use_case(repo=Depends(get_post_repository)) -> ChangePostStatusUseCase:
    return ChangePostStatus(repo)
