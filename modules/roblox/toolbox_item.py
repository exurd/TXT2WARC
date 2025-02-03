import sys
import os
from modules.roblox.shared import find_last_version
from modules.shared import add_to_stew, send_to_grab_site
from modules.request_test import request_url

TYPE_FOLDER = "rbx_toolbox_item"


def main(asset_id, data_folder):
    """
    This uses Asset Delivery API v1. This is because it uses HTTP 302
    headers to automatically show the location to the CDN url for the
    version and grab_site will download both without intervention.
    """
    amount = find_last_version(asset_id)

    if amount is False:
        return False  # sys.exit(1)

    filename = f"{asset_id}.txt"
    file_path = os.path.join(data_folder, TYPE_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    print("Adding URLs to text file...")

    # asset id apis
    add_to_stew(f"https://www.roblox.com/item-thumbnails?params=[{{assetId:{asset_id}}}]", file_path)
    add_to_stew(f"https://economy.roblox.com/v2/assets/{asset_id}/details", file_path)
    add_to_stew(f"https://apis.roblox.com/toolbox-service/v1/items/details?assetIds={asset_id}", file_path)
    add_to_stew(f"https://apis.roblox.com/asset-reviews-api/v1/assets/{asset_id}/comments/count")
    for i in range(amount+1):  # remember, python counts *FROM* 0!
        add_to_stew(f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}&version={str(i)}", file_path)
        # add_to_stew(f"https://assetdelivery.roblox.com/v2/assetId/{place_id}/version/{str(i)}", file_path)  # cdn url will be different to v1, so why download what would be an appendix to the warc?

    return send_to_grab_site(filename=filename, file_path=file_path, data_folder=data_folder, type_folder=TYPE_FOLDER)
