import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv('D:\HansaCequity\output\Global_AI_Content_Impact_Dataset_cleaned.csv')

# 1. Top 5 countries with the highest average ImpactScore
top_countries = df.groupby('Country')['ImpactScore'].mean().sort_values(ascending=False).head(5)
print("Top 5 Countries:\n", top_countries)

# 2. Most affected content category and industry
# Assuming 'ContentCategory' and 'ConsumerIndustry' are the columns for content category and industry respectively but ContentCategory is not in the dataset
# most_affected_content = df['ContentCategory'].value_counts().idxmax()
most_affected_industry = df['ConsumerIndustry'].value_counts().idxmax()

# print(f"Most Affected Content Category: {most_affected_content}")
print(f"Most Affected Industry: {most_affected_industry}")

# 3. ImpactScore Trend Over Time
# Assuming 'Date' is the date column in the dataset but not available in the dataset
# df['Date'] = pd.to_datetime(df['Date'])  # Ensure your Date column is datetime
# trend = df.groupby('Date')['ImpactScore'].mean()

plt.figure(figsize=(10,5))
# trend.plot(marker='o')
plt.title('ImpactScore Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Avg ImpactScore')
plt.grid()
plt.tight_layout()
plt.savefig('impactscore_trend.png')
plt.show()
