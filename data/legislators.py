import requests, yaml, json

SOURCE = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml'

def parse(full):
	term = full['terms'][-1]
	return {
		'bioguide_id': full['id']['bioguide'],
		'name': full['name']['official_full'],
		'phone': term['phone'],
		'party': term['party'],
		'state': term['state'],
		'type': term['type'],
	}

if __name__ == '__main__':
	raw = yaml.load(requests.get(SOURCE).text)
	legislators = map(parse, raw)
	with open('./data/legislators.json', 'w') as f:
		for person in legislators:
			f.write(json.dumps(person)+'\n')