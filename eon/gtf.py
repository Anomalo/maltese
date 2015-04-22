import urllib
import cPickle as pickle
import os

def getGTF(taxon='Mus musculus',release=78, dir='annotations/'):
	taxon = taxon.lower().replace(' ','_')
	url = 'ftp://ftp.ensembl.org/pub/release-'+str(release)+'/gtf/'+taxon+'/'
	response = urllib.urlopen(url).read()
	responselines = response.splitlines()
	for line in responselines:
		if '.gtf.gz' in line:
			fname = line.split()[-1]
			URL = url+fname

	os.system('clear')
	os.system(' '.join(['wget',
		URL,
		'-P',
		dir]))
	os.system(' '.join(['gunzip',
		dir+fname,
		'-d',
		dir]))

class gtf:
    def _splitLine(self,line,header):
        '''
        Given a ta delaminated string, and a header list, it returns a 
        dictionary with headers as keys
        '''
        line = line.replace('"','')
        line = line.split('\t')
        if len(line[0])<3:
            line[0] = 'chr'+line[0]
        for i in range(len(line)):
            try: line[i] = int(line[i])
            except: pass
        line = dict(zip(header, line))
        attr = line['attribute'].split('; ')
        for at in attr:
            attName, attVal = at.split(' ')
            line.update({attName: attVal})
        del line['attribute']
        return line
    
    def __init__(self, f = None):
        '''
        object to get fast queries regarding gtf data
        f = gtf file
        '''
                
        if f == None:
            f = self.readCONFIG()
        f = open(f,'r')
        self.header = ['seqname',
                       'source',
                       'feature',
                       'start',
                       'end',
                       'score',
                       'strand',
                       'frame',
                       'attribute']
        bigGTFlistdict = []
        n =0
        while True:
            line = f.readline()
            n+=1
            if line == '': break
            if line[0]!='#':
                if 'exon' == line.split('\t')[2]:
                    bigGTFlistdict.append(self._splitLine(line, self.header))
        self.bigGTFlistdict = bigGTFlistdict
        chrDict = {}
        for line in bigGTFlistdict:
            chromosome = line['seqname']
            if not chromosome in chrDict:
                chrDict.update({chromosome:[]})
            chrDict[chromosome].append(line)
        self.chrDict = chrDict
        self.bigGTFdict={}
        self.names_transcripts = {}
        for line in self.bigGTFlistdict:
            if not line['transcript_name'] in self.bigGTFdict:
                self.bigGTFdict.update({line['transcript_name'].upper():line})
            name  = line['gene_name']
            if not name.upper() in self.names_transcripts:
                self.names_transcripts.update({name.upper():[]})
            self.names_transcripts[name.upper()].append(line['transcript_name'].upper())
        #orders and cleans self.names_transcripts
        for i in self.names_transcripts:
            self.names_transcripts[i] =  sorted(set(self.names_transcripts[i]))
    def readCONFIG(self, fname = 'config.txt'):
        '''
        return GTF file acording to config file, a string of the .gmt file name from 
        the config.txt file
        '''
        f = open(fname, 'r')
        exec(f.read())
        f.close()
        GTF = 'annotations/' + GTF
        return GTF


    def getGene(self, chromosome, start, end):
        '''
        given chromosome, start, and end of a gene it returns the 
	gene attributes
        '''
        chromosomeGenes = self.chrDict[chromosome]
        for line in chromosomeGenes:
            lstart = line['start']
            lend = line['end']
            if lstart<=start<=lend or lstart<=end<=lend:
                return line   
    def getExon(self, transcriptName):
        '''
        given a transcript name it returns the GFT data of that transcript in a 
        dictionaty.
        '''
        return self.bigGTFdict[transcriptName.upper()]
    def transcriptNames(self, gene):
        '''
        given a gene name it returns a list of transcript names (exon specific)
        '''
	if gene.upper() in self.names_transcripts:

	        return (self.names_transcripts[gene.upper()])
	else: return []

    def getTranscriptCoords(self,transcript):
        '''
        Given a transcript name, it returns a tuple (chromosome, start, end)
        '''
        data = self.getExon(transcript)
        return (data['seqname'].replace('chr',''),
                int(data['start']),
                int(data['end']),
		data['strand'])

    def getGeneList(self):
        '''
        returns a list of all the genes
        '''
        genes = []
        for i in self.bigGFTlistdict:
            genes.append(i['gene_name'])
        return sorted(set(genes))

try:
    def purge():
        '''redoes thr GTF object'''
        GTF = gtf()
        pickle.dump(GTF,open('annotations/gtf.p','wb'))    
    def getGene(chromosome, start, end):
        '''
        given chromosome, start, and end of a gene it returns the
        gene attributes
        '''
        return GTF.getGene(chromosome, start, end)

    def getExon(transcriptName):
        '''
        given a transcript name it returns the GFT data of that transcript in a 
        dictionaty.
        '''
        return GTF.getExon(transcriptName)

    def transcriptNames(gene):
        '''
        given a gene name it returns a list of transcript names (exon specific)
        '''
        return GTF.transcriptNames(gene)

    def getTranscriptCoords(transcript):
        '''
        given a transcript name, it returns a tuple (chromosome, start, end)
        '''
        return GTF.getTranscriptCoords(transcript)

    def getGeneList():
        '''
        returns a list of all the genes
        '''
        return GTF.getGeneList()
    GTF = gtf()
except:print 'could not load'
    

if __name__ == '__main__':
    while True:
        try:exec(raw_input('>>>'))
        except Exception as e: print e

