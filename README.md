# Red Scare - ALDES 2025


## Overview
This repository contains our solutions and tooling for the Red Scare project in MSc Algorithm Design at ITU Copenhagen. The full exercise description is available in `doc/red-scare.pdf` and the report template can be found in `doc/report.tex`.


## Setup

`generate_results.py` runs the available solvers on every `.txt` instance in `data/` and writes the tab-separated summary required in the report.

1. Clone the repository:
	```powershell
	git clone https://github.com/Josh0104/red-scare-aldes-2025.git
	```
2. From the repository root run:
	```powershell
	py generate_results.py
	```
	This command runs all algorithms and saves the results into `results.txt`.


## Results

The results.txt contains tab-separated results for all algorithms on all graphs in the data folder.

Marking:
- `n`: number of vertices in the data file
- `A`: Alternate algorithm results
- `F`: Few algorithm results
- `M`: Many algorithm results
- `N`: None algorithm results
- `S`: Some algorithm results
- `?`: Result inconclusive / runtime exceeds limit


## Contributors

Joshua James Medilo Calba, Mohtashim Haider, Jobayer Hossain, Miina Johanna Mäkinen, Samikshya Rana, Courage Räsänen

- Course: M.Sc. Algorithm Design
- University: IT University Copenhagen
- Year: 2025
