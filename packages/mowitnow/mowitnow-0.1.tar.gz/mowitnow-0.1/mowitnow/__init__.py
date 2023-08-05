#! /usr/local/Cellar/python
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
    Xavier RUIZ <XRUIZ@externe.generali.fr>

HISTORY
    0.01 XRU 12/10/2018 Versoion initiale
"""

import argparse
import os

# Fonction de récupération des arguments
def get_arguments():

	parser = argparse.ArgumentParser(
		prog='MowItNow_Controller',
		description='Controle un ensemble de tondeuses MowItNow.')

	# Argument contenant le path complet du fichier de controle
	parser.add_argument(
		'-f', '--file',
		required=True,
		help='Path complet du fichier dentree du programme contenant les instructions de controle.')

	return parser.parse_args()

# Main
if __name__ == '__main__':
	args = get_arguments()
	strtest="test"
	print (strtest)
