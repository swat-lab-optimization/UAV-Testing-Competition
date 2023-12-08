<h1 align="center">
	AmbieGen tool for autonomous UAV testing
</h1>

This repository contains the implementation of our tool AmbieGen, adapted for the [SBFT 2024 UAV testing competition](https://github.com/sbft-cps-tool-competition/cps-tool-competition). This tool is based on our previous search-based tool [AmbieGen](https://github.com/swat-lab-optimization/AmbieGen-tool):
```
@article{HUMENIUK2023102990,
title = {AmbieGen: A search-based framework for autonomous systems testing},
journal = {Science of Computer Programming},
volume = {230},
pages = {102990},
year = {2023},
issn = {0167-6423},
doi = {https://doi.org/10.1016/j.scico.2023.102990},
url = {https://www.sciencedirect.com/science/article/pii/S0167642323000722},
author = {Dmytro Humeniuk and Foutse Khomh and Giuliano Antoniol}
}
```

In AmbieGen, we leverage a single-objective genetic algorithm to evolve randomly produced scenarios representing N randomly placed rectangular obstacles. Ultimate goal is to make the drone fail i.e. come to the obstacles at an unsafe distance. To achieve this, we first evolve the test scenarios based on the perforamce of a planning algorithm, such as RRT, on the provided scene with obstacles. We assume a simple drone trajectory - going forward. When the planning algorithms generates the paths to the targets longer, than a certain threshold, we run the simulation. If a failure is revealed during the simulation we increase the fitness value of a test scenario. We also give an additional reward if less obstacles are used. The search stops when the provided simulation budget expires.

## Usage

### With the host-cli

1. Run:
```python
pip install -r requirements.txt
```
to install the rquirements.  

2. Configure the container:
```
docker build . -t sbft2024_uav_swat
```
3. Create a folder named `results` in the repository's root directory.

3. To run our generator execute the following command:
```python3 
python3 cli.py generate case_studies/mission1.yaml 100
```
###  Inside the container

1. Configure the container:
```
docker build . -t sbft2024_uav_swat
```
2. Run the container:
```
docker run -it --rm sbft2024_uav_swat
```


## Authors
### [Dmytro Humeniuk](https://dgumenyuk.github.io/) and [Foutse Khomh](http://khomh.net/)
Polytechnique Montréal, Canada, 2023  
Contact e-mail: dmytro.humeniuk@polymtl.ca