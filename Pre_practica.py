import random
import time
import paho.mqtt.publish as publish
import json


# Setările brokerului MQTT
broker = "mqtt.beia-telemetrie.ro"
port = 1883
topic = "training/device/Bolborici-Robert"
topic2 = "training/device/Bolborici-Robert/processed"

# Funcțiile pentru generarea random a parametrilor(viteza vantului, temperatura si umiditate)
def generate_random_wind_speed():
    return random.randint(1, 100)

def generate_random_temperature():
    return random.uniform(0.0, 40.0)

def generate_random_humidity_level():
    return random.randint(10, 60)


while True:
    wind_speed = generate_random_wind_speed()
    print (f"{wind_speed} km/h")
    temperature = generate_random_temperature()
    print (f"{temperature:.2f} celsius")
    humidity = generate_random_humidity_level()
    print (f"{humidity} %")


    payload_dict = {
        "wind_speed" : wind_speed,
        "temperature" : temperature,
        "humidity_level" : humidity
    }

    # Publicarea datelor de mediu random în topic
    publish.single(topic, hostname=broker, port=port, payload=json.dumps(payload_dict))

    # Așteptare pentru o perioadă de timp
    time.sleep(5)
