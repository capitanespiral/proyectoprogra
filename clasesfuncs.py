#!/usr/bin/python
#-*- coding:utf-8 -*-
from math import *
import numpy as np
from time import *
#TODA LISTA USADA TIENE QUE SER ARRAY DE NUMPY
#Definir método para que posición cambie segun velocidad ¿o tengo que definirlo con todo lo demás?
#Definir choques
#Definir tamaño en función de la masa
#Definir cálculo de X a través de runge kutta

class cuerpo:
	#m masa (acepta float), v velocidad (acepta lista, origen en el cuerpo en si, definida cartesiana), p posición (acepta lista, definida de forma polar)
	def __init__(self,p,v,m):
		#agregar metodo que p cambie en función de v
		self.p=p
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

vector=[0.0,0.0]
def acel(t,p,v,m,n):
	#función que da aceleracion (segunda derivada de posición), recibe tiempo, posición (lista de listas de posiciones), velocidad inicial, masa y cantidad de partículas. 
	d2p=np.array([vector]*n)
	G=-6.673884e-11
	#d=distancia en la cual la velocidad ya no aumenta?
	for i in range(0,n):
		for j in range(0,n):
			if j!=i:
				Rij=np.linalg.norm(p[i]-p[j])
				d2p[i]=d2p[i]+G*m[j]*(p[i]-p[j])/pow(Rij,3)
				
	return d2p

#def fx(v):
#	return v
				
def rk1(kp,kv,p0,v0,n,var,h):
	#las cuatro primeras listas de listas,kp(kix) -> k de las posiciones, kv(kiv) -> k de las velocidades. p0(xio)->posiciones iniciales, v0(vio) -> velocidades iniciales. n cantidad de cuerpos, var NIIDEA, h?
	kp1=h*kp
	kv1=h*kv
	p1=np.array([vector]*n)
	v1=np.array([vector]*n)
	for i in range(0,n):
		if var==1:
			p1[i]=p0[i]+kp1[i]/2.0
			v1[i]=v0[i]+kv1[i]/2.0
		else:
			p1[i]=p0[i]+kp1[i]
			v1[i]=v0[i]+kv1[i]
	return p1,v1,kp1,kv1

def rk2(k1,k2,k3,k4,p0,n):
	#las cinco primeras lista de listas, p0 y n same que arriba, k son las k para rukkatacaputa
	p1=np.array([vector]*n)
	for i in range(0,n):
		p1[i]=p0[i]+(k1[i]+2*(k2[i]+k3[i])+k4[i])/6.0
	return p1

def rk(p0,v0,tf,ti,m,n):
	#primeras dos same que arriba
	var=1
	h=tf-ti

	#Las dos k son listas de listas
	k1x=v0
	k1v=acel(ti,p0,v0,m,n)
	p1,v1,k1x,k1v=rk1(k1x,k1v,p0,v0,n,var,h)

	k2x=v1
	k2v=acel(ti+h/2.0,p1,v1,m,n)	
	p1,v1,k2x,k2v=rk1(k2x,k2v,p0,v0,n,var,h)
	
	var=0
	k3x=v1
	k3v=acel(ti+h/2.0,p1,v1,m,n)
	p1,v1,k3x,k3v=rk1(k3x,k3v,p0,v0,n,var,h)

	k4x=v1
	k4v=acel(ti+h,p1,v1,m,n)
	p1,v1,k4x,k4v=rk1(k4x,k4v,p0,v0,n,var,h)
	
	p1=rk2(k1x,k2x,k3x,k4x,p0,n)
	pf=p1
	
	v1=rk2(k1v,k2v,k3v,k4v,v0,n)
	vf=v1

	return pf,vf


tf=30
ti=10
