import asyncio
import json
import logging
import os
import sys
import time

import discord

import utils as u
from .feature_manager import Logger, FeatureManager

workshop = None
ready = False
fm = Logger()


def start():
    global workshop
    global ready
    global fm
    asyncio.set_event_loop(asyncio.new_event_loop())
    sk_start_time = int(round(time.time() * 1000))

    client = discord.Client()

    # When bot is ready

    @client.event
    async def on_ready():
        global fm
        global ready
        time_took = int(round(time.time() * 1000)) - sk_start_time
        if workshop.config['logging']['channel'] is not None:
            workshop.log_channel = workshop.client.get_channel(workshop.config['logging']['channel'])

        fm.logger.info('Ready! ({}ms)'.format(time_took))
        fm.logger.debug('Logged in as: {} ({})'.format(client.user.name, client.user.id))

        if workshop.log_channel is not None:
            await u.log(workshop, {
                'Start Time': u.format_ms_time(sk_start_time),
                'Ready At': u.format_ms_time(sk_start_time + time_took),
                'PID': os.getpid()
            }, title='Bot Started', footer="\U000023F3 Took {}ms".format(time_took))

        u.loop = asyncio.get_event_loop()
        fm.loop = asyncio.get_event_loop()

        await fm.enable_all_features()

    # Setup logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename='discord.log', encoding='utf-8', mode='a+')
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] <%(levelname)s> [%(name)s] %(message)s'))
    # logger.addHandler(handler)

    bot_logger = logging.getLogger('bot')
    bot_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        filename='bot.log', encoding='utf-8', mode='a+')
    handler.setFormatter(logging.Formatter(
        '[%(asctime)s] <%(levelname)s> %(message)s'))
    bot_logger.addHandler(handler)

    fm.logger.info('------------------------------')
    fm.logger.info('Parameters: {}'.format(sys.argv))
    fm.logger.info('Discord.py version: {}'.format(discord.__version__))
    config = None
    try:
        config = json.load(open('config.json'))
    except Exception as e:
        fm.logger.info('------------------------------')
        fm.logger.info('Missing or invalid config file.')
        fm.logger.info(e)
        quit(1)

    if 'discord_token' not in config or \
            'logging' not in config:
        fm.logger.info('------------------------------')
        fm.logger.info('Invalid config file.')
        quit(1)

    fm.logger.info('------------------------------')

    # Bot Setup
    workshop = u.Bot(
        discord_token=config['discord_token'],
        client=client,
        start_time=sk_start_time,
        config=config,
        lang=u.lang_obj(None)
    )

    fm = FeatureManager(workshop)

    workshop.feature_manager = fm

    fm.logger.info('Starting Bot...')

    workshop.run()


if __name__ == "__main__":
    start()
