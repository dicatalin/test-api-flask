```bash
pip install flask flask-sqlalchemy psycopg2-binary
pip install flask-cors
pip install python-dotenv
```

```bash
python app.py
```

```bash
docker build -t api-carti-image .
```

```bash
# Salvezi imaginea din Docker într-o arhivă
docker save api-carti-image:latest > api-carti.tar

# O imporți în namespace-ul de Kubernetes (k8s.io)
ctr -n k8s.io images import api-carti.tar
```

```bash
http://192.168.122.241:30001/carti