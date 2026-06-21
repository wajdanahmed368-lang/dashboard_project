document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('filters-form');
    const resetBtn = document.getElementById('btn-reset');
    const searchInput = document.getElementById('filter-search');
    const seasonSelect = document.getElementById('filter-season');
    const startDateInput = document.getElementById('filter-start-date');
    const endDateInput = document.getElementById('filter-end-date');
    const marginSlider = document.getElementById('filter-margin');
    const marginValueLabel = document.getElementById('margin-value');
    const teamsContainer = document.getElementById('teams-multiselect');
    const playerSelect = document.getElementById('filter-player');
    
    // Header & KPIs Elements
    const recordCountBadge = document.getElementById('record-count');
    const kpiMatches = document.getElementById('kpi-matches');
    const kpiRuns = document.getElementById('kpi-runs');
    const kpiAvgTarget = document.getElementById('kpi-avg-target');
    const kpiTossImpact = document.getElementById('kpi-toss-impact');
    const kpiTopPlayer = document.getElementById('kpi-top-player');

    // Chart image elements
    const chartIds = [
        'toss_decision', 'target_runs_hist', 'matches_trend', 'top_winners', 
        'target_vs_margin', 'margin_box', 'correlation_heat', 'cumulative_wins', 
        'cities_count', 'target_violin'
    ];
    
    // Store metadata
    let filterMetadata = {};
    let debounceTimer;

    // Helper: Format numbers with commas
    function formatNumber(num) {
        return num.toLocaleString();
    }

    // 1. Fetch initial filter parameters from Flask API
    async function initializeFilters() {
        try {
            const response = await fetch('/api/filters');
            const data = await response.json();
            
            if (data.error) {
                console.error("Error loading filter metadata:", data.error);
                return;
            }

            filterMetadata = data;

            // Populate Seasons Dropdown
            data.seasons.forEach(season => {
                const option = document.createElement('option');
                option.value = season;
                option.textContent = `Season ${season}`;
                seasonSelect.appendChild(option);
            });

            // Populate Players Dropdown
            data.players.forEach(player => {
                const option = document.createElement('option');
                option.value = player;
                option.textContent = player;
                playerSelect.appendChild(option);
            });

            // Populate Teams checkboxes
            data.teams.forEach(team => {
                const label = document.createElement('label');
                label.className = 'checkbox-item';
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = team;
                checkbox.className = 'team-checkbox';
                
                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(team));
                teamsContainer.appendChild(label);
            });

            // Set Margin Slider limits
            marginSlider.max = data.margin_max;
            marginSlider.value = 0;
            marginValueLabel.textContent = "0";

            // Set Date Picker limits
            startDateInput.min = data.min_date;
            startDateInput.max = data.max_date;
            endDateInput.min = data.min_date;
            endDateInput.max = data.max_date;

            // Register event listeners after dynamic options are added
            registerEventListeners();

            // Load initial dashboard state
            loadDashboard();
        } catch (error) {
            console.error("Failed to connect to API on startup:", error);
        }
    }

    // 2. Fetch Dashboard metrics & base64 charts
    async function loadDashboard() {
        showLoaders();

        // Compile filter parameters
        const checkedTeams = Array.from(document.querySelectorAll('.team-checkbox:checked')).map(cb => cb.value);
        
        const payload = {
            search: searchInput.value,
            seasons: [seasonSelect.value],
            player: playerSelect.value,
            start_date: startDateInput.value,
            end_date: endDateInput.value,
            min_margin: parseInt(marginSlider.value) || 0,
            teams: checkedTeams.length > 0 ? checkedTeams : ['all']
        };

        try {
            const response = await fetch('/api/dashboard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            if (data.error) {
                console.error("Dashboard calculation error:", data.error);
                hideLoaders();
                return;
            }

            // Update KPIs
            kpiMatches.textContent = formatNumber(data.kpis.total_matches);
            kpiRuns.textContent = formatNumber(data.kpis.total_runs);
            kpiAvgTarget.textContent = data.kpis.avg_target.toFixed(1);
            kpiTossImpact.textContent = `${data.kpis.toss_impact}%`;
            kpiTopPlayer.textContent = data.kpis.top_player;
            
            // Update match counts badge
            recordCountBadge.textContent = formatNumber(data.record_count);

            // Update Charts
            chartIds.forEach(id => {
                const img = document.getElementById(`chart-${id}`);
                const base64Data = data.charts[id];
                
                if (img && base64Data) {
                    img.classList.remove('loaded');
                    img.onload = () => {
                        img.classList.add('loaded');
                    };
                    img.src = `data:image/png;base64,${base64Data}`;
                    if (img.complete) {
                        img.classList.add('loaded');
                    }
                }
            });

        } catch (error) {
            console.error("API call to load dashboard failed:", error);
        } finally {
            hideLoaders();
        }
    }

    // Loader controls
    function showLoaders() {
        document.querySelectorAll('.loader-overlay').forEach(overlay => {
            overlay.classList.remove('hidden');
        });
    }

    function hideLoaders() {
        document.querySelectorAll('.loader-overlay').forEach(overlay => {
            overlay.classList.add('hidden');
        });
    }

    // Debounce function for keyword searching
    function debounce(func, delay) {
        return function(...args) {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(this, args), delay);
        };
    }

    // Register all change listeners
    function registerEventListeners() {
        // Keyword Search (Debounced)
        searchInput.addEventListener('input', debounce(() => {
            loadDashboard();
        }, 450));

        // Category dropdown (Season)
        seasonSelect.addEventListener('change', loadDashboard);

        // Player dropdown
        playerSelect.addEventListener('change', loadDashboard);

        // Date Inputs
        startDateInput.addEventListener('change', loadDashboard);
        endDateInput.addEventListener('change', loadDashboard);

        // Slider value labels and triggers
        marginSlider.addEventListener('input', (e) => {
            marginValueLabel.textContent = e.target.value;
        });
        marginSlider.addEventListener('change', loadDashboard);

        // Teams checkboxes change
        teamsContainer.addEventListener('change', (e) => {
            if (e.target.classList.contains('team-checkbox')) {
                loadDashboard();
            }
        });

        // Reset Filters Button
        resetBtn.addEventListener('click', () => {
            searchInput.value = '';
            seasonSelect.value = 'all';
            playerSelect.value = 'all';
            startDateInput.value = '';
            endDateInput.value = '';
            marginSlider.value = 0;
            marginValueLabel.textContent = '0';
            
            document.querySelectorAll('.team-checkbox').forEach(cb => {
                cb.checked = false;
            });

            loadDashboard();
        });
    }

    // Initialize
    initializeFilters();
});
