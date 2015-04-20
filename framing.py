import re
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import os.path
from emotion import *
import math


# Get z-score to compare 2 proportions
def two_prop_test(num1, total1, num2, total2):
	numerator = [(num1/total1) - (num2/total2)]
	phat = (num1 + num2) / (total1 + total2)
	denom = math.sqrt(phat*(1-phat)*((1/total1) + (1/total2)))
	return (numerator/denom)

### HYP: Depressed individuals are more likely to put 
### themselves as the object of a negative verb

# Directory example: './mypersonality/depression'
# Returns # of times negative verb is used with 1st person personal pronoun as object 
# and number of times a negative verb is used
def neg_verb_dobj(directory):
	load() # loads depression_verbs
	negverb = 0.0
	nv_pp = 0.0
	perspron = ['me', 'myself', 'ourselves', 'ourself', 'us', 'i', 'we']
	for filename in os.listdir(directory):
		if filename[0] == '.':
			continue
		f = open(directory + str(filename), 'r')
		#print f.read()
		soup = BeautifulSoup(f.read())
		f.close()

		w = soup.find_all(type = "collapsed-dependencies")
		for item in w:
			x = item.find_all(type = "dobj")
			for item in x:
				y = item.find("governor")
				z = item.find("dependent")
				verb = y.contents[0].lower()
				dobj = z.contents[0].lower()
				for regex in depression_verbs:
					if re.match(regex, verb):
						negverb += 1
						if dobj in perspron:
							nv_pp += 1
							#print verb
							#print dobj
	return nv_pp, negverb, len(x)

### HYP: Depressed individuals are less likely to be the 
### subject of verbs with positive outcomes / action verbs, etc.

# List_file example: depression_verbs
# Returns # of times a kind of verb (as given in list_file) is used 
# with a personal pronoun as subject and number of times total that 
# kind of verb is used
def find_verb_subj(directory, list_file):
	pv_pp = 0.0
	posverb = 0.0
	perspron = ['me', 'myself', 'ourselves', 'ourself', 'us', 'i', 'we']
	for filename in os.listdir(directory):
		if filename[0] == '.':
			continue
		f = open(str(directory) + str(filename), 'r')
		#print f.read()
		soup = BeautifulSoup(f.read())
		f.close()

		w = soup.find_all(type = "collapsed-dependencies")
		for item in w:
			x = item.find_all(type = "nsubj")
			for item in x:
				y = item.find("governor")
				z = item.find("dependent")
				verb = y.contents[0].lower()
				subj = z.contents[0].lower()
				for regex in list_file: # positive_verbs
					if re.match(regex, verb):
						posverb += 1
						if subj in perspron:
							pv_pp += 1
							#print verb
							#print dobj
	return pv_pp, posverb, len(x)

### HYP: Depressed individuals are more likely to express 
### regret through an increased usage of modal verbs

# Directory is directory with XMLs, directory2 is directory with the text files
# Returns number of times modal ('would have', etc. - as defined in regex) is used 
# and # of times all verbs are used
def find_modals(directory, directory2):
	verb_types = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	vb_count = 0.0
	md_count = 0.0
	for filename in os.listdir(directory):
		if filename[0] == '.':
			continue
		f = open(str(directory) + str(filename), 'r')
		soup = BeautifulSoup(f.read())
		f.close()

		w = soup.find_all("tokens")
		for item in w:
			allverbs = []
			for verb in verb_types:
				x = item.find_all(text = verb)
				allverbs = allverbs + x
			vb_count += len(allverbs)

	for filename in os.listdir('./project_materials/' + str(directory2) + '/text'):
		if filename[0] == '.':
			continue
		f = open('./project_materials/' + str(directory2) + '/text/' + str(filename))
		regex = '(c|w|sh)ould( have|\'ve|a|ve| of|of)'
		match = re.findall(regex, f.read())
		md_count += len(match)

	return md_count, vb_count

### HYP: Depressed individuals make more use of past tense

# Returns # of times past tense is used
# and number of times any verb is used 
def find_pasttense(directory, directory2):
	verb_types = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	vb_count = 0.0
	vbd_count = 0.0
	for filename in os.listdir(directory):
		if filename[0] == '.':
			continue
		f = open(str(directory) + str(filename), 'r')
		soup = BeautifulSoup(f.read())
		f.close()

		w = soup.find_all("tokens")
		for item in w:
			allverbs = []
			for verb in verb_types:
				x = item.find_all(text = verb)
				allverbs = allverbs + x
				if verb == 'VBD':
					vbd_count += len(x)
			vb_count += len(allverbs)

	return vbd_count, vb_count


### HYP: Depressed individuals make use of fewer actions verbs, more cognitive verbs, etc.
# Returns number of times a type of word (as defined by list_file) is used
# and number of times a verb is used total
def find_verbtype(directory, list_file):
	verb_types = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	vbtype_count = 0.0
	vb_count = 0.0
	for filename in os.listdir(directory):
		if filename[0] == '.':
			continue
		f = open(str(directory) + str(filename), 'r')
		soup = BeautifulSoup(f.read())
		f.close()

		w = soup.find_all("tokens")
		for item in w:
			allverbs = []
			for verb in verb_types:
				x = item.find_all(text = verb)
				allverbs = allverbs + x
				for verb2 in x:
					for regex in list_file:
						if re.match(regex, verb2):
							vbtype_count += 1
			vb_count += len(allverbs)

	return vbtype_count, vb_count	


### HYP: Depressed individuals make use of more transitive constructions 
### when they are the agent of a negative event,but more intransitive 
### constructions when they are the agent of a positive event

# Returns # of times a verb of type in list_file with a personal pronoun subject is used 
# transitively and # of times that verb type occurs with a personal pronoun total
def find_trans(directory, list_file):
	total = 0.0
	trans = 0.0
	perspron = ['me', 'myself', 'ourselves', 'ourself', 'us', 'i', 'we']
	for filename in os.listdir(directory):
		if filename[0] == '.':
			continue
		f = open(str(directory) + str(filename), 'r')
		#print f.read()
		soup = BeautifulSoup(f.read())
		f.close()

		w = soup.find_all(type = "collapsed-dependencies")
		for block in w:
			subj_verbs = []
			obj_verbs = []
			x = block.find_all(type = "nsubj")
			for item in x:
				y = item.find("governor")
				z = item.find("dependent")
				verb = y.contents[0].lower()
				for regex in list_file:
					if re.match(regex, verb):
						subj = z.contents[0].lower()
						if subj in perspron:
							subj_verbs.append(verb)

			x = block.find_all(type = "dobj")
			for item in x:
				y = item.find("governor")
				verb = y.contents[0].lower()
				obj_verbs.append(verb)

			for verb in subj_verbs:
				total += 1
				if verb in obj_verbs:
					trans += 1

	return trans, total


load()
print find_trans('./mypersonality/depression/', depression_verbs)

#redditdep = neg_verb_dobj('./mypersonality/depression')
#redditnon = neg_verb_dobj('./mypersonality/nondepression')
#print two_prop_test(neg_verb_dobj(redditdep[0], redditdep[1], redditnon[0], redditnon[1])
#print find_modals('./mypersonality/depression/', 'mypersonality_depression')



