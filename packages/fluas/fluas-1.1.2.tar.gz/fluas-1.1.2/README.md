# `fluas`
Next-gen data processing and quality control procedures.

# Dependencies
+ [python 3](https://www.continuum.io/downloads)
+ [bwa](https://github.com/lh3/bwa)
+ [samtools](https://github.com/samtools/samtools)
+ [fastq-multx](https://github.com/brwnj/fastq-multx)
+ [fastq-join](https://github.com/brwnj/fastq-join)

# Install

If you already have `python3` and want to install dependencies manually:

```
git clone https://brow015@stash.pnnl.gov/scm/~brow015/fluas.git
cd fluas
python setup.py install
```

Or if you have `conda`, you can create `fluas-env` with all of the
prerequisite software, including `python` and its requirements, for this
workflow:

```
git clone https://brow015@stash.pnnl.gov/scm/~brow015/fluas.git
cd fluas
conda env create
source activate fluas-env
python setup.py install
```

`source deactivate` will leave that environment when you're finished.

# Multiplexed Data

Barcodes are expected as tab delimited text with columns sample then barcode.

## `barcode-stats`

```
fluas barcode-stats --counts counts.csv --stats stats.csv <runid> <r1> <barcodes>
```

Head of `counts.csv`:

| Barcode    | Sample | Count | RunID |
|------------|--------|-------|-------|
|CAAGTGAAGGGA|s6EC9-0 |68069  |run001 |
|GAAATCTTGAAG|s89E5-18|65932  |run001 |
|TAATCGGTGCCA|s6EC9-82|63971  |run001 |
|GACTCAACCAGT|s23EB-82|63003  |run001 |

Head of `stats.csv`:

|RunID |OnTarget          |OffTarget|Unmatched         |GiniCoefficient|
|------|------------------|---------|------------------|---------------|
|run001|0.6927980851807003|NA       |0.3072019148192997|0.25596616952  |

As off target is unknown, it's recorded as NA.

## Carry-over Contamination
To check for carry-over contamination across the 515 forward primer list, we
supply the table with values for the following:

| Plate Name(s) | Plate Number | Well Position | Sequence Name | Sequence | Barcode |
|---------------|--------------|---------------|---------------|----------|---------|
|IL_515fBC...   |Plate 1       |	       A1  |515rcbc_JedA...|AATGATA...|AGCCTT...|

**TODO**: This input really needs to be more generalized in the future.

```
fluas barcode-stats --master 515f_barcode_list_OCT2014.txt \
    --counts counts.csv \
    --stats stats.csv \
    <runid> <r1> <barcodes>
```

That will alter `counts.csv` to:

|Barcode     |Plate Name(s)|Plate Number|Well Position|Sequence Name|Sequence|Sample  |Count|RunID |
|------------|-------------|------------|-------------|-------------|--------|--------|-----|------|
|CAAGTGAAGGGA|IL_515f...   |Plate 1     |B10          |515rcbc_Je...|AATGA...|s6EC9-0 |68069|run001|
|GAAATCTTGAAG|IL_515f...   |Plate 1     |C11          |515rcbc_Je...|AATGA...|s89E5-18|65932|run001|
|TAATCGGTGCCA|IL_515f...   |Plate 1     |B12          |515rcbc_Je...|AATGA...|s6EC9-82|63971|run001|

And `stats.csv` to:

|RunID |OnTarget|OffTarget|Unmatched|GiniCoefficient|
|------|--------|---------|---------|---------------|
|run001|0.692798|6.748e-05|0.3071344|0.25596616     |

## `demultiplex`

```
fluas demultiplex --out-dir reads --stats <stats> --dist-plot <pdf> -m 0 \
    <barcodes> <r1>
```

Runs `fastq-multx` and gives:

```
sample_files/
├── sample1_R1.fastq
├── sample1_R2.fastq
└── ...
```

Stats output looks like:

|Id                   |Count|File(s)                          |
|---------------------|-----|---------------------------------|
|B10-256-PO-H2O-3W-cec|0    |B10-256-PO-H2O-3W-cec_R1.fastq...|
|B10-264-PO-Abx-3W-cec|0    |B10-264-PO-Abx-3W-cec_R1.fastq...|

Distribution of reads across samples is summarized by a Lorenz curve:

<img src="http://imgur.com/3YHGeu1.png" width="600" height="450"/>

# Read Joining

```
fluas join-reads <r1> <r2> <joined fastq>
```

Reads are joined using `fastq-join`. Output files include:

+ prefix_lengths.txt
    + list of read join lengths
+ prefix_stats.txt
    + text file with the following:
        + total reads
        + total joined
        + average join len
        + stdev join len
        + version

# Cross-over Contamination

Check FASTQs against reference FASTAs and build statistics table
containing contamination hits per sample.

```
fluas cross-over -r <references> <fastq> <alignment stats> <affected reads>
```

You end up with an alignment stats table something like:

|Sample  |bsubtilis_v4|cytophaga_v4|metallosphaera_v4|phiX|
|--------|------------|------------|-----------------|----|
|B3CD-0  |4           |0           |0                |8   |

`--overlap` defines the required overlap fraction per read to be considered

`--identity` is the required mapping fraction of the overlapping section
