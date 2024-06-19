import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(message)s')


class BinPrinter:
    def __init__(self, input, output, dtype, shape):
        self.input = input
        self.dtype = dtype
        self.shape = shape
        self.output = output
    
    def read_bin(self):
        # 根据dtype的类型读取bin文件
        if self.dtype == 'float32':
            data = np.fromfile(self.input, dtype=np.float32)
        elif self.dtype == 'float64':
            data = np.fromfile(self.input, dtype=np.float64)
        elif self.dtype == 'int32':
            data = np.fromfile(self.input, dtype=np.int32)
        elif self.dtype == 'int64':
            data = np.fromfile(self.input, dtype=np.int64)
        elif self.dtype == 'uint8':
            data = np.fromfile(self.input, dtype=np.uint8)
        elif self.dtype == 'uint16':
            data = np.fromfile(self.input, dtype=np.uint16)
        elif self.dtype == 'uint32':
            data = np.fromfile(self.input, dtype=np.uint32)
        elif self.dtype == 'uint64':
            data = np.fromfile(self.input, dtype=np.uint64)
        else:
            raise ValueError('Unsupported dtype: {}'.format(self.dtype))
        
        return data
    
    def transform_to_dataframe(self, data):
        # 异常处理和输入验证
        if data is None:
            raise ValueError("Data cannot be None.")
        if not isinstance(self.shape, (list, tuple)) or not all(isinstance(dim, int) for dim in self.shape):
            raise ValueError("Shape must be a list or tuple of integers.")
        if len(self.shape) < 2:
            raise ValueError("Data must be at least two-dimensional.")
        
        # 动态索引名称生成
        index_names = ['dim{}'.format(i) for i in range(1, len(self.shape))]
        
        # 使用numpy的reshape方法来调整数据的形状，-1表示自动计算这一维的大小
        reshaped_data = data.reshape(-1, self.shape[-1])
        
        # 动态构建MultiIndex的参数和DataFrame的列名
        index = pd.MultiIndex.from_product([range(dim) for dim in self.shape[:-1]], names=index_names)
        columns = [str(i) for i in range(self.shape[-1])]
        
        # 创建DataFrame
        df = pd.DataFrame(reshaped_data, index=index, columns=columns)
        
        return df
    def print_bin(self):
        data = self.read_bin()
        self.df = self.transform_to_dataframe(data)

        fmt = '{:.' + str(3) + 'f}'        
        pd.set_option('display.float_format', fmt.format)
        pd.set_option('display.width', None)
        pd.set_option('display.unicode.ambiguous', True)
        pd.set_option('display.unicode.east_asian_width', True)
        pd.set_option('display.max_rows', 10)
        pd.set_option('display.max_columns', 40)
        logging.info("\n----------------------------------------------------------------------------- show data -----------------------------------------------------------------------------")
        logging.info("input:{}, shape:{}, dtype:{}".format(self.input, self.shape, self.dtype))
        logging.info("\n{}".format(self.df))
        logging.info("-----------------------------------------------------------------------------  end show -----------------------------------------------------------------------------")
        
    def save_data(self):
        self.df.to_csv(self.output, sep='\t', index=True, header=True)
        logging.info("\n[WARNING] total result saved to: {}".format(self.output))

def data_print(args):
    printer = BinPrinter(args.bin_file, args.output, args.dtype, args.shape)
    printer.print_bin()
    printer.save_data()

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Print bin file')
#     parser.add_argument('--bin', type=str, help='bin file')
#     parser.add_argument('--output', type=str, help='output file')
#     args = parser.parse_args()
#     printer = BinPrinter(args.bin, args.output)

