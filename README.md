# Create an information retrieval system
A data querying program for 10 to 100,000 email data in XML format, converted to txt and index files for the users to easily search through all items.

# How to use (overview)
a. Phase 1 first: ~> python3 phase1.py
b. Phase 2: ~> python3 phase2.py [txt file as input] [idx file as
output] [berkeley DB data type] (assume it’s also accurate that we
need to db_dump into a text file)
c. Phase 3: ~> python3 phase3.py

# How to use (details)
a. Phase 1:
   i. To generate the text files, run the program (phase1.py) using the
  command line Python3 phase1.py. Program will ask the user to input
  source file name, then asks the user to input another filename for the
  respective file to be generated

b. Phase 2:
  i. To make idx files, unix commands need to be entered. “Python3 [program
  file, i.e. a python file] [txt file from phase 1, i.e. input file] [idx file to be
  made] [type of data structure in Berkeley DB]”.
  ii. Before the program db_load, program will ask for a filename to output the
  dp_dump result into, instead of showing the result in stdout, there is no
  need to state file type, e.g. “.txt”. (as it’s stated when the program asks)

c. Phase 3:
  i. Run using ‘python3 phase3.py’
  ii. Exit at anytime by typing ‘quit’ once the program is running
  iii. Otherwise, search in the database with queries that use the following
  format: [search keyword][operator][search term] ex) body:business
  iv. There can be any number of spaces between the three parts of the query
  v. Search keywords are as follows: subj, from, to, body, bcc, cc, and date
  vi. The operator should always be a colon ‘:’ unless working with dates, then
  equality symbols ‘<’, ‘>’, and ‘=’ are allowed
  vii. Search keywords are case sensitive, search terms are not
  viii. Entering only a term and no keyword or operator defaults to searching the
  ‘subj’ and ‘body’ indices
  ix. Entering ‘output=full’ or ‘output=brief’ will change the amount of data
  returned from a search. The program defaults to brief upon startup
