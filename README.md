1. Open streamlit app, create an user and generate API_KEY: 
```bash
streamlit run streamlit_app.py
```
Login with following credentials:
```
username : admin
password : Password+123

```

2. FAST API
```bash
uvicorn main:app --reload
```

Open : 127.0.0.1:8000/docs and authorize with API_KEY generated in step 1.
Then you can test the API.

