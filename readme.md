
# Bulk import of manuscripts and publications pages


**Requirements**
- Access to scans
- CSV (IRI, label)

**Process**
1. Create XML files
	1. Secure access to scans (mount Scanlett)
	2. Download schema to validate XML for bulk import
	3. Run python script to create XML files, reading list of scans and csv (IRI and label of publications)
2. Load the pages using XML files (bulk import)




## Bulk import commands

**DOWNLOAD the schemas for the XML files (in browser)**

http://localhost:3333/v1/resources/xmlimportschemas/http%3A%2F%2Fwww.knora.org%2Fontology%2F0112%2Froud-oeuvres

http://knora.unil.ch/v1/resources/xmlimportschemas/http%3A%2F%2Fwww.knora.org%2Fontology%2F0112%2Froud-oeuvres


**UPLOAD the XML file (in terminal)**
curl -X POST -d @importTest.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112

curl -X POST -d @backup_images_all_tif_1_copy.xml http://root%40example.com:test@localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112

curl -X POST -d @backup_images_all_tif_1.xml http://root%40example.com:test@knora.unil.ch/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0112




## Access to Scanlett
**Mount**	
	
	sudo mount -t cifs -o username=espadini,domain=ad,vers=3.0 //nas.unil.ch/scanlett /mnt/scanlettMounted

**Unmount**	
	
	sudo umount -f /mnt/scanlettMounted
	



## Problems in ms import
- for importing the xml with curl
	147 images yes, 189 no, 170 yes
	Also, this image does not work
		<p0112-roud-oeuvres:Page xmlns:knoraXmlImport="http://api.knora.org/ontology/knoraXmlImport/v1#" xmlns:p0112-roud-oeuvres="http://api.knora.org/ontology/0112/roud-oeuvres/xml-import/v1#" id="CRLR_GR_MS2C14a_1r_1.png"><knoraXmlImport:label>page_CRLR GR MS 2 C/14a___f. 1r___1</knoraXmlImport:label><knoraXmlImport:file mimetype="image/png" path="/mnt/scanlettMounted/GustaveRoud/E_Scan/Scans_import/FondsArchive/CRLR_GR_MS2C14a/CRLR_GR_MS2C14a_1r_1.png" /><p0112-roud-oeuvres:hasSeqnum knoraType="int_value">1</p0112-roud-oeuvres:hasSeqnum><p0112-roud-oeuvres:pageHasName knoraType="richtext_value">f. 1r</p0112-roud-oeuvres:pageHasName><p0112-roud-oeuvres:pageIsPartOfManuscript><p0112-roud-oeuvres:Manuscript knoraType="link_value" linkType="iri" target="http://rdfh.ch/0112/roud-oeuvres/vG0O91nzRWuwx7r3fAaiXw" /></p0112-roud-oeuvres:pageIsPartOfManuscript></p0112-roud-oeuvres:Page>
	deleted in backup_images_all.xml !!!!!!!!!!!!

