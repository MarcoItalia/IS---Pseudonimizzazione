import pandas as pd
import uuid
import hashlib
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import base64
import os
#from utils_delete import delete_file


SALT = "123"
KEY_PATH = 'aes/key.txt'

# Step 2: Cifra i dati identificativi e genera il patient_id
def generate_patient_id_aes(input_path, output_path):
    df = pd.read_csv(input_path)

    # Salva la chiave solo se non esiste già
    if not os.path.exists(KEY_PATH):
        key = base64.urlsafe_b64encode(SALT.ljust(32, '0').encode())
        os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
        with open(KEY_PATH, 'wb') as f:
            f.write(key)
    else:
        with open(KEY_PATH, 'rb') as f:
            key = f.read()

    cipher = Fernet(key)

    # Concatena i valori da cifrare
    columns_to_encrypt = ['nome', 'cognome', 'data_di_nascita', 'codice_fiscale', 'sesso', 'cap', 'data_di_diagnosi']
    def aes_row(row):
        values = [str(row[col]) for col in columns_to_encrypt]
        concat = '|'.join(values)
        token = cipher.encrypt(concat.encode('utf-8'))
        return token.decode('utf-8')

    df['patient_id'] = df.apply(aes_row, axis=1)

    # Tieni solo le colonne cliniche e il patient_id
    clinical_columns = ['diagnosi', 'tipo_diagnosi', 'data_di_diagnosi', 'trattamento', 'ospedale', 'reparto']
    output_df = df[['patient_id'] + clinical_columns]
    #output_df = df[['patient_id'] + ['data_di_diagnosi']]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    output_df.to_csv(output_path, index=False)
    print(f'File pseudonimizzato con patient_id AES salvato in {output_path}')

# Generalizzata l'anno di diagnosi
def generate_pseudonymized_file(input_path, output_path):
    df = pd.read_csv(input_path)
    # Generalizza la data al solo anno
    df['data_di_diagnosi'] = pd.to_datetime(df['data_di_diagnosi'], errors='coerce').dt.year
    df.to_csv(output_path, index=False)
    print(f'File speudonimizzato salvato in {output_path}')

# Esecuzione completa
if __name__ == "__main__":
    input_file = 'dataset_pazienti.csv'
    output_file = 'aes/dataset_pazienti_pseudonimizzato_aes.csv'

    generate_patient_id_aes(input_file, output_file)
    generate_pseudonymized_file(output_file, output_file)

    # Cancella il file dei dati originali
    #delete_file(input_file)
