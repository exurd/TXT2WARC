import os
import time
import shutil
import subprocess


def list_directory_contents(directory):
    return set(os.listdir(directory))


def add_to_stew(string, filename):
    """simple text emulisfer writer (backronyms suck)"""
    if type(string) is str:
        with open(filename, 'a', encoding='UTF-8') as file:
            file.write(string)
            file.write("\n")
            #print("Wrote to file.")


def send_to_grab_site(filename, file_path, data_folder, type, polling_interval=5, timeout=120, no_scrape=True):
    """
    Sends the specified file to a docker container of grab_site.

    polling_interval and timeout are in seconds.
    """
    print("Telling grab-site to use the text file...")

    monitor_folder = data_folder  # "../"  # D:\grab-site-data

    # create folder for finished warcs
    os.makedirs(os.path.join(data_folder, "__finishedWarcs"), exist_ok=True)
    
    before_snapshot = list_directory_contents(monitor_folder)

    container_name = "grab-site-container"
    command = ["docker", "exec", "-d", container_name, "grab-site", "-i", f"/data/{type}/{filename}", "--finished-warc-dir", "/data/__finishedWarcs", "--wpull-args=--no-warc-compression", "--igsets=global,youtube"]

    # execute command for grab-site docker container
    try:
        subprocess.run(command, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False  # sys.exit(1)

    elapsed_time = 0

    print("Waiting for grab-site to create a folder for item...")
    while elapsed_time < timeout:
        time.sleep(polling_interval)
        elapsed_time += polling_interval

        after_snapshot = list_directory_contents(monitor_folder)

        created_items = after_snapshot - before_snapshot
        if created_items:
            print(f"New items created in folder: {created_items}")
            THEfolder = next(iter(created_items))
            break
    else:
        print("No new items were created within the timeout period.")
        return False

    print(THEfolder)
    if no_scrape:
        os.remove(os.path.join(data_folder, THEfolder, "scrape"))  # https://github.com/ArchiveTeam/grab-site?tab=readme-ov-file#preventing-a-crawl-from-queuing-any-more-urls

    # destination = f"./done/{filename}"
    # if os.path.exists(destination):
    #     os.remove(destination)
    # os.rename(filename, destination)

    print("Waiting for grab-site to download everything in list...")
    while True:
        expected_file_path = os.path.join(data_folder, "__finishedWarcs", THEfolder + ".cdx")

        if os.path.isfile(expected_file_path):
            print(f"File '{expected_file_path}' is there.")
            break
        # else:
        #     print(f"File '{expected_file_path}' is not there yet...")
        time.sleep(15)

    # once this timer is up, the ecomony api rate limit is up
    print("Almost done, waiting 60 secs to allow other files to be moved then deleting the folder...")
    time.sleep(60)

    try:
        shutil.rmtree(os.path.join(data_folder, THEfolder))
        print("Folder and its content removed")
    except:
        print("Folder not deleted")

    return True
