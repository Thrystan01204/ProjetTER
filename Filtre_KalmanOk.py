from numpy import dot
from numpy import dot, sum, tile, linalg
from numpy.linalg import inv,det 
import numpy as np
import math

class Filtre_Kalman:
    #initialisation
    def __init__(self,cx,cy,w,h,dt,Y):        #cx la position en abscisse de l'objet
        #cy la position en ordonnÃ©e, x la largeur, h la hauteur, dt la diffÃ©rence de temps
        #entre chaque image
        #la matrice MM qui stocke 5 valeurs mesurÃ©es
        self.Y=Y
        self.X=np.array([[cx],[cy],[w],[h]])        #matrice des positions moyennes de l'objet Ã  l'instant t
        self.P=np.diag((0.01, 0.01, 0.01, 0.01))                 #matrice des valeurs covariantes de l'objet Ã  l'instant t                                    
        self.Q=np.eye(4)*0.001           #matrice de bruit de la camÃ©ra (incertitudes)
        self.dt=dt                  #le temps entre chaque image
        self.A=np.array([[1, 0, dt , 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0,1]])   #matrice A de transition qui va calculer les futures valeurs
        self.B = np.eye(np.shape(np.array([cx,cy,w,h]))[0])     
        self.U = np.zeros((np.shape(np.array([cx,cy,w,h]))[0],1))

        #initialisation de matrices de mesures
        self.H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]]) 
        self.R= np.eye(np.shape(Y)[0])

    #fonction qui calcule les valeurs moyennes prÃ©dictives de l'objet 
    def kf_predict(self):
        self.X = dot(self.A,self.X) + dot(self.B, self.U)
        self.P = dot(self.A, dot(self.P, self.A.T)) + self.Q
        return(self.X,self.P)
    def gauss_pdf(self,X, M, S):
        if np.shape(M)[1] == 1:
            DX = X - tile(M, np.shape(X)[1])
            E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
            E = E + 0.5 * np.shape(M)[0] * np.log(2 * math.pi) + 0.5 * np.log(det(S))
            P = np.exp(-E)
        elif np.shape(X)[1] == 1:
            DX = tile(X, np.shape(M)[1])- M
            E = 0.5 * sum(DX * (dot(inv(S), DX)), axis=0)
            E = E + 0.5 * np.shape(M)[0] * np.log(2 * math.pi) + 0.5 * np.log(det(S))
            P = np.exp(-E)
        else:
            DX = X-M
            E = 0.5 * dot(DX.T, dot(inv(S), DX))
            E = E + 0.5 *np.shape(M)[0] * np.log(2 * math.pi) + 0.5 * np.log(det(S))
            P = np.exp(-E)
        return (P[0],E[0])

    #fonction qui dÃ©termine les positions futures Ã  l'instant t+1
    def kf_update(self,X, P, Y, H, R):
        self.IM = dot(self.H, self.X)
        self.IS = R + dot(H, dot(P, H.T))
        self.K = dot(P, dot(H.T, inv(self.IS)))
        self.X = X + dot(self.K, (Y-self.IM))
        self.P = P - dot(self.K, dot(self.IS, (self.K).T))
        self.LH = self.gauss_pdf(Y, self.IM, self.IS)
        return (self.X,self.P,self.K,self.IM,self.IS,self.LH)
    #fonction qui calcule les valeurs probables de l'objet avec la mÃ©thode de Gauss
    
    def main(self,n):   #n le nombre d'itÃ©rations
        nb_col=np.shape(self.Y)[0]
        try:
            nb_raw=np.shape(self.Y)[1]
        except:
            nb_raw=0
        i=1
        Y=self.Y[i:nb_col]
        
    # Number of iterations in Kalman Filter
        N_iter = n
        #Application du filtre de Kalman
        for i in range(0, N_iter):
            (self.X, self.P) = self.kf_predict()
            (self.X, self.P, self.K, self.IM, self.IS, self.LH) = self.kf_update(self.X, self.P, Y, self.H, self.R)
            i=i+1
            Y=self.Y[i:nb_col]
            
    def main_test(self):
        self.Y = np.array([[self.X[0,0] + abs(np.random.randn(1)[0])], [self.X[1,0] +abs(np.random.randn(1)[0])]])
        self.H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
        self.R = np.eye(np.shape(self.Y)[0])
        # Number of iterations in Kalman Filter
        N_iter = 50
        # Applying the Kalman Filter
        for i in range(0, N_iter):
            (self.X, self.P) = self.kf_predict()
            (self.X, self.P, self.K, self.IM, self.IS, self.LH) = self.kf_update(self.X, self.P, self.Y, self.H, self.R)
            self.Y = np.array([[self.X[0,0] + abs(0.1 * np.random.randn(1)[0])],[self.X[1, 0] +abs(0.1 * np.random.randn(1)[0])]]) 
# Ã  chaque instant t, pour pouvoir prÃ©dire les futures positions de l'objet

#1) initialiser la matrice de mesures des positions de l'objet Y
#Y  la matrice qui dÃ©termine les positions mesurÃ©es Ã  chaque instant t


#On rÃ©cupÃ¨re alors la matrice des valeurs moyennes des positions M et
#de covariances S
#LH les valeurs prÃ©dictives probables (probabilitÃ©s) 



