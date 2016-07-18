from decimal import Decimal
import copy
import sys
Dictionary={}
Vars=[]
decision_nodes=[]
def main():
	fi=open(sys.argv[2],'r')
	flag=0
	inbound=[]
	queries=[]
	tree=[]
	global Dictionary
	utilities=[]
	for lines in fi:
		inbound.append(lines.rstrip('\n'))    
	for i in range(len(inbound)):
		if flag==0 and inbound[i]!='******':
			queries.append(inbound[i])
		elif flag==0 and inbound[i]=='******':
			flag=1
		elif flag==1:
			if inbound[i]=='******':
				flag=2
			elif inbound[i]!='***':
				tree.append(inbound[i])
			else:
				addelement(tree)
				tree=[]
		elif flag==2:
			utilities.append(inbound[i])
	addelement(tree)
	if len(utilities)>0:
		addelement(utilities)
	#print "Global Dictionary",Dictionary
	#print "utilities",utilities
	#return
##	#print queries
	fo = open('output.txt', 'w+')
	for query in queries:
		try:
			calculation(query,fo)
		except:
			continue
		fo.write('\n')
	fi.close()
	fi.close

def addelement(tree):
	#global Dictionary
	#global Vars
	#global decision_nodes
	if '|' in tree[0]:
		dDictionary=probDictionary(tree[1:])
		s=tree[0].split('| ')
		Dictionary[s[0].strip()]=[s[1].split(),dDictionary]
		Vars.append(s[0].strip())
	elif tree[1]!='decision':
		Dictionary[tree[0]]={'noParent':float(tree[1])}
		Vars.append(tree[0])
	else:
		decision_nodes.append(tree[0])
		Dictionary[tree[0]]='decision'
		Vars.append(tree[0])

def probDictionary(dtree):
	dDictionary={}
	for i in range(len(dtree)):
		dDictionary["".join(dtree[i].split()[1:])]=float(dtree[i].split()[0])
	return dDictionary

def enumerate_all(Vars, e):
	if not Vars:
		return 1.0
	Y = Vars[0]
	if Y in e:
		return prob_parent(Y,e[Y],e)*enumerate_all(Vars[1:],e)
	else:
		res = 0.0
		for y in ['+','-']:
			prob_first = prob_parent(Y, y, e)
			e[Y] = y
			prob_rest = enumerate_all(Vars[1:], e)
			res = res+(prob_first*prob_rest)
		del e[Y]
		return res

def enumeration_ask(query):
	l= query[0].split(' = ')
	e  = {}
	for item in query[1].strip().split(', '):
		item = item.split(' = ')
		e[item[0]]=item[1]
	e[l[0]]=l[1]
	prob_first = enumerate_all(Vars, e)
	if l[1]=='+':
		e[l[0]]='-'
	else:
		e[l[0]]=='+'
	prob_rest = enumerate_all(Vars, e)
	res = prob_first/(prob_first + prob_rest)
	return res

def prob_parent(key, value, e):
	if 'decision' in Dictionary[key]:
		return 1.0
	if 'noParent' in Dictionary[key]:
		if value=='-':
			return 1-Dictionary[key]['noParent']
		else:
			return Dictionary[key]['noParent']
	new_key = []
	for parent in Dictionary[key][0]:
		new_key.append(e[parent])
	new_key = "".join(new_key)
	if value=='-': 
		return 1-Dictionary[key][1][new_key]
	else: 
		return Dictionary[key][1][new_key]

def prob(query):
	query=query.split('(')[1].split(')')[0]
	query=query.split(' | ')
	if len(query) != 1:
		return enumeration_ask(query)
	else:
		query = query[0].split(', ')
		e = {}
		for term in query:
			term = term.split(' = ')
			e[term[0]] = term[1]
		Q = enumerate_all(Vars, e)
		return Q	
		
def eu(query):
	query=query.split('(')[1].split(')')[0]
	l=query.split(' | ')
	l1 = []

	for i in range(len(l)):
		q = l[i].split(', ')
		l1.extend(q)

	l = l1
	e = {}
	parents= Dictionary['utility'][0]
	for item in l:
		item = item.split(' = ')
		e[item[0]] = item[1]

	if len(parents) == 1:
		parent = parents[0]
		res = Compute1(parent, e)

		return res
	elif len(parents) == 2:
		res = Compute2(parents, e)
		return res
	else:
		res = Compute3(parents, e)
		return res

def Compute1(parent, e):
	flag = False
	value = False
	if parent in e:
		flag = True
		value = e[parent]

	localDictionary= {}
	X = Dictionary['utility'][0][0]
	U = Dictionary['utility'][1]
	e[X] = '+'
	r1 = enumerate_all(Vars, e)
	e[X] = '-'
	r2 = enumerate_all(Vars, e)
	localDictionary['+']  = r1/(r1 + r2) * U['+']
	localDictionary['-'] = (1 - r1/(r1 + r2)) * U['-']
	del e[X]

	res   = 0.0
	if flag:
		if not value:
			res = res + localDictionary['-']
		else:
			res = res + localDictionary['+']
	else:
		res = res+localDictionary['+']
		res = res+localDictionary['-']
	return res

def Compute2(parents, e):
	fact = {}
	for parent in parents:
		if parent in e:
			fact[parent] = e[parent]	
	localDictionary= {}
	combination = Dictionary['utility'][1].keys()
	parents = Dictionary['utility'][0]
	U = Dictionary['utility'][1]

	for item in combination:
		newDictionary = copy.copy(e)
		for parent, elem in zip(parents, item):
			newDictionary[parent] = elem
		res = enumerate_all(Vars, newDictionary)
		res = res * U[item]
		localDictionary[item] = res

	res = 0.0
	if len(fact) == 0:
		res = sum(localDictionary.values())
	if len(fact) == 1:
		if parents[0] in fact:
			res = res+localDictionary[fact[parents[0]]+'+']
			res = res+localDictionary[fact[parents[0]]+'-']
		else:
			res = res+localDictionary['+'+fact[parents[1]]]
			res = res+localDictionary['-'+fact[parents[1]]]			
	if len(fact) == 2:
		if not parents[0] and not parents[1]:
			res = res + localDictionary['--']
		elif not parents[0] and parents[1]:
			res = res + localDictionary['-+']
		elif parents[0] and not parents[1]:
			res = res + localDictionary['+-']
		elif parents[0] and parents[1]:
			res = res + localDictionary['++']
	return res

def Compute3(parents, e):
	fact = {}
	for parent in parents:
		if parent in e:
			fact[parent] = e[parent]
	
	localDictionary= {}
	combination = Dictionary['utility'][1].keys()
	parents = Dictionary['utility'][0]
	U = Dictionary['utility'][1]

	for item in combination:
		newDictionary = copy.copy(e)
		for parent, elem in zip(parents, item):
			newDictionary[parent] = elem
		res = enumerate_all(Vars, newDictionary)
		res = res * U[item]
		localDictionary[item] = res

	res = 0.0
	if len(fact) == 0:
		res = sum(localDictionary.values())
	elif len(fact) == 1:
		if parents[0] in fact:
			res = res + localDictionary[fact[parents[0]]+'--']
			res = res + localDictionary[fact[parents[0]]+'-+']
			res = res + localDictionary[fact[parents[0]]+'+-']
			res = res + localDictionary[fact[parents[0]]+'++']
		elif parents[1] in fact:
			res = res + localDictionary['-'+fact[parents[0]]+'-']
			res = res + localDictionary['-'+fact[parents[0]]+'+']
			res = res + localDictionary['+'+fact[parents[0]]+'-']
			res = res + localDictionary['+'+fact[parents[0]]+'+']
		else:
			res = res + localDictionary['--'+fact[parents[0]]]
			res = res + localDictionary['-+'+fact[parents[0]]]
			res = res + localDictionary['+-'+fact[parents[0]]]
			res = res + localDictionary['++'+fact[parents[0]]]
	elif len(fact) == 2:
		if parents[0] in fact and parents[1] in fact:
			res = res + localDictionary[fact[parents[0]]+fact[parents[1]]+'-']
			res = res + localDictionary[fact[parents[0]]+fact[parents[1]]+'+']
		elif parents[0] in fact and parents[2] in fact:
			res = res + localDictionary[fact[parents[0]]+'-'+fact[parents[2]]]
			res = res + localDictionary[fact[parents[0]]+'+'+fact[parents[2]]]
		else:
			res = res + localDictionary['-'+fact[parents[1]]+fact[parents[2]]]
			res = res + localDictionary['+'+fact[parents[1]]+fact[parents[2]]]
	else:
			res = res + localDictionary[fact[parents[0]]+fact[parents[1]]+fact[parents[2]]]
	return res


def meu(query):
	query=query.split('(')[1].split(')')[0]
	query = query.split(' | ')
	l1  = []
	e = {}
	fact = {}
	newQuery = []
	for index in range(len(query)):
		q = query[index].split(', ')
		l1.extend(q)
	#print "l1",l1
	#print decision_nodes
	for item in l1:
		item = item.split(' = ')
		if item[0] in decision_nodes:
			newQuery.append(item[0])
			continue
		#print "Items",item[0],item[1]
		#if len(item)>1:
		e[item[0]]=item[1]

	if len(decision_nodes) == 1:
		localDictionary = Dec1(newQuery[0], e)
		return localDictionary
	elif len(decision_nodes) == 2:
		localDictionary = Dec2(newQuery, e)
		return localDictionary
	else:
		localDictionary = Dec3(newQuery, e)
		return localDictionary

def Dec1(dec, e):
		newDictionary  = copy.copy(e)
		localDictionary = {}
		parents  = Dictionary['utility'][0]
		for val in ['+', '-']:
			newDictionary[dec] = val
			if len(parents) == 1:
				parent = parents[0]
				res = Compute1(parent, newDictionary)
			elif len(parents) == 2:
				res = Compute2(parents, newDictionary)
			else:
				res = Compute3(parents, newDictionary)
			localDictionary[val] = res
		#print sol
		if localDictionary['+'] > localDictionary['-']:
			res = int(round(localDictionary['+']))
			res = '+ ' + str(res)
		else:
			res = int(round(localDictionary['-']))
			res = '- ' + str(res)
		return res

def Dec2(dlst, e):
	newDictionary = copy.copy(e)
	localDictionary= {}
	parents = Dictionary['utility'][0]
	for val in ['--', '-+', '+-', '++']:
		newDictionary[dlst[0]] = val[0]
		newDictionary[dlst[1]] = val[1]
		if len(parents) == 1:
			parent = parents[0]
			res = Compute1(parent, newDictionary)
		elif len(parents) == 2:
			res = Compute2(parents, newDictionary)
		else:
			res = Compute3(parents, newDictionary)
		localDictionary[val] = res
	Key = None
	Max = None
	for key, value in localDictionary.items():
		if Max == None or Max < value:
			Key = key
			Max = value
	Max = str(int(round(Max)))
	res=" ".join(Key)+" "+Max
	return res

def Dec3(dlst, e):
	newDictionary = copy.copy(e)
	localDictionary= {}
	parents = Dictionary['utility'][0]
	for val in ['---','--+','-+-','-++','+--','+-+','++-','+++']:
		newDictionary[dlst[0]] = val[0]
		newDictionary[dlst[1]] = val[1]
		if len(parents) == 1:
			parent = parents[0]
			res = Compute1(parent, newDictionary)
		elif len(parents) == 2:
			res = Compute2(parents, newDictionary)
		else:
			res = Compute3(parents, newDictionary)
		localDictionary[val] = res
	Key = None
	Max = None
	for key, value in localDictionary.items():
		if Max == None or Max < value:
			Key = key
			Max = value
	Max = str(int(round(Max)))

	res = " ".join(Key)+" "+Max
	return res

def calculation(query,fo):
	if query[0]=='P':
		fo.write(str(Decimal(str(prob(query))).quantize(Decimal('.01'))))
		#print Decimal(str(prob(query))).quantize(Decimal('.01'))
	elif query[0]=='E':
		fo.write(str(int(round(eu(query)))))
		#print eu(query)
		#print int(round(eu(query)))
	elif query[0]=='M':
		fo.write(str(meu(query)))
		#print meu(query)

if __name__=="__main__":
	main()