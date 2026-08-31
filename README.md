# MediGuide AI

A two-step Streamlit health-guidance interface:

1. **API Key page** — user enters the OpenAI API key.
2. **Health Information page** — user enters age, gender, duration, severity, conditions, medications and symptoms.
3. The app sends the information to OpenAI and displays educational guidance.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Important

This is an educational prototype. Do not use it as a medical diagnosis or emergency service.

The API key is kept in Streamlit session state and is not written to a local database/file by this code. For production, use a secure server-side secret-management strategy and avoid exposing API keys to client-side code.
