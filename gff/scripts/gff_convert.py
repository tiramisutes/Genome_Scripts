#!/usr/bin/env python
"""Convert a GFF and associated FASTA file into GenBank format.
Usage:
    gff_convert.py -f genbank -s <GFF annotation file> <FASTA sequence file>
"""
import sys
import os
from Bio import SeqIO
from Bio.Alphabet import generic_dna
from Bio import Seq
import argparse
from BCBio import GFF

parser=argparse.ArgumentParser(
    description='''Script that converts GFF + Fasta to GBK or EMBL ''',
    epilog="""hope (2019)  http://tiramisutes.github.io/2019/04/05/PBGNCBI.html""")
parser.add_argument("gff", help='GFF file')
parser.add_argument("fasta", help='Fasta file')
parser.add_argument("-f", "--format", choices=['genbank', 'embl'])
parser.add_argument("-s","--split", action='store_true', help='Split output into single files, 1 per contig')
parser.add_argument("-o","--output", help='Set the directory of output file/files')
args=parser.parse_args()

if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)
    

def _fix_ncbi_id(fasta_iter):
    """GenBank identifiers can only be 16 characters; try to shorten NCBI.
    """
    for rec in fasta_iter:
        if len(rec.name) > 16 and rec.name.find("|") > 0:
            new_id = [x for x in rec.name.split("|") if x][-1]
            print "Warning: shortening NCBI name %s to %s" % (rec.id, new_id)
            rec.id = new_id
            rec.name = new_id
        yield rec

def _check_gff(gff_iterator):
    """Check GFF files before feeding to SeqIO to be sure they have sequences.
    """
    for rec in gff_iterator:
        if isinstance(rec.seq, Seq.UnknownSeq):
            print "Warning: FASTA sequence not found for '%s' in GFF file" % (
                    rec.id)
            rec.seq.alphabet = generic_dna
        yield _flatten_features(rec)

def _flatten_features(rec):
    """Make sub_features in an input rec flat for output.
    GenBank does not handle nested features, so we want to make
    everything top level.
    """
    out = []
    for f in rec.features:
        cur = [f]
        while len(cur) > 0:
            nextf = []
            for curf in cur:
                out.append(curf)
                if len(curf.sub_features) > 0:
                    nextf.extend(curf.sub_features)
            cur = nextf
    rec.features = out
    return rec

gff_file = args.gff
fasta_file = args.fasta
format = args.format
output_dir = args.output

if args.split:
    if format == "genbank":
        print("Output set to " + format + ", splitting files and writting individual records to directory: " + output_dir)
        fasta_input = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta", generic_dna))
        for rec in GFF.parse(gff_file, fasta_input):
            SeqIO.write(_check_gff(_fix_ncbi_id([rec])), open(output_dir + "/" + rec.id + ".gbk", "w"), "genbank")
    if format == "embl":
        print("Output set to " + format + ", splitting files and writting individual records to directory: " + output_dir)
        fasta_input = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta", generic_dna))
        for rec in GFF.parse(gff_file, fasta_input):
            SeqIO.write(_check_gff(_fix_ncbi_id([rec])), open(output_dir + "/" + rec.id + ".embl", "w"), "embl")
else:
    if format == "genbank":
        out_file = output_dir + "/%s.gb" % os.path.splitext(os.path.basename(gff_file))[0]
        print("Output set to " + format + ", writing file to " + out_file)
        fasta_input = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta", generic_dna))
        gff_iter = GFF.parse(gff_file, fasta_input)
        SeqIO.write(_check_gff(_fix_ncbi_id(gff_iter)), out_file, "genbank")
    if format == "embl":
        out_file = output_dir + "/%s.embl" % os.path.splitext(os.path.basename(gff_file))[0]
        print("Output set to " + format + ", writing file to " + out_file)
        fasta_input = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta", generic_dna))
        gff_iter = GFF.parse(gff_file, fasta_input)
        SeqIO.write(_check_gff(_fix_ncbi_id(gff_iter)), out_file, "embl")
