import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# 1. Pedestrian dwell duration by zone (Zone 1 vs. Zone 2)
df = pd.read_csv('stay_duration_stats_hourly.csv')

p_df = df[df['category'] == 'pedestrian'].copy()
p_df['Zone'] = p_df['sensor'].apply(
    lambda s: 'Zone 1' if 'Zone 1' in s else ('Zone 2' if 'Zone 2' in s else 'Other')
)
p_df['avg_stay_seconds'] = (p_df['sum_ms'] / p_df['objects']) / 1000

zone_trends = p_df.groupby(['hour_of_the_day', 'Zone'])['avg_stay_seconds'].mean().unstack()

plt.figure(figsize=(14, 6.5))
plt.plot(zone_trends.index, zone_trends['Zone 1'],
         marker='o', color='#1f77b4', linewidth=2.5, markersize=6, label='Zone 1')
plt.plot(zone_trends.index, zone_trends['Zone 2'],
         marker='s', color='#ff7f0e', linewidth=2.5, markersize=6, label='Zone 2')

for hour in zone_trends.index:
    val1 = zone_trends.loc[hour, 'Zone 1']
    val2 = zone_trends.loc[hour, 'Zone 2']
    plt.text(hour, val1 + 0.15, f"{val1:.1f}s",
             ha='center', va='bottom', fontsize=8, color='#1f77b4', fontweight='bold')
    plt.text(hour, val2 - 0.15, f"{val2:.1f}s",
             ha='center', va='top', fontsize=8, color='#ff7f0e', fontweight='bold')

plt.title('Axeltorv: Hourly Comparison of Pedestrian Stay Durations', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Hour of the Day (00:00 - 23:00)', fontsize=12)
plt.ylabel('Average Stay Duration (Seconds)', fontsize=12)
plt.xticks(range(0, 24))
plt.ylim(0, max(zone_trends.max()) * 1.35)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(frameon=True, facecolor='white', loc='upper right', fontsize=11)
plt.tight_layout()
plt.savefig('zone_comparison_labeled.png', dpi=300)
plt.close()

# 2. Accessibility check: general pedestrians vs. strollers (prams)
family_df = df[df['category'].isin(['pedestrian', 'pram'])].copy()
family_df['avg_stay_seconds'] = (family_df['sum_ms'] / family_df['objects']) / 1000
family_df['Zone'] = family_df['sensor'].apply(lambda x: 'Zone 1' if 'Zone 1' in x else 'Zone 2')

family_summary = family_df.groupby(['Zone', 'category'])['avg_stay_seconds'].mean().unstack()
family_summary.plot(kind='bar', figsize=(10, 5), color=['#1f77b4', '#e377c2'], edgecolor='white')
plt.title('Axeltorv Accessibility: Pedestrians vs. Strollers (Prams)', fontsize=12, fontweight='bold')
plt.ylabel('Average Stay Duration (Seconds)')
plt.xlabel('Square Zones')
plt.xticks(rotation=0)
plt.legend(title='Category')
plt.tight_layout()
plt.savefig('family_accessibility_comparison.png', dpi=300)
plt.close()

# 3. Movement volume by hour & weekday and daily transport mode trends
mov = pd.read_csv('movement_stats_hourly.csv')

ped_mov = mov[mov['category'] == 'pedestrian'].copy()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hourly_weekday = ped_mov.groupby(['hour_of_the_day', 'weekday'])['amount'].sum().unstack()[weekday_order]

palette = {
    'Friday': '#2b8cbe', 'Monday': '#1a237e', 'Saturday': '#d95f02',
    'Sunday': '#6a1b9a', 'Thursday': '#e7298a', 'Tuesday': '#3f007d', 'Wednesday': '#31a354'
}

plt.figure(figsize=(13, 6))
for day in weekday_order:
    plt.plot(hourly_weekday.index, hourly_weekday[day], linewidth=2.2, color=palette[day], label=day)

plt.title('Axeltorv: Pedestrian Movement by Hour and Day of the Week', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Hour of the Day (00:00 - 23:00)', fontsize=11)
plt.ylabel('Total Pedestrian Count', fontsize=11)
plt.xticks(range(0, 24))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Weekday', frameon=True, facecolor='white', ncol=4, loc='upper left')
plt.tight_layout()
plt.savefig('pedestrian_movement_by_weekday.png', dpi=300)
plt.close()

daily_mov = mov[mov['category'].isin(['pedestrian', 'car', 'bicycle'])].copy()
daily_mov['date_parsed'] = pd.to_datetime(daily_mov['date_only'], format='%m/%d/%Y')
daily_summary = daily_mov.groupby(['date_parsed', 'category'])['amount'].sum().unstack(fill_value=0)

plt.figure(figsize=(13, 5.5))
plt.plot(daily_summary.index, daily_summary['pedestrian'], color='#1b6ca8', linewidth=2.2, label='Pedestrian')
plt.plot(daily_summary.index, daily_summary['car'], color='#7b2cbf', linewidth=2, label='Car')
plt.plot(daily_summary.index, daily_summary['bicycle'], color='#2b9348', linewidth=2, label='Bicycle')

plt.title('Axeltorv: Daily Movement Volume by Transport Mode (Feb – May 2026)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Date', fontsize=11)
plt.ylabel('Daily Count', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Category', frameon=True, facecolor='white')
plt.tight_layout()
plt.savefig('daily_movement_by_mode.png', dpi=300)
plt.close()
