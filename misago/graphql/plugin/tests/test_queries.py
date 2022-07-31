import pytest

from ....plugins import PluginsLoader

PLUGINS_QUERY = """
    {
        plugins {
            name
            description
            license
            icon
            color
            version
            author
            homepage {
                domain
                url
            }
            repo {
                domain
                icon
                url
            }
            directory
            admin
            client
        }
    }
"""


@pytest.mark.asyncio
async def test_admin_schema_plugins_query_returns_plugins_list(
    mocker, plugins_root, query_admin_api, admin
):
    plugins_loader = PluginsLoader(plugins_root)
    mocker.patch("misago.graphql.plugin.queries.plugins_loader", plugins_loader)

    result = await query_admin_api(PLUGINS_QUERY)
    assert result["data"]["plugins"]


@pytest.mark.asyncio
async def test_admin_schema_plugins_query_requires_admin_auth(query_admin_api):
    result = await query_admin_api(
        PLUGINS_QUERY,
        expect_error=True,
        include_auth=False,
    )
    assert result["errors"][0]["extensions"]["code"] == "UNAUTHENTICATED"
    assert result["data"] is None