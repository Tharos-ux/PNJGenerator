from tensorflow.keras import models, layers, utils, backend as tfk
import matplotlib.pyplot as plt
import tensorflow as tf
import shap
import plot_ann as vz

"""
model_naive = models.Sequential(name="GeNoms", layers=[
    layers.Dense(             # layer totalement connecté
          name="dense",
          input_dim=3,        # 3 entrées
          units=1,            # 1 sortie
          activation='linear' # def : f(x)=x on peut remplacer par le nom d'une fonction
    )
])
model_naive.summary()
"""

n_features = 4
model = models.Sequential(name="DeepGeNoms", layers=[
    ### couche cachée 1
    layers.Dense(name="h1", input_dim=n_features,
                 units=int(round((n_features+1)/2)), 
                 activation='relu'),
    layers.Dropout(name="drop1", rate=0.2),
    
    ### couche cachée 2
    layers.Dense(name="h2", units=int(round((n_features+1)/4)), 
                 activation='relu'),
    layers.Dropout(name="drop2", rate=0.2),
    
    ### couche de sortie
    layers.Dense(name="output", units=1, activation='sigmoid')
])
# model.summary() # permet d'afficher le modèle

vz.visualize_nn(model)

# exemple de fonction d'activation, laissée ici pour se souvenir du format de retour
def binary_step_activation(x):
    # 1 si x>0 sinon 0 
    return tfk.switch(x>0, tf.math.divide(x,x), tf.math.multiply(x,0))