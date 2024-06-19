import logging
import numpy as np
import argparse
from ..dataPrint import BinPrinter


# 按照给定模式生成多维数组

def get_numpy_dtype(type_str):
    if type_str == 'float32':
        return np.float32
    elif type_str == 'float16':
        return np.float16
    elif type_str == 'int32':
        return np.int32
    elif type_str == 'int16':
        return np.int16
    elif type_str == 'int8':
        return np.int8
    elif type_str == 'uint8':
        return np.uint8
    elif type_str == 'bool':
        return np.bool
    elif type_str == 'int64':
        return np.int64
    elif type_str == 'uint16':
        return np.uint16
    elif type_str == 'uint32':
        return np.uint32
    elif type_str == 'uint64':
        return np.uint64
    else :
        logging.error('dtype error')
        return


import numpy as np

def generate_diagonal_matrix(shape, dtype):
    """
    Generate a multi-dimensional matrix with diagonal data along the last two dimensions.
    
    Parameters:
    shape (tuple): The shape of the multi-dimensional matrix. The last two dimensions must be equal.
    
    Returns:
    np.ndarray: The generated matrix with diagonal data.
    """
    if shape[-1] != shape[-2]:
        raise ValueError("The last two dimensions must be equal to form a square matrix.")

    # Create an empty matrix with the given shape
    matrix = np.zeros(shape, dtype=dtype)

    # Set the diagonal elements to 1
    indices = np.arange(shape[-1])
    matrix[..., indices, indices] = 1
    
    return matrix

class Generator:

    def __init__(self, output, dtype, shape, mode, max, min):
        self.output = output
        self.dtype_str = dtype
        self.dtype = get_numpy_dtype(dtype)
        self.shape = shape
        self.mode = mode
        self.max = max
        self.min = min

    def generate(self):
        if self.mode == 'random':
            data = np.random.rand(*self.shape).astype(self.dtype)
        elif self.mode == 'zero':
            data = np.zeros(self.shape, dtype=self.dtype)
        elif self.mode == 'one':
            data = np.ones(self.shape, dtype=self.dtype)
        elif self.mode == 'range':
           data = np.random.randint(self.min, self.max, self.shape, dtype=self.dtype)
        elif self.mode == 'eye':
            data = generate_diagonal_matrix(self.shape, self.dtype)
        elif self.mode == 'increase':
            data = np.arange(np.prod(self.shape), dtype=self.dtype).reshape(self.shape)
        elif self.mode == 'decrease':
            data = np.arange(np.prod(self.shape), dtype=self.dtype)[::-1].reshape(self.shape) 
        else:
            logging.error('mode error')
            return
        # 保存为bin文件
        # print(data)
        data.tofile(self.output)

        printer = BinPrinter(self.output, "", self.dtype_str, self.shape)
        printer.print_bin()

def data_generate(args):
    generator = Generator(args.output, args.dtype, args.shape, args.mode, args.max, args.min)
    generator.generate()