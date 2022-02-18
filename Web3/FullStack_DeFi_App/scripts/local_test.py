from scripts.deploy import deploy_farm, deploy_stonk_token
from scripts.add_allowed_tokens import add_allowed_tokens
from scripts.update_front_end_config import update_front_end_config


def main():
    deploy_stonk_token()
    deploy_farm()
    add_allowed_tokens()
    update_front_end_config()
