from brownie import AdvancedCollectible, network
from scripts.utils import ENV_LOCAL, get_contract, get_account
from scripts.advanced_collectible.create_collectible import create_collectible
from scripts.advanced_collectible.fund_with_link import fund_with_link
from scripts.advanced_collectible.deploy import deploy

import pytest

MOCK_VRF_RANDOMNESS = 42


def test_can_create_advanced_collectible():
    if network.show_active() not in ENV_LOCAL:
        pytest.skip()

    # Act
    advanced_collectible = deploy()
    tx = fund_with_link()
    tx.wait(1)
    tx_create = create_collectible()
    tx_create.wait(1)

    requestId = tx_create.events["requestedCollectible"]["requestId"]
    get_contract("vrf_coordinator", "vrf").callBackWithRandomness(
        requestId,
        MOCK_VRF_RANDOMNESS,
        advanced_collectible.address,
        {"from": get_account()},
    )

    # Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToStonkType(0) == MOCK_VRF_RANDOMNESS % 3
