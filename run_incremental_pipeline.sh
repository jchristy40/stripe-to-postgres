#!/bin/bash

# Absolute path to project directory
PROJECT_DIR="/home/ubuntu/stripe-to-postgres"

# Activate the virtual environment
source "$PROJECT_DIR/venv/bin/activate"

# Navigate to the project directory
cd "$PROJECT_DIR"

# Run the pipeline

python stripe_analytics_pipeline.py --dataset-name public incremental_load



# Deactivate the virtual environment (optional)
deactivate
