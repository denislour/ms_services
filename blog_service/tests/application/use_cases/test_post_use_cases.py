import pytest
from uuid import uuid4
from application.use_cases.post.create_post_with_comments import CreatePostWithComments
from application.use_cases.post.delete_post import DeletePost
from application.use_cases.post.get_post import GetPost
from application.use_cases.post.list_posts import ListPosts
from application.use_cases.post.update_post import UpdatePost
from domain.value_objects.post_status import PostStatus

pytestmark = pytest.mark.asyncio

class TestCreatePostWithComments:
    async def test_create_post_with_comments(self, uow):
        # Arrange
        use_case = CreatePostWithComments(uow)
        comments_data = [
            {"content": "Comment 1", "author": "Commenter 1"},
            {"content": "Comment 2", "author": "Commenter 2"}
        ]

        # Act
        post, comments = await use_case.execute(
            title="Test Post",
            content="Test Content",
            author="Test Author",
            comments_data=comments_data
        )

        # Assert
        assert post.title == "Test Post"
        assert post.content == "Test Content"
        assert post.author == "Test Author"
        assert len(comments) == 2
        assert all(comment.post_id == post.id for comment in comments)
        assert uow.committed is True

class TestGetPost:
    async def test_get_existing_post(self, uow, sample_post):
        # Arrange
        await uow.posts.add(sample_post)
        use_case = GetPost(uow)

        # Act
        result = await use_case.execute(sample_post.id)

        # Assert
        assert result == sample_post

    async def test_get_non_existing_post(self, uow):
        # Arrange
        use_case = GetPost(uow)
        non_existing_id = uuid4()

        # Act
        result = await use_case.execute(non_existing_id)

        # Assert
        assert result is None

class TestListPosts:
    async def test_list_posts(self, uow, sample_post):
        # Arrange
        await uow.posts.add(sample_post)
        use_case = ListPosts(uow)

        # Act
        posts = await use_case.execute()

        # Assert
        assert len(posts) == 1
        assert posts[0] == sample_post

    async def test_list_empty_posts(self, uow):
        # Arrange
        use_case = ListPosts(uow)

        # Act
        posts = await use_case.execute()

        # Assert
        assert len(posts) == 0

class TestUpdatePost:
    async def test_update_existing_post(self, uow, sample_post):
        # Arrange
        await uow.posts.add(sample_post)
        use_case = UpdatePost(uow)

        # Act
        updated_post = await use_case.execute(
            post_id=sample_post.id,
            title="Updated Title",
            content="Updated Content"
        )

        # Assert
        assert updated_post.title == "Updated Title"
        assert updated_post.content == "Updated Content"
        assert updated_post.id == sample_post.id
        assert uow.committed is True

    async def test_update_non_existing_post(self, uow):
        # Arrange
        use_case = UpdatePost(uow)
        non_existing_id = uuid4()

        # Act
        result = await use_case.execute(
            post_id=non_existing_id,
            title="Updated Title",
            content="Updated Content"
        )

        # Assert
        assert result is None

class TestDeletePost:
    async def test_delete_existing_post(self, uow, sample_post):
        # Arrange
        await uow.posts.add(sample_post)
        use_case = DeletePost(uow)

        # Act
        await use_case.execute(sample_post.id)

        # Assert
        deleted_post = await uow.posts.get(sample_post.id)
        assert deleted_post is None
        assert uow.committed is True

    async def test_delete_non_existing_post(self, uow):
        # Arrange
        use_case = DeletePost(uow)
        non_existing_id = uuid4()

        # Act
        await use_case.execute(non_existing_id)

        # Assert
        assert uow.committed is True  # Should commit even if post doesn't exist
