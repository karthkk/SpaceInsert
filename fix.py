import sys

def breakwrds(word,scores,force=False):
	found_candidates = {}
	level_max_scores = {}
	for i in range(1,len(word)+1):
		best_candidate_word = ''
		best_score = -1
		for j in range(0,i):
			w = word[j:i]
			score = level_max_scores.get(j,0)+scores.get(w.lower(),-2)
			if score>best_score:
				best_score = score
				best_candidate_word = w
		found_candidates[i]=best_candidate_word
		level_max_scores[i]=best_score			
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
	strg = strg.replace("'","")
	wrds = strg.split(' ')
	wrds = filter(lambda x: x.strip() != '', wrds)
	return wrds
	

if __name__ == '__main__':
	f = open(sys.argv[1]).readlines()
	s = ' '.join(f)
	words = s.split(' ')
	words = map(lambda x: x.lower().strip(), words)
	words = filter(lambda x: x.strip()!='',words)
	cnts = {}
	for w in words:
		cnts[w] = cnts.get(w,0)+1
	scored_words = map(lambda x:(x[0],x[1]+len(x[0])),cnts.items())
	proper_words = dict(filter(lambda x: x[1]>2 and len(x[0])>1 ,scored_words))
	
	dicwords = open('allwords').readlines()
	dicwords = dict(map(lambda x:(x.strip(),len(x)*len(x)),dicwords))
	proper_words.update(dicwords)

	proper_words = dict(filter(lambda x:  len(x[0])>1 ,proper_words.items()))

	#print proper_words
	proper_words['a'] = 1
	proper_words['i'] = 1
	s = open('/tmp/nf','w')
	for line in file(sys.argv[1]):
		words = getwords(line.strip())
		allw = []
		for w in words:
			if (cnts.get(w.lower(),0) < 3 and len(w)>5) or len(w) > 15 :
				wrd = breakwrds(w,proper_words,len(w)>15)
				allw.append( wrd )
			else:
				allw.append( w )
		s.write( ' '.join(allw) )
		print ' '.join(allw)
		s.write("\n")
	s.close()
