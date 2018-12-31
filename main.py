#!/usr/bin/python
#-*- coding:utf-8 -*-
from clasesfuncs import *
import random as rm
import numpy as np
from time import sleep
n=input("Cuantos cuerpitos? ")
cuerpitos=[]
p0=[]
v0=[]
m=[]

for i in range(0,n):
	a=cuerpo([rm.uniform(-10,10),rm.uniform(-10,10)],[rm.uniform(-10,10),rm.uniform(-10,10)],rm.uniform(1e10,2e10))
	cuerpitos.append(a)
	p0.append(a.p)
	v0.append(a.v)
	m.append(a.m)
p0=np.array(p0)
v0=np.array(v0)
m=np.array(m)

print "Las posiciones iniciales son:"
print p0
print
print "Las velocidades iniciales son:"
print v0
print
print "Las masas:"
print m
print
raw_input("Presiona enter para comenzar")

while True:
	a,b=rk(p0,v0,tf,ti,m,n)
	print "Posiciones"
	print a
	print
	print "Velocidades"
	print b
	print
	p0=a
	v0=b
	sleep(1)
