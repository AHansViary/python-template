import json
import logging
from time import time
from flask import request
from routes import app
logger = logging.getLogger(__name__)
@app.route('/digital-colony', methods=['POST'])

def generate_next_generation(d):
    weight = sum(map(int,d))
    new_generation = []
    for i in range(len(d)-1):
        pair = d[i:i+2]
        digit1, digit2 = pair[0], pair[1]
        signature = (digit1 - digit2) % 10
        new_digit = (weight + signature) % 10
        new_generation.append(d[i])
        new_generation.append(new_digit)
    new_generation.append(d[-1])
    return new_generation

def simulate_generations(start_colony, num_generations):
    e = [int(digit) for digit in start_colony]
    for _ in range(num_generations):
        e = generate_next_generation(e)
    total_weight = calculate_weight(e)
    return e, total_weight

def evaluate():
    start = time()
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for part in data:
        generation = part["generations"]
        colons = part["colony"]
        final_colony, final_weight = simulate_generations(colons, generation)
        logging.info(final_colony)
        result.append(final_weight)
    logging.info(time() - start)
    logging.info("My result: {}".format(result))
    return json.dumps(result)
