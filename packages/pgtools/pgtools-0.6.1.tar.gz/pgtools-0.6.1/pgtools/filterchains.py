__author__ = 'dskola'
import datetime
import multiprocessing
import os

import numpy
from pgtools import toolbox

THREADS = 8
REPORTING_INTERVAL = 1000000
CHAINFILE_BASEPATH = os.path.join(os.environ['HOME'], 'oasis_local/chain_files')
INTERVAL_BASEPATH = os.path.join(os.environ['HOME'], 'oasis_local/best_intervals')
INTERVAL_FILE_TEMPLATE = '{}To{}.best.txt'
CHAINFILE_TEMPLATE = '{}To{}.over.chain'
MAX_OPEN_FILES = 512
EMPTY_REF_CHROM_VALUE = 65535

TMP_DIR = '/tmp/{}'.format(os.environ['USER'])

def get_liftover_intervals(dest_build, dest_chrom_lengths, source_build, source_chrom_lengths,
                           multiprocessing_method='None', interval_basepath=INTERVAL_BASEPATH,
                           chainfile_basepath=CHAINFILE_BASEPATH, score_threshold=None, query_size_threshold=None,
                           ref_size_threshold=None, source_chromosome_dialect='ucsc', dest_chromosome_dialect='ucsc'):
    """
    Wrapper function
    :param dest_build:
    :param dest_chrom_lengths:
    :param source_build:
    :param source_chrom_lengths:
    :param multiprocessing_method:
    :param interval_basepath:
    :param chainfile_basepath:
    :param score_threshold:
    :param query_size_threshold:
    :param ref_size_threshold:
    :param source_chromosome_dialect:
    :param dest_chromosome_dialect:
    :return:
    """
    return get_liftover_intervals_bucket(dest_build=dest_build,
                                         dest_chrom_lengths=dest_chrom_lengths,
                                         source_build=source_build,
                                         source_chrom_lengths=source_chrom_lengths,
                                         multiprocessing_method=multiprocessing_method,
                                         interval_basepath=interval_basepath,
                                         chainfile_basepath=chainfile_basepath,
                                         score_threshold=score_threshold,
                                         query_size_threshold=query_size_threshold,
                                         ref_size_threshold=ref_size_threshold,
                                         source_chromosome_dialect=source_chromosome_dialect,
                                         dest_chromosome_dialect=dest_chromosome_dialect)


def get_liftover_intervals_bucket(dest_build, dest_chrom_lengths, source_build, source_chrom_lengths,
                           multiprocessing_method='None', interval_basepath=INTERVAL_BASEPATH,
                           chainfile_basepath=CHAINFILE_BASEPATH, score_threshold=None, query_size_threshold=None,
                           ref_size_threshold=None, source_chromosome_dialect='ucsc', dest_chromosome_dialect='ucsc'):
    '''
    Returns a dictionary of mapped intervals between species that have been obtained from a liftOver chain file and
     filtered to be single-coverage in query AKA source (normally already filtered to be single coverage in reference AKA target).

    If this set does not exist in the specified path, generate it and save it to a file for future use.

    The filtering is done by keeping only the highest-scoring (usually also the longest) chains that cover a particular
    interval.

    The set of intervals returned is a dictionary of intervals keyed by query (source) chromosome, with coordinates relative
    to the query, and containing a data dictionary with keys for the corresponding chromosome in the reference as well as an
    offset of the reference position from the query position which can be applied to the query coordinates to regenerate
    the reference coordinates.

    :param dest_build:
    :param dest_chrom_lengths:
    :param source_build:
    :param source_chrom_lengths:
    :param interval_basepath:
    :param score_threshold:
    :param query_size_threshold:
    :param ref_size_threshold:
    :param source_chromosome_dialect:
    :param dest_chromosome_dialect:
    :return:
    '''
    toolbox.establish_path(interval_basepath)
    interval_fname = os.path.join(interval_basepath,
                                  INTERVAL_FILE_TEMPLATE.format(source_build, toolbox.first_upper(dest_build)))
    try:
        start_time = datetime.datetime.now()
        print(('Trying to load intervals from {}...'.format(interval_fname)))
        best_intervals = load_intervals(interval_fname)
    except (OSError, IOError):
        print('Can\'t load intervals, so need to generate them')
        generate = True
    else:
        print(('Succesfully loaded intervals from file in {}.'.format(datetime.datetime.now() - start_time)))
        generate = False

    if generate:
        chain_filename = os.path.join(chainfile_basepath,
                                      '{}To{}.over.chain'.format(dest_build, toolbox.first_upper(source_build)))

        filtering_start_time = datetime.datetime.now()

        # load intervals from chain file
        print(('Generating mapping for {} to {} using chain file {}'.format(source_build, dest_build, chain_filename)))

        chromosome_buckets, chrom_indexer = chains_to_buckets(chain_filename, source_build=source_build,
                                              source_chrom_lengths=source_chrom_lengths, dest_build=dest_build,
                                              dest_chrom_lengths=dest_chrom_lengths,
                                              source_chromosome_dialect=source_chromosome_dialect,
                                              dest_chromosome_dialect=dest_chromosome_dialect)

        #mem-map up to MAX_OPEN_FILES chromosomes to conserve ram
        mapped_file_counter = 0
        for chrom in sorted(list(chromosome_buckets.keys()), reverse=True, key=lambda x: source_chrom_lengths[x]):
            if mapped_file_counter < MAX_OPEN_FILES:
                chromosome_buckets[chrom]['ref_chrom'] = toolbox.replace_with_mem_map(
                    chromosome_buckets[chrom]['ref_chrom'], read_only=True)
                chromosome_buckets[chrom]['ref_offset'] = toolbox.replace_with_mem_map(
                    chromosome_buckets[chrom]['ref_offset'], read_only=True)
            mapped_file_counter += 2

        if multiprocessing_method == 'pool':
            print(('Spawning up to {} subprocesses (using multiprocessing.Pool) to filter {} query chromosomes'.format(
                THREADS, len(chromosome_buckets))))
            p = multiprocessing.Pool(THREADS)
            param_list = [[query_chrom, chromosome_buckets[query_chrom], chrom_indexer] for query_chrom in
                          sorted(chromosome_buckets, reverse=True, key=lambda x: source_chrom_lengths[x])]
            results = p.map(buckets_to_intervals_chromslave, param_list)
            best_intervals = {}
            for query_chrom, filtered_intervals in results:
                best_intervals[query_chrom] = filtered_intervals
            del results

        elif multiprocessing_method == 'antfarm':
            raise Exception('Method currently not supported!')
        else:
            param_list = [[query_chrom, chromosome_buckets[query_chrom], chrom_indexer] for query_chrom in
                          sorted(chromosome_buckets, reverse=True, key=lambda x: source_chrom_lengths[x])]
            best_intervals = {}
            for paramset in param_list:
                query_chrom, filtered_intervals = buckets_to_intervals_chromslave(paramset)
                best_intervals[query_chrom] = filtered_intervals
        del chromosome_buckets

        print(('Done generating filtered intervals in {}.'.format(datetime.datetime.now() - filtering_start_time)))

        # Save intervals to file
        save_intervals(best_intervals, interval_fname)

    return best_intervals


def save_intervals(interval_tuple_dict, interval_fname):
    """
    Saves a dictionary of mapping intervals to the specified file name as a text file with the following format:

    Each chromosome is saved as a block of text whose first line is a header consisting of the '>' character followed
    by the query chromosome name.

    Immediately following this, each line defines an interval with the following tab-delimited fields:
    <query_start(int)> <size> <reference_chromosome(string)> <reference_offset(int), polarity("+" or "-")>

    Each block of intervals should be followed by a blank line but this is optional

    :param interval_dict:
    :param interval_fname:
    :return:
    """
    start_time = datetime.datetime.now()
    interval_count = 0

    with open(interval_fname, 'w') as interval_file:
        print(('Saving intervals to {}'.format(interval_fname)))
        for query_chrom in sorted(interval_tuple_dict):
            print(('\tSaving intervals for {}...'.format(query_chrom)))
            interval_file.write('>{}\n'.format(query_chrom))
            for interval_tuple in interval_tuple_dict[query_chrom]:
                interval_file.write('{}\t{}\t{}\t{}\t{}\n'.format(interval_tuple[0],
                                                                  interval_tuple[1] - interval_tuple[0],
                                                                  interval_tuple[2], interval_tuple[3],
                                                                  {1: '+', -1: '-'}[interval_tuple[4]]))
                interval_count += 1
            interval_file.write('\n')
    print(('Done saving {} intervals in {}'.format(interval_count, datetime.datetime.now() - start_time)))


# def chains_to_intervals(chain_fname, dest_build, dest_chrom_lengths, source_build, source_chrom_lengths,
# source_chromosome_dialect='ucsc', dest_chromosome_dialect='ucsc', score_threshold=0, query_size_threshold=0,
#                         ref_size_threshold=0):
#     chain_intervals = {}
#     for chrom in source_chrom_lengths:
#         chain_intervals[chrom] = intervaltree.IntervalTree()
#
#     header_fields = (
#         'dummy', 'score', 'tName', 'tSize', 'tStrand', 'tStart', 'tEnd', 'qName', 'qSize', 'qStrand', 'qStart', 'qEnd',
#         'id')
#     missing_chroms_ref = set([])
#     missing_chroms_query = set([])
#
#     print 'Generating mapping for {} to {} using chain file {}'.format(source_build, dest_build, chain_fname)
#
#     with open(chain_fname, 'rU') as chain_file:
#         print 'Building interval trees from chain file...'
#         start_time = datetime.datetime.now()
#         # self._initialize(pileup_dtype=destination_dtype)
#
#         new_chain = True
#         good_chain = False
#
#         for line_num, line in enumerate(chain_file):
#             if line_num % REPORTING_INTERVAL == 0:
#                 print 'Processing line {}'.format(line_num)
#             if new_chain and line != '\n':  # insurance against multiple blank lines
#                 header = toolbox.parse_line_dict(line, header_fields, split_char=' ', strict=True)
#                 assert header['dummy'] == 'chain'
#                 new_chain = False
#
#                 # relative offsets within the chain
#                 ref_chain_pos = 0
#                 query_chain_pos = 0
#
#                 ref_chrom = toolbox.convert_chroms(header['tName'], dest=dest_chromosome_dialect)
#                 query_chrom = toolbox.convert_chroms(header['qName'], dest=source_chromosome_dialect)
#
#                 good_chain = False
#                 chain_score = int(header['score'])
#
#                 if query_chrom in source_chrom_lengths:
#                     if int(header['qSize']) != source_chrom_lengths[query_chrom]:
#                         raise Exception('Error on line {}, chain {}. Chain file size of {} for query chromosome {} does not match source size of {}'.format(
#                             line_num, header['id'], header['qSize'], query_chrom, source_chrom_lengths[query_chrom]))
#                     else:
#                         if ref_chrom in dest_chrom_lengths:
#                             if int(header['tSize']) != dest_chrom_lengths[ref_chrom]:
#                                 raise Exception('Error on line {}, chain {}. Chain file size of {} for reference chromosome {} does not match destination size of {}'.format(
#                                     line_num, header['id'], header['tSize'], ref_chrom,
#                                     dest_chrom_lengths[ref_chrom]))
#                             elif (not score_threshold or chain_score >= score_threshold) and (
#                                             not query_size_threshold or header['qSize'] >= query_size_threshold) and (
#                                             not ref_size_threshold or header['tSize'] >= ref_size_threshold):
#                                 good_chain = True
#                         else:
#                             missing_chroms_ref.add(ref_chrom)
#                 else:
#                     missing_chroms_query.add(query_chrom)
#
#                 ref_chain_start = int(header['tStart'])
#                 query_chain_start = int(header['qStart'])
#
#             elif line == '\n':
#                 # start a new chain on the next line
#                 new_chain = True
#
#             elif good_chain:
#                 # it must be a data line
#                 split_line = line.split('\t')
#                 size = int(split_line[0])
#
#                 if len(split_line) == 3:
#                     ref_diff = int(split_line[1])
#                     query_diff = int(split_line[2])
#
#                 elif len(split_line) == 1:
#                     ref_diff = 0
#                     query_diff = 0
#
#                 else:
#                     raise Exception(
#                         'Encountered a chain alignment data line of length 2 on line {}. Unsure how to handle this.'.format(
#                             line_num))
#
#                 ref_start_pos = ref_chain_start + ref_chain_pos
#                 ref_end_pos = ref_start_pos + size
#                 ref_chain_pos += size + ref_diff
#
#                 query_start_pos = query_chain_start + query_chain_pos
#                 query_end_pos = query_start_pos + size
#                 query_chain_pos += size + query_diff
#
#                 ref_offset = ref_start_pos - query_start_pos
#                 # query_offset = query_start_pos - ref_start_pos
#                 if query_start_pos < 0:
#                     raise Exception('Error on line {}: query start position {} is before start of chromosome {} (0)'.format(line_num, query_start_pos, query_chrom))
#                 if ref_start_pos < 0:
#                     raise Exception('Error on line {}: reference start position {} is before start of chromosome {} (0)'.format(line_num, ref_start_pos, ref_chrom))
#                 if query_start_pos > source_chrom_lengths[query_chrom]:
#                     raise Exception('Error on line {}: query end position {} is after end of chromosome {} ({})'.format(line_num, query_end_pos, query_chrom, source_chrom_lengths[query_chrom]))
#                 if ref_end_pos > dest_chrom_lengths[ref_chrom]:
#                     raise Exception('Error on line {}: reference end position {} is after end of chromosome {} ({})'.format(line_num, ref_end_pos, ref_chrom, dest_chrom_lengths[ref_chrom]))
#
#                 chain_intervals[query_chrom].addi(query_start_pos, query_end_pos, {'score': chain_score,
#                                                                                    'ref_chrom': ref_chrom,
#                                                                                    'ref_offset': ref_offset})
#
#         print 'Done loading in {}'.format(datetime.datetime.now() - start_time)
#         if missing_chroms_ref:
#             print 'The following chromosomes in the chain file were missing in the destination organism: {}'.format(
#                 ','.join(sorted(list(missing_chroms_ref))))
#         if missing_chroms_query:
#             print 'The following chromosomes in the chain file were missing in the source organism: {}'.format(
#                 ','.join(sorted(list(missing_chroms_query))))
#     return chain_intervals


def load_intervals(interval_fname):
    """
    Parses a text file containing mapping intervals and returns a data structure consisting of a dictionary keyed
     by query chromosome that contains a list of tuples in the form (interval_start, interval_end, reference_chromosome, reference_offset)

    Assumes correct input -- currently no error trapping or accounting for malformed files
    :param interval_fname:
    :return:
    """
    interval_dict = {}
    with open(interval_fname, 'rU') as interval_file:
        for line in interval_file:
            if line != '\n':
                if line[0] == '>':
                    # new query chromosome
                    query_chromosome = line.strip()[1:]
                    interval_dict[query_chromosome] = []
                else:
                    try:
                        split_line = line.strip().split('\t')
                        query_start = int(split_line[0])
                        query_end = query_start + int(split_line[1])
                        ref_chromosome = split_line[2]
                        ref_offset = int(split_line[3])
                        polarity = {'+': 1, '-': -1}[split_line[4]]

                    except ValueError as ve:
                        print(split_line)

                    else:
                        interval_dict[query_chromosome].append(
                            (query_start, query_end, ref_chromosome, ref_offset, polarity))

    return interval_dict


# def interval_trees_to_tuples(interval_tree_dict):
#     """
#     Converts a data structure consiting of a dictionary of interval trees into a dictionary of sorted lists of tuples in the
# form (interval_start, interval_end, reference_chromosome, reference_offset)
#     :param interval_tree_dict:
#     :return:
#     """
#     interval_tuple_dict = {}
#     for query_chrom in interval_tree_dict:
#         interval_tuple_dict[query_chrom] = interval_tree_to_tuple_list(interval_tree_dict[query_chrom])
#     return interval_tuple_dict
#
#
# def interval_tree_to_tuple_list(interval_tree):
#     interval_tuple_list = []
#     for interval in sorted(interval_tree):
#         interval_tuple_list.append(
#             (interval.begin, interval.end, interval.data['ref_chrom'], interval.data['ref_offset']))
#     return interval_tuple_list


# def filter_intervals_chromslave(params):
#     """
#     Process intervals (find the highest scoring for each genome segment) for one chromosome
# """
#     chrom_start_time = datetime.datetime.now()
#     query_chrom, interval_chain = params
#
#     print '\tProcessing intervals for {}'.format(query_chrom)
#     print '\t\tSplitting {} intervals  for chromosome {} at intersections...'.format(len(interval_chain), query_chrom)
#     start_time = datetime.datetime.now()
#     interval_chain.split_overlaps()
#     print '\t\tDone in {}'.format(datetime.datetime.now() - start_time)
#
#     print '\t\tFiltering {} intervals for chromosome {} to keep only best alignment for each segment...'.format(
#         len(interval_chain), query_chrom)
#     start_time = datetime.datetime.now()
#     filtered_intervals = intervaltree.IntervalTree()
#
#     interval_counter = 0
#     while len(interval_chain) > 0:
#         i = interval_chain.pop()
#         interval_counter += 1
#         if interval_counter % REPORTING_INTERVAL == 0:
#             print('\t\t\tProcessing interval {} for chromosome {}'.format(interval_counter, query_chrom))
#         best_score = i.data['score']
#         best_interval = i
#         overlapping = interval_chain.search(i)
#         for j in overlapping:
#             if j.data['score'] > best_score:
#                 best_score = j.data['score']
#                 best_interval = j
#             interval_chain.remove(j)
#         filtered_intervals.add(best_interval)
#     print '\t\tDone in {}'.format(datetime.datetime.now() - start_time)
#     print '\tAll done with chromosome {} in {}'.format(query_chrom, datetime.datetime.now() - chrom_start_time)
#     return query_chrom, filtered_intervals
#
#
# def filter_intervals_chromslave_2(params):
#     """
#     Process intervals (find the highest scoring for each genome segment) for one chromosome
#      (interval_start, interval_end, reference_chromosome, reference_offset)
#     """
#     chrom_start_time = datetime.datetime.now()
#     query_chrom, interval_chain = params
#
#     print '\tProcessing intervals for {}'.format(query_chrom)
#     print '\t\tSplitting {} intervals  for chromosome {} at intersections...'.format(len(interval_chain), query_chrom)
#     start_time = datetime.datetime.now()
#     interval_chain.split_overlaps()
#     print '\t\tDone in {}'.format(datetime.datetime.now() - start_time)
#
#     print '\t\tFiltering {} intervals for chromosome {} to keep only best alignment for each segment...'.format(
#         len(interval_chain), query_chrom)
#
#     start_time = datetime.datetime.now()
#     filtered_intervals = []
#     interval_chain = sorted(interval_chain)
#
#     cur_pos = -1
#     best_interval = interval_chain[0]
#
#     for i in xrange(1, len(interval_chain)):
#         interval = interval_chain[i]
#         if interval.begin == cur_pos and interval.data['score'] > best_interval.data['score']:
#             best_interval = interval
#         else:
#             filtered_intervals.append((best_interval.begin, best_interval.end, best_interval.data['ref_chrom'], best_interval.data['ref_offset']))
#             best_interval = interval
#             cur_pos = interval.begin
#
#     print '\t\tDone in {}'.format(datetime.datetime.now() - start_time)
#     print '\tAll done with chromosome {} in {}'.format(query_chrom, datetime.datetime.now() - chrom_start_time)
#     return query_chrom, filtered_intervals


def chains_to_buckets(chain_fname, source_build, source_chrom_lengths, dest_build, dest_chrom_lengths,
                      source_chromosome_dialect='ucsc', dest_chromosome_dialect='ucsc', score_threshold=0,
                      query_size_threshold=0, ref_size_threshold=0, query_chromosomes_to_use=set([]), reference_chromosomes_to_use=set([])):
    """Processes the chains in <chain_fname> into a nested dictionary of pairs of chromosome-wide vectors, 'ref_chrom',
      which contains an index to the chromosome of the best-match orthologous position in the query, and
      'ref_offset', which contains the difference between the reference and query coordinates.

      Each position contains a mapping given by the best-scoring chain that addresses that position.

      Returns a tuple consisting of a dictionary, keyed by chromosome, of dictionaries with 'ref_chrom' and 'ref_offset'
      vectors, and an indexer object which can be used to regenerate the full chromosome names from the index number.
    """
    chromosome_buckets = {}
    for chrom in source_chrom_lengths:
        # cutting the data types a little close here to be ultra-stingy, but should work for present application. Not
        # guaranteed to work with all genomes though.
        chromosome_buckets[chrom] = {'ref_offset':numpy.zeros(source_chrom_lengths[chrom], dtype=numpy.int32),
                                     'ref_chrom': numpy.full(source_chrom_lengths[chrom], fill_value=EMPTY_REF_CHROM_VALUE,
                                                             dtype=numpy.uint16),
                                     'score':numpy.zeros(source_chrom_lengths[chrom],
                                                         dtype=numpy.uint32)}  # assuming only non-negative integer scores

    chrom_indexer = toolbox.Serializer()  # index chromosome names to avoid storing strings

    header_fields = (
        'dummy', 'score', 'tName', 'tSize', 'tStrand', 'tStart', 'tEnd', 'qName', 'qSize', 'qStrand', 'qStart', 'qEnd',
        'id')
    missing_chroms_ref = set([])
    missing_chroms_query = set([])

    with open(chain_fname, 'rU') as chain_file:
        print('Building chromosome-wide mapping vectors from chain file...')
        if len(query_chromosomes_to_use):
            print(('Only processing chains mapping to chromosome {} in source'.format(
                ', '.join(list(query_chromosomes_to_use)))))
        if len(reference_chromosomes_to_use):
            print(('Only processing chains mapping to chromosome {} in destination'.format(
                ', '.join(list(reference_chromosomes_to_use)))))
        start_time = datetime.datetime.now()
        # self._initialize(pileup_dtype=destination_dtype)

        new_chain = True
        good_chain = False

        total_unfiltered_coverage = 0
        total_coverage = 0
        # duplicate_coverage = 0

        for line_num, line in enumerate(chain_file):
            # if line_num > 100000:
            #                 break
            if line_num % REPORTING_INTERVAL == 0:
                print(('\tProcessing line {}'.format(line_num)))
            if new_chain and line != '\n':  # insurance against multiple blank lines
                header = toolbox.parse_line_dict(line, header_fields, split_char=' ', strict=True)
                assert header['dummy'] == 'chain'
                new_chain = False

                # relative offsets within the chain
                ref_chain_pos = 0
                query_chain_pos = 0

                ref_chrom = toolbox.convert_chroms(header['tName'], dest=dest_chromosome_dialect)
                query_chrom = toolbox.convert_chroms(header['qName'], dest=source_chromosome_dialect)

                ref_strand = {'+':1, '-':-1}[header['tStrand']]
                query_strand = {'+': 1, '-': -1}[header['qStrand']]

                good_chain = False
                chain_score = int(header['score'])

                if query_chrom in source_chrom_lengths:
                    if (not len(query_chromosomes_to_use) or query_chrom in query_chromosomes_to_use):
                        if int(header['qSize']) != source_chrom_lengths[query_chrom]:
                            raise Exception(
                                'Error on line {}, chain {}. Chain file size of {} for query chromosome {} does not match source size of {}'.format(
                                    line_num, header['id'], header['qSize'], query_chrom,
                                    source_chrom_lengths[query_chrom]))

                    if ref_chrom in dest_chrom_lengths:
                        if (not len(reference_chromosomes_to_use) or ref_chrom in reference_chromosomes_to_use):
                            if int(header['tSize']) != dest_chrom_lengths[ref_chrom]:
                                raise Exception(
                                    'Error on line {}, chain {}. Chain file size of {} for reference chromosome {} does not match destination size of {}'.format(
                                        line_num, header['id'], header['tSize'], ref_chrom,
                                        dest_chrom_lengths[ref_chrom]))

                            if (not score_threshold or chain_score >= score_threshold) and (
                                        not query_size_threshold or header['qSize'] >= query_size_threshold) and (
                                        not ref_size_threshold or header['tSize'] >= ref_size_threshold):
                                good_chain = True
                    else:
                        missing_chroms_ref.add(ref_chrom)
                else:
                    missing_chroms_query.add(query_chrom)

                if ref_strand == 1:
                    ref_chain_start = int(header['tStart'])
                else:
                    ref_chain_start = int(
                        header['tEnd'])  # start from the end of the block and work backwards for reverse strand

                if query_strand == 1:
                    query_chain_start = int(header['qStart'])
                else:
                    query_chain_start = int(
                        header['qEnd'])  # start from the end of the block and work backwards for reverse strand

            elif line == '\n':
                # start a new chain on the next line
                new_chain = True

            elif good_chain:
                # it must be a data line
                split_line = line.split('\t')
                size = int(split_line[0])

                if len(split_line) == 3: # standard data line
                    ref_diff = int(split_line[1])
                    query_diff = int(split_line[2])

                elif len(split_line) == 1: # last data line in chain
                    ref_diff = 0
                    query_diff = 0

                else:
                    raise Exception(
                        'Encountered a chain alignment data line of length 2 on line {}. Unsure how to handle this.'.format(
                            line_num))

                ref_start_pos = ref_chain_start + ref_chain_pos
                ref_end_pos = ref_start_pos + size * ref_strand
                # slicing backwards requires subtracting 1 from both indices to get the same positions as a forward slice
                if ref_strand == -1:
                    ref_start_pos -= 1
                    ref_end_pos -= 1
                ref_chain_pos += (size + ref_diff) * ref_strand

                query_start_pos = query_chain_start + query_chain_pos
                query_end_pos = query_start_pos + size * query_strand
                if query_strand == -1:
                    query_start_pos -= 1
                    query_end_pos -= 1

                query_chain_pos += (size + query_diff) * query_strand

                ref_offset = ref_start_pos - query_start_pos
                # query_offset = query_start_pos - ref_start_pos

                ref_chrom_index = chrom_indexer.get_index(ref_chrom)

                try:
                    if query_end_pos == -1:
                        query_end_pos = None  # make sure we include the 0th element in the reverse slice

                    loci_to_assign = numpy.nonzero(
                        numpy.greater(numpy.full(size, fill_value=chain_score),
                                      chromosome_buckets[query_chrom]['score'][
                                      query_start_pos:(query_end_pos, None)[query_end_pos == -1]:query_strand]))[0]
                    if len(loci_to_assign):
                        if ref_strand == query_strand:
                            chromosome_buckets[query_chrom]['ref_offset'][query_start_pos:query_end_pos][
                                loci_to_assign] = ref_offset
                        else:
                            chromosome_buckets[query_chrom]['ref_offset'][query_start_pos:query_end_pos:query_strand][
                                loci_to_assign] = numpy.arange(ref_offset, ref_offset + size * 2 + 1, step=2)[
                                loci_to_assign]
                        chromosome_buckets[query_chrom]['score'][query_start_pos:query_end_pos:query_strand][
                            loci_to_assign] = chain_score
                        chromosome_buckets[query_chrom]['ref_chrom'][query_start_pos:query_end_pos:query_strand][
                            loci_to_assign] = ref_chrom_index
                except ValueError as ve:
                    print()
                    print(('*' * 80))
                    print(('Problem on line {}, {}'.format(line_num, line)))
                    print(('Query interval: {}, {}, {}'.format(query_chrom, query_start_pos, query_end_pos)))
                    print(('Ref interval: {}, {}, {}'.format(ref_chrom, ref_start_pos, ref_end_pos)))
                    print(('Interval size: {}'.format(size)))
                    print(('Query chromosome size: {}, reference chromosome size: {}'.format(
                        source_chrom_lengths[query_chrom], dest_chrom_lengths[ref_chrom])))
                    print(('*' * 80))
                    raise ve
                else:
                    total_unfiltered_coverage += numpy.abs(query_end_pos - query_start_pos)
                    total_coverage += len(loci_to_assign)

        print(('Done loading in {}'.format(datetime.datetime.now() - start_time)))
        if missing_chroms_ref:
            print(('The following chromosomes in the chain file were missing in the reference build: {}'.format(
                ','.join(sorted(list(missing_chroms_ref))))))

        if missing_chroms_query:
            print(('The following chromosomes in the chain file were missing in the reference build: {}'.format(
                ','.join(sorted(list(missing_chroms_query))))))

    # we can throw away the scores now to save RAM:
    for query_chrom in chromosome_buckets:
        del chromosome_buckets[query_chrom]['score']

    query_genome_size = sum(source_chrom_lengths.values())
    ref_genome_size = sum(dest_chrom_lengths.values())

    print(('{} base pairs in all chains, {:>3} of query total, {:>3} of reference total'.format(
        total_unfiltered_coverage, total_unfiltered_coverage / float(query_genome_size),
        total_unfiltered_coverage / float(ref_genome_size))))
    print(('{} base pairs in filtered chains, {:>3} of query total, {:>3} of reference total'.format(total_coverage,
                                                                                                    total_coverage / float(
                                                                                                        query_genome_size),
                                                                                                    total_coverage / float(
                                                                                                        ref_genome_size))))

    return chromosome_buckets, chrom_indexer


def buckets_to_intervals_chromslave(params):
    """
    (interval_start, interval_end, reference_chromosome, reference_offset)
    :param chromosome_buckets:
    :param chrom_indexer:
    :return:
    """
    start_time = datetime.datetime.now()
    query_chrom, chromosome_buckets, chrom_indexer = params

    print(('\tProcessing query chromosome  {}'.format(query_chrom)))
    interval_counter = 0

    filtered_intervals = []
    last_chrom = chromosome_buckets['ref_chrom'][0]
    last_offset = chromosome_buckets['ref_offset'][0]
    interval_start = 0

    if 1 < len(chromosome_buckets['ref_offset']) and chromosome_buckets['ref_offset'][1] == \
                    chromosome_buckets['ref_offset'][0] - 2 and chromosome_buckets['ref_chrom'][1] == \
            chromosome_buckets['ref_chrom'][0]:
        interval_polarity = -1
    else:
        interval_polarity = 1
    active_interval = chromosome_buckets['ref_chrom'][0] != 65535

    for query_pos in range(1, len(chromosome_buckets['ref_offset'])):
        # print
        # print 'Position: {}, ref_chrom: {}, ref_offset: {}, current_offset: {}'.format(pos, chromosome_buckets['ref_chrom'][pos], chromosome_buckets['ref_offset'][pos], cur_offset)

        last_strand = interval_polarity
        last_active = active_interval

        active_interval = (chromosome_buckets['ref_chrom'][query_pos] != 65535)

        if chromosome_buckets['ref_offset'][query_pos] == last_offset:
            interval_polarity = 1
        elif chromosome_buckets['ref_offset'][query_pos] == last_offset - 2:
            interval_polarity = -1
        else:
            interval_polarity = 0

        if last_active and (chromosome_buckets['ref_chrom'][
                                query_pos] != last_chrom or interval_polarity != last_strand or not active_interval):
            # we've finished an interval
            if last_strand == 1:
                filtered_intervals.append(
                    (interval_start, query_pos, chrom_indexer.index_to_name[last_chrom], last_offset, last_strand))
            else:
                filtered_intervals.append(
                    (interval_start, query_pos, chrom_indexer.index_to_name[last_chrom],
                     last_offset + (query_pos - interval_start - 1),
                     last_strand))
            interval_counter += 1
            last_active = False

        if active_interval and not last_active:
            # we're starting a new interval

            interval_start = query_pos

            if query_pos + 1 < len(chromosome_buckets['ref_offset']) and chromosome_buckets['ref_offset'][
                        query_pos + 1] == chromosome_buckets['ref_offset'][query_pos] - 2 and \
                            chromosome_buckets['ref_chrom'][query_pos] == chromosome_buckets['ref_chrom'][
                                query_pos + 1]:
                interval_polarity = -1
            else:
                interval_polarity = 1
            last_chrom = chromosome_buckets['ref_chrom'][query_pos]

        last_offset = chromosome_buckets['ref_offset'][query_pos]

    # pos += 1
    if active_interval:
        filtered_intervals.append(
            (interval_start, query_pos+1, chrom_indexer.index_to_name[last_chrom], last_offset, last_strand))
        interval_counter += 1
    # print 'Finished interval: {}'.format(filtered_intervals[-1])
    print(('\tGenerated {} intervals for query chromosome {} in {}'.format(interval_counter, query_chrom,
                                                                          datetime.datetime.now() - start_time)))

    return query_chrom, filtered_intervals


# def buckets_to_intervals(chromosome_buckets, chrom_indexer):
#     """
# (interval_start, interval_end, reference_chromosome, reference_offset)
#     :param chromosome_buckets:
#     :param chrom_indexer:
#     :return:
#     """
#
#     overall_start_time = datetime.datetime.now()
#     print 'Converting genome-wide mapping vectors to compact intervals...'
#     filtered_intervals = {}
#
#     for chrom_idx, query_chrom in enumerate(chromosome_buckets.keys()):
#         chrom_start_time = datetime.datetime.now()
#         print '\tProcessing query chromosome {} of {}: {}'.format(chrom_idx+1, len(chromosome_buckets), query_chrom)
#         filtered_intervals[query_chrom] = []
#         cur_chrom = chromosome_buckets[query_chrom]['ref_chrom'][0]
#         cur_offset = chromosome_buckets[query_chrom]['ref_offset'][0] + 1
#         interval_start = 0
#
#         active_interval = chromosome_buckets[query_chrom]['ref_chrom'][0] != 65535
#
#         interval_counter = 0
#
#         for pos in xrange(1, len(chromosome_buckets[query_chrom]['ref_offset'])):
#             # print
#             # print 'Position: {}, ref_chrom: {}, ref_offset: {}, current_offset: {}'.format(pos, chromosome_buckets[query_chrom]['ref_chrom'][pos], chromosome_buckets[query_chrom]['ref_offset'][pos], cur_offset)
#
#             if chromosome_buckets[query_chrom]['ref_offset'][pos] != cur_offset or chromosome_buckets[query_chrom]['ref_chrom'][pos]  != cur_chrom:
#                 # we've started a new interval
#                 if active_interval:
#                     filtered_intervals[query_chrom].append((
#                     interval_start, pos, chrom_indexer.index_to_name[cur_chrom], cur_offset - (pos - interval_start) ))
#                     interval_counter += 1
#                     # print 'Finished interval: {}'.format(filtered_intervals[-1])
#                 if chromosome_buckets[query_chrom]['ref_chrom'][pos] != 65535:
#                     interval_start = pos
#                     active_interval = True
#                     cur_chrom = chromosome_buckets[query_chrom]['ref_chrom'][pos]
#                     cur_offset = chromosome_buckets[query_chrom]['ref_offset'][pos] + 1
#                 else:
#                     active_interval = False
#             else:
#                 cur_offset += 1
#         pos += 1
#         if active_interval:
#             filtered_intervals[query_chrom].append(
#                 (interval_start, pos, chrom_indexer.index_to_name[cur_chrom], cur_offset - (pos - interval_start) ))
#             interval_counter += 1
#         print '\tGenerated {} intervals for query chromosome {} in {}'.format(interval_counter, query_chrom,
#                                                                               datetime.datetime.now() - chrom_start_time)
#         # print 'Finished interval: {}'.format(filtered_intervals[query_chrom][-1])
#     print 'Done generating intervals in {}'.format(datetime.datetime.now() - overall_start_time)
#     return filtered_intervals


