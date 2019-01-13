#!/usr/bin/python
#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
from clasesfuncs3d import *
import random as rm
import numpy as np
from time import sleep
crear=raw_input("Crear sistema o generar random? (Enter, genera random, 1 ingresa archivo con estado inicial, otro permite crear) ")
#annos=float(input("Cuantos años? "))
#Unidades año, UA y kg
#Agregar densidad (implica cambiar varias weas de clases

tiempo=0.0
cuerpitos=[]
if crear=="":
	while True:
		try: 
			n=input("Cuantos cuerpitos? ")
			break
		except:
			print "Por favor ingresa un valor numérico\n"
			continue
	for i in Range(n):
		a=cuerpo([rm.uniform(-1,1),rm.uniform(-1,1),rm.uniform(-1,1)],[rm.uniform(-10,10),rm.uniform(-10,10),rm.uniform(-10,10)],rm.uniform(1e10,2e10))
		cuerpitos.append(a)
elif crear=="1":
	while True:
		try:
			archivo=raw_input("¿Nombre de archivo con estado inicial? ")
			est_inicial=open(archivo,"r")
			info=[line.split() for line in est_inicial.readlines()]
			est_inicial.close()
			for lista in info:
				posicion=[]
				velocidad=[]
				for i,elemento in enumerate(lista):
					if i==0:
						masa=float(elemento)
					elif 1<=i<=3:
						posicion.append(float(elemento))
					else:
						velocidad.append(float(elemento))
				cuerpitos.append(cuerpo(posicion,velocidad,masa))
			n=len(cuerpitos)
			break
		except IOError:
			print "Disculpa, "+str(archivo)+" no existe o hubo un error inesperado al intentar abrirlo\n"
			continue
else:		
	while True:
		try: 
			n=input("Cuantos cuerpitos? ")
			break
		except:
			print "Por favor ingresa un valor numérico\n"
			continue
	i=1
	while i<=n:
		masitas=float(input("Masa cuerpo "+str(i)+": "))
		#densidad=float(input("Densidad cuerpo "+str(i)+": "))
		pos=raw_input("Pos. inicial cuerpo "+str(i)+": ")
		vel=raw_input("Vel. inicial cuerpo "+str(i)+": ")
		print
		a=cuerpo(map(lambda x: float(x),pos.split(",")),map(lambda x: float(x),vel.split(",")),masitas)
		cuerpitos.append(a)
		i+=1

while True:	
	try:
		tau=float(input("Tiempo de paso inicial? "))
		pasomaximo=float(input("Tiempo de paso máximo? "))
		tiempototal=raw_input("Tiempo max? (Enter para que sea infinito) ")
		if tiempototal!="":
			tiempototalisimo=float(tiempototal)
		break
	except:
		print "Por favor ingresa un valor númerico\n"
		continue

pos=np.array(map(lambda x: x.p,cuerpitos))
vel=np.array(map(lambda x: x.v,cuerpitos))
masas=np.array(map(lambda x: x.m,cuerpitos))
#densidades=np.array(map(lambda x: x.d,cuerpitos))
print "Las posiciones iniciales son:"
print pos
print
print "Las velocidades iniciales son:"
print vel
print
print "Las masas:"
print masas
print
#print "Las densidades:"
#print densidades
#print

raw_input("Presione enter para comenzar")
posiciones=[]
ecinetica=[]
epotencial=[]
etotal=[]
tiempito=[]
#while annos>tiempo:
while True:
#Distinta cantidad de elementos en el map parece :O
	try:
		pos,vel,tiempo,tau=rka(pos,vel,tiempo,tau,masas,n,pasomaximo)
		posiciones.append(pos)
		print "tau"+str(tau)
		#Genera error cuando solo queda un cuerpo
		cuerpitos=map(lambda w,x,y,z: w.cambios(x,y,z),cuerpitos,pos,vel,masas)
		print "#################"+"Año "+str(tiempo)+"#############################"
		print "Posiciones"
		print pos
		print
		print "Velocidades"
		print vel
		print
		cinetica=energia_cinetica(vel,cuerpitos,n)
		potencial=energia_potencial(pos,cuerpitos,n)
		total=cinetica+potencial
		ecinetica.append(cinetica)
		epotencial.append(potencial)
		etotal.append(total)
		tiempito.append(tiempo)
		print "Energias"
		print cinetica
		print potencial
		print total
		colisionar=evalua_dists(pos,n,cuerpitos)
		print "colisiones"
		print colisionar
		cuerpitos=choques(colisionar,cuerpitos)
		if n!=len(cuerpitos):
			masas=np.array(map(lambda x: x.m,cuerpitos))
			momentum=np.array(map(lambda x: x.mom,cuerpitos))
			pos=np.array(map(lambda x: x.p,cuerpitos))
			vel=np.array(map(lambda x: x.v,cuerpitos))
			n=len(cuerpitos)
		if tiempototal!="":
			if tiempototalisimo<tiempo:
				break
		#sleep(1)
	except KeyboardInterrupt:
		break
plt.plot(tiempito,ecinetica)
plt.plot(tiempito,epotencial)
plt.plot(tiempito,etotal)
plt.savefig("energia.png")
plt.show()
plt.clf()


for i in Range(len(posiciones[0])):
	cadacuerpo=[]
	for instante in posiciones:
		cadacuerpo.append(instante[i])
	plt.plot([x[0] for x in cadacuerpo],[x[1] for x in cadacuerpo])
plt.axis("equal")
plt.savefig("orbita.png")
plt.show()




