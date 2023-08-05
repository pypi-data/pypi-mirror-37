import os
import csv
import time
import subprocess

import vcf
import xlsxwriter
import pandas as pd

from .targets import TargetDatabase





def get_header(samplesheet):
    "Read samplesheet and find line with Sample_ID. Return integer."
    with open(samplesheet, 'r') as f:
        for i, line in enumerate(f):
            if line.startswith('Sample_ID'):
                return i


def samplesheet_to_sample_genesis(samplesheet):
    """Read samplesheet part with sample info. Use ngsscriptlibrary to get
    targets to use and analyses to perform. Return dict.
    """
    samples = list()
    with open(samplesheet) as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            if i > get_header(samplesheet):
                samples.append(line)
    sample_genesis = list()
    for line in samples:
        sample = line[0]
        genesis = line[-1]
        genesis = genesis.replace('.NGS', '')
        sample_genesis.append((sample, genesis))
    return sample_genesis


def parse_samplesheet_for_pipeline(samplesheet, db, exclude=None):
    """Read samplesheet part with sample info. Use ngsscriptlibrary to get
    targets to use and analyses to perform. Return dict.
    """
    samples = list()
    if exclude is None:
        exclude = list()

    with open(samplesheet) as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            if i > get_header(samplesheet):
                samples.append(line)
    TD = TargetDatabase(db)
    samples_todo = dict()
    for line in samples:
        genesis = line[-1]
        serie = line[-2]
        if genesis in exclude or serie in exclude:
            continue
        genesis = genesis.replace('.NGS', '')
        samples_todo[line[0]] = TD.get_todo(genesis)
        samples_todo[line[0]]['serie'] = serie
        samples_todo[line[0]]['genesis'] = genesis
        vcapture = samples_todo[line[0]]['capture']
        oid = TD.get_oid_for_vcapture(vcapture)
        samples_todo[line[0]]['oid'] = oid
    return samples_todo


def get_rs_gpos_dict():
    rs_gpos_dict = dict()
    basedir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(basedir, 'docs', 'snpcheck.csv')) as f:
        reader = csv.reader(f)
        for line in reader:
            rs, locus, _genotype = line
            rs_gpos_dict[rs] = locus
            rs_gpos_dict[locus] = rs
    return rs_gpos_dict


def parse_sangers(sangerfile):
    """Read file into dataframe. Create a dict with loci as keys and WT, HET
    or HOM as value. Return a dict.
    """
    sanger = dict()
    sangerout = pd.read_csv(sangerfile, sep='\t')
    sangerout.set_index('mut Effect', inplace=True)

    for locus in sangerout.index:
        if str(locus) == 'nan':
            next
        elif 'het' in sangerout.loc[locus]['Nuc Change']:
            sanger[locus] = 'HET'
        elif 'homo' in sangerout.loc[locus]['Nuc Change']:
            sanger[locus] = 'HOM'
        elif ('het' not in sangerout.loc[locus]['Nuc Change'] and
              'homo' not in sangerout.loc[locus]['Nuc Change']):
            sanger[locus] = 'WT'
    return sanger


def parse_taqman(taqmanfile):
    """Parse CSV file with rsID, genotype info. Create a dict with rsID as keys
    and WT, HET, HOM or NoTaqman (no call) as value. Return a dict.
    """
    rsid_to_locus = get_rs_gpos_dict()
    taqman = dict()
    with open(taqmanfile, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            rs, call = line
            if rs.endswith(')'):
                rs = rs.split(' ')[0]
            else:
                rs = rs.rsplit()[0]
            if call != 'WT' and call != 'HET' and call != 'HOM':
                call = 'NoTaqMan'
            locus = rsid_to_locus[rs]
            taqman[locus] = call
    return taqman


def parse_ngssnpcheck(ngssnpcheck):
    """Parse vcf with vcfreader. Create a dict with loci as key and WT, HET,
    HOM or NC (no coverage) as value. Return a dict.
    """
    d = dict()
    d['0/0'] = 'WT'
    d['0/1'] = 'HET'
    d['1/1'] = 'HOM'
    d['./.'] = 'NC'

    ngsdict = dict()
    vcfreader = vcf.Reader(open(ngssnpcheck, 'r'))

    for record in vcfreader:
        for call in record:
            if d[call['GT']] == 'NC' and record.INFO['DP'] > 29:
                ngsdict['{}:{}'.format(record.CHROM, record.POS)] = 'WT'
            else:
                ngsdict['{}:{}'.format(record.CHROM,
                                       record.POS)] = d[call['GT']]
    return ngsdict


def compare_snpchecks(sangerdict, ngsdict):
    """Compare values from 2 dicts with overlapping keys. NGS-dict contains
    all keys from sangerdict. Create dict with loci as keys and ok or ERROR as
    values. Ok when both values are the same, ERROR if not. Return a dict.
    """
    out = dict()
    for k, v in sangerdict.items():
        try:
            if ngsdict[k] == v:
                out[k] = 'ok'
            elif ngsdict[k] != v:
                out[k] = 'ERROR'
        except KeyError:
            out[k] = 'NoNGS'
        if v == 'NoTaqMan':
            out[k] = 'NoTaqMan'
    return out


def print_extra_ngscalls(compfile, extrangsfile):
    with open(extrangsfile) as fin, open(compfile, 'a') as fout:
        for line in fin:
            line.strip()
            fout.write(line)


def read_summary(summary):
    "Parse GATK CallableLoci summary. Return dict."
    d = dict()
    with open(summary, 'r') as f:
        next(f)
        for line in f:
            x, y = line.lstrip().split()
            d[x] = y
    return d


def get_line(picardfile, phrase):
    """Read file. Report line number that starts with phrase and the first
    blank line after that line. Return tuple of integers
    """
    with open(picardfile, 'r') as f:
        start = 1000
        end = 1000
        for i, line in enumerate(f):
            if line.startswith(phrase):
                start = i
            if line.startswith('\n'):
                end = i
            if start < end:
                return (start, end)


def readmetrics(sampleID, serie, metrics):
    "Read block (line x through y) from file with pandas. Return dataframe."
    start, end = get_line(metrics, '## METRICS CLASS')
    df = pd.read_csv(metrics, sep='\t', header=start, nrows=end - start - 2)
    df['SAMPLE'] = sampleID
    df['SERIE'] = serie
    df.set_index(['SAMPLE', 'SERIE'], inplace=True)
    return df


def parse_bed_to_loci(target):
    "Read BED file and create chr:pos for each targetbase. Return list."
    loci = list()
    with open(target) as f:
        for line in f:
            chromosome, start, end, *_ = line.split()
            start = int(start)
            end = int(end)
            while start <= end:
                locus = '{}:{}'.format(chromosome, start)
                loci.append(locus)
                start += 1
    return loci


def calc_perc_target_covered(docfile, filter_regions=False, target=None):
    """Calculate targetpercentage covered with >30 reads from GATK's
    DepthOfCoverage output. Filter regions if requested. Return float.
    """
    df = pd.read_csv(docfile, usecols=['Total_Depth', 'Locus'],
                     sep='\t', index_col='Locus')
    if filter_regions:
        loci = parse_bed_to_loci(target)
        df = df.loc[loci]
    return float((1 - df[df['Total_Depth'] < 30].count() / df.count()) * 100)


def annotate_callables(bed, annottarget, tempbed):
    "Intersect annotated target with callable region. Return dataframe."
    bash = 'bedtools intersect -wa  -a {} -wb -b {} > {}'.format(
        annottarget, bed, tempbed)
    subprocess.call(bash, shell=True)
    try:
        df = pd.DataFrame.from_csv(tempbed, sep='\t', header=None,
                                   index_col=None)
    except pd.io.common.EmptyDataError:
        return pd.DataFrame()
    else:
        df = df.drop([4], axis=1)
        df.columns = ['chromosome', 'targetstart', 'targetend',
                      'gene', 'regionstart', 'regionend', 'callable']

        integerlist = ['targetstart', 'targetend',
                       'regionstart', 'regionend']

        df[integerlist] = df[integerlist].apply(pd.to_numeric)
        df['regionsize'] = df['regionend'] - df['regionstart']
        df['targetsize'] = df['targetend'] - df['targetstart']
        df.set_index(['chromosome', 'targetstart', 'targetend'], inplace=True)
        return df


def get_basecounts(fastq):
    """Use subprocess/bash to get all bases from a fastq in a string.
    Count A, C, G, T and divide by total length of string. Return tuple.
    """
    if fastq.endswith('.gz'):
        bash = "zcat {} | paste - - - - | cut -f 2 | tr -d '\n'".format(fastq)
    else:
        bash = "cat {} | paste - - - - | cut -f 2 | tr -d '\n'".format(fastq)

    proc = subprocess.Popen(bash,
                            stdout=subprocess.PIPE,
                            shell=True)

    out, _err = proc.communicate()
    out = str(out)

    countA = float(out.count('A') / len(out))
    countT = float(out.count('T') / len(out))
    countC = float(out.count('C') / len(out))
    countG = float(out.count('G') / len(out))

    return(countA, countT, countC, countG)


def get_base_count_filelist(outputfile, filelist):
    "Feed all fastqs in filelist and combine output."

    if len(filelist) == 0:
        return 'No fastq R1 files found'

    else:
        counts = [(pd.DataFrame({f: get_basecounts(f)},
                                index=['A', 'T', 'C', 'G']
                                )
                   ) for f in filelist if 'R2' not in f]

        df = pd.concat(counts, axis=1).transpose()
        df.index = [path.split('/')[-1] for path in df.index]
        df.index = [fn.split('_')[0] for fn in df.index]
        df.to_csv(outputfile, sep='\t')


def standaardfragmenten_naar_df(excelfile):
    "Read excel with standard fragments into dataframe and return dataframe"
    try:
        df = pd.read_excel(excelfile, sheet_name=2)
    except IndexError:
        return pd.DataFrame()
    else:
        df['chr.'] = df['chr.'].astype('int32')
        df['primer min'] = df['primer min'].astype('int32')
        df['primer max'] = df['primer max'].astype('int32')
        df['fragment min'] = df['fragment min'].astype('int32')
        df['fragment max'] = df['fragment max'].astype('int32')
        df.set_index(['FRACTIENR'], inplace=True)
        df.sort_index(inplace=True)
        return df


def standaardfragmenten_dict_sample(sample, df):
    "Turn dataframe with standard fragments into per patientdict and return dict"
    try:
        std_frag_df = df.loc[sample].fillna('Geen score')
    except KeyError as e:
        print(e)
        std_frag_dict = dict()
    else:
        std_frag_dict = std_frag_df.reset_index().to_dict('records')
    return std_frag_dict
