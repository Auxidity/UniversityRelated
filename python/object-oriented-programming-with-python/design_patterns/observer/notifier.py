class Subject:
    def __init__(self):
        self._observers = []
        self._state = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self._notify()

    def attach(self,observer):
        self._observers.append(observer)

    def detach(self,observer):
        self._observers.remove(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self)

class Observer:
    def update(self, subject):
        pass

class HexSystem(Observer):
    def update(self, subject):
        print(f'State in hex: {subject.state:x}')

class BinarySystem(Observer):
    def update(self, subject):
        print(f'State in binary: {subject.state:b}')





# Example usage
subject = Subject()
hex_observer = HexSystem()
bin_observer = BinarySystem()

subject.attach(hex_observer)
subject.attach(bin_observer)

#Prints the state on attached components
subject.state = 12


