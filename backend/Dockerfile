FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

# Command to run the FastAPI app
CMD ["fastapi", "run", "main.py", "--port", "8000"]
