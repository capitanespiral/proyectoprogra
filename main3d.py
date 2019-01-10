#!/usr/bin/python
#-*- coding:utf-8 -*-
from clasesfuncs3d import *
import random as rm
import numpy as np
from time import sleep
crear=raw_input("Crear sistema o generar random? (Enter, genera random, 1 sistemas precreados, otro permite crear) ")
tau=input("Tiempo de paso? ")
#Unidades año, UA y kg
#Agregar densidad (implica cambiar varias weas de clases

tiempo=0.0
cuerpitos=[]
if crear=="":
	n=input("Cuantos cuerpitos? ")
	for i in Range(n):
		a=cuerpo([rm.uniform(-10,10),rm.uniform(-10,10),rm.uniform(-10,10)],[rm.uniform(-10,10),rm.uniform(-10,10),rm.uniform(-10,10)],rm.uniform(1e10,2e10))
		cuerpitos.append(a)
elif crear=="1":
	#Sistemas predefenidos, por ahora solo tierra y sol
	cuerpitos.append(cuerpo([1,0,0],[0,6.27768770053476,0],5.07e24,5515))
	cuerpitos.append(cuerpo([0,0,0],[0,0,0],1.9891e30,1411))
	n=2
	tau=0.01
else:
	n=input("Cuantos cuerpitos? ")
	i=1
	while i<=n:
		masitas=float(input("Masa cuerpo "+str(i)+": "))
		densidad=float(input("Densidad cuerpo "+str(i)+": "))
		pos=raw_input("Pos. inicial cuerpo "+str(i)+": ")
		vel=raw_input("Vel. inicial cuerpo "+str(i)+": ")
		print
		a=cuerpo(map(lambda x: float(x),pos.split(",")),map(lambda x: float(x),vel.split(",")),masitas,densidad)
		cuerpitos.append(a)
		i+=1

pos=np.array(map(lambda x: x.p,cuerpitos))
vel=np.array(map(lambda x: x.v,cuerpitos))
masas=np.array(map(lambda x: x.m,cuerpitos))
densidades=np.array(map(lambda x: x.d,cuerpitos))
print "Las posiciones iniciales son:"
print pos
print
print "Las velocidades iniciales son:"
print vel
print
print "Las masas:"
print masas
print
print "Las densidades:"
print densidades
print
raw_input("Presiona enter para comenzar")

while True:
#Distinta cantidad de elementos en el map parece :O
	p,v,tiempo,tau=rka(pos,vel,tiempo,tau,masas,n)
	print "tau"+str(tau)
	cuerpitos=map(lambda w,x,y,z: w.cambios(x,y,z),cuerpitos,p,v,masas)
	print "#################"+"Año "+str(tiempo)+"#############################"
	print "Posiciones"
	print p
	print
	print "Velocidades"
	print v
	print
	print "Masas"
	print masas
	print
	print "Momentums"
	print np.array(map(lambda x:x.mom,cuerpitos))
	print
	colisionar=evalua_dists(p,n,cuerpitos)
	print "colisiones"
	print colisionar
	cuerpitos=choques(colisionar,cuerpitos)
	pos=np.array(map(lambda x: x.p,cuerpitos))
	print "nuevas posiciones"
	print pos
	vel=np.array(map(lambda x: x.v,cuerpitos))
	print "nuevas velocidades"
	print vel
	masas=np.array(map(lambda x: x.m,cuerpitos))
	print "nuevas masas"
	print masas
	momentum=np.array(map(lambda x: x.mom,cuerpitos))
	print "nuevo momentum"
	print momentum
	n=len(cuerpitos)
	sleep(1)

