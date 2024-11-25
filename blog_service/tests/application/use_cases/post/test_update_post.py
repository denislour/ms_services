import pytest
from uuid import uuid4
from application.use_cases.post.update_post import UpdatePost
from domain.value_objects.post_status import PostStatus

pytestmark = pytest.mark.asyncio

async def test_update_existing_post(uow, sample_post):
    """Test updating an existing post with new data"""
    # Arrange
    await uow.posts.add(sample_post)
    use_case = UpdatePost(uow)
    new_title = "Updated Title"
    new_content = "Updated Content"

    # Act
    updated_post = await use_case.execute(
        post_id=sample_post.id,
        title=new_title,
        content=new_content
    )

    # Assert
    assert updated_post.title == new_title
    assert updated_post.content == new_content
    assert updated_post.id == sample_post.id
    assert updated_post.author == sample_post.author  # Unchanged field
    assert updated_post.updated_at is not None
    assert uow.committed is True

    # Verify changes were persisted
    saved_post = await uow.posts.get(sample_post.id)
    assert saved_post == updated_post

async def test_update_post_status(uow, sample_post):
    """Test updating post status"""
    # Arrange
    await uow.posts.add(sample_post)
    use_case = UpdatePost(uow)

    # Act
    updated_post = await use_case.execute(
        post_id=sample_post.id,
        status=PostStatus.PUBLISHED
    )

    # Assert
    assert updated_post.status == PostStatus.PUBLISHED
    assert updated_post.updated_at is not None
    assert uow.committed is True

async def test_update_non_existing_post(uow):
    """Test updating a non-existing post returns None"""
    # Arrange
    use_case = UpdatePost(uow)
    non_existing_id = uuid4()

    # Act
    result = await use_case.execute(
        post_id=non_existing_id,
        title="New Title",
        content="New Content"
    )

    # Assert
    assert result is None
    assert uow.committed is True  # Should still commit even if post not found

async def test_update_post_with_invalid_data(uow, sample_post):
    """Test updating post with invalid data should raise error"""
    # Arrange
    await uow.posts.add(sample_post)
    use_case = UpdatePost(uow)

    # Act & Assert
    with pytest.raises(ValueError, match="Title cannot be empty"):
        await use_case.execute(
            post_id=sample_post.id,
            title="",  # Invalid empty title
            content="Some content"
        )
    
    # Verify original post was not changed
    saved_post = await uow.posts.get(sample_post.id)
    assert saved_post == sample_post
    assert uow.rolled_back is True
