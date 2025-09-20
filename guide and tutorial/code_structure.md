****Code Structure Guide
This document explains the organization of our Cafe Billing System project codebase to help you navigate and contribute effectively.****

## **_Project Root-_**
*    .gitignore - Specifies files and folders excluded from Git version control.

*    LICENSE - Project license details (MIT License).

*    README.md - Main project overview and setup instructions.

*    requirements.txt - List of Python package dependencies.
 
*    .venv/ - Python virtual environment folder containing installed packages (do not modify directly).
 

## **_Directories-_**

#### src/

This folder holds all Python source code for the project’s core functionality.

* main.py - Entry point of the application; the main program runner.

* db.py - Database connection and query execution code.

* orders.py - Order management logic including creating and updating customer orders.

* billing.py - Handles calculation of bills, discounts, and generating receipts.

## **_sql/_**

Contains SQL scripts to setup and seed the database.

* schema.sql - SQL commands to create database tables and relationships.

* seed.sql - Inserts sample data into the database to get started quickly.

reports/
Reserved for scripts that generate reports such as daily sales summaries or customer activity reports. This folder may be empty initially and files will be added as needed.