name = 'buildabot'
__title__ = 'buildabot'
__author__ = 'AL_1'
__copyright__ = 'Copyright 2018-2020 AL_1'
__version__ = '1.0.1'

from .bot import Bot
from .typer import Typer
from .logger import Logger
from . import utils
from .feature_manager import FeatureManager
from .feature import Feature
from .event_handler import EventHandler
from collections import namedtuple

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=1, minor=0, micro=0, releaselevel='beta', serial=0)
