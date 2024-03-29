import time
import json
import pandas as pd
import streamlit as st
from frictionless import validate
from frictionless import Schema
from mapping import ogdNbr_mapping
from urllib.request import urlopen


# function to perform quality check
def perform_quality_check(frame, file_name):

    MAX_RETRIES = 2
    DELAY_SECONDS = 1

    try:

        if file_name in ogdNbr_mapping:

            # get OGD# from the mapping file to load the correct datapackage
            ID = ogdNbr_mapping[file_name]
            datapackage_url = f"https://www.uvek-gis.admin.ch/BFE/ogd/{ID}/datapackage.json"

            # fetching datapackage with retry logic
            attempts = 0
            while attempts < MAX_RETRIES:
                try:
                    response = urlopen(datapackage_url)
                    
                    if response.getcode() == 200:
                        datapackage = response.read().decode('utf-8')
                        # load datapackage
                        datapackage_json = json.loads(datapackage)
                        
                        uploaded_file_schema = None

                        # find schema corresponding to uploaded file (some datapackages contain schemas for multiple files)
                        for resource in datapackage_json.get('resources', []):

                            if 'path' in list(resource.keys()) and file_name in resource['path']:
                                uploaded_file_schema = resource['schema']
                                break


                        if uploaded_file_schema:

                            # pandas has no dtype 'year' --> so it is changed to 'integer'
                            for field in uploaded_file_schema['fields']:
                                if field['type'] == 'year':
                                    field['type'] = 'integer'

                            # convert dictionary schema into frictionless schema object
                            schema = Schema(uploaded_file_schema)

                        
                            # change the data type of the first column to 'float' if all dtypes are 'int'
                            # for some reason, if all dtypes of frame are 'int', it throws an error even if the CSV is valid
                            # to escape that, change the type of the first column
                            if all(frame.dtypes == 'int64'):
                                frame.iloc[:, 0] = frame.iloc[:, 0].astype(float)

                            # perform validation using schema matched to uploaded file
                            report = validate(frame, schema=schema)
                            
                            return report

                        return f"No schema found for the uploaded file '{file_name}' in the datapackage."

                except Exception as e:
                    print(f"Error fetching datapackage: {e}")

                attempts += 1
                # exponential backoff delay
                time.sleep(DELAY_SECONDS * attempts)  

            return f"Failed to fetch datapackage after multiple attempts."

        else:
            return f"There is no datapackage for the file '{file_name}' "

    except Exception as e:
        return f"Error during validation: {e}"


# get cleaner error messages
def get_error_messages(report):

    text = ''
    
    for err in report.tasks[0].errors:
        text = text + err.title + ':\n' + err.message + '\n\n'

    return text



#-------------------------------------------------------------------------------
# translation dictionaries
translations = {
    "Deutsch": {
        "title": "CSV-Qualitätsprüfung mit Frictionless",
        "upload": "Laden Sie eine CSV-Datei hoch",
        "uploaded_success": "Datei erfolgreich hochgeladen!",
        "check_button": "Überprüfen",
        "error": "Fehler während der Validierung:",
        "validation_complete": "Validierung abgeschlossen!",
        "valid": "Das Dokument ist gültig.",
    },
    "Français": {
        "title": "Contrôle de qualité CSV avec Frictionless",
        "upload": "Télécharger un fichier CSV",
        "uploaded_success": "Fichier téléchargé avec succès !",
        "check_button": "Vérifier",
        "error": "Erreur de validation:",
        "validation_complete": "Validation terminée !",
        "valid": "Le document est valide.",
    },
    "Italiano": {
        "title": "Controllo qualità CSV con Frictionless",
        "upload": "Caricare un file CSV",
        "uploaded_success": "File caricato con successo!",
        "check_button": "Controllo",
        "error": "Errore durante la validazione:",
        "validation_complete": "Validazione completata!",
        "valid": "Il documento è valido.",
    },
    "English": {
        "title": "CSV Quality Check with Frictionless",
        "upload": "Upload a CSV file",
        "uploaded_success": "File uploaded successfully!",
        "check_button": "Check",
        "error": "Error during validation:",
        "validation_complete": "Validation complete!",
        "valid": "The document is valid.",
    }
}
#-------------------------------------------------------------------------------

# function for changing language
def set_language(language):
    st.session_state.language = language

# main function
def main():
    # default language German
    if "language" not in st.session_state:
        st.session_state.language = "Deutsch"

    # language selection dropdown
    selected_language = st.sidebar.selectbox("Select Language", list(translations.keys()), index=list(translations.keys()).index(st.session_state.language))
    set_language(selected_language)

    # display content based on selected language
    translation = translations[st.session_state.language]

    # set title
    st.title(translation["title"])

    # create upload element
    uploaded_file = st.file_uploader(translation["upload"], type=["csv"])

    if uploaded_file is not None:
        st.write(translation["uploaded_success"])

        dataframe = pd.read_csv(uploaded_file, sep='[;,]', engine='python', skip_blank_lines=False)
        st.write(dataframe)
        if st.button(translation["check_button"]):
            progress_bar = st.progress(0)
            report = perform_quality_check(dataframe, uploaded_file.name)

            if isinstance(report, str):
                st.error(f"{translation['error']} {report}")
            else:
                # file is valid
                if report.valid:
                    st.success(translation["validation_complete"])
                    st.success(translation["valid"])
                # file is not valid
                else:
                    st.error(translation["validation_complete"])
                    st.error(get_error_messages(report))

if __name__ == "__main__":
    main()
