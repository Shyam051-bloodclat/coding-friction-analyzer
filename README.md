# Coding Friction Analyzer

A Python-Flask based system that analyzes student programming attempts, identifies coding errors, and records performance data for future machine-learning-based coding difficulty analysis.

## Overview

Traditional coding platforms mainly tell students whether their submission is correct or incorrect.

The Coding Friction Analyzer goes a step further by analyzing coding attempts, identifying errors, and recording information such as solving time, attempt number, topic, difficulty, result, and error type.

The collected data can later be used to identify recurring coding difficulties and provide targeted practice recommendations.

## Features

- Python programming problem selection
- Controlled test-case based code evaluation
- Syntax error detection
- Runtime error detection
- Wrong-answer detection
- Function and parameter validation
- AST-based Python code analysis
- Error type identification
- Attempt tracking
- Solving time tracking
- Topic and difficulty tracking
- CSV-based attempt data collection
- Planned machine-learning-based coding friction analysis
- Planned personalized practice recommendations

## System Workflow

```text
Student
   ↓
Select Problem
   ↓
Submit Python Code
   ↓
Code Analysis
   ↓
Test Cases
   ↓
Record Attempt
   ↓
Feature Extraction
   ↓
Machine Learning
   ↓
Friction Profile
   ↓
Targeted Recommendations