import hashlib
import json
import random
import time
import paho.mqtt.publish as publish
import sqlite3
import datetime

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def calculate_hash(self):
        data = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.data)
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Create the first block (genesis block)
        genesis_block = Block(0, "", datetime.datetime.now(), {}, "")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)

    def create_block(self, data):
        # Create a new block based on the data
        previous_block = self.chain[-1]
        new_block = Block(previous_block.index + 1, previous_block.hash, datetime.datetime.now(), data, "")
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def print_chain(self):
        # Print the last block added to the chain
        block = self.chain[-1]
        print(f"Block #{block.index}")
        print(f"Timestamp: {block.timestamp}")
        print("Data:")
        for key, value in block.data.items():
            print(f"\t -> {key}: {value} {get_measurement_unit(key)}")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print()

def get_measurement_unit(key):
    if key == "wind_speed":
        return "km/h"
    elif key == "temperature":
        return "°C"
    elif key == "humidity_level":
        return "%"
    else:
        return ""


# Example usage
blockchain = Blockchain()

# MQTT broker's settings
broker = "mqtt.beia-telemetrie.ro"
port = 1883
topic = "training/device/Bolborici-Robert"
topic2 = "training/device/Bolborici-Robert/processed"

# Random weather parameters generator
def generate_random_wind_speed():
    return random.randint(1, 100)

def generate_random_temperature():
    return random.uniform(0.0, 40.0)

def generate_random_humidity_level():
    return random.randint(10, 60)

while True:
    wind_speed = generate_random_wind_speed()
    temperature = generate_random_temperature()
    humidity = generate_random_humidity_level()

    # Create payload dictionary
    payload_dict = {
        "wind_speed": wind_speed,
        "temperature": temperature,
        "humidity_level": humidity
    }

    # Create a new block with the payload data
    blockchain.create_block(payload_dict)

    # Print the last block added to the chain
    blockchain.print_chain()

    # Wait for a chosen period of time
    time.sleep(5)
