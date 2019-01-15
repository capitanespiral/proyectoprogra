#!/usr/bin/python
#-*- coding:utf-8 -*-
import math
import numpy as np
#HACER LISTA GENERAL DE ATRIBUTOS
#densidad=3132.375 promedio de los planetas del sistema solar



G=-6.674e-11 #en mks
conversionm_a_ua=(1.0/149597870700)
conversions_a_a=3600*24*365
G_ua_anio=G*(conversionm_a_ua**3)*((3600*24*365)**2)
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

	#Funcion que crea un objeto resultado de choque de varios.
	def unionchoque(self,otros):
		totalmasa=0.0
		momentumtotal=np.array([0.0]*3)
		sumapos=np.array([0.0]*3)
		for i in otros:
			totalmasa+=i.m
			momentumtotal+=np.array(i.mom)
			sumapos+=i.p
			
		self.m=totalmasa
		self.mom=momentumtotal
		self.p=sumapos/float(len(otros))
		self.v=self.mom/float(self.m)
		self.vx=float(self.v[0])
		self.vy=float(self.v[1])
		self.vz=float(self.v[2])
		self.R=(3.348071936e-33*((3*self.m)/(4*math.pi*self.d)))**(1/3.0)

		return self



#DEFINIR FUNCIONES

#range generador		
def Range(f,i=0,p=1):
	while i<f:
		yield i
		i+=p

def comparamasas(a,b):
	if a.m>b.m:
		return 1
	elif a.m<b.m:
		return -1
	return 0

def momentoangular(p,v,masa):
	#Masa en masas terrestres
	#Funciona con el elemento que gira en primera fila y el centro en segunda fila
	m_a=[]
	m_p=[]
	m_v=[]
	m=masa[1:]
	for indice,masa in enumerate(m):
		mom_ang=[]
		modpos=[]
		modvel=[]
		for k in Range(len(p)):
			L=(masa/(5.972e24))*np.cross(p[k][indice+1],v[k][indice+1])
			mom_ang.append(np.linalg.norm(L))
			modpos.append(np.linalg.norm(p[k][indice+1]))
			modvel.append(np.linalg.norm(v[k][indice+1]))
		m_a.append(mom_ang)
		m_p.append(modpos)
		m_v.append(modvel)
	return m_a,m_p,m_v

def energia_cinetica_par(vel,masa):
	m=masa[1:]
	e_c=[]
	for indice,masa in enumerate(m):
		e_cin=[]
		for i in Range(len(vel)):
			#Guardo energía cinética de todos los tiempos para cada cuerpo
			vicuad=(np.linalg.norm(vel[i][indice+1]))**2
			cinetica=vicuad*masa
			e_cin.append(0.5*cinetica)
		e_c.append(e_cin)
	return e_c

def per_distorb_terc_ley(p,ec,t,m):
	global G_ua_anio
	G=G_ua_anio
	#Guardamos las x de cada cuerpo para todos los tiempos.
	x_total=[]
	for indice in Range(len(m)-1):
		x=[]
		for k in p:
			x.append(k[indice+1][0])
		x_total.append(x)

	semiejes=map(lambda x:(abs(max(x))+abs(min(x)))/2.0,x_total)
	
	peaks_total=[]
	for i in ec:
		i=i[1:]
		peaks=[]
		k=0
		for ind,obj in enumerate(i):
			if i[ind-1]<obj and i[ind+1]<obj:
				peaks.append(ind)
				k+=1
			if k==2:
				peaks_total.append(peaks)
				break
	k=1
	periodos=[]
	constantes=[]
	for i in peaks_total:
		tiemposs=t[:]
		t1=t.pop(i[0])
		t2=t.pop(i[1])
		periodo=(abs(t1-t2))
		c1=(((periodo**2)*(m[0]+m[k]))/((semiejes[k-1])**3))
		c2=((4*(math.pi**2))/(G))
		c=[c1,c2]
		periodos.append(periodo)
		constantes.append(c)
		k+=1		
	
	return periodos,semiejes,constantes

def energia_potencial(p,cuerpitos,n):
	global G_ua_anio
	G=G_ua_anio
	e_pot=[]
	for k in Range(len(p)):
		potencial=0.0
		for i in Range(n):
			for j in Range(n):
				if j!=i:
					Rij=np.linalg.norm(p[k][i]-p[k][j])
					potencial+=(G*cuerpitos[i].m*cuerpitos[j].m)/Rij
		e_pot.append(0.5*potencial)
	return np.array(e_pot)

def energia_cinetica(vel,cuerpitos,n):
	e_cin=[]
	for i in Range(len(vel)):
		cinetica=0.0
		for j in Range(n):
			vicuad=(np.linalg.norm(vel[i][j]))**2
			cinetica+=vicuad*cuerpitos[j].m
		e_cin.append(0.5*cinetica)
	return np.array(e_cin)

				
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
	global G_ua_anio
	G=G_ua_anio
	d=0.0003342293561134223
	for i in Range(n):
		for j in Range(n):
			if j!=i:
				Rij=np.linalg.norm(p[i]-p[j])
				if Rij>d: 
					evalua[i]+=G*m[j]*(p[i]-p[j])/pow(Rij,3)
				

				
	return evalua,v
				
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

def distmax(pos):
	for i in pos:
		for j in i:
			distmaxx=[]
			distmaxx.append(np.linalg.norm(j))
	return max(distmaxx)

def rk4(p_i,v_i,tiempo,h,m,n):
	#Las dos primeras listas de listas
	#Obtenemos cada k1
	#kp_1=v_i
	kv_1,kp_1=evaluar_diff(p_i,v_i,m,n)
	#Cambiamos pt de evaluación para obtener k2
	var=1
	p_i_,v_i_,kp_1_h,kv_1_h=camb_pt_eval(kp_1,kv_1,p_i,v_i,n,var,h)
	#Calculamos k2 en el punto medio
	#kp_2=v_i_
	kv_2,kp_2=evaluar_diff(p_i_,v_i_,m,n)
	#Cambiamos punto de evaluación para obtener k3
	p_i_,v_i_,kp_2_h,kv_2_h=camb_pt_eval(kp_2,kv_2,p_i,v_i,n,var,h)
	#Calculamos k3 en el punto medio
	#kp_3=v_i_
	kv_3,kp_3=evaluar_diff(p_i_,v_i_,m,n)
	#Cambiamos punto de evaluación para obtener k4
	var=0
	p_i_,v_i_,kp_3_h,kv_3_h=camb_pt_eval(kp_3,kv_3,p_i,v_i,n,var,h)
	#Calculamos k4 al final
	#kp_4=v_i_
	kv_4,kp_4=evaluar_diff(p_i_,v_i_,m,n)
	kp_4_h,kv_4_h=kp_4*h,kv_4*h
	
	p_i_1=p_i+(kp_1_h+2*(kp_2_h+kp_3_h)+kp_4_h)/6.0
	
	v_i_1=v_i+(kv_1_h+2*(kv_2_h+kv_3_h)+kv_4_h)/6.0

	return p_i_1,v_i_1


def rka(p,v,tiempo_actual,tau,m,n,pasomaximo):

	adaptErr=1e-3
	# factores de seguridad
	safe1 = 0.7
	safe2 = 1.4
	maxTray=100
	for iTray in range(maxTray):
		# Tomemos dos pequeños pasos en el tiempo
		half_tau = 0.5*tau
		xSmall,vSmall=rk4(p,v, tiempo_actual, half_tau,m,n)
		tiempo_sig=tiempo_actual+half_tau
		xSmall,vSmall=rk4(xSmall,vSmall, tiempo_sig, half_tau,m,n)
		# Tomemos un solo tiempo grande
		xBig,vBig=rk4(p,v, tiempo_actual, tau,m,n)

		eps = 1.0e-16
		errores=[]
		for i in Range(n):
			for j in Range(3):
				scalex = adaptErr*(abs(xSmall[i][j])+abs(xBig[i][j]))/2.0
				scalev=adaptErr*(abs(vSmall[i][j])+abs(vBig[i][j]))/2.0
				error_truncax = vSmall[i][j]-vBig[i][j]
				error_truncav = xSmall[i][j]-xBig[i][j]
				ratiox = abs(error_truncax)/(scalex+eps)
				ratiov= abs(error_truncav)/(scalev+eps)
				if ratiox==0.0:
					ratiox=eps
				if ratiov==0.0:
					ratiov=eps
				errores.append(ratiox)
				errores.append(ratiov)
			ratio=max(errores)
		
	# Estimamos el nuevo valor de tau (incluyendo factores de seguridad)
			tau_ant= tau
			print "ratio"+str(ratio)
			tau = safe1*tau_ant*pow(ratio,-0.20)
			if tau < tau_ant/safe2 :
				tau=tau_ant/safe2
			elif tau > safe2*tau_ant :
				tau=safe2*tau_ant
			else:
				tau=tau
			if tau>pasomaximo:
				tau=pasomaximo
		# Si el error es aceptable regrese los valores computados
			if ratio < 1 :
				return xSmall,vSmall,tiempo_actual+tau,tau 
	else:
		print "Error: Runge-Kutta adaptativo fallo"
		exit()


