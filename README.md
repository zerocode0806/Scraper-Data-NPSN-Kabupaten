# NPSN School Scraper (Playwright)

## Overview

This project is a **Python web scraper** that collects Indonesian school data (NPSN and School Name) from the official **Kemendikdasmen Referensi Pendidikan website**.

The script automatically:

* Retrieves **all districts (kecamatan)** from a selected region page.
* Visits each district page.
* Extracts **NPSN, School Name, and NPSN Detail Link**.
* Handles **pagination automatically**.
* Uses **multi-threading** to speed up scraping.
* Exports results to an **Excel file**.

The scraper supports multiple education levels simply by changing the `BASE_URL`.

---

## Data Collected

For each school the scraper extracts:

| Field                  | Description                           |
| ---------------------- | ------------------------------------- |
| Kecamatan              | District where the school is located  |
| NPSN                   | National School Identification Number |
| Nama_Satuan_Pendidikan | Official school name                  |
| Link_NPSN              | Detail page link of the school        |

---

## Supported Education Levels

The scraper works for multiple education levels from the **Referensi Data Kemendikdasmen** website.

| Level | Example URL                     |
| ----- | ------------------------------- |
| SD    | `/pendidikan/dikdas/...`        |
| SMP   | `/pendidikan/dikdas/...`        |
| SMA   | `/pendidikan/dikmen/.../13/...` |
| SMK   | `/pendidikan/dikmen/.../15/...` |

You only need to modify **BASE_URL**.

Example:

### SMA

```
https://referensi.data.kemendikdasmen.go.id/pendidikan/dikmen/050200/2/jf/13/all
```

### SMK

```
https://referensi.data.kemendikdasmen.go.id/pendidikan/dikmen/050200/2/jf/15/all
```

---

# Requirements

Install the required dependencies:

```
pip install playwright pandas
```

Then install Playwright browser:

```
playwright install
```

---

# How To Run

1. Clone or download this project

2. Install dependencies

```
pip install playwright pandas
playwright install
```

3. Open the Python script and edit:

```
BASE_URL = "YOUR_TARGET_URL"
OUTPUT_FILE = "output.xlsx"
```

Example for SMK:

```
BASE_URL = "https://referensi.data.kemendikdasmen.go.id/pendidikan/dikmen/050200/2/jf/15/all"
```

4. Run the script

```
python scraper.py
```

---

# Output

After the scraping process completes, an Excel file will be generated:

```
data_sekolah_smk.xlsx
```

Example structure:

| Kecamatan | NPSN     | Nama_Satuan_Pendidikan | Link_NPSN            |
| --------- | -------- | ---------------------- | -------------------- |
| Tarik     | 20582212 | SMK Negeri 1 Tarik     | https://referensi... |

---

# Features

* Multi-thread scraping
* Automatic pagination handling
* Retry mechanism for failed page loads
* Flexible for multiple education levels
* Excel export using Pandas
* Headless browser support

---

# Configuration

Inside the script you can configure:

| Variable      | Description                  |
| ------------- | ---------------------------- |
| `BASE_URL`    | Target page to scrape        |
| `OUTPUT_FILE` | Output Excel filename        |
| `MAX_WORKERS` | Number of concurrent threads |
| `MAX_RETRY`   | Retry attempts if page fails |
| `HEADLESS`    | Run browser in background    |

Example:

```
MAX_WORKERS = 4
HEADLESS = True
```

Increasing workers can improve speed but may increase server load.

---

# Notes

* The scraper depends on the structure of the **Referensi Kemendikdasmen website**.
* If the website layout changes, selectors may need to be updated.
* Avoid setting very high thread counts to prevent server blocking.

---

# Disclaimer

This project is intended for **educational and research purposes only**.

Please ensure that scraping complies with the website's terms of service and use reasonable request rates.

---

# Author

Developed using:

* Python
* Playwright
* Pandas
