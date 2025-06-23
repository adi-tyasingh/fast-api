import asyncio
import unittest

from dotenv import load_dotenv
from httpx import AsyncClient

from app.main import app

load_dotenv(".env.test")


class test_routes(unittest.TestCase):

    def testRoute(self):
        pass
