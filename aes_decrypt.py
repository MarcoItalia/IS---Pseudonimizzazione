import pandas as pd
from cryptography.fernet import Fernet
import os

# Colonne originali cifrate in ordine
columns_to_decrypt = ['nome', 'cognome', 'data_di_nascita', 'codice_fiscale', 'sesso', 'cap', 'data_di_diagnosi']

# Colonne cliniche mantenute nel CSV pseudonimizzato
clinical_columns = ['diagnosi', 'tipo_diagnosi', 'trattamento', 'ospedale', 'reparto']

def load_key(key_path):
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Chiave AES non trovata in '{key_path}'")
    with open(key_path, 'rb') as f:
        return f.read()

def decrypt_patient_ids(input_file, output_file, key_path):
    # Carica il file CSV pseudonimizzato
    df = pd.read_csv(input_file)
    # Crea oggetto Fernet per la decifratura
    cipher = Fernet(load_key(key_path))

    # Funzione per decifrare ogni token della colonna patient_id
    def decrypt_token(token):
        try:
            # Decifra il token e separa i campi originali
            return cipher.decrypt(token.encode()).decode().split('|')
        except Exception as e:
            print(f"Errore decifrando token: {e}")
            # In caso di errore, restituisce una riga di errori
            return ['ERRORE'] * len(columns_to_decrypt)

    # Applica la decifratura a tutta la colonna patient_id
    decrypted_data = df['patient_id'].apply(decrypt_token).tolist()
    # Crea un nuovo DataFrame con i dati decifrati
    df_decrypted = pd.DataFrame(decrypted_data, columns=columns_to_decrypt)
    # Aggiunge le colonne cliniche (se presenti nel file)
    for col in clinical_columns:
        if col in df.columns:
            df_decrypted[col] = df[col]
    # Salva il risultato su file
    df_decrypted.to_csv(output_file, index=False)
    print(f'Tabella ricostruita salvata in {output_file}')

if __name__ == "__main__":
    key_path = 'aes/key.txt'
    input_file = 'aes/dataset_pazienti_pseudonimizzato_aes.csv'
    output_file = 'aes/dataset_pazienti_ripristinato.csv'
    decrypt_patient_ids(input_file, output_file, key_path)
