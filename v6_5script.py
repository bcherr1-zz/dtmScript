import re,sys,os.path,datetime;
#File: DTM JSON parser
#Author: Brandon Cherry
#Date: August 4, 2015
#Description:
#This takes an exported JSON.stringify sting file 
#looping over the report strcture and placing the 
#the report names with the proper events and eVars
def createReportObj(reportObj,reportName,index):
	for i in reportObj:
		reportPropNum =  i[index::]
		for j in reportName:
			testVar = j.split('.')[0]
			if reportPropNum ==testVar[1::]:
				reportObj[i]= j
	return reportObj
#opening the csv file
outPutFile = open('eventCsv .csv' ,'r+')
readTheText  = outPutFile.read()
#parsing the information
#print readTheText
csvParsed = readTheText.split(',')
eventReports = {}
propReports = {}
eVarReports = {}
eventReportName=[]
evarReportName = []
propReportName = []
#getting all the vales to create my prop reports strcture  
for i in csvParsed:
	if  re.search('e[0-9]+\D',i):	
		eventReportName.append(i)
		#pageLoadContainer[i].append(i)
	elif re.search('c[0-9]+\D',i):
		evarReportName.append(i)
	elif re.search('t[0-9]+\D',i):
		propReportName.append(i)

	if  re.search('event[0-9]+',i):
		#clean up the key Value
		keyVal = re.sub('\r\n', '', str(i))
		if i not in eventReports:
			#print i
			eventReports[keyVal] = []
			#eventReports[keyVal].append(event)
	elif  re.search('eVar[0-9]+',i):
		#clean up the key Value
		keyVal = re.sub('Text String\r\n', '', str(i))
		if i not in eVarReports:
			eVarReports[keyVal] = []
			#pageLoadContainer[i].append(i)
	elif  re.search('prop[0-9]+',i):
		#clean up the key Value
		keyVal = re.sub('\r\n', '', str(i))
		if i not in propReports:
			propReports[keyVal] = []
			#pageLoadContainer[i].append(i)

#filling in the reports with the proper data
propReports=createReportObj(propReports,propReportName,4)

eVarReports=createReportObj(eVarReports,evarReportName,4)

eventReports=createReportObj(eventReports,eventReportName,5)


stripTheText = re.sub('[()"{}<>]"', '', str(readTheText))
#this is used to curl the Libary 
result = os.popen("curl : Enter the dtm http src you want to curl").read()
#trying to clean some of the data
stripCurlData = re.sub('[()"{}<>]"', '', str(result))
#getting the page load data
pageLoadData = stripCurlData.split(',pageLoadRules')
#getting the rules data which is actually dynamic call rules in DTM
pageLoadContainer = {}
#cleaning up the rules data
pageLoadStrip = re.sub('[()"{}<>]"', '', str(pageLoadData[1]))
#parsing to get a key id for my rules container 
parsePageLoadRules = pageLoadStrip.split('},{name')
#looping over the rules and parsing the name to create my strcture 
for i in parsePageLoadRules:
	
	keyForPageLoad = i.split(':')[1].split(',')[0].strip('"')
	#print keyForPageLoad
	if keyForPageLoad not in pageLoadContainer:
			pageLoadContainer[keyForPageLoad] = []
			pageLoadContainer[keyForPageLoad].append(i)
#Writing an Html Document
htmlFile = 'dtmRules.html'
newFile = open(htmlFile,"w")
newFile.write('<html><head><title>'+str(htmlFile)+'</title><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js">></script><link rel="stylesheet" href="" type="text/css" />')
newFile.write('</head><body >')
newFile.write('<div class = dtm_Rules>')
newFile.write('<h1>North America Dtm Rules</h1>')
for i in pageLoadContainer:
	pageLoadContainer[i]=re.sub('[(){}<>"\[\]]', '', str(pageLoadContainer[i]))
	newFile.write(str('<div class = "keyVal"><h3>'+i+'</h3></div>'))
	dataInsidePageLoad = pageLoadContainer[i].split(',')
	#print dataInside
	for attribute in dataInsidePageLoad:
		#matching the key value to the data in the event report
		for keysInsideOfEventReports in eventReports:
			if  re.search(keysInsideOfEventReports,attribute):
				event = '<span>event report name:</span> '+str(eventReports[keysInsideOfEventReports])
				newFile.write('<div class = "data" >'+event+"<br></div>")
				#print event
		#matching the key value to the data in the evar report
		for keysInsideOfEventReports in eVarReports:
			if  re.search(keysInsideOfEventReports,attribute):
				evar = '<span>eVar report name: </span>  ' +str(eVarReports[keysInsideOfEventReports])
				newFile.write('<div class = "data" >'+evar+"<br></div>")
		#matching the key value to the data in the prop report
		for keysInsideOfEventReports in propReports:
			
			if  re.search(keysInsideOfEventReports,attribute):
				prop = '<span>prop report name:</span>   '+str(propReports[keysInsideOfEventReports])
				newFile.write('<div class = "data" >'+prop+"<br></div>")			
	#	newFile.write('<div class = "data" >'+str(attribute)+"<br></div>")
newFile.write('</div>')

newFile.write('</body></html>')
newFile.close()
