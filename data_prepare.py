# Import Libraries
import os
import pandas as pd


# Configurations
FILE_PATH = os.listdir('Datasets/Full')
dataset = []
label_dict = {"aquaculture": 0, "barrenland": 1, "crop": 2, "forest": 3, "grassland": 4, "residential": 5, "rice": 6,
              "scrub": 7, "water": 8}

# Read Excel File
for file in FILE_PATH:
    df = pd.read_excel('Datasets/Full/' + file, engine='openpyxl')
    df["label"].replace(label_dict, inplace=True)
    dataset.append(df)

# Shuffle, Split Datasets into Train, Evaluation, and Test
data = pd.concat(dataset, ignore_index=True)
data = data.sample(frac=1).reset_index(drop=True)
idx_train = int(data.shape[0] / 100 * 60)
idx_eval = int(data.shape[0] / 100 * 80)
train_data = data[0:idx_train]
eval_data = data[idx_train + 1:idx_eval]
test_data = data[idx_eval + 1:]

# Export Prepared Datasets
train_data.to_excel('Datasets/Train/Train.xlsx', index=False)
eval_data.to_excel('Datasets/Train/Evaluate.xlsx', index=False)
test_data.to_excel('Datasets/Train/Test.xlsx', index=False)
