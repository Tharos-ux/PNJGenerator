from tensorflow.keras import models, layers, utils, backend as K
import matplotlib.pyplot as plt
import shap

model = models.Sequential(name="GeNoms",layers=[layers.Dense(name="Dense",imput_dim=3,units=1,activation='linear')])
model.summary()