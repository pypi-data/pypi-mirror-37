from valis import ValisAPI, Genome

client = ValisAPI()

# Get 2nd contig name (note that contig names are in string, not numerical, sorted order)
chr10 = client.contigs()[1]['name']

# Filter the genomic annotations to type 'gene' and contig 'chr10'
q = client.genomeQuery().filterType(Genome.GENE).filterContig(chr10)


print('Running query: %s' % q.json())

# Fetch the genes using cursor, with full information
i = 0
genes = []
while True:
	curr_genes, reached_end = client.getQueryResults(q, startIdx=i, endIdx=i+1000)
	genes += curr_genes
	i += 1000
	if reached_end:
		break

# print total
print('Found %d genes' % len(genes))

