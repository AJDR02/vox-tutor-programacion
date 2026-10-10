# Vox — Tutor de programación

Aplicación de Streamlit con OpenAI API para tutoría de programación, chat por texto, transcripción de audio y respuestas habladas.

## Requisitos
- Python 3.10 o posterior
- Una clave de OpenAI API con crédito disponible

## Ejecutar en Windows (PowerShell)
Desde la carpeta que contiene `app.py`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Crea `.streamlit/secrets.toml` copiando `secrets.example.toml` y reemplaza el texto de ejemplo por tu clave privada. Nunca subas `secrets.toml` a GitHub ni compartas su contenido.

Luego inicia:

```powershell
streamlit run app.py
```

## Notas
- Enter en el campo de texto envía el mensaje.
- El botón de flecha ofrece una alternativa para enviar.
- Para enviar audio, graba en el control del micrófono y pulsa la flecha.
- El costo de uso de la API es independiente de la suscripción de ChatGPT.
