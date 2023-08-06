class Feature(object):
    """
    A feature is, well, a feature. Features loaded when the program is loaded and enabled when the bot is ready
    """

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
        """
        Attempt to enable the feature
        """
        if 'disable' in self.meta:
            if self.meta['disable']:
                return
        if self.is_enabled():
            return
        await self.on_enable()
        self.logger.info('Enabled')
        self._enabled = True

    async def disable(self):
        """
        Attempt to disable the feature
        :return:
        """
        if not self.is_enabled():
            return
        if 'threaded' in self.meta:
            if self.meta['threaded']:
                return
        await self.on_disable()
        self.logger.info('Disabled')
        self._enabled = False

    def is_enabled(self):
        """
        Get weather the feature is enabled
        :return: boolean
        """
        return self._enabled

    def on_event(self, event, func, priority=0, ignore_canceled=False):
        """
        Add an event handler
        :param event: Name of the event
        :param func: Function to be called when the event is called
        :param priority: Priority of event, higher numbers will be called first
        :param ignore_canceled: Ignore the event if it is canceled before the listener can be called
        :return: The event handler
        """
        event = self.feature_manager.on_event(self, event, func, priority=priority, ignore_canceled=ignore_canceled)
        self.events.append(event)
        return event

    def unregister_all_events(self):
        """
        Unregister all events associated with this feature. This is called when the feature is disabled.
        :return:
        """
        for event in self.events:
            event.unregister(self.feature_manager.events)
        self.events = []

    # defaults
    def on_load(self):
        """
        Called when the feature is loaded

        Note: Do not attempt to get other features in this method as they might not be loaded
        """
        pass

    async def on_enable(self):
        """
        Called when the feature is enabled
        """
        pass

    async def on_disable(self):
        """
        Called when the feature is disabled
        """
        pass
