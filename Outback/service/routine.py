import decimal


def decimal_to_float(item):
    for key, value in item.items():
        if type(value) is decimal.Decimal:
            if value == value.to_integral_value():
                item[key] = int(value)
            else:
                item[key] = float(value)
        elif type(value) is dict:
            item[key] = decimal_to_float(value)
        elif type(value) is list:
            for i in range(0, len(value)):
                if type(value[i]) is decimal.Decimal:
                    if item[key][i] == item[key][i].to_integral_value():
                        item[key][i] = int(item[key][i])
                    else:
                        item[key][i] = float(item[key][i])
                elif type(value[i]) is dict:
                    item[key][i] = decimal_to_float(value[i])

    return item
