# Simple observer pattern implementation
subscribers = dict()

def subscribe(event_type: str,function):
    if not event_type in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(function)

def post_event(event_type: str, data):
    if not event_type in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(data)