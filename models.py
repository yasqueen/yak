import json

states = {}
phones = set()
phones.add(u'3148274356')

def clean_phone(input):
	input.replace('-','')

with open('./data/legislators.json') as f:
	for line in f:
		rep = json.loads(line)
		if rep['type'] == 'sen':
			phones.add(clean_phone(rep['phone']))
			state = rep['state'].lower()
			if state in states:
				states[state].append(rep)
			else:
				states[state] = [rep]


