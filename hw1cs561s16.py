def main():
  a=[]
  fr=open('input.txt','r')
  for lines in fr:
    line=lines.rstrip('\n')
    a.append(line)
  fr.close()
  b=[]
  for i in range(3,8):
    b.extend(a[i].split())      
  c=[]
  for i in range(8,13):
    for j in range(5):
      c.extend(a[i][j])
  if a[0]=='1':
    writeToOutputFile(gbfs(b,c,a[1]))
  elif a[0]=='2':
    mm(b,c)
  elif a[0]=='3':
    abp(b,c)
  else:
    return

def gbfs(a,b,c):
  a=map(int,a)
  d=[1]*25
  if c=='X':
    p='O'
  elif c=='O':
    p='X'
  m=min(a)
  j=[]
  for i in range(len(b)):
    if b[i]==c:
#check top
      if b[i-5]!=c and b[i-5]!=p and i>4:
#       print str(i-5)+' top'
        if (i-10)>-1 and b[i-10]==p and ((a[i-10]+a[i-5])>m):
          m=a[i-10]+a[i-5]
          del j[:]
          j.append(i-10)
          j.append(i-5)
          d[i-10]=0
          d[i-5]=0
# 	  print 'top top '+b[i-10]+' '+str(i-10)
        if (i-6)>-1 and b[i-6]==p and ((a[i-6]+a[i-5])>m):
          m=a[i-6]+a[i-5]
          del j[:]
          j.append(i-6)
          j.append(i-5)
          d[i-6]=0
          d[i-5]=0
# 	  print 'top left '+b[i-6]+' '+str(i-6)
        if b[i-4]==p and ((a[i-4]+a[i-5])>m):
          m=a[i-4]+a[i-5]
          del j[:]
          j.append(i-4)
          j.append(i-5)
          d[i-4]=0
          d[i-5]=0
# 	  print 'top right '+b[i-4]+' '+str(i-4)
        if a[i-5]>m:
          m=a[i-5]
          del j[:]
          j.append(i-5)
          d[i-5]=0
#         print a[i-5]
#       print m

#check bottom
      if b[i+5]!=c and b[i+5]!=p and i<20:
#       print str(i+5)+' bottom'
        if (i+10)<25 and b[i+10]==p and ((a[i+10]+a[i+5])>m):
          m=a[i+10]+a[i+5]
          del j[:]
          j.append(i+10)
          j.append(i+5)
          d[i+10]=0
          d[i+5]=0
# 	  print 'bottom bottom '+b[i+10]+' '+str(i+10)
        if (i+6)<25 and b[i+6]==p and ((a[i+6]+a[i+5])>m):
          m=a[i+6]+a[i+5]
          del j[:]
          j.append(i+6)
          j.append(i+5)
          d[i+6]=0
          d[i+5]=0
# 	  print 'bottom right '+b[i+6]+' '+str(i+6)
        if b[i+4]==p and ((a[i+4]+a[i+5])>m):
          m=a[i+4]+a[i+5]
          del j[:]
          j.append(i+4)
          j.append(i+5)
          d[i+4]=0
          d[i+5]=0
# 	  print 'bottom left '+b[i+4]+' '+str(i+4)
        if a[i+5]>m:
          m=a[i+5]
          del j[:]
          j.append(i+5)
          d[i+5]=0
#        print m

#check left
      if b[i-1]!=c and b[i-1]!=p and (i%5)!=0:
#        print str(i-1)+' left'
#        print m
        if (i-1)%5!=0 and b[i-2]==p and ((a[i-1]+a[i-2])>m):
          m=a[i-1]+a[i-2]
          del j[:]
          j.append(i-1)
          j.append(i-2)
          d[i-1]=0
          d[i-2]=0
# 	  print 'left left '+b[i-2]+' '+str(i-2)
        if (i-6)>-1 and b[i-6]==p and ((a[i-1]+a[i-6])>m):
          m=a[i-1]+a[i-6]
          del j[:]
          j.append(i-1)
          j.append(i-6)
          d[i-1]=0
          d[i-6]=0
# 	  print 'left top '+b[i-6]+' '+str(i-6)
        if (i+4)<25 and b[i+4]==p and ((a[i-1]+a[i+4])>m):
          m=a[i-1]+a[i+4]
          del j[:]
          j.append(i-1)
          j.append(i+4)
          d[i-1]=0
          d[i+4]=0
# 	  print 'left bottom '+b[i+4]+' '+str(i+4)
        if a[i-1]>m:
          m=a[i-1]
          del j[:]
          j.append(i-1)
          d[i-1]=0
#        print m

#check right
      if b[i+1]!=c and b[i+1]!=p and ((i+1)%5)!=0:
#        print str(i+1)+' right'
        if (i+2)%5!=0 and b[i+2]==p and ((a[i+1]+a[i+2])>m):
          m=a[i+1]+a[i+2]
          del j[:]
          j.append(i+1)
          j.append(i+2)
          d[i+1]=0
          d[i+2]=0
# 	  print 'right right '+b[i+2]+' '+str(i+2)
        if (i-4)>-1 and b[i-4]==p and ((a[i+1]+a[i-4])>m):
          m=a[i+1]+a[i-4]
          del j[:]
          j.append(i+1)
          j.append(i-4)
          d[i+1]=0
          d[i-4]=0
# 	  print 'right top '+b[i-4]+' '+str(i-4)
        if (i+6)<25 and b[i+6]==p and ((a[i+1]+a[i+6])>m):
          m=a[i+1]+a[i+6]
          del j[:]
          j.append(i+1)
          j.append(i+6)
          d[i+1]=0
          d[i+6]=0
# 	  print 'right bottom '+b[i+6]+' '+str(i+6)
        if a[i+1]>m:
          m=a[i+1]
          del j[:]
          j.append(i+1)
          d[i+1]=0
      
#      print (str(i)+'-'+str(a[i]))
#  print m
#  print j
#  print a
  n=min(a)
  for i in range(25):
    if d[i]==1 and b[i]!=c and b[i]!=p and a[i]>m:
      del j[:]
      j.append(i)
  for i in j:
    b[i]=c
#  print b
  return b

def mm(a,b):
  print('mm')

def abp(a,b):
  print ('abp')

def writeToOutputFile(c):
  f = open('output.txt', 'r+')  
  for i in range(0,5):
    x=''
    for j in range(0,5):
      x=x+c[(5*i)+j]
    f.write(x)
    f.write('\n')

if __name__ == '__main__':
  main()
