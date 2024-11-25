import pytest
from uuid import uuid4
from application.use_cases.comment.delete_comment import DeleteComment

pytestmark = pytest.mark.asyncio

async def test_delete_existing_comment(uow, sample_post, sample_comment):
    """Test deleting an existing comment"""
    # Arrange
    await uow.posts.add(sample_post)
    await uow.comments.add(sample_comment)
    use_case = DeleteComment(uow)

    # Act
    await use_case.execute(sample_comment.id)

    # Assert
    # Verify comment was deleted
    deleted_comment = await uow.comments.get(sample_comment.id)
    assert deleted_comment is None
    
    # Verify post still exists
    existing_post = await uow.posts.get(sample_post.id)
    assert existing_post == sample_post
    
    assert uow.committed is True

async def test_delete_non_existing_comment(uow):
    """Test deleting a non-existing comment"""
    # Arrange
    use_case = DeleteComment(uow)
    non_existing_id = uuid4()

    # Act
    await use_case.execute(non_existing_id)

    # Assert
    assert uow.committed is True  # Should commit even if comment doesn't exist

async def test_delete_comment_transaction_rollback(uow, sample_post, sample_comment):
    """Test transaction rollback when delete fails"""
    # Arrange
    await uow.posts.add(sample_post)
    await uow.comments.add(sample_comment)
    use_case = DeleteComment(uow)
    
    # Simulate database error
    uow.comments.delete = lambda _: (_ for _ in ()).throw(Exception("Database error"))

    # Act & Assert
    with pytest.raises(Exception, match="Database error"):
        await use_case.execute(sample_comment.id)
    
    # Verify comment still exists due to rollback
    existing_comment = await uow.comments.get(sample_comment.id)
    assert existing_comment == sample_comment
    assert uow.rolled_back is True
