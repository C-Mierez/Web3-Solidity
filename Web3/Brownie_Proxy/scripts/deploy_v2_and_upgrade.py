from scripts.utils import get_account, encode_function_data
from brownie import Contract, BoxV2, TransparentUpgradeableProxy, ProxyAdmin

from scripts.deploy_box import get_value, main as m


def deploy_V2():
    account = get_account()

    box_v2 = BoxV2.deploy({"from": account})
    return box_v2


def upgrade():
    account = get_account()
    box_v2 = BoxV2[-1]
    # For testing purposes, I'll use increment() as an initializer
    initializer = box_v2.increment
    encoded_initializer = encode_function_data(initializer)

    _upgrade(
        box_v2.address,
        TransparentUpgradeableProxy[-1],
        proxy_admin_contract=ProxyAdmin[-1],
        account=account,
        initializer=encoded_initializer,
    )


def _upgrade(
    new_impl_address,
    proxy_contract,
    proxy_admin_contract=None,
    initializer=None,
    account=None,
    *args
):
    if proxy_admin_contract:
        if initializer:
            encoded_initializer = encode_function_data(initializer, *args)
            tx = proxy_admin_contract.upgradeAndCall(
                proxy_contract.address,
                new_impl_address,
                encoded_initializer,
                {"from": account},
            )
            tx.wait(1)
        else:
            tx = proxy_admin_contract.upgrade(
                proxy_contract.address,
                new_impl_address,
                {"from": account},
            )
            tx.wait(1)
    else:
        if initializer:
            encoded_initializer = encode_function_data(initializer, *args)
            tx = proxy_contract.upgradeToAndCall(
                new_impl_address,
                encoded_initializer,
                {"from": account},
            )
            tx.wait(1)
        else:
            tx = proxy_contract.upgradeTo(
                new_impl_address,
                {"from": account},
            )
            tx.wait(1)
    print("Proxy has been upgraded.")
    return tx


def increment():
    account = get_account()
    box = Contract.from_abi(
        "BoxV2", TransparentUpgradeableProxy[-1].address, BoxV2[-1].abi
    )

    # Now it is possible to interact with Box like normally
    tx = box.increment({"from": account})
    tx.wait(1)
    print("Incremented value.")


def main():
    m()
    deploy_V2()
    upgrade()
    get_value()
    increment()
    increment()
    get_value()
