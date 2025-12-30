
class EventManager:
    """
    A class to manage event subscriptions and posting.
    """
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: str, function):
        """
        Subscribe a function to an event type.
        """
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(function)

    def post_event(self, event_type: str, data):
        """
        Post an event, notifying all subscribers.
        """
        if event_type not in self.subscribers:
            return
        for fn in self.subscribers[event_type]:
            fn(data)

# Global instance for now, to ease transition or for singleton usage
event_manager = EventManager()
