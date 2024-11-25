import pytest
from uuid import uuid4
from application.use_cases.post.create_post_with_comments import CreatePostWithComments
from domain.value_objects.post_status import PostStatus

pytestmark = pytest.mark.asyncio

async def test_create_post_without_comments(uow):
    """Test creating a post without any comments"""
    # Arrange
    use_case = CreatePostWithComments(uow)

    # Act
    post, comments = await use_case.execute(
        title="Test Post",
        content="Test Content",
        author="Test Author",
        comments_data=[]
    )

    # Assert
    assert post.title == "Test Post"
    assert post.content == "Test Content"
    assert post.author == "Test Author"
    assert post.status == PostStatus.DRAFT
    assert len(comments) == 0
    assert uow.committed is True

    # Verify post was saved
    saved_post = await uow.posts.get(post.id)
    assert saved_post == post

async def test_create_post_with_comments(uow):
    """Test creating a post with multiple comments"""
    # Arrange
    use_case = CreatePostWithComments(uow)
    comments_data = [
        {"content": "First comment", "author": "Commenter 1"},
        {"content": "Second comment", "author": "Commenter 2"}
    ]

    # Act
    post, comments = await use_case.execute(
        title="Post with Comments",
        content="Post Content",
        author="Post Author",
        comments_data=comments_data
    )

    # Assert
    assert post.title == "Post with Comments"
    assert len(comments) == 2
    assert all(comment.post_id == post.id for comment in comments)
    
    # Verify comments were saved
    for comment in comments:
        saved_comment = await uow.comments.get(comment.id)
        assert saved_comment == comment

async def test_create_post_with_invalid_comment_data(uow):
    """Test creating a post with invalid comment data should rollback"""
    # Arrange
    use_case = CreatePostWithComments(uow)
    invalid_comments = [
        {"content": "", "author": ""}  # Invalid empty content and author
    ]

    # Act & Assert
    with pytest.raises(ValueError, match="Comment validation failed"):
        await use_case.execute(
            title="Test Post",
            content="Test Content",
            author="Test Author",
            comments_data=invalid_comments
        )
    
    # Verify nothing was saved due to rollback
    posts = await uow.posts.list()
    comments = await uow.comments.list()
    assert len(posts) == 0
    assert len(comments) == 0
    assert uow.rolled_back is True
