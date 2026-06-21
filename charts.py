import io
import base64
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import seaborn as sns

# Color Palette Config
THEME_BG = '#16171d'
CARD_BG = '#20212a'
TEXT_COLOR = '#ffffff'
TEXT_MUTED = '#a0aec0'
GRID_COLOR = '#2d3748'
BORDER_COLOR = '#2d3748'

PALETTE_NEONS = ['#00f2fe', '#8a2be2', '#ffd700', '#ff7f50', '#10b981', '#3b82f6', '#f43f5e']

def apply_chart_style():
    plt.rcParams['figure.facecolor'] = THEME_BG
    plt.rcParams['axes.facecolor'] = CARD_BG
    plt.rcParams['text.color'] = TEXT_COLOR
    plt.rcParams['axes.labelcolor'] = TEXT_MUTED
    plt.rcParams['xtick.color'] = TEXT_MUTED
    plt.rcParams['ytick.color'] = TEXT_MUTED
    plt.rcParams['grid.color'] = GRID_COLOR
    plt.rcParams['axes.edgecolor'] = BORDER_COLOR
    plt.rcParams['font.size'] = 10
    sns.set_theme(style="dark", rc={
        "figure.facecolor": THEME_BG,
        "axes.facecolor": CARD_BG,
        "grid.color": GRID_COLOR,
        "text.color": TEXT_COLOR,
        "axes.labelcolor": TEXT_MUTED
    })

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=110, facecolor=THEME_BG)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_str

def draw_empty_chart(title):
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.text(0.5, 0.5, "No Data Matching Filters", 
            color=TEXT_MUTED, ha='center', va='center', fontsize=12, fontweight='bold')
    ax.set_title(title, color=TEXT_COLOR, fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(BORDER_COLOR)
    return fig_to_base64(fig)

# 1. Pie Chart - Toss Decision Distribution
def get_toss_decision_chart(matches):
    if len(matches) == 0:
        return draw_empty_chart("Toss Decision Distribution")
    
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    data = matches['toss_decision'].value_counts()
    colors = ['#8a2be2', '#00f2fe']
    
    ax.pie(
        data, 
        labels=data.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors,
        textprops={'color': TEXT_COLOR, 'fontsize': 11, 'weight': 'bold'},
        wedgeprops={'edgecolor': CARD_BG, 'linewidth': 2}
    )
    
    # Draw a circle at the center to make it a donut chart
    centre_circle = plt.Circle((0,0),0.70,fc=CARD_BG)
    fig.gca().add_artist(centre_circle)
    
    ax.set_title("Toss Decision Distribution", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    return fig_to_base64(fig)

# 2. Histogram - Target Runs Distribution
def get_target_runs_histogram(matches):
    if len(matches) == 0 or 'target_runs' not in matches.columns:
        return draw_empty_chart("Target Runs Distribution")
        
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    
    sns.histplot(
        data=matches, 
        x='target_runs', 
        kde=True, 
        ax=ax, 
        color='#ffd700', 
        edgecolor=THEME_BG,
        alpha=0.8
    )
    
    ax.set_title("Distribution of Target Runs", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Target Runs", color=TEXT_MUTED, fontsize=11)
    ax.set_ylabel("Count of Matches", color=TEXT_MUTED, fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    return fig_to_base64(fig)

# 3. Line Chart - Trend of Matches Played Over Seasons
def get_matches_trend_chart(matches):
    if len(matches) == 0:
        return draw_empty_chart("Matches Played Trend")
        
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    trend = matches['season'].value_counts().sort_index()
    
    ax.plot(
        trend.index, 
        trend.values, 
        marker='o', 
        linewidth=2.5, 
        color='#00f2fe',
        markerfacecolor='#ffd700', 
        markeredgecolor=CARD_BG, 
        markersize=8
    )
    
    ax.set_title("Matches Played Over Seasons", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Season", color=TEXT_MUTED, fontsize=11)
    ax.set_ylabel("Number of Matches", color=TEXT_MUTED, fontsize=11)
    plt.xticks(rotation=45)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    return fig_to_base64(fig)

# 4. Bar Chart - Top Teams by Wins
def get_top_winners_chart(matches):
    # Filter out 'No Result' and count wins
    wins_data = matches[matches['winner'] != 'No Result']['winner'].value_counts()
    if len(wins_data) == 0:
        return draw_empty_chart("Top Teams by Wins")
        
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    
    top_teams = wins_data.head(10)
    
    # Horizontal bar plot
    bars = ax.barh(
        top_teams.index, 
        top_teams.values, 
        color=sns.color_palette("viridis", len(top_teams))
    )
    
    # Add values on the bar edges
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 1, 
            bar.get_y() + bar.get_height()/2, 
            f'{int(width)}', 
            ha='left', 
            va='center', 
            color=TEXT_COLOR, 
            fontweight='bold'
        )
        
    ax.invert_yaxis()  # top-down
    ax.set_title("Top 10 Teams by Victory Count", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Total Wins", color=TEXT_MUTED, fontsize=11)
    ax.set_ylabel("Team Name", color=TEXT_MUTED, fontsize=11)
    ax.grid(True, axis='x', linestyle='--', alpha=0.2)
    
    return fig_to_base64(fig)

# 5. Scatter Plot - Target Runs vs. Result Margin
def get_target_vs_margin_scatter(matches):
    if len(matches) == 0:
        return draw_empty_chart("Target Runs vs. Result Margin")
        
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    
    # Only plot matches where a result was achieved with a numeric margin
    valid_matches = matches[matches['result'].isin(['runs', 'wickets'])]
    
    if len(valid_matches) == 0:
        return draw_empty_chart("Target Runs vs. Result Margin")
        
    sns.scatterplot(
        data=valid_matches,
        x='target_runs',
        y='result_margin',
        hue='result',
        palette={'runs': '#ff7f50', 'wickets': '#00f2fe'},
        alpha=0.8,
        s=50,
        edgecolor=THEME_BG,
        ax=ax
    )
    
    ax.set_title("Target Runs vs. Victory Margin", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Target Runs", color=TEXT_MUTED, fontsize=11)
    ax.set_ylabel("Result Margin (Runs/Wickets)", color=TEXT_MUTED, fontsize=11)
    ax.legend(title="Win Mode", facecolor=CARD_BG, edgecolor=BORDER_COLOR)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    return fig_to_base64(fig)

# 6. Box Plot - Result Margin Distribution by Win Method
def get_margin_boxplot(matches):
    valid_matches = matches[matches['result'].isin(['runs', 'wickets'])]
    if len(valid_matches) == 0:
        return draw_empty_chart("Result Margin Spread")
        
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    sns.boxplot(
        data=valid_matches,
        x='result',
        y='result_margin',
        hue='result',
        palette={'runs': '#ff7f50', 'wickets': '#00f2fe'},
        legend=False,
        ax=ax,
        linewidth=2,
        flierprops={'marker': 'x', 'markeredgecolor': '#ffd700'}
    )
    
    ax.set_title("Victory Margin Spread by Win Type", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Win Type (Runs vs Wickets)", color=TEXT_MUTED, fontsize=11)
    ax.set_ylabel("Winning Margin", color=TEXT_MUTED, fontsize=11)
    ax.grid(True, axis='y', linestyle='--', alpha=0.2)
    
    return fig_to_base64(fig)

# 7. Heatmap - Correlation Matrix
def get_correlation_heatmap(matches):
    if len(matches) == 0:
        return draw_empty_chart("Feature Correlation Heatmap")
        
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    # Select numerical columns
    cols = ['target_runs', 'result_margin', 'target_overs']
    
    # Add season year if it's numeric after mapping
    temp_df = matches.copy()
    try:
        temp_df['season_year'] = pd.to_numeric(temp_df['season'], errors='coerce')
        cols.append('season_year')
    except:
        pass
        
    corr_df = temp_df[cols].corr()
    
    sns.heatmap(
        corr_df,
        annot=True,
        cmap='mako',
        fmt=".2f",
        vmin=-1,
        vmax=1,
        annot_kws={'size': 11, 'weight': 'bold'},
        ax=ax,
        cbar=True
    )
    
    ax.set_title("Correlation Heatmap of Match Attributes", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    return fig_to_base64(fig)

# 8. Area Chart - Cumulative Wins for Top Teams Over Seasons
def get_cumulative_wins_area(matches):
    # Find top 4 teams by overall wins
    overall_wins = matches[matches['winner'] != 'No Result']['winner'].value_counts()
    if len(overall_wins) == 0:
        return draw_empty_chart("Cumulative Wins Over Time")
        
    top_teams = overall_wins.head(4).index.tolist()
    
    # Filter matches to only top teams' wins
    top_wins = matches[matches['winner'].isin(top_teams)]
    if len(top_wins) == 0:
        return draw_empty_chart("Cumulative Wins Over Time")
        
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    
    # Group by season and winner, count wins
    wins_by_season = top_wins.groupby(['season', 'winner']).size().unstack(fill_value=0)
    
    # Make sure all seasons are represented
    all_seasons = sorted(matches['season'].unique())
    wins_by_season = wins_by_season.reindex(all_seasons, fill_value=0)
    
    # Calculate cumulative wins
    cum_wins = wins_by_season.cumsum()
    
    # Plot Area Chart
    ax.stackplot(
        cum_wins.index,
        [cum_wins[team] for team in top_teams],
        labels=top_teams,
        colors=['#00f2fe', '#8a2be2', '#ffd700', '#ff7f50'],
        alpha=0.75
    )
    
    ax.set_title("Cumulative Wins Trend (Top 4 Teams)", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Season", color=TEXT_MUTED, fontsize=11)
    ax.set_ylabel("Cumulative Victories", color=TEXT_MUTED, fontsize=11)
    plt.xticks(rotation=45)
    ax.legend(loc='upper left', facecolor=CARD_BG, edgecolor=BORDER_COLOR)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    return fig_to_base64(fig)

# 9. Count Plot - Matches Played by City
def get_cities_countplot(matches):
    if len(matches) == 0:
        return draw_empty_chart("Matches Played by City")
        
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    city_counts = matches['city'].value_counts().head(10)
    
    sns.barplot(
        x=city_counts.values,
        y=city_counts.index,
        hue=city_counts.index,
        palette="crest",
        legend=False,
        ax=ax
    )
    
    # Add labels to bars
    for i, v in enumerate(city_counts.values):
        ax.text(v + 1, i, str(v), color=TEXT_COLOR, va='center', fontweight='bold')
        
    ax.set_title("Top 10 Host Cities by Match Count", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Matches Played", color=TEXT_MUTED, fontsize=11)
    ax.set_ylabel("City", color=TEXT_MUTED, fontsize=11)
    ax.grid(True, axis='x', linestyle='--', alpha=0.2)
    
    return fig_to_base64(fig)

# 10. Violin Plot - Target Runs Spread Over Seasons
def get_target_runs_violin(matches):
    if len(matches) == 0:
        return draw_empty_chart("Target Runs Spread Over Seasons")
        
    apply_chart_style()
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    
    # Sort seasons for nice plotting
    sorted_seasons = sorted(matches['season'].unique())
    
    sns.violinplot(
        data=matches,
        x='season',
        y='target_runs',
        order=sorted_seasons,
        hue='season',
        palette="plasma",
        legend=False,
        ax=ax,
        linewidth=1.5
    )
    
    ax.set_title("Target Runs Density and Spread over Seasons", color=TEXT_COLOR, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Season", color=TEXT_MUTED, fontsize=11)
    ax.set_ylabel("Target Score", color=TEXT_MUTED, fontsize=11)
    plt.xticks(rotation=45)
    ax.grid(True, axis='y', linestyle='--', alpha=0.2)
    
    return fig_to_base64(fig)
