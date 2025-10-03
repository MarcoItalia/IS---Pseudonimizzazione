import pandas as pd
import hashlib
from datetime import datetime
#from utils_delete import delete_file
SALT = "123"

# Genera hash pseudonimo da identificativi e salva tabella di corrispondenza
def generate_hashed_patient_ids(input_path, mapping_output_path):
    df = pd.read_csv(input_path)

    # Colonne su cui applicare l'hash
    columns_to_hash = ['codice_fiscale', 'nome', 'cognome', 'cap', 'data_di_nascita', 'sesso', 'data_di_diagnosi']

    def hash_row(row):
        values = [str(row[col]) for col in columns_to_hash]
        concat = '|'.join(values) + f"|{SALT}"
        return hashlib.sha256(concat.encode('utf-8')).hexdigest()

    # Applica hash
    df['patient_id'] = df.apply(hash_row, axis=1)

    # Salva la tabella di corrispondenza (non completamente anonima)
    df_out = df[['patient_id'] + columns_to_hash]
    df_out.to_csv(mapping_output_path, index=False)
    print(f'Tabella di corrispondenza salvata in {mapping_output_path}')

    return df  # ritorna il DataFrame con patient_id per lo step successivo

# Genera tabella pseudonimizzata (clinica) con solo patient_id e anno di diagnosi
def generate_pseudonymized_file(df_with_id, output_path):
    clinical_columns = ['diagnosi', 'tipo_diagnosi', 'data_di_diagnosi', 'trattamento', 'ospedale', 'reparto']

    # Mantieni solo patient_id + clinica
    df_clinical = df_with_id[['patient_id'] + clinical_columns].copy()
    df_clinical['data_di_diagnosi'] = pd.to_datetime(df_clinical['data_di_diagnosi'], errors='coerce').dt.year

    df_clinical.to_csv(output_path, index=False)
    print(f'File pseudonimizzato salvato in {output_path}')

# Esecuzione
if __name__ == "__main__":
    input_file = 'dataset_pazienti.csv'
    lookup_output = 'hashed/lookup.csv.csv'
    output_file = 'hashed/dataset_pazienti_pseudonimizzato_hashed.csv'

    df_with_hash = generate_hashed_patient_ids(input_file, lookup_output)
    generate_pseudonymized_file(df_with_hash, output_file)
    
    # Cancella il file dei dati originali
    #delete_file(input_file)