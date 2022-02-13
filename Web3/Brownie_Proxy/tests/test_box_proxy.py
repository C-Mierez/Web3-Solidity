from scripts.utils import get_account, encode_function_data
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_proxy_delegates_calls():
    account = get_account()

    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    encoded_initializer = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_initializer,
        {"from": account, "gas_limit": 1000000},
    )

    proxy_box = Contract.from_abi("Box", proxy.address, box.abi)

    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account}).wait(1)
    assert proxy_box.retrieve() == 1
