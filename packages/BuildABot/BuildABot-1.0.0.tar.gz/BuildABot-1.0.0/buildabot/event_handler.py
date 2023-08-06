import asyncio


class EventHandler(object):

    def __init__(self, feature, event_name, func, priority, ignore_canceled):
        from .feature import Feature
        self.feature: Feature = feature
        self.event_name: str = event_name
        self.func: asyncio.coroutine = func
        self.priority: int = priority
        self.ignore_canceled: bool = ignore_canceled
        self.registered = True

    def unregister(self, events):
        event_copy = dict(events)
        for event_name in event_copy:
            prioritys = events[event_name]
            for priority_index in prioritys:
                priority = prioritys[priority_index]
                for handler in priority:
                    if self == handler:
                        events[event_name][priority_index].remove(handler)
        self.registered = False

    async def call(self, *args, **kwargs):
        if not self.registered:
            return True
        return await self.func(*args, **kwargs)
