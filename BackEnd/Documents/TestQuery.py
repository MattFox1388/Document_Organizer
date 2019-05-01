from sabackend import SABackend
import sys
import time

back = SABackend('ceas-e384d-dev1.cs.uwm.edu', 'documentorganizer', 'doc_org', 'd3NXWWfyHT', '5432')
print("Connected to server")


# print(back.add_tag(100000, "Test"))
print(back.get_doc_by_id(59038))
# query = ' '.join(sys.argv[1:])
# print("Searching for \'%s\'\n" % query)
#
# start = time.time()
# docs = back.get(query)
# end = time.time()
#
# for doc in docs:
#     print(str(doc.get_file_path()) + ' - ' + str(doc.get_hash()))
#
# print("Time Taken: %s seconds"%(end-start))
# print("%s results found"%len(docs))
