#!/usr/bin/python
#-*- coding:utf-8 -*-
from math import *
import numpy as np
#TODA LISTA USADA TIENE QUE SER ARRAY DE NUMPY
#Definir choques
#HACER LISTA GENERAL DE ATRIBUTOS
#densidad=3132.375 promedio de los planetas del sistema solar
#modificar listas por generadores, compresion de listas, etc... (tambien en main)
#Crear clase estrella

class cuerpo:
	#m masa (acepta float), v velocidad (acepta lista, origen en el cuerpo en si, definida cartesiana), p posición (acepta lista, definida de forma cartesiana)
	def __init__(self,p=[0.0,0.0],v=[0.0,0.0],m=1.0,d=3132.375):
		#Posición
		self.p=p
		self.x=float(self.p[0])
		self.y=float(self.p[1])
		#masa y densidad
		self.m=float(m)
		self.d=float(d)
		#velocidad y sus componentes
		self.v=v
		self.vx=float(self.v[0])
		self.vy=float(self.v[1])
		#Momentum lineal
		self.mom=[self.m*self.vx,self.m*self.vy]
		self.R=((3*self.m)/(4*pi*self.d))**(1/3)
	#Cambios de atributos
	def cambios(self,p,v,m):
		self.p=p	
		self.x=float(self.p[0])
		self.y=float(self.p[1])
		self.m=float(m)
		self.v=v		
		self.vx=float(self.v[0])
		self.vy=float(self.v[1])				
		self.mom=[self.m*self.vx,self.m*self.vy]
		self.R=((3*self.m)/(4*pi*self.d))**(1/3.0)
		return self
	#Coordenadas polares
	def ppol(self):
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

	def unionchoque(self,otros):
		totalmasa=0.0
		momentumtotal=np.array([0.0,0.0])
		sumapos=np.array([0.0,0.0])
		densidad=0.0
		for i in otros:
			totalmasa=totalmasa+i.m
			momentumtotal=momentumtotal+np.array(i.mom)
			sumapos=sumapos+i.p
			densidad+=i.d

		self.m=totalmasa
		self.mom=momentumtotal
		self.p=sumapos/float(len(otros))
		self.x=self.p[0]
		self.y=self.p[1]
		self.v=self.mom/float(self.m)
		self.vx=float(self.v[0])
		self.vy=float(self.v[1])
		self.R=((3*self.m)/(4*pi*self.d))**(1/3)
		return self
		
		
		
vector=[0.0,0.0]
def evalua_dists(p,n,cuerpitos):
	#Reciba lista de lista de posiciones.
	paraunir=[]
	paraunirtotal=[]
	for i in range(n):
		for j in range(n):
			if j!=i:
				Rij=np.linalg.norm(p[i]-p[j])
				if Rij<=(cuerpitos[i].R+cuerpitos[j].R):
					unir=[i,j]
					unir.sort()
					if unir not in paraunir:
						#Genero lista que guarda pares ordenados representando el posible "choque" (menos de los dos radios)
						paraunir.append(unir)
	#Seleccionando a los que interactuan entre si
	while len(paraunir)!=0:
		pegaditos=[]
		pegaditos.append(paraunir[0][0])
		pegaditos1=[]
		while len(pegaditos1)!=len(pegaditos):
			pegaditos1=pegaditos[:]
			for j in pegaditos:
				for h in paraunir:
					if j==h[0]:
						a=h[:]
						paraunir.remove(h)
						if a[1] not in pegaditos:
							pegaditos.append(a[1])
					elif j==h[1]:
						a=h[:]
						paraunir.remove(h)
						if a[0] not in pegaditos:
							pegaditos.append(a[0])
		#Voy guardando cada lista conteniendo los que interactuan entre si.				
		paraunirtotal.append(pegaditos)
	return paraunirtotal


def choques(paraunirtotal,cuerpitos):
	#función que crea objetos por unirlos a través de choques
	listaplana=[]
	nuevoscuerpos=[]
	for colisionados in paraunirtotal:
		cuerposo=[]
		for j in colisionados:
			listaplana.append(j)
			cuerposo.append(cuerpitos[j])
		a=cuerpo()
		b=a.unionchoque(cuerposo)
		cuerpitos.append(b)
	for j in range(len(cuerpitos)):
		if j not in listaplana:
			nuevoscuerpos.append(cuerpitos[j])
	
	return nuevoscuerpos
	

def evaluar_diff(p,v,m,n):
	#función que evalua la diferencial principal. p y v listas de listas, m solo lista, n natural
	evalua=np.array([vector]*n)
	G=-6.673884e-11
	#d=distancia en la cual la velocidad ya no aumenta?
	for i in range(n):
		for j in range(n):
			if j!=i:
				Rij=np.linalg.norm(p[i]-p[j])
				evalua[i]=evalua[i]+G*m[j]*(p[i]-p[j])/pow(Rij,3)
				
	return evalua
				
def camb_pt_eval(kp_i,kv_i,p_i,v_i,n,var,h):
	#cambia punto donde se evalua diferencial, 4 primeras listas de listas, n natural, var natural, h escalar
	kp_i_h=h*kp_i
	kv_i_h=h*kv_i
	p_i_=np.array([vector]*n)
	v_i_=np.array([vector]*n)
	for i in range(n):
		if var==1:
			p_i_[i]=p_i[i]+kp_i_h[i]/2.0
			v_i_[i]=v_i[i]+kv_i_h[i]/2.0
		else:
			p_i_[i]=p_i[i]+kp_i_h[i]
			v_i_[i]=v_i[i]+kv_i_h[i]
	return p_i_,v_i_,kp_i_h,kv_i_h

def r_final(k1_h,k2_h,k3_h,k4_h,p_v_i,n):
	#las cinco primeras lista de listas, n natural, p_v_i -> entrará p o v y saldrá resultado final de rk4.
	p_v_i_1=np.array([vector]*n)
	for i in range(0,n):
		p_v_i_1[i]=p_v_i[i]+(k1_h[i]+2*(k2_h[i]+k3_h[i])+k4_h[i])/6.0
	return p_v_i_1

def rk4(p_i,v_i,h,m,n):
	#Las dos primeras listas de listas
	#Obtenemos cada k1
	kp_1=v_i
	kv_1=evaluar_diff(p_i,v_i,m,n)
	#Cambiamos pt de evaluación para obtener k2
	var=1
	p_i_,v_i_,kp_1_h,kv_1_h=camb_pt_eval(kp_1,kv_1,p_i,v_i,n,var,h)
	#Calculamos k2 en el punto medio
	kp_2=v_i_
	kv_2=evaluar_diff(p_i_,v_i_,m,n)
	#Cambiamos punto de evaluación para obtener k3
	p_i_,v_i_,kp_2_h,kv_2_h=camb_pt_eval(kp_2,kv_2,p_i,v_i,n,var,h)
	#Calculamos k3 en el punto medio
	kp_3=v_i_
	kv_3=evaluar_diff(p_i_,v_i_,m,n)
	#Cambiamos punto de evaluación para obtener k4
	var=0
	p_i_,v_i_,kp_3_h,kv_3_h=camb_pt_eval(kp_3,kv_3,p_i,v_i,n,var,h)
	#Calculamos k4 al final
	kp_4=v_i_
	kv_4=evaluar_diff(p_i_,v_i_,m,n)
	kp_4_h,kv_4_h=kp_4*h,kv_4*h
	
	p_i_1=r_final(kp_1_h,kp_2_h,kp_3_h,kp_4_h,p_i,n)
	
	v_i_1=r_final(kv_1_h,kv_2_h,kv_3_h,kv_4_h,v_i,n)

	return p_i_1,v_i_1





