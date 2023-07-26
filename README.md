Programs for converting+combining/extracting tif to ims and the other way round.

**tif2ims**: receive a set of tif files that represent channels and combine them into a single file using the imaris format. **The order of the channels in the output file is determined by the lexicographical order of the file names.** Result is written to an ims file with the same file name prefix as the original.

For example, the output file created from the following files will
have the channel order:
```
1. SLIDE-1895_4.0.4_R001_Cy3_CD86_FINAL_AFR_F.tif
2. SLIDE-1895_4.0.4_R001_Cy5_Pax5_FINAL_AFR_F.tif
3. SLIDE-1895_4.0.4_R001_Cy7_ERTR-7_FINAL_AFR_F.tif
4. SLIDE-1895_4.0.4_R001_DAPI__FINAL_F.tif
```

If we want to change the order we can modify the file name, after the common prefix, for instance:
```
1. SLIDE-1895_4.0.4_R001_01_DAPI__FINAL_F.tif
2. SLIDE-1895_4.0.4_R001_02_Cy5_Pax5_FINAL_AFR_F.tif
3. SLIDE-1895_4.0.4_R001_03_Cy7_ERTR-7_FINAL_AFR_F.tif
4. SLIDE-1895_4.0.4_R001_04_Cy3_CD86_FINAL_AFR_F.tif
```

**ims2tif**: receive a set of ims files and extract the specified channel, time point and level in the image pyramid from each of the files. Result is written to tif file with the channel number, pyramid level and time point prefixed to the original file name.

For example, the output created for the file `Barcode_1034_CollIV.ims` when extracting channel 1, pyramid level 3 and timepoint 2 is `c1_l3_t2_Barcode_1034_CollIV.tif`. Note that all indexes (channel, pyramid level and timepoint are zero based).

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
1. Edit the `run_tif2ims.bat` and `run_ims2tif.bat` files. Set the path to anaconda and path to vips library (see current batch file for example).

## Usage
1. Double click the  `run_tif2ims.bat` file or `run_ims2tif.bat`.

On OSX/Linux installation is easier, no need to download the libvips and set the path to it. Install `conda env create -f osx_linux.yml` and then edit the `run_tif2ims.sh` `run_ims2tif.sh` files, updating the path to anaconda.

### Running from commandline

If run without any arguments, will open a GUI:
```
pythonw tif2ims.py
```
Notice that we use `pythonw` which is compatible with wxPython.

To run without a GUI provide the data directory and channel file name prefix on the commanadline, for example:

```
pythonw tif2ims.py data SLIDE-1895_1.0.4_R000
```

