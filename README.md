# COVID-19

[![version](https://img.shields.io/badge/version-0.1.0-yellow.svg)](https://semver.org)
[![Python 3.8.5](https://img.shields.io/badge/python-3.8.5-blue.svg)](https://www.python.org/downloads/release/python-376/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

This is a demo of using Azure DevOps for Agile data science at scale.  A single Python script was develop to analyze a running history of daily increases in positive cases of COVID-19 in the United States.

## Files

Files in this project are organized as follows:

```bash
.
├── README.md
├── REFERENCES.md
├── azure-pipelines.yml
├── data/
│   ├── 01_raw/
│   │   └── daily_extract_data.csv
│   ├── 02_intermediate/
│   │   ├── daily_add_columns.csv
│   │   ├── daily_rename_columns.csv
│   │   └── weekly_add_columns.csv
│   └── 03_processed/
├── docs/
├── notebooks/
├── references/
├── results/
│   ├── plot_series.png
│   ├── summarize_dow.png
│   ├── summarize_dow_percent.png
│   ├── summarize_dow_zscore.png
│   └── summarize_maxima.png
└── src/
    └── main.py
```

### Source Code

This project requires a single [Python](https://www.python.org) v3.7.6 script file, `main.py`, to do the following:

1. Download source data;
2. Extract key measurements and categorical data;
3. Shape the data via integration and the derivation of new data in preparation for visualization and summarization;
4. Appropriately label processed data set with descriptive variable names;
5. Create artifacts in the form of visualizations and summaries comprising the final results set.

This script has 3 third-party package dependencies:

* [`matplotlib`](https://matplotlib.org)
* [`pandas`](https://pandas.pydata.org)
* [`seaborn`](https://seaborn.pydata.org)

These package dependencies come preloaded with the [Anaconda](https://www.anaconda.com/products/individual) distribution of Python.

### Source Data

All source data used in this project can be found using the [Data API](https://covidtracking.com/data/api) from the [COVID Tracking Project](https://covidtracking.com/).  The full URL of this API's endpoint is:

`https://covidtracking.com/data/api/v1/us/`

Key files from this source are:

* `daily.csv`

A full description of this data is available in the *Historic US Values* section of the site where it was obtained:

`https://covidtracking.com/data/api`

### Target Data

TODO: List the final target data processed after running `main.py`.

### Results

The following figures are visual summaries of daily counts of new positive incidents of COVID-19 in the United States.

![Time series](results/plot_series.png)
![Local maxima](results/summarize_maxima.png)
![Day of week](results/summarize_dow.png)
![Day of week by percentage](results/summarize_dow_percent.png)
![Day of week by z-score](results/summarize_dow_zscore.png)

### Documentation

One documentation file is required to be included in the GitHub repository for this project:

* `README.md`: This file, the intention of which is to clearly and understandably explain how all of the scripts work and how they are connected with the other analysis files cited here.

## Protocol

1. Extract data.
    1. Download the source data as a CSV file.
    2. Read the source data into a `pandas` data frame.
    3. Save a raw copy of the source data.
2. Transform data.
    1. Rename data columns.
    2. Add data columns.
3. Visualize data.
    1. Set graphic figure defaults.
    2. Generate and save graphic figures.

## Known Issues

Currently, there are no known issues.  If you discover any, please kindly submit a [pull request](CONTRIBUTING.md).

## Contributing

Code and codeless (e.g., documentation) contributions toward improving the COVID-19 project are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for more information on how to become a contributor.

## License

The COVID-19 project is released under the [MIT License](LICENSE).

## References

See [REFERENCES.md](REFERENCES.md) for a list of these.
