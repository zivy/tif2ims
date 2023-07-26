import argparse
from gooey import Gooey
import pathlib
import sys
import SimpleITK as sitk
import sitk_ims_file_io as sio

def nonnegative_int(i):
    res = int(i)
    if res >= 0:
        return res
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid argument ({i}), expected value >= 0 ."
        )

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
        description="Extract a specific channel, pyramid level, frame number/timepoint from the imaris file and save to tif."
    )
    # positional/required argument
    parser.add_argument(
        "data_dir",
        type=dir_path,
        help="Path to the directory containing the ims files (expected file extension is .ims).",
    )
    parser.add_argument(
        "-l",
        type=nonnegative_int,
        default=0,
        help="Pyramid level (zero based indexing).",
    )
    parser.add_argument("-c", type=nonnegative_int, default=0, help="Channel number (zero based indexing).")
    parser.add_argument("-t", type=nonnegative_int, default=0, help="Frame number (zero based indexing).")

    if argv == None:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)

    file_names = sorted(list(pathlib.Path(args.data_dir).glob("*.ims")))
    if not file_names:
        print(
            "Directory does not contain files with the given prefix ({args.filename_prefix}).",
            sys.stderr,
        )
        return 1

    for file_name in file_names:
        meta_data = sio.read_metadata(file_name)

        num_pyramid_levels = len(meta_data["sizes"])
        if num_pyramid_levels <= args.l:
            print(
                f"{file_name}: cannot extract pyramid level {args.l}, valid levels are in [0,{num_pyramid_levels-1}]."
            )
            continue

        num_channels = len(meta_data["channels_information"])
        if num_channels <= args.c:
            print(
                f"{file_name}: cannot extract channel number {args.c}, valid channels are in [0,{num_channels-1}]."
            )
            continue

        num_frames = len(meta_data["times"])
        if num_frames <= args.t:
            print(
                f"{file_name}: cannot extract frame number {args.t}, valid frames are in [0,{num_frames-1}]."
            )
            continue

        image = sio.read(
            file_name, channel_index=args.c, resolution_index=args.l, time_index=args.t
        )
        new_file_name = file_name.with_suffix(".tif")
        sitk.WriteImage(
            image,
            pathlib.Path(new_file_name.parent)
            / pathlib.Path(f"c{args.c}_l{args.l}_t{args.t}_{new_file_name.name}"),
        )

    return sys.exit(0)


if __name__ == "__main__":
    main()
