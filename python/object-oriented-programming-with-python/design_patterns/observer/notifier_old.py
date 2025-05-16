class Subject:
    def __init__(self):
        self._state = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self._notify()

    def _notify(self):
        # Calling consumer functions directly
        hex_print(self._state)
        binary_print(self._state)

def hex_print(state):
    print(f'State in hex: {state:x}')

def binary_print(state):
    print(f'State in binary: {state:b}')

# Example usage
subject = Subject()
subject.state = 12
# This will invoke the consumer functions to print the state in hex and binary


