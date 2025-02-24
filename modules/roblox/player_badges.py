import sys
import os
from modules.request_test import exponential_binary_search, request_url
from modules.shared import add_to_stew, send_to_grab_site

TYPE_FOLDER = "rbx_player_badges"


def main(badge_id, data_folder):
    # amount = find_last_version(badge_id)

    # if amount is False:
    #     return False  # sys.exit(1)

    filename = f"{badge_id}.txt"
    file_path = os.path.join(data_folder, TYPE_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    print("Adding URLs to text file...")

    # badge apis
    add_to_stew(f"https://www.roblox.com/badges/{badge_id}", file_path)
    add_to_stew(f"https://badges.roblox.com/v1/badges/{badge_id}", file_path)
    add_to_stew(f"https://economy.roblox.com/v2/assets/{badge_id}/details", file_path)  # in case an asset badge is requested

    # asset id apis
    # add_to_stew(f"https://www.roblox.com/item-thumbnails?params=[{{assetId:{badge_id}}}]", file_path)

    return send_to_grab_site(filename, file_path, data_folder, type_folder=TYPE_FOLDER)
