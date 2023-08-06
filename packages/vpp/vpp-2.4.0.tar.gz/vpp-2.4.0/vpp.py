import os.path
from ctypes import *
from ctypes.util import find_library

vpp = CDLL(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'libvpp.so'))
assert(vpp)

class file_p(c_void_p):
    pass

# FILE* vpp_init_input(const char* filename, int* w, int* h, int* d);
f_init_input = vpp.vpp_init_input
f_init_input.restype = file_p
f_init_input.argtypes = [c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

def raw_init_input(filename):
    w = c_int()
    h = c_int()
    d = c_int()
    f = f_init_input(filename.encode('utf-8'), w, h, d)
    return f, w.value, h.value, d.value

# int vpp_init_inputs(int n, FILE** files, const char** filenames, int* w, int* h, int* d);
f_init_inputs = vpp.vpp_init_inputs
f_init_inputs.restype = c_int
f_init_inputs.argtypes = [c_int, POINTER(file_p), POINTER(c_char_p), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

def raw_init_inputs(filenames):
    n = len(filenames)
    cfilenames = [f.encode('utf-8')  for f in filenames]
    cfilenames = (c_char_p * n)(*cfilenames)
    files = (file_p * n)()
    ws = (c_int * n)()
    hs = (c_int * n)()
    ds = (c_int * n)()
    r = f_init_inputs(n, files, cfilenames, ws, hs, ds)
    if not r:
        return None
    files = [files[i] for i in range(n)]
    ws = [ws[i] for i in range(n)]
    hs = [hs[i] for i in range(n)]
    ds = [ds[i] for i in range(n)]
    return files, ws, hs, ds

# FILE* vpp_init_output(const char* filename, int w, int h, int d);
f_init_output = vpp.vpp_init_output
f_init_output.restype = file_p
f_init_output.argtypes = [c_char_p, c_int, c_int, c_int]

def raw_init_output(filename, w, h, d):
    f = f_init_output(filename.encode('utf-8'), w, h, d)
    return f

# int vpp_read_frame(FILE* in, float* frame, int w, int h, int d);
f_read_frame = vpp.vpp_read_frame
f_read_frame.restype = c_int
f_read_frame.argtypes = [file_p, POINTER(c_float), c_int, c_int, c_int]

def raw_read_frame(file, array):
    r = f_read_frame(file, array.ctypes.data_as(POINTER(c_float)), array.shape[0], array.shape[1], array.shape[2])
    return r

# int vpp_write_frame(FILE* out, float* frame, int w, int h, int d);
f_write_frame = vpp.vpp_write_frame
f_write_frame.restype = c_int
f_write_frame.argtypes = [file_p, POINTER(c_float), c_int, c_int, c_int]

def raw_write_frame(file, array):
    w = array.shape[0]
    h = len(array.shape) <= 1 and 1 or array.shape[1]
    d = len(array.shape) <= 2 and 1 or array.shape[2]
    array = np.ascontiguousarray(array, dtype='float32')
    r = f_write_frame(file, array.ctypes.data_as(POINTER(c_float)), w, h, d)
    return r


class InputStream:
    def __init__(self, file, w, h, d):
        self.file = file
        self.w = w
        self.h = h
        self.d = d
        self.array = np.ascontiguousarray(np.empty((w, h, d)), dtype='float32')

    def read(self):
        if raw_read_frame(self.file, self.array):
            return self.array.copy()

class OutputStream:
    def __init__(self, file, w, h, d):
        self.file = file
        self.w = w
        self.h = h
        self.d = d

    def write(self, array):
        assert(array is not None)
        assert(len(array.shape) in (2,3))
        assert(array.shape[0] == self.w)
        assert(array.shape[1] == self.h)
        d = len(array.shape) == 2 and 1 or array.shape[2]
        assert(d == self.d)
        return raw_write_frame(self.file, array)

def init_input(filename):
    assert(type(filename) == str)
    f, w, h, d = raw_init_input(filename)
    if not f:
        return None
    return InputStream(f, w, h, d)

def init_inputs(filenames):
    assert(type(filenames) in (list, tuple))
    files, ws, hs, ds = raw_init_inputs(filenames)
    if not files:
        return None
    return [InputStream(files[i], ws[i], hs[i], ds[i]) for i in range(len(files))]

def init_output(filename, w, h, d):
    f = raw_init_output(filename, w, h, d)
    if not f:
        return None
    return OutputStream(f, w, h, d)


__all__ = {
    'InputStream': InputStream,
    'OutputStream': OutputStream,
    'init_input': init_input,
    'init_inputs': init_inputs,
    'init_output': init_output
}

