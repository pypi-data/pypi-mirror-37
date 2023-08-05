enzyme-cost
===========

Kinetic modeling of pathway fluxes for estimating the specific cost in enzymes
for sustaining a given flux.

Based on the idea of taking a kinetic model, and assuming fluxes are fixed but
the enzyme and metabolite levels are variables. This way, we minimize the total
enzyme level to get the minimal enzyme cost needed to achieve a certain 
pathway flux.

Dependencies:
- Ubuntu packages: `sudo apt install X`
    - glpk-utils (4.63-1)

- PyPI packages:   `sudo pip install X`
    - numpy
    - scipy
    - matplotlib
    - pulp
    - pandas
    - sbtab
    - equilibrator-api
    
Example
-------
Try running the example script:
```
python -m example.test
```

