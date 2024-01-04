# CSV Quality Check with Frictionless
This [Streamlit app](https://appfrictionless-test0.streamlit.app/) enables users to perform quality checks on CSV files of SFOE OGD publications using the Frictionless framework. The app allows for easy validation of CSV files against defined schemas (extracted from corresponding `datapackage.json`) found on _uvek-gis_, ensuring data integrity and adherence to specified formats.

You can find the app [here](https://appfrictionless-test0.streamlit.app/)

## Feautres
- **File Upload**: Users can upload CSV files for validation directly through the Streamlit interface.
- **Schema-based Validation**: Leveraging Frictionless, the app validates uploaded CSV files against predefined schemas or inferred data structures.
- **Error Handling**: Error messages are provided in case of validation issues, aiding users in understanding and rectifying data problems.


## Files
- `app.py`: This is the main Python file containing the Streamlit application code.
- `mapping.py`: This file contains the mapping from file name to OGD number. Note: There is not a datapackage for every SFOE OGD publication.
- `requirements.txt`: Lists the Python dependencies required for running the Streamlit app.
- `.streamlit/config.toml`: This is the Streamlit configuraion file. It allows customization of Streamlit's behavior, including server settings, theming, and other preferences.
