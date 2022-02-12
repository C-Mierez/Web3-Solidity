from brownie import network

import pytest

from scripts.utils import ENV_LOCAL, get_account
from scripts.simple_collectible.create_collectible import deploy_and_create


def test_can_create_simple_collectible():
    if network.show_active() not in ENV_LOCAL:
        pytest.skip()

    account = get_account()
    simple_collectible = deploy_and_create()

    assert simple_collectible.ownerOf(0) == account
