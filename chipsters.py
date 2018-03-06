import sys


def print_line(address, num_deliveries, kilos):
    out = '"' + address["site"] + '";'
    out += '"' + address["street"] + '";'
    out += '"' + address["postal"] + '";'
    out += '"' + address["city"] + '";'
    out += str(num_deliveries) + ';'
    out += "{0:.2f}".format(kilos).replace('.', ',') + ';'
    out += '"' + get_maps_url(address) + '"'
    print out


def get_maps_url(address):
    base_url = 'https://www.google.com/maps/search/?api=1&query='
    street = address["street"].replace(' ', '+').replace(',', '%2C')
    city = address["city"].replace(' ', '+').replace(',', '%2C')
    return base_url + street + '+' + address["postal"] + '+' + city


def parse_address(line):
    addr = {}
    addr["site"] = line[0:29].strip()
    tokens = filter(None, line[29:].split('  '))
    tokens = map(str.strip, tokens)
    addr["street"] = tokens[0].split(None, 1)[1]
    addr["postal"] = tokens[1].split()[0]
    addr["city"] = tokens[1].split(None, 1)[1]
    return addr


filename = sys.argv[1]

with open(filename) as f:
    content = f.readlines()

address = None
kilos = 0
num_deliveries = 0
i = 0
print '"Kohde";"Katuosoite";"Postinumero";"Kaupunki";"Lahetteita";"Kiloja";"Maps"'

while i < len(content):
    line = content[i].strip()
    if not line:
        i = i + 1
        continue
    if "Pudotuksia" in line:
        i = i + 1
        continue
    if "P U D O T U S L I S T A" in line:
        i = i + 6
        continue
    if address is None:
        address = parse_address(line)
        i = i + 1
        continue
    if "Huomautus:" not in line:
        if len(line) is 89 or len(line) is 23:  # kilomaara
            data = line.split()
            kilos += float(data[-1].replace(',', '.'))
            num_deliveries = num_deliveries + 1
            i = i + 1
            continue
        else:  # address
            print_line(address, num_deliveries, kilos)
            address = None
            num_deliveries = 0
            kilos = 0
            continue
    else:  # huomautus
        i = i + 1
        continue

print_line(address, num_deliveries, kilos)
