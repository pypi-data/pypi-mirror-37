from valis import ValisAPI, Dataset, Genome

client = ValisAPI()


# all traits
traitQuery = client.infoQuery().filterType('trait')

# all missense variants in ExAC
variantQuery = client.genomeQuery().filterSource(Dataset.EXAC).filterVariantTag('missense_variant')

# GWAS relations are an edge between a variant and a trait
gwasQuery = client.edgeQuery().filterSource(Dataset.GWAS_CATALOG)


# Build graph query fetching variants that have a gwas relation to a trait :
missenseGwasVariants = variantQuery.addToEdge(gwasQuery.toNode(traitQuery))

print(client.getQueryResults(missenseGwasVariants))

