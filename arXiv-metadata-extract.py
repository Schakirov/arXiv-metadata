"""
arXiv-metadata-extract.py --- 25 June 2016
-------------------------------------------------
This script has been coded for Python3.
This script downloads metadata from the arXiv.  For the moment it's set to pull data from physics:quant-ph. The arXiv participates in the Open Archives Initiative (OAI; http://www.openarchives.org/).  Requests can be made to the URL http://export.arxiv.org/oai2, returning metadata in XML format.

The metadata consists of the following entries:
	dc:title
	dc:creator (authors)
	dc:subject (keywords)
	dc:description (abstract)
	dc:date (date of submission)
	dc:identifier (final publishing locations)

Each article entry is referred to as a <Record>, and the entire list is within the structure of <ListRecords>.
They restrict queries to 1k records.  As of 25 June 2016 there were around 73768 total records dating back to 1992 (average of 3k records per year over 25 years).  Each 1k block of XML data occupies about 1.7MB.  A resumptionToken allows us to pick up the query where we left off.  When the token return is empty, we've reached the end of our query.
OAI2 allows to specify the date range of entries using <datestamp>, but note that this is the date of the metadata update, not the article submission date.  The entire metadata set was updated in 1 April 2007.  I've decided to break up the XML data into 3 year blocks -- block1: 2007-2009, block2: 2010-2012, block3: 2013-2015, block4: 2016

Some future improvements:
- pull out information on how many total records are available.
- error handling in the event of OAI2 server complaints
"""
#################################################################################################
#################################################################################################
import urllib.request
import time
from itertools import chain
from xml.dom import minidom
import sys

#################################################################################################
#################################################################################################

## blocks of data based on metadata update date
fname = 'arXiv-articles.xml'; queryDate='from=2019-09-03&until=2019-09-04';

if len(sys.argv) == 2:
    queryDate='from=' + sys.argv[1] + '&until=' + sys.argv[1];
if len(sys.argv) == 3:
    queryDate='from=' + sys.argv[1] + '&until=' + sys.argv[2];

#################################################################################################
#################################################################################################
## initial http request to OA server 
url = 'http://export.arxiv.org/oai2?verb=ListRecords&set=cs&metadataPrefix=oai_dc&{}'.format(queryDate)
## setup XML file, write header
f=open(fname,'w')
f.write('<ListRecords>\n')
## start pulling in data, 1000 entries at a time.  
token = 'dummy'
indEnd = 31415
i=0
while (token != '') and (indEnd > -1):
	i+=1
	print('Executing HTTP query {}'.format(i))
	print('indEnd = ' + str(indEnd))
	rawData = str(urllib.request.urlopen(url).read())

	## find indicies to extract token and chop data
	indStart=rawData.find('<record>')
	indEnd=rawData.find('<resumptionToken')
	indToken1=rawData.find('>',indEnd)
	indToken2=rawData.find('<',indToken1)	

	## write to file
	f.write(rawData[indStart:indEnd]) ## if no resumptionToken,  then almost to end (except one char)
	## find resumption token
	if indEnd > -1:
            token=rawData[indToken1+1:indToken2]
            print('\tResumption token = {}'.format(token))
            url = 'http://export.arxiv.org/oai2?verb=ListRecords&resumptionToken={}'.format(token)	
            ## wait 20 seconds to keep OAI2 happy
            time.sleep(20)

#################################################################################################
#################################################################################################
## write XML footer and close file
f.write('</ListRecords>\n')
f.close()

#################################################################################################
#################################################################################################
## parse XML data and test some outputs
## data = minidom.parse(fname)
## titles = data.getElementsByTagName("dc:title")
## for i in chain(range(0,10), range(1000,1010)):
##	print (titles[i].firstChild.data)
