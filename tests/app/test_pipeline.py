import re

import pytest

from porinco.app.node import Node
from porinco.app.pipeline import MissingDependencyError, Pipeline


def test_execute_runs_node_and_stores_output():
    node = Node(
        name="foo", operation=lambda bar: bar**2, dependencies=("bar",), provides="baz"
    )
    pipeline = Pipeline(nodes=[node], context={"bar": 2})
    pipeline.execute()
    assert pipeline["baz"] == 4


def test_execute_raises_when_dependency_is_missing():
    node = Node(
        name="foo",
        operation=lambda bar, foo: bar**foo,
        dependencies=("bar", "foo"),
        provides="baz",
    )
    pipeline = Pipeline(nodes=[node])

    with pytest.raises(
        MissingDependencyError,
        match=re.escape("Node 'foo' is missing dependencies: ['bar', 'foo']"),
    ):
        pipeline.execute()


def test_execute_runs_multiple_nodes_in_order():
    nodes = [
        Node(
            name="foo",
            operation=lambda bar: bar**2,
            dependencies=("bar",),
            provides="baz",
        ),
        Node(
            name="bar",
            operation=lambda baz: baz**baz,
            dependencies=("baz",),
            provides="foo",
        ),
    ]

    pipeline = Pipeline(nodes=nodes, context={"bar": 2})
    pipeline.execute()

    assert pipeline["foo"] == 256


def test_execute_stops_when_node_fails():
    nodes = [
        Node(
            name="foo",
            operation=lambda bar: bar / 0,
            dependencies=("bar",),
            provides="baz",
        ),
        Node(
            name="bar",
            operation=lambda baz: baz / 1,
            dependencies=("baz",),
            provides="foo",
        ),
    ]

    pipeline = Pipeline(nodes=nodes, context={"bar": 2})

    with pytest.raises(ZeroDivisionError):
        pipeline.execute()

    assert "baz" not in pipeline.available
    assert "foo" not in pipeline.available


def test_provide_makes_value_available():
    pipeline = Pipeline()

    pipeline.provide("bar", 2)

    assert pipeline["bar"] == 2
