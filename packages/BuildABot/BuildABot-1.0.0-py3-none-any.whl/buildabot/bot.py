import asyncio
import json
import time

import discord

from . import utils as u


class Bot(object):
    """Hi"""
    instance = None

    def __init__(self, config=None):
        from .feature_manager import FeatureManager
        if Bot.instance is not None:
            raise ValueError('Bot already started')
        if config is None:
            config = 'config.json'
        self.client = discord.Client()
        self.start_time = 0
        self.discord_token = ''
        self.config: dict = config
        self.feature_manager: FeatureManager = FeatureManager(self)
        self.logger = self.feature_manager.logger
        Bot.instance = self

        if isinstance(self.config, str):
            self.config = json.load(open(self.config))
        if not isinstance(self.config, dict):
            raise TypeError('Invalid config type')

    async def on_ready(self):
        time_took = int(round(time.time() * 1000)) - self.start_time

        self.logger.info('Ready! ({}ms)'.format(time_took))
        self.logger.debug('Logged in as: {} ({})'.format(self.client.user.name, self.client.user.id))
        u.loop = asyncio.get_event_loop()
        self.feature_manager.loop = asyncio.get_event_loop()

        await self.feature_manager.enable_all_features()

    def run(self):
        self.client.event(self.on_ready)
        self.start_time = int(round(time.time() * 1000))
        self.client.run(self.config['apis']['discord']['token'])
