import json

states = {}
phones = set()
phones.add(u'314-827-4356')

with open('./data/legislators.json') as f:
	for line in f:
		rep = json.loads(line)
		if rep['type'] == 'sen':
			phones.add(rep['phone'])
			state = rep['state'].lower()
			if state in states:
				states[state].append(rep)
			else:
				states[state] = [rep]


