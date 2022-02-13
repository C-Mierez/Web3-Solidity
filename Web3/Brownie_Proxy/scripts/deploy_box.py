from scripts.utils import get_account, encode_function_data
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def deploy():
    account = get_account()

    print(f"Deploying Box to {network.show_active()}...")

    box = Box.deploy({"from": account})

    print(f"Deployed Box at {box.address}")

    proxy_admin = ProxyAdmin.deploy({"from": account})

    # Initializers are used when there's a need for constructor logic
    # since constructors are not present when using proxies
    # Need to encode for the proxy
    # The proxy handles the data as bytes
    initializer = box.store, 1
    # Not sending a function will just return a 0x bytes (So no initializer will be used)
    encoded_box_initializer = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encoded_box_initializer,
        {"from": account, "gas_limit": 1000000},
    )

    print(f"Proxy deployed to {proxy.address}")


def store_value():
    account = get_account()
    # Assigning the Proxy address the Box ABI. This works because the Proxy
    # delegates all the calls to the implementation... which IS Box.
    box = Contract.from_abi("Box", TransparentUpgradeableProxy[-1].address, Box[-1].abi)

    # Now it is possible to interact with Box like normally
    tx = box.store(10, {"from": account})
    tx.wait(1)
    print("Stored.")


def get_value():
    box = Contract.from_abi("Box", TransparentUpgradeableProxy[-1].address, Box[-1].abi)

    print(f"Box value is: {box.value()}.")


def main():
    deploy()
    get_value()
    store_value()
    get_value()
