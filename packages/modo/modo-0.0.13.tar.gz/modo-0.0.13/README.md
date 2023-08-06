# Modo

modo is a framework for building bootstrap images
for bootstrapping immutable machines by running docker containers

# Table of Contents
1. [Usage](##Usage)
2. [Installation](###Installation)
3. [Example](###Example)
4. [Workflow](docs/workflow.md)



## Usage

### Installation

```bash
pip install modo
```

for developing:

```bash
git clone git@bitbucket.org:mindcurv/modo.git
cd modo; virtualenv venv --python=python3
. venv/bin/activate
pip install -e .[dev]
python setup.py develop
```

### Example

```python

from modo import RoseCLI, SowRose, GrowRose

class SowExample(SowRose):

    def run(self):
       print(self.jinja_context)

class GrowExample(GrowRose):

    def run(self):
       print('@}->--')

cli = RoseCLI(SowExample, GrowExample)

if __name__ == '__main__':
    cli()
```    

for detailed workflow [click here](docs/workflow.md)