```mermaid
classDiagram

    class SuperHero{
        +name: str
        +superpowers: list
    }

    class SuperGroup{
        #name: str
        #location: str
        #members: list
        +get_name(): str
        +get_location(): str
        +add_member()
        +print_group()
    }

    SuperHero o-- SuperGroup

```