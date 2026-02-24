# -*- coding: utf-8 -*-

from rdkit import Chem
from google.colab import files
uploaded=files.upload()

import pandas as pd

df=pd.read_csv('full qGC dataset.csv')

df=df[['Molecule ChEMBL ID','Smiles','pChEMBL Value']]
df=df.dropna()

df = df.groupby('Molecule ChEMBL ID').agg({
    'Smiles': 'first',
    'pChEMBL Value': 'mean'
}).reset_index()

df = df.drop_duplicates(subset='Molecule ChEMBL ID', keep='first').reset_index(drop=True)
df = df.sort_values(by='pChEMBL Value', ascending=True).reset_index(drop=True)


def is_salt(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    frags = Chem.GetMolFrags(mol)
    return len(frags) > 1

df["is_salt"] = df["Smiles"].apply(is_salt)

df


# SCAFFOLD
import pandas as pd
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold
from collections import defaultdict
import random
def generate_scaffold(smiles, include_chirality=False):
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        scaffold = MurckoScaffold.GetScaffoldForMol(mol)
        return Chem.MolToSmiles(scaffold, isomericSmiles=include_chirality)
    except:
        return None

def scaffold_split(df, smiles_col='Smiles', frac_train=0.8, frac_val=0.1, frac_test=0.1, seed=42):

    assert (frac_train + frac_val + frac_test) > 0.99 and (frac_train + frac_val + frac_test) < 1.01

    df['scaffold'] = df[smiles_col].apply(generate_scaffold)

    df = df.dropna(subset=['scaffold']).reset_index(drop=True)

    scaffolds = defaultdict(list)
    for i, scaffold in enumerate(df['scaffold']):
        scaffolds[scaffold].append(i)

    scaffold_list = list(scaffolds.values())
    random.seed(seed)
    random.shuffle(scaffold_list)

    n_total = len(df)
    n_train = int(frac_train * n_total)
    n_val = int(frac_val * n_total)

    # Phân chia chỉ số vào các tập
    train_idx, val_idx, test_idx = [], [], []

    for group in scaffold_list:
        if len(train_idx) + len(group) <= n_train:
            train_idx.extend(group)
        elif len(val_idx) + len(group) <= n_val:
            val_idx.extend(group)
        else:
            test_idx.extend(group)

    df_train = df.iloc[train_idx].drop(columns=['scaffold'])
    df_val = df.iloc[val_idx].drop(columns=['scaffold'])
    df_test = df.iloc[test_idx].drop(columns=['scaffold'])

    return df_train, df_val, df_test

df_train, df_val, df_test = scaffold_split(
    df,
    smiles_col='Smiles',
    frac_train=0.8,
    frac_val=0.1,
    frac_test=0.1
)


def summarize_pchembl(df, name):
    print(f"\n{name}")
    print("N =", len(df))
    print(df["pChEMBL Value"].describe())

summarize_pchembl(df_train, "TRAIN")
summarize_pchembl(df_val,   "VAL")
summarize_pchembl(df_test,  "TEST")


train_filename = 'train_scaffold_split.csv'
val_filename = 'validation_scaffold_split.csv'
test_filename = 'test_scaffold_split.csv'

df_train.to_csv(train_filename, index=False)
df_val.to_csv(val_filename, index=False)
df_test.to_csv(test_filename, index=False)
