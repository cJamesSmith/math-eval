# LLM Math Evaluation Results Visualization

A comprehensive web application for visualizing and analyzing Large Language Model (LLM) evaluation results on mathematical reasoning tasks.

## 📊 Features

### 🏠 Dashboard
- **Summary Statistics**: Overview of model performance across all datasets
- **Interactive Charts**: Visual comparison of accuracy and processing time
- **Performance Metrics**: Detailed statistics including accuracy, processing time, empty responses, and timeouts

### 🔍 Case Study Browser
- **Detailed Question Analysis**: Browse individual questions and model responses
- **Advanced Filtering**: Filter by model, dataset, correctness, difficulty level, and question content
- **Interactive UI**: Expandable question details with model reasoning and reference solutions
- **LaTeX Support**: Mathematical expressions rendered with MathJax
- **Pagination**: Efficient browsing of large datasets

### ⚖️ Model Comparison
- **Side-by-Side Analysis**: Compare different model configurations
- **Visual Charts**: Bar charts, radar charts, and scatter plots for comprehensive analysis
- **Head-to-Head Comparison**: Direct comparison between two selected models
- **Efficiency Analysis**: Performance vs processing time visualization

## 🏗️ Project Structure

```
math-eval/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── start_server.sh       # Startup script
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Dashboard page
│   ├── case_study.html   # Case study browser
│   └── comparison.html   # Model comparison page
└── static/              # Static files (CSS, JS, images)
```

## 📁 Data Structure

The application expects evaluation results in the following structure:

```
simplelr_math_eval/outputs/
├── model-name-1/
│   └── dataset-name/
│       ├── test_*_metrics.json    # Performance metrics
│       └── test_*.jsonl           # Detailed results
└── model-name-2/
    └── dataset-name/
        ├── test_*_metrics.json
        └── test_*.jsonl
```

### Metrics File Format (JSON)
```json
{
    "num_samples": 500,
    "num_scores": 500,
    "timeout_samples": 0,
    "empty_samples": 1,
    "acc": 73.2,
    "pass_acc": 73.2,
    "pass@k": {"1": 73.2},
    "time_use_in_second": 189.97,
    "time_use_in_minite": "3:09"
}
```

### Results File Format (JSONL)
Each line contains a JSON object with:
```json
{
    "idx": 0,
    "question": "Question text...",
    "gt_cot": "Ground truth chain of thought...",
    "gt": "Ground truth answer",
    "level": 2,
    "answer": "Answer",
    "code": ["Model reasoning..."],
    "pred": ["Model prediction"],
    "score": [true/false],
    "finish_reason": ["stop"]
}
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- LLM evaluation results in the expected format

### Installation & Usage

1. **Clone or navigate to the project directory**
   ```bash
   cd /path/to/math-eval
   ```

2. **Start the application**
   ```bash
   ./start_server.sh
   ```

   This script will:
   - Create a virtual environment (if not exists)
   - Install dependencies
   - Start the Flask development server

3. **Access the application**
   - Dashboard: http://localhost:5000
   - Case Studies: http://localhost:5000/case_study
   - Model Comparison: http://localhost:5000/comparison

### Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py
```

## 🔧 Configuration

### Data Directory
The application loads data from `/home/aiops/chenxw/math-eval/simplelr_math_eval/outputs` by default. 

To change the data directory, modify the `DataLoader` initialization in `app.py`:

```python
data_loader = DataLoader('/path/to/your/outputs/directory')
```

### Server Configuration
- **Host**: `0.0.0.0` (accessible from any IP)
- **Port**: `5000`
- **Debug Mode**: Enabled for development

To modify these settings, update the `app.run()` call in `app.py`.

## 📊 Available Models and Datasets

Based on your current data structure:

### Models
- `long-cot-Qwen3-4B-Base`
- `long-cot-boxed-Qwen3-4B-Base`  
- `qwen-boxed-Qwen3-4B-Base`
- `qwen25-math-cot-Qwen3-4B-Base`

### Datasets
- `math500`

## 🔍 API Endpoints

### GET `/api/summary`
Returns summary statistics for all models and datasets.

### GET `/api/cases`
Returns filtered case results with pagination.

**Parameters:**
- `model`: Filter by model name
- `dataset`: Filter by dataset name
- `correct_only`: Filter by correctness (true/false)
- `difficulty_level`: Filter by difficulty level
- `question_contains`: Search in question text
- `page`: Page number (default: 1)
- `per_page`: Results per page (default: 20)

### GET `/api/comparison_data`
Returns data grouped by dataset for model comparison.

## 🎨 Customization

### Adding New Visualizations
1. Add new chart canvas elements in the HTML templates
2. Implement chart rendering functions in JavaScript
3. Add corresponding API endpoints if needed

### Styling
- Modify the CSS in `templates/base.html`
- Add custom stylesheets to the `static/` directory
- Bootstrap 5 classes are available throughout

### Adding New Filters
1. Add form elements in `case_study.html`
2. Update the `get_detailed_results()` method in `app.py`
3. Update the JavaScript filtering logic

## 🐛 Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   ```bash
   # Kill existing process
   sudo lsof -ti:5000 | xargs kill -9
   ```

2. **Data not loading**
   - Check that the data directory path is correct
   - Verify that JSON/JSONL files are valid
   - Check browser console for JavaScript errors

3. **MathJax not rendering**
   - Ensure internet connection (MathJax loads from CDN)
   - Check browser console for loading errors

## 📈 Performance Notes

- The application loads all data into memory on startup
- For large datasets (>10K samples), consider implementing database storage
- Pagination is used to improve browser performance with large result sets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the repository for license details.

---

🎯 **Happy analyzing!** This tool should help you gain comprehensive insights into your LLM evaluation results.
