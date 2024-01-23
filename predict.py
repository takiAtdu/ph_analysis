import pickle

model = 'model_reg.sav'


loaded_model = pickle.load(open(model, 'rb'))
result = loaded_model.score(X_test, Y_test)
print(result)