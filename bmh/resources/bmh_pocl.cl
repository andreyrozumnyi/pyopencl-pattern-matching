__kernel void bmh_search(
    __global char* text,
    __global char* pattern,
    __global int* table,
    const int text_len,
    const int pattern_len,
    const int pieces_num,
    __global int* matches)
{
    int i = get_global_id(0);
    if (i < pattern_len) {
       __private int A = "A" - "0";
/*     printf("%d\n", (char)("A"));
       printf("%d\n", (char)("d")); */
    }
}






