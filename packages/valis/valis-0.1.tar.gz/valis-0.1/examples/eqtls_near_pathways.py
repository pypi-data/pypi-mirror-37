from valis import ValisAPI, Dataset, Genome

client = ValisAPI()


# get the pathway names
q = client.infoQuery().filterType('pathway')
pathways = client.distinctValues('name', q)

# print the data for the first 3 pathways
for pathway in pathways[:3]:

	# query to fetch genes in pathway
	genes_in_pathway = client.genomeQuery().filterType(Genome.GENE).filterPathway(pathway)

	# fetch all eQTL's that are known to modulate genes in this set
	eQTLs = client.edgeQuery().filterSource(Dataset.GTEX).filterMaxPValue(0.01)
	variants = client.genomeQuery().filterType(Genome.SNP).filterSource(Dataset.DBSNP)
	eQTLs_near_pathway = variants.addToEdge(eQTLs.toNode(genes_in_pathway))
	
	# find which of these are within 100bp of roadmap epigenomics annotations in 'Lung': 
	roadmap_annotations = client.genomeQuery().filterSource(Dataset.ROADMAP).filterBiosample('Lung')

	snps_near_annotations = eQTLs_near_pathway.intersect(roadmap_annotations, windowSize=100)

	# fetch the snps near annotations
	print(client.getQueryResults(snps_near_annotations))
