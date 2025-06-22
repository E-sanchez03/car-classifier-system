import json
import base64
import numpy as np
import tensorflow as tf
from kafka import KafkaConsumer
from PIL import Image
import io

# --- Configuración ---
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'taller_camara_stream'
MODEL_PATH = './models/clasificador_coches_v4.keras'
CLASS_NAMES_PATH = './models/marcas_coches.json'
IMG_SIZE = (224, 224)

# --- Cargar Modelo y Clases ---
print("Cargando modelo y nombres de clase...")
model = tf.keras.models.load_model(MODEL_PATH)
with open(CLASS_NAMES_PATH, 'r') as f:
    class_names = json.load(f)
print("¡Modelo y clases cargados exitosamente!")

# --- Inicializar Consumidor de Kafka ---
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest', # Empezar a leer desde los mensajes más nuevos
    fetch_max_bytes=20971520 # 20MB
)

print(f"Consumidor escuchando en el tópico '{KAFKA_TOPIC}'...")

# --- Bucle Principal ---
try:
    for message in consumer:
        # Extraer datos del mensaje
        data = message.value
        image_name = data['image_name']
        image_b64 = data['image_data']
        print(f"\n--- Mensaje Recibido: {image_name} ---")

        # Decodificar la imagen desde base64
        image_bytes = base64.b64decode(image_b64)
        
        # Usar PIL/Pillow para abrir la imagen desde los bytes
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Pre-procesar la imagen para el modelo
        img_resized = img.resize(IMG_SIZE)
        img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
        img_expanded = np.expand_dims(img_array, axis=0)

        # Realizar la predicción
        predictions = model.predict(img_expanded)
        predicted_index = np.argmax(predictions[0])
        predicted_name = class_names[str(predicted_index)]
        confidence = np.max(predictions[0]) * 100

        # Mostrar el resultado
        print(f"🚗 Predicción: {predicted_name}")
        print(f"   Confianza: {confidence:.2f}%")
        

except KeyboardInterrupt:
    print("\nConsumidor detenido.")
finally:
    consumer.close()