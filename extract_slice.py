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

def percent_float(f):
    res = float(f)
    if res >= 0 and res<=1:
        return res
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid argument ({f}), expected value in [0,1]."
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
        description="Extract a slice, frame number/timepoint from the imaris file."
    )
    # positional/required argument
    parser.add_argument(
        "data_dir",
        type=dir_path,
        help="Path to the directory containing the ims files (expected file extension is .ims).",
    )
    parser.add_argument(
        "-p",
        type=percent_float,
        default=0.5,
        help="Slice to extract as a percentage of the number of slices (0.5 is the middle slice)",
    )
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

        num_frames = len(meta_data["times"])
        if num_frames <= args.t:
            print(
                f"{file_name}: cannot extract frame number {args.t}, valid frames are in [0,{num_frames-1}]."
            )
            continue

        slice_number = int(args.p*meta_data['sizes'][0][2])

        image = sio.read(
            file_name, time_index=args.t, sub_ranges = [range(0,meta_data['sizes'][0][0]), range(0,meta_data['sizes'][0][1]), range(slice_number, slice_number+1)]
        )
        new_file_name =  str(file_name.parent / file_name.stem) + f"_s{slice_number}_t{args.t}.ims"
        sio.write(image, new_file_name)

    return sys.exit(0)


if __name__ == "__main__":
    main()
