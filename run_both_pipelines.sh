#!/bin/bash

# Absolute path to project directory
PROJECT_DIR="/home/ubuntu/stripe-to-postgres"

# Activate the virtual environment
source "$PROJECT_DIR/venv/bin/activate"

# Navigate to the project directory
cd "$PROJECT_DIR"

# Run the pipeline

python stripe_analytics_pipeline.py --dataset-name public incremental_load
python stripe_analytics_pipeline.py --dataset-name public full_load --skip-incremental-endpoints




# Deactivate the virtual environment (optional)
deactivate
