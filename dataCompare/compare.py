import logging
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(message)s')

class BinCompare:
    
    def __init__(self, bin1, bin2, dtype, shape, output):
        self.bin1 = bin1
        self.bin2 = bin2
        self.dtype = dtype
        self.shape = shape
        self.output = output
    def read_bin(self):
        # 根据dtype的类型读取bin文件
        if self.dtype == 'float32':
            data1 = np.fromfile(self.bin1, dtype=np.float32)
            data2 = np.fromfile(self.bin2, dtype=np.float32)
        elif self.dtype == 'float64':
            data1 = np.fromfile(self.bin1, dtype=np.float64)
            data2 = np.fromfile(self.bin2, dtype=np.float64)
        elif self.dtype == 'int32':
            data1 = np.fromfile(self.bin1, dtype=np.int32)
            data2 = np.fromfile(self.bin2, dtype=np.int32)
        elif self.dtype == 'int64':
            data1 = np.fromfile(self.bin1, dtype=np.int64)
            data2 = np.fromfile(self.bin2, dtype=np.int64)
        elif self.dtype == 'uint8':
            data1 = np.fromfile(self.bin1, dtype=np.uint8)
            data2 = np.fromfile(self.bin2, dtype=np.uint8)
        elif self.dtype == 'uint16':
            data1 = np.fromfile(self.bin1, dtype=np.uint16)
            data2 = np.fromfile(self.bin2, dtype=np.uint16)
        elif self.dtype == 'uint32':
            data1 = np.fromfile(self.bin1, dtype=np.uint32)
            data2 = np.fromfile(self.bin2, dtype=np.uint32)
        elif self.dtype == 'uint64':
            data1 = np.fromfile(self.bin1, dtype=np.uint64)
            data2 = np.fromfile(self.bin2, dtype=np.uint64)
        else:
            raise ValueError('Unsupported dtype: {}'.format(self.dtype))
        
        return data1, data2
    
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

    def compare_bins(self):
        data1, data2 = self.read_bin()

        # 计算bin1和bin2的cosine相似度和最大误差，以及最大误差的位置
        cosine_similarity = np.dot(data1, data2) / (np.linalg.norm(data1) * np.linalg.norm(data2))
        max_error = np.max(np.abs(data1 - data2))
        max_error_index = np.unravel_index(np.argmax(np.abs(data1 - data2)), data1.shape)

        self.df1 = self.transform_to_dataframe(data1)
        self.df2 = self.transform_to_dataframe(data2)

        self.result_df = self.df1.compare(self.df2)

        fmt = '{:.' + str(3) + 'f}'
        pd.set_option('display.float_format', fmt.format)
        pd.set_option('display.width', None)
        pd.set_option('display.unicode.ambiguous', True)
        pd.set_option('display.unicode.east_asian_width', True)
        pd.set_option('display.max_rows', 10)
        pd.set_option('display.max_columns', 40)
        logging.info("\n----------------------------------------------------------------------------- show data -----------------------------------------------------------------------------")
        logging.info("input:{},{}, shape:{}, dtype:{}".format(self.bin1, self.bin2, self.shape, self.dtype))
        logging.info("Cosine Similarity: {:.6f}".format(cosine_similarity))
        logging.info("Max Error: {:.6f}".format(max_error))
        logging.info("Max Error Index: {}".format(max_error_index))
        logging.info("\n{}".format(self.result_df))
        logging.info("-----------------------------------------------------------------------------  end show -----------------------------------------------------------------------------")

    def save_result(self):
        self.result_df.to_csv(self.output, sep='\t', index=True, header=True, na_rep='same')
        logging.info("\n[WARNING] total result saved to: {}".format(self.output))
    
def data_compare(args):
    compare = BinCompare(args.bin_file1, args.bin_file2, args.dtype, args.shape, args.output)
    compare.compare_bins()
    compare.save_result()