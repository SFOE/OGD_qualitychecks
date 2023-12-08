import streamlit as st
from frictionless import validate
from mapping import ogdNbr_mapping


# function to perform quality check
def perform_quality_check(file):
    try:
        report = validate(file)
        return report
    except Exception as e:
        return f"Error during validation: {e}"

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
    },
    "Français": {
        "title": "Contrôle de qualité CSV avec Frictionless",
        "upload": "Télécharger un fichier CSV",
        "uploaded_success": "Fichier téléchargé avec succès !",
        "check_button": "Vérifier",
        "error": "Erreur de validation:",
        "validation_complete": "Validation terminée !",
    },
    "Italiano": {
        "title": "Controllo qualità CSV con Frictionless",
        "upload": "Caricare un file CSV",
        "uploaded_success": "File caricato con successo!",
        "check_button": "Controllo",
        "error": "Errore durante la validazione:",
        "validation_complete": "Validazione completata!",
    },
    "English": {
        "title": "CSV Quality Check with Frictionless",
        "upload": "Upload a CSV file",
        "uploaded_success": "File uploaded successfully!",
        "check_button": "Check",
        "error": "Error during validation:",
        "validation_complete": "Validation complete!",
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

    st.title(translation["title"])

    uploaded_file = st.file_uploader(translation["upload"], type=["csv"])

    if uploaded_file is not None:
        st.write(translation["uploaded_success"])
        if st.button(translation["check_button"]):
            progress_bar = st.progress(0)
            report = perform_quality_check(uploaded_file)

            if isinstance(report, str):
                st.error(f"{translation['error']} {report}")
            else:
                st.success(translation["validation_complete"])
                st.write(report)

if __name__ == "__main__":
    main()
