import json
import logging
from time import time
from flask import request
from routes import app

logger = logging.getLogger(__name__)

def greedy_monkey_solve(w, v, f):
    # Solve using dynamic programming
    dp = [[0] * (v+1) for _ in range(w+1)]

    for i in range(1, len(f)+1):
        weight, volume, value = f[i-1]
        for j in range(w, weight-1, -1):
            for k in range(v, volume-1, -1):
                dp[j][k] = max(dp[j][k], dp[j-weight][k-volume] + value)

    return dp[w][v]

@app.route('/greedymonkey', methods=['POST'])
def evaluate():
    start = time()
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    w = data["w"]
    v = data["v"]
    f = data["f"]
    finish = time() - start
    
    result = greedy_monkey_solve(w, v, f)
    logging.info("Time elapsed  :{}".format(finish))
    logging.info("My result :{}".format(result))
    return str(result)
