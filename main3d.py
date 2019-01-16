#!/usr/bin/python
#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from clasesfuncs3d import *
import random as rm
import numpy as np
import os
crear=raw_input("Crear sistema o generar random? (Enter, genera random, 1 ingresa archivo con estado inicial, otro permite crear) ")
colisionesisimas=raw_input("¿Desea colisiones activadas? (Enter no, cualquier otro si) ")
guardar=raw_input("¿Deseas guardar los gráficos generados? (Enter no, cualquier otro si) ")
tiempo=0.0
cuerpitos=[]
if crear=="":
	while True:
		try: 
			n_original=input("Cuantos cuerpitos? ")
			if type(n_original)==str:
				print "Por favor ingresa un valor numérico\n"
				continue
			break
		except KeyboardInterrupt:
			print
			exit()
		except:
			print "Por favor ingresa un valor numérico\n"
			continue
	for i in Range(n_original):
		a=cuerpo([rm.uniform(-1,1),rm.uniform(-1,1),rm.uniform(-1,1)],[rm.uniform(-6,6),rm.uniform(-6,6),rm.uniform(-6,6)],rm.uniform(1e20,2e30))
		cuerpitos.append(a)
elif crear=="1":
	while True:
		try:
			archivo=raw_input("¿Nombre de archivo con estado inicial? ")
			est_inicial=open(archivo,"r")
			info=[line.split() for line in est_inicial.readlines()]
			est_inicial.close()
			nombres=[]
			h=0
			for lista in info:
				posicion=[]
				velocidad=[]
				for i,elemento in enumerate(lista):
					if i==0:
						masa=float(elemento)
					elif 1<=i<=3:
						posicion.append(float(elemento))
					elif 4<=i<=6:
						velocidad.append(float(elemento))
				if len(lista)==8:
					nombres.append(lista[7])
				else:
					nombres.append(0)
				cuerpitos.append(cuerpo(posicion,velocidad,masa,nombre=nombres[h]))
				h+=1
			n_original=len(cuerpitos)
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
			n_original=input("Cuantos cuerpitos? ")
			if type(n_original)==str:
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
	while i<=n_original:
		try:
			masitas=float(input("Masa cuerpo "+str(i)+": "))
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
n=n_original
cuerpitos.sort(cmp=comparamasas,reverse=True)
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

if guardar!="":
	k=0
	while True:
		carpeta="Simulacion"+str(k)
		if not os.path.exists(carpeta):
			os.mkdir(carpeta)
			break
		k+=1

# se crean los ejes en tres dimensiones 	
fig = plt.figure()	
ax = p3.Axes3D(fig)	
#define los colores	
colores = plt.cm.jet(np.linspace(0, 1, n))	

#punto de vista inicial	
ax.view_init(10, 0)	

# crea un arreglo con las posiciones de todos los cuerpos, es usado en la animación	
data = []	
for i in range(n):	
	a=[x[i] for x in posiciones]	
	xs=[x[0] for x in a]	
	ys=[y[1] for y in a]	
	zs=[z[2] for z in a]	
	p=np.array([xs,ys,zs])	
	data.append(p)	

#
radios=[x.R*((-1.5*distmax(posiciones)+52.5)/0.007976817937469764) for x in cuerpitos]	


# Creating fifty line objects.	
# NOTE: Can't pass empty arrays into 3d version of plot()	
#lineas y puntos	
#definir valores por defecto para weas aleatorias	
lineas = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1], "-",c=c, markersize=0.01)[0] for dat,c in zip(data,colores)]	
pts = sum([ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1], 'o', c=c, markersize=r)for dat,c,r in zip(data, colores, radios)],[])	

# Setting the axes properties	

ax.set_xlim3d([-distmax(posiciones), distmax(posiciones)])	
ax.set_xlabel('X')	

ax.set_ylim3d([-distmax(posiciones), distmax(posiciones)])	
ax.set_ylabel('Y')	

ax.set_zlim3d([-distmax(posiciones), distmax(posiciones)])	
ax.set_zlabel('Z')	

ax.set_title('Prueba 3D')	

# Creating the Animation object	
ani = animation.FuncAnimation(fig, update, len(data[0][0]), fargs=(data, lineas, pts),interval=200)	
plt.show()

e_p=energia_potencial(posiciones,cuerpitos,n)
e_c=energia_cinetica(velocidades,cuerpitos,n)
e_total=e_p+e_c
plt.title("Energia cinetica, potencial y total del Sistema")
plt.xlabel("Tiempo")
plt.ylabel("Energia")
plt.plot(tiempito,e_c,"b",tiempito,e_p,"g",tiempito,e_total,"r")
plt.legend(("Cinetica","Potencial","Total"))
if guardar!="":
	plt.savefig(carpeta+"/energiatotal.png")
plt.show()
plt.clf()

if n==n_original:
	mom_ang,modpos,modvel=momentoangular(posiciones,velocidades,masas)
	r=1
	for i,j,k in zip(mom_ang,modpos,modvel):
		plt.xlabel("Tiempo")
		plt.plot(tiempito,i,"r",tiempito,j,"b",tiempito,k,"g")
		plt.legend(("Momento angular","Modulo de posicion","Modulo de velocidad"))
		if cuerpitos[r].nombre!="0":
			plt.title("Momento angular, posiciones y velocidad - "+cuerpitos[r].nombre)
			if guardar!="":
				plt.savefig(carpeta+"/mom_ang_"+cuerpitos[r].nombre+".png")
		else:
			plt.title("Momento angular, posiciones y velocidad de Cuerpo "+str(r))
			if guardar!="":
				plt.savefig(carpeta+"/mom_ang_cuerpo"+str(r)+".png")
		plt.show()
		plt.clf()
		r+=1
	try:
		e_c=energia_cinetica_par(velocidades,masas)
		periodos,semiejes,constantes=per_distorb_terc_ley(posiciones,e_c,tiempito,masas)
		h=1
		for i,j,k in zip(constantes,periodos,semiejes):
			plt.bar(1,i[0],align='center',color='SkyBlue',label=r'$\frac{T^2}{a^3}(M+m)$')
			plt.bar(2,i[1],align='center',color='IndianRed',label=r'$\frac{4\pi^2}{G}$')
			plt.text(0.65,0.2e30,str(i[0]),bbox=dict(facecolor='wheat',alpha=0.5))
			plt.text(1.65,0.2e30,str(i[1]),bbox=dict(facecolor='wheat',alpha=0.5))
			plt.text(0.65,0.6e30,"T="+str(j),bbox=dict(facecolor='wheat',alpha=0.5))
			plt.text(0.65,0.8e30,"a="+str(k),bbox=dict(facecolor='wheat',alpha=0.5))
			plt.legend()
			if cuerpitos[h].nombre!="0":
				plt.title("Tercera ley de Kepler - "+cuerpitos[h].nombre)
				if guardar!="":	
					plt.savefig(carpeta+"/tercera_ley_"+cuerpitos[h].nombre+".png")
			else:
				plt.title("Tercera ley de Kepler - Cuerpo "+str(h))
				if guardar!="":	
					plt.savefig(carpeta+"/tercera_ley_cuerpo"+str(h)+".png")
			plt.show()
			plt.clf()
			h+=1
	except:
		pass		
	r=1
	for i in Range(n):
		cadacuerpo=[]
		for instante in posiciones:
			cadacuerpo.append(instante[i])
		if cuerpitos[i].nombre!="0":
			plt.plot([x[0] for x in cadacuerpo],[x[1] for x in cadacuerpo],".",label=cuerpitos[i].nombre)
		else:
			plt.plot([x[0] for x in cadacuerpo],[x[1] for x in cadacuerpo],".",label="Cuerpo "+str(i+1))
	plt.legend()
	plt.axis("equal")
	plt.title("Orbitas en 2D")
	if guardar!="":
		plt.savefig(carpeta+"/orbita.png")
	plt.show()
	plt.clf()


#Definir opcion de guardado o no
#Graficar colisiones?
#Sentido dimensional al random
