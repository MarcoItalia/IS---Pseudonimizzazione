import pandas as pd

# Percorsi dei file
lookup_file = 'randomized/lookup.csv'
pseudonymized_file = 'randomized/dataset_pazienti_pseudonimizzato_randomized.csv'
output_file = 'randomized/dataset_ripristinato.csv'

# Leggi i file CSV
lookup = pd.read_csv(lookup_file)
pseudonymized = pd.read_csv(pseudonymized_file)

# Tieni solo la prima occorrenza di ogni patient_id nel lookup
lookup = lookup.drop_duplicates(subset=['patient_id'])

# Seleziona solo le colonne di lookup che NON sono già in pseudonymized
cols_to_add = [col for col in lookup.columns if col not in pseudonymized.columns or col == 'data_di_diagnosi']

# Fai il merge partendo dal file pseudonimizzato
merged = pd.merge(
    lookup[["patient_id"] + cols_to_add],
    pseudonymized,
    on='patient_id',
    how='left'
)

# Rimuovi la colonna 'patient_id'
merged = merged.drop(columns=['patient_id'])

# Rimuovi eventuali duplicati (dovrebbero già essere unici ora)
merged = merged.drop_duplicates()

# Salva il risultato su un nuovo file
merged.to_csv(output_file, index=False)