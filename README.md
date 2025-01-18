# Medical System QA Automation Project

This repository contains automated testing solutions for a cloud-based medical system, focusing on data integrity across AWS, PostgreSQL, and S3 Parquet files.

## Project Overview

The project implements automated testing for:
- Data consistency between PostgreSQL and S3 Parquet files
- API endpoint validation
- Database CRUD operations
- Performance monitoring
- Comprehensive test reporting

## Prerequisites

- AWS Account with appropriate permissions
- PostgreSQL (version 13 or higher)
- Python 
- AWS CLI configured with appropriate credentials
  ```bash
  # Install AWS CLI using Homebrew
  brew install awscli
  ```
- Allure Framework for test reporting
  ```bash
  # Install AWS CLI using Homebrew
  brew install allure
  ```
  
## Installation

1. Clone the repository:
```bash
git clone https://github.com/inbarw/project
cd project
```

2. Install dependencies:
```bash
# For Python implementation
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials and configuration
```

## Running Tests

### Task 1: Database Validation Tests
These tests validate the integrity of data between PostgreSQL and S3, along with CRUD operations.

#### Run All Database Tests
```bash
pytest part_1_2/tests/
```
#### Run Specific Database Test (e.g., Data Loader and Export)
```bash
pytest part_1_2/tests/test_data_loader_and_export.py
```

### Task 2: API Tests
These tests validate the API endpoints of the medical system, ensuring that the API behaves as expected.
#### Run API test
```bash
pytest part_3/tests
```

### Task 3: Generate Test Report
After running the tests, you can generate and view the Allure report for detailed results.
```bash
./run_tests.sh
```
This will run all the tests and generate an Allure report.


## Test Reports
The test reports are generated using the Allure Framework and contain the following information:
- **Test Execution Summary**: Overview of the tests run, including passed/failed tests.
- **Data Validation Results**: Status of data consistency tests.
- **API Test Results**: Status of API endpoint validation tests.
- **Duration of Each Test**: Performance details for each test.
- **Error Details**: Information on any test failures or issues.


## CI/CD Integration
This project includes GitHub Actions workflows for automated testing:
- `.data-integrity-check.yml`: Runs part 1 and 2 tests on push requests

## Troubleshooting

Common issues and solutions:

1. Database Connection Issues:
   - Verify PostgreSQL credentials in `.env`
   - Ensure database service is running
   - Check network connectivity

2. AWS Access Issues:
   - Verify AWS credentials are properly configured
   - Check IAM permissions for S3 access
   - Validate S3 bucket existence and permissions

## Task Information
**Note** I acknowledge that there are opportunities to improve the methods and design, such as addressing code duplication and enhancing error handling. However, due to my limited experience with S3, databases, and mocking, as well as time constraints, my primary focus has been on ensuring the functionality works correctly and the tests pass.
## Part 1: Environment Setup and Data Preparation

### Overview
The PostgreSQL schema for imported data is dynamically created from CSV files. This process involves parsing CSV files, inferring column types (e.g., INT, FLOAT, DATE, VARCHAR(255)), and creating tables in PostgreSQL.

### Process:
1. **CSV File Parsing**: The program reads CSV files and infers column types based on the first few rows.
2. **Table Creation**: Corresponding tables are created in PostgreSQL based on the CSV data.
3. **Column Type Inference**:
   - **INT**: For columns containing integers.
   - **FLOAT**: For columns containing floating-point values.
   - **DATE**: For columns containing date values in `YYYY-MM-DD` format.
   - **VARCHAR(255)**: For other data types or inconsistent data.

### Test for Data Loading and Export to S3
- **Test File**: `test_data_loader_and_export.py`
- This test ensures that data is correctly loaded into the database and exported to S3.

**Note**: There is a missing `lab_results.csv` file, which requires special data handling. This file was not included in the current implementation.

---

## Part 2: Database and Data Validation Tests

These tests focus on validating the data consistency between PostgreSQL and S3, including checking the schema and performing CRUD operations.

### Test Files:
- `test_data_validation.py`
- `test_schema_validation.py`
- `test_crud_operations.py`

### Execution Order:
The tests in part 2 are executed after the data has been loaded and exported to S3. The execution order is controlled using `@pytest.mark.run(order=)` to ensure the `test_data_loader_and_export.py` test runs first.

---

## Part 3: API Tests

The API tests ensure that the medical system's API endpoints function as expected. They test various scenarios such as retrieving medical records, handling errors, and validating response formats.

### Test File:
- `test_medical_records.py`
- This test file validates the functionality of the medical records API.

