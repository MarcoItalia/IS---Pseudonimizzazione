import os

def delete_file(filepath):
    # Cancella il file se esiste
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Dataset '{filepath}' cancellato.")
    else:
        print(f"Dataset '{filepath}' non trovato, nessuna cancellazione eseguita.")
