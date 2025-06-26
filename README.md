# CMS Hospital Data Downloader
## Features

- Downloads only "Hospital" datasets in CSV format.
- Converts all column names in CSV headers to snake_case.
- Processes multiple datasets in parallel using threads.
- Tracks last run metadata to avoid re-downloading unchanged files.
- Cross-platform: works on Windows and Linux.

## Requirements
- Python 3.7+
- [requests](https://pypi.org/project/requests/)


## Usage
1. Clone this repository and navigate to the project directory.
2. Run the script:
```sh
python index.py
```
3. Processed CSV files will be saved in the `cms_data` directory.
4. Metadata about processed files is stored in `last_run_metadata.json`.

## Output Example
You will see output like:

```
[ThreadPoolExecutor-0_3] Downloading and processing: Complications and Unplanned Hospital Visits - PPS-Exempt Cancer Hospital - Hospital
 Processed: Complications and Unplanned Hospital Visits - PPS-Exempt Cancer Hospital - Hospital
[ThreadPoolExecutor-0_3] Downloading and processing: Complications and Unplanned Hospital Visits - PPS-Exempt Cancer Hospital - National
 Processed: Complications and Unplanned Hospital Visits - PPS-Exempt Cancer Hospital - National
[ThreadPoolExecutor-0_3] Downloading and processing: Hospital-Acquired Condition (HAC) Reduction Program
 Processed: Hospital General Information
 All done.
```

## Notes

- Only the `requests` package is required, all other modules are part of the Python standard library.
---
