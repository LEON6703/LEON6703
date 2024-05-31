import pandas as pd
import xlsx_path

directory = xlsx_path.getting_xlsx()

def imp_csv(status, filepath):
    data = {}   
    get_column_key = pd.read_excel(filepath,skiprows=2,nrows=0,)
 
    count_rows = get_column_key.shape[1]
   
    for column in range(count_rows):
        data[get_column_key.columns[column]] = pd.read_excel(filepath, skiprows=2, usecols=[column]).iloc[:, 0].tolist()
      
    #print(data) #Reines debugging
    return data[status][0]


def extract_acl_dest_values(filepath):

     
    # Lese die Spaltennamen der Excel-Datei ein
    column_names = pd.read_excel(filepath, skiprows=2, nrows=0).columns

    # Initialisiere einen leeren String, um die Werte der acl_dest-Spalten zu speichern
    acl_dest_values_string = ""
    
    # Iteriere über die Spaltennamen und extrahiere die Werte der acl_dest-Spalten
    for column_name in column_names:
        # Überprüfe, ob der Spaltenname dem Format "aclx_dest" entspricht
        if column_name.startswith("acl") and column_name.endswith("_dest"):
            # Extrahiere die Zahl "x" aus dem Spaltennamen
            try:
                x = int(column_name[3])  # Die Ziffer folgt nach "acl"
                if 1 <= x <= 5:  # Überprüfe, ob x im Bereich von 1 bis 5 liegt
                    # Lies die Werte der Spalte aus der Excel-Datei und füge sie zum String hinzu
                    acl_dest_values_string += f"ACL {x}:    "
                    values = pd.read_excel(filepath, skiprows=2, usecols=[column_name]).iloc[0].tolist()
                  
                    acl_dest_values_string += "\n".join(map(str, values))+ "\n"
            except ValueError:
                pass  # Wenn die Ziffer nicht extrahiert werden kann, überspringe sie
    
    return acl_dest_values_string

extract_acl_dest_values(directory)
