class Feature(object):

    def __init__(self, feature_manager, meta: dict):
        from buildabot import Bot, FeatureManager, Logger
        self.feature_manager: FeatureManager = feature_manager
        self.bot: Bot = feature_manager.bot
        self.meta: dict = meta
        self._enabled = False
        self.logger = Logger(feature=self)
        self.events = []
        self.config = {}

    async def enable(self):
        if 'disable' in self.meta:
            if self.meta['disable']:
                return
        if self.is_enabled():
            return
        await self.on_enable()
        self.logger.info('Enabled')
        self._enabled = True

    async def disable(self):
        if not self.is_enabled():
            return
        if 'threaded' in self.meta:
            if self.meta['threaded']:
                return
        await self.on_disable()
        self.logger.info('Disabled')
        self._enabled = False

    def is_enabled(self):
        return self._enabled

    def on_event(self, event, func, priority=0, ignore_canceled=False):
        event = self.feature_manager.on_event(self, event, func, priority=priority, ignore_canceled=ignore_canceled)
        self.events.append(event)
        return event

    def unregister_all_events(self):
        for event in self.events:
            event.unregister(self.feature_manager.events)
        self.events = []

    # defaults
    def on_load(self):
        pass

    async def on_enable(self):
        pass

    async def on_disable(self):
        pass
