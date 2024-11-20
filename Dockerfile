FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN apt-get install poppler-utils -y 

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# Uncomment to run FastAPI only
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8", "--reload"]

# Expose the Streamlit port
EXPOSE 8501

# Default command to run both FastAPI and Streamlit
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --workers 8 --reload & streamlit run chat_app.py --server.port 8501 --server.address 0.0.0.0"]
