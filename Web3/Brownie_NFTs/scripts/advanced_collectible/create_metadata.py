from brownie import AdvancedCollectible, network
from meta.advanced_collectible_template import metadata_template
from pathlib import Path
from random import randint

import json
import os
import requests

STONK_MAPPING = {
    0: "UltraStonks",
    1: "Stonks",
    2: "NoStonks",
}

stonkType_to_image_uri = {
    "UltraStonks": "https://ipfs.io/ipfs/QmasXLAmfybUxNxzWJQgDpa8q5hP1heq49h62uV6qo2R6u?filename=ultrastonks.png",
    "Stonks": "https://ipfs.io/ipfs/QmeDU3zPDvwQrbYaE6ZUqJH2cY8jy21A7crJZYmKbTCPNG?filename=stonks.png",
    "NoStonks": "https://ipfs.io/ipfs/Qmctsi9PtbrP4RQFWqg861696jofMn7cb3btT3xJ3xyVAr?filename=nostonks.png",
}


def create_metadata():
    advanced_collectible = AdvancedCollectible[-1]

    advanced_collectible_count = advanced_collectible.tokenCounter()

    print(f"Amount of Collectibles: {advanced_collectible_count}.")

    # Loop through all tokens and set the metadata for each one
    for token_id in range(advanced_collectible_count):
        stonkType = STONK_MAPPING[advanced_collectible.tokenIdToStonkType(token_id)]

        metadata_file_name = f"./meta/{network.show_active()}/{advanced_collectible}/{token_id}-{stonkType}"

        if Path(metadata_file_name + ".json").exists():
            print(f"Metadata file already exists: {metadata_file_name}.json")
        else:
            print(f"Creating metadata file: {metadata_file_name}.json")
            collectible_metadata = metadata_template
            collectible_metadata["name"] = stonkType
            collectible_metadata["description"] = f"Feeling like a {stonkType} day."

            # This is just for fun. Should probably not use this rand function for this
            collectible_metadata["attributes"][0]["value"] = randint(0, 100)

            # Set the image path
            image_path = "./img/" + stonkType.lower().replace("_", "-") + ".png"

            # Only upload to IPFS if the image doesn't exist already
            image_uri = None
            if os.getenv("UPLOAD_TO_IPFS") == "true":
                # Uploading to IPFS using a local node
                # image_uri = upload_to_ipfs(image_path)

                # Uploading to IPFS using and pinning the image to Pinata
                image_uri = upload_to_pinata(image_path)
            image_uri = image_uri if image_uri else stonkType_to_image_uri[stonkType]

            collectible_metadata["image"] = image_uri

            # Create network subdir in the meta dir if it doesn't exist already
            if not Path(
                f"./meta/{network.show_active()}/{advanced_collectible}/"
            ).exists():
                os.mkdir(f"./meta/{network.show_active()}/{advanced_collectible}/")
            # Write the metadata to a file
            with open(metadata_file_name + ".json", "w") as file:
                json.dump(collectible_metadata, file)

            # if os.getenv("UPLOAD_TO_IPFS") == "true":
            # Upload json info
            file_uri = upload_to_pinata(metadata_file_name + ".json")

            # Save the uri in a file
            with open(metadata_file_name + "-INFO" + ".json", "w") as file:
                json.dump(
                    {"ipfs_uri": file_uri, "image_uri": image_uri},
                    file,
                )


def upload_to_ipfs(filepath):
    with Path(filepath, encoding="utf8").open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = os.getenv("IPFS_WEB_UI_URL")
        endpoint = "/api/v0/add"
        response = requests.post(
            ipfs_url + endpoint,
            files={
                "file": image_binary,
            },
        )
        ipfs_hash = response.json()["Hash"]

        # Separate by '/' and keep the last one
        # "./img/0-Stonks.png" -> 0-Stonks.png
        filename = filepath.split("/")[-1:][0]

        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        return image_uri


def upload_to_pinata(filepath):
    PINATA_BASE_URL = "https://api.pinata.cloud/"
    endpoint = "pinning/pinFileToIPFS"
    filename = filepath.split("/")[-1:][0]

    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_PRIVATE_KEY"),
    }

    with Path(filepath, encoding="utf8").open("rb") as fp:
        image_binary = fp.read()
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={
                "file": (filename, image_binary),
            },
            headers=headers,
        )
        ipfs_hash = response.json()["IpfsHash"]

        # Separate by '/' and keep the last one
        # "./img/0-Stonks.png" -> 0-Stonks.png
        filename = filepath.split("/")[-1:][0]

        file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(file_uri)
        return file_uri


def main():
    return create_metadata()
