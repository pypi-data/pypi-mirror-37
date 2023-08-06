import asyncio
import importlib
import json
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
    """
    Get all files in a directory
    :param a_dir: Directory to search
    :return: List of files in directory
    """
    return [name for name in os.listdir(a_dir)
            if os.path.isfile(os.path.join(a_dir, name))]


def get_sub_fd(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isfile(os.path.join(a_dir, name)) or os.path.isdir(os.path.join(a_dir, name))]


class FeatureManager(object):
    """
    The FeatureManager handles the loading, enabling and reloading of features and all events.
    """

    def __init__(self, bot, features_dir=None):
        self.bot: Bot = bot
        self.logger = Logger()
        self.features = {}
        self.loop: asyncio.BaseEventLoop = None
        self.features_dir = features_dir
        if self.features_dir is None:
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
        """
        Call an event
        :param event_name: Name of the event, it must be already defined
        :param args: Arguments to be sent to the event
        :param kwargs: Named arguments to be sent to the event
        :return: true if canceled
        """
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
        """
        Define an event
        :param event_name: Name of the event
        :return: None
        """
        event_name = event_name.lower().strip()

        if event_name in self.events:
            return

        self.events[event_name] = {}

    def load_all_features(self):
        """
        Load every available feature
        :return: None
        """
        features_dir = self.features_dir
        for feature_file in get_sub_fd(features_dir):
            try:
                if feature_file.endswith(".py"):
                    feature_file = feature_file[:len(feature_file) - 3]
                f = self.load_feature(feature_file)
                if not f:
                    self.logger.error('Invalid feature', feature_file)
            except Exception as e:
                self.logger.error('Failed to load feature', feature_file)
                self.logger.error(traceback.format_exc())

    def load_feature(self, name):
        """
        Load a feature. Each feature is automatically loaded when `load_all_features` is called.
        :param name: Name of the feature
        :return: The feature
        """
        name = str(name).lower()
        features_dir = self.features_dir

        template = {
            'main': 'str',
            'class*': 'str',
            'name*': 'str',
            'description*': 'str',
            'disable': 'bool',
            'threaded': 'bool',
            'depends': 'str[]',
            'softdepends': 'str[]'
        }

        package = "features"
        if Path("{}/{}.py".format(features_dir, name)).is_file():
            module = getattr(__import__(package, fromlist=[name]), name)
            meta = module.meta

            Typer.verify_dict(template, meta)
        elif Path("{}/{}".format(features_dir, name)).is_dir():
            feature_meta_file = Path("{}/{}/feature.json".format(features_dir, name))
            if not feature_meta_file.is_file():
                return False
            meta = json.load(feature_meta_file.open(mode='r'))

            Typer.verify_dict(template, meta)

            split: list = meta['class'].split('.')
            main = split[-1]
            package = '{}.{}.{}'.format(package, name, '.'.join(split[0:-1])).strip('.')
            module = __import__(package, fromlist=[main])
        else:
            return False

        importlib.reload(module)

        feature: Feature = getattr(module, meta['class'].split('.')[-1])(self, meta)
        feature.logger.info('Loaded')
        self.features[meta['name']] = feature
        if meta['name'] in self.bot.config['features']:
            feature.config = self.bot.config['features'][meta['name']]
        feature.on_load()
        return feature

    def get_feature(self, name):
        """
        Get a feature
        :param name: Name of the feature
        :return: The feature object
        """
        if name not in self.features:
            return None
        return self.features[name]

    async def enable_all_features(self):
        """
        Attempts to enable all features. This is automatically called when the bot is ready
        :return:
        """
        self.logger.info("Enabling features...")
        skiped = []
        last_len = 0
        start_time = int(round(time.time() * 1000))

        async def enable(feature_name, force=False):
            try:
                feature = self.features[feature_name]
                if not force:
                    if 'depends' in feature.meta:
                        for d in feature.meta['depends']:
                            if not self.is_enabled(d):
                                if not feature_name in skiped:
                                    skiped.append(feature_name)
                                return False
                    if 'softdepends' in feature.meta:
                        for d in feature.meta['softdepends']:
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
            if 'depends' in feature.meta:
                for d in feature.meta['depends']:
                    if not self.is_enabled(d):
                        missing.append(d)

            if len(missing) > 0:
                feature.logger.error('Failed to enable')
                feature.logger.error('Missing one or more dependencies: {}'.format(', '.join(missing)))
            else:
                await enable(fn, force=True)
        took = int(round(time.time() * 1000)) - start_time
        self.logger.info('Done! ({}ms)'.format(took))

    def can_disable(self, f):
        """
        Checks to see if a feature is able to be disabled.
        This commonly occurs if the feature is already disabled or has enabled "threaded" in its meta.
        :param f: The feature object
        :return:
        """
        if not f.is_enabled():
            return False
        if 'threaded' in f.meta:
            if f.meta['threaded']:
                return False
        return True

    def is_enabled(self, name):
        """
        Check if a feature is enabled
        :param name: Name of the feature
        :return: True if the named feature is enabled
        """
        feature: Feature = self.get_feature(name)
        if feature is None:
            return False
        return feature.is_enabled()

    async def disable_all_features(self):
        """
        Disable all features
        :return: None
        """
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
        """
        Attempts to disable, reload and re-enable all features
        :return: None
        """
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
        """
        Add an event handler
        :param feature: The feature associated with the handler
        :param event: Name of the event
        :param func: function to be called
        :param priority: Priority of event, higher numbers will be called first
        :param ignore_canceled: Ignore the event if it is canceled before the listener can be called
        :return: The event handler
        """
        if priority not in self.events[event]:
            self.events[event][priority] = []
        handler = EventHandler(feature, event, func, priority, ignore_canceled)
        self.events[event][priority].append(handler)
        return handler

    def event(self, event, priority=0, ignore_canceled=False):
        """
        Add an event handler
        :param event: Name of the event
        :param priority: Priority of event, higher numbers will be called first
        :param ignore_canceled: Ignore the event if it is canceled before the listener can be called
        :return: The event handler
        """

        def add(func):
            self.on_event(event, func, priority=priority, ignore_canceled=ignore_canceled)

        return add

    def _call_event_sync(self, event_name, *args, **kwargs):
        """
        Call an event in sync
        :param event_name: Name of the event, it must be already defined
        :param args: Arguments to be sent to the event
        :param kwargs: Named arguments to be sent to the event
        :return: true if canceled
        """
        caller = self._call_event(event_name, *args, **kwargs)

        return self.loop.create_task(caller)
