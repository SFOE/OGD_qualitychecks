import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from frictionless import validate
from flask import Flask

# flask server setup
server = Flask(__name__)
app = dash.Dash(server=server, suppress_callback_exceptions=True)
app.title = 'CSV-Quality'
server = app.server

# Translation dictionaries
translations = {
    "Deutsch": {
        "title": "CSV-Qualitätsprüfung mit Frictionless",
        "upload": "Laden Sie eine CSV-Datei hoch",
        "uploaded_success": "Datei erfolgreich hochgeladen!",
        "error": "Fehler während der Validierung:",
        "validation_complete": "Validierung abgeschlossen!",
    },
    "Français": {
        "title": "Contrôle de qualité CSV avec Frictionless",
        "upload": "Télécharger un fichier CSV",
        "uploaded_success": "Fichier téléchargé avec succès !",
        "error": "Erreur de validation:",
        "validation_complete": "Validation terminée !",
    },
    "Italiano": {
        "title": "Controllo qualità CSV con Frictionless",
        "upload": "Caricare un file CSV",
        "uploaded_success": "File caricato con successo!",
        "error": "Errore durante la validazione:",
        "validation_complete": "Validazione completata!",
    },
    "English": {
        "title": "CSV Quality Check with Frictionless",
        "upload": "Upload a CSV file",
        "uploaded_success": "File uploaded successfully!",
        "error": "Error during validation:",
        "validation_complete": "Validation complete!",
    }
}

# Initialize the Dash app
app.layout = html.Div([
    html.H1(id='app-title'),
    dcc.Dropdown(
        id='language-dropdown',
        options=[{'label': lang, 'value': lang} for lang in translations.keys()],
        value="Deutsch",
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV File'),
        multiple=False
    ),
    html.Div(id='output-message'),
    html.Div(id='output-report')
])


# Function to perform quality check
def perform_quality_check(file):
    try:
        report = validate(file)
        return report
    except Exception as e:
        return f"Error during validation: {e}"


# Define callbacks to update the content based on user interaction
@app.callback(
    [Output('app-title', 'children'),
     Output('upload-data', 'children'),
     Output('output-message', 'children'),
     Output('output-report', 'children')],
    [Input('language-dropdown', 'value'),
     Input('upload-data', 'contents')]
)
def update_content(selected_language, contents):
    # Determine which input triggered the callback
    input_id = dash.callback_context.triggered_id
    translation = translations[selected_language]

    if input_id == 'language-dropdown.value':
        return translation["title"], html.Button(translation["upload"]), '', ''
    elif input_id == 'upload-data.contents':
        # Rest of your logic for file upload
        try:
            report = perform_quality_check(contents)
            if isinstance(report, str):
                return translation["title"], html.Button(translation["upload"]), f"{translation['error']} {report}", ''
            else:
                return translation["title"], html.Button(translation["upload"]), translation["validation_complete"], str(report)
        except Exception as e:
            return translation["title"], html.Button(translation["upload"]), f"{translation['error']} {str(e)}", ''


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
