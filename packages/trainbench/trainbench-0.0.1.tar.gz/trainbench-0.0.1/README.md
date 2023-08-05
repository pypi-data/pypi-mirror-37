[![PyPI version](https://badge.fury.io/py/trainbench.svg)](https://badge.fury.io/py/trainbench)

# Trainbench 

Trainbench is a tool for quickly setup a (Deep Learning) cross-validation training session with configuration instantiation, learned weights, plots, etc, recording at each training epoch.

Compatible with Keras.

**! ⚠️ This  package is currently under active development ⚠️ !**

## Getting started

##### Install
```bash
pip install trainbench
```

##### Create a train session
```python
# train.py

# name
name = 'experiment_01'

# parameters to cross validate against
parameters = {
    'fc_size': [256, 512, 1024]    
    # ...
}

def train(parameters):
    xyz = parameters['xyz']
    # ...
    
    
```

##### Running from the command line
```bash
trainbench .
```

##### Checkout your results
```
    <name>/crosses/
                   /001 
                       ├─ meta.yml 
                       ├─ history.pkl 
                       └─ weights/
                              ├─ 001.h5
                              └─ 002.h5
                                 ...
```




##### In Jupyter Notebooks/Python script
```python
from trainbench import Bench

parameters = {

}

def train_fn(parameters):
    pass
    
bench = Bench()
bench.train('experiment_xyz', train_fn, parameters)
```


### Author notes

I'm wrote this tool for my own usage. Feel free to use it at your own will. 
If you would like to see any additional features / report existing issues please submit a pull request and/or open an issue.
