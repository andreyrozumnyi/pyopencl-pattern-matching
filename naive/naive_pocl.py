import pyopencl as cl
import numpy


def main():
    # Set up OpenCL
    context = cl.create_some_context(False) #don't ask user about platform
    queue = cl.CommandQueue(context)

    with open("resources/naive_pocl.cl", "r") as kernel_file:
        kernel_src = kernel_file.read()

    program = cl.Program(context, kernel_src).build()

    #read data
    string = "acbcbck"
    pattern = "cbc"

    #initialize the result array
    matches = numpy.zeros(len(string)).astype(numpy.int)

    # Create the input (string, pattern) strings in device memory and copy data from host
    d_str = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=string.encode())
    d_pat = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=pattern.encode())
    # Create the output (matches) string in device memory
    d_matches = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, matches.nbytes)

    search = program.naive_search
    search.set_scalar_arg_dtypes([None, None, int, int, None])
    search(queue, (len(string)-len(pattern)+1, ), None, d_str, d_pat, len(string), len(pattern), d_matches)

    # Wait for the commands to finish before reading back
    queue.finish()

    # Read back the results from the compute device
    cl.enqueue_copy(queue, matches, d_matches)

    print (matches)


def read_data_from(file_name):
    """ read all data from file """
    with open(file_name, 'r') as file:
        string = file.read()
    return string

main()



