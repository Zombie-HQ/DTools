import argparse
import logging

from .dataPrint import data_print
from .dataGenerate import data_generate

parser = argparse.ArgumentParser(prog='DTool', description='Debug Tools')
subparsers = parser.add_subparsers(help='sub-command help', dest='command')

def shape_to_list(shape):
    parts = str(shape).split('x')
    return [int(part) for part in parts]

# data print
print_parser = subparsers.add_parser('print', help='Print data')
print_parser.add_argument('bin_file', help='Binary file to print')
print_parser.add_argument('-s', '--shape', type=shape_to_list, help='Shape of the data, eg: -s 1x2x3x4')
print_parser.add_argument('-d', '--dtype', type=str, help='Data type of the data, eg: -d float32')
print_parser.add_argument('-o', '--output', type=str, default='data_print.log', help='Output file, eg: -o data_print.log')
print_parser.add_argument('-n', '--num_decimals', type=int, default=3, help='Number of decimals to print, eg: -n 3')
print_parser.set_defaults(func=data_print)

# data generate
generate_parser = subparsers.add_parser('generate', help='generate data, eg: python -m dtool generate -o data.bin -d float32 -s 1x2x3x4 -m random -max 100 -min 0')
generate_parser.add_argument('-o', '--output', type=str, help='output file path, eg: -o data.bin')
generate_parser.add_argument('-d', '--dtype', type=str, help='data type, eg: -d float32')
generate_parser.add_argument('-s', '--shape', type=shape_to_list, help='shape, eg: -s 1x2x3x4')
generate_parser.add_argument('-m', '--mode', type=str, default='ones', help='generate mode, eg: -m random')
generate_parser.add_argument('-max', type=int, default=100, help='max value, eg: -max 100')
generate_parser.add_argument('-min', type=int, default=0, help='min value, eg: -min 0')
generate_parser.set_defaults(func=data_generate)

if __name__ == '__main__':
    args = parser.parse_args()
    # logging.basicConfig(level=logging.INFO, filename=args.output, filemode='w', format='%(message)s')
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    args.func(args)

