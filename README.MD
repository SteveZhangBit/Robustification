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
2022-03-15 15:53:20.962278 Size of the plant: 12 states, 27 transitions
2022-03-15 15:53:20.962565 ====================================>
2022-03-15 15:53:20.962564 Initializing search by using pareto search...
2022-03-15 15:53:20.962583 Number of preferred behaviors: 1
2022-03-15 15:53:20.962607 Number of controllable events: 9
2022-03-15 15:53:20.962612 Number of observable events: 9
2022-03-15 15:53:21.024936 Read back.lts...
2022-03-15 15:53:21.817714 Maximum fulfilled preferred behavior: ['back.lts']
2022-03-15 15:53:21.828250 Start search from events:
        Ec: ['back', 'confirm', 'password', 'select', 'vote']
        Eo: ['back', 'confirm', 'eo.enter', 'eo.exit', 'password', 'select', 'v.enter', 'v.exit', 'vote']
2022-03-15 15:53:21.828385 Initialization completes, time: 0:00:00.865823
2022-03-15 15:53:21.828402 ====================================>
2022-03-15 15:53:21.828414 Weaken the preferred behavior by 0 Essential, 0 Important, and 0 Minor...
2022-03-15 15:53:21.828406 Start finding the next solution(s)...
2022-03-15 15:53:21.828435 Try to weaken the preferred behavior by either: [()]
2022-03-15 15:53:23.168601 This iteration completes, time: 0:00:01.340199
2022-03-15 15:53:23.169002 Number of controller synthesis process invoked: 14

...

2022-03-15 15:53:23.196284 New pareto-optimal found:
        Ec: {'select', 'confirm', 'back', 'password', 'vote'}
        Eo: {'eo.enter', 'select', 'password', 'back', 'confirm', 'vote', 'eo.exit'}
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
2022-03-15 15:54:51.817889 Initializing search by using pareto search...
2022-03-15 15:54:51.817908 Number of preferred behaviors: 3
2022-03-15 15:54:51.817933 Number of controllable events: 8
2022-03-15 15:54:51.818045 Number of observable events: 8
2022-03-15 15:54:51.868565 Read back1.lts...
2022-03-15 15:54:52.626067 Read back2.lts...
2022-03-15 15:54:53.400547 Read back3.lts...
2022-03-15 15:54:54.185018 Maximum fulfilled preferred behavior: ['back1.lts', 'back2.lts', 'back3.lts']
2022-03-15 15:54:54.192952 Start search from events:
        Ec: ['b']
        Eo: ['b', 'e', 'enter', 'fire_ebeam', 'fire_xray', 'setMode', 'up', 'x']
2022-03-15 15:54:54.193046 Initialization completes, time: 0:00:02.375159
2022-03-15 15:54:54.193062 ====================================>
2022-03-15 15:54:54.193073 Weaken the preferred behavior by 0 Essential, 0 Important, and 0 Minor...
2022-03-15 15:54:54.193066 Start finding the next solution(s)...
2022-03-15 15:54:54.193093 Try to weaken the preferred behavior by either: [()]
2022-03-15 15:54:54.254896 This iteration completes, time: 0:00:00.061834
2022-03-15 15:54:54.254987 Number of controller synthesis process invoked: 1
2022-03-15 15:54:54.257307 New pareto-optimal found:
        Ec: {'b'}
        Eo: {'e', 'fire_ebeam', 'x', 'fire_xray', 'setMode', 'b', 'up', 'enter'}
        Preferred Behavior: {'back3.lts', 'back2.lts', 'back1.lts'}
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

2022-03-15 15:56:07.115644 Initializing search by using fast search...
2022-03-15 15:56:07.115663 Number of preferred behaviors: 2
2022-03-15 15:56:07.115752 Number of controllable events: 11
2022-03-15 15:56:07.115817 Number of observable events: 19
2022-03-15 15:56:07.557077 Read ideal.lts...
2022-03-15 15:56:08.388128 Read recover.lts...
2022-03-15 15:56:09.226877 Maximum fulfilled preferred behavior: ['ideal.lts', 'recover.lts']
2022-03-15 15:56:09.333604 Start search from events:
        Ec: ['line[1].dispense_main_med_flow', 'line[1].flow_complete', 'line[1].set_rate', 'line[1].start_dispense']
        Eo: ['alarm_silence', 'battery_charge', 'battery_spent', 'enable_alarm', 'line[1].change_settings', 'line[1].clear_rate', 'line[1].confirm_settings', 'line[1].dispense_main_med_flow', 'line[1].erase_and_unlock_line', 'line[1].flow_complete', 'line[1].lock_line', 'line[1].lock_unit', 'line[1].set_rate', 'line[1].start_dispense', 'line[1].unlock_unit', 'plug_in', 'turn_off', 'turn_on', 'unplug']
2022-03-15 15:56:09.333762 Initialization completes, time: 0:00:02.218120
2022-03-15 15:56:09.333779 ====================================>
2022-03-15 15:56:09.333793 Weaken the preferred behavior by 0 Essential, 0 Important, and 0 Minor...
2022-03-15 15:56:09.333784 Start finding the next solution(s)...
2022-03-15 15:56:09.334017 Try to weaken the preferred behavior by either: [()]
2022-03-15 15:56:25.386485 This iteration completes, time: 0:00:16.052706
2022-03-15 15:56:25.386584 Number of controller synthesis process invoked: 13
2022-03-15 15:56:25.448809 New solution found:
        Ec: {'line[1].start_dispense', 'line[1].dispense_main_med_flow', 'line[1].flow_complete', 'line[1].set_rate'}
        Eo: {'line[1].confirm_settings', 'line[1].change_settings', 'unplug', 'line[1].dispense_main_med_flow', 'line[1].flow_complete', 'line[1].start_dispense', 'line[1].set_rate', 'turn_off', 'turn_on', 'line[1].clear_rate'}
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
