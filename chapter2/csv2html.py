"""
Читает данные в формате CSV и выводит HTML таблицу, содержащую эти данные
"""
import sys
import xml.sax.saxutils
def print_start():
    print("<table border='1'>")


def print_end():
    print(r"</table>")


def extract_fields(line):
    fields = []
    field = ''
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None:
                quote = c
            elif quote == c:
                quote = None
            else:
                field += c
            continue
        if quote is None and c == ",":
            fields.append(field)
            field = ''
        else:
            field += c
    if field:
        fields.append(field)
    return fields



def print_line(line, color, maxwidth, form):
    print("<tr bgcolor='{0}'>".format(color))
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print('<td></td>')
        else:
            number = field.replace(',', '')
            try:
                x = float(number)
                out = "<td align='right'>{0:" + form + "}</td>"
                print(out.format(round(x)))
            except ValueError:
                field = field.title()
                field = field.replace(' And', ' and')
                field = xml.sax.saxutils.escape(field)
                if len(field) <= maxwidth:
                    print("<td>{0}</td>".format(field))
                else:
                    print("<td>{0:.{1}} ...</td>".format(field, maxwidth))
    print("</tr>")




def main():
    maxwidth, form = process_options()
    if not maxwidth:
        return 0
    print_start()
    count = 0
    while True:
        try:
            line = input()
            if count == 0:
                color ='lightgreen'
            elif count % 2:
                color = 'white'
            else:
                color = 'lightyellow'
            print_line(line, color, maxwidth, form)
            count += 1
        except EOFError:
            break
    print_end()


def process_options():
    maxwidth = 100
    form = '.0f'
    if len(sys.argv) > 1:
        if (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
            print('Используйте:', file=sys.stderr)
            print("""csv2html.py [maxwidth=int] [format=str] < infile.csv > outfile.html""", file=sys.stderr)
            return (None, None)
        elif len(sys.argv) == 3:
            form = sys.argv[2]
        else:
            try:
                maxwidth = int(sys.argv[1])
            except ValueError as err:
                print(err, file=sys.stderr)
                return (None, None)
    return maxwidth, form


main()