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

# For Java implementation
mvn install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials and configuration
```

## Part 1: Environment Setup

### Database Schema

The PostgreSQL schema for the imported data is dynamically created from CSV files. The following steps describe the schema generation process:
1. CSV File Parsing: The program reads CSV files, infers column types (INT, FLOAT, DATE, or VARCHAR(255)), and uses this information to create the schema for each table.
2. Table Creation: A table is created in PostgreSQL using the inferred column types. The table name corresponds to the CSV file name (without the .csv extension).
3. Column Type Inference: The column data types are determined based on the first few rows in the CSV file. The following rules are applied:
   * INT: For columns containing integer values.
   * FLOAT: For columns containing floating-point values.
   * DATE: For columns containing dates in YYYY-MM-DD format.
   * VARCHAR(255): For columns with other or inconsistent data types.

### S3 Bucket Structure

## Running Tests

### Database Validation Tests
```bash
# Run all database tests
pytest part_1/tests/

# Run specific test suite
pytest part_1/tests/test_data_loader_and_export.py
```

### API Tests
```bash
# Run all API tests
pytest part_3/tests

# Run performance tests only
pytest part_3/tests/test_medical_records.py
```

### Generate Test Report
```bash
run_tests.sh
```

## Test Reports

- Reports are generated using Allure Framework
- Access the report dashboard at `http://localhost:5000` after running the report server
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
