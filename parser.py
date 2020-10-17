import csv


date = []
addresses = []


def csv_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=';')
    for row in reader:
        #tmp = row;
        date.append(row['date'])
        addresses.append(row['address'])
    return {"date": date, "address": addresses}


if __name__ == "__main__":
    csv_path = "lite.csv"
    with open(csv_path, "r") as f_obj:
        csv_reader(f_obj)