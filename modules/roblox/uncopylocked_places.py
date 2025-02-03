import sys
import os
from modules.roblox.shared import find_last_version
from modules.shared import add_to_stew, send_to_grab_site
from modules.request_test import request_url

TYPE_FOLDER = "rbx_uncopylocked_places"


def main(place_id, data_folder):
    """
    This uses Asset Delivery API v1. This is because it uses HTTP 302
    headers to automatically show the location to the CDN url for the
    version and grab_site will download both without intervention.
    """
    amount = find_last_version(place_id)

    if amount is False:
        return False  # sys.exit(1)

    filename = f"{place_id}.txt"
    file_path = os.path.join(data_folder, TYPE_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    print("Adding URLs to text file...")

    # place apis
    # add_to_stew(f"https://www.roblox.com/games/{place_id}", file_path)  # loads of urls are requested when this is added
    add_to_stew(f"https://apis.roblox.com/universes/v1/places/{place_id}/universe", file_path)

    universe_req = request_url(f"https://apis.roblox.com/universes/v1/places/{place_id}/universe")
    if universe_req:
        universe_id = universe_req.json()["universeId"]
        add_to_stew(f"https://games.roblox.com/v2/games/{universe_id}/media", file_path)
        add_to_stew(f"https://games.roblox.com/v1/games/votes?universeIds={universe_id}", file_path)
        add_to_stew(f"https://games.roblox.com/v1/games/{universe_id}/game-passes?limit=100&sortOrder=1", file_path)
        add_to_stew(f"https://games.roblox.com/v1/games/{universe_id}/game-passes?limit=100&sortOrder=2", file_path)
        add_to_stew(f"https://games.roblox.com/v1/games/{universe_id}/favorites/count", file_path)

    # asset id apis
    add_to_stew(f"https://www.roblox.com/item-thumbnails?params=[{{assetId:{place_id}}}]", file_path)
    add_to_stew(f"https://www.roblox.com/places/api-get-details?assetId={place_id}", file_path)
    add_to_stew(f"https://economy.roblox.com/v2/assets/{place_id}/details", file_path)
    for i in range(amount+1):  # remember, python counts *FROM* 0!
        add_to_stew(f"https://assetdelivery.roblox.com/v1/asset/?id={place_id}&version={str(i)}", file_path)
        # add_to_stew(f"https://assetdelivery.roblox.com/v2/assetId/{place_id}/version/{str(i)}", file_path)  # cdn url will be different to v1, so why download what would be an appendix to the warc?

    return send_to_grab_site(filename, file_path, data_folder, type_folder=TYPE_FOLDER)
