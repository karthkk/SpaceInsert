import sys
import os
import math

def breakwrds(word,scores,force=False):
	found_candidates = {}
	level_max_scores = {}
	for i in range(1,len(word)+1):
		best_candidate_word = ''
		best_score = -1
		for j in range(0,i):
			w = word[j:i]
			score = level_max_scores.get(j,0)+scores.get(w.lower(),-100)
			if score>best_score:
				best_score = score
				best_candidate_word = w
		found_candidates[i]=best_candidate_word
		level_max_scores[i]=best_score			
	print level_max_scores
	print found_candidates
	words = []
	s = len(word)
	while s>0:
		sw = found_candidates.get(s)
		if not force and not sw.lower() in scores:
			return word
		if len(sw) == 0:
			return word
		words.append(sw)
		s = s-len(sw)
	words.reverse()
	return ' '.join(words)

def getwords(strg):
	strg = strg.replace(',',' , ')
	strg = strg.replace('.',' . ')
	strg = strg.replace('?',' ? ')
	strg = strg.replace('!',' ! ')
	strg = strg.replace('-',' - ')
	strg = strg.replace('"',' " ')
#	strg = strg.replace("'","")
	wrds = strg.split(' ')
	wrds = filter(lambda x: x.strip() != '', wrds)
	return wrds
	
def fix_floating_s(words):
	words = words.replace(' s ', 's ')
	return words

def get_word_prob(files):
	cnts = {}
	for fl in files:
		f = open(fl).readlines()
		s = ' '.join(f)
		words = getwords(s)
		words = map(lambda x: x.lower().strip(), words)
		words = filter(lambda x: x.strip()!='',words)
		for w in words:
			cnts[w] = cnts.get(w,0)+1
	scored_words = map(lambda x:(x[0],x[1]+len(x[0])),cnts.items())
	proper_words = dict(filter(lambda x:  len(x[0])>1 ,scored_words))
	return proper_words
	

if __name__ == '__main__r':
	word_probs = get_word_prob(map(lambda x: 'sample_texts/'+x,os.listdir('sample_texts')))
	wp = word_probs.items()
	wp.sort(lambda x,y:cmp(y[1],x[1]))
	f = open('probs','w')
	f.write('\n'.join(map(lambda x: x[0].replace(':','')+':'+str(x[1]*len(x[0])),wp)))
	f.close()

def loadprobs():
	s = open('probs').readlines()
	l = map(lambda x: x.strip().split(':'),s)
	m = map(lambda x: (x[0],math.log(int(x[1]))*math.pow(len(x[0]),1.2)),l)
	return dict(m)

if __name__ == '__main__':
	proper_words = {}
	dicwords = open('allwords').readlines()
	dicwords = dict(map(lambda x:(x.strip(),len(x)),dicwords))
	proper_words.update(dicwords)
	proper_words.update(get_word_prob([sys.argv[1]]))
	proper_words.update(loadprobs())

	print 'st ' +  str(proper_words.get('st'))
	print 'coast ' + str( proper_words.get('coast'))
	#print proper_words
	proper_words['a'] = 1
	proper_words['i'] = 1
	s = open('/tmp/nf','w')
	for line in file(sys.argv[1]):
		words = getwords(line.strip())
		allw = []
		for w in words:
			if (proper_words.get(w.lower(),0) < 3 and len(w)>5) or len(w) > 15 :
				wrd = breakwrds(w,proper_words,len(w)>15)
				allw.append( fix_floating_s(wrd) )
			else:
				allw.append( w )
		s.write( ' '.join(allw) )
#		print ' '.join(allw)
		s.write("\n")
	s.close()
