from datetime import datetime
from typing import Dict, Any
from uuid import UUID
from domain.entities.comment import Comment

class CommentDocument:
    @staticmethod
    def to_document(comment: Comment) -> Dict[str, Any]:
        return {
            "_id": str(comment.id),
            "post_id": str(comment.post_id),
            "content": comment.content,
            "author": comment.author,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at
        }

    @staticmethod
    def from_document(doc: Dict[str, Any]) -> Comment:
        return Comment(
            id=UUID(doc["_id"]),
            post_id=UUID(doc["post_id"]),
            content=doc["content"],
            author=doc["author"],
            created_at=doc["created_at"],
            updated_at=doc.get("updated_at")
        )
