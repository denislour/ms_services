from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from domain.entities.post import Post
from domain.value_objects.post_status import PostStatus

class PostDocument:
    @staticmethod
    def to_document(post: Post) -> Dict[str, Any]:
        return {
            "_id": str(post.id),
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "status": post.status.value,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "comments": [CommentDocument.to_document(comment) for comment in post.comments]
        }

    @staticmethod
    def from_document(doc: Dict[str, Any]) -> Post:
        return Post(
            id=UUID(doc["_id"]),
            title=doc["title"],
            content=doc["content"],
            author=doc["author"],
            status=PostStatus(doc["status"]),
            created_at=doc["created_at"],
            updated_at=doc.get("updated_at"),
            comments=[CommentDocument.from_document(comment) for comment in doc.get("comments", [])]
        )
