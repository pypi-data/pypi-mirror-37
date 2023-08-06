import logging
import numpy as np
import os
import pandas as pd
import re
import string

from .plots import heatmap_by_group
from .utils import check_sample_id, runcmd

translation = str.maketrans("ACGTRYSWKMBDHVN", "TGCAYRSWMKVHDBN")
rev_comp = lambda s: str.translate(s[::-1], translation)
logger = logging.getLogger(__name__)


def is_samplesheet(dataframe, additional_cols=None):
    """
    Args:
        dataframe (pandas.DataFrame): parsed sample sheeet
        additional_cols (list): any additional columns necessary for the sheet at the time of validation

    Returns:
        bool

    Raises:
        ValueError: lists missing required columns
    """
    required_cols = [
        'POC',
        'SAMPLE_ID',
        'PRIMER_PLATE_NUMBER',
        'PRIMER_WELL_POSITION',
        'PRIMER_BARCODE',
    ]
    if additional_cols:
        required_cols += additional_cols
    missing_cols = []
    for c in required_cols:
        if c not in dataframe.columns:
            missing_cols.append(c)
    if len(missing_cols) > 0:
        raise ValueError("Missing required columns: %s" % ", ".join(missing_cols))

    return True


def preprocess_samplesheet(
    excel_file, out_file=None, cols=None, reverse_complement=False
):
    """Checks incoming samplesheet for required columns:

        'POC', 'SAMPLE_ID', 'PRIMER_PLATE_NAME', 'PRIMER_PLATE_NUMBER',
        'PRIMER_WELL_POSITION', 'PRIMER_SEQUENCE_NAME', 'SEQUENCE', 'PRIMER_BARCODE'

    String case and order does not matter.

    POC, SAMPLE ID, and PRIMER_BARCODE must be present for each row.

    Args:
        excel_file (str): path to .xls file where sheet one header matches above required columns
        out_file (Optional[str]): path to file (CSV) of processes samplesheet including new header
            item VALID_SAMPLE_ID. When not specified, out_file will be written as SampleSheet.csv
            within the same directory as the excel file.
        cols (Optional[str]): column label and values to add onto sheet,
            e.g. 'SEQUENCE_CENTER:PNNL,PLATFORM:Illumina'; organized as column header and column
            value pairs

    Returns:
        str

    Raises:
        ValueError
    """
    if out_file is None:
        out_file = os.path.join(os.path.dirname(excel_file), "SampleSheet.csv")
    df = pd.read_excel(excel_file)
    # upper case all column labels
    df.columns = map(str.upper, df.columns)
    # lets just map the common labels to our labels...
    column_name_map = {
        "PLATE NAME(S)": "PRIMER_PLATE_NAME",
        "PLATE NUMBER": "PRIMER_PLATE_NUMBER",
        "WELL POSITION": "PRIMER_WELL_POSITION",
        "SEQUENCE NAME": "PRIMER_SEQUENCE_NAME",
        "BARCODE": "PRIMER_BARCODE",
        "SAMPLEID": "SAMPLE_ID",
    }
    remapped_column_names = []
    for i in range(len(df.columns)):
        if df.columns[i] in column_name_map:
            remapped_column_names.append(column_name_map[df.columns[i]])
        else:
            remapped_column_names.append(df.columns[i])
    df.columns = remapped_column_names
    # validate this dataframe
    is_samplesheet(df)
    # make sure there's a POC per sample
    if any(df.POC.isnull()):
        offending_rows = [i + 2 for i in df.index[df.POC.isnull() == True].tolist()]
        raise ValueError(
            "All rows must contain a POC [CHECK ROWS [%s]]" %
            ",".join(map(str, offending_rows))
        )

    # make sure there's a barcode per sample
    if any(df.PRIMER_BARCODE.isnull()):
        offending_rows = [
            i + 2 for i in df.index[df.PRIMER_BARCODE.isnull() == True].tolist()
        ]
        raise ValueError(
            "All rows must contain a PRIMER BARCODE [CHECK ROWS [%s]]" %
            ",".join(map(str, offending_rows))
        )

    # make sure there's a sample id per sample entry
    if any(df.SAMPLE_ID.isnull()):
        offending_rows = [
            i + 2 for i in df.index[df.SAMPLE_ID.isnull() == True].tolist()
        ]
        raise ValueError(
            "All rows must contain a SAMPLE ID [CHECK ROWS [%s]]" %
            ",".join(map(str, offending_rows))
        )

    # fail on duplicate primer barcodes
    if any(df.duplicated(subset="PRIMER_BARCODE", keep=False)):
        raise ValueError("Duplicate PRIMER BARCODEs exist")

    # process the sample IDs
    df['VALID_SAMPLE_ID'] = df['SAMPLE_ID'].apply(check_sample_id)
    # append barcode to any duplicate sample IDs
    df['VALID_SAMPLE_ID'] = np.where(
        df.duplicated(subset="VALID_SAMPLE_ID", keep=False),
        df['VALID_SAMPLE_ID'] + '-' + df['PRIMER_BARCODE'],
        df['VALID_SAMPLE_ID'],
    )
    # change separator where multiple POCs are listed
    df['POC'] = df['POC'].apply(check_sample_id)
    if cols:
        for label_value_pair in cols.split(","):
            try:
                label, value = label_value_pair.split(":")
                df[label] = value
            except ValueError:
                logger.warning(
                    "Ignoring label:value pair [%s] as no ':' was identified as the separator" %
                    label_value_pair
                )
    if reverse_complement:
        df['PRIMER_BARCODE'] = df['PRIMER_BARCODE'].apply(rev_comp)
    # print the new samplesheet
    df.to_csv(out_file, index=False)


def barcode_tsv_from_samplesheet(csv, out_file=None):
    """Prints a TSV of SAMPLE:BARCODE from a sample sheet (CSV).

    Checks incoming samplesheet for required columns:

        'POC', 'SAMPLE_ID', 'PRIMER_PLATE_NUMBER', 'PRIMER_WELL_POSITION', 'PRIMER_BARCODE', 'VALID_SAMPLE_ID'

    Args:
        csv (str): path to samplesheet (CSV) file with required header
        out_file (Optional[str]): path to write barcodes TSV file. If None, out_file is written
            to same directory as csv as barcodes.tsv.

    Returns:
        str
    """
    if out_file is None:
        out_file = os.path.join(os.path.dirname(csv), "barcodes.tsv")
    df = pd.read_csv(csv, header=0, comment="#")
    df.columns = map(str.upper, df.columns)
    is_samplesheet(df, ['VALID_SAMPLE_ID'])
    df[['VALID_SAMPLE_ID', 'PRIMER_BARCODE']].to_csv(
        out_file, index=False, header=False, sep="\t"
    )
    return out_file


def column_from_samplesheet(csv, column_label):
    """Parse the sample names from a validated sample sheet (CSV).

    Args:
        csv (str): sample sheet CSV file path
        column_label (str): label should match column label to grab

    Returns:
        numpy.array

    Raises:
        ValueError when label is missing from the samplesheet.
    """
    df = pd.read_csv(csv, header=0, comment="#")
    df.columns = map(str.upper, df.columns)
    is_samplesheet(df, [column_label.upper()])
    return df[column_label.upper()].values


def pocs_from_samplesheet(csv):
    """Parse the POCs from a validated sample sheet (CSV).

    Args:
        csv (str): sample sheet CSV file path

    Returns:
        numpy.array
    """
    df = pd.read_csv(csv, header=0, comment="#")
    df.columns = map(str.upper, df.columns)
    is_samplesheet(df)
    pocs = df.POC.unique()
    return pocs, [check_sample_id(i) for i in pocs]


def contamination_per_plate(csv, out_file):
    """
    Args:
        csv (str): fully annotated samplesheet file path
        out_file (str): pdf plot of contamination per plate

    Returns:
        str: out file path
    """
    df = pd.read_csv(csv, header=0, comment="#")
    # needs to check for 'positive_control*'
    is_samplesheet(df)
    # identify positive controls
    control_cols = [col for col in list(df) if col.startswith('POSITIVE_CONTROL')]
    df[control_cols] = pd.to_numeric(df[control_cols], errors='coerce')
    # sum across the rows
    df['TOTAL_CONTAMINATION'] = df[control_cols].sum(axis=1)
    # split A1 to 'A' and 1
    df['WELL_ROW'] = df['PRIMER_WELL_POSITION'].apply( lambda x: x[0])
    df['WELL_COL'] = df['PRIMER_WELL_POSITION'].apply( lambda x: int(x[1:]))
    heatmap_by_group(
        df,
        out_file,
        'TOTAL_CONTAMINATION',
        'WELL_ROW',
        'WELL_COL',
        'PRIMER_PLATE_NUMBER',
    )
    return out_file
