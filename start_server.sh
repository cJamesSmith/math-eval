#!/bin/bash

# Start the Flask application
echo "🌐 Starting Flask application on http://localhost:5000"
echo "📊 Dashboard: http://localhost:5000"
echo "🔍 Case Studies: http://localhost:5000/case_study"
echo "🔬 Differential Analysis: http://localhost:5000/differential"
echo ""
echo "Press Ctrl+C to stop the server"

python visualization/app.py
