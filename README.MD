This is an implementation of the robustification tool.

The implementation assumes the user should provide the system specitication, the deviated environment w.r.t. some deviation, safety property, progress property, priorities for a set of preferred behavior and controllable/observable events. The tool automatically synthesizes new designs that satisfy the properties and maximize an objective function w.r.t. the common behavior between the original design and the new design and the cost of changes.

We assume all the specifications of the models should be specified in FSP, the modeling language used by [the LTSA tool](https://www.doc.ic.ac.uk/ltsa/).

## System Requirements
This program requires Java version >= 1.8 and Python 3.8. The program has been tested under
```
openjdk version "11.0.14" 2022-01-18
OpenJDK Runtime Environment (build 11.0.14+9-post-Debian-1deb11u1)
OpenJDK 64-Bit Server VM (build 11.0.14+9-post-Debian-1deb11u1, mixed mode, sharing)

Python 3.8.12
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
2022-03-16 23:53:01.584641 Size of the plant: 12 states, 27 transitions
2022-03-16 23:53:01.584748 ====================================>
2022-03-16 23:53:01.584746 Initializing search by using pareto search...
2022-03-16 23:53:01.584768 Number of preferred behaviors: 1
2022-03-16 23:53:01.584805 Number of controllable events with cost: 4
2022-03-16 23:53:01.585236 Number of observable events with cost: 4
2022-03-16 23:53:01.647576 Read back.lts...
2022-03-16 23:53:02.549111 Maximum fulfilled preferred behavior: ['back.lts']
2022-03-16 23:53:02.565136 Start search from events:
        Ec: ['back', 'confirm', 'password', 'select', 'vote']
        Eo: ['back', 'confirm', 'eo.enter', 'eo.exit', 'password', 'select', 'v.enter', 'v.exit', 'vote']
2022-03-16 23:53:02.565463 Initialization completes, time: 0:00:00.980719
2022-03-16 23:53:02.565584 ====================================>
2022-03-16 23:53:02.565609 Weaken the preferred behavior by 0 Essential, 0 Important, and 0 Minor...
2022-03-16 23:53:02.565597 Start finding the next solution(s)...
2022-03-16 23:53:02.565697 Try to weaken the preferred behavior by either: [()]
2022-03-16 23:53:04.041189 This iteration completes, time: 0:00:01.475596
2022-03-16 23:53:04.041283 Number of controller synthesis process invoked: 14
...
2022-03-16 23:53:04.073540 New pareto-optimal found:
        Ec: {'password', 'confirm', 'vote', 'select', 'back'}
        Eo: {'password', 'eo.exit', 'back', 'confirm', 'vote', 'select', 'eo.enter'}
        Preferred Behavior: {'back.lts'}
        Preferred Behavior Utility: 5
        Cost: -2
```

### Radiation Therapy System
```
cd /Robustification/models/therac25
python run.py
```
This program searches the pareto-optimal solutions of the Radiation Therapy system. Then, it should print the following results:
```
...
2022-03-16 23:54:52.141086 Size of the plant: 21 states, 44 transitions
2022-03-16 23:54:52.141315 ====================================>
2022-03-16 23:54:52.141312 Initializing search by using pareto search...
2022-03-16 23:54:52.141904 Number of preferred behaviors: 3
2022-03-16 23:54:52.141978 Number of controllable events with cost: 8
2022-03-16 23:54:52.142101 Number of observable events with cost: 1
2022-03-16 23:54:52.197949 Read back1.lts...
2022-03-16 23:54:53.075066 Read back2.lts...
2022-03-16 23:54:53.958304 Read back3.lts...
2022-03-16 23:54:54.756141 Maximum fulfilled preferred behavior: ['back1.lts', 'back2.lts', 'back3.lts']
2022-03-16 23:54:54.764780 Start search from events:
        Ec: ['b']
        Eo: ['b', 'e', 'enter', 'fire_ebeam', 'fire_xray', 'setMode', 'up', 'x']
2022-03-16 23:54:54.764883 Initialization completes, time: 0:00:02.623573
2022-03-16 23:54:54.764905 ====================================>
2022-03-16 23:54:54.765502 Weaken the preferred behavior by 0 Essential, 0 Important, and 0 Minor...
2022-03-16 23:54:54.765474 Start finding the next solution(s)...
2022-03-16 23:54:54.765656 Try to weaken the preferred behavior by either: [()]
2022-03-16 23:54:54.829395 This iteration completes, time: 0:00:00.063925
2022-03-16 23:54:54.829483 Number of controller synthesis process invoked: 1
2022-03-16 23:54:54.831873 New pareto-optimal found:
        Ec: {'b'}
        Eo: {'e', 'b', 'enter', 'fire_xray', 'up', 'fire_ebeam', 'setMode', 'x'}
        Preferred Behavior: {'back1.lts', 'back3.lts', 'back2.lts'}
        Preferred Behavior Utility: 28
        Cost: -13
```

### Infusion Pump
```
cd /Robustification/models/pump
python run.py
```
We configure the program to use the fast-search strategy for the Infusion pump example. Then, it should print the following results:
```
...
2022-03-16 23:56:21.744292 Size of the plant: 104 states, 484 transitions
2022-03-16 23:56:21.744413 ====================================>
2022-03-16 23:56:21.744411 Initializing search by using fast search...
2022-03-16 23:56:21.744433 Number of preferred behaviors: 2
2022-03-16 23:56:21.744469 Number of controllable events with cost: 8
2022-03-16 23:56:21.744578 Number of observable events with cost: 12
2022-03-16 23:56:22.229873 Read ideal.lts...
2022-03-16 23:56:23.060573 Read recover.lts...
2022-03-16 23:56:23.882073 Maximum fulfilled preferred behavior: ['ideal.lts', 'recover.lts']
2022-03-16 23:56:24.002922 Start search from events:
        Ec: ['line[1].dispense_main_med_flow', 'line[1].flow_complete', 'line[1].set_rate', 'line[1].start_dispense']
        Eo: ['alarm_silence', 'battery_charge', 'battery_spent', 'enable_alarm', 'line[1].change_settings', 'line[1].clear_rate', 'line[1].confirm_settings', 'line[1].dispense_main_med_flow', 'line[1].erase_and_unlock_line', 'line[1].flow_complete', 'line[1].lock_line', 'line[1].lock_unit', 'line[1].set_rate', 'line[1].start_dispense', 'line[1].unlock_unit', 'plug_in', 'turn_off', 'turn_on', 'unplug']
2022-03-16 23:56:24.003093 Initialization completes, time: 0:00:02.258684
2022-03-16 23:56:24.003112 ====================================>
2022-03-16 23:56:24.003130 Weaken the preferred behavior by 0 Essential, 0 Important, and 0 Minor...
2022-03-16 23:56:24.003117 Start finding the next solution(s)...
2022-03-16 23:56:24.003982 Try to weaken the preferred behavior by either: [()]
2022-03-16 23:56:41.616002 This iteration completes, time: 0:00:17.612889
2022-03-16 23:56:41.616115 Number of controller synthesis process invoked: 13
2022-03-16 23:56:41.685799 New solution found:
        Ec: {'line[1].set_rate', 'line[1].dispense_main_med_flow', 'line[1].flow_complete', 'line[1].start_dispense'}
        Eo: {'line[1].set_rate', 'line[1].clear_rate', 'line[1].dispense_main_med_flow', 'line[1].confirm_settings', 'turn_off', 'unplug', 'turn_on', 'line[1].start_dispense', 'line[1].flow_complete', 'line[1].change_settings'}
        Preferred Behavior: {'ideal.lts', 'recover.lts'}
        Preferred Behavior Utility: 70
        Cost: -106
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
    env=[<Files for the deviated environment model>],
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

result = r.synthesize()
next(iter(result)) # use 'for i in result' to enumerate the iterator or use next to call the next iteration.
```
