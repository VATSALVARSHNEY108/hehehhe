import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all science and math tools"""

    tool_categories = {
        "Basic Math": [
            "Calculator", "Unit Converter", "Percentage Calculator", "Fraction Calculator", "Ratio Calculator"
        ],
        "Algebra": [
            "Equation Solver", "Quadratic Formula", "System of Equations", "Polynomial Calculator",
            "Logarithm Calculator"
        ],
        "Geometry": [
            "Area Calculator", "Volume Calculator", "Perimeter Calculator", "Triangle Calculator", "Circle Calculator"
        ],
        "Trigonometry": [
            "Trigonometric Functions", "Angle Converter", "Law of Cosines", "Law of Sines", "Unit Circle"
        ],
        "Calculus": [
            "Derivative Calculator", "Integral Calculator", "Limit Calculator", "Series Calculator", "Function Plotter"
        ],
        "Statistics": [
            "Descriptive Statistics", "Probability Calculator", "Distribution Calculator", "Hypothesis Testing",
            "Confidence Intervals"
        ],
        "Physics": [
            "Motion Calculator", "Force Calculator", "Energy Calculator", "Wave Calculator", "Electricity Calculator"
        ],
        "Chemistry": [
            "Molecular Weight", "Chemical Equation Balancer", "pH Calculator", "Concentration Calculator", "Gas Laws"
        ],
        "Engineering": [
            "Ohm's Law Calculator", "Beam Calculator", "Stress Calculator", "Fluid Mechanics", "Heat Transfer"
        ],
        "Number Theory": [
            "Prime Numbers", "GCD/LCM Calculator", "Factorization", "Number Base Converter", "Fibonacci Sequence"
        ]
    }

    selected_category = st.selectbox("Select Science/Math Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Science/Math Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Calculator":
        advanced_calculator()
    elif selected_tool == "Unit Converter":
        unit_converter()
    elif selected_tool == "Quadratic Formula":
        quadratic_formula()
    elif selected_tool == "Area Calculator":
        area_calculator()
    elif selected_tool == "Trigonometric Functions":
        trig_functions()
    elif selected_tool == "Function Plotter":
        function_plotter()
    elif selected_tool == "Descriptive Statistics":
        descriptive_statistics()
    elif selected_tool == "Motion Calculator":
        motion_calculator()
    elif selected_tool == "Molecular Weight":
        molecular_weight()
    elif selected_tool == "Prime Numbers":
        prime_numbers()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def advanced_calculator():
    """Advanced scientific calculator"""
    create_tool_header("Advanced Calculator", "Perform complex mathematical calculations", "🧮")

    # Calculator interface
    st.markdown("### 🧮 Scientific Calculator")

    expression = st.text_input("Enter mathematical expression:", placeholder="2 + 3 * sin(pi/4)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Available Functions:**")
        st.write("Basic: +, -, *, /, **, (), abs()")
        st.write("Trigonometric: sin(), cos(), tan(), asin(), acos(), atan()")
        st.write("Logarithmic: log(), log10(), ln() (natural log)")
        st.write("Other: sqrt(), exp(), factorial(), pi, e")

    with col2:
        st.markdown("**Examples:**")
        st.code("2 + 3 * 4")
        st.code("sin(pi/2)")
        st.code("log(100)")
        st.code("sqrt(16)")
        st.code("2**3")

    if expression and st.button("Calculate"):
        result = calculate_expression(expression)
        if result is not None:
            st.success(f"**Result:** {result}")
        else:
            st.error("Invalid expression. Please check your syntax.")


def calculate_expression(expression):
    """Safely evaluate mathematical expressions"""
    try:
        # Replace common mathematical functions
        expression = expression.replace("ln(", "log(")
        expression = expression.replace("factorial(", "math.factorial(")
        expression = expression.replace("pi", "math.pi")
        expression = expression.replace("e", "math.e")

        # Add math. prefix to functions
        math_functions = ["sin", "cos", "tan", "asin", "acos", "atan", "log", "log10",
                          "sqrt", "exp", "abs", "floor", "ceil"]
        for func in math_functions:
            expression = expression.replace(f"{func}(", f"math.{func}(")

        # Evaluate safely
        allowed_names = {
            "__builtins__": {},
            "math": math,
        }

        result = eval(expression, allowed_names)
        return result
    except:
        return None


def unit_converter():
    """Convert between different units"""
    create_tool_header("Unit Converter", "Convert between various units of measurement", "📏")

    category = st.selectbox("Unit Category:", [
        "Length", "Weight/Mass", "Temperature", "Area", "Volume", "Speed", "Energy", "Pressure"
    ])

    if category == "Length":
        convert_length()
    elif category == "Weight/Mass":
        convert_weight()
    elif category == "Temperature":
        convert_temperature()
    elif category == "Area":
        convert_area()
    elif category == "Volume":
        convert_volume()
    elif category == "Speed":
        convert_speed()
    else:
        st.info(f"{category} conversion coming soon!")


def convert_length():
    """Convert length units"""
    st.markdown("### 📏 Length Conversion")

    value = st.number_input("Enter value:", value=1.0)

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From:",
                                 ["meters", "kilometers", "centimeters", "millimeters", "inches", "feet", "yards",
                                  "miles"])
    with col2:
        to_unit = st.selectbox("To:", ["meters", "kilometers", "centimeters", "millimeters", "inches", "feet", "yards",
                                       "miles"])

    if st.button("Convert"):
        result = convert_length_units(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")


def convert_length_units(value, from_unit, to_unit):
    """Convert between length units"""
    # Convert to meters first
    to_meters = {
        "meters": 1,
        "kilometers": 1000,
        "centimeters": 0.01,
        "millimeters": 0.001,
        "inches": 0.0254,
        "feet": 0.3048,
        "yards": 0.9144,
        "miles": 1609.344
    }

    meters = value * to_meters[from_unit]
    result = meters / to_meters[to_unit]
    return result


def convert_weight():
    """Convert weight units"""
    st.markdown("### ⚖️ Weight/Mass Conversion")

    value = st.number_input("Enter value:", value=1.0)

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From:", ["kilograms", "grams", "pounds", "ounces", "tons", "stones"])
    with col2:
        to_unit = st.selectbox("To:", ["kilograms", "grams", "pounds", "ounces", "tons", "stones"])

    if st.button("Convert"):
        result = convert_weight_units(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")


def convert_weight_units(value, from_unit, to_unit):
    """Convert between weight units"""
    # Convert to kilograms first
    to_kg = {
        "kilograms": 1,
        "grams": 0.001,
        "pounds": 0.453592,
        "ounces": 0.0283495,
        "tons": 1000,
        "stones": 6.35029
    }

    kg = value * to_kg[from_unit]
    result = kg / to_kg[to_unit]
    return result


def convert_temperature():
    """Convert temperature units"""
    st.markdown("### 🌡️ Temperature Conversion")

    value = st.number_input("Enter temperature:", value=0.0)

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From:", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.selectbox("To:", ["Celsius", "Fahrenheit", "Kelvin"])

    if st.button("Convert"):
        result = convert_temperature_units(value, from_unit, to_unit)
        st.success(f"{value}° {from_unit} = {result:.2f}° {to_unit}")


def convert_temperature_units(value, from_unit, to_unit):
    """Convert between temperature units"""
    # Convert to Celsius first
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:  # Celsius
        celsius = value

    # Convert from Celsius to target
    if to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    else:  # Celsius
        return celsius


def convert_area():
    """Convert area units"""
    st.info("Area conversion coming soon!")


def convert_volume():
    """Convert volume units"""
    st.info("Volume conversion coming soon!")


def convert_speed():
    """Convert speed units"""
    st.info("Speed conversion coming soon!")


def quadratic_formula():
    """Solve quadratic equations"""
    create_tool_header("Quadratic Formula", "Solve quadratic equations ax² + bx + c = 0", "📐")

    st.markdown("### Quadratic Equation: ax² + bx + c = 0")

    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.number_input("Coefficient a:", value=1.0)
    with col2:
        b = st.number_input("Coefficient b:", value=0.0)
    with col3:
        c = st.number_input("Coefficient c:", value=0.0)

    if a != 0 and st.button("Solve"):
        discriminant = b ** 2 - 4 * a * c

        st.markdown(f"### Equation: {a}x² + {b}x + {c} = 0")
        st.markdown(f"**Discriminant (Δ):** {discriminant}")

        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2 * a)
            x2 = (-b - math.sqrt(discriminant)) / (2 * a)
            st.success(f"**Two real solutions:**")
            st.write(f"x₁ = {x1:.6f}")
            st.write(f"x₂ = {x2:.6f}")
        elif discriminant == 0:
            x = -b / (2 * a)
            st.success(f"**One real solution:**")
            st.write(f"x = {x:.6f}")
        else:
            real_part = -b / (2 * a)
            imaginary_part = math.sqrt(-discriminant) / (2 * a)
            st.success(f"**Two complex solutions:**")
            st.write(f"x₁ = {real_part:.6f} + {imaginary_part:.6f}i")
            st.write(f"x₂ = {real_part:.6f} - {imaginary_part:.6f}i")
    elif a == 0:
        st.error("Coefficient 'a' cannot be zero for a quadratic equation")


def area_calculator():
    """Calculate areas of various shapes"""
    create_tool_header("Area Calculator", "Calculate areas of geometric shapes", "📐")

    shape = st.selectbox("Select shape:", [
        "Rectangle", "Square", "Triangle", "Circle", "Parallelogram", "Trapezoid", "Ellipse"
    ])

    if shape == "Rectangle":
        calculate_rectangle_area()
    elif shape == "Square":
        calculate_square_area()
    elif shape == "Triangle":
        calculate_triangle_area()
    elif shape == "Circle":
        calculate_circle_area()
    elif shape == "Parallelogram":
        calculate_parallelogram_area()
    elif shape == "Trapezoid":
        calculate_trapezoid_area()
    elif shape == "Ellipse":
        calculate_ellipse_area()


def calculate_rectangle_area():
    """Calculate rectangle area"""
    st.markdown("### 📐 Rectangle Area")

    col1, col2 = st.columns(2)
    with col1:
        length = st.number_input("Length:", min_value=0.0, value=5.0)
    with col2:
        width = st.number_input("Width:", min_value=0.0, value=3.0)

    if st.button("Calculate Area"):
        area = length * width
        perimeter = 2 * (length + width)
        st.success(f"**Area:** {area} square units")
        st.info(f"**Perimeter:** {perimeter} units")


def calculate_square_area():
    """Calculate square area"""
    st.markdown("### ⬜ Square Area")

    side = st.number_input("Side length:", min_value=0.0, value=4.0)

    if st.button("Calculate Area"):
        area = side ** 2
        perimeter = 4 * side
        diagonal = side * math.sqrt(2)
        st.success(f"**Area:** {area} square units")
        st.info(f"**Perimeter:** {perimeter} units")
        st.info(f"**Diagonal:** {diagonal:.6f} units")


def calculate_triangle_area():
    """Calculate triangle area"""
    st.markdown("### 🔺 Triangle Area")

    method = st.selectbox("Calculation method:", ["Base and Height", "Three Sides (Heron's Formula)"])

    if method == "Base and Height":
        col1, col2 = st.columns(2)
        with col1:
            base = st.number_input("Base:", min_value=0.0, value=6.0)
        with col2:
            height = st.number_input("Height:", min_value=0.0, value=4.0)

        if st.button("Calculate Area"):
            area = 0.5 * base * height
            st.success(f"**Area:** {area} square units")

    else:  # Three Sides
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("Side a:", min_value=0.0, value=3.0)
        with col2:
            b = st.number_input("Side b:", min_value=0.0, value=4.0)
        with col3:
            c = st.number_input("Side c:", min_value=0.0, value=5.0)

        if st.button("Calculate Area"):
            # Check if triangle is valid
            if a + b > c and b + c > a and a + c > b:
                s = (a + b + c) / 2  # Semi-perimeter
                area = math.sqrt(s * (s - a) * (s - b) * (s - c))
                st.success(f"**Area:** {area:.6f} square units")
                st.info(f"**Perimeter:** {a + b + c} units")
            else:
                st.error("Invalid triangle! The sum of any two sides must be greater than the third side.")


def calculate_circle_area():
    """Calculate circle area"""
    st.markdown("### ⭕ Circle Area")

    radius = st.number_input("Radius:", min_value=0.0, value=5.0)

    if st.button("Calculate Area"):
        area = math.pi * radius ** 2
        circumference = 2 * math.pi * radius
        diameter = 2 * radius
        st.success(f"**Area:** {area:.6f} square units")
        st.info(f"**Circumference:** {circumference:.6f} units")
        st.info(f"**Diameter:** {diameter} units")


def calculate_parallelogram_area():
    """Calculate parallelogram area"""
    st.markdown("### ▱ Parallelogram Area")

    col1, col2 = st.columns(2)
    with col1:
        base = st.number_input("Base:", min_value=0.0, value=6.0)
    with col2:
        height = st.number_input("Height:", min_value=0.0, value=4.0)

    if st.button("Calculate Area"):
        area = base * height
        st.success(f"**Area:** {area} square units")


def calculate_trapezoid_area():
    """Calculate trapezoid area"""
    st.markdown("### 🔺 Trapezoid Area")

    col1, col2, col3 = st.columns(3)
    with col1:
        base1 = st.number_input("Base 1:", min_value=0.0, value=5.0)
    with col2:
        base2 = st.number_input("Base 2:", min_value=0.0, value=3.0)
    with col3:
        height = st.number_input("Height:", min_value=0.0, value=4.0)

    if st.button("Calculate Area"):
        area = 0.5 * (base1 + base2) * height
        st.success(f"**Area:** {area} square units")


def calculate_ellipse_area():
    """Calculate ellipse area"""
    st.markdown("### ⬭ Ellipse Area")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Semi-major axis (a):", min_value=0.0, value=5.0)
    with col2:
        b = st.number_input("Semi-minor axis (b):", min_value=0.0, value=3.0)

    if st.button("Calculate Area"):
        area = math.pi * a * b
        st.success(f"**Area:** {area:.6f} square units")


def trig_functions():
    """Calculate trigonometric functions"""
    create_tool_header("Trigonometric Functions", "Calculate sin, cos, tan and their inverses", "📐")

    angle_unit = st.selectbox("Angle unit:", ["Degrees", "Radians"])
    angle = st.number_input("Enter angle:", value=45.0 if angle_unit == "Degrees" else math.pi / 4)

    if st.button("Calculate"):
        if angle_unit == "Degrees":
            rad_angle = math.radians(angle)
        else:
            rad_angle = angle

        try:
            sin_val = math.sin(rad_angle)
            cos_val = math.cos(rad_angle)
            tan_val = math.tan(rad_angle)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("sin", f"{sin_val:.6f}")
                if abs(sin_val) <= 1:
                    asin_val = math.degrees(math.asin(sin_val)) if angle_unit == "Degrees" else math.asin(sin_val)
                    st.metric("arcsin", f"{asin_val:.6f}")

            with col2:
                st.metric("cos", f"{cos_val:.6f}")
                if abs(cos_val) <= 1:
                    acos_val = math.degrees(math.acos(cos_val)) if angle_unit == "Degrees" else math.acos(cos_val)
                    st.metric("arccos", f"{acos_val:.6f}")

            with col3:
                if abs(tan_val) < 1e10:  # Avoid displaying very large numbers
                    st.metric("tan", f"{tan_val:.6f}")
                else:
                    st.metric("tan", "undefined")

                atan_val = math.degrees(math.atan(tan_val)) if angle_unit == "Degrees" else math.atan(tan_val)
                st.metric("arctan", f"{atan_val:.6f}")

        except Exception as e:
            st.error(f"Error in calculation: {str(e)}")


def function_plotter():
    """Plot mathematical functions"""
    create_tool_header("Function Plotter", "Plot mathematical functions", "📈")

    function = st.text_input("Enter function f(x):", value="x**2", placeholder="x**2, sin(x), exp(x)")

    col1, col2 = st.columns(2)
    with col1:
        x_min = st.number_input("X minimum:", value=-10.0)
        x_max = st.number_input("X maximum:", value=10.0)

    with col2:
        num_points = st.slider("Number of points:", 100, 1000, 500)

    if function and st.button("Plot Function"):
        plot_function(function, x_min, x_max, num_points)


def plot_function(function, x_min, x_max, num_points):
    """Plot mathematical function"""
    try:
        x = np.linspace(x_min, x_max, num_points)

        # Replace common functions for numpy
        func_str = function.replace("^", "**")
        func_str = func_str.replace("ln(", "np.log(")
        func_str = func_str.replace("log(", "np.log10(")
        func_str = func_str.replace("sin(", "np.sin(")
        func_str = func_str.replace("cos(", "np.cos(")
        func_str = func_str.replace("tan(", "np.tan(")
        func_str = func_str.replace("exp(", "np.exp(")
        func_str = func_str.replace("sqrt(", "np.sqrt(")
        func_str = func_str.replace("abs(", "np.abs(")
        func_str = func_str.replace("pi", "np.pi")
        func_str = func_str.replace("e", "np.e")

        # Evaluate function
        allowed_names = {
            "x": x,
            "np": np,
            "__builtins__": {},
        }

        y = eval(func_str, allowed_names)

        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, linewidth=2)
        plt.grid(True, alpha=0.3)
        plt.xlabel("x")
        plt.ylabel(f"f(x) = {function}")
        plt.title(f"Plot of f(x) = {function}")

        # Add axis lines
        plt.axhline(y=0, color='k', linewidth=0.5)
        plt.axvline(x=0, color='k', linewidth=0.5)

        plt.tight_layout()
        st.pyplot(plt)
        plt.close()

    except Exception as e:
        st.error(f"Error plotting function: {str(e)}")
        st.info("Make sure to use valid Python/NumPy syntax. Examples: x**2, np.sin(x), np.exp(x)")


def descriptive_statistics():
    """Calculate descriptive statistics"""
    create_tool_header("Descriptive Statistics", "Calculate statistical measures", "📊")

    data_input_method = st.selectbox("Data input method:", ["Manual Entry", "Upload File"])

    if data_input_method == "Manual Entry":
        data_text = st.text_area("Enter numbers (separated by commas or spaces):",
                                 placeholder="1, 2, 3, 4, 5 or 1 2 3 4 5")

        if data_text and st.button("Calculate Statistics"):
            try:
                # Parse data
                data = []
                for item in data_text.replace(',', ' ').split():
                    try:
                        data.append(float(item))
                    except ValueError:
                        continue

                if data:
                    calculate_stats(data)
                else:
                    st.error("No valid numbers found in input")

            except Exception as e:
                st.error(f"Error parsing data: {str(e)}")

    else:  # Upload File
        uploaded_file = FileHandler.upload_files(['csv', 'txt'], accept_multiple=False)

        if uploaded_file:
            try:
                if uploaded_file[0].name.endswith('.csv'):
                    df = FileHandler.process_csv_file(uploaded_file[0])
                    numeric_cols = df.select_dtypes(include=[np.number]).columns

                    if len(numeric_cols) > 0:
                        selected_col = st.selectbox("Select column:", numeric_cols)
                        if st.button("Calculate Statistics"):
                            data = df[selected_col].dropna().tolist()
                            calculate_stats(data)
                    else:
                        st.error("No numeric columns found in CSV file")
                else:
                    content = FileHandler.process_text_file(uploaded_file[0])
                    if st.button("Calculate Statistics"):
                        data = []
                        for line in content.split('\n'):
                            for item in line.replace(',', ' ').split():
                                try:
                                    data.append(float(item))
                                except ValueError:
                                    continue

                        if data:
                            calculate_stats(data)
                        else:
                            st.error("No valid numbers found in file")

            except Exception as e:
                st.error(f"Error processing file: {str(e)}")


def calculate_stats(data):
    """Calculate and display statistics"""
    if not data:
        st.error("No data provided")
        return

    data = np.array(data)

    # Basic statistics
    st.markdown("### 📊 Descriptive Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Count", len(data))
        st.metric("Mean", f"{np.mean(data):.4f}")

    with col2:
        st.metric("Median", f"{np.median(data):.4f}")
        st.metric("Mode", f"{stats.mode(data)[0]:.4f}")

    with col3:
        st.metric("Std Dev", f"{np.std(data, ddof=1):.4f}")
        st.metric("Variance", f"{np.var(data, ddof=1):.4f}")

    with col4:
        st.metric("Min", f"{np.min(data):.4f}")
        st.metric("Max", f"{np.max(data):.4f}")

    # Quartiles
    st.markdown("### 📈 Quartiles")
    q1 = np.percentile(data, 25)
    q2 = np.percentile(data, 50)  # Median
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Q1 (25%)", f"{q1:.4f}")
    with col2:
        st.metric("Q2 (50%)", f"{q2:.4f}")
    with col3:
        st.metric("Q3 (75%)", f"{q3:.4f}")
    with col4:
        st.metric("IQR", f"{iqr:.4f}")

    # Histogram
    st.markdown("### 📊 Data Distribution")
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=min(30, len(data) // 2), alpha=0.7, color='skyblue', edgecolor='black')
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Data")
    plt.grid(True, alpha=0.3)
    st.pyplot(plt)
    plt.close()

    # Box plot
    plt.figure(figsize=(10, 4))
    plt.boxplot(data, vert=False)
    plt.xlabel("Value")
    plt.title("Box Plot of Data")
    plt.grid(True, alpha=0.3)
    st.pyplot(plt)
    plt.close()


def motion_calculator():
    """Calculate motion physics"""
    create_tool_header("Motion Calculator", "Calculate motion and kinematics", "🚀")

    motion_type = st.selectbox("Motion type:", [
        "Uniform Motion", "Uniformly Accelerated Motion", "Projectile Motion", "Circular Motion"
    ])

    if motion_type == "Uniform Motion":
        calculate_uniform_motion()
    elif motion_type == "Uniformly Accelerated Motion":
        calculate_accelerated_motion()
    elif motion_type == "Projectile Motion":
        calculate_projectile_motion()
    elif motion_type == "Circular Motion":
        calculate_circular_motion()


def calculate_uniform_motion():
    """Calculate uniform motion"""
    st.markdown("### 🚗 Uniform Motion: v = d/t")

    # Input two values, calculate the third
    col1, col2, col3 = st.columns(3)

    with col1:
        distance = st.number_input("Distance (m):", value=0.0, help="Leave as 0 to calculate")
    with col2:
        time = st.number_input("Time (s):", value=0.0, help="Leave as 0 to calculate")
    with col3:
        velocity = st.number_input("Velocity (m/s):", value=0.0, help="Leave as 0 to calculate")

    if st.button("Calculate"):
        # Count non-zero values
        values = [distance, time, velocity]
        non_zero_count = sum(1 for v in values if v != 0)

        if non_zero_count == 2:
            if distance == 0:
                distance = velocity * time
                st.success(f"**Distance:** {distance} m")
            elif time == 0:
                time = distance / velocity if velocity != 0 else 0
                st.success(f"**Time:** {time} s")
            elif velocity == 0:
                velocity = distance / time if time != 0 else 0
                st.success(f"**Velocity:** {velocity} m/s")
        else:
            st.error("Please provide exactly 2 values and leave the third as 0 to calculate")


def calculate_accelerated_motion():
    """Calculate uniformly accelerated motion"""
    st.markdown("### 🏎️ Uniformly Accelerated Motion")

    st.markdown("**Equations:**")
    st.latex(r"v = u + at")
    st.latex(r"s = ut + \frac{1}{2}at^2")
    st.latex(r"v^2 = u^2 + 2as")

    col1, col2 = st.columns(2)

    with col1:
        u = st.number_input("Initial velocity (u) m/s:", value=0.0)
        v = st.number_input("Final velocity (v) m/s:", value=0.0, help="Leave as 0 if unknown")
        a = st.number_input("Acceleration (a) m/s²:", value=0.0, help="Leave as 0 if unknown")

    with col2:
        t = st.number_input("Time (t) s:", value=0.0, help="Leave as 0 if unknown")
        s = st.number_input("Displacement (s) m:", value=0.0, help="Leave as 0 if unknown")

    if st.button("Calculate"):
        # Try different equations based on known values
        if t != 0 and a != 0:
            v_calc = u + a * t
            s_calc = u * t + 0.5 * a * t ** 2
            st.success(f"**Final velocity:** {v_calc} m/s")
            st.success(f"**Displacement:** {s_calc} m")
        elif v != 0 and a != 0:
            t_calc = (v - u) / a if a != 0 else 0
            s_calc = (v ** 2 - u ** 2) / (2 * a) if a != 0 else 0
            st.success(f"**Time:** {t_calc} s")
            st.success(f"**Displacement:** {s_calc} m")
        else:
            st.error("Please provide sufficient known values")


def calculate_projectile_motion():
    """Calculate projectile motion"""
    st.info("Projectile motion calculator coming soon!")


def calculate_circular_motion():
    """Calculate circular motion"""
    st.info("Circular motion calculator coming soon!")


def molecular_weight():
    """Calculate molecular weight"""
    create_tool_header("Molecular Weight Calculator", "Calculate molecular weight of compounds", "⚛️")

    # Common atomic weights
    atomic_weights = {
        'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811,
        'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
        'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
        'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
        'Fe': 55.845, 'Cu': 63.546, 'Zn': 65.380, 'Br': 79.904, 'I': 126.905
    }

    st.markdown("### ⚛️ Enter Chemical Formula")
    formula = st.text_input("Chemical formula:", placeholder="H2O, NaCl, C6H12O6", value="H2O")

    if formula and st.button("Calculate Molecular Weight"):
        mol_weight = calculate_molecular_weight(formula, atomic_weights)
        if mol_weight:
            st.success(f"**Molecular weight of {formula}:** {mol_weight:.3f} g/mol")
        else:
            st.error("Invalid chemical formula or unknown elements")

    # Show available elements
    with st.expander("Available Elements"):
        cols = st.columns(5)
        elements = list(atomic_weights.keys())
        for i, element in enumerate(elements):
            with cols[i % 5]:
                st.write(f"**{element}:** {atomic_weights[element]}")


def calculate_molecular_weight(formula, atomic_weights):
    """Calculate molecular weight from chemical formula"""
    import re

    try:
        # Find all element-number pairs
        pattern = r'([A-Z][a-z]?)(\d*)'
        matches = re.findall(pattern, formula)

        total_weight = 0

        for element, count in matches:
            if element in atomic_weights:
                count = int(count) if count else 1
                total_weight += atomic_weights[element] * count
            else:
                return None  # Unknown element

        return total_weight
    except:
        return None


def prime_numbers():
    """Generate and check prime numbers"""
    create_tool_header("Prime Numbers", "Generate and check prime numbers", "🔢")

    option = st.selectbox("Choose option:", [
        "Check if number is prime",
        "Generate prime numbers up to N",
        "Find prime factors"
    ])

    if option == "Check if number is prime":
        number = st.number_input("Enter number:", min_value=2, value=17, step=1)

        if st.button("Check Prime"):
            if is_prime(int(number)):
                st.success(f"✅ {int(number)} is a prime number!")
            else:
                st.error(f"❌ {int(number)} is not a prime number")

    elif option == "Generate prime numbers up to N":
        n = st.number_input("Generate primes up to:", min_value=2, value=100, step=1)

        if st.button("Generate Primes"):
            primes = generate_primes(int(n))
            st.success(f"Found {len(primes)} prime numbers up to {int(n)}")

            # Display primes in columns
            cols = st.columns(5)
            for i, prime in enumerate(primes):
                with cols[i % 5]:
                    st.write(prime)

    elif option == "Find prime factors":
        number = st.number_input("Enter number to factor:", min_value=2, value=60, step=1)

        if st.button("Find Prime Factors"):
            factors = prime_factors(int(number))
            st.success(f"Prime factors of {int(number)}: {factors}")

            # Show factorization
            factor_str = " × ".join(map(str, factors))
            st.write(f"**Factorization:** {int(number)} = {factor_str}")


def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_primes(n):
    """Generate all prime numbers up to n using Sieve of Eratosthenes"""
    if n < 2:
        return []

    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False

    return [i for i in range(2, n + 1) if sieve[i]]


def prime_factors(n):
    """Find prime factors of a number"""
    factors = []
    d = 2

    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1

    if n > 1:
        factors.append(n)

    return factors