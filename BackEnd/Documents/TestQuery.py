from sabackend import SABackend
import sys

back = SABackend('ceas-e384d-dev1.cs.uwm.edu', 'documentorganizer', 'doc_org', 'd3NXWWfyHT', '5432')


query = sys.argv[0]

docs = back._get_docs(query)
for doc in docs:
    print(doc.get_file_path())