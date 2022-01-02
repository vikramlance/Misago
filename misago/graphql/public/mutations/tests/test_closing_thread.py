import pytest

from .....errors import ErrorsList
from ..closethread import resolve_close_thread


CLOSE_THREAD_MUTATION = """
    mutation CloseThread($input: CloseThreadInput!) {
        closeThread(input: $input) {
            thread {
                id
                isClosed
            }
            errors {
                location
                type
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_close_thread_mutation_closes_thread(query_public_api, moderator, thread):
    result = await query_public_api(
        CLOSE_THREAD_MUTATION,
        {"input": {"thread": str(thread.id), "isClosed": True}},
        auth=moderator,
    )

    assert result["data"]["closeThread"] == {
        "thread": {
            "id": str(thread.id),
            "isClosed": True,
        },
        "errors": None,
    }

    thread_from_db = await thread.refresh_from_db()
    assert thread_from_db.is_closed


@pytest.mark.asyncio
async def test_close_thread_mutation_opens_thread(
    query_public_api, moderator, closed_thread
):
    result = await query_public_api(
        CLOSE_THREAD_MUTATION,
        {"input": {"thread": str(closed_thread.id), "isClosed": False}},
        auth=moderator,
    )

    assert result["data"]["closeThread"] == {
        "thread": {
            "id": str(closed_thread.id),
            "isClosed": False,
        },
        "errors": None,
    }

    thread_from_db = await closed_thread.refresh_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_close_thread_mutation_fails_if_user_is_not_authorized(
    query_public_api, thread
):
    result = await query_public_api(
        CLOSE_THREAD_MUTATION,
        {"input": {"thread": str(thread.id), "isClosed": True}},
    )

    assert result["data"]["closeThread"] == {
        "thread": {
            "id": str(thread.id),
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["thread"],
                "type": "auth_error.not_moderator",
            },
            {
                "location": [ErrorsList.ROOT_LOCATION],
                "type": "auth_error.not_authorized",
            },
        ],
    }

    thread_from_db = await thread.refresh_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_close_thread_mutation_fails_if_user_is_not_moderator(
    query_public_api, user, thread
):
    result = await query_public_api(
        CLOSE_THREAD_MUTATION,
        {"input": {"thread": str(thread.id), "isClosed": True}},
        auth=user,
    )

    assert result["data"]["closeThread"] == {
        "thread": {
            "id": str(thread.id),
            "isClosed": False,
        },
        "errors": [
            {
                "location": ["thread"],
                "type": "auth_error.not_moderator",
            },
        ],
    }

    thread_from_db = await thread.refresh_from_db()
    assert not thread_from_db.is_closed


@pytest.mark.asyncio
async def test_close_thread_mutation_fails_if_thread_id_is_invalid(
    query_public_api,
    moderator,
):
    result = await query_public_api(
        CLOSE_THREAD_MUTATION,
        {"input": {"thread": "invalid", "isClosed": True}},
        auth=moderator,
    )

    assert result["data"]["closeThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["thread"],
                "type": "type_error.integer",
            },
        ],
    }


@pytest.mark.asyncio
async def test_close_thread_mutation_fails_if_thread_doesnt_exist(
    query_public_api,
    moderator,
):
    result = await query_public_api(
        CLOSE_THREAD_MUTATION,
        {"input": {"thread": "4000", "isClosed": True}},
        auth=moderator,
    )

    assert result["data"]["closeThread"] == {
        "thread": None,
        "errors": [
            {
                "location": ["thread"],
                "type": "value_error.thread.not_exists",
            },
        ],
    }
