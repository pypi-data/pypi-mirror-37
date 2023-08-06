class EventObject (object) :

    def __init__(self) :
        super(EventObject, self).__init__()
        self.listeners = {}

    def on(self, ev, f) :
        if not ev in self.listeners :
            self.listeners[ev] = []
        self.listeners[ev].append(f)

    def trigger(self, ev, event_object) :
        listeners = self.listeners[ev] if ev in self.listeners else []
        for f in listeners :
            f(self, event_object)
