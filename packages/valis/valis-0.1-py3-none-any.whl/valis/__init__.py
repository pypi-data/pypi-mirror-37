import json
import requests

from enum import EnumMeta

class Genome(EnumMeta):
  VARIANT = 'variant'
  SNP = 'SNP'
  GENE = 'gene'
  # TODO : Finish listing all types

class FileType(EnumMeta):
  TXT_23ANDME = '23andme'
  VCF = 'vcf'
  BED = 'bed'

class QueryType(EnumMeta):
  GENOME = 'GenomeNode'
  INFO = 'InfoNode'
  EDGE = 'EdgeNode'

class Dataset(EnumMeta):
  GENOME = 'GRCh38_gff';
  GWAS_CATALOG = 'GWAS Catalog';
  CLINVAR = 'ClinVar';
  DBSNP = 'dbSNP';
  ENCODE_ANNOTATIONS = 'ENCODE';
  ROADMAP = 'Roadmap Epigenomics';
  FASTA = 'RefSeq';
  EFO = 'EFO';
  ENCODE_BIGWIG = 'ENCODEbigwig';
  EXAC = 'ExAC';
  TCGA = 'TCGA';
  ENSEMBL = 'ENSEMBL';
  GTEX = 'GTEx';


class QueryBuilder:
  def __init__(self):
    self.query = None

  def duplicate(self):
    copy = QueryBuilder()
    copy.query = json.loads(self.json())
    return copy

  def newGenomeQuery(self):
    self.query = {
      'type': QueryType.GENOME,
      'filters': {},
      'toEdges': [],
      'arithmetics': [],
    }
    return self

  def newInfoQuery(self):
    self.query = {
      'type': QueryType.INFO,
      'filters': {},
      'toEdges': [],
      'arithmetics': [],
    }
    return self

  def newEdgeQuery(self):
    self.query = {
      'type': QueryType.EDGE,
      'filters': {},
      'toEdges': [],
      'arithmetics': [],
    }
    return self

  def filterID(self, id):
    copy = self.duplicate()
    copy.query['filters']['_id'] = id;
    return copy

  def filterType(self, type):
    copy = self.duplicate()
    copy.query['filters']['type'] = type;
    return copy
  
  def filterSource(self, source):
    copy = self.duplicate()
    copy.query['filters']['source'] = source;
    return copy
  
  def filterContig(self, contig):
    if (self.query['type'] != QueryType.GENOME):
      raise 'filter contig only available for GenomeNodes';
    copy = self.duplicate()
    copy.query['filters']['contig'] = contig;
    return copy
  
  def filterLength(self, length):
    if (self.query.type != QueryType.GENOME):
      raise 'Length only available for GenomeNodes';
    
    copy = self.duplicate()
    copy.query['filters']['length'] = length;
    return copy
  
  def filterName(self, name):
    copy = self.duplicate()
    copy.query['filters']['name'] = name;
    return copy
  
  def filterPathway(self, pathways):
    copy = self.duplicate()
    copy.query['filters']['info.kegg_pathways'] = pathways;
    return copy
  
  def filterMaxPValue(self, pvalue):
    copy = self.duplicate()
    copy.query['filters']['info.p-value'] = { '<': pvalue };
    return copy
  
  def filterBiosample(self, biosample):
    copy = self.duplicate()
    if type(biosample) == list :
      copy.query['filters']['info.biosample'] = { '$in' : biosample };
    else:
      copy.query['filters']['info.biosample'] = biosample;
    return copy
    
  def filterTargets(self, targets):
    if len(targets):
      copy = self.duplicate()
      copy.query['filters']['info.targets'] = { '$all': targets };
    return copy
    
  def filterInfotypes(self, type):
    copy = self.duplicate()
    copy.query['filters']['info.types'] = type;
    return copy
  
  def filterAssay(self, assay):
    copy = self.duplicate()
    copy.query['filters']['info.assay'] = assay;
    return copy
  
  def filterOutType(self, outType):
    copy = self.duplicate()
    copy.query['filters']['info.outtype'] = outType;
    return copy
  
  def filterPatientBarCode(self, outType):
    copy = self.duplicate()
    copy.query['filters']['info.patient_barcodes'] = outType;
    return copy
  
  def filterStartBp(self, start):
    if self.query['type'] != QueryType.GENOME:
      raise 'filterStartBp is only available for an Genome Query.';
    
    copy = self.duplicate()
    copy.query['filters']['start'] = start;
    return copy
  
  def filterEndBp(self, end):
    if self.query['type'] != QueryType.GENOME:
      raise 'filterEndBp is only available for an Genome Query.';
    copy = self.duplicate()
    copy.query['filters']['end'] = end;
    return copy
  
  def filterAffectedGene(self, gene):
    previous = self.query['filters']['variant_affected_genes'] or [];
    copy = self.duplicate()
    copy.query['filters']['info.variant_affected_genes'] = gene;
    return copy
  
  def filterVariantTag(self, tag):
    copy = self.duplicate()
    if type(tag) == list:
      copy.query['filters']['info.variant_tags'] = { '$in' : tag };
    else:
      copy.query['filters']['info.variant_tags'] = tag;
    return copy

  def searchText(self, text):
    copy = self.duplicate()
    copy.query['filters']['$text'] = text;
    return copy

  def setLimit(self, limit):
    self.query['limit'] = limit;
    return copy

  def get(self):
    return self.query

  def json(self):
    return json.dumps(self.query)
 
  def __str__(self):
    return json.dumps(self.query)

  def isGwas(self):
    return False

  def addToEdge(self, edgeQuery):
    if (self.query['type'] == QueryType.EDGE):
      raise 'Edge can not be connected to another edge.';
    copy = self.duplicate()
    copy.query['toEdges'].append(edgeQuery.get());
    return copy

  def toNode(self, nodeQuery, reverse=False):
    if (self.query['type'] != QueryType.EDGE):
      raise 'toNode is only available for an Edge Query.';
    copy = self.duplicate()
    copy.query['toNode'] = nodeQuery.get();
    copy.query['reverse'] = reverse;
    return copy


  def intersect(self, genomeQuery, windowSize=None):
    if (self.query['type'] != QueryType.GENOME):
      raise 'Arithmetic is only available for an Genome Query.'
    ar = {
      'operator': 'intersect',
      'target_queries': [genomeQuery.get()],
    }
    if (windowSize != None):
      ar['windowSize'] = int(windowSize)
      ar['operator'] = 'window'
    copy = self.duplicate()
    copy.query['arithmetics'].append(ar);
    return copy

  def union(self, queries):
    if type(queries) != list:
      queries = [queries.get()]
    else:
      queries = [query.get() for query in queries]
    ar = {
      'operator': 'union',
      'target_queries': queries,
    }
    copy = self.duplicate()
    copy.query['arithmetics'].append(ar);
    return copy

  def diff(self, queries):
    if type(queries) != list:
      queries = [queries.get()]
    else:
      queries = [query.get() for query in queries]
    ar = {
      'operator': 'diff',
      'target_queries': queries,
    }
    copy = self.duplicate()
    copy.query['arithmetics'].append(ar);
    return copy

class ValisAPI:
    def __init__(self, ip='http://35.185.230.75', username=None, password=None):
        self.apiUrl = ip
        pass

    def genomeQuery(self):
        return QueryBuilder().newGenomeQuery()

    def infoQuery(self):
        return QueryBuilder().newInfoQuery()

    def edgeQuery(self):
        return QueryBuilder().newEdgeQuery()

    def contigs(self):
        return json.loads(requests.get('%s/contig_info' % self.apiUrl).content)

    def getUploadedFiles(self):
        return json.loads(requests.get('%s/user_files' % self.apiUrl).content)

    def getDetails(dataID, userFileID=None):
        requestUrl = '%s/details/%s' % (self.apiUrl, dataID);
        if (userFileID):
            requestUrl = requestUrl + "?userFileID=" + userFileID;
        return json.loads(requests.get(requestUrl).content)

    def distinctValues(self, key, query):
        requestUrl = '%s/distinct_values/%s' % (self.apiUrl, key);
        return json.loads(requests.post(requestUrl, json=query.get()).content)

    def uploadFile(self, file_path):
        url = '%s/user_files' % self.apiUrl
        files = {'file': open(file_path, 'rb'), 'fileType' : file_type}
        return requests.post(url, files=files)


    def downloadQuery(self, query, output_path, sort=False):
        requestUrl = '%s/download_query' % self.apiUrl
        result = requests.post(requestUrl, json={ 'query': query.get(), 'sort': sort}).content
        with open(output_path, "wb") as f:
            f.write(result)

    def getQueryResults(self, query, full=False, startIdx=None, endIdx=None):
        requestUrl = '%s/query/basic' % self.apiUrl
        if (full):
            requestUrl = '%s/query/full' % self.apiUrl;

        if (query.isGwas()):
            requestUrl = '%s/query/gwas' % self.apiUrl;

        options = [];
        if (startIdx != None):
            options.append('result_start=%d' % startIdx);

        if (endIdx != None):
            options.append('result_end=%d' % endIdx);

        if (len(options)):
            requestUrl = requestUrl + '?' + '&'.join(options)

        result = json.loads(requests.post(requestUrl, json=query.get()).content)
        return result['data'], result['reached_end']



