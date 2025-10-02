import random
import math
import numpy as np

from const import SBOX, invSBOX, hw256, T, N
from bruit_gaussien import double_gauss

# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def simulation():
    """
    Cette fonction retourne la clé utilisée dans la simulation et les observations bruitées correspondantes
    """
    Observation_bruite=[]
    K=list(range(256))
    k=random.choice(K) #clé générée aléatoirement

    for t in range(T):
        
        m=np.random.randint(0,255) #m généré aléatoirement suivant une loi uniforme
        x=m^k
        y=invSBOX[x]
        obs=(hw256[m],hw256[y])

        # bruits gaussiens :
        bruit_g_1=double_gauss() 
        bruit_g_2=double_gauss() 

        # mesures bruitées du poids de Hamming 
        obs_1=hw256[m]+bruit_g_1
        obs_2=hw256[y]+bruit_g_2

        observation_bruite=(obs_1, obs_2)
        Observation_bruite.append(observation_bruite) #stocke les couples de poids de Hamming (hm,hy) 
        
    return (k, Observation_bruite)


def calcul_proba(distrib_hw_bruitee, k):
    """
    Cette fonction retourne la probabilité P(k|(h_m,h_y)) 
    """
    proba_cle_sachant_couple = 0
    for h_m_obs, h_y_obs in distrib_hw_bruitee:
        Somme=0
        for m in range(256):
            x=m^k
            y=invSBOX[x]

            calcul_hm= h_m_obs-hw256[m]
            calcul_hy= h_y_obs-hw256[y]

            partie1=(1/math.sqrt(2 * math.pi))*math.exp(-(1/2)*calcul_hm**2)
            partie2=(1/math.sqrt(2 * math.pi))*math.exp(-(1/2)*calcul_hy**2)
            bruite_sachant_vrai= partie1*partie2
            Somme+=bruite_sachant_vrai

        proba_cle_sachant_couple += math.log(Somme / 256)
        
    return proba_cle_sachant_couple


def retrouver_cle(Observation_bruite):
    #on initialise a -inf et -1 car ce sont des valeurs inatteignables pour MV et clé resp.
    meilleure_proba=float('-inf')
    k_meilleur_proba=-1
    
    for k in range(256):
        score_actuel=calcul_proba(Observation_bruite, k)
        if score_actuel > meilleure_proba:
            meilleure_proba = score_actuel
            k_meilleur_proba = k
    
    return (k_meilleur_proba, meilleure_proba)


def exploitation(N):
    succes = 0
    print("Nombre de traces:", T, "Nombres d'attaques: ", N)
    for n in range(N):
        k_reel, observations = simulation()
        k_estime, meilleure_proba = retrouver_cle(observations)
        if k_estime == k_reel:
            succes += 1
            resultat = f"{bcolors.OKGREEN}(Succès){bcolors.ENDC}"
        else:
            resultat = f"{bcolors.FAIL}(Echec){bcolors.ENDC}"
        
        print(f"[{n+1}/{N}] Clé réelle: {k_reel}; Estimée: {k_estime} {resultat}")
    print(f"\nTaux de succès : {succes}/{N} : {round(succes / N, 2)*100} %")

if __name__ == "__main__":
    np.random.seed(3)
    random.seed(3)
    exploitation(N)