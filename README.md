## Welcome to Genome Scripts

A repository for scripts used in genome project.
![](https://raw.githubusercontent.com/wiki/tiramisutes/blog_image/genome_scripts.png)
## What We can do?
### 1. Change the genome fa and gff3 format file to Genbank [gff]
```
python scripts/gff_convert.py -f genbank -s -o /home/zpxu /home/zpxu/genome/annotation.gff3 /home/zpxu/genome/genome.fa
```
### 2. Preparing genomes for submission to NCBI [WGS2NCBI]
```
cd /home/zpxu/software/wgs2ncbi
./script/wgs2ncbi prepare -conf ./share/wgs2ncbi.ini
./script/wgs2ncbi process -conf ./share/wgs2ncbi.ini
./script/wgs2ncbi convert -conf ./share/wgs2ncbi.ini
./script/wgs2ncbi compress -conf ./share/wgs2ncbi.ini
```
