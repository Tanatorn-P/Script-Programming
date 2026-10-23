import os
import openpyxl

def create_sample_data():
    os.makedirs('data', exist_ok=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "SalesData"

    headers = ["Product Name", "Quantity", "Unit Price"]
    ws.append(headers)

    data = [
        ["Laptop", 2, 1200.50],
        ["Mouse", 5, 25.00],
        ["Keyboard", 3, 75.99],
        ["Monitor", 1, 300.00],
        ["Projector", 1, 850.00],
        ["Webcam", 10, 45.00],
        ["Headset", 4, 99.99],
        ["SSD", 2, 180.00],
        ["Router", 1, 70.00]
    ]

    for row in data:
        ws.append(row)

    file_path = os.path.join('data', 'input_data.xlsx')
    wb.save(file_path)
    print(f"Sample data successfully created at: {file_path}")

if __name__ == "__main__":
    create_sample_data()