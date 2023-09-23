import json
import logging
from time import time
from flask import request
from routes import app

logger = logging.getLogger(__name__)

def calculate_max_value(w, v, values):
    n = len(values)
    memo = {}

    def dp(weight, volume, idx):
        if weight <= 0 or volume <= 0 or idx >= n:
            return 0

        if (weight, volume, idx) in memo:
            return memo[(weight, volume, idx)]

        curr_weight, curr_volume, value = values[idx]
        if curr_weight > weight or curr_volume > volume:
            result = dp(weight, volume, idx + 1)
        else:
            result = max(dp(weight, volume, idx + 1),
                         dp(weight - curr_weight, volume - curr_volume, idx + 1) + value)

        memo[(weight, volume, idx)] = result
        return result

    return dp(w, v, 0)

@app.route('/greedymonkey', methods=['POST'])
def evaluate():
    start = time()
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    w = data["w"]
    v = data["v"]
    f = data["f"]
    
    result = calculate_max_value(w, v, f)
    finish = time() - start
    logging.info("Time elapsed  :{}".format(finish))
    logging.info("My result :{}".format(result))
    return str(result)
