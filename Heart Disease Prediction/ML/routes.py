import warnings
import pandas as pd
from flask import render_template,url_for,Blueprint,redirect
from flask import Flask, render_template, request, Response,url_for
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
from ml.utils import AlgoForm
from sklearn.model_selection import train_test_split


warnings.filterwarnings('ignore')
route =Blueprint('ml',__name__)
df = pd.read_csv('ml/static/ecg.csv')
for i in range(len(df)):
    if df.iloc[i,4] == 'F':
        df.iloc[i,4] = 0
    else:
        df.iloc[i,4] = 1
        
    if df.iloc[i,5]=='Yes':
        df.iloc[i,5] = 1
    else:
        df.iloc[i,5] = 0
        
    if df.iloc[i,6] == '(B':
        df.iloc[i,6] = 1
    elif df.iloc[i,6] == '(T':
        df.iloc[i,6] = 2
    elif df.iloc[i,6] == '(VT':
        df.iloc[i,6] = 3
    elif df.iloc[i,6] == '(N':
        df.iloc[i,6] = 0

x=df[df.columns[~df.columns.isin(["arrhythmia"])]].to_numpy()
y=df.arrhythmia.to_numpy()
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2)




    
@route.route("/", methods=['GET','POST'])
def predict():

    print("working")
    form  = AlgoForm()
    if form.validate_on_submit():
        if form.Medicine.data=='Yes':
            form.Medicine.data = 1
        else:
            form.Medicine.data = 0
        if form.Sex.data=='MALE':
            form.Sex.data = 1
        else:
            form.Sex.data = 0
        X_values=[form.amlitude.data,form.RR.data,form.speed.data,form.Age.data,form.Sex.data,form.Medicine.data]
        KNN_Reg = KNeighborsRegressor(leaf_size = 1, n_neighbors = 2, p = 1)
        KNN_Reg.fit(x_train, y_train)
        final_features = [np.array(X_values)]
        predictedArrhythmia=KNN_Reg.predict(final_features)
        Arrhythmia = ''
        Discription = ''
        predictedArrhythmia[0] = round(predictedArrhythmia[0])
        if predictedArrhythmia[0]==0.0:
            Arrhythmia = 'No Problems'
            Discription = ''
        elif predictedArrhythmia[0]==1.0:
            Arrhythmia = 'Bradycardia'
            Discription = 'Slow heart rhythms(with a rate below 60 beats per minute) that may be caused by disease in the heart’s conduction system, such as the sinoatrial (SA) node, atrioventricular (AV) node or HIS-Purkinje network'
        elif predictedArrhythmia[0]==2.0:
            Arrhythmia = 'Tachycardia'
            Discription = 'A fast heart rhythm with a rate of more than 100 beats per minute.'
        elif predictedArrhythmia[0]==3.0:
            Arrhythmia =  'Ventricular arrhythmias'
            Discription = 'Arrhythmias that begin in the ventricles (the heart’s lower chambers).'
        else:
            Arrhythmia = 'No idea'
            Discription =''
        return render_template('analysis.html',Arrhythmia = Arrhythmia,Discription =Discription)
    return render_template("predict.html", form=form)



      
    
    

  

