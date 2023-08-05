import os
import pytest
import sys

sys.path.append(os.path.abspath('../anybot'))
from anybot.action import Action
from anybot.bot import Bot


def pytest_addoption(parser):
    parser.addoption("--api-access", action="store_true")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--api-access"):
        return
    skip_slow = pytest.mark.skip(reason="add --api-access option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


class DummyAction(Action):
    def __init__(self):
        super(DummyAction, self).__init__()
        self.begun = self.finished = False
        self.count = 0

    def begin(self, api):
        self.begun = True

    def end(self, api):
        self.finished = True

    def step(self, api):
        self.count += 1
        if self.count >= 5:
            self.done = True


@pytest.fixture
def action():
    return DummyAction()


@pytest.fixture
def bot():
    return Bot(None)
