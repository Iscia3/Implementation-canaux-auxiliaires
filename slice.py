import random
import math
import numpy as np

from const import SBOX, invSBOX, hw256
from bruit_gaussien import double_gauss


def slice_methode(T=512):
    """
    Cette fonction retourne une liste de couples d'estimations (h_m, h_y).
    """
    obs_m=[]
    obs_y=[]
    h_m_estime=[]
    h_y_estime=[]
    Compte=[]
    couples = []
    K=list(range(256))

    assert T % 256 == 0 #on veut T multiple de 256 pour une répartition parfaite

    for t in range(T):
        k=random.choice(K) #clé générée aléatoirement
        m=np.random.randint(0,255) #m généré aléatoirement suivant une loi uniforme
        x=m^k
        y=SBOX[x]

        # bruits gaussiens :
        bruit_g_1=double_gauss() 
        bruit_g_2=double_gauss() 

        # mesures bruitées du poids de Hamming 
        obs_m.append(hw256[m]+bruit_g_1)
        obs_y.append(hw256[y]+bruit_g_2)

        obs_m_trie=sorted(obs_m)
        obs_y_trie=sorted(obs_y)
    
    #Générerattion des 8 poids de Hamming (Slice)
    for h in range(9): 
        k_parmi_n=math.comb(8, h)
        compte=(T/256)*k_parmi_n
        Compte.append(compte) #liste qui contient le nombre d'éléments par slice 
        
    h_m_estime= assigner_hw(obs_m_trie, Compte)
    h_y_estime= assigner_hw(obs_y_trie, Compte)

    #Constitution des couples
    hw_m = dict(zip(obs_m_trie, h_m_estime)) #constitue des couples :(obs_trie, hm_ estime)
    hw_y = dict(zip(obs_y_trie, h_y_estime))

    for t in range(T):
        hm = hw_m[obs_m[t]]
        hy = hw_y[obs_y[t]]
        couples.append((hm, hy))

    return(couples)

def assigner_hw(obs_trie, Compte):
    longueur=len(obs_trie)
    hw_estime=[0]*longueur
    index=0

    for h in range(9):
        compte=int(round(Compte[h]))
        for c in range(compte):
            if index < longueur: #permet de remplir les listes suivant les bonnes slice
                hw_estime[index]=h
                index+=1

    return(hw_estime)

if __name__ == "__main__":
    np.random.seed(3)
    random.seed(3)
    print(slice_methode())