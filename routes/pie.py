from flask import request
import math
import json
import logging
from routes import app
logger = logging.getLogger(__name__)

# Assume 100% is 6.2831853 radian
def generate_pie_chart(instruments):
    # Get the instruments quantity in a list
    instrument = instruments["data"]
    values = []
    for i in instrument:
        values.append(i["quantity"]*i["price"])
    # Sort in descending order
    sorted_values = sorted(values, reverse=True)
    
    # Convert to proportion
    total_values = sum(sorted_values)
    proportions = [(q / total_values) for q in sorted_values]
    
    # Find if there is a proportion less than 0.05%
    # if it is, increase it to 0.05% and decrease the one before for adjustment
    if any(p < 0.0005 for p in proportions):
        for i in range(len(proportions)):
            if proportions[i] < 0.0005:
                # Do proportional adjustment
                dif = 0.0005- proportions[i]
                proportions[i] = 0.0005
                for j in range(i):
                    proportions[j] -= dif*proportions[j]
                    
    # Convert the proportions to radian
    print(proportions)
    radian = [p * 2 *math.pi for p in proportions]
    
    # Return the radians in summed up list
    radian_summed = [0.0]
    for i in range(len(radian)):
        radian_summed.append(sum(radian[:i+1]))
    # max 7 decimal points or 8?
    radian_summed = [round(r, 8) for r in radian_summed]
    return [round(a, 8) for a in radian_summed]

@app.route('/pie-chart', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    result = generate_pie_chart(data)
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)
