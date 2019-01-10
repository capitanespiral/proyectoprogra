#!/usr/bin/python
#-*- coding:utf-8 -*-
import math
import numpy as np
#TODA LISTA USADA TIENE QUE SER ARRAY DE NUMPY
#Definir choques
#HACER LISTA GENERAL DE ATRIBUTOS
#densidad=3132.375 promedio de los planetas del sistema solar
#modificar listas por generadores, compresion de listas, etc... (tambien en main)
#Crear clase estrella

#CREACIÓN DE CLASE DE CUERPO
class cuerpo:
	#m masa (acepta float) [kg], v velocidad (acepta lista, origen en el cuerpo en si, definida cartesiana) [ua/año], p posición (acepta lista, definida de forma cartesiana) [ua]
	def __init__(self,p=[0.0]*3,v=[0.0]*3,m=1.0,d=3132.375):
		#Posición
		self.p=p
		#masa y densidad
		self.m=float(m)
		self.d=float(d)
		#velocidad y sus componentes
		self.v=v
		self.vx=float(self.v[0])
		self.vy=float(self.v[1])
		self.vz=float(self.v[2])
		#Momentum lineal
		self.mom=[self.m*self.vx,self.m*self.vy,self.m*self.vz]
		self.R=(3.348071936e-33*((3*self.m)/(4*math.pi*self.d)))**(1/3.0)

		#self.x=float(self.p[0])
		#self.y=float(self.p[1])
		#self.z=float(self.p[2])

	#Cambios de atributos
	def cambios(self,p,v,m):
		self.p=p	
		self.m=float(m)
		self.v=v			
		self.vx=float(self.v[0])
		self.vy=float(self.v[1])
		self.vz=float(self.v[2])	
		self.mom=[self.m*self.vx,self.m*self.vy,self.m*self.vz]
		self.R=(3.348071936e-33*((3*self.m)/(4*math.pi*self.d)))**(1/3.0)

		#self.x=float(self.p[0])
		#self.y=float(self.p[1])
		#self.z=float(self.p[2])
		return self

	#Coordenadas polares
	def ppol(self):
		r=math.sqrt(self.x**2+self.y**2)
		if self.x==0:
			if self.y>0:
				ang=math.pi/2
			else:
				ang=3*math.pi/2
		elif self.y==0:
			if self.x>0:
				ang=0
			else:
				ang=math.pi
		elif self.x>0:
			if self.y>0:
				ang=math.atan(self.y/self.x)
			else:
				ang=2*math.pi+math.atan(self.y/self.x)
		else:
			if self.y>0:
				ang=math.pi+math.atan(self.y/self.x)
			else:
				ang=math.pi+math.atan(self.y/self.x)
		return [r,ang]

#Arreglar unión con densidad ponderada
	def unionchoque(self,otros):
		totalmasa=0.0
		densidad=0.0
		momentumtotal=np.array([0.0]*3)
		sumapos=np.array([0.0]*3)
		for i in otros:
			totalmasa+=i.m
			momentumtotal+=np.array(i.mom)
			sumapos+=i.p
			densidad+=i.d

		self.m=totalmasa
		self.mom=momentumtotal
		self.p=sumapos/float(len(otros))
		self.v=self.mom/float(self.m)
		self.vx=float(self.v[0])
		self.vy=float(self.v[1])
		self.vz=float(self.v[2])
		self.R=(3.348071936e-33*((3*self.m)/(4*math.pi*self.d)))**(1/3.0)

		#self.x=self.p[0]
		#self.y=self.p[1]
		#self.z=self.p[2]

		return self



#DEFINIR FUNCIONES

#range generador		
def Range(f,i=0,p=1):
	while i<f:
		yield i
		i+=p

		
vector=[0.0,0.0,0.0]
def evalua_dists(p,n,cuerpitos):
	#Reciba lista de lista de posiciones.
	paraunir=[]
	paraunirtotal=[]
	for i in Range(n):
		for j in Range(n):
			if j!=i:
				Rij=np.linalg.norm(p[i]-p[j])
				if Rij<=(cuerpitos[i].R+cuerpitos[j].R):
					unir=[i,j]
					unir.sort()
					if unir not in paraunir:
						#Genero lista que guarda pares ordenados representando el posible "choque" (menos de dos radios)
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
	#función que crea objetos para unirlos a través de choques
	indices=[]
	nuevoscuerpos=[]
	#itera sobre cada lista de paraunirtotal (los que se viven una instancia de tocarse)
	for colisionados in paraunirtotal:
		chocadores=[]
		for j in colisionados:
			indices.append(j)
			chocadores.append(cuerpitos[j])
		a=cuerpo()
		b=a.unionchoque(chocadores)
		cuerpitos.append(b)
	for j in Range(len(cuerpitos)):
		if j not in indices:
			nuevoscuerpos.append(cuerpitos[j])
	
	return nuevoscuerpos
	

def evaluar_diff(p,v,m,n):
	#función que evalua la diferencial principal. p y v listas de listas, m solo lista, n natural
	evalua=np.array([vector]*n)
	G=-1.9812727537285508e-29
	#d=distancia en la cual la velocidad ya no aumenta?
	for i in Range(n):
		for j in Range(n):
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
	if var==1:
		p_i_=p_i+kp_i_h/2.0
		v_i_=v_i+kv_i_h/2.0
	else:
		p_i_=p_i+kp_i_h
		v_i_=v_i+kv_i_h
	return p_i_,v_i_,kp_i_h,kv_i_h

def rk4(p_i,v_i,tiempo,h,m,n):
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
	
	p_i_1=p_i+(kp_1_h+2*(kp_2_h+kp_3_h)+kp_4_h)/6.0
	
	v_i_1=v_i+(kv_1_h+2*(kv_2_h+kv_3_h)+kv_4_h)/6.0

	return p_i_1,v_i_1

def rka(p,v,tiempo,tau,m,n):
	adaptErr=1e-3
	tSave = tiempo
	## factores de seguridad
	safe1 = 0.9
	safe2 = 4.0
	maxTray=100
	for iTray in range(maxTray):
		## Tomemos dos pequennos pasos en el tiempo
		half_tau = 0.5*tau
		xSmall,vSmall=rk4(p,v, tSave, half_tau,m,n)
		tiempo = tSave + half_tau
		xSmall,vSmall=rk4(xSmall,vSmall, tiempo, half_tau,m,n)
		## Tomemos un solo tiempo grande
		xBig,vBig=rk4(p,v, tSave, tau,m,n)
		## Calculemos el error de truncamiento estimado
		erroRatiox = 0.0
		erroRatiov=0.0
		eps = 1.0e-16
		for i in Range(n):
			for j in Range(3):
				scale = adaptErr*(abs(xSmall[i][j])+abs(xBig[i][j]))/2.0
				xDiff = xSmall[i][j]-xBig[i][j]
				ratiox = abs(xDiff)/(scale+eps)
				if erroRatiox <= ratiox :
					erroRatiox=ratiox
		
	## Estimamos el nuevo valor de tau (incluyendo factores de seguridad)
		tau_old= tau
		print "errorRatiox"+str(erroRatiox)
		tau = safe1*tau_old*math.pow(erroRatiox,-0.20)
		if tau <= tau_old/safe2 :
			tau=tau_old/safe2
		if tau >= safe2*tau_old :
			tau=safe2*tau_old
	## Si el error es aceptable regrese los valores computados
		if erroRatiox < 1 :
			return xSmall,vSmall,tiempo+tau,tau 

#numpy.array( [xSmall[0],xSmall[1],xSmall[2],xSmall[3], tiempo, tau] )
	else:
		print "Error: Runge-Kutta adaptativo fallo"
		exit()


