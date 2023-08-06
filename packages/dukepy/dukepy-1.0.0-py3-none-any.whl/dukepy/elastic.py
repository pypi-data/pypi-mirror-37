# Install and config elasticsearch :
# 	http://caraulean.com/2016/install-and-configure-elasticsearch-in-windows/
# 	https://www.elastic.co/downloads/elasticsearch

# !/usr/bin/python3
#   This script is a simple introduction to the python elasticsearch API.
#
#   This script will populate an elasticsearch index from a file and then give a simple command line query interface.
#   Each line of the input file will be mapped into a JSON document of the form { "text": "my file line..." } and added
#   to the index.
#
#   You can use Docker to spin up a local elasticsearch instance to play around with, e.g.
#   docker run --name elasticsearch -d -p 9200:9200 elasticsearch:latest
#

import argparse, elasticsearch, json

import os
from elasticsearch import Elasticsearch

from ir_data import IRData


def parse_args():
	# argument help
	parser = argparse.ArgumentParser(description='Add lines from a file to a simple text Elasticsearch index.')
	parser.add_argument('--file', help='Name of file to parse, e.g. /usr/share/dict/american-english')
	parser.add_argument('--host', default="localhost", help='Elasticsearch host.')
	parser.add_argument('-p', '--port', default=9200, help='port, default is 9200')
	return parser.parse_args()


def index_irs(NBR_OF_IRS=1000):
	latest = IRData().GetLatestIR()
	for incident in IRData().GetListOfIRs(latest - NBR_OF_IRS, latest):
		print("Indexing - %s" % (incident))
		es.index(
			index="irs",
			doc_type="document",
			body=incident,
			# parent=currentParent["id"]
		)


def search():
	# now we can do searches.
	print("Ok. I've got an index of {0} documents. Let's do some searches...".format(count['count']))
	while True:
		try:
			query = input("Enter a search: ")
			result = es.search(index=INDEX_NAME, doc_type=TYPE,
							   body=fuzzy_search(query, "eco_justification_free_text"))
			if result.get('hits') is not None and result['hits'].get('hits') is not None:
				print("\nResults: " + str(result['hits']['total']) + "\n")
				for hit in result['hits']['hits']:
					source = hit["_source"]
					print("name: " + str(source["name"][0]))
					print("title: " + str(source["title"][0]))
					# print("description: " + source["description"][0].encode('utf-8'))
					# print("severity: " + str(source["severity"][0]))
					print("lastmodifieddate: " + str(source["lastmodifieddate"][0]) + "\n")
			else:
				print({})
		except(KeyboardInterrupt):
			break
		except KeyError as e:
			pass


def fuzzy_search(term, field):
	return {
		"query": {
			"match": {
				field: {
					"query": term.strip(),
					"fuzziness": "AUTO"
				}
			}
		}
	}


if __name__ == "__main__":
	args = parse_args()

	# index and document type constants
	INDEX_NAME = "irs"
	TYPE = "document"

	# get a client
	es = Elasticsearch(hosts=[{"host": args.host, "port": args.port}])

	# create an index, ignore if it exists already
	es.indices.create(index='documents', ignore=400)

	# index_irs(10000)

	# count the matches
	count = es.count(index=INDEX_NAME, doc_type=TYPE, body={"query": {"match_all": {}}})

	search()
