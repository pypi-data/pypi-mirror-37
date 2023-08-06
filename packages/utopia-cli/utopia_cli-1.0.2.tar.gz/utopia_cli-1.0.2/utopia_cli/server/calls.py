"""File defining the GraphQL calls to the database."""

import json

import graphcall
from . import utils


def get_last_rev():
    """Get the last non-dev revision of the database."""
    node = graphcall.Node("query")
    (node.addNode("revisions")
        .addEdge("version"))
    result = graphcall.Request(node).send("https://api.utopia-server.com/")
    revisions = [rev["version"] for rev in result["data"]["revisions"]]
    revisions.sort(key=utils.compute_version, reverse=True)
    return revisions[0]


def get_mods(revisions: str):
    """Get the mods from this revisions."""
    node = graphcall.Node("query")
    (node.addNode("revisions")
        .addParameterField("version", revisions)
        .addNode("mods")
        .addEdge("md5")
        .addEdge("url"))
    result = graphcall.Request(node).send("https://api.utopia-server.com/")
    mods = [mod for mod in result["data"]["revisions"][0]["mods"]]
    return mods
