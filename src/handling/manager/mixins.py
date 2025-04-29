from typing import Any


class ContextMixin:
    def __init__(self, *args, context: dict[str, Any] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.context: dict[str, Any] = context or {}

    def get_context(self, name: str) -> Any:
        context_value = self.context.get(name)
        if context_value is None:
            raise KeyError(f"Context {name} not found.")

        return context_value
