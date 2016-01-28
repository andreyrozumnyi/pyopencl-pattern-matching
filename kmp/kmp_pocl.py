import pyopencl as cl
import numpy
PIECES_NUM = 1


def main():
    # Set up OpenCL
    context = cl.create_some_context(False)  # don't ask user about platform
    queue = cl.CommandQueue(context)

    with open("resources/kmp_pocl.cl", "r") as kernel_file:
        kernel_src = kernel_file.read()

    program = cl.Program(context, kernel_src).build()

    # read data
    string = "abcbcbasdca"
    pattern = "bcb"
    if len(string)/PIECES_NUM <= len(pattern) or PIECES_NUM > len(string):
        raise ValueError("Choose less number of pieces as one piece length less than pattern length "
                         "or pieces number is more than string length")

    # calculate prefix function for pattern
    pi = numpy.array(prefix_func(pattern)).astype(numpy.int)
    # initialize the result array
    matches = numpy.zeros(len(string)).astype(numpy.int)

    # Create the input (string, pattern, pi) strings in device memory and copy data from host
    d_str = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=string.encode())
    d_pat = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=pattern.encode())
    d_pi = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=pi)
    # Create the output (matches) string in device memory
    d_matches = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, matches.nbytes)

    search = program.kmp_search
    search.set_scalar_arg_dtypes([None, None, None, int, int, int, None])
    search(queue, (len(string)-len(pattern)+1, ), None, d_str, d_pat, d_pi,
           len(string), len(pattern), PIECES_NUM, d_matches)

    # Wait for the commands to finish before reading back
    queue.finish()

    # Read back the results from the compute device
    cl.enqueue_copy(queue, matches, d_matches)

    print(matches)


def prefix_func(pattern):
    """ returns prefix function array of the given string """
    str_len = len(pattern)
    pi = [0]*str_len
    for i in range(1, str_len):
        k = pi[i-1]
        while k > 0 and pattern[k] != pattern[i]:
            k = pi[k-1]

        if pattern[k] == pattern[i]:
            k += 1

        pi[i] = k

    return pi


def read_data_from(file_name):
    """ read all data from file """
    with open(file_name, 'r') as file:
        string = file.read()
    return string

main()