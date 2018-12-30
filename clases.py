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
def fv1(t,p,v,m,n):
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

def fx(v):
	return v
				
def rk1(kix,kiv,xio,vio,n,var,h):
	#kix tiene que ser array
	kipx=h*kix
	kipv=h*kiv
	print kipx
	print kipv
	xip=np.array([vector]*n)
	vip=np.array([vector]*n)
	for i in range(0,n):
		if var==1:
			xip[i]=xio[i]+kipx[i]/2
			vip[i]=vio[i]+kipv[i]/2
		else:
			xip[i]=xio[i]+kipx[i]
			vip[i]=vio[i]+kipv[i]
	return xip,vip,kipx,kipv

def rk2(k1,k2,k3,k4,xio2,n):
	xip2=xio2+(k1+2*(k2+k3)+k4)/6
	return xip2

def rk(fv,fx,xi,vi,tf,ti,m,n):
	var=1
	h=tf-ti

	k1x=fx(vi)
	k1v=fv(ti,xi,vi,m,n)
	xiv,viv,k1x,k1v=rk1(k1x,k1v,xi,vi,n,var,h)

	k2x=fx(viv)
	k2v=fv(ti+h/2.0,xiv,viv,m,n)	
	xiv,viv,k2x,k2v=rk1(k2x,k2v,xi,vi,n,var,h)
	
	var=0
	k3x=fx(viv)
	k3v=fv(ti+h/2.0,xiv,viv,m,n)
	xiv,viv,k3x,k3v=rk1(k3x,k3v,xi,vi,n,var,h)

	k4x=fx(viv)
	k4v=fv(ti+h,xiv,viv,m,n)
	xiv,viv,k4x,k4v=rk1(k4x,k4v,xi,vi,n,var,h)
	
	xiv=rk2(k1x,k2x,k3x,k4x,xi,n)
	xf=xiv
	
	viv=rk2(k1v,k2v,k3v,k4v,vi,n)
	vf=viv

	return xf,vf


posiciones=np.array([[0,3],[0,2],[0,-2],[1,1]])
a=rk1(posiciones,posiciones,posiciones,posiciones,4,0,7)
#print a

