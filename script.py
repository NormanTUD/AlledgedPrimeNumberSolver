from math import *
from time import perf_counter
from decimal import *
getcontext().prec = 192
import sys

#could use a segment to determine bitlength or
#otherwise let user set bitlength themselves.
n = 0
m = 0 
c = 0
a = 0
b = 0
factorRange = 0

pStr = (input("product: ")).replace(",", "")
try:
  p = Decimal(pStr)
except Exception:
  print("no product given. Exiting!")
  exit()


print("[RECOMMENDED] entering -1 in any field indicates you want qsolver to attempt to guesttimate that value")
print("(use -2 for n if you want it to estimate Q first)")
nStr = input("n: ")
print("(use -2 for m if you want to set m to cutoff)")
mStr = input("m: ")
cStr = input("cutoff: ")
try:
  n = Decimal(nStr)
  m = Decimal(mStr)
  c = Decimal(cStr)
except Exception:
  print("error - invalid number or format. Setting n and m, and cutoff to 0")
  n = Decimal('0.0')
  m = Decimal('0.0')
  c = Decimal('0.0')


checkPseudo = input("estimate pseudofactors? y|n (or press enter to skip): ")
try:
  if str.lower(checkPseudo) == "y":
    getLower = True
  else:
    getLower = False
except Exception:
  print("skipping pseudo factor checking")
  getLower = False

if getLower:
  a = (input("factor a: ")).replace(",", "")
  b = (input("factor b: ")).replace(",", "")
  factorRange = input("factor range: ")
  try:
    a = Decimal(a)
    b = Decimal(b)
    factorRange = Decimal(factorRange)
  except Exception:
    print("error - invalud numbers or format. Skipping pseudo factor check.")



#returns the unit digit and mantissa of n
def sublimate(n):
  _n = str(Decimal(n))
  i = 0
  #then loop until we hit a period
  while i < len(_n):
    if _n[i] == '.':
      break
    i = i + 1
  
  i = i - 1 #back off to the unit digit
  
  if _n[len(_n)-1] == ".":
    #if the last digit in the string is a period it's because it's a whole number
    #so return the digit before it
    return Decimal(_n[len(_n)-2])
  else:
    #otherwise, return up to the last, fractional digit, in the mantissa
    return Decimal(_n[i:len(_n)])





#find pseudo factor
def findPseudo(x, y, range):
  #print("searching for pseudo factor..")
  if abs(x-y) <= range:
    print("FOUND pseudo factor! x-y: " + str(abs(x-y)))
    return x
  else:
    return None 


#attempts to find a suitable N before solving with n and m
def findN(p):
  w = p.sqrt()
  g = w**(1/p.ln())
  Q = w**g
  q = Q/w
  v = w/q
  n = v-sublimate(w)
  return n


#solves for n and m given Q
def solveQ(p, N = 0, M = 0, C = 0, a = 0, b = 0, fRange = 0):
  n = 0
  m = 0
  cutoff = 0
  w = p.sqrt()

  if N == -1:
    #n = floor(log(p**2))
    n = Decimal(floor(log(p*w)))
  if N == -2:
    n = Decimal(floor(findN(p)))-1
  else:
    n = N

  if M == -1:
    m = Decimal(floor(p.ln() ** Decimal(e)))
  elif M== -2:
    m = Decimal(ceil(Decimal(ceil(Decimal(p.ln())*w)).sqrt())) #uses cutoff method
  else:
    m = M

  if C < 1:
    cutoff = Decimal(ceil(Decimal(ceil(Decimal(log(p))*w)).sqrt()))
  else:
    cutoff = C

  print("n: " + str(n))
  print("m: "+ str(m))
  print("c: " + str(cutoff))
  print("a: " + str(a) + ",  b: " + str(b) + ",  range: " + str(fRange))
  
  i=0
  t=0
  while n < cutoff:
    Q = ((w/(Decimal(sublimate(w))+n))*w)
    q = (w/Decimal((sublimate(w))+n))
    #m = Decimal(floor(p.ln() ** Decimal(e)))
    m = 0
    total = 0
    #while m > (total):
    while m < cutoff:
      r = Q/(q-m)
      #print("r: " + str(r))
      if a > 0:
        f = findPseudo(Decimal(abs(r)), a, fRange)
        if f != None:
          print("pseudo factor f: " + str(f)[:32] + ", t: " + str(t) + ",  n: " + str(n) + ",  m: " + str(m))
          return f
      elif b > 0:
        f = findPseudo(Decimal(abs(r)), b, fRange)
        if f != None:
          print("pseudo factor f: " + str(f)[:32] + ", t: " + str(t) + ",  n: " + str(n) + ",  m: " + str(m))
          return f


      #n2 = floor(w/q)
      r2 = r
      r2ceil = Decimal(ceil(r2))
      r2floor = Decimal(floor(r2))
      r2ceilAdd = Decimal(r2ceil+1)
      r2ceilSub = Decimal(r2ceil-1)
      r2floorAdd = Decimal(r2floor+1)
      r2floorSub = Decimal(r2floor-1)
      f = 0
      while f < 2:
        #in-range checks. Basically see if we're close at any point
        if (p/r2ceil)%1 == 0:
          print("\n[SEQ] FOUND FACTOR! = " + str(r2ceil))
          print("r2CEIL, n: " + str(n) + ",  m: " + str(m) + ",  t: " + str(t))
          print("-m") if f<1 else print("+m")
          print("cutoff: " + str(cutoff))
          return abs(r2ceil)
        if (p/r2floor)%1 == 0:
          print("\n[SEQ] FOUND FACTOR! = " + str(r2floor))
          print("r2FLOOR, n: " + str(n) + ",  m: " + str(m) + ",  t: " + str(t))
          print("-m") if f<1 else print("+m")
          print("cutoff: " + str(cutoff))
          return abs(r2floor)
        if (p/r2ceilAdd)%1 == 0:
          print("\n[SEQ] FOUND FACTOR! = " + str(r2ceilAdd))
          print("r2CEILADD, n: " + str(n) + ",  m: " + str(m) + ",  t: " + str(t))
          print("-m") if f<1 else print("+m")
          print("cutoff: " + str(cutoff))
          return abs(r2ceilAdd)
        if (p/r2ceilSub)%1 == 0:
          print("\n[SEQ] FOUND FACTOR! = " + str(r2ceilSub))
          print("r2CEILSUB, n: " + str(n) + ",  m: " + str(m) + ",  t: " + str(t))
          print("-m") if f<1 else print("+m")
          print("cutoff: " + str(cutoff))
          return abs(r2ceilSub)
        if (p/r2floorAdd)%1 == 0:
          print("\n[SEQ] FOUND FACTOR! = " + str(r2floorAdd))
          print("r2FLOORADD, n: " + str(n) + ",  m: " + str(m) + ",  t: " + str(t))
          print("-m") if f<1 else print("+m")
          print("cutoff: " + str(cutoff))
          return abs(r2floorAdd)
        if (p/r2floorSub)%1 == 0:
          print("\n[SEQ] FOUND FACTOR! = " + str(r2floorSub))
          print("r2FLOORSUB, n: " + str(n) + ",  m: " + str(m) + ",  t: " + str(t))
          print("-m") if f<1 else print("+m")
          print("cutoff: " + str(cutoff))
          return abs(r2floorSub)
        
        #same thing but with +m now instead of -m
        r = Q/(q+m)
        r2 = r
        r2ceil = Decimal(ceil(r2))
        r2floor = Decimal(floor(r2))
        r2ceilAdd = Decimal(r2ceil+1)
        r2ceilSub = Decimal(r2ceil-1)
        r2floorAdd = Decimal(r2floor+1)
        r2floorSub = Decimal(r2floor-1)
        f = f + 1
        #if r2ceil < 2 or r2floor < 2 or r2ceilAdd < 2 or r2ceilSub < 2 or r2floorAdd < 2 or r2floorSub < 2:
        #  break
        #print("r: " + str(r))
      
      if i >= 10000:
        sys.stdout.write(".")
        sys.stdout.flush()
        i=0
    
      i=i+1
    
    
      #print("r: " + str(r))
      if r <= 0:
        break
      
      if r != 1 and r != 0 and r != p and (p/r)%1 == 0: #and p/(p/r)%1 == 0:
        print("\nFOUND factor: " + str(r))
        print("n: " + str(n) + ",  m: " + str(m) + ",  t: " + str(t))
        print("-m") if f<1 else print("+m")
        print("cutoff: " + str(cutoff))
        return r
      
      
      
      #m = m - 1
      m = m + 1
      t = t + 1
    
    n = n + 1
    t = t + 1
  
  print("NO FACTOR FOUND! (or an exception happened)")
  print("cutoff: " + str(cutoff))
  return -1 #no such value was found


f = -1
_ = input("press ENTER to begin search.")
startTime = perf_counter()
f = solveQ(p, n, m, c, a, b, factorRange)

print("time: " + str(perf_counter() - startTime) + "s\n")

print("NOTE - if the solver fails to find a factor, try increasing the cutoff first.")
