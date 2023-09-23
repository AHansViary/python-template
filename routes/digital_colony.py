import json
import logging
from time import time
from flask import request
from routes import app
logger = logging.getLogger(__name__)
@app.route('/digital-colony', methods=['POST'])

def calculate_weight(colony):
    return sum(map(int,colony))

def calculate_signature(pair):
    digit1, digit2 = pair[0], pair[1]
    return (digit1 - digit2) % 10

def generate_next_generation(colony):
    weight = calculate_weight(colony)
    new_generation = []
    for i in range(len(colony)-1):
        pair = colony[i:i+2]
        signature = calculate_signature(pair)
        new_digit = (weight + signature) % 10
        new_generation.append(colony[i])
        new_generation.append(new_digit)
    new_generation.append(colony[-1])
    return new_generation

def simulate_generations(start_colony, num_generations):
    colony = [int(digit) for digit in start_colony]
    for _ in range(num_generations):
        colony = generate_next_generation(colony)
    total_weight = calculate_weight(colony)
    return colony, total_weight

def evaluate():
    start = time()
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for part in data:
        generation = part["generations"] # number
        colony = part["colony"] # string
        final_colony, final_weight = simulate_generations(colony, generation)
        logging.info(final_colony)
        result.append(final_weight)
    logging.info(time()-start)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
