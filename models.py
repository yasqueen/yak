import json

states = {}
phones = set()

def clean_phone(input):
	input.replace('-','').replace('+','')[-10:]

phones.add(clean_phone(u'3148274356'))

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


