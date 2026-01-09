# Folosim o imagine oficială Python
FROM python:3.10-slim

# Setăm folderul de lucru în interiorul containerului
WORKDIR /app

# Instalăm dependențele de sistem necesare pentru driverul de baza de date
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiem fișierul de dependințe și le instalăm
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem tot codul din folderul curent în container
COPY . .

# Expunem portul pe care rulează Flask (implicit 5000)
EXPOSE 5000

# Comanda pentru a rula aplicația
CMD ["python", "app.py"]