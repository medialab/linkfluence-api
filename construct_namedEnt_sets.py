import csv, sys

if __name__ =='__main__':
    argsize = len(sys.argv)
    if argsize < 2:
        sysexit('USAGE : '+sys.argv[0]+' [file1] [file2] ...')
    uniq_set_list = []
    for i in range(1, argsize):
        with open(sys.argv[i], 'r') as f:
            uniq_set_list.append(set())
            src_CSV = csv.reader(f)
            for line_num, record in enumerate(src_CSV):
                if not line_num:
                    continue
                uniq_set_list[-1].add(record[1])

    intersect_set = uniq_set_list[0]
    for current_set_index in range(1, len(uniq_set_list)):
        intersect_set &= uniq_set_list[current_set_index]

    for key in intersect_set:
        print(key)
