import os
from flask import Flask, jsonify, request, send_from_directory
from filters import get_filter_options, filter_data, calculate_kpis
import charts

app = Flask(__name__)

# Serve static files from root directory
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

# Serve static images if any
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# API - Get filter options
@app.route('/api/filters', methods=['GET'])
def api_filters():
    try:
        options = get_filter_options()
        return jsonify(options)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API - Get dashboard data (KPIs & base64 chart images)
@app.route('/api/dashboard', methods=['POST'])
def api_dashboard():
    try:
        filters = request.json or {}
        
        # 1. Filter Data
        filtered_matches, filtered_deliveries = filter_data(filters)
        
        # 2. Calculate KPIs
        kpis = calculate_kpis(filtered_matches, filtered_deliveries)
        
        # 3. Generate Charts (Base64 encoded strings)
        chart_images = {
            "toss_decision": charts.get_toss_decision_chart(filtered_matches),
            "target_runs_hist": charts.get_target_runs_histogram(filtered_matches),
            "matches_trend": charts.get_matches_trend_chart(filtered_matches),
            "top_winners": charts.get_top_winners_chart(filtered_matches),
            "target_vs_margin": charts.get_target_vs_margin_scatter(filtered_matches),
            "margin_box": charts.get_margin_boxplot(filtered_matches),
            "correlation_heat": charts.get_correlation_heatmap(filtered_matches),
            "cumulative_wins": charts.get_cumulative_wins_area(filtered_matches),
            "cities_count": charts.get_cities_countplot(filtered_matches),
            "target_violin": charts.get_target_runs_violin(filtered_matches)
        }
        
        # 4. Return response
        return jsonify({
            "kpis": kpis,
            "charts": chart_images,
            "record_count": len(filtered_matches)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Local Dev Server
    print("Starting IPL EDA Dashboard dev server...")
    print("Go to http://localhost:5000 in your browser.")
    app.run(debug=True, host='0.0.0.0', port=5000)
