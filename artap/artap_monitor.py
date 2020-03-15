import os
import time
import rpyc
import datetime
import getopt
import sys

MONITOR_PORT = 16000
port = MONITOR_PORT
MONITOR_SERVER = "localhost"
server = MONITOR_SERVER

options, remainder = getopt.getopt(sys.argv[1:], "h:s:p:", ["help", "server=", "port="])

for opt, args in options:
    if opt in ('-s', '--server'):
        # print("server", args)
        server = args
    elif opt in ('-p', '--port'):
        print("port", args)
        port = int(args)
    elif opt in ('-h', '--help'):
        print("Usage: artap_monitor\n")
        print("\t-s, --server\t\tserver")
        print("\t-p, --port\t\tport")
        exit(0)


def clear():
    os.system('clear' if os.name == 'nt' else 'clear')


# connect to server
conn = rpyc.classic.connect(server, port)
while True:
    name = conn.root.problem.name
    parameters = conn.root.problem.parameters
    costs = conn.root.problem.costs
    stats = conn.root.stats()
    populations = conn.root.populations()

    # clear
    clear()

    print("Artap Monitor - {}".format(name))
    print("")

    # stats
    print("Individuals: {}\t\tNumber of populations: {}".format(stats["individuals_count"], stats["populations_count"]))
    print("Empty:       {}".format(stats["individuals_stats"]["empty"]))
    print("In progress: {}".format(stats["individuals_stats"]["in_progress"]))
    print("Evaluated:   {}".format(stats["individuals_stats"]["evaluated"]))
    print("Failed:      {}".format(stats["individuals_stats"]["failed"]))
    print("")
    parameters_str = ""
    for parameter in parameters:
        parameters_str += "{}: {}, ".format(parameter["name"], parameter["bounds"])
    if len(parameters_str):
        parameters_str = parameters_str[:-2]
    costs_str = ""
    for cost in costs:
        costs_str += "{}, ".format(cost["name"])
        # costs_str += "{}: {}, ".format(cost["name"], cost["criteria"])
    if len(costs_str):
        costs_str = costs_str[:-2]
    print("Parameters: {}".format(parameters_str))
    print("Costs:      {}".format(costs_str))
    print("")

    # individuals
    if len(populations) > 0:
        last_population = populations[-1]
        if last_population is not None:
            template = "{:13s}{:11}{:11}{:13}{:" + str(len(parameters) * 10 + 3) + "s}{:" + str(len(costs) * 10 + 3) + "s}"

            print(template.format("State", "Start", "Finish", "Elapsed", "Parameters", "Costs"))
            for individual in last_population.individuals:
                state = individual.state
                state_str = "empty"
                if state.value == 1:
                    state_str = "in progress"
                elif state.value == 2:
                    state_str = "evaluated"
                elif state.value == 3:
                    state_str = "failed"

                if individual.info["start_time"] > 0:
                    dt_startime = datetime.datetime.fromtimestamp(individual.info["start_time"]).strftime("%H.%M.%S")
                else:
                    dt_startime = ""
                if individual.info["finish_time"] > 0:
                    dt_finishtime = datetime.datetime.fromtimestamp(individual.info["finish_time"]).strftime("%H.%M.%S")
                    dt_elapsedtime = (datetime.datetime.fromtimestamp(individual.info["finish_time"]) - datetime.datetime.fromtimestamp(individual.info["start_time"])).microseconds / 1000
                else:
                    dt_finishtime = ""
                    dt_elapsedtime = datetime.timedelta().microseconds * 1000

                hours, rem = divmod(dt_elapsedtime, 3600)
                minutes, seconds = divmod(rem, 60)
                elapsedtime_str = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds) if dt_elapsedtime > 0 else ""

                vector_str = "{}".format(", ".join(format(x, " 5.2e") for x in individual.vector))
                costs_str = "{}".format(", ".join(format(x, " 5.2e") for x in individual.costs)) if state.value == 2 else ""

                print(template.format(state_str, dt_startime, dt_finishtime, elapsedtime_str, vector_str, costs_str))

    time.sleep(1.0)
