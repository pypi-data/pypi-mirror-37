# Tripod Applications
Tripod is the evolution of our old project bootstrapper 'falsk-manager'. 
It is under constant development and improvement process.

Tripod is a lightweight project extension that provides command-line utilities for yours applications.
This includes running a development server, a customised Python shell, scripts to run the project test.

This project is intended to be flexible enough to give users easy ways to extend the commands and their behaviours.

Task from this module are called from the command line in the following format:
```
tripod [command]
```


## Getting Started

Tripod assumes that the project using it will follow some structural conventions.

The following defines an ordinary project structure tree:

```
- project_name/
    - tests/
    - static/
    - settings.py
    - tasks.py
```


# Settings

The 'settings.py' file is used as a repository for the project settings.
In the settings.py file is where we generally put project configurations,
register application blueprints and so on.
In the following we present a common 'settings.py' file:

```
import os
import pkg_resources
    
__version__ = pkg_resources.resource_stream(__name__, 'VERSION').read().decode('UTF-8')
    
DEBUG = False
TESTING = False
PROPAGATE_EXCEPTIONS = True
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
BLUEPRINTS = []
    
# logger path configuration
LOG_MODULE = 'aws_utils.aws_logger'
LOG_GROUP = "/"
    
# os system vars
tripod_config = os.getenv('TRIPOD_APP_CONFIG', False)
stream_logs_disable = os.getenv('STREAM_LOGS_DISABLE', False)
```
### Environment Identification
We might have different settings for different environment.
Tripod identifies the environment running by reading a environment variable named **'TRIPOD_APP_CONFIG'**.
For example possible values for **'TRIPOD_APP_CONFIG'** variable are:
```
- $export TRIPOD_APP_CONFIG=development
- $export TRIPOD_APP_CONFIG=production
- $export TRIPOD_APP_CONFIG=test
```
The **default** value is 'development'. So if you dont export a value for TRIPOD_APP_CONFIG 
then tripod will work using **development** settings.

### Settings package
The most common practice is split the settings across sub-packages.

```
- settings/
        - development/
            - __init__.py
            - settings.py
            - env.json
        - production/
            - __init__.py
            - settings.py
            - env.json
        - test/
            - __init__.py
            - settings.py
            - env.json
        - __init__.py
        - settings.py
        - env.json
        - config.py
```

The settings.py file placed on the settings root directory is used as a base_settings
file for the other settings.
Depending on the environment variable 'FLASK-CONFIG' value, the project settings will be updated with the settings files
from one of the settings sub-packages.


# Tasks

The 'tasks.py' is used to register command line functions that can be invoked from the project root directory.

```
from invoke import task 
@task()
def sayhello(context):
    print("hello")
    

# On the bash console:
  # $tripod sayhello
  # outputs:
  # hello
```
It is commonly located on a project package named 'tasks'. But it can be placed on the project root directory too.

### Tasks package
On the tasks package you can split your tasks across subdirectories and files.

This way, tasks defined on the file named 'tasks.py' will be registered on the tripod root name space,
and the other on the module dotted path to task.

Suppose **'./tasks/example.py'** file:
```
from invoke import task 
@task()
def sayhello(context):
    print("hello")
    

# On the bash console:
    $tripod example.sayhello
  # outputs:
  # hello
```

And **'./tasks/tasks.py'** file:
```
from invoke import task 
@task()
def sayhello(context):
    print("hello")
    

# On the bash console:
    $tripod sayhello
  # outputs:
  # hello
```

# Blueprints
TODO

# Calling from console

Tripod comes with some builtin functions. 
The following examples illustrates their usage.

### Initializing development server 
```
tripod run --dev
```
### Initialize project with Gunicorn
```
tripod run 
```

### Running project tests

```
tripod test
```

### behave

TODO

### Initialize project template
```
tripod init-project
```
### Creating Blueprints
```
tripod init-blueprint
```

# Installing
Tripod is part of a bigger set of packages named learn-utils.

So, by the time the only way of installing it is installing learn-utils packs from
 the internal learn pip-server:
```
pip install learn-utils
```
