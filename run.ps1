Start-Process powershell -ArgumentList "-NoExit", "-Command", "py app.py"

Start-Sleep -Seconds 5

Start-Process powershell -ArgumentList "-NoExit", "-Command", "py -m streamlit run streamlit_app.py"

Start-Sleep -Seconds 5