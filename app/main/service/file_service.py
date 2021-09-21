import xlsxwriter
import tempfile


def generate_typhoon_report(tracking_information):

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        workbook = xlsxwriter.Workbook(tmp.name)

        worksheet = workbook.add_worksheet("Tracking Information")
        # tracking_header = ['id', 'is_event', 'name', 'code', 'year', 'month', 'day', 'hour', 'lat', 'lon', 'pressure', 'wind','classification']
        tracking_header = list(tracking_information[0].keys())
        write_table(tracking_header , tracking_information,worksheet)

        tmp.close()
        workbook.close()
        return tmp.name


def write_table(headers, data, ws):
    first_row = 0
    for header in headers:
        col = headers.index(header)  # We are keeping order.
        ws.write(first_row, col, header)  # We have written first row which is the header of worksheet also.

    row = 1
    for row_dict in data:
        for _key, _value in row_dict.items():
            col = headers.index(_key)
            ws.write(row, col, _value)
        row += 1  # enter the next row
