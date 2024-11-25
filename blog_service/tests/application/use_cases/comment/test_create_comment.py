import pytest
from uuid import uuid4
from application.use_cases.comment.create_comment import CreateComment

pytestmark = pytest.mark.asyncio

async def test_create_comment_for_existing_post(uow, sample_post):
    """Test creating a comment for an existing post"""
    # Arrange
    await uow.posts.add(sample_post)
    use_case = CreateComment(uow)

    # Act
    comment = await use_case.execute(
        post_id=sample_post.id,
        content="Test Comment",
        author="Test Author"
    )

    # Assert
    assert comment.content == "Test Comment"
    assert comment.author == "Test Author"
    assert comment.post_id == sample_post.id
    assert uow.committed is True

    # Verify comment was saved
    saved_comment = await uow.comments.get(comment.id)
    assert saved_comment == comment

async def test_create_comment_for_non_existing_post(uow):
    """Test creating a comment for a non-existing post"""
    # Arrange
    use_case = CreateComment(uow)
    non_existing_id = uuid4()

    # Act & Assert
    with pytest.raises(ValueError, match="Post not found"):
        await use_case.execute(
            post_id=non_existing_id,
            content="Test Comment",
            author="Test Author"
        )
    
    # Verify no comment was saved
    comments = await uow.comments.list()
    assert len(comments) == 0
    assert uow.rolled_back is True

async def test_create_comment_with_invalid_data(uow, sample_post):
    """Test creating a comment with invalid data"""
    # Arrange
    await uow.posts.add(sample_post)
    use_case = CreateComment(uow)

    # Act & Assert
    with pytest.raises(ValueError, match="Content cannot be empty"):
        await use_case.execute(
            post_id=sample_post.id,
            content="",  # Invalid empty content
            author="Test Author"
        )
    
    # Verify no comment was saved
    comments = await uow.comments.list()
    assert len(comments) == 0
    assert uow.rolled_back is True
