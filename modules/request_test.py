import requests
import random, math, time

requestSession = requests.Session()


def request_url(url, retryAmount=8, headers=None, allow_redirects=False):
    tries = 0
    print(f"Requesting {url}...")
    for _ in range(retryAmount):
        tries += 1
        try:
            if headers != None:
                response: requests.Response = requestSession.get(url, headers=headers, allow_redirects=allow_redirects)
            else:
                response: requests.Response = requestSession.get(url, allow_redirects=allow_redirects)
            if response.status_code == 200:
                return response
            if response.status_code == 302: # Found
                return response
            if response.status_code == 403: # Forbidden
                return response
            print(response.status_code)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print("Timed out!")
            print(f"Request failed: {e}")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects!")
            print(f"Request failed: {e}")
            return False
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print("Too many requests!")
            if response.status_code == 404:
                return False
            # elif response.status_code == 403:
            #     print("Token Validation Failed. Re-validating...")
            #     validate_CSRF()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
        if tries < retryAmount:
            sleep_time = random.randint(
                math.floor(2 ** (tries - 0.5)),
                math.floor(2 ** tries)
                )
            print("Sleeping", sleep_time, "seconds.")
            time.sleep(sleep_time)
    return False


def exponential_binary_search(url, id):
    k = 0  # 2**0 = 1
    while request_url(url.format(id, 2**k)):
        k += 1

    # perform binary search in the range [2^(k-1) + 1, 2^k]
    low = 2**(k-1) + 1
    high = 2**k

    while low <= high:
        mid = (low + high) // 2
        if not request_url(url.format(id, mid)):
            high = mid - 1
        else:
            low = mid + 1

    return low - 1
