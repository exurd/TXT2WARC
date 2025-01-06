Basically, it's a text file to WARC pipeline for grab-site (and technically [ArchiveBot](https://wiki.archiveteam.org/index.php/ArchiveBot)).

Prototype was coded on Windows and requires Python, 7-Zip & Docker. Untested on other platforms.

# Instructions

1. Download and install [Docker](https://www.docker.com).
2. Grab Dockerfile from [Nold360/docker-grab-site](https://github.com/Nold360/docker-grab-site) and place into a folder in a directory (e.g. `D:\grab-site-data`, `/home/user/grab-site-data/`).
    1. This will become the data folder for the docker containers, where the WARCs will be saved. It's recommened to use a root directory with no spaces.
3. Build the image with `docker build -t grab-site .` (Size of docker image is around 500 mb)
    1. If you are on an ARM system (or Apple Silicon), it is recommended to add `--platform=linux/amd64` to all of these docker commands you run avoid [issues with wget's WARC creation.](https://wiki.archiveteam.org/index.php/ArchiveTeam_Warrior#Can_I_run_the_Warrior_on_ARM_or_some_other_unusual_architecture?)
4. Spin the container up with `docker run -d --rm -p29000:29000 -v DATA_FOLDER:/data --name grab-site-container grab-site`
    1. Set `DATA_FOLDER` to the path of the above directory.
5. Create a text file of a bunch of IDs you want the script to archive.
    1. To see what this program supports, see [SUPPORTED.md](./SUPPORTED.md)
6. Open a terminal in this repo directory.
7. Run `python . DATA_FOLDER TEXTFILE ITEM_TYPE`
    1. `DATA_FOLDER` is the directory above, `TEXTFILE` is the text file and `ITEM_TYPE` is what type the items in the text file are.
