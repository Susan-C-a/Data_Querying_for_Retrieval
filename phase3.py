from bsddb3 import db
import numpy
import re

briefOut = True
databases = []


def checkQuery(query):
    #this function used to check for command validity, but apparently non-column words with no operators are still valid, so this always returns true 
    operators = set("<>=%:")
    if any((char in operators) for char in query):
        return True
    else:
        print("No command given, searching subjects and body for given arguments")
        return True

#uses database 2 for full records
def output(rows):
    global briefOut, databases
    space = databases[1]
    data = []
    for row in rows:
        data.append(space[1].set((row).encode("utf-8"))[1].decode("utf-8"))
    for i in range(len(data)):
        if briefOut:
            subStart = data[i].find("<subj>") + 6
            subEnd = data[i].find("</subj>")
            print("Row: " + rows[i] + "\nSubject: " + data[i][subStart:subEnd])
        else:
            #behold, the wall
            subStart = data[i].find("<subj>") + 6
            subEnd = data[i].find("</subj>")
            dateStart = data[i].find("<date>") + 6
            dateEnd = data[i].find("</date>")
            fromStart = data[i].find("<from>") + 6
            fromEnd = data[i].find("</from>")
            toStart = data[i].find("<to>") + 4
            toEnd = data[i].find("</to>")
            ccStart = data[i].find("<cc>") + 4
            ccEnd = data[i].find("</cc>")
            bccStart = data[i].find("<bcc>") + 5
            bccEnd = data[i].find("</bcc>")
            bodyStart = data[i].find("<body>") + 6
            bodyEnd = data[i].find("</body>")
            
            print("Row: " + rows[i])
            print("Date: " + data[i][dateStart:dateEnd])
            print("From: " + data[i][fromStart:fromEnd])
            print("To: " + data[i][toStart:toEnd])
            print("Subject: " + data[i][subStart:subEnd])
            print("CC: " + data[i][ccStart:ccEnd])
            print("BCC: " + data[i][bccStart:bccEnd])
            print("Body: " + data[i][bodyStart:bodyEnd])
        
def init():
    global databases
    
    #database for terms index
    database = db.DB()
    DB_File = input("Please enter the name of the terms index file (Case sensitive)")
    #DB_File = "new_te10.idx"
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()
    #database for records index
    database2 = db.DB()
    DB_File2 = input("Please enter the name of the records index file (Case sensitive)")
    #DB_File2 = "new_re10.idx"
    database2.open(DB_File2, None, db.DB_HASH, db.DB_CREATE)
    curs2 = database2.cursor()
    #database for emails index
    database3 = db.DB()
    DB_File3 = input("Please enter the name of the emails index file (Case sensitive)")
    #DB_File3 = "new_em10.idx"
    database3.open(DB_File3, None, db.DB_BTREE, db.DB_CREATE)
    curs3 = database3.cursor()
    #database for date index
    database4 = db.DB()
    DB_File4 = input("Please enter the name of the date index file (Case sensitive)")
    #DB_File4 = "new_da10.idx"
    database4.open(DB_File4, None, db.DB_BTREE, db.DB_CREATE)
    curs4 = database4.cursor()
    
    return [(database, curs), (database2, curs2), (database3,curs3), (database4, curs4)]

def shutdown(databases):
    for twopair in databases:
        twopair[0].close()
        twopair[1].close()

#use db1
def subj(terms):
    global databases
    space = databases[0]
    terms = terms[0].split(' ')
    results = []
    if type(terms) == type(str()):
        results.append(space[1].set(("s-" + terms).encode("utf-8")))
    else:
        for item in terms:
            results.append(space[1].set(("s-" + item).encode("utf-8")))
    if not results[0] == None:
       dup = space[1].next_dup()
       while dup != None:
          results.append(dup[1].decode("utf-8"))
          dup = space[1].next_dup()
    goodData = True
    for i in range(len(terms)):
        if not results[i] is None:
            results[i] = results[i][1].decode("utf-8")
        else:
            print("No results returned for query term: " + terms[i])
            goodData = False
    if goodData:
        return results

#use db 3
# Arthur corrected the error, but it's not reflected here
def fromq (address):
    global databases
    space = databases[2]
    address = address[0].split(' ')
    results = []

    if type(address) == type(str()):
        results.append(space[1].set(("from-"+address).encode("utf-8")))
    else:
        for adr in address:
           results.append(space[1].set(("from-"+adr).encode("utf-8")))
    if not results[0] == None:
       dup = space[1].next_dup()
       while dup != None:
          results.append(dup)
          dup = space[1].next_dup()
    goodData = True
    for i in range(len(results)):
        if not results[i] is None:
            results[i] = results[i][1].decode("utf-8")
        else:
            print("No results returned for query term: " + address[i])
            goodData = False
    if goodData:
        return results

#use db3
def to(address):

    global databases
    space = databases[2]
    address = address[0].split(' ')
    results = []
    
    if type(address) == type(str()):
        results.append(space[1].set(("to-"+address).encode("utf-8")))
    else:
        for adr in address:
           results.append(space[1].set(("to-"+adr).encode("utf-8")))
    if not results[0] == None:
       dup = space[1].next_dup()
       while dup != None:
          results.append(dup[1].decode("utf-8"))
          dup = space[1].next_dup()
    goodData = True
    for i in range(len(results)):
        if not results[i] is None:
            results[i] = results[i][1].decode("utf-8")
        else:
            print("No results returned for query term: " + address[i])
            goodData = False
    if goodData:
        return results

#use db4
# Susan is still working on this
def date(dates):
    global databases
    # date idx
    space = databases[3]
    dates = dates[0].split(" ")
    results = []
    for i in range(len(dates)):
        dates[i].replace('date', '')

    for date in dates:
        if not date == '':
            equal = space[1].set((""+date[1:]).encode("utf-8"))
            if date[:1] == '<' and date[:2] != "<=":
                found = space[1].first()
                while(found!=None):
                    content = space[1].set(found[0])[0]
                    if(content.decode("utf-8")>(""+date[1:])):
                        break
                    row_id = space[1].set(found[0])[1]
                    if equal != found:
                        results.append(row_id.decode("utf-8"))
                    dup = space[1].next_dup()
                    while(dup!=None):
                        content = dup[0].decode("utf-8")
                        if content>(""+date[1:]):
                            break
                        if equal != None:
                            if equal[0] != dup[0]:
                                results.append(dup[1].decode("utf-8"))
                        else:
                            results.append(dup[1].decode("utf-8"))
                        dup = space[1].next_dup()
                    else:
                        found = space[1].next()
            
            elif date[:1] == '>' and date[:2] != ">=":
                found = space[1].set_range((""+date[1:]).encode("utf-8"))
                while found != None:
                    row_id = space[1].set(found[0])[1]
                    if equal != found:
                        results.append(row_id.decode("utf-8"))
                    dup = space[1].next_dup()
                    while(dup!=None):
                        content = dup[0].decode("utf-8")
                        if equal != None:
                            if equal[0] != dup[0]:
                                results.append(dup[1].decode("utf-8"))
                        else:
                            results.append(dup[1].decode("utf-8"))
                        dup = space[1].next_dup()
                    else:
                        found = space[1].next()
            
            elif date[:2] == "<=":
                found = space[1].first()
                while(found!=None):
                    content = space[1].set(found[0])[0]
                    if(content.decode("utf-8")>(""+date[2:])):
                        break
                    row_id = space[1].set(found[0])[1]
                    results.append(row_id.decode("utf-8"))
                    dup = space[1].next_dup()
                    while(dup!=None):
                        content = dup[0].decode("utf-8")
                        if content>(""+date[2:]):
                            break
                        results.append(dup[1].decode("utf-8"))
                        dup = space[1].next_dup()
                    else:
                        found = space[1].next()
            
            elif date[:2] == ">=":
                found = space[1].set_range((""+date[2:]).encode("utf-8"))
                while found != None:
                    row_id = space[1].set(found[0])[1]
                    results.append(row_id.decode("utf-8"))
                    dup = space[1].next_dup()
                    while(dup!=None):
                        content = dup[0].decode("utf-8")
                        results.append(dup[1].decode("utf-8"))
                        dup = space[1].next_dup()
                    else:
                        found = space[1].next()
            
            elif date[:1].isdigit():
                # date idx
                row_id = (space[1].set((""+date).encode("utf-8")))[1]
                # [1] of the result return the value, [0] return the key
                results.append(row_id.decode("utf-8"))
                dup = space[1].next_dup()
                while(dup!=None):
                    results.append(dup[1].decode("utf-8"))
                    dup = space[1].next_dup()
            
    return(results)
    #change
#use db3
def bcc(address):
    global databases
    #email idx
    space = databases[2]
    address = address[0].split(" ")
    results = []

    if type(address) == type(str()):
        results.append(space[1].set(("bcc-"+address).encode("utf-8")))
    else:
        for adr in address:
           results.append(space[1].set(("bcc-"+adr).encode("utf-8")))
    if not results[0] == None:
       dup = space[1].next_dup()
       while dup != None:
          results.append(dup[1].decode("utf-8"))
          dup = space[1].next_dup()
    goodData = True
    for i in range(len(results)):
        if not results[i] is None:
            results[i] = results[i][1].decode("utf-8")
        else:
            print("No results returned for query term: " + address[i])
            goodData = False
    if goodData:
        return results
        # bcc:alb@cpuc.ca.gov

#use db3
def cc(address):
    global databases
    space = databases[2]
    address = address[0].split(' ')
    results = []
    if type(address) == type(str()):
        results.append(space[1].set(("cc-"+address).encode("utf-8")))
    else:
        for adr in address:
           #print(space[1].set(("cc-"+adr).encode("utf-8")))
           results.append(space[1].set(("cc-"+adr).encode("utf-8")))
    if not results[0] == None:
       dup = space[1].next_dup()
       while dup != None:
          results.append(dup[1].decode("utf-8"))
          dup = space[1].next_dup()
    goodData = True
    for i in range(len(results)):
        if not results[i] is None:
            results[i] = results[i][1].decode("utf-8")
        else:
            print("No results returned for query term: " + address[i])
            goodData = False
    if goodData:
        return results
        # cc:alb@cpuc.ca.gov

#use db1
# Now it's doing partial search
def body(terms):
    global databases
    space = databases[0]
    terms = terms[0].split(' ')
    results = []

    if type(terms) == type(str()):
        if terms.endswith('%'):
            search = space[1].set_range(("b-" + terms).encode("utf-8"))
            while search!=None:
                row_id = space[1].set(search[0])
                results.append(row_id)
                dup = space[1].next_dup()
                while(dup!=None):
                    results.append(dup)
                    dup = space[1].next_dup()
                else:
                    search = space[1].next()
        else:
            results.append(space[1].set(("b-" + terms).encode("utf-8")))
    else:
        for item in terms:
            if item.endswith('%'):
                search = space[1].set_range(("b-" + item).encode("utf-8"))
                while search!=None:
                    row_id = space[1].set(search[0])
                    results.append(row_id)
                    dup = space[1].next_dup()
                    while(dup!=None):
                        results.append(dup)
                        dup = space[1].next_dup()
                    else:
                        search = space[1].next()
            else:
                results.append(space[1].set(("b-" + item).encode("utf-8")))
    goodData = True
    for i in range(len(results)):
        if not results[i] is None:
            results[i] = results[i][1].decode("utf-8")
        else:
            print("No results returned for query term: " + terms[i])
            goodData = False
    if goodData:
        return results
            
        #row_id = space[1].set(("b-"+item).encode("utf-8"))
        
        #row_id = space[1].get(("b-"+item).encode("utf-8"))
    

def main():
    global briefOut, databases
    databases = init()
    
    keywords = ["subj", "from", "to", "date", "bcc", "cc", "body"]
    
    goodInput = False
    while(True):
        while(not goodInput):
            #gets user input to send to DB for querying
            rawquery = input("Type your command in, or see documentation for help:\n")
            if re.search("output=full", rawquery, re.IGNORECASE):
                print("Output type changed to full data dump")
                briefOut = False
            elif re.search("output=brief", rawquery, re.IGNORECASE):
                print("Output type changed to brief data dump")
                briefOut = True
            else:
                goodInput = checkQuery(rawquery)
        if re.search("quit", rawquery[:4], re.IGNORECASE):
            print("Thank you have a nice day")
            break
            

        #splits the raw query based on ':' and ' ', then reassembles it into one list instead of a list of lists
        rawquery = rawquery.split(':')
        for i in range(len(rawquery)):
            rawquery[i] = rawquery[i].strip()
            rawquery[i] = rawquery[i].split(' ')
        query = []
        for sublist in rawquery:
            for item in sublist:
                # Date keyword might not be followed by 
                if re.search("date", item[:4], re.IGNORECASE) and len(item) > 4:
                    query.append(item[:4])
                    query.append(item[4:])
                else:
                    query.append(item)               
        #in short, builds a function call using keywords in the query and then evaluates it
        pos = -1
        results = []
        #need to check every word of query against every keyword
        for part in query:
            pos = pos + 1
            for keyword in keywords:
                if part in keyword:
                    argn = pos + 1
                    #while the words after a discovered keyword are not another keyword, 
                    #count how many arguments there are for that discovered keyword
                    while not (query[argn] in keywords):                            
                        if argn == len(query) - 1:
                            argn = argn + 1
                            break
                        argn = argn + 1
                    #args is a list of every word in query from a discovered keyword to the end of query or the next keyword. a space is added in to keep arguments seperate when args is turned into an array
                    args = query[pos + 1:argn]
                    for i in range(len(args)):
                        args[i] = args[i] + ' '
                    #get rid of the space at the end of the last arg, was causing issues
                    args[len(args) - 1] = args[len(args) - 1][:-1]
                    func = []
                    for i in range(len(args)):
                       #special case for "from" because from is already a python function
                       if keyword == "from":
                           func.append(keyword + "q(")
                       #special case for bcc and cc because cc is in bcc for keyword check
                       elif part == "cc":
                           #print(args)
                           func.append(part + "(")
                       elif part == "bcc":
                           func.append(part + "(")                           
                       else:
                           func.append(keyword + "(")
                       args = numpy.asarray(args)                
                       func[i] = func[i] + str(args) + ')'
                    #func is a string form of a function made of the keyword and its args
                    # for example, if subj:foo was typed in the query, then func is "subj(['foo'])
                    for foo in func:
                       results.append(eval(foo))
        #if any row is empty, there cant possibly be a match between queries
        #if len(results) == 0:
          # results = ''
        #if more than one query was called, compare them to see which results fit all queries
        if len(results) > 1:
            shared = []
            for query1 in results:
                for query2 in results:
                    if (not query1 == query2) and (query1 != None) and (query2 != None):
                        temp = set(query1) - (set(query1) - set(query2))
                        shared.append(temp)
                    else:
                        shared = [set()]
            while(len(shared) > 1):
                for i in range(len(shared)):
                    if len(shared[i]) == 0:
                        del shared[i]    
                        break
                for query1 in shared:
                    for query2 in shared:
                        if not query1 == query2:
                            shared.append(set(query1) - (set(query1) - set(query2)))
            if shared == [set()]:
                results = ' '
            else:
                results = shared
        elif results:
           if type(results[0]) != type(str()):
               results = results[0]
        if results == '' or results == ' ':
            print("No match in data with given parameters")
        else:
            output(results)            
        goodInput = False
    shutdown(databases)

if __name__ == "__main__":
    main()
