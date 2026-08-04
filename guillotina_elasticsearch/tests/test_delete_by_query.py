from guillotina_elasticsearch.exceptions import ElasticsearchConflictException
from guillotina_elasticsearch.exceptions import QueryErrorException
from guillotina_elasticsearch.utility import ElasticSearchUtility
from unittest.mock import AsyncMock

import pytest


pytestmark = [pytest.mark.asyncio]

PATH_QUERY = {"query": {"bool": {"must": []}}}


def make_utility(responses):
    utility = ElasticSearchUtility()
    conn = AsyncMock()
    conn.delete_by_query = AsyncMock(side_effect=responses)
    utility.get_connection = lambda: conn
    return utility, conn


async def test_delete_by_query_returns_deleted_count():
    utility, conn = make_utility([{"deleted": 3, "version_conflicts": 0}])
    result = await utility._delete_by_query(PATH_QUERY, "idx")
    assert result == {"deleted": 3}
    assert conn.delete_by_query.await_count == 1
    kwargs = conn.delete_by_query.await_args.kwargs
    assert kwargs["conflicts"] == "proceed"
    assert kwargs["requests_per_second"] == -1


async def test_delete_by_query_reruns_on_version_conflicts():
    utility, conn = make_utility(
        [
            {"deleted": 10, "version_conflicts": 2},
            {"deleted": 2, "version_conflicts": 0},
        ]
    )
    result = await utility._delete_by_query(PATH_QUERY, "idx")
    assert result == {"deleted": 12}
    assert conn.delete_by_query.await_count == 2


async def test_delete_by_query_raises_when_conflicts_persist():
    utility, conn = make_utility([{"deleted": 1, "version_conflicts": 3}] * 5)
    with pytest.raises(ElasticsearchConflictException):
        await utility._delete_by_query(PATH_QUERY, "idx")
    assert conn.delete_by_query.await_count == 5


async def test_delete_by_query_raises_on_failures():
    utility, conn = make_utility(
        [
            {
                "deleted": 1,
                "version_conflicts": 0,
                "failures": [{"status": 429, "cause": {"reason": "rejected"}}],
            }
        ]
    )
    with pytest.raises(QueryErrorException):
        await utility._delete_by_query(PATH_QUERY, "idx")
