#!/bin/bash

# Start the Flask application
echo "🌐 Starting Flask application on http://localhost:5000"
echo "📊 Dashboard: http://localhost:5000"
echo "🔍 Case Studies: http://localhost:5000/case_study"
echo "⚖️ Model Comparison: http://localhost:5000/comparison"
echo ""
echo "Press Ctrl+C to stop the server"

python visualization/app.py
