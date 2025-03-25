# GaoKao Data Analysis Project

This project is designed for analyzing and visualizing Gaokao (Chinese College Entrance Examination) data.

## Project Structure

```
GaoKaoData/
├── data/                    # Data directory
│   ├── raw/                # Original data files (CSV, Excel, HTML, etc.)
│   └── processed/          # Processed and cleaned data files
├── src/                    # Source code
│   ├── data_processing/    # Data processing scripts
│   └── visualization/      # Visualization scripts
├── output/                 # Output files
│   ├── figures/           # Generated charts and graphs
│   └── reports/           # Analysis reports
├── docs/                   # Documentation
├── tests/                  # Test files
└── requirements.txt        # Project dependencies
```

## Directory Descriptions

- `data/raw/`: Contains original data files in various formats (CSV, Excel, HTML, etc.)
- `data/processed/`: Contains cleaned and processed data files ready for analysis
- `src/data_processing/`: Contains scripts for data cleaning, transformation, and processing
- `src/visualization/`: Contains scripts for generating charts and visualizations
- `output/figures/`: Stores generated charts, graphs, and visualizations
- `output/reports/`: Contains analysis reports and documentation
- `docs/`: Project documentation, including usage guides and API references
- `tests/`: Unit tests and test data

## Setup and Installation

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your raw data files in the `data/raw/` directory
2. Run data processing scripts from `src/data_processing/`
3. Generate visualizations using scripts from `src/visualization/`
4. Find generated outputs in the `output/` directory

## Dependencies

- pandas: Data manipulation and analysis
- matplotlib: Basic plotting
- seaborn: Statistical visualizations
- plotly: Interactive visualizations
- jupyter: Interactive notebooks for analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
