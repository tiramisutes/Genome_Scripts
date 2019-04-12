import sys

with open(sys.argv[1], "r") as gtf:
    header = next(gtf)
    last_gene = {
        "gene": None,
        "chr": None,
        "end": None,
    }

    for line in gtf:
        gene, chr, start, end = line.strip().split("\t")[:4]

        if chr != last_gene["chr"]:
            last_gene["gene"] = gene
            last_gene["chr"] = chr
            last_gene["end"] = end

        else:
            print(
                last_gene["chr"],
                last_gene["end"],
                start,
                last_gene["gene"]+"_"+gene,
                sep="\t"
            )

            last_gene = {
                "gene": gene,
                "chr": chr,
                "end": end
            }