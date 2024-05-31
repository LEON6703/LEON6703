import os
import pathlib
import glob
import sys

def getting_xlsx():

    current_directory  = str(pathlib.Path().parent.absolute()) + "\data"

    excel_files = glob.glob(os.path.join(current_directory, "*.xlsx"))

    if excel_files:
        directory = excel_files[0]  # Verwende die erste gefundene Excel-Datei
        return directory
    else:
        print("Keine Excel-Datei im aktuellen Verzeichnis gefunden.")
        sys.exit()
    
    
