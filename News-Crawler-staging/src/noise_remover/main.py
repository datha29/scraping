import sys,os
from os import path
sys.path.append(os.path.abspath('./..'))
from src.noise_remover.recognise_noise_patterns import NoiseRemoval


noise= NoiseRemoval()
noise.identitfy_noise_pattern()