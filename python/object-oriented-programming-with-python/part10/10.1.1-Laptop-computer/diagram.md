```mermaid
classDiagram

    class Computer{
        +model: str
        +speed: int
    }

    class LaptopComputer{
        +weight: int
    }

    Computer <|--  LaptopComputer

```
