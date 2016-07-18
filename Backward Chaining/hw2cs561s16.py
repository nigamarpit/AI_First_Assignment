#import re
import sys
from copy import deepcopy
#import collections

var_count = 0
tl=[]
kb=[]
atom=[]
imp=[]
goal=""
iter_limit = 100
cur_iter = 0

def main():
	global goal
	fr=open(sys.argv[2],'r')
	query=fr.readline().rstrip('\n')
	#print query
	n=int(fr.readline())
	#print n

	for i in range(n):
		kb.append(fr.readline().rstrip('\n'))
	#print kb
	#l=fetch_rules_for_goal(kb,query)
	#print l
	for rule in kb:
		seperate_rule(rule)
	goal=query
	#print atom
	#print imp
	#print(getPredicate("Tells(Anakin, x, Sidious)"))
	#print(getArguments("Tells(Anakin, x, Sidious)"))
	#print(break_and("ViterbiSquirrel(x) && Secret(y) && Tells(x, y, z) && Hostile(z)"))
	#standardize_variables(['ViterbiSquirrel(x) && Secret(y) && Tells(x, y, z) && Hostile(z)', 'Traitor(x)'])
	#print build_clause("Tells",['x0', 'y0', 'z0'])
	fol_bc_ask(kb,break_and(query))
	#unify('Traitor(x0)','Traitor(Anakin)',{})
	#print tl
	writeToOutputFile(tl)


def writeToOutputFile(tl):
	f = open('output.txt', 'w+')
	for i in range(len(tl)):
		if getPredicate(tl[i].split(': ')[1])==getPredicate(goal) and tl[i].split(': ')[0]!="Ask":
			print "tli: ", tl[i]
			f.write(tl[i])
			f.write('\n')
			f.write(tl[i].split(':')[0])
			f.close()
			return tl[i].split(': ')[0]
		else:
			#print tl[i]
			f.write(tl[i])
			f.write('\n')
	#f.write(tl[-1].split(':')[0])
	f.close()
	return tl[-1].split(': ')[0]

def fol_bc_ask(kb, query):
	res = list()
	for x in fol_bc_or(kb, query, {}):
		res.append(x)
	return res
	#return fol_bc_or(kb, query, {})

def fol_bc_or(kb, goal, theta):
	global cur_iter, iter_limit

	if cur_iter < iter_limit:
		cur_iter += 1
	else:
		return
	#print "OR:::KB:::"+str(kb)
	#print "OR:::GOAL:::"+str(goal)
	thetan=deepcopy(theta)
	#print (fetch_rules_for_goal(kb,goal))
	#return
	#print print_clause(goal)
	tl.append(print_clause(goal))
	for rule in fetch_rules_for_goal(kb,goal):
	#	print "Rule::"+str(rule)
		#print "rule: ", rule
		lhs,rhs=standardize_variables(rule)
	#	print "lhs, rhs", lhs, rhs
		#print "rhs",rhs
		#print "RHS:::"+str(rhs)
		#print goal
		#print thetan
		#return
		#print kb
		#print "LHS:::"+str(lhs)
		#fol_bc_and(kb, lhs, y)
		#print "DEBUG 1"
	#	print thetan
		print "rhs, goal, thetan:", rhs, goal, thetan
		y=unify(rhs, goal, thetan)
		print "y: ", y
		for theta1 in fol_bc_and(kb, lhs, y):
			if y is None:
				tl.append("False: "+str(tl.append(tl[len(tl)-1])))
			else:
				print "theta1, goal[0]: ", theta1, goal[0]
				query=subs(theta1,goal[0])
				print "query: ", query
				tl.append("True: "+str(query))
			yield theta1

def subs(theta,clause):
	#print clause
	s=getPredicate(clause)+'('
	for i in range(len(getArguments(clause))-1):
		if (getArguments(clause)[i]) in theta.keys():
			s=s+str(theta[getArguments(clause)[i]])+', '
		else:
			s=s+str(getArguments(clause)[i])+', '
	if getArguments(clause)[-1] in theta.keys():
		s=s+str(theta[getArguments(clause)[-1]])+')'
	else:
		s=s+str(getArguments(clause)[-1])+')'
	return s

def print_clause(l_clause):
	clause=getPredicate(l_clause[0])+'('
	for i in range(len(getArguments(l_clause[0]))-1):
		if isvariable(getArguments(l_clause[0])[i]):
			clause=clause+'_'+', ';
		else:
			clause=clause+ getArguments(l_clause[0])[i]+', '
	if isvariable(getArguments(l_clause[0])[-1]):
		clause="Ask: "+clause+'_'+')'
	else:
		clause="Ask: "+clause+getArguments(l_clause[0])[-1]+')'
	return clause

def fol_bc_and(kb, goals, theta):
	#print theta
	#print "AND_GOALS::"+str(goals)
	#print len(goals)
	thetan=deepcopy(theta)
	#=raw_input()
	if theta is None:
		tl.append("False: "+tl[-1].split(': ')[1])
		pass
	elif len(goals)==0:
		#print "here"
		yield thetan
	else:
		#print "here",goals[0]
		first, rest = goals[0], goals[1:]
		firstn=deepcopy(first)
		restn=deepcopy(rest)
		#print "FIRST::"+str(firstn)
		#print "REST::"+str(restn)
		s=substitute(thetan, firstn)
		#print "Subs",s
		for theta1 in fol_bc_or(kb, s , thetan):
			for theta2 in fol_bc_and(kb, restn, theta1):
				yield theta2

def substitute(theta, clause):
	#print "Theta",theta
	#print "Clause",clause
	pred=getPredicate(clause)
	args=getArguments(clause)
	args_new=[]
	for arg in args:
		if arg in theta.keys():
			args_new.append(theta[arg])
		else:
			args_new.append(arg)
	return [build_clause(pred,args_new)]


def seperate_rule(rule):
	b=rule.split(' => ')
	if len(b)>1:
		rhs=rule.split(' => ')[1].rstrip('\n')
		lhs=rule.split(' => ')[0]
		imp.append([lhs,rhs])
	else:
		rhs=rule.split(' => ')[0].rstrip('\n')
		lhs=[]
		atom.append([lhs,rhs])

def standardize_variables(rule):
	rules=break_rule(rule)
	global var_count
	#print rules
	#print rules##lhs
	if rules[0]!=[]:
		lhs=""
		rhs=""
		for rule in break_and(rules[0]):
			#print rule
			args=getArguments(rule)
			for i in range(len(args)):
				if isvariable(args[i]):
					args[i]=args[i]+str(var_count)
			lhs=lhs+' && '+ build_clause(getPredicate(rule),args)
		for rule in break_and(rules[1]):
			args=getArguments(rule)
			for i in range(len(args)):
				if isvariable(args[i]):
					args[i]=args[i]+str(var_count)
			rhs=rhs+' && '+build_clause(getPredicate(rule),args)
		var_count += 1
		return break_and(lhs[4:]),break_and(rhs[4:])
	else:
		lhs=""
		rhs=""
		for rule in break_and(rules[1]):
			args=getArguments(rule)
			for i in range(len(args)):
				if isvariable(args[i]):
					args[i]=args[i]+str(var_count)
			rhs=rhs+' && '+build_clause(getPredicate(rule),args)
		var_count += 1
		return lhs,break_and(rhs[4:])

def unify(a, b, s):
	print "a, b, s:", a, b, s 
	print type(a), type(b)
	if s == None:
		return None
	elif a == b:
		return s
	elif isvariable(a):
		print "isvariable"
		return unify_var(a,b,s)
	elif isvariable(b):
		print "isvariable2"
		return unify_var(b,a,s)
	elif iscompound(a) and iscompound(b):
		print "is compound"
		print "getargs(a), getargs(b)", getArguments(a), getArguments(b)
		return unify(getArguments(a), getArguments(b), unify(getPredicate(a), getPredicate(b), s))
	elif type(a) == type([]) and type(b) == type([]):
		print "islist"
		if len(a) == 0:
			return s
		else:
			return unify(a[1:], b[1:], unify(a[0], b[0], s))
	else:
		print "ret none"
		return None

def unify_var(var, x, s):
	if var in s.keys():
		return unify(s[var], x, s)
	elif x in s.keys():
		return unify(var, s[x], s)
	else:
		print ""
		print "s, var, x: ", s, var, x
		s[var] = x
		#s = extend(s, var, x)
		print "new s:", s
		return s
'''		
def unify(a, b, s):

	#print "a,b", a, b
	#print b
	print "a: ", a
	print "a0: ", a[0]
	x=getArguments(a[0])
	print "x: ", x
	#print x
	y=getArguments(b[0])
	#print y
	#print "s"+str(s)
	#print isvariable(x[0][0])
	#print isvariable(y[0][0])
	if s is None:
		return None
	elif a == b:
		return s
	elif isvariable(x[0][0]) and len(x)==1:
		print "x0, y0, s:", x[0], y[0], s
		return unify_var(x[0], y[0], s)
	elif isvariable(y[0][0]) and len(y)==1:
		return unify_var(y[0], x[0], s)
	elif len(x)>1 and len(y)>1 and len(x) == len(y):
		#print "here"
		#print x
		#print build_clause(getPredicate(a),[x[0]])
		#print y
		if not x:
			return s
		else:
			return unify([build_clause(getPredicate(a[0]),x[1:])], [build_clause(getPredicate(a[0]),y[1:])], unify([build_clause(getPredicate(a[0]),[x[0]])], [build_clause(getPredicate(a[0]),[y[0]])], s))
	else:
		return None

def unify_var(var, x, s):
	if var in s:
		return unify(s[var], x, s)
	elif x in s:
		print "var, s[x], s: ", var, s[x], s
		return unify(var, s[x], s)
	#elif occur_check(var, x, s):
	#	return None
	else:
		return extend(s, var, x)
'''

def occur_check(var, x, s):
	if var == x:
		return True
	elif x[1] and x in s:
		return occur_check(var, s[x], s)
	else:
		return False


def extend(s, var, val):
	s2 = s.copy()
	s2[var] = val
	return s2

def getPredicate(clause):
	return clause.split('(')[0]

def getArguments(clause):
	#print clause
	return clause.split('(')[1].split(')')[0].split(', ')

def isvariable(pred):
	if type(pred) == type([]):
		return False

	if pred[0].islower():
		return True
	else:
		return False

def iscompound(clause):
		print "clause", clause
		if type(clause) == type([]):
			return False
		if clause[0].isupper() and '(' in clause and ')' in clause:
			return True
		else:
			return False

def break_and(rule):
	return rule.split(' && ')

def build_clause(pred,args):
	s=pred+'('
	for i in range(len(args)-1):
		s=s+args[i]+', '
	s=s+str(args[-1])+')'
	return s

def fetch_rules_for_goal(kb,goal):
	l=[]
	for rule in kb:
		#print rule
		#raw_input()
		if getPredicate(break_rule(rule)[1])==getPredicate(goal[0]):
			l.append(rule)
	return l

def break_rule(rule):
	b=rule.split(' => ')
	if len(b)>1:
		rhs=rule.split(' => ')[1].rstrip('\n')
		lhs=rule.split(' => ')[0]
	else:
		rhs=rule.split(' => ')[0].rstrip('\n')
		lhs=[]
	return [lhs,rhs]

if __name__ == "__main__":
	main()
