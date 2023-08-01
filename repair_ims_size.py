import argparse
from gooey import Gooey
import pathlib
import sys
import sitk_ims_file_io as sio
import pandas as pd


def dir_path(path):
    p = pathlib.Path(path)
    if p.is_dir():
        return p
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid argument ({path}), not a directory path or directory does not exist."
        )


def csv_path(path, required_columns={}):
    """
    Define the csv_path type for use with argparse. Checks
    that the given path string is a path to a csv file and that the
    header of the csv file contains the required columns.
    """
    p = pathlib.Path(path)
    required_columns = set(required_columns)
    if p.is_file():
        try:  # only read the csv header
            expected_columns_exist = required_columns.issubset(
                set(pd.read_csv(path, nrows=0).columns.tolist())
            )
            if expected_columns_exist:
                return p
            else:
                raise argparse.ArgumentTypeError(
                    f"Invalid argument ({path}), does not contain all expected columns."
                )
        except UnicodeDecodeError:
            raise argparse.ArgumentTypeError(
                f"Invalid argument ({path}), not a csv file."
            )
    else:
        raise argparse.ArgumentTypeError(f"Invalid argument ({path}), not a file.")


# GUI will appear if no commandline argument is given.
# Solution by @zertrin, https://github.com/chriskiehl/Gooey/issues/449
# this needs to be *before* the @Gooey decorator!
# (this code allows to only use Gooey when no arguments are passed to the script)
if len(sys.argv) >= 2:
    if "--ignore-gooey" not in sys.argv:
        sys.argv.append("--ignore-gooey")


def repair_size(file_name, x_in_um, y_in_um, z_in_um, output_dir):
    try:
        image = sio.read(file_name, vector_pixels=True)
        image.SetSpacing([x_in_um, y_in_um, z_in_um])
        image.SetMetaData("unit", "um")
        sio.write(image, output_dir / file_name.name)
    except Exception as e:
        print(e, sys.stderr)


@Gooey
def main(argv):
    parser = argparse.ArgumentParser(
        description="Change/repair the pixel size in an ims file to the correct one."
    )
    # positional/required arguments
    parser.add_argument(
        "csv_path",
        type=csv_path,
        help="Path to csv file with columns titled: file_name,x_in_um,y_in_um,z_in_um."
        + "The paths in the file_name column are relative to the csv file location.",
    )
    parser.add_argument(
        "output_dir",
        type=dir_path,
        help="Path to the output directory (choose different directory from where the original "
        + "ims files are found, otherwise they will be overwritten).",
    )
    args = parser.parse_args(argv)

    df = pd.read_csv(args.csv_path)
    df["file_name"] = df["file_name"].apply(
        lambda x: args.csv_path.parent / pathlib.Path(x)
    )
    df[["file_name", "x_in_um", "y_in_um", "z_in_um"]].apply(
        lambda x: repair_size(*x, args.output_dir), axis=1
    )

    return sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
