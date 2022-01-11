# Import Libraries
import numpy as np
import pandas as pd
import xgboost as xgb


# Read Excel File
train_data = pd.read_excel('Datasets/Train/Train.xlsx', engine='openpyxl')
eval_data = pd.read_excel('Datasets/Train/Evaluate.xlsx', engine='openpyxl')
test_data = pd.read_excel('Datasets/Train/Test.xlsx', engine='openpyxl')

# Prepare Datasets
train_label = train_data['label'].values
train_data = train_data.loc[:, ['Band_1', 'Band_2', 'Band_3', 'Band_4', 'Band_5',
                                'Band_6', 'Band_7']]
eval_label = eval_data['label'].values
eval_data = eval_data.loc[:, ['Band_1', 'Band_2', 'Band_3', 'Band_4', 'Band_5',
                              'Band_6', 'Band_7']]
test_label = test_data['label'].values
test_data = test_data.loc[:, ['Band_1', 'Band_2', 'Band_3', 'Band_4', 'Band_5',
                              'Band_6', 'Band_7']]

# Make Dataset as XGBoost Matrices
dtrain = xgb.DMatrix(train_data, label=train_label, missing=np.nan)
deval = xgb.DMatrix(eval_data, label=eval_label, missing=np.nan)

# Declare Parameters
param = {'max_depth': 2, 'eta': 0.3, 'objective': 'multi:softmax', 'nthread': 4,
         'num_class': 9, 'shuffle': True}
evallist = [(deval, 'eval'), (dtrain, 'train')]
num_round = 100

# Training
bst = xgb.train(param, dtrain, num_round, evallist)

# Save Model
bst.save_model('Models/best.model')

# Testing
dtest = xgb.DMatrix(test_data)
labelpred = bst.predict(dtest)
print('=' * 100)
print("Prediction Accuracy: " + str(int(np.sum(labelpred == test_label) / labelpred.shape[0] * 100)) + " %")

# Calculate F1 Board for Debug
F1_board = np.zeros((9, 9))
for i in range(len(labelpred)):
    a = int(labelpred[i])
    F1_board[test_label[i]][a] += 1

# Calculate Scores
score = np.ones(9)
for i in range(9):
    score[i] = F1_board[i][i]/(np.sum(F1_board[i]))

# Debug Print
print('=' * 100)
print('Score = ')
print(score)
print('=' * 100)
print('F1_board = ')
print(F1_board)
print('=' * 100)
