import argparse
from gooey import Gooey
import pathlib
import sys
import SimpleITK as sitk
import sitk_ims_file_io as sio
import pyvips


def dir_path(path):
    p = pathlib.Path(path)
    if p.is_dir():
        return p
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid argument ({path}), not a directory path or directory does not exist."
        )


# GUI will appear if no commandline argument is given.
# Solution by @zertrin, https://github.com/chriskiehl/Gooey/issues/449
# this needs to be *before* the @Gooey decorator!
# (this code allows to only use Gooey when no arguments are passed to the script)
if len(sys.argv) >= 2:
    if "--ignore-gooey" not in sys.argv:
        sys.argv.append("--ignore-gooey")


@Gooey
def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert from tif to ims and combine channels into single file."
    )
    # positional/required arguments
    parser.add_argument(
        "data_dir",
        type=dir_path,
        help="Path to the directory containing the tif files.",
    )
    parser.add_argument(
        "filename_prefix",
        help="Filename prefix shared by all files that represent channels in the same image (e.g. SLIDE-1895_1.0.4_R000",
    )
    args = parser.parse_args(argv)
    prefix_len = len(args.filename_prefix)
    file_names = list(pathlib.Path(args.data_dir).glob(args.filename_prefix + "*.tif"))
    if not file_names:
        print(
            "Directory does not contain files with the given prefix ({args.filename_prefix}).",
            sys.stderr,
        )
        return 1

    output_filename = args.data_dir / pathlib.Path(args.filename_prefix + ".ims")
    default_colors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    channel_info = {
        "description": "",
        "range": [0.0, 255.0],
        "gamma": 1.0,
        "alpha": 1.0,
    }
    fname = file_names[0]
    # Read tif image using pyvips. The default SimpleITK tif reader doesn't read the intensity data
    # correctly (issues a warning about it). Didn't want to compile SimpleITK with the SCFIO bioformats
    # module because it makes installation for others hard.
    im = pyvips.Image.new_from_file(fname)
    image = sitk.GetImageFromArray(im.numpy())
    image.SetSpacing([im.xres, im.yres])
    channel_info["name"] = fname.stem[prefix_len + 1 :]
    channel_info["color"] = default_colors[0]
    # imaris images are always 3D
    image3d = sitk.JoinSeries([image])
    image3d.SetMetaData(
        sio.channels_metadata_key,
        sio.channels_information_list2xmlstr([(0, channel_info)]),
    )
    sio.write(image3d, output_filename)
    print(f"Converted {fname}")

    for i, fname in enumerate(file_names[1:], start=1):
        im = pyvips.Image.new_from_file(fname)
        image = sitk.GetImageFromArray(im.numpy())
        image.SetSpacing([im.xres, im.yres])
        channel_info["name"] = fname.stem[prefix_len + 1 :]
        channel_info["color"] = default_colors[i % len(default_colors)]
        # imaris images are always 3D
        image3d = sitk.JoinSeries([image])
        image3d.SetMetaData(
            sio.channels_metadata_key,
            sio.channels_information_list2xmlstr([(0, channel_info)]),
        )
        sio.append_channels(image3d, output_filename)
        print(f"Converted {fname}")
    print(f"Output file is: {output_filename}")


if __name__ == "__main__":
    main(sys.argv[1:])
