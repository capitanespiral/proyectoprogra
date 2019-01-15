#!/usr/bin/python
#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
from clasesfuncs3d import *
import random as rm
import numpy as np
from time import sleep
crear=raw_input("Crear sistema o generar random? (Enter, genera random, 1 ingresa archivo con estado inicial, otro permite crear) ")
colisionesisimas=raw_input("¿Desea colisiones activadas? (Enter no, cualquier otro si) ")
tiempo=0.0
cuerpitos=[]
if crear=="":
	while True:
		try: 
			n=input("Cuantos cuerpitos? ")
			if type(n)==str:
				print "Por favor ingresa un valor numérico\n"
				continue
			break
		except KeyboardInterrupt:
			print
			exit()
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
		except KeyboardInterrupt:
			print
			exit()
		except:
			print "Disculpa, "+str(archivo)+" no existe o hubo un error inesperado al intentar abrirlo\n"
			continue
else:		
	while True:
		try: 
			n=input("Cuantos cuerpitos? ")
			if type(n)==str:
				print "Por favor ingresa un valor numérico\n"
				continue
			break
		except KeyboardInterrupt:
			print
			exit()
		except:
			print "Por favor ingresa un valor numérico\n"
			continue
	i=1
	while i<=n:
		try:
			masitas=float(input("Masa cuerpo "+str(i)+": "))
			#densidad=float(input("Densidad cuerpo "+str(i)+": "))
			pos=raw_input("Pos. inicial cuerpo "+str(i)+": ")
			vel=raw_input("Vel. inicial cuerpo "+str(i)+": ")
			print
			a=cuerpo(map(lambda x: float(x),pos.split(",")),map(lambda x: float(x),vel.split(",")),masitas)
			cuerpitos.append(a)
			i+=1
		except KeyboardInterrupt:
			print
			exit()
		except:
			print "Error inesperado, ingresa de nuevo los datos para ese cuerpo\n"
			continue

while True:	
	try:
		tau=float(input("Tiempo de paso inicial? "))
		pasomaximo=float(input("Tiempo de paso máximo? "))
		tiempototal=raw_input("Tiempo max? (Enter para que sea infinito) ")
		if tiempototal!="":
			tiempototalisimo=float(tiempototal)
		break
	except KeyboardInterrupt:
		print
		exit()
	except:
		print "Por favor ingresa un valor númerico\n"
		continue

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

raw_input("Presione enter para comenzar")
posiciones=[]
velocidades=[]
tiempito=[]

while True:

	try:
		posiciones.append(pos)
		velocidades.append(vel)
		tiempito.append(tiempo)
		pos,vel,tiempo,tau=rka(pos,vel,tiempo,tau,masas,n,pasomaximo)
		print "tau"+str(tau)
		cuerpitos=map(lambda w,x,y,z: w.cambios(x,y,z),cuerpitos,pos,vel,masas)
		print "#################"+"Año "+str(tiempo)+"#############################"
		print "Posiciones"
		print pos
		print
		print "Velocidades"
		print vel
		print
		if colisionesisimas!="":
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
	except KeyboardInterrupt:
		break

e_p=energia_potencial(posiciones,cuerpitos,n)
e_c=energia_cinetica(velocidades,cuerpitos,n)
e_total=e_p+e_c
plt.plot(tiempito,e_c)
plt.plot(tiempito,e_p)
plt.plot(tiempito,e_total)
plt.savefig("energia.png")
plt.show()
plt.clf()

if n==2:
	mom_ang,modpos,modvel=momentoangular(posiciones,velocidades,masas)
	plt.plot(tiempito,mom_ang,c="r")
	plt.plot(tiempito,modpos,c="b")
	plt.plot(tiempito,modvel,c="g")
	plt.savefig("momento_ang.png")
	plt.show()
	plt.clf()

	a,b,c=per_distorb_terc_ley(posiciones,e_c,tiempito,masas)
	plt.hist(c)
	plt.savefig("periodo.png")
	plt.show()

for i in Range(len(posiciones[0])):
	cadacuerpo=[]
	for instante in posiciones:
		cadacuerpo.append(instante[i])
	plt.plot([x[0] for x in cadacuerpo],[x[1] for x in cadacuerpo],".")
plt.axis("equal")
plt.savefig("orbita.png")
plt.show()
plt.clf()


#Unidades año, UA y kg
#Mas sistemas predefinidos, poner titulos y cosas a gráficos, intentar graficar cuando colisionan las cosas, hacer parte gráfica (dah), crear funcion while true con except.
#Sentido dimensional al random, aclarar cosas excluivas para dos cuerpos (programisticamente y en los docs)
#Agregar opciones para pocos planetas (osea, que para pocos hayan muchas y para hartos pocas), desactivar o activar colisiones, tener opcion de colisiones.
#amononar gráficos
#importar bash? en primer rawinput