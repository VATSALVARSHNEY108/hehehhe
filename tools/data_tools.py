import streamlit as st
import pandas as pd
import numpy as np
import json
import csv
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all data analysis tools"""

    tool_categories = {
        "Data Import/Export": [
            "CSV Converter", "JSON Converter", "Excel Reader", "Data Format Converter", "Database Connector"
        ],
        "Data Cleaning": [
            "Missing Value Handler", "Duplicate Remover", "Data Validator", "Data Type Converter", "Outlier Detector"
        ],
        "Data Analysis": [
            "Statistical Summary", "Correlation Analysis", "Data Profiling", "Distribution Analysis", "Trend Analysis"
        ],
        "Data Visualization": [
            "Chart Generator", "Heatmap Creator", "Scatter Plot", "Time Series Plot", "Dashboard Builder"
        ],
        "Data Transformation": [
            "Pivot Table Creator", "Data Aggregator", "Column Calculator", "Data Merger", "Data Splitter"
        ],
        "Machine Learning": [
            "Linear Regression", "Clustering Analysis", "Classification", "Feature Selection", "Model Evaluator"
        ],
        "Text Analytics": [
            "Text Mining", "Sentiment Analysis", "Word Frequency", "N-gram Analysis", "Topic Modeling"
        ],
        "Time Series": [
            "Trend Decomposition", "Seasonality Analysis", "Forecasting", "Time Series Plot", "Moving Averages"
        ],
        "Statistical Tests": [
            "T-Test", "Chi-Square Test", "ANOVA", "Normality Test", "Hypothesis Testing"
        ],
        "Data Quality": [
            "Data Profiling", "Quality Assessment", "Completeness Check", "Consistency Validator", "Accuracy Measure"
        ]
    }

    selected_category = st.selectbox("Select Data Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Data Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "CSV Converter":
        csv_converter()
    elif selected_tool == "JSON Converter":
        json_converter()
    elif selected_tool == "Statistical Summary":
        statistical_summary()
    elif selected_tool == "Chart Generator":
        chart_generator()
    elif selected_tool == "Missing Value Handler":
        missing_value_handler()
    elif selected_tool == "Correlation Analysis":
        correlation_analysis()
    elif selected_tool == "Data Validator":
        data_validator()
    elif selected_tool == "Pivot Table Creator":
        pivot_table_creator()
    elif selected_tool == "Linear Regression":
        linear_regression()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def csv_converter():
    """Convert between different data formats"""
    create_tool_header("CSV Converter", "Convert CSV to other formats and vice versa", "📊")

    conversion_type = st.selectbox("Conversion Type:", [
        "CSV to JSON", "JSON to CSV", "CSV to Excel", "Excel to CSV"
    ])

    if conversion_type in ["CSV to JSON", "CSV to Excel"]:
        uploaded_file = FileHandler.upload_files(['csv'], accept_multiple=False)
        if uploaded_file:
            df = FileHandler.process_csv_file(uploaded_file[0])
            if df is not None:
                st.dataframe(df.head())

                if conversion_type == "CSV to JSON":
                    convert_csv_to_json(df)
                else:
                    convert_csv_to_excel(df)

    elif conversion_type == "JSON to CSV":
        uploaded_file = FileHandler.upload_files(['json'], accept_multiple=False)
        if uploaded_file:
            json_data = FileHandler.process_text_file(uploaded_file[0])
            convert_json_to_csv(json_data)

    elif conversion_type == "Excel to CSV":
        uploaded_file = FileHandler.upload_files(['xlsx', 'xls'], accept_multiple=False)
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file[0])
                st.dataframe(df.head())
                convert_excel_to_csv(df)
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")


def convert_csv_to_json(df):
    """Convert CSV DataFrame to JSON"""
    json_format = st.selectbox("JSON Format:", ["Records", "Index", "Values"])

    if st.button("Convert to JSON"):
        try:
            if json_format == "Records":
                json_data = df.to_json(orient='records', indent=2)
            elif json_format == "Index":
                json_data = df.to_json(orient='index', indent=2)
            else:
                json_data = df.to_json(orient='values', indent=2)

            st.code(json_data, language='json')
            FileHandler.create_download_link(json_data.encode(), "converted_data.json", "application/json")
            st.success("✅ Conversion completed!")
        except Exception as e:
            st.error(f"Conversion error: {str(e)}")


def convert_csv_to_excel(df):
    """Convert CSV DataFrame to Excel"""
    if st.button("Convert to Excel"):
        try:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)

            excel_data = output.getvalue()
            FileHandler.create_download_link(excel_data, "converted_data.xlsx",
                                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            st.success("✅ Conversion completed!")
        except Exception as e:
            st.error(f"Conversion error: {str(e)}")


def convert_json_to_csv(json_data):
    """Convert JSON to CSV"""
    try:
        data = json.loads(json_data)

        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            st.error("JSON format not supported for CSV conversion")
            return

        st.dataframe(df.head())

        if st.button("Convert to CSV"):
            csv_data = df.to_csv(index=False)
            FileHandler.create_download_link(csv_data.encode(), "converted_data.csv", "text/csv")
            st.success("✅ Conversion completed!")

    except json.JSONDecodeError:
        st.error("Invalid JSON format")
    except Exception as e:
        st.error(f"Conversion error: {str(e)}")


def convert_excel_to_csv(df):
    """Convert Excel DataFrame to CSV"""
    if st.button("Convert to CSV"):
        try:
            csv_data = df.to_csv(index=False)
            FileHandler.create_download_link(csv_data.encode(), "converted_data.csv", "text/csv")
            st.success("✅ Conversion completed!")
        except Exception as e:
            st.error(f"Conversion error: {str(e)}")


def json_converter():
    """Convert and format JSON data"""
    create_tool_header("JSON Converter", "Format, validate, and convert JSON data", "📋")

    uploaded_file = FileHandler.upload_files(['json'], accept_multiple=False)

    if uploaded_file:
        json_text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded JSON:", json_text[:500] + "..." if len(json_text) > 500 else json_text, height=150,
                     disabled=True)
    else:
        json_text = st.text_area("Enter JSON data:", height=200,
                                 placeholder='{"name": "John", "age": 30, "city": "New York"}')

    if json_text:
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Validate JSON"):
                validate_json(json_text)

        with col2:
            if st.button("Format JSON"):
                format_json(json_text)

        with col3:
            if st.button("Minify JSON"):
                minify_json(json_text)


def validate_json(json_text):
    """Validate JSON format"""
    try:
        data = json.loads(json_text)
        st.success("✅ Valid JSON!")

        # Show structure info
        if isinstance(data, dict):
            st.info(f"Object with {len(data)} keys")
        elif isinstance(data, list):
            st.info(f"Array with {len(data)} items")
        else:
            st.info(f"Simple value: {type(data).__name__}")

    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON: {str(e)}")


def format_json(json_text):
    """Format JSON with indentation"""
    try:
        data = json.loads(json_text)
        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        st.code(formatted, language='json')
        FileHandler.create_download_link(formatted.encode(), "formatted.json", "application/json")
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON: {str(e)}")


def minify_json(json_text):
    """Minify JSON by removing whitespace"""
    try:
        data = json.loads(json_text)
        minified = json.dumps(data, separators=(',', ':'))
        st.code(minified)
        FileHandler.create_download_link(minified.encode(), "minified.json", "application/json")
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON: {str(e)}")


def statistical_summary():
    """Generate statistical summary of data"""
    create_tool_header("Statistical Summary", "Generate comprehensive statistical analysis", "📈")

    uploaded_file = FileHandler.upload_files(['csv', 'xlsx'], accept_multiple=False)

    if uploaded_file:
        if uploaded_file[0].name.endswith('.csv'):
            df = FileHandler.process_csv_file(uploaded_file[0])
        else:
            df = pd.read_excel(uploaded_file[0])

        if df is not None:
            st.dataframe(df.head())

            if st.button("Generate Summary"):
                generate_summary(df)


def generate_summary(df):
    """Generate statistical summary"""
    st.markdown("### 📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    # Data types
    st.markdown("### 📋 Column Information")
    info_df = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.astype(str),
        'Non-Null Count': df.count(),
        'Null Count': df.isnull().sum(),
        'Unique Values': df.nunique()
    })
    st.dataframe(info_df)

    # Numerical summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.markdown("### 📊 Numerical Summary")
        st.dataframe(df[numeric_cols].describe())

    # Categorical summary
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        st.markdown("### 📝 Categorical Summary")
        for col in categorical_cols[:5]:  # Show first 5 categorical columns
            st.write(f"**{col}** - Unique values: {df[col].nunique()}")
            if df[col].nunique() <= 10:
                value_counts = df[col].value_counts()
                st.bar_chart(value_counts)


def chart_generator():
    """Generate various charts from data"""
    create_tool_header("Chart Generator", "Create beautiful charts from your data", "📈")

    uploaded_file = FileHandler.upload_files(['csv', 'xlsx'], accept_multiple=False)

    if uploaded_file:
        if uploaded_file[0].name.endswith('.csv'):
            df = FileHandler.process_csv_file(uploaded_file[0])
        else:
            df = pd.read_excel(uploaded_file[0])

        if df is not None:
            st.dataframe(df.head())

            chart_type = st.selectbox("Chart Type:", [
                "Line Chart", "Bar Chart", "Histogram", "Scatter Plot", "Box Plot", "Heatmap"
            ])

            if chart_type in ["Line Chart", "Bar Chart"]:
                x_col = st.selectbox("X-axis column:", df.columns)
                y_col = st.selectbox("Y-axis column:", df.select_dtypes(include=[np.number]).columns)

                if st.button("Generate Chart"):
                    create_chart(df, chart_type, x_col, y_col)

            elif chart_type == "Histogram":
                col = st.selectbox("Column:", df.select_dtypes(include=[np.number]).columns)
                if st.button("Generate Chart"):
                    create_histogram(df, col)

            elif chart_type == "Scatter Plot":
                x_col = st.selectbox("X-axis:", df.select_dtypes(include=[np.number]).columns)
                y_col = st.selectbox("Y-axis:", df.select_dtypes(include=[np.number]).columns)
                if st.button("Generate Chart"):
                    create_scatter_plot(df, x_col, y_col)


def create_chart(df, chart_type, x_col, y_col):
    """Create line or bar chart"""
    plt.figure(figsize=(10, 6))

    if chart_type == "Line Chart":
        plt.plot(df[x_col], df[y_col])
        plt.title(f"Line Chart: {y_col} vs {x_col}")
    else:  # Bar Chart
        plt.bar(df[x_col], df[y_col])
        plt.title(f"Bar Chart: {y_col} vs {x_col}")

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)
    plt.close()


def create_histogram(df, col):
    """Create histogram"""
    plt.figure(figsize=(10, 6))
    plt.hist(df[col], bins=30, alpha=0.7)
    plt.title(f"Histogram: {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()

    st.pyplot(plt)
    plt.close()


def create_scatter_plot(df, x_col, y_col):
    """Create scatter plot"""
    plt.figure(figsize=(10, 6))
    plt.scatter(df[x_col], df[y_col], alpha=0.6)
    plt.title(f"Scatter Plot: {y_col} vs {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.tight_layout()

    st.pyplot(plt)
    plt.close()


def missing_value_handler():
    """Handle missing values in dataset"""
    create_tool_header("Missing Value Handler", "Detect and handle missing values", "🔍")

    uploaded_file = FileHandler.upload_files(['csv', 'xlsx'], accept_multiple=False)

    if uploaded_file:
        if uploaded_file[0].name.endswith('.csv'):
            df = FileHandler.process_csv_file(uploaded_file[0])
        else:
            df = pd.read_excel(uploaded_file[0])

        if df is not None:
            st.dataframe(df.head())

            # Show missing values
            missing_stats = show_missing_values(df)

            if missing_stats['total_missing'] > 0:
                handle_missing_values(df)
            else:
                st.success("✅ No missing values found in the dataset!")


def show_missing_values(df):
    """Show missing value statistics"""
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df)) * 100

    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Missing Count': missing_count,
        'Missing Percentage': missing_percent.round(2)
    })

    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)

    if len(missing_df) > 0:
        st.markdown("### 🚨 Missing Values Summary")
        st.dataframe(missing_df)

        # Visualize missing values
        if len(missing_df) > 0:
            st.bar_chart(missing_df.set_index('Column')['Missing Count'])

    return {'total_missing': missing_count.sum(), 'columns_with_missing': len(missing_df)}


def handle_missing_values(df):
    """Provide options to handle missing values"""
    st.markdown("### 🔧 Handle Missing Values")

    strategy = st.selectbox("Choose strategy:", [
        "Remove rows with missing values",
        "Remove columns with missing values",
        "Fill with mean (numeric only)",
        "Fill with median (numeric only)",
        "Fill with mode",
        "Forward fill",
        "Backward fill"
    ])

    if st.button("Apply Strategy"):
        try:
            if strategy == "Remove rows with missing values":
                cleaned_df = df.dropna()
            elif strategy == "Remove columns with missing values":
                cleaned_df = df.dropna(axis=1)
            elif strategy == "Fill with mean (numeric only)":
                cleaned_df = df.copy()
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].mean())
            elif strategy == "Fill with median (numeric only)":
                cleaned_df = df.copy()
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].median())
            elif strategy == "Fill with mode":
                cleaned_df = df.fillna(df.mode().iloc[0])
            elif strategy == "Forward fill":
                cleaned_df = df.fillna(method='ffill')
            elif strategy == "Backward fill":
                cleaned_df = df.fillna(method='bfill')

            st.success(f"✅ Strategy applied! Rows before: {len(df)}, Rows after: {len(cleaned_df)}")
            st.dataframe(cleaned_df.head())

            # Download cleaned data
            csv_data = cleaned_df.to_csv(index=False)
            FileHandler.create_download_link(csv_data.encode(), "cleaned_data.csv", "text/csv")

        except Exception as e:
            st.error(f"Error applying strategy: {str(e)}")


def correlation_analysis():
    """Analyze correlations between variables"""
    create_tool_header("Correlation Analysis", "Analyze relationships between variables", "🔗")

    uploaded_file = FileHandler.upload_files(['csv', 'xlsx'], accept_multiple=False)

    if uploaded_file:
        if uploaded_file[0].name.endswith('.csv'):
            df = FileHandler.process_csv_file(uploaded_file[0])
        else:
            df = pd.read_excel(uploaded_file[0])

        if df is not None:
            numeric_df = df.select_dtypes(include=[np.number])

            if len(numeric_df.columns) < 2:
                st.error("Need at least 2 numeric columns for correlation analysis")
                return

            st.dataframe(numeric_df.head())

            if st.button("Calculate Correlations"):
                calculate_correlations(numeric_df)


def calculate_correlations(df):
    """Calculate and display correlations"""
    corr_matrix = df.corr()

    st.markdown("### 📊 Correlation Matrix")
    st.dataframe(corr_matrix)

    # Heatmap
    st.markdown("### 🔥 Correlation Heatmap")
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=0.5)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()

    # Strong correlations
    st.markdown("### 🔍 Strong Correlations")
    strong_corr = []

    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > 0.7:  # Strong correlation threshold
                strong_corr.append({
                    'Variable 1': corr_matrix.columns[i],
                    'Variable 2': corr_matrix.columns[j],
                    'Correlation': round(corr_value, 3)
                })

    if strong_corr:
        strong_corr_df = pd.DataFrame(strong_corr)
        st.dataframe(strong_corr_df)
    else:
        st.info("No strong correlations (|r| > 0.7) found")


def data_validator():
    """Validate data quality"""
    create_tool_header("Data Validator", "Validate data quality and identify issues", "✅")

    uploaded_file = FileHandler.upload_files(['csv', 'xlsx'], accept_multiple=False)

    if uploaded_file:
        if uploaded_file[0].name.endswith('.csv'):
            df = FileHandler.process_csv_file(uploaded_file[0])
        else:
            df = pd.read_excel(uploaded_file[0])

        if df is not None:
            st.dataframe(df.head())

            if st.button("Validate Data"):
                validate_data_quality(df)


def validate_data_quality(df):
    """Perform comprehensive data validation"""
    st.markdown("### 📋 Data Quality Report")

    # Basic statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        duplicate_rows = df.duplicated().sum()
        st.metric("Duplicate Rows", duplicate_rows)

    # Missing values
    missing_values = df.isnull().sum().sum()
    if missing_values > 0:
        st.warning(f"⚠️ Found {missing_values} missing values")
    else:
        st.success("✅ No missing values found")

    # Data type issues
    st.markdown("### 🔍 Potential Data Type Issues")
    for col in df.columns:
        if df[col].dtype == 'object':
            # Check if numeric values are stored as text
            try:
                pd.to_numeric(df[col], errors='raise')
                st.warning(f"⚠️ Column '{col}' contains numeric data but is stored as text")
            except:
                # Check for mixed types
                sample = df[col].dropna().head(100)
                if len(sample) > 0:
                    numeric_count = sum(1 for x in sample if str(x).replace('.', '').replace('-', '').isdigit())
                    if 0 < numeric_count < len(sample):
                        st.warning(f"⚠️ Column '{col}' has mixed data types")

    # Outlier detection for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.markdown("### 📊 Outlier Detection")
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()

            if outliers > 0:
                st.write(f"**{col}:** {outliers} potential outliers found")


def pivot_table_creator():
    """Create pivot tables from data"""
    create_tool_header("Pivot Table Creator", "Create interactive pivot tables", "📊")

    uploaded_file = FileHandler.upload_files(['csv', 'xlsx'], accept_multiple=False)

    if uploaded_file:
        if uploaded_file[0].name.endswith('.csv'):
            df = FileHandler.process_csv_file(uploaded_file[0])
        else:
            df = pd.read_excel(uploaded_file[0])

        if df is not None:
            st.dataframe(df.head())

            create_pivot_table(df)


def create_pivot_table(df):
    """Create pivot table interface"""
    st.markdown("### ⚙️ Pivot Table Configuration")

    col1, col2 = st.columns(2)

    with col1:
        index_cols = st.multiselect("Row Labels (Index):", df.columns)
        values_cols = st.multiselect("Values:", df.select_dtypes(include=[np.number]).columns)

    with col2:
        column_cols = st.multiselect("Column Labels:", df.columns)
        aggfunc = st.selectbox("Aggregation Function:", ["sum", "mean", "count", "min", "max"])

    if index_cols and values_cols and st.button("Create Pivot Table"):
        try:
            pivot_kwargs = {
                'data': df,
                'index': index_cols,
                'values': values_cols,
                'aggfunc': aggfunc
            }

            if column_cols:
                pivot_kwargs['columns'] = column_cols

            pivot_table = pd.pivot_table(**pivot_kwargs)

            st.markdown("### 📊 Pivot Table Results")
            st.dataframe(pivot_table)

            # Download option
            csv_data = pivot_table.to_csv()
            FileHandler.create_download_link(csv_data.encode(), "pivot_table.csv", "text/csv")

        except Exception as e:
            st.error(f"Error creating pivot table: {str(e)}")


def linear_regression():
    """Perform linear regression analysis"""
    create_tool_header("Linear Regression", "Perform linear regression analysis", "📈")

    uploaded_file = FileHandler.upload_files(['csv', 'xlsx'], accept_multiple=False)

    if uploaded_file:
        if uploaded_file[0].name.endswith('.csv'):
            df = FileHandler.process_csv_file(uploaded_file[0])
        else:
            df = pd.read_excel(uploaded_file[0])

        if df is not None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns

            if len(numeric_cols) < 2:
                st.error("Need at least 2 numeric columns for linear regression")
                return

            st.dataframe(df.head())

            perform_linear_regression(df, numeric_cols)


def perform_linear_regression(df, numeric_cols):
    """Perform linear regression analysis"""
    col1, col2 = st.columns(2)

    with col1:
        x_col = st.selectbox("Independent Variable (X):", numeric_cols)
    with col2:
        y_col = st.selectbox("Dependent Variable (Y):", numeric_cols)

    if x_col != y_col and st.button("Run Regression"):
        try:
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import r2_score

            # Prepare data
            X = df[[x_col]].dropna()
            y = df[y_col].dropna()

            # Align the data
            common_index = X.index.intersection(y.index)
            X = X.loc[common_index]
            y = y.loc[common_index]

            # Fit model
            model = LinearRegression()
            model.fit(X, y)

            # Predictions
            y_pred = model.predict(X)

            # Results
            st.markdown("### 📊 Regression Results")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("R-squared", f"{r2_score(y, y_pred):.4f}")
            with col2:
                st.metric("Slope", f"{model.coef_[0]:.4f}")
            with col3:
                st.metric("Intercept", f"{model.intercept_:.4f}")

            # Equation
            st.markdown(f"### 📝 Regression Equation")
            st.latex(f"y = {model.coef_[0]:.4f}x + {model.intercept_:.4f}")

            # Plot
            st.markdown("### 📈 Regression Plot")
            plt.figure(figsize=(10, 6))
            plt.scatter(X, y, alpha=0.6, label='Data points')
            plt.plot(X, y_pred, color='red', linewidth=2, label='Regression line')
            plt.xlabel(x_col)
            plt.ylabel(y_col)
            plt.title(f"Linear Regression: {y_col} vs {x_col}")
            plt.legend()
            plt.tight_layout()
            st.pyplot(plt)
            plt.close()

        except Exception as e:
            st.error(f"Error in regression analysis: {str(e)}")