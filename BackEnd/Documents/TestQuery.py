from sabackend import SABackend
import sys
import time

back = SABackend('ceas-e384d-dev1.cs.uwm.edu', 'documentorganizer', 'doc_org', 'd3NXWWfyHT', '5432')
print("Connected to server")
query = sys.argv[1]
print("Searching for \'%s\'\n"%query)

start = time.time()
docs = back.get(query)
end = time.time()
print("Time Taken: %s seconds"%(end-start))
print("%s results found"%len(docs))


for doc in docs:
    print(str(doc.get_file_path()) + ' - ' + str(doc.get_hash()))