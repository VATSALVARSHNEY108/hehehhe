import streamlit as st
import re
import json
import ast
import keyword
import tokenize
import io
import subprocess
import sys
import base64
import urllib.parse
from datetime import datetime
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler
from utils.ai_client import ai_client


def display_tools():
    """Display all coding tools"""

    tool_categories = {
        "Code Editors": [
            "Syntax Highlighter", "Code Formatter", "Bracket Matcher", "Auto-Complete Simulator", "Code Snippets"
        ],
        "Code Formatters": [
            "Python Formatter", "JavaScript Formatter", "HTML Formatter", "CSS Formatter", "JSON Formatter"
        ],
        "Code Validators": [
            "Python Validator", "JavaScript Validator", "HTML Validator", "CSS Validator", "JSON Validator"
        ],
        "Code Converters": [
            "Language Converter", "Encoding Converter", "Format Transformer", "Case Converter", "Indentation Converter"
        ],
        "Documentation Tools": [
            "README Generator", "API Documentation", "Code Comments", "Documentation Parser", "Changelog Generator"
        ],
        "Testing Tools": [
            "Unit Test Generator", "Test Case Creator", "Mock Data Generator", "Test Runner", "Coverage Reporter"
        ],
        "Version Control": [
            "Git Helper", "Diff Viewer", "Merge Helper", "Commit Message Generator", "Branch Manager"
        ],
        "API Tools": [
            "REST Client", "API Tester", "Endpoint Documentation", "Request Builder", "Response Analyzer"
        ],
        "Database Tools": [
            "Query Builder", "Schema Generator", "Migration Creator", "Data Seeder", "Connection Tester"
        ],
        "Development Utilities": [
            "Environment Setup", "Config Manager", "Deployment Helper", "Build Tools", "Package Manager"
        ]
    }

    selected_category = st.selectbox("Select Coding Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Coding Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Python Formatter":
        python_formatter()
    elif selected_tool == "JSON Formatter":
        json_formatter()
    elif selected_tool == "Code Validator":
        code_validator()
    elif selected_tool == "Syntax Highlighter":
        syntax_highlighter()
    elif selected_tool == "README Generator":
        readme_generator()
    elif selected_tool == "API Tester":
        api_tester()
    elif selected_tool == "Query Builder":
        query_builder()
    elif selected_tool == "Unit Test Generator":
        unit_test_generator()
    elif selected_tool == "Git Helper":
        git_helper()
    elif selected_tool == "Code Comments":
        code_comments()
    elif selected_tool == "Language Converter":
        language_converter()
    elif selected_tool == "Mock Data Generator":
        mock_data_generator()
    elif selected_tool == "Config Manager":
        config_manager()
    elif selected_tool == "REST Client":
        rest_client()
    elif selected_tool == "Diff Viewer":
        diff_viewer()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def python_formatter():
    """Python code formatter"""
    create_tool_header("Python Formatter", "Format and beautify Python code", "🐍")

    # File upload option
    uploaded_file = FileHandler.upload_files(['py'], accept_multiple=False)

    if uploaded_file:
        python_code = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Python Code", python_code, height=200, disabled=True)
    else:
        python_code = st.text_area("Enter Python code to format:", height=300, value="""def hello_world(name,age=25):
    if name:
        print(f"Hello, {name}!")
        if age>18:
            print("You are an adult")
        else:print("You are a minor")
    return True

class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def greet(self):return f"Hi, I'm {self.name}"
""")

    if python_code:
        # Formatting options
        col1, col2 = st.columns(2)
        with col1:
            indent_size = st.selectbox("Indent Size", [2, 4, 8], index=1)
            line_length = st.slider("Max Line Length", 50, 120, 79)
            normalize_quotes = st.selectbox("Quote Style", ["Keep Original", "Single Quotes", "Double Quotes"])

        with col2:
            sort_imports = st.checkbox("Sort Imports", True)
            remove_unused_imports = st.checkbox("Remove Unused Imports", True)
            add_trailing_commas = st.checkbox("Add Trailing Commas", False)

        if st.button("Format Python Code"):
            try:
                formatted_code = format_python_code(python_code, {
                    'indent_size': indent_size,
                    'line_length': line_length,
                    'normalize_quotes': normalize_quotes,
                    'sort_imports': sort_imports,
                    'remove_unused_imports': remove_unused_imports,
                    'add_trailing_commas': add_trailing_commas
                })

                st.subheader("Formatted Code")
                st.code(formatted_code, language="python")

                # Show differences
                if formatted_code != python_code:
                    st.subheader("Changes Made")
                    changes = get_code_changes(python_code, formatted_code)
                    for change in changes:
                        st.write(f"• {change}")

                FileHandler.create_download_link(formatted_code.encode(), "formatted_code.py", "text/x-python")

            except Exception as e:
                st.error(f"Error formatting code: {str(e)}")


def json_formatter():
    """JSON formatter and validator"""
    create_tool_header("JSON Formatter", "Format, validate, and beautify JSON", "📋")

    # File upload option
    uploaded_file = FileHandler.upload_files(['json', 'txt'], accept_multiple=False)

    if uploaded_file:
        json_text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded JSON", json_text, height=200, disabled=True)
    else:
        json_text = st.text_area("Enter JSON to format:", height=300,
                                 value='{"name":"John Doe","age":30,"city":"New York","hobbies":["reading","coding","traveling"],"address":{"street":"123 Main St","zipcode":"10001"}}')

    if json_text:
        col1, col2 = st.columns(2)
        with col1:
            indent_size = st.selectbox("Indent Size", [2, 4, 8], index=1)
            sort_keys = st.checkbox("Sort Keys", False)
        with col2:
            compact_mode = st.checkbox("Compact Mode", False)
            ensure_ascii = st.checkbox("Ensure ASCII", True)

        if st.button("Format JSON"):
            try:
                # Parse JSON
                parsed_json = json.loads(json_text)

                # Format options
                if compact_mode:
                    formatted_json = json.dumps(parsed_json, ensure_ascii=ensure_ascii,
                                                sort_keys=sort_keys, separators=(',', ':'))
                else:
                    formatted_json = json.dumps(parsed_json, indent=indent_size,
                                                ensure_ascii=ensure_ascii, sort_keys=sort_keys)

                st.success("✅ Valid JSON!")

                st.subheader("Formatted JSON")
                st.code(formatted_json, language="json")

                # JSON statistics
                st.subheader("JSON Statistics")
                stats = analyze_json_structure(parsed_json)
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Objects", stats['objects'])
                with col2:
                    st.metric("Arrays", stats['arrays'])
                with col3:
                    st.metric("Keys", stats['keys'])
                with col4:
                    st.metric("Max Depth", stats['max_depth'])

                FileHandler.create_download_link(formatted_json.encode(), "formatted.json", "application/json")

            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON: {str(e)}")

                # Try to suggest fixes
                suggestions = suggest_json_fixes(json_text, str(e))
                if suggestions:
                    st.subheader("Suggested Fixes")
                    for suggestion in suggestions:
                        st.write(f"• {suggestion}")


def code_validator():
    """Multi-language code validator"""
    create_tool_header("Code Validator", "Validate syntax for multiple languages", "✅")

    language = st.selectbox("Select Language", ["Python", "JavaScript", "HTML", "CSS", "JSON", "XML"])

    # File upload option
    file_extensions = {
        "Python": ['py'],
        "JavaScript": ['js'],
        "HTML": ['html', 'htm'],
        "CSS": ['css'],
        "JSON": ['json'],
        "XML": ['xml']
    }

    uploaded_file = FileHandler.upload_files(file_extensions[language], accept_multiple=False)

    if uploaded_file:
        code = FileHandler.process_text_file(uploaded_file[0])
        st.text_area(f"Uploaded {language} Code", code, height=200, disabled=True)
    else:
        code = st.text_area(f"Enter {language} code to validate:", height=300)

    if code and st.button("Validate Code"):
        validation_result = validate_code(code, language)

        if validation_result['is_valid']:
            st.success("✅ Code is syntactically correct!")
        else:
            st.error("❌ Syntax errors found:")
            for error in validation_result['errors']:
                st.error(f"Line {error.get('line', '?')}: {error['message']}")

        if validation_result['warnings']:
            st.warning("⚠️ Warnings:")
            for warning in validation_result['warnings']:
                st.warning(f"Line {warning.get('line', '?')}: {warning['message']}")

        # Code statistics
        if validation_result['stats']:
            st.subheader("Code Statistics")
            stats = validation_result['stats']
            cols = st.columns(len(stats))
            for i, (key, value) in enumerate(stats.items()):
                with cols[i % len(cols)]:
                    st.metric(key.replace('_', ' ').title(), value)


def syntax_highlighter():
    """Code syntax highlighter"""
    create_tool_header("Syntax Highlighter", "Highlight code syntax for various languages", "🎨")

    language = st.selectbox("Select Language", [
        "Python", "JavaScript", "HTML", "CSS", "JSON", "SQL", "XML", "YAML",
        "C", "C++", "Java", "PHP", "Ruby", "Go", "Rust", "TypeScript"
    ])

    uploaded_file = FileHandler.upload_files(['txt', 'py', 'js', 'html', 'css', 'json'], accept_multiple=False)

    if uploaded_file:
        code = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Code", code, height=200, disabled=True)
    else:
        code = st.text_area("Enter code to highlight:", height=300)

    if code:
        # Theme selection
        theme = st.selectbox("Select Theme", ["Default", "Dark", "Monokai", "GitHub", "VS Code"])

        if st.button("Apply Syntax Highlighting"):
            st.subheader("Highlighted Code")

            # Use Streamlit's built-in code highlighting
            st.code(code, language=language.lower())

            # Additional analysis
            analysis = analyze_code_structure(code, language)

            if analysis:
                st.subheader("Code Analysis")
                for key, value in analysis.items():
                    st.write(f"**{key}**: {value}")


def readme_generator():
    """README.md generator"""
    create_tool_header("README Generator", "Generate comprehensive README files", "📖")

    # Project information
    st.subheader("Project Information")

    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name", "My Awesome Project")
        description = st.text_area("Short Description", "A brief description of your project")
        author = st.text_input("Author", "Your Name")

    with col2:
        license_type = st.selectbox("License", ["MIT", "Apache 2.0", "GPL v3", "BSD 3-Clause", "Custom"])
        project_type = st.selectbox("Project Type", ["Web App", "CLI Tool", "Library", "API", "Desktop App"])
        language = st.selectbox("Primary Language", ["Python", "JavaScript", "Java", "C++", "Go", "Rust"])

    # Features and sections
    st.subheader("README Sections")

    col1, col2 = st.columns(2)
    with col1:
        include_installation = st.checkbox("Installation Instructions", True)
        include_usage = st.checkbox("Usage Examples", True)
        include_api_docs = st.checkbox("API Documentation", False)
        include_contributing = st.checkbox("Contributing Guidelines", True)

    with col2:
        include_changelog = st.checkbox("Changelog", False)
        include_license = st.checkbox("License Section", True)
        include_badges = st.checkbox("Status Badges", True)
        include_screenshots = st.checkbox("Screenshots", False)

    # Additional details
    if include_installation:
        installation_steps = st.text_area("Installation Steps", "pip install my-awesome-project")

    if include_usage:
        usage_example = st.text_area("Usage Example", "from my_project import main\nmain.run()")

    features_list = st.text_area("Key Features (one per line)", "Feature 1\nFeature 2\nFeature 3")

    if st.button("Generate README"):
        readme_content = generate_readme(
            project_name=project_name,
            description=description,
            author=author,
            license_type=license_type,
            project_type=project_type,
            language=language,
            features=features_list.split('\n') if features_list else [],
            installation_steps=installation_steps if include_installation else None,
            usage_example=usage_example if include_usage else None,
            include_badges=include_badges,
            include_contributing=include_contributing,
            include_license=include_license,
            include_api_docs=include_api_docs
        )

        st.subheader("Generated README.md")
        st.code(readme_content, language="markdown")

        # Preview
        st.subheader("Preview")
        st.markdown(readme_content)

        FileHandler.create_download_link(readme_content.encode(), "README.md", "text/markdown")


def api_tester():
    """REST API testing tool"""
    create_tool_header("API Tester", "Test REST APIs and analyze responses", "🔌")

    # Request configuration
    st.subheader("HTTP Request Configuration")

    col1, col2 = st.columns([3, 1])
    with col1:
        url = st.text_input("URL", "https://api.github.com/users/octocat")
    with col2:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE", "PATCH"])

    # Headers
    st.subheader("Headers")
    num_headers = st.number_input("Number of Headers", 0, 10, 2)
    headers = {}

    for i in range(num_headers):
        col1, col2 = st.columns(2)
        with col1:
            header_key = st.text_input(f"Header {i + 1} Key", f"Authorization" if i == 0 else "Content-Type",
                                       key=f"header_key_{i}")
        with col2:
            header_value = st.text_input(f"Header {i + 1} Value", f"Bearer token" if i == 0 else "application/json",
                                         key=f"header_value_{i}")

        if header_key and header_value:
            headers[header_key] = header_value

    # Request body
    if method in ["POST", "PUT", "PATCH"]:
        st.subheader("Request Body")
        content_type = st.selectbox("Content Type", ["JSON", "Form Data", "Plain Text", "XML"])

        if content_type == "JSON":
            request_body = st.text_area("JSON Body", '{\n  "key": "value"\n}')
        else:
            request_body = st.text_area("Request Body", "")
    else:
        request_body = None

    # Query parameters
    st.subheader("Query Parameters")
    num_params = st.number_input("Number of Parameters", 0, 10, 0)
    params = {}

    for i in range(num_params):
        col1, col2 = st.columns(2)
        with col1:
            param_key = st.text_input(f"Param {i + 1} Key", key=f"param_key_{i}")
        with col2:
            param_value = st.text_input(f"Param {i + 1} Value", key=f"param_value_{i}")

        if param_key and param_value:
            params[param_key] = param_value

    # Send request
    if st.button("Send Request") and url:
        try:
            import requests

            # Prepare request
            request_kwargs = {
                'method': method,
                'url': url,
                'headers': headers if headers else None,
                'params': params if params else None,
                'timeout': 30
            }

            if request_body and method in ["POST", "PUT", "PATCH"]:
                if content_type == "JSON":
                    try:
                        request_kwargs['json'] = json.loads(request_body)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON in request body")
                        return
                else:
                    request_kwargs['data'] = request_body

            # Make request
            with st.spinner("Sending request..."):
                response = requests.request(**request_kwargs)

            # Display response
            st.subheader("Response")

            col1, col2, col3 = st.columns(3)
            with col1:
                status_color = "green" if response.status_code < 400 else "red"
                st.markdown(f"**Status Code**: <span style='color: {status_color}'>{response.status_code}</span>",
                            unsafe_allow_html=True)
            with col2:
                st.write(f"**Response Time**: {response.elapsed.total_seconds():.3f}s")
            with col3:
                st.write(f"**Content Length**: {len(response.content):,} bytes")

            # Response headers
            st.subheader("Response Headers")
            for key, value in response.headers.items():
                st.write(f"**{key}**: {value}")

            # Response body
            st.subheader("Response Body")

            content_type = response.headers.get('content-type', '').lower()

            if 'application/json' in content_type:
                try:
                    formatted_json = json.dumps(response.json(), indent=2)
                    st.code(formatted_json, language="json")
                except (json.JSONDecodeError, ValueError):
                    st.text(response.text)
            else:
                st.text(response.text)

            # Save response
            if st.button("Save Response"):
                response_data = {
                    'request': {
                        'method': method,
                        'url': url,
                        'headers': headers,
                        'params': params,
                        'body': request_body
                    },
                    'response': {
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'body': response.text,
                        'response_time': response.elapsed.total_seconds()
                    },
                    'timestamp': datetime.now().isoformat()
                }

                response_json = json.dumps(response_data, indent=2)
                FileHandler.create_download_link(response_json.encode(), "api_response.json", "application/json")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {str(e)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")


def query_builder():
    """SQL query builder"""
    create_tool_header("Query Builder", "Build SQL queries visually", "🗃️")

    query_type = st.selectbox("Query Type", ["SELECT", "INSERT", "UPDATE", "DELETE"])

    if query_type == "SELECT":
        # SELECT query builder
        st.subheader("SELECT Query Builder")

        col1, col2 = st.columns(2)
        with col1:
            table_name = st.text_input("Table Name", "users")
            columns = st.text_area("Columns (comma-separated)", "id, name, email, created_at")

        with col2:
            distinct = st.checkbox("DISTINCT")
            limit = st.number_input("LIMIT", 0, 1000, 0)

        # WHERE clause
        st.subheader("WHERE Conditions")
        num_conditions = st.number_input("Number of Conditions", 0, 10, 1)
        where_conditions = []

        for i in range(num_conditions):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                column = st.text_input(f"Column {i + 1}", "id", key=f"where_col_{i}")
            with col2:
                operator = st.selectbox(f"Operator {i + 1}", ["=", "!=", ">", "<", ">=", "<=", "LIKE", "IN"],
                                        key=f"where_op_{i}")
            with col3:
                value = st.text_input(f"Value {i + 1}", "1", key=f"where_val_{i}")
            with col4:
                if i > 0:
                    logical_op = st.selectbox(f"Logic {i}", ["AND", "OR"], key=f"where_logic_{i}")
                else:
                    logical_op = None

            if column and value:
                condition = {
                    'column': column,
                    'operator': operator,
                    'value': value,
                    'logical_op': logical_op
                }
                where_conditions.append(condition)

        # ORDER BY
        st.subheader("ORDER BY")
        order_column = st.text_input("Order Column", "")
        order_direction = st.selectbox("Direction", ["ASC", "DESC"]) if order_column else None

        # GROUP BY
        group_column = st.text_input("GROUP BY Column", "")

        if st.button("Generate SELECT Query"):
            query = build_select_query(
                table=table_name,
                columns=columns,
                distinct=distinct,
                where_conditions=where_conditions,
                order_column=order_column,
                order_direction=order_direction,
                group_column=group_column,
                limit=limit if limit > 0 else None
            )

            st.subheader("Generated SQL Query")
            st.code(query, language="sql")

            # Query explanation
            st.subheader("Query Explanation")
            explanation = explain_sql_query(query, query_type)
            st.write(explanation)

            FileHandler.create_download_link(query.encode(), "query.sql", "text/plain")

    elif query_type == "INSERT":
        # INSERT query builder
        st.subheader("INSERT Query Builder")

        table_name = st.text_input("Table Name", "users")

        st.subheader("Column Values")
        num_columns = st.number_input("Number of Columns", 1, 20, 3)
        column_values = {}

        for i in range(num_columns):
            col1, col2 = st.columns(2)
            with col1:
                column = st.text_input(f"Column {i + 1}", f"column_{i + 1}", key=f"insert_col_{i}")
            with col2:
                value = st.text_input(f"Value {i + 1}", f"'value_{i + 1}'", key=f"insert_val_{i}")

            if column and value:
                column_values[column] = value

        if st.button("Generate INSERT Query") and column_values:
            query = build_insert_query(table_name, column_values)

            st.subheader("Generated SQL Query")
            st.code(query, language="sql")

            FileHandler.create_download_link(query.encode(), "insert_query.sql", "text/plain")


def unit_test_generator():
    """Unit test generator"""
    create_tool_header("Unit Test Generator", "Generate unit tests for your code", "🧪")

    language = st.selectbox("Programming Language", ["Python", "JavaScript", "Java", "C#"])
    test_framework = st.selectbox("Test Framework", get_test_frameworks(language))

    # File upload option
    uploaded_file = FileHandler.upload_files(['py', 'js', 'java', 'cs'], accept_multiple=False)

    if uploaded_file:
        source_code = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Source Code", source_code, height=200, disabled=True)
    else:
        source_code = st.text_area("Enter source code:", height=300, value=get_sample_code(language))

    if source_code:
        # Test generation options
        col1, col2 = st.columns(2)
        with col1:
            include_edge_cases = st.checkbox("Include Edge Cases", True)
            include_negative_tests = st.checkbox("Include Negative Tests", True)
            include_mocks = st.checkbox("Include Mocks/Stubs", False)

        with col2:
            test_coverage = st.selectbox("Test Coverage Level", ["Basic", "Comprehensive", "Extensive"])
            async_support = st.checkbox("Async/Promise Support", False)

        if st.button("Generate Unit Tests"):
            with st.spinner("Generating tests with AI..."):
                # Use AI to generate comprehensive unit tests
                prompt = f"""
                Generate comprehensive unit tests for the following {language} code using {test_framework}.

                Requirements:
                - {"Include edge cases" if include_edge_cases else "Skip edge cases"}
                - {"Include negative test cases" if include_negative_tests else "Skip negative tests"}
                - {"Include mocks and stubs" if include_mocks else "No mocks needed"}
                - Coverage level: {test_coverage}
                - {"Support async/promises" if async_support else "Synchronous only"}

                Source code:
                {source_code}

                Generate complete, runnable test code with proper imports and setup.
                """

                generated_tests = ai_client.generate_text(prompt, max_tokens=2000)

                if generated_tests and "error" not in generated_tests.lower():
                    st.subheader("Generated Unit Tests")
                    st.code(generated_tests, language=language.lower())

                    # Test analysis
                    analysis = analyze_generated_tests(generated_tests, language)

                    st.subheader("Test Analysis")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Test Methods", analysis.get('test_count', 0))
                    with col2:
                        st.metric("Assertions", analysis.get('assertion_count', 0))
                    with col3:
                        st.metric("Coverage", f"{analysis.get('coverage_estimate', 0)}%")

                    # Download
                    file_extension = get_file_extension(language)
                    FileHandler.create_download_link(generated_tests.encode(), f"test_code.{file_extension}",
                                                     "text/plain")
                else:
                    st.error("Failed to generate unit tests. Please try again or modify your code.")


def git_helper():
    """Git helper tools"""
    create_tool_header("Git Helper", "Git commands and workflow assistance", "🌿")

    tab1, tab2, tab3 = st.tabs(["Commit Message Generator", "Branch Helper", "Git Commands"])

    with tab1:
        st.subheader("Commit Message Generator")

        commit_type = st.selectbox("Commit Type", [
            "feat", "fix", "docs", "style", "refactor", "test", "chore", "perf"
        ])

        scope = st.text_input("Scope (optional)", placeholder="auth, ui, api")
        description = st.text_area("Description", placeholder="Brief description of changes")

        breaking_change = st.checkbox("Breaking Change")

        if description:
            # Generate conventional commit message
            scope_part = f"({scope})" if scope else ""
            breaking_part = "!" if breaking_change else ""

            commit_message = f"{commit_type}{scope_part}{breaking_part}: {description}"

            st.subheader("Generated Commit Message")
            st.code(commit_message)

            # Add body and footer if needed
            body = st.text_area("Body (optional)", placeholder="Detailed explanation of changes")
            footer = st.text_area("Footer (optional)", placeholder="References, breaking changes, etc.")

            full_message = commit_message
            if body:
                full_message += f"\n\n{body}"
            if footer:
                full_message += f"\n\n{footer}"

            if body or footer:
                st.subheader("Full Commit Message")
                st.code(full_message)

            FileHandler.create_download_link(full_message.encode(), "commit_message.txt", "text/plain")

    with tab2:
        st.subheader("Branch Management Helper")

        current_branch = st.text_input("Current Branch", "main")
        feature_name = st.text_input("Feature Name", "new-feature")

        st.subheader("Common Git Commands")

        commands = [
            f"git checkout -b feature/{feature_name}",
            f"git add .",
            f"git commit -m \"feat: add {feature_name}\"",
            f"git push origin feature/{feature_name}",
            f"git checkout {current_branch}",
            f"git merge feature/{feature_name}",
            f"git branch -d feature/{feature_name}"
        ]

        for i, cmd in enumerate(commands):
            st.code(cmd, language="bash")
            if st.button(f"Copy Command {i + 1}", key=f"git_cmd_{i}"):
                st.success(f"Command copied: {cmd}")

    with tab3:
        st.subheader("Git Command Reference")

        command_categories = {
            "Basic Commands": [
                "git init - Initialize a new Git repository",
                "git clone <url> - Clone a repository",
                "git add <file> - Stage changes",
                "git commit -m 'message' - Commit changes",
                "git push - Push commits to remote",
                "git pull - Pull changes from remote"
            ],
            "Branching": [
                "git branch - List branches",
                "git checkout <branch> - Switch branch",
                "git checkout -b <branch> - Create and switch to new branch",
                "git merge <branch> - Merge branch",
                "git branch -d <branch> - Delete branch"
            ],
            "History & Information": [
                "git log - Show commit history",
                "git status - Show working tree status",
                "git diff - Show changes",
                "git show <commit> - Show commit details",
                "git blame <file> - Show file annotations"
            ]
        }

        for category, commands in command_categories.items():
            st.subheader(category)
            for cmd in commands:
                st.write(f"• `{cmd}`")


# Helper functions
def format_python_code(code, options):
    """Format Python code based on options"""
    try:
        # Parse the AST to ensure valid syntax
        ast.parse(code)

        formatted = code

        # Basic formatting improvements
        lines = formatted.split('\n')
        formatted_lines = []
        indent_level = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append('')
                continue

            # Adjust indent level
            if stripped.endswith(':'):
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
            elif stripped.startswith(('return', 'break', 'continue', 'pass', 'raise')):
                formatted_lines.append('    ' * indent_level + stripped)
            elif stripped.startswith(('except', 'elif', 'else', 'finally')):
                formatted_lines.append('    ' * (indent_level - 1) + stripped)
                if stripped.endswith(':'):
                    # Don't change indent level as it's already adjusted
                    pass
            elif any(keyword in stripped for keyword in ['def ', 'class ', 'if ', 'for ', 'while ', 'with ', 'try:']):
                formatted_lines.append('    ' * indent_level + stripped)
                if stripped.endswith(':'):
                    indent_level += 1
            else:
                formatted_lines.append('    ' * indent_level + stripped)

        # Handle dedentation
        final_lines = []
        indent_level = 0

        for i, line in enumerate(formatted_lines):
            stripped = line.strip()
            if not stripped:
                final_lines.append('')
                continue

            # Calculate proper indentation
            if i > 0:
                prev_line = formatted_lines[i - 1].strip()
                if prev_line.endswith(':'):
                    indent_level += 1
                elif stripped.startswith(('except', 'elif', 'else', 'finally')) and indent_level > 0:
                    indent_level -= 1
                elif not prev_line.endswith(':') and len(prev_line) > 0:
                    # Check if we need to dedent
                    if not any(keyword in prev_line for keyword in
                               ['def ', 'class ', 'if ', 'for ', 'while ', 'with ', 'try:']):
                        pass  # Keep current indent

            final_lines.append('    ' * max(0, indent_level) + stripped)

        return '\n'.join(final_lines)

    except SyntaxError as e:
        raise Exception(f"Syntax error in Python code: {str(e)}")


def get_code_changes(original, formatted):
    """Get list of changes made during formatting"""
    changes = []

    if len(formatted.split('\n')) != len(original.split('\n')):
        changes.append("Adjusted line breaks and spacing")

    if '    ' in formatted and '    ' not in original:
        changes.append("Standardized indentation to 4 spaces")

    if original.count(' ') != formatted.count(' '):
        changes.append("Normalized whitespace")

    return changes if changes else ["Code formatting applied"]


def analyze_json_structure(data, depth=0):
    """Analyze JSON structure recursively"""
    stats = {
        'objects': 0,
        'arrays': 0,
        'keys': 0,
        'max_depth': depth
    }

    if isinstance(data, dict):
        stats['objects'] = 1
        stats['keys'] = len(data)
        for key, value in data.items():
            sub_stats = analyze_json_structure(value, depth + 1)
            stats['objects'] += sub_stats['objects']
            stats['arrays'] += sub_stats['arrays']
            stats['keys'] += sub_stats['keys']
            stats['max_depth'] = max(stats['max_depth'], sub_stats['max_depth'])

    elif isinstance(data, list):
        stats['arrays'] = 1
        for item in data:
            sub_stats = analyze_json_structure(item, depth + 1)
            stats['objects'] += sub_stats['objects']
            stats['arrays'] += sub_stats['arrays']
            stats['keys'] += sub_stats['keys']
            stats['max_depth'] = max(stats['max_depth'], sub_stats['max_depth'])

    return stats


def suggest_json_fixes(json_text, error_message):
    """Suggest fixes for JSON syntax errors"""
    suggestions = []

    if "Expecting property name" in error_message:
        suggestions.append("Check for missing or extra commas")
        suggestions.append("Ensure all property names are enclosed in double quotes")

    if "Expecting ',' delimiter" in error_message:
        suggestions.append("Missing comma between object properties or array elements")

    if "Expecting ':'" in error_message:
        suggestions.append("Missing colon after property name")

    if "Expecting value" in error_message:
        suggestions.append("Check for trailing comma or missing value")

    # Check for common issues
    if "'" in json_text:
        suggestions.append("Replace single quotes with double quotes")

    if json_text.count('{') != json_text.count('}'):
        suggestions.append("Mismatched curly braces")

    if json_text.count('[') != json_text.count(']'):
        suggestions.append("Mismatched square brackets")

    return suggestions


def validate_code(code, language):
    """Validate code syntax for different languages"""
    result = {
        'is_valid': False,
        'errors': [],
        'warnings': [],
        'stats': {}
    }

    try:
        if language == "Python":
            ast.parse(code)
            result['is_valid'] = True
            result['stats'] = {
                'lines': len(code.split('\n')),
                'functions': len(re.findall(r'def\s+\w+', code)),
                'classes': len(re.findall(r'class\s+\w+', code)),
                'imports': len(re.findall(r'import\s+\w+|from\s+\w+', code))
            }

        elif language == "JavaScript":
            # Basic JavaScript validation
            if code.strip():
                result['is_valid'] = True
                result['stats'] = {
                    'lines': len(code.split('\n')),
                    'functions': len(re.findall(r'function\s+\w+|=>\s*{|\w+\s*=\s*function', code)),
                    'variables': len(re.findall(r'var\s+\w+|let\s+\w+|const\s+\w+', code))
                }

        elif language == "JSON":
            json.loads(code)
            result['is_valid'] = True
            parsed = json.loads(code)
            result['stats'] = analyze_json_structure(parsed)

        else:
            # Basic validation for other languages
            result['is_valid'] = len(code.strip()) > 0
            result['stats'] = {'lines': len(code.split('\n'))}

    except SyntaxError as e:
        result['errors'].append({
            'line': getattr(e, 'lineno', '?'),
            'message': str(e)
        })
    except json.JSONDecodeError as e:
        result['errors'].append({
            'line': getattr(e, 'lineno', '?'),
            'message': str(e)
        })
    except Exception as e:
        result['errors'].append({
            'message': str(e)
        })

    return result


def analyze_code_structure(code, language):
    """Analyze code structure and provide insights"""
    analysis = {}

    if language.lower() == "python":
        analysis['Functions'] = len(re.findall(r'def\s+\w+', code))
        analysis['Classes'] = len(re.findall(r'class\s+\w+', code))
        analysis['Imports'] = len(re.findall(r'import\s+\w+|from\s+\w+', code))
        analysis['Comments'] = len(re.findall(r'#.*', code))
        analysis['Docstrings'] = len(re.findall(r'""".*?"""', code, re.DOTALL))

    elif language.lower() == "javascript":
        analysis['Functions'] = len(re.findall(r'function\s+\w+|=>\s*{|\w+\s*=\s*function', code))
        analysis['Variables'] = len(re.findall(r'var\s+\w+|let\s+\w+|const\s+\w+', code))
        analysis['Comments'] = len(re.findall(r'//.*|/\*.*?\*/', code, re.DOTALL))

    analysis['Lines of Code'] = len([line for line in code.split('\n') if line.strip()])
    analysis['Total Lines'] = len(code.split('\n'))

    return analysis


def generate_readme(project_name, description, author, license_type, project_type,
                    language, features, installation_steps=None, usage_example=None,
                    include_badges=True, include_contributing=True, include_license=True,
                    include_api_docs=False):
    """Generate README.md content"""

    readme = f"# {project_name}\n\n"

    if include_badges:
        readme += f"""![License](https://img.shields.io/badge/license-{license_type.replace(' ', '%20')}-blue)
![Language](https://img.shields.io/badge/language-{language}-green)
![Status](https://img.shields.io/badge/status-active-success)

"""

    readme += f"{description}\n\n"

    if features:
        readme += "## ✨ Features\n\n"
        for feature in features:
            if feature.strip():
                readme += f"- {feature.strip()}\n"
        readme += "\n"

    if installation_steps:
        readme += "## 🚀 Installation\n\n"
        readme += f"```bash\n{installation_steps}\n```\n\n"

    if usage_example:
        readme += f"## 📖 Usage\n\n```{language.lower()}\n{usage_example}\n```\n\n"

    if include_api_docs:
        readme += """## 📚 API Documentation

### Main Functions

#### `function_name(parameter)`

Description of the function.

**Parameters:**
- `parameter` (type): Description

**Returns:**
- `type`: Description

"""

    if include_contributing:
        readme += """## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

"""

    if include_license:
        readme += f"## 📄 License\n\nThis project is licensed under the {license_type} License.\n\n"

    readme += f"## 👤 Author\n\n**{author}**\n\n"
    readme += "---\n\n"
    readme += "⭐ Star this project if you find it helpful!"

    return readme


def build_select_query(table, columns, distinct=False, where_conditions=None,
                       order_column=None, order_direction=None, group_column=None, limit=None):
    """Build SELECT SQL query"""

    query_parts = []

    # SELECT clause
    select_clause = "SELECT DISTINCT" if distinct else "SELECT"
    query_parts.append(f"{select_clause} {columns}")

    # FROM clause
    query_parts.append(f"FROM {table}")

    # WHERE clause
    if where_conditions:
        where_parts = []
        for i, condition in enumerate(where_conditions):
            condition_str = f"{condition['column']} {condition['operator']} {condition['value']}"
            if i > 0 and condition.get('logical_op'):
                condition_str = f"{condition['logical_op']} {condition_str}"
            where_parts.append(condition_str)

        if where_parts:
            query_parts.append(f"WHERE {' '.join(where_parts)}")

    # GROUP BY clause
    if group_column:
        query_parts.append(f"GROUP BY {group_column}")

    # ORDER BY clause
    if order_column:
        query_parts.append(f"ORDER BY {order_column} {order_direction or 'ASC'}")

    # LIMIT clause
    if limit:
        query_parts.append(f"LIMIT {limit}")

    return '\n'.join(query_parts) + ';'


def build_insert_query(table, column_values):
    """Build INSERT SQL query"""
    columns = ', '.join(column_values.keys())
    values = ', '.join(column_values.values())

    return f"INSERT INTO {table} ({columns})\nVALUES ({values});"


def explain_sql_query(query, query_type):
    """Explain what an SQL query does"""
    explanations = {
        'SELECT': f"This query retrieves data from the database. It selects specific columns and may filter, sort, or group the results."
    }
    return explanations.get(query_type, "This query performs a database operation.")


def get_test_frameworks(language):
    """Get available test frameworks for a language"""
    frameworks = {
        "Python": ["unittest", "pytest", "nose2"],
        "JavaScript": ["Jest", "Mocha", "Jasmine", "Cypress"],
        "Java": ["JUnit", "TestNG", "Mockito"],
        "C#": ["NUnit", "MSTest", "xUnit"]
    }
    return frameworks.get(language, ["Default"])


def get_sample_code(language):
    """Get sample code for different languages"""
    samples = {
        "Python": """def calculate_total(items, tax_rate=0.1):
    \"\"\"Calculate total price including tax\"\"\"
    if not items:
        return 0

    subtotal = sum(item['price'] * item['quantity'] for item in items)
    tax = subtotal * tax_rate
    return subtotal + tax

def validate_email(email):
    \"\"\"Validate email format\"\"\"
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))""",

        "JavaScript": """function calculateTotal(items, taxRate = 0.1) {
    if (!items || items.length === 0) {
        return 0;
    }

    const subtotal = items.reduce((sum, item) => {
        return sum + (item.price * item.quantity);
    }, 0);

    const tax = subtotal * taxRate;
    return subtotal + tax;
}

function validateEmail(email) {
    const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return pattern.test(email);
}""",

        "Java": """public class Calculator {
    public static double calculateTotal(List<Item> items, double taxRate) {
        if (items == null || items.isEmpty()) {
            return 0.0;
        }

        double subtotal = items.stream()
            .mapToDouble(item -> item.getPrice() * item.getQuantity())
            .sum();

        double tax = subtotal * taxRate;
        return subtotal + tax;
    }

    public static boolean validateEmail(String email) {
        String pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$";
        return email != null && email.matches(pattern);
    }
}"""
    }
    return samples.get(language, "// Sample code")


def analyze_generated_tests(test_code, language):
    """Analyze generated test code"""
    analysis = {}

    if language.lower() == "python":
        analysis['test_count'] = len(re.findall(r'def test_\w+', test_code))
        analysis['assertion_count'] = len(re.findall(r'assert\w*\s', test_code))
    elif language.lower() == "javascript":
        analysis['test_count'] = len(re.findall(r'test\s*\(|it\s*\(', test_code))
        analysis['assertion_count'] = len(re.findall(r'expect\(|assert\w*\(', test_code))
    else:
        analysis['test_count'] = test_code.count('test')
        analysis['assertion_count'] = test_code.count('assert')

    # Estimate coverage based on test count
    analysis['coverage_estimate'] = min(analysis['test_count'] * 20, 100)

    return analysis


def get_file_extension(language):
    """Get file extension for programming language"""
    extensions = {
        "Python": "py",
        "JavaScript": "js",
        "Java": "java",
        "C#": "cs",
        "C++": "cpp",
        "C": "c"
    }
    return extensions.get(language, "txt")


# Additional helper functions for remaining tools
def code_comments():
    """Code commenting tool"""
    st.info("Code Comments Generator - Coming soon!")


def language_converter():
    """Programming language converter"""
    st.info("Language Converter - Coming soon!")


def mock_data_generator():
    """Mock data generator"""
    st.info("Mock Data Generator - Coming soon!")


def config_manager():
    """Configuration manager"""
    st.info("Config Manager - Coming soon!")


def rest_client():
    """REST API client"""
    st.info("Advanced REST Client - Coming soon!")


def diff_viewer():
    """Code diff viewer"""
    st.info("Code Diff Viewer - Coming soon!")
