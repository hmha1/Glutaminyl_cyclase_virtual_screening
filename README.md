# Deep learning for QC inhibitor prediction
A hybrid deep learning framework for pIC50 regression using:
- Transformer-based molecular embeddings (ChemBERTa)
- Morgan fingerprints (ECFP4)
- Feature fusion with deep neural network

 ##  Computational Workflow

The workflow integrates deep learning screening with structure-based validation to identify potential QC inhibitors.

1. Deep learning prediction
A hybrid ChemBERTa + Morgan fingerprint model predicts pIC50 values. Compounds with predicted pIC50 > 7 are selected.

2. Molecular docking
Selected compounds are docked to the QC enzyme to evaluate binding affinity.

3. ADME filtering
Drug-likeness and pharmacokinetic properties are assessed using Lipinski’s rule, BBB permeability, and ADME analysis.

4. Molecular dynamics simulation
Top candidates are validated through MD simulations by analyzing RMSD, RMSF, SASA, and radius of gyration.

<p align="center">
  <img src="image/figure workflow.png" width="600"><br>
  <em>Figure 1. Integrated deep learning and structure-based workflow for QC inhibitor identification.</em>
</p> 


## Dataset 
The training pipeline expects three CSV files:
`train.csv`
`validation.csv`
`test.csv`
Each file must contain the following columns:
- Smiles
- pChEMBL Value
### Example 
| Smiles | pChEMBL Value |
|----------|----------|
| CCOc1ccc2nc(S(N)(=O)=O)sc2c1  | 7.52 |
| CN1CCN(CC1)C2=NC3=CC=CC=C3N2| 6.84|
  
## Model architecture 
The proposed model is a hybrid regression framework that combines transformer-based embeddings and Morgan fingerprint features, both generated from SMILES strings. The architecture includes a transformer branch, a fingerprint branch, and a fusion regression head for pIC50 prediction.

<p align="center">
  <img src="image/model_architecture.png" width="600"><br>
  <em>Figure 2. Hybrid ChemBERTa and ECFP4 fingerprint model architecture.</em>
</p> 

### Transformer Branch
- Pretrained model: `seyonec/ChemBERTa-zinc-base-v1`
- Maximum sequence length: 128
- CLS token embedding extracted
- Multilayer perceptron: `2048 → 1024 → 512` (512-dimensional feature)
### Fingerprint Branch
- Morgan fingerprint (ECFP4)
- Radius = 2
- 2048-bit 
- Multilayer perceptron: `2048 → 1024 → 512` (512-dimensional feature)
### Fusion and Regression Head
## Fusion and Regression Head

The 512-dimensional transformer feature and the 512-dimensional fingerprint feature are concatenated into a 1024-dimensional vector. This fused representation is passed through a fully connected regression network:

`1024 → 512 → 256 → 128 → 1`

`Dropout = 0.2` and ReLU activation functions are applied between layers.  
The final output layer produces a single continuous value corresponding to the predicted pIC50.

## Training Configuration

- **Batch size:** 16  
- **Epochs:** 50  
- **Loss function:** Mean Squared Error (MSE)  
- **Optimizer:** AdamW  
- **Learning rate:** 1e-3  
- **Weight decay:** 0.01  
- **Scheduler:** Cosine schedule with 10% warmup  
- **Model selection:** Best model selected based on lowest validation RMSE

## How to Run
Place the dataset CSV files in the same directory as `train.py`, then run:
python `train.py`

