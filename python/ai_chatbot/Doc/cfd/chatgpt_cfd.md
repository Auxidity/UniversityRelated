


## ask_chatgpt()
```mermaid
graph TD

A[Execution call from main] -->B[Config script for language]
B --> C[STT Module] --> D[STT Parser for keyword]
D-->|No keyword found on language|B
D-->|Keyword found on Language|E[Config script for target age group]
E-->C[STT Module]
D-->|No Keyword found for age group|E
D-->|Keyword found on age group|F[Save configs for the chatgpt prompts]
F-->C
C-->|Write logs|L[Debug logs]
C-->I[Parse the question from STT Module to text format and speak outloud chatgpt answer]

I-->G[Another question prompt using same config]
G-->C

D-->|Additional question keyword match|C
D-->|Keyword to not ask questions using same config. Check previous script state to not accidentally exit|H[Exit to main]

```

Additional feature on every step:

Timeout on every function call, if met break current & call exit to main

Potentially create this as FSM.

## Feedback variant for visual clarity
```mermaid
graph TD

A[Execution call from main] -->B[Config script for language]
B --> C[STT Module] --> D[STT Parser for keyword]
D-->|No keyword found on language|B
D-->|Keyword found on Language|E[Config script for target age group]
E-->F[STT Module]
F-->G[STT Parser for keyword]
G-->|No Keyword found on age group|E
G-->H[Save Config for chatgpt prompt]
H-->J[STT Module]
J-->I[Parse the speech as question to chatgpt and speak outloud the answer]
I-->K[Additional question?]
K-->L[STT Module]
L-->M[STT Parser for keyword]
M-->|Keyword found for additional questions|J
M-->|Keyword for exit|N[Exit to main]
```