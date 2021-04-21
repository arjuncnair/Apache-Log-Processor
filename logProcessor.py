import os, sys
from collections import Counter,OrderedDict

pageList = []
hostList = []
successfulPageList = []
unSuccessfulPagesList = []
hostWithPage = {}
errorLogFileName = "Error.log"

def commonDictProcessor(dataList,resource_type,kind,limit):
    topTenHosts = []
    print "------------------------------------------------"
    print "List of Top 10 :".rjust(25),kind,"-",resource_type
    print "------------------------------------------------"
    dataDict = dict(Counter(dataList))    
    sortedTupleList = sorted(dataDict.items(), key=lambda x: x[1],reverse=True)[0:limit]
    print resource_type.rjust(15),"\t\t |\tCount"
    print "------------------------------------------------"
#Retreiving Data from Tuple    
    for data in sortedTupleList:
        print data[0].rjust(20),"\t : \t".rjust(10), data[1]
        if resource_type == "Host":
            topTenHosts.append(data[0])

#For each of the top 10 hosts, show the top 5 pages requested and the number of requests for each -- Code Below Calling PageProcessor Method to find top 5 Pages Requested
    if resource_type == "Host":
        for ip in topTenHosts:
            topFivePageProcessor(ip,"Pages",5)
    raw_input("\nPress <Enter> to Continue...")
#Function to Finds the Top 5 Pages Requested by Hosts
def topFivePageProcessor(ip,resource_type,limit):
    print "************************************************"
    print "List of Top 5".rjust(10),resource_type, "requested by", ip
    print "------------------------------------------------"
    dataDict = dict(Counter(hostWithPage[ip]))
    sortedTupleList = sorted(dataDict.items(), key=lambda x: x[1],reverse=True)[0:limit]
    print resource_type.rjust(15),"\t\t |\tCount"
    print "------------------------------------------------"
    for data in sortedTupleList:
        print data[0].rjust(20),"\t : \t".rjust(10), data[1]

    if resource_type == "Host" and ctr < 5:
            commonDictProcessor(hostWithPage[data[0]],"Pages",5)
    print "----------------------END-----------------------\n"        

#Function that finds Succesful request Percentage
def requestPercentageSuccesful(sucessfulRequests,totalRequests):
    print "Success % : ",str((sucessfulRequests / totalRequests) * 100)
    raw_input("\nPress <Enter> to Continue...")

#Function that finds UnSuccesful request Percentage
def requestPercentageFailed(unSuccessfulRequests,totalRequests):
    print "Failed Requests % : ",str(float(unSuccessfulRequests / totalRequests) * 100)
    raw_input("\nPress <Enter> to Continue...")


def logProcessorMain(errorLogFileName):
    try:
        accessLogFileName = sys.argv[1]
        sucessfulRequests = 0.0
        unSuccessfulRequests = 0.0
        parseError = False
        errorLogFile = open(errorLogFileName,"w+")
        with open(accessLogFileName,'r+') as logFile:
            data = logFile.readlines()

        totalRequests = len(data)

        for line in data:
    #Verifies that Logging is done with proper formatting. If Not, the line will be ignored and written to file Error.log"        
            requestStatusCode = unicode(line.split()[8],'utf-8') 

            if requestStatusCode.isnumeric():
                requestStatusCode = int(line.split()[8])
                hostname = line.split()[0]
                requestPath = line.split()[6]
                pageList.append(requestPath)
                hostList.append(hostname)
                
    # Mapping Hosts with Pages Accessed -- Start
                if hostWithPage.get(hostname) == None:
                    hostWithPage[hostname] = [requestPath]
                else:
                    hostWithPage[hostname].append(requestPath)
    # Mapping Hosts with Pages Accessed -- End

                if requestStatusCode >= 200 and requestStatusCode <= 300:
                    successfulPageList.append(requestPath)
                    sucessfulRequests += 1

                elif requestStatusCode < 200 or requestStatusCode > 300:
                    unSuccessfulPagesList.append(requestPath)
                    unSuccessfulRequests += 1
            else:
                errorLogFile.write("Log Parsing Error: " + line)
                parseError = True

        errorLogFile.close()

        if parseError:
            print "\n[WARNING]: Error Parsing Few Logs. Please Check the log file --> ", errorLogFileName, "Proceeding for the rest!"
        option = 1
        while option != 0:
            print "\n1. Top 10 Requested Pages and Number of requests made for each (Includes both succesful/Unsuccesfull Page Requests)"
            print "2. Top 10 Successful page requests"
            print "3. Top 10 Unsuccessful page requests"
            print "4. The top 10 hosts making the most requests, displaying the IP address and number of requests made."
            print "5. Percentage of successful requests (anything in the 200s and 300s range) "
            print "6. Percentage of unsuccessful requests (anything that is not in the 200s or 300s range)"
            print "0. Exit\n"
            option = int(raw_input("Please Enter your Choice: "))
            print ""
            if int(option) == 1:
                commonDictProcessor(pageList,"Page","All",10)
            elif int(option) == 2:
                commonDictProcessor(successfulPageList,"Page","Successful",10)
            elif int(option) == 3:
                commonDictProcessor(unSuccessfulPagesList,"Page","Unsuccesful",10)
            elif int(option) == 4:
                commonDictProcessor(hostList,"Host","All",10)
            elif int(option) == 5:
                requestPercentageSuccesful(sucessfulRequests,totalRequests)
            elif int(option) == 6:
                requestPercentageFailed(unSuccessfulRequests,totalRequests)
            elif int(option) == 0:
                sys.exit(0)
            else:
                print "[ERROR]: Invalid Input"
                raw_input("\nPress <Enter> to Continue...")

    except IOError as e:
        print "Error Opening File", e
    except IndexError as ie:
        print "\n[ERROR]: The script requires one argument (AccessLog) to work. Please pass Access Log as only argument.\n"
        print "Usage: \n\tpython",sys.argv[0],"<Path>/<Log File Name>\n"
        print "Example:"
        print "\tpython",sys.argv[0],"access.log"
        print "\tpython",sys.argv[0],"/home/ubuntu/access-1.log\n"
    except Exception as se:
        print "Error Occured:", se    
        
logProcessorMain(errorLogFileName)
