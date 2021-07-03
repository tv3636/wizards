from collections import defaultdict, OrderedDict
import csv, statistics, json

nameLengthCounts = defaultdict(int)
locationCounts = defaultdict(int)
titleCounts = defaultdict(int)
nameCounts = defaultdict(int)
fillerCounts = defaultdict(int)
elements = []

counts = {
	'length': defaultdict(int),
	'location': defaultdict(int),
	'title': defaultdict(int),
	'name': defaultdict(int),
	'filler': defaultdict(int), 
	'combo': defaultdict(int)
}

titles = ['The Great', 'the Bearded', 'The Wizard Empress', 'The Great and Magical', 'The Red Witch', 'The Color Master', 'The Goblin King', 'The Grey Pilgrim', 'The Bird Tamer', 'The Darkness Slayer', 'The East Helper', 'The Witch', 'Holy Magus', 'Holy Arcanist', 'Alien Arcanist', 'Summoner', 'Evoker', 'Runecaster', 'Archmagus', 'Voodoo Priest', 'Solar Mage', 'Sacred Key', 'Holy Monk', 'Stellar Mage', 'Light Mage', 'Transmuter', 'Conjurer', 'Bunny Wizard', 'Prismatic Magi', 'Master Ape', 'Thaumaturge', 'Rogue Mage', 'Sorcerer', 'Cleric', 'Aeromancer', 'Ghost Eater', 'Supa Wizz', 'Void Disciple', 'Illusionist', 'Druid', 'Fortune Teller', 'Adept', 'Battle Mage', 'Witch', 'Shaman', 'Ice Mage', 'Wild Mage', 'Clairvoyant', 'Shadow Mage', 'Hex Mage', 'Chaos Mage', 'Chronomancer', 'Colormancer', 'Diabolist', 'Wise', 'Artificer', 'Sky Master', 'Hydromancer', 'Electromancer', 'Battlemage', 'Geomancer', 'Headless', 'Null Mage', 'Loop Master', 'Hedge Wizard', 'Charmer', 'Oracle', 'Cartomancer', 'Enchanter', 'Crow Master Claire', 'Augurer', 'Ghost Eater', '3D Wizz', 'Mystic', 'Necromancer', 'Arch-Magician', 'Sage', 'Cosmic Mage', 'Evil Arcanist', 'Great Old One', 'Cryptomancer', 'Medium', 'Scryer', 'Cat Wizard El Crypto', 'Bard', 'Punk Rock Arcanist', 'Edge Arcanist', 'Lunar Mage', 'Fortune Master', 'Wizard', 'Arcanist', 'Magus', 'Alchemist', 'Old', 'Diviner', 'Spellsinger', 'Vampyre', 'Pyromancer']
possibleFiller = ['out of the', 'of the', 'of ', 'in the', 'from the']
ignore = ['filler']
categories = list(set(counts.keys()) - set(ignore))

def getName(remaining):
	for fillerWords in possibleFiller:
		if fillerWords in remaining:
			remaining = remaining[:remaining.find(fillerWords)]
			return remaining.strip()

	return remaining.strip()

def validate(title, name, filler, location, fullName):
	titleName = ' '.join((title,name,filler,location)).strip().replace('  ', ' ')
	nameTitle = ' '.join((name,title,filler,location)).strip().replace('  ', ' ')
	original = fullName.strip().replace('  ', ' ')

	if original not in [titleName, nameTitle]:
		print 'old: ', original
		print 'new: ', titleName, nameTitle

def getCombo(nameDict):
	thisGrouping = {}
	for category in nameDict.keys():
		thisGrouping[category] = nameDict[category] != ''

	return str(thisGrouping)

def splitName(fullName):
	location = ''
	name = ''
	title = ''
	filler = ''

	for fillerWords in possibleFiller:
		if fillerWords in fullName and not location:
			location = fullName[fullName.find(fillerWords) + len(fillerWords):].strip()
			filler = fillerWords.strip()

	for possibleTitle in titles:
		if possibleTitle in fullName and not title:
			title = possibleTitle
			name = getName(fullName.replace(title, '').strip())

	if not title:
		name = getName(fullName)

	validate(title, name, filler, location, fullName)

	out = {'length': sum([category != '' for category in [title, name, filler, location]]), 'title': title, 'name': name, 'filler': filler, 'location': location}
	out['combo'] = getCombo(out)

	return out

def writeNameRarity(outputFile='nameRarity.csv', rarityScores=None):
	with open(outputFile, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=['name', 'serial', 'title', 'title score', 'firstName', 'name score', 'location', 'location score', 'length score', 'combo score', 'total score']) 
		writer.writeheader()

		for row in sorted(rarityScores, key=lambda x: x['total'], reverse=True):
			for category in categories + ['total']:
				row['%s score' % category] = "%.2f" % round(row[category], 2)

			row['name'] = elements[int(row['serial'])]['name'].strip()
			row['title'] = row['titleValue']
			row['location'] = row['locationValue']
			del row['titleValue']
			del row['locationValue']
			del row['length']
			del row['combo']
			del row['total']

			writer.writerow(row)

def calculateNameRarity(inputFile='wizards.csv'):
	with open(inputFile) as csvfile:
		for row in csv.DictReader(csvfile):
			elements.append(row)
			name = splitName(row['name'])

			for category in counts.keys():
				counts[category][name[category]] += 1

	rarityScores = []
	tokenSupply = len(elements)
	scoreLists = {}

	for category in counts.keys():
		categoryValues = [counts[category][x] for x in counts[category]]
		scoreLists[category] = { 
			'values': [], 
			'weight': statistics.stdev(categoryValues) / statistics.mean(categoryValues)
		}

	for element in elements:
		name = splitName(element['name'])
		rarity = {}

		for category in counts.keys():
			rarity[category] = float(tokenSupply) / float(counts[category][name[category]])
			scoreLists[category]['values'].append(rarity[category])

		for category in ignore:
			del rarity[category]

		rarity['serial'] = element['Serial']
		rarity['titleValue'] = name['title']
		rarity['firstName'] = name['name']
		rarity['locationValue'] = name['location']
		rarityScores.append(rarity)

		for category in categories:
			scoreLists[category]['values'].append(rarity[category])

	# Adjust score by score distribution
	for category in scoreLists:
		scoreLists[category]['avgScore'] = statistics.mean(scoreLists[category]['values'])

	for i in range(len(elements)):
		for category in categories:
			rarityScores[i][category] /= scoreLists[category]['avgScore']
			rarityScores[i][category] *= scoreLists[category]['weight']

		rarityScores[i]['total'] = rarityScores[i]['length'] + rarityScores[i]['title'] + rarityScores[i]['name'] + rarityScores[i]['location'] + rarityScores[i]['combo']

	return rarityScores


writeNameRarity(outputFile='nameRarity.csv', rarityScores=calculateNameRarity())

