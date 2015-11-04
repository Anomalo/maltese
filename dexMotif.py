##!/usr/bin/env python2.7
import os
from optparse import OptionParser
import csv
import glob
from eon import fa
#from eon import dex #this is imported at a later stage as it takes a long time to load
import sys
def err(*vars):
	sys.stderr.write(' '.join(map(str,vars))+'\n')

def check_files(taxon='mus musculus',dir = 'annotations/',version='GRCm38'):
	'''
	checks, downloads and installs annotation files
	'''
	try: os.makedirs(dir)
	except OSError: pass

	#check gtf
	f = glob.glob(dir+'*.gtf')
	if f == []: 
		from eon import gtf
		gtf.getGTF(taxon = taxon, dir = dir)
		reload(gtf)
	#
	fa.set_taxon(taxon=taxon,version=version)	
	
		
def main():
	description='''
	Takes as input a dexseq output file and enriches the loci with motifs
	overrepresented (compared with the rest of the gene)
	dexMotif [options] <dexseq> > <dexseqOutput>

	'''.replace('\n','').replace('\t','')
	parser = OptionParser(description=description)

	parser.add_option('-a','--annotations',
				action='store', type='string',
				dest='annotationsDir',default='annotations',
				help='directory with annotations: the gtf file')

	parser.add_option('-T','--taxon',
				action='store', type='string',
				dest='annotations',default='Mus_musculus',
				help='downloads and generates anotation files of defined taxon -A "Mus_musculus"')

	parser.add_option('-t','--taxon_version',
				action='store', type='string',
				dest='annotation_version',default='GRCm38',
				help='defines what genome version to download, default is "GRCm38"')

	parser.add_option('-p','--purge',
				action='store_true',
				dest='purge', default=False,
				help='delete all anotation files (usefull for changing the taxon of interest)')
	
	parser.add_option('-v','--verbose',
				action='store_true',
				dest ='v', default=True,
				help='shows you what am I thinking')

	parser.add_option('-V','--version',
				action='store_true',
				dest ='version', default=False,
				help='prints version')

	parser.add_option('-m','--Tempfiles',
				action='store_true',
				dest ='tempfiles', default=False,
				help='does not erase temprary files')
	

	(options, args) = parser.parse_args()
	v = options.v
	#output = options.output
	annotations = options.annotations
	annotation_version = options.annotation_version
	annotationDir = options.annotationsDir
	if options.version:
		err('this is version',0)
	
	if options.purge:
		commandOptions ='-rf'
		if v:commandOptions+='v'
		os.system('rm '+commandOptions+annotationDir+'/*')
		check_files(taxon = annotations,version =annotation_version , dir = annotationDir)
	'''
	if annotations != '':
		check_files(taxon = annotations,version =annotation_version , dir = annotationDir)
	'''

	if len(args) == 0:
		parser.print_help()
		return None

	if len(args) > 1:
		err('more than one argument given')
		return None
	
	for dexseqArg in args:
		for dexseq in glob.glob(dexseqArg):
			if v: err('Analyzing',dexseq)
			from eon import dex
			dexMotif = dex.dex(dexseq,v,
						taxon=annotations, 
						version=annotation_version , 
						temp = options.tempfiles,
						annotationDir = annotationDir)
			dexMotif.addMotifs()

if __name__ == '__main__': 
	#check_files()
	main()
'''
        while True:
                try:exec(raw_input('>>>'))
                except Exception as e: print e

'''
