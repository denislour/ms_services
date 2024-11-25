import pytest
from uuid import uuid4
from application.use_cases.post.delete_post import DeletePost

pytestmark = pytest.mark.asyncio

async def test_delete_existing_post(uow, sample_post, sample_comment):
    """Test deleting a post with comments"""
    # Arrange
    await uow.posts.add(sample_post)
    await uow.comments.add(sample_comment)  # Add a comment to the post
    use_case = DeletePost(uow)

    # Act
    await use_case.execute(sample_post.id)

    # Assert
    # Verify post was deleted
    deleted_post = await uow.posts.get(sample_post.id)
    assert deleted_post is None

    # Verify associated comments were deleted
    deleted_comment = await uow.comments.get(sample_comment.id)
    assert deleted_comment is None
    
    assert uow.committed is True

async def test_delete_non_existing_post(uow):
    """Test deleting a non-existing post"""
    # Arrange
    use_case = DeletePost(uow)
    non_existing_id = uuid4()

    # Act
    await use_case.execute(non_existing_id)

    # Assert
    assert uow.committed is True  # Should commit even if post doesn't exist

async def test_delete_post_transaction_rollback(uow, sample_post):
    """Test transaction rollback when delete fails"""
    # Arrange
    await uow.posts.add(sample_post)
    use_case = DeletePost(uow)
    
    # Simulate database error by making repository raise exception
    uow.posts.delete = lambda _: (_ for _ in ()).throw(Exception("Database error"))

    # Act & Assert
    with pytest.raises(Exception, match="Database error"):
        await use_case.execute(sample_post.id)
    
    # Verify post still exists due to rollback
    existing_post = await uow.posts.get(sample_post.id)
    assert existing_post == sample_post
    assert uow.rolled_back is True
