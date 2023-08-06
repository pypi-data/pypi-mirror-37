import asyncio
import importlib
import os
import time
import traceback
from pathlib import Path

from .feature import Feature
from .event_handler import EventHandler
from .bot import Bot
from .logger import Logger
from .typer import Typer


def get_sub_files(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isfile(os.path.join(a_dir, name))]


class FeatureManager(object):

    def __init__(self, bot):
        self.bot: Bot = bot
        self.logger = Logger()
        self.features = {}
        self.loop: asyncio.BaseEventLoop = None
        self.features_dir = 'features/'
        self.events = {
            # 'on_ready': {},
            # 'on_shard_ready': {},
            'on_resumed': {},
            'on_error': {},
            'on_socket_raw_receive': {},
            'on_socket_raw_send': {},
            'on_typing': {},
            'on_message': {},
            'on_message_delete': {},
            'on_raw_message_delete': {},
            'on_raw_bulk_message_delete': {},
            'on_message_edit': {},
            'on_raw_message_edit': {},
            'on_reaction_add': {},
            'on_raw_reaction_add': {},
            'on_reaction_remove': {},
            'on_raw_reaction_remove': {},
            'on_reaction_clear': {},
            'on_raw_reaction_clear': {},
            'on_private_channel_delete': {},
            'on_private_channel_create': {},
            'on_private_channel_update': {},
            'on_private_channel_pins_update': {},
            'on_guild_channel_delete': {},
            'on_guild_channel_create': {},
            'on_guild_channel_update': {},
            'on_guild_channel_pins_update': {},
            'on_member_join': {},
            'on_member_remove': {},
            'on_member_update': {},
            'on_guild_join': {},
            'on_guild_remove': {},
            'on_guild_update': {},
            'on_guild_role_create': {},
            'on_guild_role_delete': {},
            'on_guild_role_update': {},
            'on_guild_emojis_update': {},
            'on_guild_available': {},
            'on_voice_state_update': {},
            'on_member_ban': {},
            'on_member_unban': {},
            'on_group_join': {},
            'on_group_remove': {},
            'on_relationship_add': {},
            'on_relationship_remove': {},
            'on_relationship_update': {}
        }

        for name in self.events:
            event_name = str(name)
            funcs = {}

            exec("""async def {0}(*args, **kwargs):
    await self._call_event("{0}", *args, **kwargs)""".format(event_name), {'self': self}, funcs)

            self.bot.client.event(funcs[event_name])

        self.logger.info("Loaded {} events".format(len(self.events.keys())))
        self.logger.info("Loading features...")

        self.load_all_features()

    async def _call_event(self, event_name, *args, **kwargs):
        canceled = False
        handler: EventHandler = None
        prioritys = sorted(self.events[event_name])
        prioritys.reverse()
        for priority in prioritys:
            for handler in self.events[event_name][priority]:
                if canceled and not handler.ignore_canceled:
                    continue

                try:
                    rtn = await handler.call(*args, **kwargs)

                    if not rtn and rtn is not None:
                        canceled = True
                        break
                except:
                    self.logger.error(
                        'Error passing event "{}" to feature "{}":'.format(event_name, handler.feature.meta['class']))
                    self.logger.error(traceback.format_exc())
        return not canceled

    def define_event(self, event_name: str):
        event_name = event_name.lower().strip()

        if event_name in self.events:
            return

        self.events[event_name] = {}

    def load_all_features(self):
        features_dir = self.features_dir
        for feature_file in get_sub_files(features_dir):
            try:
                self.load_feature(feature_file[:len(feature_file) - 3])
            except Exception as e:
                self.logger.error('Failed to load feature', feature_file)
                self.logger.error(traceback.format_exc())

    def load_feature(self, name):
        name = str(name).lower()
        features_dir = self.features_dir
        feature_file = Path("{}/{}.py".format(features_dir, name))

        if not feature_file.is_file():
            return False

        package = "features"
        module = getattr(__import__(package, fromlist=[name]), name)
        importlib.reload(module)

        Typer.verify_dict({
            'class*': 'str',
            'name*': 'str',
            'description*': 'str',
            'disable': 'bool',
            'threaded': 'bool',
            'depend': 'str[]',
            'softdepend': 'str[]'
        }, module.meta)

        feature: Feature = getattr(module, module.meta['class'])(self, module.meta)
        feature.logger.info('Loaded')
        self.features[module.meta['name']] = feature
        if module.meta['name'] in self.bot.config['features']:
            feature.config = self.bot.config['features'][module.meta['name']]
        feature.on_load()

    def get_feature(self, name):
        if name not in self.features:
            return None
        return self.features[name]

    async def enable_all_features(self):
        self.logger.info("Enabling features...")
        skiped = []
        last_len = 0
        start_time = int(round(time.time() * 1000))

        async def enable(feature_name):
            try:
                feature = self.features[feature_name]
                if 'depends' in feature.meta:
                    for d in feature.meta['depends']:
                        if not self.is_enabled(d):
                            if not feature_name in skiped:
                                skiped.append(feature_name)
                            return False

                if feature.is_enabled():
                    feature.logger.info("Already enabled")
                    if feature_name in skiped:
                        skiped.remove(feature_name)
                    return True

                if feature_name in skiped:
                    skiped.remove(feature_name)

                await feature.enable()
            except Exception:
                self.logger.error('Failed to enable', feature_name)
                self.logger.error(traceback.format_exc())

            return True

        for fn in self.features:
            await enable(fn)

        while last_len != len(skiped):
            last_len = len(skiped)
            for fn in skiped:
                await enable(fn)

        for fn in skiped:
            feature = self.features[fn]
            missing = []
            for d in feature.meta['depends']:
                if not self.is_enabled(d):
                    missing.append(d)

            feature.logger.error('Failed to enable')
            feature.logger.error('Missing one or more dependencies: {}'.format(', '.join(missing)))
        took = int(round(time.time() * 1000)) - start_time
        self.logger.info('Done! ({}ms)'.format(took))

    def can_disable(self, f):
        if not f.is_enabled():
            return False
        if 'threaded' in f.meta:
            if f.meta['threaded']:
                return False
        return True

    def is_enabled(self, name):
        feature: Feature = self.get_feature(name)
        if feature is None:
            return False
        return feature.is_enabled()

    async def disable_all_features(self):
        for feature_name in self.features:
            feature = self.features[feature_name]

            if not feature.is_enabled():
                continue
            if not self.can_disable(feature):
                feature.logger.info("Can't disable")
                continue

            feature.unregister_all_events()
            await feature.disable()

    async def reload_all_features(self):
        self.logger.info("Disabling features...")

        await self.disable_all_features()

        self.logger.info("Reloading features...")

        to_load = []

        for feature_name in list(self.features):
            feature = self.features[feature_name]

            if feature.is_enabled():
                continue

            del self.features[feature_name]
            to_load.append(feature_name)

        for feature_name in to_load:
            self.load_feature(feature_name)

        await self.enable_all_features()

    def on_event(self, feature, event, func, priority=0, ignore_canceled=False):
        if priority not in self.events[event]:
            self.events[event][priority] = []
        handler = EventHandler(feature, event, func, priority, ignore_canceled)
        self.events[event][priority].append(handler)
        return handler

    def event(self, event, priority=0, ignore_canceled=False):
        def add(func):
            self.on_event(event, func, priority=priority, ignore_canceled=ignore_canceled)

        return add

    def _call_event_sync(self, event_name, *args, **kwargs):
        caller = self._call_event(event_name, *args, **kwargs)

        return self.loop.create_task(caller)
