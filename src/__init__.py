import os
import json
import time
import random
import aiohttp
import requests
import argparse
from colorama import init
from datetime import datetime
from urllib.parse import unquote
from base64 import urlsafe_b64decode
from json.decoder import JSONDecodeError
from src.headers import headers
from src.agent import gr_ua