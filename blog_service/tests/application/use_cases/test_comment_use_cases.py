import pytest
from uuid import uuid4
from application.use_cases.comment.create_comment import CreateComment
from application.use_cases.comment.delete_comment import DeleteComment
from application.use_cases.comment.get_post_comments import GetPostComments

pytestmark = pytest.mark.asyncio

class TestCreateComment:
    async def test_create_comment(self, uow, sample_post):
        # Arrange
        await uow.posts.add(sample_post)
        use_case = CreateComment(uow)

        # Act
        comment = await use_case.execute(
            post_id=sample_post.id,
            content="Test Comment",
            author="Test Commenter"
        )

        # Assert
        assert comment.content == "Test Comment"
        assert comment.author == "Test Commenter"
        assert comment.post_id == sample_post.id
        assert uow.committed is True

    async def test_create_comment_non_existing_post(self, uow):
        # Arrange
        use_case = CreateComment(uow)
        non_existing_id = uuid4()

        # Act & Assert
        with pytest.raises(ValueError, match="Post not found"):
            await use_case.execute(
                post_id=non_existing_id,
                content="Test Comment",
                author="Test Commenter"
            )

class TestGetPostComments:
    async def test_get_post_comments(self, uow, sample_post, sample_comment):
        # Arrange
        await uow.posts.add(sample_post)
        await uow.comments.add(sample_comment)
        use_case = GetPostComments(uow)

        # Act
        comments = await use_case.execute(sample_post.id)

        # Assert
        assert len(comments) == 1
        assert comments[0] == sample_comment

    async def test_get_comments_non_existing_post(self, uow):
        # Arrange
        use_case = GetPostComments(uow)
        non_existing_id = uuid4()

        # Act
        comments = await use_case.execute(non_existing_id)

        # Assert
        assert len(comments) == 0

    async def test_get_comments_empty_post(self, uow, sample_post):
        # Arrange
        await uow.posts.add(sample_post)
        use_case = GetPostComments(uow)

        # Act
        comments = await use_case.execute(sample_post.id)

        # Assert
        assert len(comments) == 0

class TestDeleteComment:
    async def test_delete_existing_comment(self, uow, sample_post, sample_comment):
        # Arrange
        await uow.posts.add(sample_post)
        await uow.comments.add(sample_comment)
        use_case = DeleteComment(uow)

        # Act
        await use_case.execute(sample_comment.id)

        # Assert
        deleted_comment = await uow.comments.get(sample_comment.id)
        assert deleted_comment is None
        assert uow.committed is True

    async def test_delete_non_existing_comment(self, uow):
        # Arrange
        use_case = DeleteComment(uow)
        non_existing_id = uuid4()

        # Act
        await use_case.execute(non_existing_id)

        # Assert
        assert uow.committed is True  # Should commit even if comment doesn't exist
