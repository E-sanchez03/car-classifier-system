import time
import os
import random
import json
import base64
from kafka import KafkaProducer

# --- Configuración ---
KAFKA_BROKER = 'broker:29092'
KAFKA_TOPIC = 'taller_camara_stream'
IMAGE_DIR = '/app/data/imagenes_test'
CAMERA_ID = 'cam01'

# --- Inicializar Productor de Kafka ---
# Nos aseguramos de que pueda manejar mensajes grandes (imágenes)
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    max_request_size=20971520 # 20MB
)

print("Productor iniciado. Enviando imágenes cada 5 segundos...")

# --- Bucle Principal ---
try:
    while True:
        # Elegir una imagen aleatoria del directorio
        image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            print(f"No se encontraron imágenes en el directorio '{IMAGE_DIR}'.")
            time.sleep(5)
            continue
            
        random_image_path = os.path.join(IMAGE_DIR, random.choice(image_files))

        # Leer la imagen como bytes y codificarla en base64
        with open(random_image_path, "rb") as image_file:
            image_bytes = image_file.read()
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')

        # Crear el mensaje
        message = {
            'timestamp': time.time(),
            'camera_id': CAMERA_ID,
            'image_name': os.path.basename(random_image_path),
            'image_data': image_b64
        }
        
        # Enviar el mensaje al tópico de Kafka
        producer.send(KAFKA_TOPIC, message)
        print(f"Enviado: {message['image_name']} desde la cámara {message['camera_id']}")
        
        # Esperar antes de enviar la siguiente imagen
        time.sleep(5)

except KeyboardInterrupt:
    print("\nProductor detenido.")
finally:
    producer.close()