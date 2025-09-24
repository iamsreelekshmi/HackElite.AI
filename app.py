from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_and_analyze():
    message = ""
    table_html = None      # Default, nothing shown on GET/refresh
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            message = "No file selected."
        else:
            try:
                df = pd.read_excel(file)
                print(df)
                message = f"File '{file.filename}' uploaded successfully!"
                total_scenarios = len(df)
                print(total_scenarios)
                critical_df = df[df['Criticality'].str.lower() == 'critical']
                print(critical_df)
                critical_passed = len(critical_df[critical_df['Status'].str.lower() == 'passed'])
                print(critical_passed)
                critical_failed = len(critical_df[critical_df['Status'].str.lower() == 'failed'])
                print(critical_failed)
                table_html = f"""
                               <table class="table table-bordered mt-4">
                                 <tr><th>Total Scenarios</th><td>{total_scenarios}</td></tr>
                                 <tr><th>Critical Scenarios (Passed)</th><td>{critical_passed}</td></tr>
                                 <tr><th>Critical Scenarios (Failed)</th><td>{critical_failed}</td></tr>
                               </table>
                               """
            except Exception as e:
                message = f"Error: {str(e)}. Ensure the file is a valid Excel file (.xlsx)."
    return render_template('upload.html', message=message, table_html=table_html)

if __name__ == "__main__":
    app.run(debug=True)
