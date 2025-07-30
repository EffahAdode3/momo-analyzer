from django.shortcuts import render
from .forms import UploadPDFForm
from django.http import HttpResponse
import pdfplumber
import pandas as pd
import re

# Parse the uploaded MoMo PDF
def parse_pdf(file):
    transactions = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            for line in lines:
                if re.search(r'\d{2}-\w{3}-\d{4}', line):
                    parts = re.split(r'\s+', line.strip())
                    try:
                        for i in range(len(parts)):
                            if parts[i].upper() in ['TRANSFER', 'PAYMENT', 'CASH_OUT', 'CASH_IN', 'DEBIT']:
                                trans_type = parts[i].upper()
                                amount = float(parts[i + 1])
                                date = parts[0]
                                to_name = parts[i + 10] if len(parts) > i + 10 else ""
                                description = " ".join(parts[i + 6:]) if len(parts) > i + 6 else ""
                                transactions.append({
                                    "Date": date,
                                    "Type": trans_type,
                                    "Amount": amount,
                                    "TO_NAME": to_name.upper(),
                                    "Description": description
                                })
                                break
                    except:
                        continue
    return pd.DataFrame(transactions)

# Summarize total per transaction type + Airtime spend
def summarize(df):
    summary_df = df.groupby("Type")["Amount"].sum().reset_index()
    summary_df.columns = ["Transaction_Type", "Total_Amount"]  # Safe keys
    airtime_total = df[df['TO_NAME'] == 'MTNONLINEAIRTIMEVENDOR']['Amount'].sum()
    return summary_df.to_dict(orient="records"), round(airtime_total, 2)

# Main upload view
def upload_view(request):
    if request.method == "POST":
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['file']
            df = parse_pdf(pdf_file)
            if df.empty:
                return render(request, "analyzer/upload.html", {"form": form, "error": "No valid transactions found."})
            summary, airtime = summarize(df)
            table_data = df.to_dict(orient="records")
            # Store CSV data in a hidden form field instead of session
            csv_data = df.to_csv(index=False)
            return render(request, "analyzer/result.html", {
                "summary": summary,
                "airtime": airtime,
                "table": table_data,
                "csv_data": csv_data
            })
    else:
        form = UploadPDFForm()
    return render(request, "analyzer/upload.html", {"form": form})

# CSV export view
def download_csv(request):
    if request.method == "POST":
        csv_data = request.POST.get('csv_data', '')
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="momo_transactions.csv"'
        return response
    return HttpResponse("No CSV data available", status=400)
