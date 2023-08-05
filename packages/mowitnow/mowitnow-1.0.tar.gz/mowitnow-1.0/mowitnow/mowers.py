#!/usr/local/bin/python3.7
# -*- coding: cp1252 -*-

# Classe : field - qui decrit le terrain sur lequel les tondeuses vont evoluer
class field:
	'Delimitation du terrain de 0,0 à x,y.'
	min_x = 0
	min_y = 0

	# Constructor field
	def __init__(self,valXY):
		field.max_x = int(valXY[0])
		field.max_y = int(valXY[1])

	# Fonction d affichage des attributs
	def displayBorders(self):
		print("Terrain : (", self.min_x,",", self.min_y,") (", self.max_x,",", self.max_y,")\n")

# Classe mowSwarm - qui decrit un ensemble de tondeuses
class mowSwarm:
	swarm = []

	# Constructor mowSwarm
	def __init__(self):
		pass

	# Ajoute une tondeuse a l essaim de tondeuses
	def addMow(self, mow):
		self.swarm.append(mow)

	# Fonction d'affichage de l essaim
	def displaySwarm(self):
		for num,mow in enumerate(self.swarm):
			print("Essaim - Tondeuse ", num , "- Position :")
			mow.displayPos()

# Classe mower - qui decrit la position initale de la tondeuse, sa position apres mouvement l action de mouvement
class mower:
	'Position de la tondeuse : x,y,orientation.'

	# Constructor mower
	def __init__(self,field,num,posXYA):
		# num of the mower
		self.num=num
		# x abscisse
		self.posX=int(posXYA[0])
		# y ordonnee
		self.posY=int(posXYA[1])
		# A orientation N,E,W,S
		self.posA=posXYA[2]

	def __getitem__(self,key):
		return self

	# Fonction d affichage des attributs
	def displayPos(self):
		print("Mower ",self.num ," Position : (", self.posX,",", self.posY,",", self.posA,")\n")

	# Fonction de mouvement - Met a jour les attributs x,y,A de la tondeuse apres mouvement
	def moveMower(self,char):
		# Test - Avancer
		if char == "A":
			# Test - Bordures du terrain - Deplacement
			if self.posA == "N":
				if self.posY < field.max_y:
					# Deplacement selon y -> y+1
					self.posY+=1
			elif self.posA == "E":
				if self.posX < field.max_x:
					# Deplacement selon x -> x+1
					self.posX+=1
			elif self.posA == "W":
				if self.posX > field.min_x:
					# Deplacement selon x -> x-1
					self.posX-=1
			elif self.posA == "S":
				if self.posY > field.min_y:
					# Deplacement selon y -> y-1 
					self.posY-=1
		# Test - Rotation gauche selon position actuelle
		elif char == "G":
			if self.posA == "N":
				self.posA = "W"
			elif self.posA == "W":
				self.posA = "S"
			elif self.posA == "S":
				self.posA = "E"
			elif self.posA == "E":
				self.posA = "N"
		# Test - Rotation droite selon position actuelle
		elif char == "D":
			if self.posA == "N":
				self.posA = "E"
			elif self.posA == "E":
				self.posA = "S"
			elif self.posA == "S":
				self.posA = "W"
			elif self.posA == "W":
				self.posA = "N"
