class _Immutable:
    """A base class that prevents modification of its attributes."""
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise ValueError(f"Cannot change a value of a constant '{name}'")
        super().__setattr__(name, value)

class CONSTANTS(_Immutable):
    tool_name: str = "null-value-inspector"
    alias: str = "nvi"