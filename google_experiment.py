import google_producer
import google_controller
import time
import redis
import os
import process_logs




HOST = os.environ['REDIS_HOST']
PORT = os.environ['REDIS_PORT']
r = redis.Redis(host=HOST, port=PORT)


#conf = {
#    2: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':20, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':2 },
#    3: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':30, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':2 },
#    5: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':4 },
#    10:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':4 },
#    20:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':8 },
#    40:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':16 },



conf = {
    2: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':20, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':2 },
    3: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':30, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':2 },
    5: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':4 },
    10:{ 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':8 },
    20:{ 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':16 },
    40:{ 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':32 },

    'EXPERIMENT_ID' : int(time.time()),
     #For paper:
    'FUNCTIONS' : (3,),
    'DIMENSIONS' : (10,20,40),       #(2,3,5,10,20)
    'INSTANCES' : range(1,2,3)    #range(1,6)+range(41, 51)

}
#Example from EvoSpace
# Parameter configuration for each dimension 10**5 * D
# 2: 200,000
# 3: 300,000
# 5: 500,000

# 40: 4,000,000

#es_conf = {
#    2: {'EVOSPACE_SIZE':250, 'NGEN':50, 'SAMPLE_SIZE': 100, 'MAX_SAMPLES':20, 'PSO':0, 'GA':2 },
#    3: {'EVOSPACE_SIZE':250, 'NGEN':50, 'SAMPLE_SIZE': 100, 'MAX_SAMPLES':30, 'PSO':0, 'GA':2 },
#    5: {'EVOSPACE_SIZE':500, 'NGEN':50, 'SAMPLE_SIZE': 100, 'MAX_SAMPLES':25, 'PSO':0, 'GA':4 },
#    10:{'EVOSPACE_SIZE':1000,'NGEN':50, 'SAMPLE_SIZE': 200, 'MAX_SAMPLES':25, 'PSO':0, 'GA':4 },
#    20:{'EVOSPACE_SIZE':2000,'NGEN':50, 'SAMPLE_SIZE': 200, 'MAX_SAMPLES':25, 'PSO':0, 'GA':8 },
#    40:{'EVOSPACE_SIZE':4000,'NGEN':50, 'SAMPLE_SIZE': 200, 'MAX_SAMPLES':25, 'PSO':0, 'GA':16 },
#}


def new_populations(env, number_of_pops, n_individuals, dim, lb, ub ):
    import random
    message_list = []
    for pop in range(number_of_pops):
        new_env = dict(env)
        new_env["population"] = [{"chromosome": [random.uniform(lb,ub) for _ in range(dim)], "id": None, "fitness": {"DefaultContext": 0.0}} for _ in range(n_individuals)]

        message_list.append(new_env)
    return message_list



def experiment(conf):
    for function in  conf['FUNCTIONS']:
        for dim in conf['DIMENSIONS'] :
            print ("DIM", dim)
            for instance in conf['INSTANCES'] :
                print ("instance:", instance)

                env = {"problem":
                            {"name": "BBOB",
                              "instance": instance,
                              "error": 1e-8,
                              "function": function,
                              "dim": dim,
                              "search_space": [-5, 5],
                              "problem_id": "%s-%s-%s-%s" % ( conf['EXPERIMENT_ID'] , function, instance, dim ),
                              "max_iterations": conf[dim]['MAX_ITERATIONS'] * conf[dim]['MESSAGES_HUB_GA'] },
                 "population": [],
                 "population_size": conf[dim]['POP_SIZE'],
                 "id": "1",
                 "algorithm": {"crossover": {"type": "cxTwoPoint", "CXPB_RND": [0.2, 0.6], "CXPB": 0.2}, "name": "GA",
                               "mutation": {"MUTPB": 0.5, "indpb": 0.05, "sigma": 0.5, "type": "mutGaussian", "mu": 0},
                               "selection": {"type": "tools.selTournament", "tournsize": 2},
                               "iterations": conf[dim]['NGEN']},
                 "experiment":
                     {"owner": "mariosky", "type": "benchmark", "experiment_id": conf['EXPERIMENT_ID']}}

                #Initialize pops
                google_messages = new_populations(env, conf[dim]['MESSAGES_HUB_GA'] , conf[dim]['POP_SIZE'],env["problem"]["dim"], env["problem"]["search_space"][0], env["problem"]["search_space"][1])
                print(google_messages)
                #Initialize experiment?
                google_producer.send_messages(google_messages)
                #kafka_producer.send_messages(kafka_messages,'populations-topic')
                print ("First Messages Sent")
                print ("Begin Message Loop")

                google_controller.experiment(env)

                #Block until this experiment is done, redis queue, time_out
                task = r.blpop("experiment_finished", 0)


                print (task, "Done")







if __name__ == '__main__':
    DESTINATION_PATH = r'/Users/mariogarcia-valdez/Desktop/CocoExp/'
    PROJECT_PATH = r'/Users/mariogarcia-valdez/evocloud/'
    experiment(conf)
    data_folder = process_logs.process_logs(conf['EXPERIMENT_ID'])
    print ("python -m cocopp -o "+ DESTINATION_PATH + str(conf['EXPERIMENT_ID'])+ " " + PROJECT_PATH + data_folder[2:])
