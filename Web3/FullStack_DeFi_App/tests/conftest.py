import pytest

from web3 import Web3


@pytest.fixture
def to_stake_amount():
    return Web3.toWei(1, "ether")
