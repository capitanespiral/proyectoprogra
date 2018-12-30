#!/usr/bin/python
#-*- coding:utf-8 -*-
from math import *
import numpy as np
#TODA LISTA USADA TIENE QUE SER ARRAY DE NUMPY
#Definir método para que posición cambie segun velocidad ¿o tengo que definirlo con todo lo demás?
#Definir choques
#Definir tamaño en función de la masa
#Definir cálculo de X a través de runge kutta
class cuerpo:
	#m masa (acepta float), v velocidad (acepta lista, origen en el cuerpo en si, definida cartesiana), p posición (acepta lista, definida de forma polar)
	def __init__(self,p,m,v):
		#agregar metodo que p cambie en función de v
		self.p=p
		#radio y ángulo de "órbita", del origen (centro estrellita) al cuerpo, ¿serán necesarios como atributos?.
		self.x=float(p[0])
		self.y=float(p[1])
		#masa
		self.m=float(m)
		#velocidad y sus componentes
		self.v=v
		self.vx=v[0]
		self.vy=v[1]
		#Momentum lineal
		self.mom=[self.m*self.vx,self.m*self.vy]
		#self.R=? -> agregar radio del cuerpo (tamaño) en función de su masa
	def ppol(self): #Mantener esto como método o agregarlo como atributos?
		r=sqrt(self.x**2+self.y**2)
		if self.x==0:
			if self.y>0:
				ang=pi/2
			else:
				ang=3*pi/2
		elif self.y==0:
			if self.x>0:
				ang=0
			else:
				ang=pi
		elif self.x>0:
			if self.y>0:
				ang=atan(self.y/self.x)
			else:
				ang=2*pi+atan(self.y/self.x)
		else:
			if self.y>0:
				ang=pi+atan(self.y/self.x)
			else:
				ang=pi+atan(self.y/self.x)
		return [r,ang]


def vf(t,p,v,m):
	#función que da ¿velocidad final?, recibe tiempo, posición (lista de listas de posiciones), velocidad inicial, masa y cantidad de partículas. 
	vector=[0.0,0.0]
	d2p=np.array([vector]*len(p))
	G=-6.673884e-11
	for i in range(0,len(p)):
		for j in range(0,len(p)):
			if j!=i:
				Rij=np.linalg.norm(p[i]-p[j])
				d2p[i]=d2p[i]+G*m[j]*(p[i]-p[j])/pow(Rij,3)
				
	return d2p
				
	#d=distancia en la cual la velocidad ya no aumenta?
	#return vfs

posiciones=np.array([[0,3],[0,2],[0,-2],[1,1]])
a=vf(1,posiciones,2,np.array([3,2,4,5]))
print a

