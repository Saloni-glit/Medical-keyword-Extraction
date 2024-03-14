# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tMIFKrgTewLYp1jSEeQ8F3UwfsbZzFFv
"""

import numpy as np # linear algebra
import pandas as pd



import os
for dirname, _, filenames in os.walk('/content'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import os

current_directory = os.getcwd()
print("Current Working Directory:", current_directory)

import pandas as pd
import numpy as np


# Read the CSV file
df = pd.read_csv('https://raw.githubusercontent.com/Saloni-glit/Medical-dataset/main/mtsamples.csv')

print(df.columns)

!pip install simpletransformers

from simpletransformers.classification import ClassificationModel, ClassificationArgs
import simpletransformers

"""# Understanding the Python Code

## Libraries and Imports

The code begins by importing essential libraries for data manipulation and machine learning tasks. It includes `pandas` for data handling, `os` and `sys` for system operations, and various modules from `sklearn` for metrics and data splitting. Additionally, it imports classes from the `simpletransformers` library, including `ClassificationModel`.
"""

import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from os.path import join
from sklearn.metrics import f1_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split

from simpletransformers.classification import ClassificationModel, ClassificationArgs
import sklearn

import torch

"""# Checking Directory Contents and Setting Data Path

This section begins by inspecting the current directory's contents and initializing the data path variable.


"""

# Checking Directory Contents and Setting Data Path
print(os.listdir())

datapath = "data"

"""
# GPU Availability Check

This part checks whether a GPU is available for training the model using PyTorch.
"""

cuda_available = torch.cuda.is_available()

"""# Evaluation Metrics Function

Defines a function to calculate balanced accuracy and F1 score, essential metrics for classification tasks.
"""

def eval_metrics(actual, pred):
    bal_acc = balanced_accuracy_score(actual,pred)
    f1_sc = f1_score(actual,pred,average="micro")
    return bal_acc, f1_sc

"""# Data Loading and Preprocessing Function

This function reads and preprocesses medical transcriptions data from a CSV file, adeptly handling class imbalances and encoding labels.

"""

def data_loader(filename):
    df = pd.read_csv('https://raw.githubusercontent.com/Saloni-glit/Medical-dataset/main/mtsamples.csv')
    df.drop(['Unnamed: 0'],axis=1,inplace=True)

    counts = df['medical_specialty'].value_counts()
    others = [k for k,v in counts.items() if v<100]
    for each_spec in others:
        df.loc[df['medical_specialty']==each_spec,'medical_specialty']=' others'

    counts = df['medical_specialty'].value_counts()
    print(counts)

    num_classes = len(df['medical_specialty'].unique())
    class_dict = dict(zip(df['medical_specialty'].unique(),list(range(num_classes))))
    df['medical_specialty'] = df['medical_specialty'].apply(lambda x:class_dict[x])
    df.dropna(inplace=True)
    df['transcription'] = df['keywords']+df['transcription']
    X = df[['transcription']]
    y = df[["medical_specialty"]]


    train_x,test_x,train_y,test_y = train_test_split(X,y, stratify=y,test_size=0.25)

    # class_weights = sklearn.utils.class_weight.compute_class_weight("balanced",list(set(list(y.values))),list(y.values))
    class_weights = [1]*num_classes

    print(df.head())

    return train_x, train_y, test_x, test_y, num_classes, class_weights, class_dict

"""# Main Execution Block

In the main block, the data loading function is called, and the training and testing datasets are meticulously prepared.

# Creating DataFrames

Pandas DataFrames are crafted for training and testing data, meticulously structured for seamless integration with the `ClassificationModel`.

---

# Setting Hyperparameters

This step involves setting crucial hyperparameters such as the learning rate and the number of training epochs.

---

# Model Configuration

The `ClassificationModel` is meticulously configured using the specified hyperparameters.

---

# Initializing and Training the Model

The RoBERTa-based classification model is initialized and undergoes rigorous training using the prepared datasets.

---

# Saving the Trained Model

The trained model is elegantly saved for future use.

---

# Model Evaluation

The model is evaluated on the test dataset, yielding results, model outputs, and insights into misclassifications.

---

# Making Predictions

The trained model flexes its capabilities, making predictions on the test data with precision.

---

# Evaluating Metrics on Predictions

Accurate assessment of model performance is achieved by calculating balanced accuracy and F1 score on the predictions.

---

# Displaying Results

The culmination of the process is highlighted by showcasing the final evaluation metrics with clarity.

---
"""

if __name__ == '__main__':
    train_x,train_y,test_x,test_y, num_classes, class_weights, class_dict = data_loader("https://raw.githubusercontent.com/Saloni-glit/Medical-dataset/main/mtsamples.csv")

    train_df = pd.DataFrame(columns=['text','labels'])
    train_df['text'] = train_x['transcription']
    train_df['labels'] = train_y['medical_specialty']
    print(train_df.head())
    test_df = pd.DataFrame(columns=['text','labels'])
    test_df['text'] = test_x['transcription']
    test_df['labels'] = test_y['medical_specialty']


    learning_rate = 1e-5
    num_of_epochs = 3

    model_args = ClassificationArgs(num_train_epochs=num_of_epochs,learning_rate = learning_rate,  reprocess_input_data= True,save_model_every_epoch=False, overwrite_output_dir= True)

    model = ClassificationModel(
        "roberta",
        "roberta-base",
        num_labels=num_classes,
        weight=class_weights,
        use_cuda=cuda_available,
        args=model_args
        )

    model.train_model(train_df)
    model.save_model()
    result, model_outputs, wrong_predictions = model.eval_model(test_df)




    result,output = model.predict(test_df['text'].values.tolist())



    acc, f1 = eval_metrics(test_df['labels'],result)

    print(acc,f1)

test_df.to_csv("test_df.csv")

saved_model = ClassificationModel(
    "roberta", "/content/outputs"
)

result,output = saved_model.predict(test_df['text'].values.tolist())
acc, f1 = eval_metrics(test_df['labels'],result)
print(acc,f1)

output

output[1]



