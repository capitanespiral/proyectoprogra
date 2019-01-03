#!/usr/bin/python
#-*- coding:utf-8 -*-
from clasesfuncs import *
import random as rm
import numpy as np
from time import sleep
n=input("Cuantos cuerpitos? ")
h=input("Largo de intervalo temporal? ")

cuerpitos=[]

for i in range(0,n):
	a=cuerpo([rm.uniform(-10,10),rm.uniform(-10,10)],[rm.uniform(-10,10),rm.uniform(-10,10)],rm.uniform(1e10,2e10))
	cuerpitos.append(a)

pos=np.array(map(lambda x: x.p,cuerpitos))
vel=np.array(map(lambda x: x.v,cuerpitos))
masas=np.array(map(lambda x: x.m,cuerpitos))
print "Las posiciones iniciales son:"
print pos
print
print "Las velocidades iniciales son:"
print vel
print
print "Las masas:"
print masas
print
raw_input("Presiona enter para comenzar")

while True:
	p,v=rk4(pos,vel,h,masas,n)
	cuerpitos=map(lambda w,x,y,z: w.cambios(x,y,z),cuerpitos,p,v,masas)
	print "Posiciones"
	print p
	print
	print "Velocidades"
	print v
	print "##############################################".center(30)
	colisionar=evalua_dists(p,n,cuerpitos)
	pos=p
	vel=v
	sleep(1)

