#!/usr/bin/python
#-*- coding:utf-8 -*-
from clasesfuncs3d import *
import random as rm
import numpy as np
from time import sleep
n=input("Cuantos cuerpitos? ")
h=input("Largo de intervalo temporal? ")
crear=raw_input("Crear sistema o generar random? (Enter, genera random, cualquier otro crear) ")
#Agregar densidad (implica cambiar varias weas de clases
#¿Agregar metodos de string para recibir el par ordenado al touch?

cuerpitos=[]
if crear=="":
	for i in range(n):
		a=cuerpo([rm.uniform(-10,10),rm.uniform(-10,10),rm.uniform(-10,10)],[rm.uniform(-10,10),rm.uniform(-10,10),rm.uniform(-10,10)],rm.uniform(1e10,2e10))
		cuerpitos.append(a)
else:
	i=1
	while i<=n:
		masitas=float(input("Masa cuerpo "+str(i)+": "))
		densidad=float(input("Densidad cuerpo "+str(i)+": "))
		posx=float(input("Pos. inicial X cuerpo "+str(i)+": "))
		posy=float(input("Pos. inicial Y cuerpo "+str(i)+": "))
		posz=float(input("Pos. inicial Z cuerpo "+str(i)+": "))
		velx=float(input("Vel. inicial X cuerpo "+str(i)+": "))
		vely=float(input("Vel. inicial Y cuerpo "+str(i)+": "))
		velz=float(input("Vel. inicial Z cuerpo "+str(i)+": "))
		print
		a=cuerpo([posx,posy,posz],[velx,vely,velz],masitas,densidad)
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
i=1
while True:
#Distinta cantidad de elementos en el map parece :O
	p,v=rk4(pos,vel,h,masas,n)
	cuerpitos=map(lambda w,x,y,z: w.cambios(x,y,z),cuerpitos,p,v,masas)
	print "#################"+"Segundo "+str(i*h)+"#############################"
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
	print colisionar
	cuerpitos=choques(colisionar,cuerpitos)
	pos=np.array(map(lambda x: x.p,cuerpitos))
	print pos
	vel=np.array(map(lambda x: x.v,cuerpitos))
	print vel
	masas=np.array(map(lambda x: x.m,cuerpitos))
	print masas
	momentum=np.array(map(lambda x: x.mom,cuerpitos))
	print momentum
	n=len(cuerpitos)
	i+=1
	sleep(1)

