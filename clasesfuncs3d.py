#!/usr/bin/python
#-*- coding:utf-8 -*-
#Importamos dos modulos a usar
import math
import numpy as np

#densidad=3132.375 promedio de los planetas del sistema solar


#La variable G, transformada a nuestro sistema  de UA'S, años y kg's. Para ser usada en las funciones
G=-6.674e-11 #en mks
conversionm_a_ua=(1.0/149597870700)
conversions_a_a=3600*24*365
G_ua_anio=G*(conversionm_a_ua**3)*((3600*24*365)**2)
#CREACIÓN DE CLASE DE CUERPO
class cuerpo:
	#Se inicia el cuerpo, los parámetros aceptados son la posición, velocidad, masa, densidad y nombre.
	#Se consideró implementar densidad pero se dejó de lado pues no agregaba tanto al proyecto y si complicaba bastante.
	#Como ya estaba definido se dejó como la densidad promedio de los planetas del sistema solar (en kg/m^3)
	def __init__(self,p=[0.0]*3,v=[0.0]*3,m=1.0,d=3132.375,nombre=0):
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
		#Radio de cada cuerpo, en funcion de su densidad y masa. La constante al principio lo transforma en UA
		self.R=(3.348071936e-33*((3*self.m)/(4*math.pi*self.d)))**(1/3.0)
		self.nombre=str(nombre)

	#Cambios de atributos. Función para actualizar los atributos de los cuerpos en cada iteración.
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

	#Coordenadas polares. Se definieron al comienzo pero nunca se usaron. Habrían sido una mejor solución para calcular el periodo de los cuerpos.
	#Se definen de tal forma que no se indefinan y siempre entreguen entre 0 y 2pi.
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

	#Funcion que crea un objeto resultado de choque de varios. Luego de elegir a los que chocaron se invoca esta función.
	def unionchoque(self,otros):
		#Definimos un acumulador y 2 matrices acumuladoras (mismo tamaño que lo que queremos guardar) y sumamos.
		totalmasa=0.0
		momentumtotal=np.array([0.0]*3)
		sumapos=np.array([0.0]*3)
		for i in otros:
			totalmasa+=i.m
			momentumtotal+=np.array(i.mom)
			sumapos+=i.p
		
		#El primer objeto se transforma en el "absorvedor" de los otros. Su masa es la suma de todas, su momentum la suma vectorial.
		#En base a estos dos se define la velocidad y sus componentes, se asigna el promedio de las posiciones y el nuevo radio.	
		self.m=totalmasa
		self.mom=momentumtotal
		self.p=sumapos/float(len(otros))
		self.v=self.mom/float(self.m)
		self.vx=float(self.v[0])
		self.vy=float(self.v[1])
		self.vz=float(self.v[2])
		self.R=(3.348071936e-33*((3*self.m)/(4*math.pi*self.d)))**(1/3.0)

		return self



#FUNCIONES A USAR

#range() generador, para gastar menos memoria		
def Range(f,i=0,p=1):
	while i<f:
		yield i
		i+=p

#Función que devuelve la posición mas lejana del cero en toda la simulación. Se usa para definir los ejes en la simulación 3d. 
def distmax(pos):
	for i in pos:
		for j in i:
			distmaxx=[]
			distmaxx.append(np.linalg.norm(j))
	return max(distmaxx)
	
#Comparación de masas, usada para ordenar la lista de cuerpos de mayor a menor masa con sort y cmp.
def comparamasas(a,b):
	if a.m>b.m:
		return 1
	elif a.m<b.m:
		return -1
	return 0

#Función que calcula el momento angular, el módulo de la posición, de la velocidad cada uno para cada instante. Usada para la segunda ley de kepler
#Lo hace para todos excepto para el primer cuerpo (pues es una ley sobre los cuerpos orbitando, asi que imaginamos el mas masivo como la estrella)
#Devuelve 3 listas de listas, con una lista por cuerpo de todos los valores mencionados en el tiempo.
#Recibe todas las posiciones, velocidades, y masas.
def momentoangular(p,v,masa):
	#Masa en masas terrestres para que en el gráfico se vean mas claros los valores.
	#Creamos las listas mas grandes
	m_a=[]
	m_p=[]
	m_v=[]
	#Solo consideramos del segundo cuerpo en adelante
	m=masa[1:]
	#Calculamos el momento angular para cada cuerpo
	for indice,masa in enumerate(m):
		#Almacenamos para cada cuerpo todo su historial de estos valores en estas listas que vamos limpiando.
		mom_ang=[]
		modpos=[]
		modvel=[]
		#Se hace el calculo en sí, y se guardan los modulos necesarios para el calculo
		for k in Range(len(p)):
			L=(masa/(5.972e24))*np.cross(p[k][indice+1],v[k][indice+1])
			mom_ang.append(np.linalg.norm(L))
			modpos.append(np.linalg.norm(p[k][indice+1]))
			modvel.append(np.linalg.norm(v[k][indice+1]))
		m_a.append(mom_ang)
		m_p.append(modpos)
		m_v.append(modvel)
	return m_a,m_p,m_v

#Función de la energia cinetica por separado (excepto al cuerpo central), solo se usa para calcular periodos. No funciona bien con sistemas de mas de dos particulas, lamentablemente.
def energia_cinetica_par(vel,masa):
	m=masa[1:]
	e_c=[]
	#El formato de la lista es muy similar al de la funcion anterior.
	for indice,masa in enumerate(m):
		e_cin=[]
		for i in Range(len(vel)):
			#Guardo energía cinética de todos los tiempos para cada cuerpo
			vicuad=(np.linalg.norm(vel[i][indice+1]))**2
			cinetica=vicuad*masa
			e_cin.append(0.5*cinetica)
		e_c.append(e_cin)
	return e_c

#Funcion que calcula las constantes explicitadas en la tercera ley de kepler. Para cada cuerpo excepto el central.
#Calcula periodo (muy mal con mas de dos cuerpos), semiejes y las constantes de la ley.
#Recibe posiciones, la funcion anterior, los tiempos y las masas.
def per_distorb_terc_ley(p,ec,t,m):
	#Usamos la G definida al principio
	global G_ua_anio
	G=G_ua_anio
	#Guardamos las x de cada cuerpo para todos los tiempos.
	x_total=[]
	for indice in Range(len(m)-1):
		x=[]
		for k in p:
			x.append(k[indice+1][0])
		x_total.append(x)
	#Obtenemos una lista de los semiejes de la elipse de cada cuerpo (el conocido "a").
	semiejes=map(lambda x:(abs(max(x))+abs(min(x)))/2.0,x_total)
	
	#Buscamos los dos primeros peaks de cada una de las listas de energia cinetica (una es el historial de ec de cada cuerpo). Guardamos su indice
	#Funciona bien con sistemas estables y aburridos, pues ahí cada peak es el perihelio, asi que el tiempo entre dos peaks sería el periodo.
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

	#Usamos los indices de los peaks para encontrar los tiempos y así el periodo (pues todo esta bien ordenado)
	periodos=[]
	constantes=[]
	for i in peaks_total:
		tiemposs=t[:]
		t1=t.pop(i[0])
		t2=t.pop(i[1])
		periodo=(abs(t1-t2))
		#Calculamos las constantes y almacenamos toda la info a retornar
		c1=(((periodo**2)*(m[0]+m[k]))/((semiejes[k-1])**3))
		c2=((4*(math.pi**2))/(G))
		c=[c1,abs(c2)]
		periodos.append(periodo)
		constantes.append(c)
		k+=1		
	
	return periodos,semiejes,constantes

#Funcion que calcula la energia potencial de todo el sistema, en todo momento. Recibe las posiciones, los cuerpos y la cantidad de cuerpos.
def energia_potencial(p,cuerpitos,n):
	#Se usa la variable global G
	global G_ua_anio
	G=G_ua_anio
	#Se calcula la energia potencial del sistema a cada tiempo y se devuelve como un arreglo numpy
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

#Esta funcion hace lo mismo que la anterior, pero con la energía cinetica. Recibe las velocidades, los cuerpos y la cantidad de cuerpos.
def energia_cinetica(vel,cuerpitos,n):
	e_cin=[]
	for i in Range(len(vel)):
		cinetica=0.0
		for j in Range(n):
			vicuad=(np.linalg.norm(vel[i][j]))**2
			cinetica+=vicuad*cuerpitos[j].m
		e_cin.append(0.5*cinetica)
	return np.array(e_cin)

#Defino un vector para las siguientes funciones.				
vector=[0.0,0.0,0.0]

#Funcion que evalua quienes son los cuerpos que chocaron. Recibe las posiciones de todos de cada instante (no todas las historicas como en las funciones anteriores), la cantidad de cuerpos y los cuerpos.
def evalua_dists(p,n,cuerpitos):
	#Reciba lista de lista de posiciones.
	paraunir=[]
	paraunirtotal=[]
	#Evaluamos si chocaron o no
	for i in Range(n):
		for j in Range(n):
			#No analizamos con uno mismo
			if j!=i:
				Rij=np.linalg.norm(p[i]-p[j])
				#Si distan menos de sus radios sumados, chocaron.
				if Rij<=(cuerpitos[i].R+cuerpitos[j].R):
					#Guardamos el par ordenado de los indices de quienes chocaron, lo ordenamos y vemos si ya esta para guardarlo o no.
					#Esto evita guardar el j,i si ya se vió el i,j
					unir=[i,j]
					unir.sort()
					if unir not in paraunir:
						paraunir.append(unir)

	#Seleccionando a los que interactuan entre si. Si 1 toca a 2 toca a 3 sin que 1 toque a 3, de todas formas se unen todos.
	#Se definió así pues se pensó que simplificaria las cosas.
	#Esto provoca chocar con todos los que chocan con lo que chocan contigo, por lo que la recursión es complicada (costó que saliera).
	#La recursion general termina cuando la lista de los que se uniran queda vacia
	while len(paraunir)!=0:
		#Agregamos el primer elemento del primer par ordenado.
		pegaditos=[]
		pegaditos.append(paraunir[0][0])
		pegaditos1=[]
		#Hacemos una copia que recorremos buscando a todos con quien interactua el indice agregado
		while len(pegaditos1)!=len(pegaditos):
			pegaditos1=pegaditos[:]
			for j in pegaditos:
				#Verificamos que si el numero esta en X se guarde X, y si esta en Y se guarde X. Luego borramos el par ordenado donde se encontró.
				#Buscamos no repetir ningun elemento
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
		#Esta lista contiene listas, cada una contiene quienes se unen entre si en ese momento. Claramente las listas tienen que ser mutuamente excluyentes (no compartir elementos).			
		paraunirtotal.append(pegaditos)
	return paraunirtotal

#Funcion que une finalmente los cuerpos usando el metodo para esto y la funcion anterior.
#Recibe la lista de lista de los que colisionarán y los cuerpos
def choques(paraunirtotal,cuerpitos):
	#función que crea objetos para unirlos a través de choques
	indices=[]
	nuevoscuerpos=[]
	#itera sobre cada lista de paraunirtotal (los que se viven una instancia de tocarse)
	for colisionados in paraunirtotal:
		chocadores=[]
		#Colisiona a los que deberian colisionar y agrega el nuevo elemento.
		for j in colisionados:
			indices.append(j)
			chocadores.append(cuerpitos[j])
		a=cuerpo()
		b=a.unionchoque(chocadores)
		cuerpitos.append(b)
	#Luego agregamos los que no estaban en los indices (pues debiesen seguir donde estaban)
	for j in Range(len(cuerpitos)):
		if j not in indices:
			nuevoscuerpos.append(cuerpitos[j])
	#Devolvemos la nueva lista de cuerpos
	return nuevoscuerpos
	
#Primera funcion para usar runge kutta. Evalua la diferencial.
#Recibe las posiciones, velocidades, masas, cantidad de cuerpos a cada instante.
def evaluar_diff(p,v,m,n):
	#Creo una lista del tamaño necesario.
	evalua=np.array([vector]*n)
	#Uso G global
	global G_ua_anio
	G=G_ua_anio
	#La siguiente siguiente linea y el if al final era para evitar que se dispararan las particulas cuando estuvieran muy cerca.
	#Sin embargo, no se logro a tiempo pegar las velocidades anteriores, asi que se anulaban en el proceso.
	#d=0.0003342293561134223
	for i in Range(n):
		for j in Range(n):
			#No se busca la interaccion con uno mismo
			if j!=i:
				Rij=np.linalg.norm(p[i]-p[j])
				#if Rij>d: 
				evalua[i]+=G*m[j]*(p[i]-p[j])/pow(Rij,3)
				

	#Retornan la evaluacion y la misma lista de velocidad
	return evalua,v

#Funcion que cambia el punto de evaluacion para runge kutta, recibe las k's (constantes de runge kutta) para posicion y evaluacion.
#Tambien las posiciones y velocidades actuales, cantidad de cuerpos, una variable para ajustar cuando hacer que cambio y h (el paso)
def camb_pt_eval(kp_i,kv_i,p_i,v_i,n,var,h):
	#Multiplicamos por el paso y creamos listas del tamaño que queremos
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

#Runge kutta tal cual, recibe las posiciones y velocidades actuales, el tiempo, el paso "h", las masas y la cantidad de cuerpos.
#Se usan las dos funciones anteriores.
def rk4(p_i,v_i,tiempo,h,m,n):
	#Obtenemos cada k1
	kv_1,kp_1=evaluar_diff(p_i,v_i,m,n)
	#Cambiamos pt de evaluación para obtener k2
	var=1
	p_i_,v_i_,kp_1_h,kv_1_h=camb_pt_eval(kp_1,kv_1,p_i,v_i,n,var,h)
	#Calculamos k2 en el punto medio
	kv_2,kp_2=evaluar_diff(p_i_,v_i_,m,n)
	#Cambiamos punto de evaluación para obtener k3
	p_i_,v_i_,kp_2_h,kv_2_h=camb_pt_eval(kp_2,kv_2,p_i,v_i,n,var,h)
	#Calculamos k3 en el punto medio
	kv_3,kp_3=evaluar_diff(p_i_,v_i_,m,n)
	#Cambiamos punto de evaluación para obtener k4
	var=0
	p_i_,v_i_,kp_3_h,kv_3_h=camb_pt_eval(kp_3,kv_3,p_i,v_i,n,var,h)
	#Calculamos k4 al final
	kv_4,kp_4=evaluar_diff(p_i_,v_i_,m,n)
	kp_4_h,kv_4_h=kp_4*h,kv_4*h

	#Evaluamosrunge kutta y obtenemos el siguiente instante. Se devuelven las nuevas posiciones y velocidades.
	
	p_i_1=p_i+(kp_1_h+2*(kp_2_h+kp_3_h)+kp_4_h)/6.0
	
	v_i_1=v_i+(kv_1_h+2*(kv_2_h+kv_3_h)+kv_4_h)/6.0

	return p_i_1,v_i_1

#Runge kutta adaptativo, usado para definir un paso h, ahora se usa tau.
#Recibe posiciones, velocidades, tiempo actual, el paso anterior (o inicial si es primera vez que se invoca), masas, cantidad de cuerpos y paso maximo para evitar que crezca demasiado.
def rka(p,v,tiempo_actual,tau,m,n,pasomaximo):
	#Error adaptativo
	adaptErr=1e-3
	#factores de seguridad para controlar el crecimiento o decrecimiento de tau (que no explote)
	safe1 = 0.7
	safe2 = 1.4
	#Cuantos intentos
	maxTray=100
	for iTray in range(maxTray):
		#Evaluamos con dos pasos en el tiempo
		half_tau = 0.5*tau
		pos,vel=rk4(p,v, tiempo_actual, half_tau,m,n)
		tiempo_sig=tiempo_actual+half_tau
		pos,vel=rk4(pos,vel, tiempo_sig, half_tau,m,n)
		#Evaluando un gran paso, asi "quedamos en el mismo punto"
		pos_big,vel_big=rk4(p,v, tiempo_actual, tau,m,n)

		#Se calculan los errores con los promedios y se obtienen los ratios de error.
		#Si alguno es cero se le asigna eps (valor pequeño), si no lanzaría error mas adelante.
		eps = 1.0e-16
		errores=[]
		for i in Range(n):
			for j in Range(3):
				scalex = adaptErr*(abs(pos[i][j])+abs(pos_big[i][j]))/2.0
				scalev=adaptErr*(abs(vel[i][j])+abs(vel_big[i][j]))/2.0
				error_truncax = vel[i][j]-vel_big[i][j]
				error_truncav = pos[i][j]-pos_big[i][j]
				ratiox = abs(error_truncax)/(scalex+eps)
				ratiov= abs(error_truncav)/(scalev+eps)
				if ratiox==0.0:
					ratiox=eps
				if ratiov==0.0:
					ratiov=eps
				#Guardamos todos los errores y seleccionamos el máximo (asi todo es mas preciso)
				errores.append(ratiox)
				errores.append(ratiov)
			ratio=max(errores)
		
	#Estimamos el nuevo valor de tau (incluyendo factores de seguridad)
			tau_ant= tau
			#Imprimimos el ratio de error, asi se tiene control de cuantas veces itera y los errores conseguidos
			print "ratio"+str(ratio)
			tau = safe1*tau_ant*pow(ratio,-0.20)
			if tau < tau_ant/safe2 :
				tau=tau_ant/safe2
			elif tau > safe2*tau_ant :
				tau=safe2*tau_ant
			else:
				tau=tau
			#Si se supera el paso maximo, se usa este mismo
			if tau>pasomaximo:
				tau=pasomaximo
		#Si el error es aceptable se devuelvo las nuevas posiciones, velocidades, el nuevo tiempo y el paso usado.
			if ratio < 1 :
				return pos,vel,tiempo_actual+tau,tau 
	else:
		print "Error: Runge-Kutta adaptativo fallo"
		exit()

def update(num, dataLines, lineas, pts):	
    for line,pt, data in zip(lineas, pts, dataLines):	
        # NOTE: there is no .set_data() for 3 dim data...	
        x,y=data[0:2, :num]	
        z=data[2, :num]	
        line.set_data(x,y)	
        line.set_3d_properties(z)	
        pt.set_data(x[-1:],y[-1:])	
        pt.set_3d_properties(z[-1:])	

    return lineas+pts


