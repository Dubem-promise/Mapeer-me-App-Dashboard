import random

x = 5
w = 10
y = "Hello, World!"
"""
print ("this is a double line comment")
"""
"""
print(x, y)
print(x + w)
print ("dubem is saying", y )
#this is learning of adding string in the sama line
print("This will work!", end=" ")
print('This will also work!')
#This is learning of adding number and strings together
print("I am", 35, "years old.")
"""

#learning variables
"""
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

print(type(x))
print (z)

# python are also case sesnsitive 

Y = 15
print (y + Y)
"""

#assiging mutliple var and value in same line 
"""
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
"""

# learing upacking

fruits = ["apple", "banana", "cherry", "mango"]
x, y, w, z = fruits
print(x)
print(y)
print(z)

#learnring global function


def myfunc():
  print("Python is " + x)

myfunc()

#Data Types
"""
Text Type:	str
Numeric Types:	int, float, complex
Sequence Types:	list, tuple, range
Mapping Type:	dict
Set Types:	set, frozenset
Boolean Type:	bool
Binary Types:	bytes, bytearray, memoryview
None Type:	NoneType
"""
"""
ky =1j

print(type(ky))

x = "Hello World"	str	
x = 20	int	
x = 20.5	float	
x = 1j	complex	
x = ["apple", "banana", "cherry"]	list	
x = ("apple", "banana", "cherry")	tuple	
x = range(6)	range	
x = {"name" : "John", "age" : 36}	dict	
x = {"apple", "banana", "cherry"}	set	
x = frozenset({"apple", "banana", "cherry"})	frozenset	
x = True	bool	
x = b"Hello"	bytes	
x = bytearray(5)	bytearray	
x = memoryview(bytes(5))	memoryview	
x = None	NoneType	
"""

"""

Example	Data Type
x = str("Hello World")	              str	
x = int(20)	                           int	
x = float(20.5)	                         float	
x = complex(1j)	                            complex	
x = list(("apple", "banana", "cherry"))  	list	
x = tuple(("apple", "banana", "cherry"))	tuple	
x = range(6)	                              range	
x = dict(name="John", age=36)	               dict	
x = set(("apple", "banana", "cherry"))	        set	
x = frozenset(("apple", "banana", "cherry"))	frozenset	
x = bool(5)	                                    bool	
x = bytes(5)	                                bytes	
x = bytearray(5)	                           bytearray	
x = memoryview(bytes(5))	                  memoryview

"""

#Conversion from float, int and complex

rex = 30
rex2 = 30e10
rex3 = 3+4j

print(type(rex3))

#Conversion part
a = int(rex2)

print(type(a))
print (a)

print(random.randrange(1, 1600))

#Global : n_ame

n_ame = "Dubem"
#learning about string and lenght
global p
p = 'Good Morning how are doing'

print(p)

print(p[5])

# trying looping through a string
for x in "King":
  print(x)

print(len(p))

number_letter =  int(len(p))

print(a + number_letter)

print( "Morning" in p)

if "Morning" in p:
  print("it is morning")

if "Morning" not in p:
  print( "its not evening")

#learning string slice  and upper and lower case function
print(p[2:6])
print(p[:5])
print(p[2:])
print(p[-6:-2])
print(p[-2:-1])
print(p.upper())
print(p[:5].upper())
print(p.lower())

#learning modifrying string (white space)

H = " Where are you going, chanel! "
'''
print(H.strip())
print(p, H)
print(p.replace("G", "M"))
print (p.replace("Good", "Best"))
print (p.replace(p, H))
print(p.split(" "))
word1, word2, word3, word4, word5 = p.split(" ")
print(word2)
'''

#learning Concenation in Python
'''
print(p + H)
print(p+H)
print(p+" "+H)
'''
"""
age = 25
print(n_ame, age)
his_age = f"{n_ame} {age}"
print(his_age)
his_age = f"{n_ame} {age:2f}"
print(his_age)

his_age = f"{n_ame}     {age * 5}"
print(his_age)
"""
#Learning escape such as black slashes
print("this me, \"dog\" talking right now")
print("this me, \ndog talking right now")
print("this me, \rdog talking right now")
print("this me, \fdog\f talking right now")
cap = "this me, \fDog talking right now"
"""
print(cap.capitalize())
print(cap.casefold())
print(cap.center(10))
print(cap.encode())
cap_endwith = cap.endswith("right now")
print(cap_endwith)
if True is cap_endwith:
 print("it Gmail")
print(cap.find("now"))
print(cap.translate("dog"))
"""
#"""
#Code	Result	
#\'	Single Quote	
#\\	Backslash	
#\n	New Line	
#\r	Carriage Return	
#\t	Tab	
#\b	Backspace	
#\f	Form Feed	
#\ooo	Octal value	
#\xhh	Hex value
#"""
"""
capitalize()	   Converts the first character to upper case
casefold()	     Converts string into lower case
center()	       Returns a centered string
count()	         Returns the number of times a specified value occurs in a string
encode()	       Returns an encoded version of the string
endswith()	     Returns true if the string ends with the specified value
expandtabs()	   Sets the tab size of the string
find()	         Searches the string for a specified value and returns the position of where it was found
format()	       Formats specified values in a string
format_map()     	Formats specified values in a string
index()	          Searches the string for a specified value and returns the position of where it was found
isalnum()	        Returns True if all characters in the string are alphanumeric
isalpha()	        Returns True if all characters in the string are in the alphabet
isascii()       	Returns True if all characters in the string are ascii characters
isdecimal()     	Returns True if all characters in the string are decimals
isdigit()	       Returns True if all characters in the string are digits
isidentifier()  	Returns True if the string is an identifier
islower()	       Returns True if all characters in the string are lower case
isnumeric()	    Returns True if all characters in the string are numeric
isprintable()  	Returns True if all characters in the string are printable
isspace()	      Returns True if all characters in the string are whitespaces
istitle()     	Returns True if the string follows the rules of a title
isupper()	     Returns True if all characters in the string are upper case
join()	       Joins the elements of an iterable to the end of the string
ljust()	      Returns a left justified version of the string
lower()	      Converts a string into lower case
lstrip()     	Returns a left trim version of the string
maketrans()	  Returns a translation table to be used in translations
partition()  	Returns a tuple where the string is parted into three parts
replace()	   Returns a string where a specified value is replaced with a specified value
rfind()	     Searches the string for a specified value and returns the last position of where it was found
rindex()	   Searches the string for a specified value and returns the last position of where it was found
rjust()	     Returns a right justified version of the string
rpartition()	Returns a tuple where the string is parted into three parts
rsplit()	Splits the string at the specified separator, and returns a list
rstrip()	Returns a right trim version of the string
split()	   Splits the string at the specified separator, and returns a list
splitlines()	Splits the string at line breaks and returns a list
startswith()	Returns true if the string starts with the specified value
strip()	     Returns a trimmed version of the string
swapcase()	Swaps cases, lower case becomes upper case and vice versa
title()	    Converts the first character of each word to upper case
translate()	Returns a translated string
upper()	    Converts a string into upper case
zfill()	   Fills the string with a specified number of 0 values at the beginning

"""

#Learning about booleans 

print(30>=10)
print(2<=10)
print(10<=2)
x = random.randrange(1, 200)
y = random.randrange(1, 200)

a = x
b = y
if b > a:
  print("the temperature is high")
else:
  print(" the temperature is low")
print( a, b)

print(bool({}))
print(bool(b))

def myDubemfunc() :

  return False

print(myDubemfunc())

if myDubemfunc() is False:
  print("YES!")
else:
  print("NO!")

print(isinstance(a, int))
print(isinstance(myDubemfunc(), bool))

#LEARNING ABOUT OPERATORS 
x = 15
y = 4
'''
print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y) 
print(x ** y) # this raise to power
print(x // y) #division without float
'''
x += 3
#y &= 3
b |= 3
x ^= 3
print(x)
print (y)
print(b)
print(x)
print(y)
print(-6^3)
print(x>>y)

#learning about Wlrus assignmant opperators

numbers = ['bags', 'shoe', 'cap', 'pusre', 'car','moto']

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")

if poke := x:
  print( "it is me")

#learning about camparison operators

print(1 < y < 10)

print(1 < x and y > 10)
print (1 > y or y < 10)
print(not(1 < x and x < 10))

things = ['bags', 'shoe', 'cap', 'pusre', 'car','moto']
#numbers = things
print(things is numbers)
print(things == numbers)
print( things is not numbers)

#learning Precedence in Python
print((3+4)*5/(2+4))

#learning about List
MyCars = [ "Volvo", "toyota", "lexus", "kia", "honda", "Honda", "benz", "toyota", 10 , False]

print(MyCars)
print(type(MyCars))
print(len(MyCars))
print( False is MyCars)
print(isinstance(MyCars, list))
p = str (MyCars)
print(p)
thislist = list(("apple", "banana", "cherry")) # note the double round-brackets
print(thislist)
print(type(p))

print("volvo" in MyCars)
print(MyCars[4])
print(MyCars[-1])
print(MyCars[2:7])
print(cap[-2])
print(MyCars[:5])
print(MyCars[-4:-2])
MyCars[3] = "Ford"
MyCars[2:4] = ["Vbut", "Lambo", "lorry", "jeep", "carabo" ]
MyCars[2] = ['tires', "wheel", "steering"]

print(MyCars)

#how to insert, extend, append, and remove in a list
MyCars.insert(3, "venza")
MyCars.append("volkswagen")
MyCars.extend(thislist)
print(p)
#print(MyCars)
p = list(p)
#MyCars.extend(p)
print(MyCars)
print(len(p))

#You can add tuple to list using extend too

thisTuple = ("parlor", "room", "passage")
print(type(thisTuple))
MyCars.extend(thisTuple)
print(MyCars)
print(type(MyCars))
#MyCars.remove('o')
print(MyCars)
#del MyCars[4:8]\
MyCars.pop(2)
#MyCars.clear()
MyCars.extend(thisTuple)
MyCars = [ x for x in MyCars if x not in ("y","o", "t", "a", "'", "1", "0" )]

#learning about loop FOR and WHILE
for x in range(len(MyCars)):
  print(MyCars[x])
for x in range(len(MyCars)):
  print(MyCars[x])
for x in MyCars:
 print(x)

utnsil = ['pot', 'spoon', 'plate']

#for x in utnsil:
#  print(x)

i = 0
while i < len(MyCars):
  print(MyCars[i])
  i += 1
#list comprehension

print(type(MyCars))

#add_list = []

#for x in utnsil:
 # if "a" in x:
  # add_list.append(x)
#print(add_list)

add_list = [x for x in utnsil if "o" in x]
print(add_list)
fruit = [x for x in thislist if "c" in x]
fruitz = [x for x in thislist if "apple" != x]
carz = [ x for x in  MyCars if x not in ("honda", "apple", "room", "Passage")]
print(carz)
print(fruitz)
print(fruit)
print(MyCars)
#boy = [x for x in range(20)]
boy = [x for x in range(20) if (x *2) <= 5]
boyz = [ x for x in MyCars if x in ["honda", "carabo"]]
#boyCar =["baby boy" for x in  MyCars]
#boyCar = [x.upper() if x == "honda" else "carabo" for x in MyCars ]
boyCar = [x.upper() for x in MyCars if x == "honda"]
for x in range(len(boyCar)):
  print(x)
print(boyCar)
print(boy)
print (boyz)
print(range(20))

#Converting list items from str to int and also Sorting them
MyCars = [ str(x) for x in MyCars]
MyCars.sort(key= str.lower), MyCars.reverse()
#MyCars.sort(key= str.upper)
print(MyCars)
#MyCars.sort(reverse= True)
#MyCars.reverse()
print(MyCars)
Py = MyCars.index('False')
print(Py)
#for /r %i in (__pycache__) do @rd/s/q "%i" del /s/q *.pyc

# Copying of List item

uber_MyCars = MyCars.copy()
indriveCars = MyCars[:]
JanrideCars = list(MyCars)

uber_MyCars.remove('False'), uber_MyCars.append("corrola")

#checking if I modify the list
if ['False'] in uber_MyCars:
  print("No I have not remove it")
else:
 print( "Yes I have remove it")

if MyCars == indriveCars and JanrideCars:
  print ( "They copied right")
else:
  print("the copy is not correct")
print (uber_MyCars)

#Adding list together
many_cars = MyCars + indriveCars

for x in MyCars:
  indriveCars.append(x)
print(indriveCars)

MyCars= MyCars + uber_MyCars
if many_cars == indriveCars and  MyCars:
  print('its the same')
else:
  print('they are not')
"""
#List Methods
append()	Adds an element at the end of the list
clear()	Removes all the elements from the list
copy()	Returns a copy of the list
count()	Returns the number of elements with the specified value
extend()	Add the elements of a list (or any iterable), to the end of the current list
index()	Returns the index of the first element with the specified value
insert()	Adds an element at the specified position
pop()	Removes the element at the specified position
remove()	Removes the item with the specified value
reverse()	Reverses the order of the list
sort()	Sorts the list

"""

#Learning About Tuple 

MyCa = ( "benz", "bettle", "Vbut")
print(type(MyCa))
print(type(MyCars))

for x in MyCa:
  print(x)
