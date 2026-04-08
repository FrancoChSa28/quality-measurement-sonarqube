# Quality Measurement SonarQube Report Analyzer

This project is a tool for analyzing and exporting issues from SonarQube reports. It processes the issues, retrieves relevant code snippets, and generates a detailed JSON report.

## Project Structure
```
quality-measurement-sonarqube/
├── get_issues.py
├── settings.yml
├── requirements.txt
├── README.md
```

### Key Files

- **`get_issues.py`**: The main script for fetching and processing issues from SonarQube. It retrieves issues, caches rule titles, and exports a detailed JSON report.
- **`settings.yml`**: Configuration file for SonarQube server URL, project key, severities, and other settings.
- **`requirements.txt`**: Lists the Python dependencies required for the project.
- **`sonarqube_report_data-{PROJECT_KEY}.json`**: The output file containing the processed issues and their details.

## Prerequisites

- Python 3.10 or higher
- A virtual environment is recommended for managing dependencies.

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Generador-de-FUA
   ```

2. Create and activate a virtual environment:
    ```
    python -m venv .env
    source .env/Scripts/activate  # On Windows
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Configure the `settings.yml` file:
    - Set the server-url to your SonarQube server.
    - Provide the project-key for the project you want to analyze.
    - Add your SonarQube authentication cookies under cookies.
    - Sample:
    ```yaml
    sonarqube:
        server-url: ""
        project-key: ""
        severity:
            - "BLOCKER"
            - "CRITICAL"
            - "MAJOR"
            - "MINOR"
            - "INFO"
        context-lines: 5
        impact:
            software-qualities:
            - "RELIABILITY"
            - "SECURITY"
            - "MAINTAINABILITY"
            severities:
            - "BLOCKER"
            - "HIGH"
            - "MEDIUM"
    cookies:
        JWT-SESSION: ""
        XSRF-TOKEN: ""
    ```

## Usage
Run the `get_issues.py` script to fetch and process issues from SonarQube:
```bash
python get_issues.py
```

The script will:
1. Fetch issues from the SonarQube server.
2. Retrieve code snippets for each issue.
3. Export the processed data to sonarqube_report_data-{PROJECT_KEY}.json.

## Output
The output JSON file contains:
* Issue descriptions
* File paths and line numbers
* Rule titles and severities
* Code snippets for context

## Example Output
```json
{
  "project": "Generador-de-FUA",
  "total_issues": 125,
  "issues": [
    {
      "message": "Remove this commented out code.",
      "file": "src/controllers/FUAFormatFromSchemaController.ts",
      "line": 236,
      "rule_key": "typescript:S125",
      "rule_title": "Sections of code should not be commented out",
      "severity": "MAJOR",
      "type": "CODE_SMELL",
      "source_code": "..."
    }
  ]
}
```

## Contributing
Feel free to submit issues or pull requests to improve this project.

## Licence
This project is licensed under the MIT License.