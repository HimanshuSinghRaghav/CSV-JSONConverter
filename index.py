import streamlit as st
import pandas as pd
import json
import io

def detect_file_type(file_contents):
    try:
        pd.read_csv(io.BytesIO(file_contents))
        return "csv"
    except pd.errors.ParserError:
        pass

    try:
        json.loads(file_contents.decode('utf-8'))
        return "json"
    except json.JSONDecodeError:
        pass

    return None

def convert_data(input_data, conversion_type):
    if conversion_type == "CSV to JSON":
        df = pd.read_csv(io.BytesIO(input_data))
        return df.to_json(orient="records")
    elif conversion_type == "JSON to CSV":
        try:
            data = json.loads(input_data.decode('utf-8'))
        except json.JSONDecodeError:
            data = []

        # Check if the data is a JSON array
        if isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            # If not a list, create a single-row DataFrame
            df = pd.json_normalize([data])

        # Check if the DataFrame is not empty before converting to CSV
        if not df.empty:
            return df.to_csv(index=False, encoding='utf-8')
        else:
            return "No data available for conversion"



def main():
    st.title("CSV/JSON Converter")

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "json"])

    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        file_type = detect_file_type(file_contents)

        st.text("File content:")
        st.code(file_contents)

        st.text("Converted Data:")

        conversion_type = st.radio("Select conversion type:", ["CSV to JSON", "JSON to CSV"])

        converted_data = convert_data(file_contents, conversion_type)

        if conversion_type == "CSV to JSON":
            st.json(json.loads(converted_data))
            st.download_button(
                label="Download JSON",
                data=converted_data,
                file_name="converted_data.json",
                key="download_json_button",
                help="Click to download JSON file"
            )

        elif conversion_type == "JSON to CSV":
            df = pd.read_csv(io.StringIO(converted_data))
            st.write("Converted CSV Data Table:")
            st.table(df)

            st.download_button(
                label="Download CSV",
                data=converted_data.encode("utf-8"),
                file_name="converted_data.csv",
                key="download_csv_button",
                help="Click to download CSV file"
            )

if __name__ == "__main__":
    main()
