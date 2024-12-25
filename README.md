Basically, it's a text file to WARC pipeline for grab-site (and technically [ArchiveBot](https://wiki.archiveteam.org/index.php/ArchiveBot)).

Prototype was coded on Windows and requires Python, 7-Zip & Docker. Untested on other platforms.

# Instructions

1. Download and install [Docker](https://www.docker.com).
2. Grab Dockerfile from [Nold360/docker-grab-site](https://github.com/Nold360/docker-grab-site) and place into a folder in a root directory (e.g. `D:\grab-site-data`). This will become the data folder for the docker containers.
3. Build the image with `docker build -t grab-site .` (Size of docker image is around 500 mb)
4. Spin the container up with `docker run -d --rm -p29000:29000 -v DATA_FOLDER:/data --name grab-site-container grab-site` (Set `DATA_FOLDER` to the path of the above directory)
5. Create a text file of a bunch of IDs you want the script to archive.
6. Open a terminal in this repo directory.
7. Run `python . DATA_FOLDER TEXTFILE ITEM_TYPE` (with `DATA_FOLDER` being the directory above, `TEXTFILE` being the text file and `ITEM_TYPE` being what type the items in the text file are).
