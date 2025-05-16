```mermaid
classDiagram

    class Money{
        -euros: int
        -cents: int
        +__eq__() bool
        +__gt__() bool
        +__add__()Money
        +__sub__()Money
    }

```