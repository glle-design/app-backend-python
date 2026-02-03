from pymongo import MongoClient

# Conexión Local a MongoDB
# db_client = MongoClient().local

# Conexión Remoto a MongoDB (Producción)
db_client = MongoClient("mongodb+srv://glle:adminDB@cluster0.leqor2q.mongodb.net/?appName=Cluster0").Cluster0