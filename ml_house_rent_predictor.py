# -*- coding: utf-8 -*-
"""ML_House_Rent_Predictor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1plrj3Pvvb0Z-FzOsvwawrdy--caMPw1q

# Rent Price Prediction Case Study

  'Kaizen Property Solutions' is an innovative firm focused on providing data-driven insights for rental property management and investment. The company aims to enhance the rental decision-making process for landlords, tenants, and real estate investors through advanced analytical solutions.
  
Business Challenge:
    
  - In the dynamic rental market of Pune and Mumbai, accurately predicting rental prices is crucial for maximizing occupancy rates and optimizing rental income. However, property managers and landlords often face challenges in estimating rental prices due to various influencing factors, including property characteristics, location, and local market trends specific to these metropolitan areas.





Objective:
  - To tackle this challenge, 'Kaizen Property Solutions' is conducting a machine learning case study aimed at developing a predictive model for estimating rental prices based on a comprehensive dataset that includes the following features: house_type, house_size, location, city (specifically Pune and Mumbai), latitude, longitude, price, currency, numBathrooms, numBalconies, isNegotiable, priceSqFt, verificationDate, description, SecurityDeposit, and Status.
"""

from google.colab import drive
drive.mount('/content/Myfiles')

import pandas as pd
import numpy as np

pune=pd.read_csv('/content/Myfiles/MyDrive/Indian_housing_Pune_data.csv')
 mumbai=pd.read_csv('/content/Myfiles/MyDrive/Indian_housing_Mumbai_data.csv')

pune.head(1)

pune.shape

mumbai.head(1)

mumbai.shape



# Data Understanding and Quality issues
#house_type ->replace Floor to House


#house_size->remove , and sqft convert to numerical data


#location->Checking for spelling mistake in location

#City-> no problem
# latitude longitude --> drop
#Pirce-> no problem

# currency-> drop

#numBathrooms-> convert to int
# numnumBalconies
#	isNegotiable--> Yes,no

#Drop sqftprice

#Drop/use verification
#Discription - needs more research/drop it
#Deposit--> convert to numerical, replace nodeposit with zero.
#status--->No problem

df=pd.concat([pune,mumbai],ignore_index=True)

df.isna().sum() #checking missing values data

df.info()

# Creating function to clean housesize column
import re
def clean_House_Size(text):
  x = re.sub(',','',text)
  y = re.sub('sq ft','',x)
  return y.strip()

df['house_size']

df['house_size']=df['house_size'].apply(clean_House_Size).astype('int')

df['house_size']

text1 = df['description'].iloc[2]

text1

re.findall('[\d]+',text1)[2]#used in regular expressions (regex) to match strings that contain digits

# Dropping unnecessary col
df1 = df.drop(columns=['latitude','longitude','currency','priceSqFt','verificationDate','description'])

df1

"""**SecurityDeposit**"""

df1['SecurityDeposit']

def clean_Security_Deposit(text):
  return re.sub(',','',text)

df1['SecurityDeposit']=df1['SecurityDeposit'].apply(clean_Security_Deposit)

# change no Deposit to insert value for 0
df1['SecurityDeposit']=np.where(df1['SecurityDeposit']=='No Deposit',0,df1['SecurityDeposit'])

# changing data type object to int
df1['SecurityDeposit']=df1['SecurityDeposit'].astype('int')

df1['SecurityDeposit']

df1

"""**numBathrooms**"""

# check missing value
df1['numBathrooms'].isna().sum()

# filling missing value in 1
df1['numBathrooms'].fillna(1,inplace=True)

# changing data type
df1['numBathrooms']=df1['numBathrooms'].astype('int')

"""**numBalconies**"""

# checking missing value
df1['numBalconies'].isna().sum()

df1['numBalconies'].dtype

# changing data type
df1['numBalconies']=df1['numBalconies'].astype('object')

df1.groupby('numBalconies')['price'].median()

"""**Handle House Type**"""

text = df1['house_type'].head(1)[0]
text

text=text.strip()
text

def house_type_cleaning(text):
  text = text.strip()
  return re.sub(' ','_',text)

df1['house_type']=df1['house_type'].apply(house_type_cleaning)

df1['house_type']

# filling missing value for 1 and 2
import numpy as np

df1['numBalconies'] = np.where(df1['house_type'] == '2_BHK_Apartment',
                             df1['numBalconies'].fillna(1),
                             df1['numBalconies'].fillna(2))

df1

df['description']

df1['isNegotiable']=np.where(df1['isNegotiable']=='Negotiable','Yes','No')

df1.isna().sum()

"""**Exploratory Data Analysis(EDA)**"""

# to find shape of the data
df1.shape

df1.groupby('price')['house_type'].sum()

df1['house_type'].value_counts().plot(kind='barh')

"""**most of the house_types are of 1 ,2, 3 bhk an 1 RK apartments, will make another category for other house_types**"""

# to get columns of dataframe
df1.columns

df1['house_size']

import seaborn as sns
import matplotlib.pyplot as plt

sns.displot(df1['house_size'])
plt.xlim(0,3000)
plt.show

sns.boxplot(df['house_size'])
plt.show

"""**it seems that most of the houses having square feet area below 2000**

**There are outliers present in house_size**
"""

#to get summary stats
df1['house_size'].describe()

"""**almost 75% houses in data having area below 1180 sqfeets**

**Data is +vely skewed**

**Outliers are present in house_sizes**
"""

df1['location'].value_counts().sort_values(ascending=False).head(30).plot(kind='barh')

"""**most of the houses are from wagholi Area, we will take only those locations having count greater than 100**

**will make another cateory for others**
"""

df1.info()

df1

# City wise data
df1['city'].value_counts().plot(kind='bar')

# location vise data top 30
df1['location'].value_counts().sort_values(ascending=False).head(30).plot(kind='barh')

sns.displot(df1['price'])
plt.xlim(0,40000)

df1['price'].describe()

"""**Data is skewed**

**75% of houses having price below 25000**

**Outliers are present in data**
"""

df1['numBalconies'].value_counts().plot(kind='bar')

"""**most of the balconies 1 and 2**"""

df1['numBalconies'].describe()

df1['isNegotiable'].value_counts().plot(kind='pie',autopct='%0.0f%%')

"""**the data is rent is 88 per  no negotiable**

**the data rent is 12 per data is negotiablebold text**
"""

import matplotlib.pyplot as plt
sns.displot(df1['SecurityDeposit'])
plt.xlim(0,100000)

"""**50% houses do not required security deposit**

**50% houses having security deposit 20000 to 1000000**
"""

df1['SecurityDeposit'].describe()

df1['Status'].value_counts().plot(kind='pie',autopct='%0.1f%%')

"""**the data status is semi-furnished for 40 % data**

**the data status is unfornished for 36 % data**

**the data is status furnished for 22% data**
"""

df1['numBathrooms'].value_counts().plot(kind='pie',autopct="%0.f%%")

"""**97% houses having number of bathrooms 1 to 3**"""



"""**Bivariate Analysis**"""

df1.columns

#house and price
#Rent price for house type is significantly different
df1.groupby('house_type')['price'].median().plot(kind='barh')

"""**Rent price for house type is significantly different**"""

#house Size and price
sns.scatterplot(x=df1['house_size'],y=df1['price'])

"""**There is increasing trend between house_size and rent**"""

df1[['house_size','price']].corr()

"""**there is moderate level postive correlation between price and house_size**"""

#location and price
df1.groupby('location')['price'].median().head(30).plot(kind='barh')
plt.xlim(0,60000)

"""**rent is strongly depend on location**"""

#bathrooms and price
df1.groupby('numBathrooms')['price'].median().plot(kind='barh')

"""**number of bathrooms having singinificant impact on rent price**"""

# Balconies and price
df1.groupby('numBalconies')['price'].median().plot(kind='barh')

df1['numBalconies'].value_counts()

"""**# Apply anova excluding 5 and 6 balconies**"""

df1.groupby('isNegotiable')['price'].median().plot(kind='pie')

df1.columns

# securitydeposit and price
sns.scatterplot(x=df1['SecurityDeposit'],y=df1['price'])

"""**There is Positive correlation between price and security deposit**"""

#status and price
df1.groupby('Status')['price'].median().plot(kind='bar')

sns.heatmap(df1.corr(numeric_only=True),annot=True)





from sklearn.compose import ColumnTransformer   # Data preprocessing

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder # Encoding types


from sklearn.metrics import r2_score,mean_absolute_error  # Model evaulation metrics


from sklearn.linear_model import LinearRegression

from sklearn.neighbors import KNeighborsRegressor

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor,AdaBoostRegressor

from sklearn.svm import SVR

x=df1.drop(columns=['price'])
y=df1['price']

# train test split
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=2)

x_train['city'].value_counts()

x_train.head(1)

# Step 1: Column Transformer with encoding
step1 = ColumnTransformer(transformers=[
    ('tnf1', OneHotEncoder(sparse_output=False, categories='auto', handle_unknown='ignore'), [2, 3, 6]),
    ('tnf2', OrdinalEncoder(categories=[['1_RK_Studio_Apartment', '1_BHK_Apartment', '1_BHK_Independent_House',
                                         '1_BHK_Independent_Floor', '1_BHK_Villa', '2_BHK_Apartment',
                                         '2_BHK_Independent_House', '2_BHK_Independent_Floor', '2_BHK_Villa',
                                         '3_BHK_Apartment', '3_BHK_Independent_House', '3_BHK_Independent_Floor',
                                         '3_BHK_Villa', '4_BHK_Apartment', '4_BHK_Independent_House',
                                         '4_BHK_Independent_Floor', '4_BHK_Villa', '5_BHK_Apartment',
                                         '5_BHK_Independent_House', '5_BHK_Villa', '6_BHK_Apartment',
                                         '6_BHK_Independent_House', '6_BHK_Villa', '6_BHK_penthouse']],
                         handle_unknown='use_encoded_value', unknown_value=-1), [0]),
    ('tnf3', OrdinalEncoder(categories=[['Unfurnished', 'Semi-Furnished', 'Furnished']],
                            handle_unknown='use_encoded_value', unknown_value=-1), [8]),
], remainder='passthrough') # transform

# Step 2: Use Multiple Linear Regression instead of Gradient Boosting
step2 = LinearRegression()
# Create pipeline
pipe = Pipeline([
    ('step1', step1),
    ('step2', step2)
])

# Fit the pipeline to the training data
pipe.fit(x_train, y_train)
# Make predictions on the test data
y_pred = pipe.predict(x_test)
# Evaluate the model
print('R2 score:', r2_score(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))

y_pred

from sklearn.tree import DecisionTreeRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.metrics import r2_score, mean_absolute_error

# Step 1: Column Transformer with encoding
step1 = ColumnTransformer(transformers=[
    ('tnf1', OneHotEncoder(sparse_output=False, categories='auto', handle_unknown='ignore'), [2, 3, 6]),
    ('tnf2', OrdinalEncoder(categories=[['1_RK_Studio_Apartment', '1_BHK_Apartment', '1_BHK_Independent_House',
                                         '1_BHK_Independent_Floor', '1_BHK_Villa', '2_BHK_Apartment',
                                         '2_BHK_Independent_House', '2_BHK_Independent_Floor', '2_BHK_Villa',
                                         '3_BHK_Apartment', '3_BHK_Independent_House', '3_BHK_Independent_Floor',
                                         '3_BHK_Villa', '4_BHK_Apartment', '4_BHK_Independent_House',
                                         '4_BHK_Independent_Floor', '4_BHK_Villa', '5_BHK_Apartment',
                                         '5_BHK_Independent_House', '5_BHK_Villa', '6_BHK_Apartment',
                                         '6_BHK_Independent_House', '6_BHK_Villa', '6_BHK_penthouse']],
                         handle_unknown='use_encoded_value', unknown_value=-1), [0]),
    ('tnf3', OrdinalEncoder(categories=[['Unfurnished', 'Semi-Furnished', 'Furnished']],
                            handle_unknown='use_encoded_value', unknown_value=-1), [8]),
], remainder='passthrough')

# Step 2: Use Decision Tree Regressor
step2 = DecisionTreeRegressor()

# Create pipeline
pipe = Pipeline([
    ('step1', step1),
    ('step2', step2)
])

# Fit the pipeline to the training data
pipe.fit(x_train, y_train)

# Make predictions on the test data
y_pred = pipe.predict(x_test)

# Evaluate the model
print('R2 score:', r2_score(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))

# Step 1: Column Transformer with encoding
step1 = ColumnTransformer(transformers=[
    ('tnf1', OneHotEncoder(sparse_output=False, categories='auto', handle_unknown='ignore'), [2, 3, 6]),
    ('tnf2', OrdinalEncoder(categories=[['1_RK_Studio_Apartment', '1_BHK_Apartment', '1_BHK_Independent_House',
                                         '1_BHK_Independent_Floor', '1_BHK_Villa', '2_BHK_Apartment',
                                         '2_BHK_Independent_House', '2_BHK_Independent_Floor', '2_BHK_Villa',
                                         '3_BHK_Apartment', '3_BHK_Independent_House', '3_BHK_Independent_Floor',
                                         '3_BHK_Villa', '4_BHK_Apartment', '4_BHK_Independent_House',
                                         '4_BHK_Independent_Floor', '4_BHK_Villa', '5_BHK_Apartment',
                                         '5_BHK_Independent_House', '5_BHK_Villa', '6_BHK_Apartment',
                                         '6_BHK_Independent_House', '6_BHK_Villa', '6_BHK_penthouse']],
                         handle_unknown='use_encoded_value', unknown_value=-1), [0]),
    ('tnf3', OrdinalEncoder(categories=[['Unfurnished', 'Semi-Furnished', 'Furnished']],
                            handle_unknown='use_encoded_value', unknown_value=-1), [8]),
], remainder='passthrough')

# Step 2: Use Random Forest Regressor
step2 = RandomForestRegressor(n_estimators=100)
# Create pipeline
pipe = Pipeline([
    ('step1', step1),
    ('step2', step2)
])

# Fit the pipeline to the training data
pipe.fit(x_train, y_train)

# Make predictions on the test data
y_pred = pipe.predict(x_test)

# Evaluate the model
print('R2 score:', r2_score(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))

from sklearn.svm import SVR
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error
# Step 1: Column Transformer with encoding
step1 = ColumnTransformer(transformers=[
    ('tnf1', OneHotEncoder(sparse_output=False, categories='auto', handle_unknown='ignore'), [2, 3, 6]),
    ('tnf2', OrdinalEncoder(categories=[['1_RK_Studio_Apartment', '1_BHK_Apartment', '1_BHK_Independent_House',
                                         '1_BHK_Independent_Floor', '1_BHK_Villa', '2_BHK_Apartment',
                                         '2_BHK_Independent_House', '2_BHK_Independent_Floor', '2_BHK_Villa',
                                         '3_BHK_Apartment', '3_BHK_Independent_House', '3_BHK_Independent_Floor',
                                         '3_BHK_Villa', '4_BHK_Apartment', '4_BHK_Independent_House',
                                         '4_BHK_Independent_Floor', '4_BHK_Villa', '5_BHK_Apartment',
                                         '5_BHK_Independent_House', '5_BHK_Villa', '6_BHK_Apartment',
                                         '6_BHK_Independent_House', '6_BHK_Villa', '6_BHK_penthouse']],
                         handle_unknown='use_encoded_value', unknown_value=-1), [0]),
    ('tnf3', OrdinalEncoder(categories=[['Unfurnished', 'Semi-Furnished', 'Furnished']],
                            handle_unknown='use_encoded_value', unknown_value=-1), [8]),
], remainder='passthrough')

# Step 2: Use StandardScaler to scale features before applying SVR
step2_scaler = StandardScaler()

# Step 3: Use SVR
step3 = SVR(kernel='rbf')  # You can choose different kernels, like 'linear', 'poly', etc.

# Create pipeline
pipe = Pipeline([
    ('step1', step1),
    ('step2_scaler', step2_scaler),  # Apply scaling after encoding
    ('step3', step3)
])

# Fit the pipeline to the training data
pipe.fit(x_train, y_train)

# Make predictions on the test data
y_pred = pipe.predict(x_test)

# Evaluate the model
print('R2 score:', r2_score(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))

# Step 1: Column Transformer with encoding
step1 = ColumnTransformer(transformers=[
    ('tnf1', OneHotEncoder(sparse_output=False, categories='auto', handle_unknown='ignore'), [2, 3, 6]),
    ('tnf2', OrdinalEncoder(categories=[['1_RK_Studio_Apartment', '1_BHK_Apartment', '1_BHK_Independent_House',
                                         '1_BHK_Independent_Floor', '1_BHK_Villa', '2_BHK_Apartment',
                                         '2_BHK_Independent_House', '2_BHK_Independent_Floor', '2_BHK_Villa',
                                         '3_BHK_Apartment', '3_BHK_Independent_House', '3_BHK_Independent_Floor',
                                         '3_BHK_Villa', '4_BHK_Apartment', '4_BHK_Independent_House',
                                         '4_BHK_Independent_Floor', '4_BHK_Villa', '5_BHK_Apartment',
                                         '5_BHK_Independent_House', '5_BHK_Villa', '6_BHK_Apartment',
                                         '6_BHK_Independent_House', '6_BHK_Villa', '6_BHK_penthouse']],
                         handle_unknown='use_encoded_value', unknown_value=-1), [0]),
    ('tnf3', OrdinalEncoder(categories=[['Unfurnished', 'Semi-Furnished', 'Furnished']],
                            handle_unknown='use_encoded_value', unknown_value=-1), [8]),
], remainder='passthrough')

# Step 2: Use AdaBoost Regressor with DecisionTreeRegressor as base estimator
step2 = AdaBoostRegressor(estimator=DecisionTreeRegressor(), n_estimators=100)

# Create pipeline
pipe = Pipeline([
    ('step1', step1),
    ('step2', step2)
])
# Fit the pipeline to the training data
pipe.fit(x_train, y_train)
# Make predictions on the test data
y_pred = pipe.predict(x_test)
# Evaluate the model
print('R2 score:', r2_score(y_test, y_pred))
print('MAE:', mean_absolute_error(y_test, y_pred))

step1=ColumnTransformer(transformers=[('tnf1',OneHotEncoder(sparse_output=False,categories='auto',handle_unknown = 'ignore'),[2,3,6]),
('tnf2',OrdinalEncoder(categories = [['1_RK_Studio_Apartment', '1_BHK_Apartment', '1_BHK_Independent_House', '1_BHK_Independent_Floor', '1_BHK_Villa', '2_BHK_Apartment', '2_BHK_Independent_House', '2_BHK_Independent_Floor', '2_BHK_Villa', '3_BHK_Apartment', '3_BHK_Independent_House', '3_BHK_Independent_Floor', '3_BHK_Villa', '4_BHK_Apartment', '4_BHK_Independent_House', '4_BHK_Independent_Floor', '4_BHK_Villa', '5_BHK_Apartment', '5_BHK_Independent_House', '5_BHK_Villa', '6_BHK_Apartment', '6_BHK_Independent_House', '6_BHK_Villa', '6_BHK_penthouse']
],handle_unknown='use_encoded_value', unknown_value=-1),[0]),
('tnf3',OrdinalEncoder(categories=[['Unfurnished', 'Semi-Furnished', 'Furnished']
],handle_unknown='use_encoded_value', unknown_value=-1),[8]),
],remainder='passthrough')
step2 = GradientBoostingRegressor(n_estimators=500)
pipe = Pipeline([
('step1',step1),
('step2',step2)
])
pipe.fit(x_train,y_train)
y_pred = pipe.predict(x_test)
print('R2 score',r2_score(y_test,y_pred))
print('MAE',mean_absolute_error(y_test,y_pred))

import pickle
pickle.dump(df1,open('/content/dataf.pkl','wb'))
pickle.dump(pipe,open('/content/pipe1.pkl','wb'))

!pip install pandas==1.5.3

!pip install gradio

!pip install streamlit

import sklearn
import xgboost
print("Scikit-learn version:", sklearn.__version__)
print("XGBoost version:", xgboost.__version__)

import streamlit as st
import gradio as gr
import pickle
import numpy as np
import math
# Load your model and data
pipe = pickle.load(open('/content/pipe1.pkl', 'rb'))
dataf = pickle.load(open('/content/dataf.pkl', 'rb'))
def predict_rent_price(house_type, house_size, location, city, numBathrooms,
       numBalconies, isNegotiable, SecurityDeposit, Status):
    query = np.array([house_type, house_size, location, city, numBathrooms,
       numBalconies, isNegotiable, SecurityDeposit, Status])
    query = query.reshape(1, 9)
    prediction = pipe.predict(query)[0]
    return round(prediction)
# Define the inputs and outputs for the Gradio interface
inputs = [
    gr.Dropdown(choices=dataf['house_type'].unique().tolist(), label="House Type"),
    gr.Number(label="House Size in Sqft"),
    gr.Dropdown(choices=dataf['location'].unique().tolist(), label="Location"),
    gr.Dropdown(choices=dataf['city'].unique().tolist(), label="City"),
    gr.Number(label="Number of Bathrooms"),
    gr.Number(label="Number of Balconies"),

    gr.Dropdown(choices=dataf['isNegotiable'].unique().tolist(), label="IsNegotiable"),
    gr.Number(label="SecurityDeposit"),
    gr.Dropdown(choices=dataf['Status'].unique().tolist(), label="Status"),]
outputs = gr.Textbox(label="Predicted Price")
# Create and launch the Gradio interface
gr.Interface(fn=predict_rent_price, inputs=inputs, outputs=outputs, title="House Rent Prediction ").launch(debug=True)

