```mermaid
classDiagram

    class SimpleDate{
        +day: int
        +month: int
        +year: int
        +__eq__() Bool
        +__gt__() Bool
        +__add__() SimpleDate
        +__sub__() int
    }

```