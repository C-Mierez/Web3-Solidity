from scripts.utils import get_account, encode_function_data
from brownie import (
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    BoxV2,
    Contract,
    exceptions,
)
from scripts.deploy_v2_and_upgrade import _upgrade
import pytest


def test_proxy_upgrades():
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

    # Deploy BoxV2
    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, box_v2.abi)

    # Calling a V2 function on a Proxy with a V1 impl shouldn't work
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})

    # Upgrading the proxy
    _upgrade(box_v2.address, proxy, proxy_admin_contract=proxy_admin, account=account)

    proxy_box.store(5, {"from": account}).wait(1)  # Just to add a value

    # Calling a V2 function on an upgraded Proxy should work
    proxy_box.increment({"from": account}).wait(1)

    assert proxy_box.retrieve() == 10  # 5 + 5
