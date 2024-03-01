from dash import Dash
from utils.data import load_demographic_indicators
import layouts
import callbacks

# Charger les données
df = load_demographic_indicators()

# Créer une application Dash
app = Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

# Charger la mise en page
app.layout = layouts.home_page(df)

# Enregistrer les callbacks
callbacks.register_callbacks(df)

if __name__ == "__main__":
    app.run_server(debug=True)
