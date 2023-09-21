import matplotlib.pyplot
import time
import psutil
import json
# references:
# https://www.color-hex.com
# https://towardsdatascience.com/visualizing-cpu-memory-and-gpu-utilities-with-python-8028d859c2b0
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplot.html

list_CPU = []
list_M = []
iterate = []

json_path = '../task_3/data1.json'


def save_to_json(cpu_data, memory_data, iteration_data):
    data = {
        "CPU": cpu_data,
        "Memory": memory_data,
        "Iteration": iteration_data
    }
    with open(json_path, 'w') as f:
        json.dump(data, f)

try:
    fig = matplotlib.pyplot.figure()
    Axes = fig.add_subplot()

    for i in range(90):
        # max cpu
        cpu = max(psutil.cpu_percent(percpu=True))
        mm = psutil.virtual_memory().percent
        # append in lists
        list_CPU.append(cpu)
        list_M.append(mm)
        iterate.append(i)

        if i % 2 == 1:
            Axes.clear()
            # CPU
            Axes.fill_between(iterate, list_CPU, color= "#1fb18a", label="CPU", alpha=0.6)
            # Memory
            Axes.plot(iterate, list_M, color= "#d11c1c", label="Memory")
            Axes.grid(linestyle='--')
            Axes.set_ylabel("CPU consumption (%)")
            Axes.set_xlabel("Time (Iterations)")
            Axes.set_title("System Activity Monitor")
            Axes.legend()

            matplotlib.pyplot.pause(0.05)
            save_to_json(list_CPU, list_M, iterate)

        time.sleep(1)

except KeyboardInterrupt:
    print("stopped!")

finally:
    matplotlib.pyplot.show()
