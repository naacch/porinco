import logging
from typing import Any

from .node import Node

logger = logging.getLogger(__name__)


class MissingDependencyError(Exception): ...


class Pipeline:

    def __init__(
        self,
        nodes: list[Node] | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        self._nodes: list[Node] = list(nodes) if nodes is not None else []
        self._context: dict[str, Any] = dict(context) if context is not None else {}

    def __getitem__(self, key: str) -> Any:
        return self._context[key]

    @property
    def available(self) -> set[str]:
        return set(self._context.keys())

    def add_node(self, node: Node) -> None:
        self._nodes.append(node)

    def provide(self, name: str, value: Any) -> None:
        self._context[name] = value

    def _resolve_node_dependencies(self, node: Node) -> dict[str, Any]:
        missing = set(node.dependencies) - self.available
        if missing:
            raise MissingDependencyError(
                f"Node '{node.name}' is missing dependencies: {sorted(missing)}"
            )

        return {name: self._context[name] for name in node.dependencies}

    def execute(self) -> None:
        for node in self._nodes:
            # NOTE: missing dependencies indicate an invalid pipeline definition,
            # not a recoverable runtime error, so execution should fail fast.
            dependencies = self._resolve_node_dependencies(node)

            try:
                result = node.operation(**dependencies)
            except Exception:
                logger.exception("Node '%s' failed", node.name)
                raise

            self._context[node.provides] = result
