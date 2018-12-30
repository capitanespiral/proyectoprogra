#!/usr/bin/python
#-*- coding:utf-8 -*-

class cuerpo:
	#m masa (acepta float), v velocidad (acepta lista, origen en el cuerpo en si, definida cartesiana), p posición (acepta lista, definida de forma polar)
	def __init__(self,p,m,v)
		#agregar metodo que p cambie en función de v
		self.p=p
		#radio y ángulo de "órbita", del origen (centro estrellita) al cuerpo
		self.r=float(p[0])
		self.ang=float(p[1])
		#masa
		self.m=float(m)
		#velocidad y sus componentes
		self.v=v
		self.vx=v[0]
		self.vy=v[1]
		#Momentum lineal
		self.mom=[self.m*self.vx,self.m*self.vy]
		#self.R=? -> agregar radio del cuerpo (tamaño) en función de su masa
