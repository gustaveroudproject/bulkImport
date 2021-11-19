###
### CREATE XML FOR SCANS
###


from xml.etree import ElementTree as ET
import re, csv
import glob
import os
from os import listdir

mydir = '/mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_import/FondsArchive/'
# /mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_complets/FondsArchive/
o = open('../OUTPUT_xml/images.xml', 'w')



###################################
## WRITE DECLARATIONS AND BEGINNING OF THE XML FILE -adding more line breaks for readibility '+'\n'+' ???-
###################################
o.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<knoraXmlImport:resources xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://api.knora.org/ontology/knoraXmlImport/v1# ../p0112-roud-oeuvres-xml-schemas/p0112-roud-oeuvres.xsd" xmlns="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#">'+'\n')


    
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
pageIsPartOfManuscriptNS = ET.QName(NS_ROUD, "pageIsPartOfManuscript")
ManuscriptNS = ET.QName(NS_ROUD, "Manuscript")





###################################
## PREPARE CONTENT OF ELEMENTS AND ATTRIBUTES
###################################



dirs = os.listdir(mydir)
for eachDir in dirs:
    eachPath = mydir+eachDir+'/*.png'  ## attenzione *.tif or *.png
    allTif = glob.glob(eachPath)
    for eachTif in allTif:
        eachTif_splitted = os.path.split(eachTif)
        tifName = eachTif_splitted[1]
        tifHead = eachTif_splitted[0]
        tifCompletePath = eachTif
        
        
        ## -----------------------> Page/@id
        tifId = tifName
    
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
            
        
        ## -----------------------> pageIsPartOfManuscript
        coteComplete = tifHead.rsplit('/',1)[1]
        fonds = coteComplete.rsplit('_',1)[0]  # first part
        fondsReadable = re.sub('_', ' ', fonds)
        cote = coteComplete.rsplit('_',1)[1]   # second part
        ms = cote[:2]
        numb = cote[2:3]
        let = cote[3:4]
        rest = cote[4:]
        coteAsInFiche = ms+' '+numb+' '+let+'/'+rest   # recreate because in naming scans whitespaces and slash have not been used
        
        # csv downloaded from sparql query (query saved in graphdb). First column: iri, second column: cote 
        # attention to delimiter for reading csv
        with open("../INPUT_data/fiche_iri_cote.csv", 'r') as csv_cote_id_correspondance:     
            cote_id_correspondance = csv.reader(csv_cote_id_correspondance, delimiter =',', doublequote=True)
            for row in cote_id_correspondance:
                if (coteAsInFiche == row[1]):
                    ficheTarget = row[0]
        
        #with open("../INPUT_data/fiche_cote-id_correspondance.csv", 'r') as csv_cote_id_correspondance:     # csv created from backup_fiches (with xsl in /transformationScripts) just to take easily the corresponding id for each shelfmark
         #   cote_id_correspondance = csv.reader(csv_cote_id_correspondance, delimiter =';', doublequote=True)
          #  for row in cote_id_correspondance:
           #     if (coteAsInFiche == row[1]):
            #        ficheTarget = row[0]
    

        ## -----------------------> label
        scanLabel = "page_"+fondsReadable+" "+coteAsInFiche+"___"+completeName+"___"+seqnum
        
    
    
        ###################################
        ## CREATE ELEMENTS AND ATTRIBUTES (AS PREVIOUSLY DEFINED WITH NS) AND ASSIGN THEM CONTENT
        ###################################


        Page = ET.Element(PageNS, attrib={'id':tifId}) 
        
        label = ET.SubElement(Page, labelNS)
        label.text = scanLabel
    
        file = ET.SubElement(Page, fileNS, attrib={'path':filePath, 'mimetype':'image/png'})   ## mimetype: png or tiff !!!
        
        hasSeqnum = ET.SubElement(Page, hasSeqnumNS, attrib={'knoraType':'int_value'})
        hasSeqnum.text = seqnum
        
        pageHasName = ET.SubElement(Page, pageHasNameNS, attrib={'knoraType':'richtext_value'})
        pageHasName.text = completeName
        
        pageIsPartOfManuscript = ET.SubElement(Page, pageIsPartOfManuscriptNS)
        Manuscript = ET.SubElement(pageIsPartOfManuscript, ManuscriptNS, attrib={'knoraType':'link_value', 'linkType':'iri', 'target':ficheTarget})

        
        




        tree = ET.tostring(Page, encoding="unicode")
        o.write('\n''\n'+ tree)

## WRITE END OF THE XML FILE
with o:  
    o.write('\n'+'</knoraXmlImport:resources>')

o.close