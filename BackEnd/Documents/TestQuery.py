from sabackend import SABackend
import sys

back = SABackend('ceas-e384d-dev1.cs.uwm.edu', 'documentorganizer', 'doc_org', 'd3NXWWfyHT', '5432')


query = sys.argv[1]

docs = back.get(query)
for doc in docs:
    print(str(doc.get_file_path()) + ' - ' + str(doc.get_hash()))