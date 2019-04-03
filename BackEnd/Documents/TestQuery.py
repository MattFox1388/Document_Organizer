from sabackend import SABackend

back = SABackend('ceas-e384d-dev1.cs.uwm.edu', 'documentorganizer', 'doc_org', 'd3NXWWfyHT', '5432')

docs = back._get_docs('java')
for doc in docs:
    print(doc.get_file_path())