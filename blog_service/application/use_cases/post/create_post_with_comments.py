from typing import List, Tuple
from uuid import uuid4
from datetime import datetime
from domain.entities.post import Post
from domain.entities.comment import Comment
from domain.value_objects.post_status import PostStatus
from application.ports.unit_of_work import UnitOfWork

class CreatePostWithComments:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(
        self,
        title: str,
        content: str,
        author: str,
        comments_data: List[dict]
    ) -> Tuple[Post, List[Comment]]:
        # Create post entity
        post = Post(
            id=uuid4(),
            title=title,
            content=content,
            author=author,
            status=PostStatus.DRAFT,
            created_at=datetime.utcnow()
        )

        # Create comment entities
        comments = [
            Comment(
                id=uuid4(),
                post_id=post.id,
                content=comment_data["content"],
                author=comment_data["author"],
                created_at=datetime.utcnow()
            )
            for comment_data in comments_data
        ]

        async with self.uow as uow:
            try:
                # Create post
                created_post = await uow.posts.add(post)

                # Create comments
                created_comments = []
                for comment in comments:
                    created_comment = await uow.comments.add(comment)
                    created_comments.append(created_comment)

                # Commit transaction
                await uow.commit()
                return created_post, created_comments

            except Exception:
                # Rollback on any error
                await uow.rollback()
                raise
