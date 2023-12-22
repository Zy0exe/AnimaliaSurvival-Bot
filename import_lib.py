#Cog Stuff
from dotenv import load_dotenv
import logging

# Discord stuff
import discord
from discord import Embed, Game, app_commands
from discord.ext import commands, menus, tasks
from discord.ext.commands import cooldown

# Steam Stuff
import steam
from steam import steamid
from rcon.source import Client
from rcon.source import rcon

# SQL Stuff
import mysql.connector
from mysql.connector import Error

## More needed stuff
import json
import random
import os
from datetime import datetime, timedelta
import traceback
import shutil
import asyncio
import requests
import time
import signal
import sys
from typing import Literal, Optional

# Command
from commands.strike import strike_player