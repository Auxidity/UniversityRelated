

```mermaid
stateDiagram-v2 
    direction LR
    [*] --> Idle
    Idle --> [*] : Buffer contains "exit" or "quit"
    Idle --> Reddit : Buffer contains "reddit", entering Reddit module
    Idle --> Idle : Buffer doesn't contain any matching keywords
    Idle --> Telegram : Buffer contains "telegram", entering Telegram module
    Reddit --> Idle : User wishes to exit out of the module back to idle
    Telegram --> Idle : User wishes to exit out of the module back to idle
```

```mermaid
stateDiagram-v2
    direction TB
    state if_state <<choice>>
    note left of if_state
    Check if search terms have been specified
    end note
    A: Reddit Module Main State 

    B: Keyword Search
    note left of B
    User specifies keywords that they wish to search with
    end note

    C: Subreddit Search
    note right of C
    User specifies subreddits that they wish to search from
    end note

    D: Confirmation
    note left of D
    User specifies if they wish to stay in Reddit module after a search is performed
    end note


    
    F: Reddit Module Main State

    state "Reddit Flow" as Flow{
    
        [*] --> A
        A --> if_state
        if_state --> B : No search terms are present
        if_state --> D : Search is performed and displayed using search terms
        B --> C
        C --> F
        D --> [*] : User wishes to exit
        D --> F : User wishes to stay in module, previous search terms are removed from memory
        F --> if_state 
    }
    
```

```mermaid
stateDiagram-v2
    direction BT
    state "State Flow" as Flow{
    [*] --> run_pre_transition : on_message event occurs
    run_pre_transition --> handle_transition

    note left of run_pre_transition
    State specific pre-transition tasks are executed here
    end note

    note right of handle_transition
    State specific logic for determining what state to end at is handled here
    end note
    handle_transition --> [*]
    }    

```

```mermaid
stateDiagram-v2
    direction TB

    A: Telegram Initial State
    note left of A
    The need for authentication is checked
    end note

    B: Telegram Main State
    note left of B
    Buffer is searched for keywords to determine which action to perform
    end note
    C: Telegram Authentication

    D: Telegram Search
    note left of D
    User specifies who is the target of chosen operation
    end note

    E: Telegram History
    note left of E
    User is shown previous message history with specified target
    end note

    F: Telegram Message
    note right of F
    User specifies what message to send
    end note

    state if_state1 <<choice>>
    state if_state2 <<choice>>

    state "Telegram Flow" as Flow{
        [*] --> A   
        A --> if_state1
        if_state1 --> C: Authentication neccesary
        if_state1 --> B: Authentication not neccesary
        C --> A
        B --> D
        D --> if_state2
        if_state2 --> B : Search action
        if_state2 --> E : History action
        if_state2 --> F : Message action
        E --> B
        F --> B
        B --> [*]: User wishes to exit out from Telegram module
    }
```

```mermaid
flowchart TD
    linkStyle default stroke:#baa,stroke-width:4px,color:olive;



    subgraph ModuleA[FSM]
        A1[State Machine]
        A2[Reddit Module]
        A3[Telegram Module]
    end

    subgraph ModuleB[GUI / CLI]
        B1[State Synchronizer]
        B2[User Input]
    end

    subgraph ModuleC[Speech Module]
        C1[Controller]
        C2[Speech Recognition]
    end

    
    A1 -- MQTT --> A2
    A1 -- MQTT --> A3
    A1 -- File I/O --> C1
    A1 -- File I/O --> B1
    A2 -- MQTT --> A1
    A3 -- MQTT --> A1
    A1 -- MQTT --> B1
    B2 -- MQTT --> A1
    C2 -- MQTT --> A1
    A2 -- MQTT --> B1
    A3 -- MQTT --> B1
    C1 -- File I/O --> C2

    linkStyle 2,3,11 stroke:#baa,stroke-width:4px,color:green;

    classDef moduleStyle fill:#fff,stroke:#000,stroke-width:4px,color:black,font-size:20px,font-weight:bold;

    classDef submoduleStyle fill:#ccc,stroke:#000,stroke-width:1px,color:black,font-size:14px;


    class ModuleA moduleStyle;
    class ModuleB moduleStyle;
    class ModuleC moduleStyle;
    class A1,A2,A3,B1,B2,C1,C2 submoduleStyle;
```

- Functional Requirements
  - Speech Interface
  - Visual, Auditory or Audiovisual User Feedback
  - GUI or CLI

- Non-Functional Requiremens
  - Privacy
  - Performance
  - Security
  - Locality
  - Extensibility
  - Maintainability
  - Portability
  - Developer Experience

- Technical Requirements
  - Hardware Components
  - System Architecture
  - Platform Integration
  - Development Tools