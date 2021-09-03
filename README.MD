This is a prototype implementation of the robustification tool.

The implementation assumes the user should provide the system specitication, the deviated environment w.r.t. some deviation, safety property, progress property, priorities for a set of preferred behavior and controllable/observable events. The tool automatically synthesizes new designs that satisfy the properties and maximize an objective function w.r.t. the common behavior between the original design and the new design and the cost of changes.

We assume all the specifications of the models should be specified in FSP, the modeling language used by [the LTSA tool](https://www.doc.ic.ac.uk/ltsa/).

## System Requirements
This program requires Java version >= 1.8 and Python 3.8. The program has been tested under
```
openjdk version "11.0.11" 2021-04-20
OpenJDK Runtime Environment (build 11.0.11+9-Ubuntu-0ubuntu2.20.04)
OpenJDK 64-Bit Server VM (build 11.0.11+9-Ubuntu-0ubuntu2.20.04, mixed mode, sharing)

Python 3.8.10
```

## Install Instruction
This program relies on a Java program for parsing FSP models and [MDESops](https://gitlab.eecs.umich.edu/M-DES-tools/desops) for supervisory controller synthesis. Please refer to the homepage of MDESops to install the environment.

**On the other hand, we recommend using the following Docker image to try out our tool!**

### Docker Image
In order to build the Docker image:
```
cd <download directory>
docker build -t robustify .
```
The Docker image takes about 1.5 GB disk space. Then, to run the Docker image:
```
docker run -it --rm robustify
```

## Reproduce the results in the paper
The following sections assume running under the Docker image.
### Voting Machine
```
cd /Robustification/models/voting
python run.py
```
This program searches the pareto-optimal solutions of the voting example. Then, it should print the following results:
```
...

2021-09-03 00:35:39.077745 Size of the plant: 12 states, 27 transitions
2021-09-03 00:35:39.892190 Number of preferred behaviors: 1
2021-09-03 00:35:39.892312 Number of controllable events with cost: 4
2021-09-03 00:35:39.892326 Number of observable events with cost: 4
2021-09-03 00:35:40.831898 Maximum fulfilled preferred behavior: ['back.lts']
2021-09-03 00:35:40.847153 Start search from events:
	Ec: ['back', 'confirm', 'password', 'select', 'vote']
	Eo: ['back', 'confirm', 'eo.enter', 'eo.exit', 'password', 'select', 'v.enter', 'v.exit', 'vote']
2021-09-03 00:35:40.847281 Weaken the preferred behavior by 0 Essential, 0 Important, and 0 Minor...
2021-09-03 00:35:43.355529 New pareto-optimal found:
	Ec: {'confirm', 'password', 'back', 'vote', 'select'}
	Eo: {'confirm', 'v.enter', 'password', 'back', 'vote', 'select', 'v.exit'}
	Preferred Behavior: {'back.lts'}
	Preferred Behavior Utility: 5
	Cost: -2

...

2021-09-03 00:35:43.356661 New pareto-optimal found:
	Ec: {'confirm', 'password', 'back', 'vote', 'select'}
	Eo: {'confirm', 'password', 'back', 'vote', 'select', 'eo.enter', 'eo.exit'}
	Preferred Behavior: {'back.lts'}
	Preferred Behavior Utility: 5
	Cost: -2
2021-09-03 00:35:43.356686 Weaken the preferred behavior by 1 Essential, 0 Important, and 0 Minor...
2021-09-03 00:35:43.420116 No new solution found.
2021-09-03 00:35:43.456811 Total controller synthesis: 15 times.
2021-09-03 00:35:43.459636 Total time: 0:00:03.567459
2021-09-03 00:35:43.460197 Number of solutions: 6
```

### Radiation Therapy System
```
cd /Robustification/models/therac25
python run.py
```
This program searches the pareto-optimal solutions of the Radiation Therapy system. Then, it should print the following results:
```
...

2021-09-03 00:39:29.787632 New pareto-optimal found:
	Ec: {'b'}
	Eo: {'e', 'enter', 'x', 'fire_xray', 'b', 'fire_ebeam', 'setMode', 'up'}
	Preferred Behavior: {'back2.lts', 'back1.lts'}
	Preferred Behavior Utility: 16
	Cost: -13
...
```

### Infusion Pump
```
cd /Robustification/models/pump
python run.py
```
This program searches the local-optimal solutions of the Infusion Pump system with the fast-search strategy. Then, it should print the following results:
```
...

2021-09-03 00:42:26.440096 New solution found:
	Ec: {'line.1.set_rate', 'line.1.start_dispense', 'line.1.flow_complete', 'line.1.dispense_main_med_flow'}
	Eo: {'turn_on', 'line.1.clear_rate', 'unplug', 'plug_in', 'line.1.start_dispense', 'line.1.confirm_settings', 'line.1.change_settings', 'line.1.dispense_main_med_flow', 'line.1.flow_complete', 'line.1.set_rate', 'turn_off'}
	Preferred Behavior: {'recover.lts', 'ideal.lts'}
	Preferred Behavior Utility: 70
	Cost: -141
2021-09-03 00:42:26.440244 Weaken the preferred behavior by 1 Essential, 0 Important, and 0 Minor...
2021-09-03 00:43:39.689130 New solution found:
	Ec: {'line.1.set_rate', 'line.1.start_dispense', 'line.1.flow_complete', 'line.1.dispense_main_med_flow'}
	Eo: {'turn_on', 'line.1.clear_rate', 'unplug', 'line.1.start_dispense', 'line.1.confirm_settings', 'line.1.change_settings', 'line.1.dispense_main_med_flow', 'line.1.flow_complete', 'line.1.set_rate', 'turn_off'}
	Preferred Behavior: {'ideal.lts'}
	Preferred Behavior Utility: 35
	Cost: -106
...

```

## API Usage
The user can create a new project as follows:

1. Create a new folder of the system under model.
```
cd /Robustification/models
mkdir <project name>
```

2. Create the FSP specifications for the system, the deviated environment, the safety property, and the preferred behavior.

3. Create a run.py file based on the following templates:
```
import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from repair import *

alphabet = [<All the events of the system and the deviated environment>]


r = Repair(
    alg="pareto", # "fast" for fast search; "pareto" for pareto-front search
    sys=[<Files for the system model>],
    env_p=[<Files for the deviated environment model>],
    safety=[<Files for the safety properties>],
    preferred={   # rank the preferred behavior by importance
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    },
    progress=[<Events for the progress property>],
    alphabet=alphabet,
    controllable={  # rank the controllable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    },
    observable={    # rank observable events by cost
        PRIORITY3: [],
        PRIORITY2: [],
        PRIORITY1: [],
        PRIORITY0: []
    }
)

result = r.synthesize(3) # number of the maximum iterations
# Uncomment the following lines to print the new designs in FSP.
# print("Printing M' for each pareto-optimal...")
# for i, c in enumerate(result):
#     print("Solution", i)
#     print(r.fsm2fsp(c["M_prime"], c["observable"], name="M"))

```