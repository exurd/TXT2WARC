import sys
import os
from modules.request_test import exponential_binary_search, request_url
from modules.shared import add_to_stew, send_to_grab_site

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Referer': 'https://www.roblox.com'
}


def is_uncopylocked(assetId): # i last created something like this in 2022. 2022 was 2 years ago.
    version = 0
    while version <= 3:
        url = f"https://assetdelivery.roblox.com/v2/assetId/{str(assetId)}/version/{str(version)}"
        test = request_url(url, headers=headers)
        if test.ok:
            testJson = test.json()  # test most recent version
            if 'errors' in testJson:
                # and now, some old comments from 2022:
                    # not uncopylocked; may cause actual copylocked game to "fail" if 403 is on most recent version but what are the chances of that happening?
                    # EDIT: 25891754. added another check to system. sorry to all of the ones i did that said it was "copylocked" (a couple)
                    # i could just check the 404 instead of a generic error in the json. too lazy to do it right now though
                version += 1
            else:
                return True
    return False


def find_last_version(placeId):
    if type(int(placeId)) is int:
        if is_uncopylocked(placeId):
            url = "https://assetdelivery.roblox.com/v1/asset/?id={}&version={}"
            last_num = exponential_binary_search(url, placeId)
            print(f"Last number found: {last_num}")
            return last_num
        else:
            print("Not uncopylocked, exiting!")
            return False
    else:
        print("Not a vaild argument, exiting!")
        return False

def main(place_id, data_folder):
    """
    This uses Asset Delivery API v1. This is because it uses HTTP 302
    headers to automatically show the location to the CDN url for the
    version and grab_site will download both without intervention.
    """
    amount = find_last_version(place_id)

    if amount is False:
        return False  # sys.exit(1)

    filename = f"uncopylocked_{place_id}.txt"
    file_path = os.path.join(data_folder, "uncopylocked_places", filename)
    if os.path.exists(filename):
        os.remove(filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    print("Adding URLs to text file...")
    add_to_stew(f"https://www.roblox.com/places/api-get-details?assetId={place_id}", file_path)
    add_to_stew(f"https://economy.roblox.com/v2/assets/{place_id}/details", file_path)
    for i in range(amount+1):  # remember, python counts *FROM* 0!
        add_to_stew(f"https://assetdelivery.roblox.com/v1/asset/?id={place_id}&version={str(i)}", file_path)
        # add_to_stew(f"https://assetdelivery.roblox.com/v2/assetId/{place_id}/version/{str(i)}", file_path)

    return send_to_grab_site(filename, file_path, data_folder, type="uncopylocked_places")
