#!/usr/bin/env python
# coding: utf-8

# import pandas as pd
# 
# model_data = pd.read_csv("Fake_Freelancer_Profiles_Exact_Pay.csv")
# model_data

# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# 
# 
# model_data['Location'] = le.fit_transform(model_data['Location'])
# model_data['Industry'] = le.fit_transform(model_data['Industry'])
# 
# model_data

# import numpy as np
# 
# x = model_data.drop(['Pay'], axis = 1)
# y = model_data['Pay']
# x = np.array(x).astype('float32')
# y = np.array(y).astype('float32')

# from sklearn.model_selection import train_test_split
# X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size = 0.30)

# !pip install "sagemaker>=2.15.0"
# !pip install boto3

# import sagemaker
# 
# sagemaker_session = sagemaker.Session()
# bucket = "market-analysis-sagemaker-pragnya"
# prefix = "linear-learner"
# 
# role = sagemaker.get_execution_role()
# print(role)

# import io 
# import sagemaker.amazon.common as smac 
# import os
# import boto3
# 
# buf = io.BytesIO()
# smac.write_numpy_to_dense_tensor(buf, X_train, Y_train)
# buf.seek(0) 
# 
# key = 'linear-train-data'
# #Upload training data to S3
# boto3.resource('s3').Bucket(bucket).Object(os.path.join(prefix, 'train', key)).upload_fileobj(buf)
# s3_train_data = 's3://{}/{}/train/{}'.format(bucket, prefix, key)
# print('uploaded training data location: {}'.format(s3_train_data))
# 
# 
# buf = io.BytesIO() 
# smac.write_numpy_to_dense_tensor(buf, X_test, Y_test)
# buf.seek(0)
# 
# #Upload test data to S3
# key = 'linear-test-data'
# boto3.resource('s3').Bucket(bucket).Object(os.path.join(prefix, 'test', key)).upload_fileobj(buf)
# s3_test_data = 's3://{}/{}/test/{}'.format(bucket, prefix, key)
# print('uploaded training data location: {}'.format(s3_test_data))
# 
# output_location = 's3://{}/{}/output'.format(bucket, prefix)
# print('Training artifacts will be uploaded to: {}'.format(output_location))

# from sagemaker.amazon.amazon_estimator import image_uris
# container = image_uris.retrieve('linear-learner', boto3.Session().region_name)
# 
# linear = sagemaker.estimator.Estimator(container,
#                                        role, 
#                                        instance_count = 1, 
#                                        instance_type = 'ml.c4.xlarge',
#                                        output_path = output_location,
#                                        sagemaker_session = sagemaker_session)

# linear.set_hyperparameters(feature_dim = 4,
#                            predictor_type = 'regressor',
#                            mini_batch_size = 30,
#                            epochs = 4,
#                            #num_models = 10,
#                            loss = 'absolute_loss')

# linear.fit({'train': s3_train_data})

# linear_regressor = linear.deploy(initial_instance_count = 1,
#                                           instance_type = 'ml.m4.xlarge')
# print("1")
# 
# from sagemaker.predictor import csv_serializer, json_deserializer
# linear_regressor.serializer = csv_serializer
# linear_regressor.deserializer = json_deserializer
# print("2")

# import matplotlib.pyplot as plt
# 
# result = linear_regressor.predict(X_test)
# result #should be a JSON
# 
# #Iterate the result JSON to get an NP array of all the predictions so we can compare to Y test
# predictions = np.array([res['score'] for res in result['predictions']])
# predictions #should now be an numpy array
# 
# #Visualize how accurate predictions are relative to y_test
# plt.scatter(y_test, predictions)

# In[ ]:





# In[54]:


import pandas as pd

model_data = pd.read_csv("Fake_Freelancer_Profiles_Exact_Pay.csv")
model_data


# In[55]:


from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()


model_data['Location'] = le.fit_transform(model_data['Location'])
model_data['Industry'] = le.fit_transform(model_data['Industry'])

model_data.fillna(method ='ffill', inplace = True)


model_data


# In[56]:


import numpy as np

x = model_data.drop(['Pay'], axis = 1)
y = model_data['Pay']
x = np.array(x).astype('float32')
y = np.array(y).astype('float32')


# from sklearn.model_selection import train_test_split
# X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size = 0.30)

# from sklearn.preprocessing import StandardScaler
# 
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# from sklearn.linear_model import LinearRegression 
# 
# regr = LinearRegression() 
#   
# regr.fit(X_train, Y_train) 
# print(regr.score(X_test, Y_test)) 

# print(f"X_test shape: {X_test.shape}")
# print(f"Y_test shape: {Y_test.shape}")

# plt.scatter(X_test[:, 0], Y_test, color='b', label='Actual')  # Use the first feature
# plt.plot(X_test[:, 0], regr.predict(X_test), color='k', label='Predicted')
# plt.legend()
# plt.show()
# 

# from sklearn.metrics import mean_absolute_error,mean_squared_error 
#   
# mae = mean_absolute_error(y_true=Y_test,y_pred=Y_pred) 
# #squared True returns MSE value, False returns RMSE value. 
# mse = mean_squared_error(y_true=Y_test,y_pred=Y_pred) #default=True 
# rmse = mean_squared_error(y_true=Y_test,y_pred=Y_pred,squared=False) 
#   
# print("MAE:",mae) 
# print("MSE:",mse) 
# print("RMSE:",rmse)

# In[66]:


get_ipython().system('pip install xgboost')


# In[67]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor

# Simulate dataset (replace with your own dataset)
np.random.seed(42)
X = np.random.rand(200, 4)  # 200 samples, 4 features
y = np.random.rand(200) * 10  # 200 target values

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features for models that require scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Dictionary to store results
results = {}

# Define a function to train and evaluate models
def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results[name] = {"MSE": mse, "R²": r2}
    print(f"{name}:\n  MSE: {mse:.4f}\n  R²: {r2:.4f}\n")

# 1. Linear Regression
evaluate_model("Linear Regression", LinearRegression(), X_train, X_test, y_train, y_test)

# 2. Ridge Regression
evaluate_model("Ridge Regression", Ridge(alpha=1.0), X_train_scaled, X_test_scaled, y_train, y_test)

# 3. Lasso Regression
evaluate_model("Lasso Regression", Lasso(alpha=0.1), X_train_scaled, X_test_scaled, y_train, y_test)

# 4. ElasticNet Regression
evaluate_model("ElasticNet Regression", ElasticNet(alpha=0.1, l1_ratio=0.5), X_train_scaled, X_test_scaled, y_train, y_test)

# 5. Decision Tree Regression
evaluate_model("Decision Tree Regression", DecisionTreeRegressor(max_depth=5, random_state=42), X_train, X_test, y_train, y_test)

# 6. Random Forest Regression
evaluate_model("Random Forest Regression", RandomForestRegressor(n_estimators=100, random_state=42), X_train, X_test, y_train, y_test)

# 7. Gradient Boosting Regression
evaluate_model("Gradient Boosting Regression", GradientBoostingRegressor(n_estimators=100, random_state=42), X_train, X_test, y_train, y_test)

# 8. Support Vector Regression (SVR)
evaluate_model("Support Vector Regression", SVR(kernel='rbf', C=1.0), X_train_scaled, X_test_scaled, y_train, y_test)

# 9. XGBoost Regression
evaluate_model("XGBoost Regression", XGBRegressor(n_estimators=100, random_state=42, verbosity=0), X_train, X_test, y_train, y_test)

# Print all results
print("\nSummary of Results:")
for model, metrics in results.items():
    print(f"{model}: MSE={metrics['MSE']:.4f}, R²={metrics['R²']:.4f}")


# In[68]:


get_ipython().system('pip install modelbit')


# In[69]:


import modelbit
mb = modelbit.login()


# In[70]:


# import random

# def predict_weather(days_from_now: int):
#   prediction = random.choice(["sunny", "cloudy", "just right"])
#   return {
#     "weather": prediction,
#     "message": f"In {days_from_now} days it will be {prediction}!"
#   }

# mb.deploy(predict_weather)


# In[79]:


from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Train the model once
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

def my_model_deployment(input_data):
    """
    Predicts the target variable for a given input dictionary using a pre-trained RandomForestRegressor model.

    Parameters:
    - input_data (dict): A dictionary with a key 'data' containing a list of 4 numerical features.

    Returns:
    - float: Predicted value if input is valid.
    - None: If input is invalid.
    """
    # Extract 'data' key from the input dictionary
    if "data" in input_data:
        input_x = input_data["data"]
        
        # Validate input_x
        if len(input_x) == 4:
            return model.predict([input_x])[0]
        else:
            raise ValueError("The 'data' key must contain a list or array with exactly 4 numerical features.")
    else:
        raise ValueError("Input must be a dictionary with a 'data' key.")


mb.deploy(my_model_deployment, python_packages=["scikit-learn==1.5.2"])


# In[ ]:




