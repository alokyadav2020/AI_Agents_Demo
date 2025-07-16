# Financial Information Extraction System

This system is a sophisticated tool designed to extract and analyze financial information from PDF documents, particularly focused on company financial statements. It uses AI agents to process and structure the data into meaningful insights.

## Features

- **PDF Processing**: Extracts text from uploaded PDF files
- **Interactive Web Interface**: Built with Streamlit for easy user interaction
- **Comprehensive Data Extraction**: Analyzes multiple aspects of company data:
  - Company Profile Information
  - Financial Metrics
  - Balance Sheet Data
  - Key Performance Indicators (KPIs)
  - Company Valuation
  - Industry Benchmarks
  - Risk Factor Analysis

## Data Extraction Components

### 1. Company Information
- Legal company name
- Industry classification
- Business sectors
- Year founded
- Employee count
- Website
- EIN (Employer Identification Number)

### 2. Financial Metrics
- Yearly data for the last 3 years including:
  - Revenue
  - Cost of Goods Sold (COGS)
  - Operating Expenses
  - EBITDA

### 3. Balance Sheet Data
- Total Assets
- Total Liabilities
- Equity
- Debt (Long-term and Short-term)
- Cash and Cash Equivalents

### 4. Key Performance Indicators (KPIs)
- Gross Margin
- Operating Margin
- Debt to Equity Ratio
- Current Ratio
- Revenue Growth
- Market Share

### 5. Valuation Metrics
- Enterprise Value
- EV/EBITDA Multiple
- Valuation Range (Low and High estimates)

### 6. Industry Benchmarks
- Average Gross Margin
- Average Operating Margin
- Average Debt to Equity Ratio
- Average Revenue Growth

### 7. Risk Analysis
- Customer Concentration Risk
- Geographic Concentration Risk
- Supply Chain Dependency
- Debt Level Assessment
- Market Cyclicality

## Requirements

```text
streamlit
pypdf
pydantic
agno
python-dotenv
```

## Environment Setup

1. Create a `.env` file with the following variables:
```env
ENDPOINT_URL=your_azure_endpoint
DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_KEY=your_api_key
```

## Usage

1. Run the application:
```bash
streamlit run data_extraction_agents.py
```

2. Upload a PDF file containing financial statements
3. The system will automatically process the document and extract relevant information
4. Results will be displayed in a structured JSON format

## Technical Details

- Uses Azure OpenAI for AI processing
- Implements Pydantic models for data validation
- Utilizes a team of specialized agents for different aspects of data extraction
- Processes data in a coordinated manner using the Team class

## Error Handling

The system includes error handling for:
- PDF processing issues
- Data extraction failures
- API communication errors

## Note

This system is optimized for financial statements and may require adjustments for other types of financial documents.