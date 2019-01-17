# TO DO:
# Send to ENV
HOST="127.0.0.1"
PORT=6379


import os, redis, json

r = redis.Redis(host=HOST, port=PORT)


# Population is a dictionary
# Format:




def log_to_redis_coco(population):
    log_name = 'log:test_pop:' + str(population['experiment']["experiment_id"])
    r.lpush(log_name, json.dumps(get_benchmark_data(population)))




def get_benchmark_data(population):
    return {"evals": population["iterations"],
            "instance":population["problem"]["instance"],
            "worker_id":"NA",
            "params":{"sample_size":population["population_size"],
                      "init":"random:[-5,5]",
                      "NGEN":population["algorithm"]["iterations"]
                      },
             "experiment_id":population['experiment']["experiment_id"],
             "algorithm":population["algorithm"]["name"],
             "dim":population["problem"]["dim"],
             "benchmark":population["problem"]["function"],
             "fopt":population["fopt"]}