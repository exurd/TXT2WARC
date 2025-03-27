from modules.request_test import exponential_binary_search, request_url

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Referer': 'https://www.roblox.com'
}

def is_uncopylocked(assetId): # i last created something like this in 2022. 2022 was 2 years ago.
    """
    Checks if an asset is uncopylocked.
    Not just for places; any asset that is available in the AssetDelivery API can be checked.
    """
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


def find_last_version(assetId):
    """
    This uses AssetDelivery v1 as that will HTTP 404 when the version is too high.
    """
    if type(int(assetId)) is int:
        if is_uncopylocked(assetId):
            # url = "https://assetdelivery.roblox.com/v1/asset/?id={}&version={}"
            # last_num = exponential_binary_search(url, assetId)
            # print(f"Last number found: {last_num}")
            # return last_num

            # header `roblox-assetversionnumber` on this api can show last version
            req = request_url(f"https://assetdelivery.roblox.com/v1/asset/?id={str(assetId)}&version=0")
            if req:
                if req.headers:
                    return int(req.headers["roblox-assetversionnumber"])
            print("Could not get info from assetdelivery...")
            return False
        else:
            print("Not uncopylocked, exiting!")
            return False
    else:
        print("Not a vaild argument, exiting!")
        return False
