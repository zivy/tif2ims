Program that receives a set of tif files that represent channels, combines them into a single file using the imaris format.

## One time setup (Windows)

1. Install miniconda if not already installed ([download](https://docs.conda.io/en/latest/miniconda.html)).
1. Download this repository ([zip file](https://github.com/zivy/tif2ims/archive/refs/heads/main.zip)).
1. Open the Anaconda Prompt (found under the Anaconda3 start menu).
1. Type the commands in the terminal window (don't forget to change the path_to_this_directory):
    ```
    cd path_to_this_directory
    conda env create -f windows.yml
    ```
1. Download the [libvips zip file](https://github.com/libvips/build-win64-mxe/releases/download/v8.13.2/vips-dev-w64-all-8.13.2.zip).
1. Copy it to this directory and unzip it.
1. Edit the `run_tif2ims.bat` file. Set the path to anaconda and path to vips library (see current batch file for example).

## Usage
1. Double click the  `run_tif2ims.bat` file.

### Comments

On OSX/Linux installation is easier, no need to download the libvips and set the path to it. Install `conda env create -f osx_linux.yml` and then edit the `run_tif2ims.sh` file, updating the path to anaconda.
