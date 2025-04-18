import json
import boto3
import pandas as pd
from io import StringIO, BytesIO

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the S3 bucket and file name from event
    bucket = 'shailendra-ai-impact-bucket'
    key = 'uploaded_from_api.csv'
    
    # Download the CSV file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    file_content = response['Body'].read().decode('utf-8')

    # Load the CSV content into a pandas DataFrame
    df = pd.read_csv(StringIO(file_content))

    # Step 1: Data Cleaning
    df.dropna(subset=['Country', 'Industry', 'AI Adoption Rate (%)'], inplace=True)

    # Round AI Adoption Rate and create ImpactScore
    df['ImpactScore'] = df['AI Adoption Rate (%)'].round().astype(int)

    # Drop the original AI Adoption Rate (%) column
    df.drop(columns=['AI Adoption Rate (%)'], inplace=True)

    # Step 2: Rename Columns
    df.rename(columns={
        'Industry': 'ConsumerIndustry'
    }, inplace=True)

    # Step 3: Filter Rows where ImpactScore >= 50
    df = df[df['ImpactScore'] >= 50]

    # Step 4: Summary Metrics
    avg_impact_per_country = df.groupby('Country')['ImpactScore'].mean().reset_index()
    industry_counts = df['ConsumerIndustry'].value_counts().reset_index()
    max_impact_by_industry = df.groupby('ConsumerIndustry')['ImpactScore'].max().reset_index()

    # Combine all metrics into one summary DataFrame
    summary = {
        "avg_impact_per_country": avg_impact_per_country.to_dict(orient='records'),
        "industry_counts": industry_counts.to_dict(orient='records'),
        "max_impact_by_industry": max_impact_by_industry.to_dict(orient='records'),
    }

    # Save cleaned and summary files to S3
    cleaned_csv_buffer = BytesIO()
    df.to_csv(cleaned_csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key='processed/Global_AI_Content_Impact_Dataset_cleaned.csv', Body=cleaned_csv_buffer.getvalue())

    summary_csv_buffer = BytesIO()
    pd.DataFrame.from_dict(summary).to_csv(summary_csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key='processed/Global_AI_Content_Impact_Dataset_summary.csv', Body=summary_csv_buffer.getvalue())

    return {'statusCode': 200, 'body': 'File processed and saved!'}
