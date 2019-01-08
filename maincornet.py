#!/usr/bin/python
#-*- coding:utf-8 -*-
from classfuncs import *
import random as rm
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
n=input("Cuantos cuerpitos? ")
h=input("Largo de intervalo temporal? ")
crear=raw_input("Crear sistema o generar random? (Enter, genera random, cualquier otro crear) ")
#Agregar densidad (implica cambiar varias weas de clases
#¿Agregar metodos de string para recibir el par ordenado al touch?

cuerpitos=[]
if crear=="":
	for i in range(n):
		a=cuerpo([rm.uniform(-10,10),rm.uniform(-10,10)],[rm.uniform(-10,10),rm.uniform(-10,10)],rm.uniform(1e10,2e10),rm.uniform(100,7000))
		cuerpitos.append(a)
else:
	i=1
	while i<=n:
		masitas=float(input("Masa cuerpo "+str(i)+": "))
		densidad=float(input("Densidad cuerpo "+str(i)+": "))
		posx=float(input("Pos. inicial X cuerpo "+str(i)+": "))
		posy=float(input("Pos. inicial Y cuerpo "+str(i)+": "))
		velx=float(input("Vel. inicial X cuerpo "+str(i)+": "))
		vely=float(input("Vel. inicial Y cuerpo "+str(i)+": "))
		print
		a=cuerpo([posx,posy],[velx,vely],masitas,densidad)
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
xsol=[]
ysol=[]
xtierra=[]
ytierra=[]
j=0
while j<1825:
	p,v=rk4(pos,vel,h,masas,n)
	cuerpitos=map(lambda w,x,y,z: w.cambios(x,y,z),cuerpitos,p,v,masas)
	print "#################"+"Segundo "+str(i*h)+"#############################"
	print "Posiciones"
	print p
	print
	xsol.append(p[0][0])
	ysol.append(p[0][1])
	xtierra.append(p[1][0])
	ytierra.append(p[1][1])
	print "Velocidades"
	print v
	print
	i+=1
	colisionar=evalua_dists(p,n,cuerpitos)
	pos=p
	vel=v
	j+=1
	#sleep(1)

plt.plot(xsol,ysol, xtierra,ytierra)
plt.show()
