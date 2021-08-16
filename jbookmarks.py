import json

with open('/home/bogus/txt/bookmarks-2021-02-19.json') as jf:
	jd = json.load(jf)
	for jr in jd['children']['children']['children']:
		print(f'url: {jr}')

