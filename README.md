# Tools

This repository contains a toolkit for EPT (End-to-End Performance Tracking) data analysis.

## EPTBreakdownTools

EPTBreakdownTools is a comprehensive Python toolkit for analyzing and visualizing EPT performance data. These tools help you process, convert, and visualize EPT raw data.

### Tool Components

#### 1. CombineCSV.py
A tool for merging multiple CSV output files.
- **Functionality**: Combines multiple `output_*.csv` files into a single `output.csv` file
- **Features**: 
  - Automatically skips duplicate header rows
  - Deduplication processing to ensure only the first header row is kept
- **Usage**: Run the script directly, ensuring target CSV files are in the same directory

#### 2. ConvertEPTRawDataToJson.py
A tool for converting EPT raw data to standard JSON format.
- **Functionality**: Fixes JSON format issues in raw data
- **Features**:
  - Automatically adds missing quotes
  - Fixes key-value pair formatting
  - Handles nested JSON structures
- **Usage**: 
  ```bash
  python ConvertEPTRawDataToJson.py <raw_data_file>
  ```

#### 3. ParseJsonFinal.py
Parses JSON data and generates detailed performance metrics CSV reports.
- **Functionality**: Extracts performance metrics from EPT JSON data and generates structured reports
- **Features**:
  - Extracts 25 core performance metrics
  - Processes async module loading data
  - Handles font download data
  - Generates timeline-sorted CSV reports
- **Usage**:
  ```bash
  python ParseJsonFinal.py <raw_data_file> <run_index> [remove_postfix]
  ```
  - `raw_data_file`: Path to the raw data file
  - `run_index`: Run index number
  - `remove_postfix`: Optional, whether to remove font name and async module name suffixes (true/false)

#### 4. VisualizeEPTBreakdown/
Subdirectory containing data visualization tools.

##### VisualizeEPTBreakdown.py
A tool for generating EPT performance event timeline charts.
- **Functionality**: Creates event timeline visualizations from JSON data
- **Features**:
  - Generates horizontal timeline charts
  - Displays start time and duration for each event
  - Supports nested event structures
- **Usage**:
  ```bash
  python VisualizeEPTBreakdown.py <filename.json>
  ```

##### RawEPTBreakdown.json
Sample EPT data file containing timeline data for performance metrics.

#### 5. EPT_Breakdown_Viz.twbx
Tableau workbook file for advanced data visualization and analysis.

### Workflow

1. **Data Conversion**: Use `ConvertEPTRawDataToJson.py` to convert raw EPT data to standard JSON format
2. **Data Parsing**: Use `ParseJsonFinal.py` to extract performance metrics from JSON data and generate CSV reports
3. **Data Merging**: Use `CombineCSV.py` to merge results from multiple runs
4. **Data Visualization**: Use `VisualizeEPTBreakdown.py` to generate timeline charts, or use the Tableau workbook for advanced analysis

### Performance Metrics

The main performance metrics extracted by the tools include:
- **Time To First Byte (ep)**: Time to first byte
- **Static Html Start Loading (dl)**: Static HTML start loading time
- **Load Static Html (lsh)**: Load static HTML time
- **Prepare Start Session (pss)**: Prepare start session time
- **Start Session (ss)**: Start session time
- **Load Css (lcss)**: Load CSS time
- **Vizclient Application Startup (appstr)**: Vizclient application startup time
- **Vizclient Becomes Interactive (appint)**: Vizclient becomes interactive time
- **Async Modules Load**: Async module loading time
- **Download Fonts**: Font download time

### Dependencies

- Python 3.x
- pandas
- matplotlib
- json (built-in)
- re (built-in)
- sys (built-in)
- os (built-in)
- math (built-in)

### Installation

```bash
pip install pandas matplotlib
```