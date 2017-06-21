from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import requests 
import requests, pdb
from collections import Counter
import time

#Writing to File	
#open a new file named workfile.txt	
def write_txt_file(file_name):
	f = open(file_name, 'w')
	f.write('\nWRITNG TO FILE WRITNG TO FILE WRITNG TO FILE\n\n')
	f.write('TITLE\tAUTHORS\tKEYWORDS\tRELEVENT ORGANISMS\tLINKS TO TABLES\tGENES\tUNIQUE GENES\n')
write_txt_file('workfile2017_5_2-start2003.txt')

def weeklylinkspage(urlforyear):
#getting weekly links from 2016 page
	yearLinks2016 = []
	landingPg2016 = urlopen(urlforyear)
	SoupForLandingPg2016 = BeautifulSoup(landingPg2016)
	for weeklylink in SoupForLandingPg2016.findAll("table", {"class":"proxy-archive-by-year"}):
		for wklylink in weeklylink.findAll("a", href = True):
			wklylink_href = (wklylink['href'])	
			yearLinks2016.append(wklylink_href)
		print (yearLinks2016)
	return (yearLinks2016)

def pull_article_info(bsObj2, LINK1, t0):

	#most current version url
	print ("PAGEURL: \n")
	print (pageUrl)
	issueNum = str(re.search('(issue)([0-9]*)',pageUrl).group(2))
	print (issueNum)

	#JOURNAL
	print ('\nJOURNAL: \n')
	journalTitle = bsObj2.findAll("abbr",{"class": "slug-jnl-abbrev"})
	for journal in journalTitle:
		journal = journal.text.replace('\n','')
		journal = journal.replace('  ','')
		journal = journal.encode("utf-8")
		global journal
		print (journal)

	#VOLUME
	print ('\nVOLUME: \n')
	volumeNumber = bsObj2.findAll("span",{"class": "slug-vol"})
	for volume in volumeNumber:
		volume = volume.text.replace('  ','')
		volume = volume.replace('\n','')
		volume = volume.replace(',','')
		volume = volume.encode("utf-8")
		print (volume)

		#Links to tables
	print('LINKS TO TABLES:\n')
	klist = []
	print (LINK1)
	base0 = LINK1.split("/")
	#base = re.search('.*/.*/.*/./', LINK1)
	if base0:
		print ("THIS IS HERE")
		print (base0)
		base = str(base0[0] + "/" +base0[1] + "/"+ base0[2] + "/" + base0[3] + "/"+ base0[4] + "/"+ base0[5]+ "/")
		print (base)
	for link in bsObj2.findAll("div", {"class":"table-inline"}): 
		lnk = link.findAll("a")[0]['href']
		print (lnk)
		LINK2 = base+str(lnk)
		print (LINK2)
		klist.append(LINK2)
	print (klist)  

	#print ('TABLE CAPTION:')
	tablestuff2 = ()
	table=()
	for tablelink in klist: 
		tablepage = urlopen(tablelink)
		SoupForTablePage = BeautifulSoup(tablepage)
		for tablestuff in SoupForTablePage.findAll("div", {"class":"table-caption"}):
			tablestuff = tablestuff.text.replace('\n', ' ')

			kineticswords_list = ['kinetic', 'kinetics', 'kcat', 'km', 'kcat/km']
			for kineticwords in kineticswords_list:
				if kineticwords in tablestuff:
					print ('TABLE KINETICS:')
					global tablestuff
					print (tablestuff.encode("utf-8"))
					tablestuff2 = tablestuff.encode("utf-8")
					for table in SoupForTablePage.findAll("table"):
						print ("\nTABLE:")
						table = table.encode("utf-8")
						print (table)
					
	#PAGE NUMBER
	print ('\nPAGE NUMBER: \n')
	pageNumber = bsObj2.findAll("span",{"class":"slug-pages"})
	for page in pageNumber:
		page = page.text.replace('  ','')
		page = page.replace('\n','')
		page = page.encode("utf-8")
		print (page)
	#title
	print ("TITLE:\n")
	try:
		title = bsObj2.find("h1",{"id":"article-title-1"})
		tTitle = str(title.get_text().encode("utf-8"))[1:]
	except AttributeError:
		tTitle = "not found"
	print (tTitle + "\n")
	
	#Authors
	print ('AUTHORS:')
	authorsList = bsObj2.findAll("a",{"class":"name-search"}) #print authors names
	aAuthors = str(','.join([ str(author.get_text().encode("utf-8"))[1:] for author in authorsList ]))
	print (aAuthors + "\n" )

	#Keyword list
	print ('\nKEYWORD LIST: \n')
	#getting keywords
	keywordList = bsObj2.findAll("a", {"class":"kwd-search"})
	keywordList2 = ','.join([str(keyword.get_text().encode("utf-8"))[1:] for keyword in keywordList])
	print (keywordList2 + "\n")

	#Relevant Organisms - italicised words in abstract
	print ('RELEVENT ORGANISMS:')
	allstuff = []
	allItalics = []
	stopwords = ['de novo', 'ex vivo', 'in situ','ex situ', 'in silico', 'in vitro', 'in vivo']
	for stuff in bsObj2.findAll("div", {"class":"section abstract"}):#getting abstract
		stuff = stuff.encode("utf-8")
		soupstuff = BeautifulSoup(stuff)
		for emwords in soupstuff.findAll("em"):#italicised words in abstract
			emwords = str(emwords.text.encode("utf-8"))[1:]
			if re.search('\w\s\w', emwords):
				emwords = emwords.lower()
				for word in stopwords: 
					if word in emwords:
						emwords = emwords.replace(word,'')
				allItalics.append(emwords)
		print (allItalics)
		

	#GENES
	RE_list = ['AatII', 'Acc65I', 'AccI', 'AclI', 'AatII', 'Acc65I', 'AccI', 'AclI', 'AfeI', 'AflII', 'AgeI', 'ApaI', 'ApaLI', 'ApoI', 'AscI', 'AseI', 'AsiSI', 'AvrII', 'BamHI', 'BclI', 'BglII', 'Bme1580I', 'BmtI', 'BsaHI', 'BsiEI', 'BsiWI', 'BspEI', 'BspHI', 'BsrGI', 'BssHII', 'BstBI', 'BstZ17I', 'BtgI', 'ClaI', 'DraI', 'EaeI', 'EagI', 'EcoRI', 'EcoRV', 'FseI', 'FspI', 'HaeII', 'HincII', 'HindIII', 'HpaI', 'KasI', 'KpnI', 'MfeI', 'MluI', 'MscI', 'MspA1I', 'MfeI', 'MluI', 'MscI', 'MspA1I', 'NaeI', 'NarI', 'NcoI', 'NdeI', 'NgoMIV', 'NheI', 'NotI', 'NruI', 'NsiI', 'NspI', 'PacI', 'PciI', 'PmeI', 'PmlI', 'PsiI', 'PspOMI', 'PstI', 'PvuI', 'PvuII', 'SacI', 'SacII', 'SalI', 'SbfI', 'ScaI', 'SfcI', 'SfoI', 'SgrAI', 'SmaI', 'SmlI', 'SnaBI', 'SpeI', 'SphI', 'SspI', 'StuI', 'SwaI', 'XbaI', 'XhoI', 'XmaI']
	geneslist = []
	fourletters = bsObj2.findAll(string = re.compile('\s[A-Z][a-z][a-z][A-Z]\s'))
	for letters in fourletters:
		result = re.search('\s[A-Z][a-z][a-z][A-Z]\s', letters) 
		genes=result.group()
		for RestrictEnz in RE_list: 
			if RestrictEnz in genes: 
				genes = genes.replace(RestrictEnz,"")
		genes = str((genes).encode("utf-8"))[1:]
		
		#print (result)
		geneslist.append(genes)


	print ("\nGENES: \n")
	print (geneslist)
	print (Counter(geneslist))

	print ("\nUNIQUE GENES: \n")
	uniquegenes = set(geneslist)
	print (uniquegenes)

	#PUBLICATION DATE
	print ('\nPUBLICATION DATE: \n')
	datePub = bsObj2.findAll("span",{"itemprop": "datePublished"})
	for date in datePub:
		#re.sub( '\s+', ' ', date).strip()
		date = date.text.replace('\n','')
		date = re.sub('\s+','', date)
		date = date.encode("utf-8")
		global date
		print (date)

	t1 = time.time()
	timestamp = t1-t0
	print (timestamp)

	f = open('workfile2017_5_2-start2003.txt', 'a')

	#write title
	#f.write('TITLE:\n')
	titleFinal =(str(tTitle.replace('\n','').encode("utf-8"))[1:])
	#titleFinal2 = str(re.sub(' +',' ', titleFinal))
	f.write(titleFinal)
	f.write('\t')

	#write authors list
	#f.write('\n\nAUTHORS: \n')
	f.write(aAuthors)
	f.write('\t')

	#f.write('\n\nKEY WORDS: \n')
	f.write(keywordList2)
	f.write('\t')

		#f.write('\n\nRELEVENT ORGANISMS: \n')
	f.write(str(allItalics))
	f.write('\t')

	#f.write('\n\nGENES: \n')
	f.write(str(geneslist))
	f.write('\t')

	#f.write('\n\nUNIQUE GENES: \n')
	f.write(str(Counter(geneslist)))
	f.write('\t')

	#DATE
	f.write(str(date)[1:])
	f.write('\t')

	#JOURNAL 
	f.write(str(journal)[1:])
	f.write('\t')

	#VOLUME 
	f.write(str(volume)[1:])
	f.write('\t')

	#f.write('\n\nLINKS TO TABLES: \n')
	f.write(str(klist))
	f.write('\t')

	#WRITING CAPTIONS FOR TABLES WITH KINETIC-LIKE WORDS
	f.write(str(tablestuff2))
	f.write('\t')

	#TABLE VALUES
	f.write(str(table))
	f.write('\t')

	#TIMESTAMP
	f.write(str(timestamp))
	f.write('\t')

	#PAGENUMBER
	f.write(str(page)[1:])
	f.write('\t\n')



	f = open('workfile2017_5_2-start2003.txt', 'r') #read the workfile
	#print (f.read()) 
	f.close()

def lignin_scan(bsObj2, LINK,t0):
	compiled_lignin_words = []
	lignin_words = ['lignin ', 'ligninase ', 'Lignin ', 'Ligninase ']
	#for each_lignin_word in lignin_words:
	for lig_word in bsObj2.findAll('p'):
		lig_word = lig_word.text
		#print (lig_word.encode('utf-8'))
		#print('\nHERE\n')
		for each_lignin_word in lignin_words:
			if each_lignin_word in lig_word:
				print ('I FOUND A WORD')
				print (each_lignin_word)
				compiled_lignin_words.append(each_lignin_word)
			#return len(compiled_lignin_words)	
#	
	if len(compiled_lignin_words) >= 1:
		pull_article_info(bsObj2, LINK, t0)
	#print (len(compiled_lignin_words))
	time.sleep(1)	
		
#making soup for weekly page  
archivebase = ("http://www.jbc.org/content/by/year/")
yearsList = ["2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" , "2011", "2012", "2013", "2014", "2015", "2016","2017"]

for years in yearsList: 
	archiveYear = archivebase + years
	t0 = time.time()

	for pageUrl in weeklylinkspage(archiveYear): 
		count = 0
		html = urlopen("http://www.jbc.org" + pageUrl)
		bsObj = BeautifulSoup(html)
		
			
		 
		for link in bsObj.findAll("div", {"class":"cit-extra"}):
		
			lnk = link.findAll("a", href = re.compile(".*full"))[0]['href']
			#print (str(lnk))
			splitlnk = lnk.split("/")
			#print (splitlnk[3])
			#if int(splitlnk[3]) >= 22: 
				#print ('yes')
			LINK1 = "http://www.jbc.org"+str(lnk)
			print (LINK1)
			obj = requests.get(LINK1)
			bsObj2 = BeautifulSoup(obj.text, "html.parser")
			count = count + 1
			lignin_scan(bsObj2, LINK1, t0)

			#else: 
				#print (splitlnk[3])
			
			

print (count)








