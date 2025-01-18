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

### Database Validation Tests
```bash
# Run all database tests
pytest part_1_2/tests/

# Run specific test
pytest part_1_2/tests/test_data_loader_and_export.py
```

### API Tests
```bash
# Run all API tests
pytest part_3/tests

# Run specific test (there is just one - in case there are more)
pytest part_3/tests/test_medical_records.py
```

### Generate Test Report
```bash
./run_tests.sh
```

## Test Reports

- Reports are generated using Allure Framework
- Reports include:
  - Test execution summary
  - Data validation results
  - API response times
  - Error details

## CI/CD Integration

This project includes GitHub Actions workflows for automated testing:
- `.data-integrity-check.yml`: Runs all tests on push requests

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

## Task info
* I know that there are methods/design that can be improved/duplicate of code, but I'm not that familiar with s3/db/mock, and because there is limited time, there are parts that I focused on the functionality, in order the test to run/pass 

### Part 1: Environment Setup and Data Preparation

The PostgreSQL schema for the imported data is dynamically created from CSV files. The following steps describe the schema generation process:
1. CSV File Parsing: The program reads CSV files, infers column types (INT, FLOAT, DATE, or VARCHAR(255)), and uses this information to create the schema for each table.
2. Table Creation: A table is created in PostgreSQL using the inferred column types. The table name corresponds to the CSV file name (without the .csv extension).
3. Column Type Inference: The column data types are determined based on the first few rows in the CSV file. The following rules are applied:
   * INT: For columns containing integer values.
   * FLOAT: For columns containing floating-point values.
   * DATE: For columns containing dates in YYYY-MM-DD format.
   * VARCHAR(255): For columns with other or inconsistent data types.
   
* Test for loading the data and export to s3 is test_data_loader_and_export.py
* I know that lab_results.csv isn't is missing from the uploaded file, it required handling special data, and I didn't get to this 

## Part 2: Database and Data Validation Tests
* Tests for data validation: test_data_validation.py, test_schema_validation.py and test_crud_operations.py
* Tests with part 1 test aren't by order (using @pytest.mark.run(order=)), to ensure that part 1 test (load and export to s3) will run first
* I know that there is code duplication in all the tests, also the design of the class/method can be improved

## Part 3: API Tests
* Test for api test_medical_records.py


