###
### CREATE XML FOR SCANS
###


from xml.etree import ElementTree as ET
import re, csv
import glob
import os
from os import listdir

mydir = '/mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_complets/Publications/'
# /mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_import/FondsArchive/
o = open('imagesAll.xml', 'w')



###################################
## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
###################################
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')


    
###################################
#### REGISTERING NAMESPACES
###################################
NS_ROUD = "http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" 
NS_KNORAIMPORT = "http://api.knora.org/ontology/knoraXmlImport/v1#"
ET.register_namespace("p0112-roud-oeuvres", NS_ROUD)
ET.register_namespace("knoraXmlImport", NS_KNORAIMPORT)


###################################
## DEFINE ELEMENTS WITH NS
###################################
PageNS = ET.QName(NS_ROUD, "Page")
labelNS = ET.QName(NS_KNORAIMPORT, "label")
fileNS = ET.QName(NS_KNORAIMPORT, "file")
hasSeqnumNS = ET.QName(NS_ROUD, "hasSeqnum")
pageHasNameNS = ET.QName(NS_ROUD, "pageHasName")
pageIsPartOfPublicationNS = ET.QName(NS_ROUD, "pageIsPartOfPublication")
PublicationNS = ET.QName(NS_ROUD, "Publication")





###################################
## PREPARE CONTENT OF ELEMENTS AND ATTRIBUTES
###################################

'''

example
    /mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_import/Publications/pub_Roud Gustave_Adieu_Servir_1947-05-29/pub_Roud Gustave_Adieu_Servir_1947-05-29_p1_1.tif

    id = pub_Roud Gustave_Adieu_Servir_1947-05-29_p1_1.tif
    label = page_pub_Roud Gustave_Adieu_Servir_1947-05-29_p1_1
    hasSeqnum = 1
    pageHasName = p. 1
    pubIri = iri
'''

dirs = os.listdir(mydir)
for eachDir in dirs:
    eachPath = mydir+eachDir+'/*.tif'  ## attenzione *.tif or *.png
    allTif = glob.glob(eachPath)
    for eachTif in allTif:
        print(eachTif)
        tifCompletePath = eachTif
        eachTif_splitted = os.path.split(eachTif)
        tifName = eachTif_splitted[1]
        tifHead = eachTif_splitted[0]
            
        
        ## -----------------------> Page/@id
        tifId = tifName.replace(" ", "")
    
        ## -----------------------> file/@path
        filePath = tifCompletePath
        
        ## -----------------------> hasSeqnum
        seqnum = tifName.rsplit('_',1)[1].split('.',1)[0]
        
        ## -----------------------> pageHasName
        simpleName = tifName.rsplit('_',1)[0].rsplit('_',1)[1]
        if re.match(r'\d', simpleName):
            completeName = 'f. '+simpleName
        if re.match(r'p', simpleName):
            completeName = 'p. '+simpleName.split('p')[1]
        if re.match(r'annexe', simpleName):
            completeName = 'annexe '+simpleName.split('annexe')[1]
        if re.match(r'couv1', simpleName):
            completeName = 'annexe '+simpleName.split('annexe')[1]
            # TO BE ADDED WHEN COMPLETING IMAGES IMPORT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # if starts with couv
            # if starts with doc (a volte ha anche ff., a volte no)

        
        ## -----------------------> pageIsPartOfPublication
        labelAsInScan = tifName.rsplit('_', 2)[0]

        
        
        # csv downloaded from sparql query (query saved in graphdb). First column: iri, second column: cote 
        # attention to delimiter for reading csv
        with open("pub_iri_label.csv", 'r') as csv_iri_label:     
            iri_label = csv.reader(csv_iri_label, delimiter =',', doublequote=True)
            for row in iri_label:
                if (labelAsInScan == row[1]):
                    scanPubTarget = row[0]
    

        ## -----------------------> label
        scanLabel = "page_" +labelAsInScan+ "_" +completeName+ "_" +seqnum
        
    
    
        ###################################
        ## CREATE ELEMENTS AND ATTRIBUTES (AS PREVIOUSLY DEFINED WITH NS) AND ASSIGN THEM CONTENT
        ###################################


        Page = ET.Element(PageNS, attrib={'id':tifId}) 
        
        label = ET.SubElement(Page, labelNS)
        label.text = scanLabel
    
        file = ET.SubElement(Page, fileNS, attrib={'path':filePath, 'mimetype':'image/tiff'})   ## mimetype: png or tiff !!!
        
        hasSeqnum = ET.SubElement(Page, hasSeqnumNS, attrib={'knoraType':'int_value'})
        hasSeqnum.text = seqnum
        
        pageHasName = ET.SubElement(Page, pageHasNameNS, attrib={'knoraType':'richtext_value'})
        pageHasName.text = completeName
        
        pageIsPartOfPublication = ET.SubElement(Page, pageIsPartOfPublicationNS)
        Manuscript = ET.SubElement(pageIsPartOfPublication, PublicationNS, attrib={'knoraType':'link_value', 'linkType':'iri', 'target':scanPubTarget})

        
        




        tree = ET.tostring(Page, encoding="unicode")
        o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE

with o:  
    o.write('\n'+'</knoraXmlImport:resources>')

o.close