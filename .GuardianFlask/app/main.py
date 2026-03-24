from app import create_app

app = create_app()

# Funciona tanto con:  python app/main.py
# como con:            python -m app.main
app.run(debug=True, port=5000)