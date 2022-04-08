"""
Сравнение форматов сериализации
по времени сериализации\десериализации и размеру сериализованного объекта
"""

import sys
from timeit import timeit

import pandas as pd

if __name__ == '__main__':
    test_data = {
        "string_data": r"Lorem ipsum dolor sit amet, consectetur adipiscing"
                       "elit. Mauris adipiscing adipiscing placerat."
                       "Vestibulum augue augue, pellentesque quis sollicitudin id, adipiscing.",
        "array_data": [i for i in range(100)],
        "dict_data": {str(x): x + 1 for x in range(100)},
        "int_data": 123,
        "float_data": 123.09,
    }

    setup_pickle = f"import pickle ; " \
                   f"d={test_data} ;  " \
                   f"src = pickle.dumps(d, 2)"

    setup_json = f"import json; " \
                 f"d={test_data} ; " \
                 f"src = json.dumps(d)"

    setup_yaml = f"import yaml; " \
                 f"d={test_data} ; " \
                 f"src = yaml.dump(d)"

    setup_xml = f"from dicttoxml import dicttoxml;" \
                f"from xml.dom.minidom import parseString; " \
                f"d={test_data}; " \
                f"src = dicttoxml(d)"

    setup_proto = f"from google.protobuf import json_format; " \
                  f"from google.protobuf.struct_pb2 import Struct; " \
                  f"d={test_data}; " \
                  f"src = Struct(); " \
                  f"src.update(d)"

    setup_msgpack = f"import msgpack; " \
                    f"d={test_data}; " \
                    f"src = msgpack.packb(d); "

    # (title, setup, enc_test, dec_test)
    tests = [
        ('[pickle (native)]', setup_pickle, 'pickle.dumps(d, 2)', 'pickle.loads(src)'),
        ('[json]', setup_json, 'json.dumps(d)', 'json.loads(src)'),
        ('[yaml]', setup_yaml, 'yaml.dump(d)', 'yaml.safe_load(src)'),
        ('[xml]', setup_xml, 'dicttoxml(d)', 'parseString(src)'),
        ('[protobuf]', setup_proto, 's = Struct(); s.update(d)',
         'json_format.MessageToDict(src)'),
        ('[msgpack]', setup_msgpack, 'msgpack.packb(d)', 'msgpack.unpackb(src)'),
    ]

    loops = 100
    enc_table = []
    dec_table = []
    src = None
    print(f"Running tests ({loops} loops each)")
    for title, setup, enc_test, dec_test in tests:
        print(f"--------------{title}--------------")
        print(" [Encode]", enc_test)
        result = timeit(enc_test, setup, number=loops)
        exec(setup)
        enc_table.append([title, result, sys.getsizeof(src)])
        print(" [Decode]", dec_test)
        result = timeit(dec_test, setup, number=loops)
        dec_table.append([title, result])
        print("------------------------------")

    enc_table.sort(key=lambda x: x[1])
    dec_table.sort(key=lambda x: x[1])

    report_encode = pd.DataFrame(enc_table, columns=['Package', 'Seconds', 'Size'])
    report_decode = pd.DataFrame(dec_table, columns=['Package', 'Seconds'])

    print("\nEncode report\n", report_encode)
    print("\nDecode report\n", report_decode)
