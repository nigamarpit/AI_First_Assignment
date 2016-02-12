import sys
from sys import maxsize
class Node:
  def __init__(self,node,depth,heur,boardstate):
    self.node=node
    self.depth=depth
    self.heur=heur
    self.boardstate=boardstate
    self.children=[]

  def add_child(self,c):
    self.children.append(c)

class Search_Game:
  def make_tree(self,n,a,b,c):
    #print n
    #print a
    #print b
    #print c
    if c=='X':
      p='O'
    elif c=='O':
      p='X'
    dict={0:'A',1:'B',2:'C',3:'D',4:'E'}
    l=[]
    nodes=[]
    for i in range(5):
      for j in range(5):
        k=(5*i)+j
        node=dict[j]+str(i+1)
#top    
        if b[k]=='*':
          if k>4 and b[k-5]==c:
            del l[:]
            l.extend(b)
            l[k]=c
            if k<20 and b[k+5]==p:
              l[k+5]=c
            if k%5!=0 and b[k-1]==p:
              l[k-1]=c
            if (k+1)%5!=0 and b[k+1]==p:
              l[k+1]=c
            if node not in nodes:
              n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
              nodes.append(node)
#left            
          if k%5!=0 and b[k-1]==c:
            del l[:]
            l.extend(b)
            l[k]=c
            if k>4 and b[k-5]==p:
              l[k-5]=c
            if (k+1)%5!=0 and b[k+1]==p:
              l[k+1]=c
            if k<20 and b[k+5]==p:
              l[k+5]=c
            if node not in nodes:
              n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
              nodes.append(node)
#right    
          if (k+1)%5!=0 and b[k+1]==c:
            del l[:]
            l.extend(b)
            l[k]=c
            if k>4 and b[k-5]==p:
              l[k-5]=c
            if k%5!=0 and b[k-1]==p:
              l[k-1]=c
            if k<20 and b[k+5]==p:
              l[k+5]=c
            if node not in nodes:
              n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
              nodes.append(node)
#bottom
          if k<20 and b[k+5]==c:
            del l[:]
            l.extend(b)
            l[k]=c
            if k>4 and b[k-5]==p:
              l[k-5]=c
            if k%5!=0 and b[k-1]==p:
              l[k-1]=c
            if (k+1)%5!=0 and b[k+1]==p:
              l[k+1]=c
            if node not in nodes:
              n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
              nodes.append(node)
#center none

          if k>4 and k<20 and (k+1)%5!=0 and k%5!=0:
            del l[:]
            l.extend(b)
            if l[k-1]!=c and l[k+1]!=c and l[k-5]!=c and l[k+5]!=c and l[k]=='*':
              l[k]=c
              #print str(k)+node
              if node not in nodes:
                n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
                nodes.append(node)
#corner none
          if k==0 and b[1]!=c and b[5]!=c:
            del l[:]
            l.extend(b)
            l[k]=c
            n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
          elif k==4 and b[3]!=c and b[9]!=c:
            del l[:]
            l.extend(b)
            l[k]=c
            n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
          elif k==20 and b[15]!=c and b[21]!=c:
            del l[:]            
            l.extend(b)
            l[k]=c
            n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
          elif k==24 and b[19]!=c and b[23]!=c:
            del l[:]
            l.extend(b)
            l[k]=c
            n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
#borders
          if k in [1,2,3] and b[k-1]!=c and b[k+1]!=c and b[k+5]!=c:
            del l[:]
            l.extend(b)
            l[k]=c
            n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
          elif k in [5,10,15] and b[k-5]!=c and b[k+1]!=c and b[k+5]!=c:
            del l[:]
            l.extend(b)
            l[k]=c
            n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
          elif k in [9,14,19] and b[k-5]!=c and b[k-1]!=c and b[k+5]!=c:
            del l[:]
            l.extend(b)
            l[k]=c
            n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
          elif k in [21,22,23] and b[k-5]!=c and b[k-1]!=c and b[k+1]!=c:
            del l[:]
            l.extend(b)
            l[k]=c
            n.add_child(Node(node,n.depth+1,self.calc_heur(a,l,c),list(l)))
    #for child in n.children:
     # print child.node+str(child.boardstate)+str(child.heur)
    return n

  def main(self):
    l=[]
    fr=open(sys.argv[2],'r')
    for lines in fr:
      line=lines.rstrip('\n')
      l.append(line)
    if l[0][0] in ['1','2','3']:
      a=[]
      for i in range(3,8):
        a.extend(l[i].split())
      a=map(int,a)      
      b=[]
      for i in range(8,13):
        for j in range(5):
          b.extend(l[i][j])

      if(l[1].rstrip()=='X'):
        c='X'
        p='O'
      elif(l[1].rstrip()=='O'):
        c='O'
        p='X'
      n=Node('root',0,self.calc_heur(a,b,c),b)

    if l[0].rstrip()=='1':
      self.writeToOutputFile(self.gbfs(self.make_tree(n,a,b,c)))

    elif l[0].rstrip()=='2':
      self.mm(n,a,int(l[2]),l[1].rstrip(),False)
    
    elif l[0].rstrip()=='3':
      self.abp(n,a,int(l[2]),l[1].rstrip(),False)

    elif l[0].rstrip()=='4':
      f = open('next_state.txt', 'w+')
      f.close()
      if(l[1].rstrip()=='X'):
        c='X'
        p='O'
      elif(l[1].rstrip()=='O'):
        c='O'
        p='X'
      p1=l[1][0]
      p1_algo=l[2][0]
      p1_depth=l[3][0]
      p2=l[4][0]
      p2_algo=l[5][0]
      p2_depth=l[6][0]
      a=[]
      for i in range(7,12):
        a.extend(l[i].split())
      a=map(int,a)      
      b=[]
      for i in range(12,17):
        for j in range(5):
          b.extend(l[i][j])
      turn=0
      state=[]
      state=b
      while(self.gameover(state)):
        n=Node('',0,self.calc_heur(a,state,c),list(state))
        if turn%2==0:
          if p1_algo=='1':
            state=self.gbfs(self.make_tree(n,list(a),list(state),c))
          elif p1_algo=='2':
            state=self.mm(n,list(a),int(p1_depth),p1,True)
          elif p1_algo=='3':
            state=self.abp(n,a,int(p1_depth),p1,True)
        else:
          if p2_algo=='1':
            state=self.gbfs(self.make_tree(n,a,state,c))
          elif p2_algo=='2':
            state=self.mm(n,list(a),int(p2_depth),p2,True)
          elif p2_algo=='3':
            state=self.abp(n,a,int(p2_depth),p2,True)
        self.writeToTraceState(state)
        turn=turn+1
    else:
      fr.close()
      return
    fr.close()

  def gameover(self,b):
    for x in range(25):
      if b[x]=='*':
        return True
    return False

  def gbfs(self,n):
    e=[]      
    for i in range(len(n.children)):
      e.append(n.children[i].heur)
    for i in range(len(n.children)):
      if(n.children[i].heur==max(e)):
        return n.children[i].boardstate
    return n.boardstate

  def mm(self,n,a,d,c,ret):
    if c=='X':
      p='O'
    elif c=='O':
      p='X'
    queue=[]
    queue.append(n)
    while queue:
      e=queue.pop(0)
      if e.depth<int(d) and e.depth%2==0:
        r=self.make_tree(e,a,e.boardstate,c)
        for x in range(len(e.children)):
          queue.append(e.children[x])
      elif e.depth<int(d) and e.depth%2!=0:
        s=self.make_tree(e,a,e.boardstate,p)
        for x in range(len(e.children)):
          queue.append(e.children[x])
    f = open('traverse_log.txt', 'w+')
    f.write('Node,Depth,Value'+'\n')
    v = self.mm_max(n,d,f)
    f.close()
    if ret==True:
      return v[1].boardstate
    else:
      self.writeToOutputFile(list(v[1].boardstate))

  def mm_max(self,n,d,f):
    max_heur=-maxsize
    if n.depth==d-1:
      f.write(n.node+','+str(n.depth)+','+'-Infinity'+'\n')
      for x in range(len(n.children)):
        if n.children[x].heur>max_heur:
          max_heur=n.children[x].heur
          move = n.children[x]
        f.write(n.children[x].node+','+str(n.children[x].depth)+','+str(n.children[x].heur)+'\n')
        f.write(n.node+','+str(n.depth)+','+str(max_heur)+'\n')
      return (max_heur, move)
    elif n.depth<d-1:
      f.write(n.node+','+str(n.depth)+','+'-Infinity'+'\n')
      for x in range(len(n.children)):
        v = self.mm_min(n.children[x],d,f)
        if v[0] > max_heur:
          max_heur = v[0]
          move = n.children[x]
        f.write(n.node+','+str(n.depth)+','+str(max_heur)+'\n')
      return (max_heur, move)
    else:
      return

  def mm_min(self,n,d,f):
    min_heur=maxsize
    if n.depth==d-1:
      f.write(n.node+','+str(n.depth)+','+'Infinity'+'\n')
      for x in range(len(n.children)):        
        if -n.children[x].heur<min_heur:
          min_heur=-n.children[x].heur
          move = n.children[x]
        f.write(n.children[x].node+','+str(n.children[x].depth)+','+str(-n.children[x].heur)+'\n')
        f.write(n.node+','+str(n.depth)+','+str(min_heur)+'\n')
      return (min_heur, move)
    elif n.depth<d-1:
      f.write(n.node+','+str(n.depth)+','+'Infinity'+'\n')
      for x in range(len(n.children)):
        v = self.mm_min(n.children[x],d,f)
        if v[0] < min_heur:
          min_heur = v[0]
          move = n.children[x]
        f.write(n.node+','+str(n.depth)+','+str(min_heur)+'\n')
        return (min_heur, move)
    else:
      return    
    
  def abp(self,n,a,d,c,ret):
    if c=='X':
      p='O'
    elif c=='O':
      p='X'
    queue=[]
    queue.append(n)
    while queue:
      e=queue.pop(0)
      if e.depth<int(d) and e.depth%2==0:
        r=self.make_tree(e,a,e.boardstate,c)
        for x in range(len(e.children)):
          queue.append(e.children[x])
      elif e.depth<int(d) and e.depth%2!=0:
        s=self.make_tree(e,a,e.boardstate,p)
        for x in range(len(e.children)):
          queue.append(e.children[x])
    f = open('traverse_log.txt', 'w+')
    f.write('Node,Depth,Value,Alpha,Beta'+'\n')
    v = self.abp_max(n,d,f,-maxsize,maxsize)
    f.close()
    if ret==True:
      return v[1]
    else:
      self.writeToOutputFile(list(v[1].boardstate))

  def abp_max(self,n,d,f,alpha,beta):
    max_heur=-maxsize
    if n.depth==d-1:
      f.write(n.node+','+str(n.depth)+','+'-Infinity'+self.check(alpha)+','+self.check(beta)+'\n')
      for x in range(len(n.children)):
        if n.children[x].heur>max_heur:
          max_heur=n.children[x].heur
          move = n.children[x]
        f.write(n.children[x].node+','+str(n.children[x].depth)+','+str(n.children[x].heur)+self.check(alpha)+','+self.check(beta)+'\n')
        if max_heur >= beta:
          f.write(n.node+','+str(n.depth)+','+str(max_heur)+self.check(alpha)+','+self.check(beta)+'\n')
          return (max_heur, move, alpha, beta)
        if max_heur>alpha:
          alpha=max_heur
        f.write(n.node+','+str(n.depth)+','+str(max_heur)+self.check(alpha)+','+self.check(beta)+'\n')
      return (max_heur, move)
    elif n.depth<d-1:
      f.write(n.node+','+str(n.depth)+','+'-Infinity'+','+self.check(alpha)+','+self.check(beta)+'\n')
      for x in range(len(n.children)):
        v = self.abp_min(n.children[x],d,f,alpha,beta)
        if v[0] > max_heur:
          max_heur = v[0]
          move = n.children[x]
        if max_heur >= beta:
          f.write(n.node+','+str(n.depth)+','+str(max_heur)+','+self.check(alpha)+','+self.check(beta)+'\n')
          return (max_heur, move, alpha, beta)
        if max_heur>alpha:
          alpha=max_heur
        f.write(n.node+','+str(n.depth)+','+str(max_heur)+','+self.check(alpha)+','+self.check(beta)+'\n')
      return (max_heur, move, alpha, beta)
    else:
      return
    

  def abp_min(self,n,d,f,alpha,beta):
    min_heur=maxsize
    if n.depth==d-1:
      f.write(n.node+','+str(n.depth)+','+'Infinity'+','+self.check(alpha)+','+self.check(beta)+'\n')
      for x in range(len(n.children)):        
        if -n.children[x].heur<min_heur:
          min_heur=-n.children[x].heur
          move = n.children[x]
        f.write(n.children[x].node+','+str(n.children[x].depth)+','+str(-n.children[x].heur)+','+self.check(alpha)+','+self.check(beta)+'\n')
        if min_heur<=alpha:
          f.write(n.node+','+str(n.depth)+','+str(min_heur)+','+self.check(alpha)+','+self.check(beta)+'\n')
          return (min_heur, move, alpha, beta)
        if -n.children[x].heur<beta:
          beta=-n.children[x].heur
        f.write(n.node+','+str(n.depth)+','+str(min_heur)+','+self.check(alpha)+','+self.check(beta)+'\n')
      return (min_heur, move, alpha, beta)
    elif n.depth<d-1:
      f.write(n.node+','+str(n.depth)+','+'Infinity'+','+self.check(alpha)+','+self.check(beta)+'\n')
      for x in range(len(n.children)):
        v = self.abp_max(n.children[x],d,f,alpha,beta)
        #print (alpha)
        if v[0] < min_heur:
          min_heur = v[0]
          move = n.children[x]
        if min_heur<=alpha:
          f.write(n.node+','+str(n.depth)+','+str(min_heur)+','+self.check(alpha)+','+self.check(beta)+'\n')
          return (min_heur, move, alpha, beta)
        if min_heur<beta:
          beta=min_heur
        f.write(n.node+','+str(n.depth)+','+str(min_heur)+','+self.check(alpha)+','+self.check(beta)+'\n')
        return (min_heur, move, alpha, beta)
    else:
      return

  def check(self,a):
    if a==maxsize:
      return 'Infinity'
    elif a==-maxsize:
      return '-Infinity'
    else:
      return str(a)

  def calc_heur(self,a,b,c):
    if c=='X':
      p='O'
    elif c=='O':
      p='X'
    h=0
    for i in range(25):
      if b[i]==c:
        h=h+a[i]
      elif b[i]==p:
        h=h-a[i]
    return h

  def writeToOutputFile(self,c):
    #print c
    #return 
    f = open('next_state.txt', 'w+')
    for i in range(0,5):
      x=''
      for j in range(0,5):
        x=x+c[(5*i)+j]
      f.write(x)
      f.write('\n')
    f.close()

  def writeToTraceState(self,c):
    with open("trace_state.txt", "a") as f:
      for i in range(0,5):
        x=''
        for j in range(0,5):
          x=x+c[(5*i)+j]
        f.write(x)
        f.write('\n')
      f.close()

sg=Search_Game()
sg.main()