from scripts.deploy import deploy_farm, deploy_stonk_token
from scripts.add_allowed_token import add_allowed_tokens


def main():
    deploy_stonk_token()
    deploy_farm()
    add_allowed_tokens()
