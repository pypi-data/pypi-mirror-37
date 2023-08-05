#!/usr/bin/python2.7
# -*- coding: cp1252 -*-

"""
SYNOPSIS
    MowItNow_Controller.py [-h,--help] [-f,--file] [-v,--verbose]

DESCRIPTION
    Programme permettant de controler un ensemble de tondeuses MowItNow
    Specifications completes contenues dans le package - "ExerciceTechnique - La Tondeuse.pdf"

ARGUMENTS
    -h, --help			Show this help message and exit
    -f, --file			Path complet du fichier d'entree du programme contenant les instructions de controle	

AUTHOR
    Xavier RUIZ <ruiz.xvr@gmail.com>

GIT
	https://github.com/xavbyme/mowitnow.git

PYPI
	https://pypi.org/project/mowitnow

HISTORY
	0.03	XRU		13/10/2018	Corrections de la classe mower - Ajout de la classe mowSwarm - Factorisation
	0.02	XRU 	12/10/2018	Version fonctionnelle
    0.01 	XRU 	12/10/2018	Versoion initiale - Structure - Git - Deploiement Pypi.org
"""

# Impots
import argparse
import os
import sys
from copy import copy

# Fonction de parsing et récupération des arguments
def getArguments():

	parser = argparse.ArgumentParser(
		prog='MowItNow_Controller',
		description='Controle un ensemble de tondeuses MowItNow.')

	# Argument contenant le path complet du fichier de controle
	parser.add_argument(
		'-f', '--file',
		required=True,
		help='Nom du fichier dentree du programme contenant les instructions de controle.')

	return parser.parse_args()

# Parser sur les espaces et retour chariot
def parserSpace(stringSplit):
	stringWtoN = stringSplit.rstrip('\n')
	arrayWtoSpace = stringWtoN.split()
	return arrayWtoSpace

# Sortie en erreur avec affichage de l erreur
def errorExit(str):
	sys.exit(str)

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
		print "Terrain : (", self.min_x,",", self.min_y,") (", self.max_x,",", self.max_y,")\n"

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
			print "Essaim - Tondeuse ", num , "- Position :"
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
		print "Mower ",self.num ," Position : (", self.posX,",", self.posY,",", self.posA,")\n"

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

# Main
if __name__ == '__main__':
	
	# Recuperation des arguments
	args = getArguments()

	# Recuperation du path du fichier de controle
	filepath=args.file

	# Initialisation de l index de l array de tondeuses
	indMower = 0

	# Instanciation d un essaim de tondeuses
	essaimTondeuse = mowSwarm()

	# Test de presence du fichier
	if os.path.exists(filepath) is not True:
		errorExit("Erreur : Fichier de controle introuvable.")
	
	# Ouverture du fichier de controle
	fileController = open(filepath)

	# Lecture du fichier ligne a ligne
	for num, line in enumerate(fileController):
		# Parsing de la ligne extraite du fichier
		line = parserSpace(line)

		# Case ligne 0 - taille de la matrice
		if num == 0:
			# Construction d une instance de field
			terrain = field(line)
			# Affichage des caracteristiques du terrain
			terrain.displayBorders()
		
		# Case ligne 1 - position initiale de la tondeuse
		elif (num % 2) == 1:
			# Instanciation d une tondeuse
			tondeuse = mower(terrain,indMower,line)
			# Affichage de la position
			tondeuse.displayPos()

		# # Case ligne 2 - deplacement
		elif (num % 2) == 0:
		# 	# Lecture du string d instructions de mouvements de la tondeuse
			for ch in line[0]:
		# 		# Instruction de mouvement
				tondeuse.moveMower(ch)
		# 	Ajout d une tondeuse a l instance d essaim cree
			essaimTondeuse.addMow(tondeuse)
		# 	Incrementation de l indice necessaire a l array de tondeuses
			indMower+=1

	# Affichage de la position des tondeuses de l essaim
	essaimTondeuse.displaySwarm()



