import csv

try:
    from pathlib import Path

    PATHLIB_AVAILABLE = True
except ImportError:
    import os
    import errno

    PATHLIB_AVAILABLE = False


def read_lists(file_path):
    """
    Returns the data at `file_path` as a list of lists. Ignores blank lines.

    Parameters
    ----------
    file_path : string | Path

    Returns
    -------
    list[list[str]]
        A list containing a list of strings for each row.

    Example
    -------
    >>> from easycsv import csv_as_list
    >>> filepath = 'C:\\path\\to\\file.csv'
    >>> print(filepath)
    C:\path\to\file.csv
    >>> l = csv_as_list(filepath)
    >>> print(l[0])
    First,Line,Of,File,Prints,Here
    """
    with open(file_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        return [r for r in reader if r]


def read_dicts(file_path):
    """
    Returns the data at `file_path` as a list of dicts.

    Parameters
    ----------
    file_path : string | Path

    Returns
    -------
    list[dict[str: str]]
        A list containing a dict for each line of the CSV file. Each dict
        is keyed according to the CSV header.
    """
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [r for r in reader if r]


def write_lists(data, csv_path, mkdir=False):
    """
    Writes the input data to a CSV file

    Always produces a Unix-style CSV file, regardless of whether on
    Windows or not.

    Parameters
    ----------
    data : list[list]
    csv_path : string | Path
        Should have a .csv extension. `mkdir` will malfunction if it doesn't.
    mkdir : bool
        If true, creates the directory tree leading up to `csv_path`, ignoring
        if directories already exist.
    """
    if mkdir:
        __mkdirp(csv_path)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def write_dicts(data, csv_path, mkdir=False, silent_fail=False):
    """
    Writes the input data to a CSV file

    Always produces a Unix-style CSV file, regardless of whether on
    Windows or not.

    Parameters
    ----------
    data : list[dict]
        One dict per line. The first dict is expected to contain all of the
        keys that will form the header line.
    csv_path : string | Path
        Should have a .csv extension. `mkdir` will malfunction if it doesn't.
    mkdir : bool
        If true, creates the directory tree leading up to `csv_path`, ignoring
        if directories already exist.
    silent_fail: bool
        If `true`, causes the method to do nothing if `data` happens
        to be empty.
    """
    if not data:
        if silent_fail:
            return
        else:
            raise ValueError("Can't write CSV with no data")
    if mkdir:
        __mkdirp(csv_path)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def __mkdirp(csv_path):
    if PATHLIB_AVAILABLE:
        dir_path = Path(csv_path)
        if dir_path.suffix != "":
            dir_path = dir_path.parent
        dir_path.mkdir(parents=True, exist_ok=True)
    else:
        if csv_path.lower().endswith(".csv"):
            dirname = os.sep.join(csv_path.split(os.sep)[:-1])
        else:
            dirname = csv_path
        try:
            os.makedirs(dirname)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dirname):
                pass
            else:
                raise
