#!/usr/bin/perl

=head1 NAME
A scripts for remove the duplicate sequences from a FASTA files that have sequences with different IDs that nonetheless have the same sequence and presence of duplicate;

Downloaded from http://www.bioinformatics-made-simple.com

USAGE: removerep.pl input.fa output.fa
=cut

use strict;
use Bio::SeqIO;
my %unique;

my $file   = $ARGV[0];
my $outfile = $ARGV[1];

my $seqio  = Bio::SeqIO->new(-file => $file, -format => "fasta");
my $outseq = Bio::SeqIO->new(-file => ">$outfile", -format => "fasta");

while(my $seqs = $seqio->next_seq) {
  my $id  = $seqs->display_id;
  my $seq = $seqs->seq;
  unless(exists($unique{$seq})) {
    $outseq->write_seq($seqs);
    $unique{$seq} +=1;
  }
}


print "Please to check the results file : $outfile \n";