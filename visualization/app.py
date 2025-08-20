#!/usr/bin/env python3
"""
LLM Math Evaluation Results Visualization Website
A Flask web application for visualizing and analyzing LLM evaluation results on math datasets.
"""

import os
import json
import glob
from flask import Flask, render_template, request, jsonify
from collections import defaultdict
import re

app = Flask(__name__)

class DataLoader:
    def __init__(self, outputs_dir):
        self.outputs_dir = outputs_dir
        self.data = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Load all evaluation results from the outputs directory."""
        # Find all model directories
        model_dirs = [d for d in os.listdir(self.outputs_dir) 
                     if os.path.isdir(os.path.join(self.outputs_dir, d))]
        
        for model_dir in model_dirs:
            model_path = os.path.join(self.outputs_dir, model_dir)
            datasets = [d for d in os.listdir(model_path) 
                       if os.path.isdir(os.path.join(model_path, d))]
            
            for dataset in datasets:
                dataset_path = os.path.join(model_path, dataset)
                metrics_files = glob.glob(os.path.join(dataset_path, "*_metrics.json"))
                result_files = glob.glob(os.path.join(dataset_path, "*.jsonl"))
                
                if metrics_files and result_files:
                    # Load metrics
                    with open(metrics_files[0], 'r') as f:
                        metrics = json.load(f)
                    
                    # Load detailed results
                    results = []
                    with open(result_files[0], 'r') as f:
                        for line in f:
                            if line.strip():
                                results.append(json.loads(line))
                    
                    key = f"{model_dir}_{dataset}"
                    self.data[key] = {
                        'model': model_dir,
                        'dataset': dataset,
                        'metrics': metrics,
                        'results': results
                    }
    
    def get_summary_stats(self):
        """Get summary statistics for all models and datasets."""
        summary = []
        for key, data in self.data.items():
            summary.append({
                'model': data['model'],
                'dataset': data['dataset'],
                'accuracy': data['metrics']['acc'],
                'num_samples': data['metrics']['num_samples'],
                'time_minutes': data['metrics']['time_use_in_minite'],
                'empty_samples': data['metrics']['empty_samples'],
                'timeout_samples': data['metrics']['timeout_samples']
            })
        return summary
    
    def get_detailed_results(self, model=None, dataset=None, correct_only=None, 
                           difficulty_level=None, question_contains=None):
        """Get filtered detailed results."""
        results = []
        
        for key, data in self.data.items():
            if model and data['model'] != model:
                continue
            if dataset and data['dataset'] != dataset:
                continue
            
            for result in data['results']:
                # Apply filters
                if correct_only is not None:
                    if correct_only and not result['score'][0]:
                        continue
                    if not correct_only and result['score'][0]:
                        continue
                
                if difficulty_level is not None:
                    if result.get('level') != difficulty_level:
                        continue
                
                if question_contains:
                    if question_contains.lower() not in result['question'].lower():
                        continue
                
                # Add model and dataset info to result
                result_copy = result.copy()
                result_copy['model'] = data['model']
                result_copy['dataset'] = data['dataset']
                results.append(result_copy)
        
        return results

# Initialize data loader
data_loader = DataLoader('simplelr_math_eval/outputs')

@app.route('/')
def index():
    """Main dashboard page."""
    summary_stats = data_loader.get_summary_stats()
    return render_template('index.html', summary_stats=summary_stats, summary_stats_json=json.dumps(summary_stats))

@app.route('/api/summary')
def api_summary():
    """API endpoint for summary statistics."""
    return jsonify(data_loader.get_summary_stats())

@app.route('/case_study')
def case_study():
    """Case study browser page."""
    # Get available models and datasets
    models = set()
    datasets = set()
    levels = set()
    
    for key, data in data_loader.data.items():
        models.add(data['model'])
        datasets.add(data['dataset'])
        for result in data['results']:
            if 'level' in result:
                levels.add(result['level'])
    
    return render_template('case_study.html', 
                         models=sorted(models), 
                         datasets=sorted(datasets),
                         levels=sorted(levels))

@app.route('/api/cases')
def api_cases():
    """API endpoint for filtered case results."""
    model = request.args.get('model')
    dataset = request.args.get('dataset')
    correct_only = request.args.get('correct_only')
    difficulty_level = request.args.get('difficulty_level')
    question_contains = request.args.get('question_contains')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    # Convert string parameters to appropriate types
    if correct_only == 'true':
        correct_only = True
    elif correct_only == 'false':
        correct_only = False
    else:
        correct_only = None
    
    if difficulty_level:
        try:
            difficulty_level = int(difficulty_level)
        except ValueError:
            difficulty_level = None
    
    results = data_loader.get_detailed_results(
        model=model,
        dataset=dataset,
        correct_only=correct_only,
        difficulty_level=difficulty_level,
        question_contains=question_contains
    )
    
    # Pagination
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]
    
    return jsonify({
        'results': paginated_results,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })

@app.route('/comparison')
def comparison():
    """Model comparison page."""
    return render_template('comparison.html')

@app.route('/api/comparison_data')
def api_comparison_data():
    """API endpoint for model comparison data."""
    summary_stats = data_loader.get_summary_stats()
    
    # Group by dataset for comparison
    comparison_data = defaultdict(list)
    for stat in summary_stats:
        comparison_data[stat['dataset']].append(stat)
    
    return jsonify(dict(comparison_data))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
