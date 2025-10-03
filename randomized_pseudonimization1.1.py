import pandas as pd
import uuid
from datetime import datetime
#from utils_delete import delete_file

# Genera patient_id casuale e salva la tabella di corrispondenze
def generate_patient_id(input_path, output_path):
    df = pd.read_csv(input_path)
    unique_fiscal_codes = df['codice_fiscale'].unique()
    fiscal_code_to_id = {cf: str(uuid.uuid4()) for cf in unique_fiscal_codes}
    df['patient_id'] = df['codice_fiscale'].map(fiscal_code_to_id)

    # Salva tabella delle corrispondenze
    columns_to_keep = ['codice_fiscale', 'patient_id', 'nome', 'cognome', 'cap', 'data_di_nascita', 'sesso', 'data_di_diagnosi']
    df[columns_to_keep].to_csv(output_path, index=False)
    print(f'codice_fiscale → patient_id salvata in {output_path}')

    return df  

# Crea dataset pseudonimizzato finale (solo clinico + patient_id)
def generate_pseudonymized_file(df_with_id, output_path):
    clinical_columns = ['diagnosi', 'tipo_diagnosi', 'data_di_diagnosi', 'trattamento', 'ospedale', 'reparto']
    
    # Solo le colonne cliniche + patient_id
    df_clinical = df_with_id[['patient_id'] + clinical_columns].copy()
    
    # Generalizza la data della diagnosi → solo anno
    df_clinical['data_di_diagnosi'] = pd.to_datetime(df_clinical['data_di_diagnosi'], errors='coerce').dt.year

    df_clinical.to_csv(output_path, index=False)
    print(f'File clinico pseudonimizzato con anno della diagnosi salvato in {output_path}')

# Esecuzione
if __name__ == "__main__":
    input_file = 'dataset_pazienti.csv'
    lookup_output = 'randomized/lookup.csv'
    output_file = 'randomized/dataset_pazienti_pseudonimizzato_randomized.csv'

    df_with_patient_id = generate_patient_id(input_file, lookup_output)
    generate_pseudonymized_file(df_with_patient_id, output_file)

    # Cancella il file dei dati originali
    #delete_file(input_file)
