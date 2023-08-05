import itertools
import collections
import datetime
import numpy
import pandas
import multiprocessing

REPORTING_INTERVAL = 10000

CHROM_LENGTHS = '/home/dskola/model_data/reference_genomes/mm10/mm10.chrom.sizes'

# ToDo: Remove dummy region "names" introduced for backwards-compatibility with the overlaps code

def log_print(message, tabs=1):
    print('{}{}{}'.format(pretty_now(), '\t'*tabs, message))

    
def pretty_now():
    """
    Returns the current date/time in a nicely formatted string (without so many decimal places)
    """
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%b-%d %H:%M:%S')    


def subdivide(dividand, num_bins):
    """
    Approximates an even partition of :param:`dividand` into :param:`num_bins` 
    using integers.
    """
    q, r = divmod(dividand, num_bins)
    results = numpy.full(num_bins, fill_value=int(q), dtype=int)
    results[:int(r)] += 1
    
    return results
    
    
def deepcopy_dict(array_dict):
    return {k:v.copy() for k, v in array_dict.items()}
   
    
def _empirical_p_val_vectorized_left(data, values, standard_approximation=True):
    """  
    """
    i = 0
    p_vals = numpy.zeros(len(values))
    for value_idx, value in enumerate(values):
        if data[i] <= value:
#             p_vals.append()
            while i < len(data) and data[i] <= value:
#                 print(value <= data[i], i < len(data))
#                 print(value, i, data[i])
                i += 1
            i -= 1
            p_vals[value_idx] = ((i + 1 + (0,1)[bool(standard_approximation)]) / (len(data)+ (0,1)[bool(standard_approximation)]))
        else:
            p_vals[value_idx] = (0,1)[bool(standard_approximation)] / (len(data)+ (0,1)[bool(standard_approximation)])
        
    return p_vals


def _empirical_p_val_vectorized_right(data, values, standard_approximation=True):
    """  
    """
    values = values[::-1]
    data = data[::-1]
    #print(values, data)
    i = 0
    p_vals = numpy.zeros(len(values))
    for value_idx, value in enumerate(values):
        #print(value, i, data[i])
        if data[i] >= value:
            while i < len(data) and data[i] >= value:
#                 print(value <= data[i], i < len(data))                
                i += 1
#                 print(value, i, data[i])
            i -= 1
            p_vals[value_idx] = ((i + 1 + (0,1)[bool(standard_approximation)]) / (len(data)+ (0,1)[bool(standard_approximation)]))
        else:
            p_vals[value_idx] = (0,1)[bool(standard_approximation)] / (len(data)+ (0,1)[bool(standard_approximation)])
        #print(p_vals[value_idx])
    return p_vals[::-1]


def empirical_p_val(data, values, tail='both', standard_approximation=True, is_sorted=False):
    """
    Given an unsorted vector of observed data :param:`data`, returns the standard approximation 
    (adds pseudocount of 1 to prevent 0 p-values) to the empirical p-value for :param:`value`
    using either a one-sided or two-sided significance test.
    
    :param:`tail` must be 'left', 'right' (for a one-sided test) or 'both' (for a two-sided test)
    """
    if tail not in ('left', 'right', 'both'):
        raise ValueError('Invalid value for parameter :tail:, {}'.format(tail))    
    
    try:
        len(values)
    except TypeError:
        is_vector=False
        value=values
    else:
        is_vector=True
        
    if is_vector and not is_sorted:
        data = sorted(data)
        value_sort_idx = numpy.argsort(values)
        restore_values_sort_idx = numpy.argsort(values)
        values=values[value_sort_idx]
        del(value_sort_idx)

    if tail in ('left', 'both'):
        if is_vector:
            left_p_val = _empirical_p_val_vectorized_left(data, values, standard_approximation=standard_approximation)
        else:
            left_p_val = (numpy.sum(numpy.less_equal(data,value)) + 1) / (len(data) + 1)
        
    if tail in ('right', 'both'):
        if is_vector:
            right_p_val = _empirical_p_val_vectorized_right(data, values, standard_approximation=standard_approximation)
        else:
            right_p_val = (numpy.sum(numpy.greater_equal(data,value)) + 1) / (len(data) + 1)
        
    if tail == 'left':
        p_vals = left_p_val
    elif tail == 'right':
        p_vals = right_p_val
    else:
        p_vals = numpy.minimum(numpy.minimum(left_p_val, right_p_val) * 2,1)
        
    if is_vector and not is_sorted:    
        p_vals = p_vals[restore_values_sort_idx]
    
    return p_vals

    
def compute_interval_overlaps(A, B, min_overlap=0, is_sorted=False):
    """
    Given two lists, A and B, of interval tuples in the form (name, start, end)
    return a list of tuples of the form:

    (A_name, B_name, overlap_start, overlap_end)

    for every pair of intervals that overlaps by at least <min_overlap>
    """
    overlaps = []

    if not is_sorted:
        A = sorted(A, key=lambda x: x[1])
        B = sorted(B, key=lambda x: x[1])

    A_ptr = 0
    B_ptr = 0

    # Two conditions must hold to have an overlap:
    # B start <= A end
    # A start <= B end

    # initialize the loop by checking for overlaps at the start (all B intervals that overlap with the first interval in A)
    if B[B_ptr][1] <= A[A_ptr][2]:
        while B[B_ptr][1] <= A[A_ptr][2]:
            overlap_start = max(A[A_ptr][1], B[B_ptr][1])
            overlap_end = min(A[A_ptr][2], B[B_ptr][2])
            if overlap_end - overlap_start >= min_overlap:
                overlaps.append((A[A_ptr][0], B[B_ptr][0], overlap_start, overlap_end))
            if B_ptr < len(B) - 1:
                B_ptr += 1
            else:
                break
        B_ptr -= 1
#     print('initialized: {}, {}, {}, {} '.format(A_ptr, B_ptr, A[A_ptr], B[B_ptr]))
    # advance the A pointer until B start is upstream of A end
    while True:
#         print('\tnew run: {}, {}, {}, {} '.format(A_ptr, B_ptr, A[A_ptr], B[B_ptr]))
        if A_ptr < len(A) - 1:
            A_ptr += 1
#             print('\tadvanced A: {}, {}, {}, {} '.format(A_ptr, B_ptr, A[A_ptr], B[B_ptr]))
        else:
            break
        # advance the B pointer until A start is upstream of B end
        while A[A_ptr][1] > B[B_ptr][2]:
            if B_ptr < len(B) - 1:
                B_ptr += 1
#                 print('\tadvanced B: {}, {}, {}, {} '.format(A_ptr, B_ptr, A[A_ptr], B[B_ptr]))
            else:
                break
#         print('aligned: {}, {}, {}, {} '.format(A_ptr, B_ptr, A[A_ptr], B[B_ptr]))
        # capture the overlaps in B until B start is no longer upstream of A end
        if B[B_ptr][1] <= A[A_ptr][2]:
            while B[B_ptr][1] <= A[A_ptr][2]:
                overlap_start = max(A[A_ptr][1], B[B_ptr][1])
                overlap_end = min(A[A_ptr][2], B[B_ptr][2])
#                 print('grabbing: {}, {}, {}, {} '.format(A_ptr, B_ptr, A[A_ptr], B[B_ptr]))
                if overlap_end - overlap_start >= min_overlap:
                    overlaps.append((A[A_ptr][0], B[B_ptr][0],
                    overlap_start, overlap_end))
                if B_ptr < len(B) - 1:
                    B_ptr += 1
#                     print('\tadvanced B: {}, {}, {}, {} '.format(A_ptr, B_ptr, A[A_ptr], B[B_ptr]))
                else:
                    break
#             A_ptr += 1
            B_ptr -= 1
    return overlaps    
    

def convert_intervals_to_size_arrays(intervals, total_size):
    names, starts, ends = zip(*sorted(intervals, key=lambda x: x[1]))
    names = numpy.array(names)
    starts = numpy.array(starts, dtype=int)
    ends = numpy.array(ends, dtype=int)
    
    interval_sizes = ends - starts + 1
    gap_sizes = numpy.concatenate((starts, [total_size-1])) - numpy.concatenate(([0], ends))
    
    return names, interval_sizes, gap_sizes

    
def convert_size_arrays_to_intervals(names, interval_sizes, gap_sizes, total_size):
    g_s = numpy.cumsum(gap_sizes)
    i_s = numpy.cumsum(interval_sizes)
    
    starts = g_s[:-1] + numpy.concatenate(([0], i_s[:-1]))
    ends = g_s[:-1] + i_s
    
    return zip(names, starts, ends)
    

def count_overlaps(overlap_tuples):
    """
    Given a list of overlap tuples as output by `compute_interval_overlaps()`,
    returns a tuple of the counts of the number of a intervals with overlaps 
    and b intervals with overlaps.
    """
    a_set = set([])
    b_set = set([])
    
    for tup in overlap_tuples:
        a_set.add(tup[0])
        b_set.add(tup[1])
    
    return len(a_set), len(b_set)    

    
def generate_random_gaps_additive(total_gap_size, num_gaps):
    interval_locations = set([])
    while len(interval_locations) < num_gaps:
#         print('round')
        intervals_needed = num_gaps - len(interval_locations)
        interval_locations.update(numpy.random.randint(0, total_gap_size, size=intervals_needed))
        
    interval_locations = numpy.concatenate(([0], numpy.sort(list(interval_locations))))
    gap_sizes = numpy.diff(interval_locations)
    
    return gap_sizes

    
def generate_random_gaps_subtractive(total_gap_size, num_gaps):
    interval_locations = numpy.arange(total_gap_size)
    numpy.random.shuffle(interval_locations)
    interval_locations = numpy.concatenate(([0], numpy.sort(interval_locations[:num_gaps])))

    gap_sizes = numpy.diff(interval_locations)
    
    return gap_sizes

    
def generate_random_gaps(total_gap_size, num_gaps):
    if num_gaps / total_gap_size < 0.1:
        return generate_random_gaps_additive(total_gap_size, num_gaps)
    else:
        return generate_random_gaps_subtractive(total_gap_size, num_gaps)

        
def shuffle_regions(region_tuples, chrom_lengths, preserve_gap_sizes=False):
    # generate a dictionary of intervals per chromosome for the shuffled_regions
    to_shuffle_regions_by_chrom = collections.defaultdict(lambda: [])
    for name, chrom, start, end in region_tuples:
        to_shuffle_regions_by_chrom[chrom].append((name, start, end))
    for chrom in to_shuffle_regions_by_chrom:
        to_shuffle_regions_by_chrom[chrom].sort(key=lambda x: x[1])
    
    # convert the to_shuffle intervals into arrays of interval and gap sizes that we can easily shuffle
    size_arrays_by_chrom = {chrom:list(convert_intervals_to_size_arrays(regions, total_size=chrom_lengths[chrom])) for chrom, regions in to_shuffle_regions_by_chrom.items()}
    
    # shuffle the regions
    shuffled_regions_by_chrom = collections.defaultdict(lambda: [])
    for chrom in size_arrays_by_chrom:
        numpy.random.shuffle(size_arrays_by_chrom[chrom][1])
      
        if preserve_gap_sizes:
            numpy.random.shuffle(size_arrays_by_chrom[chrom][2])
        else:
            total_gap_nucleotides = chrom_lengths[chrom] - size_arrays_by_chrom[chrom][1].sum()
            size_arrays_by_chrom[chrom][2] = generate_random_gaps(total_gap_size=total_gap_nucleotides,
                                                                  num_gaps=len(size_arrays_by_chrom[chrom][2]+1))
        shuffled_regions_by_chrom[chrom] = list(convert_size_arrays_to_intervals(size_arrays_by_chrom[chrom][0], size_arrays_by_chrom[chrom][1], size_arrays_by_chrom[chrom][2], chrom_lengths[chrom]))
    
    return shuffled_regions_by_chrom        

    
def overlap_worker(params):
    numpy.random.seed()
    num_permutations, static_regions_by_chrom, size_arrays_by_chrom, chrom_lengths, preserve_gap_sizes = params
    static_overlaps = numpy.empty(num_permutations, dtype=int)
    shuffled_overlaps = numpy.empty(num_permutations, dtype=int)
    
    log_print('Starting chunk of {} permutations ...'.format(num_permutations), 2)
    
    for permutation_idx in range(num_permutations):
        this_static_overlap = 0
        this_shuffled_overlap = 0
        for chrom in size_arrays_by_chrom:
            if chrom in static_regions_by_chrom:
                # shuffle the regions
                numpy.random.shuffle(size_arrays_by_chrom[chrom][1])

                if preserve_gap_sizes:
                    numpy.random.shuffle(size_arrays_by_chrom[chrom][2])
                else:
                    total_gap_nucleotides = chrom_lengths[chrom] - size_arrays_by_chrom[chrom][1].sum()
                    size_arrays_by_chrom[chrom][2] = generate_random_gaps(total_gap_size=total_gap_nucleotides,
                                                                  num_gaps=len(size_arrays_by_chrom[chrom][2]))

                shuffled_regions = convert_size_arrays_to_intervals(size_arrays_by_chrom[chrom][0], size_arrays_by_chrom[chrom][1], size_arrays_by_chrom[chrom][2], chrom_lengths[chrom])

                # test overlap
                this_overlap = compute_interval_overlaps(static_regions_by_chrom[chrom],
                                                             list(shuffled_regions), is_sorted=True)
                o1, o2 = count_overlaps(this_overlap)
                this_static_overlap += o1
                this_shuffled_overlap += o2
        
        static_overlaps[permutation_idx] = this_static_overlap
        shuffled_overlaps[permutation_idx] = this_shuffled_overlap
        
    log_print('Done.', 2)
        
    return static_overlaps, shuffled_overlaps


def convert_interval_tuples_to_chrom_dict(interval_tuples):
    regions_by_chrom = {}
    for name, chrom, start, end in interval_tuples:
        if chrom not in regions_by_chrom:
            regions_by_chrom[chrom] = []
        regions_by_chrom[chrom].append((name, start,end))
        
    for chrom in regions_by_chrom:
        regions_by_chrom[chrom].sort(key=lambda x: x[1])

    return regions_by_chrom
    
    
def compute_empirical_p_overlaps(static_regions, to_shuffle_regions, num_permutations=999999,   
                                  preserve_gap_sizes=False,
                                  num_cores=28, tail='right',
                                  chrom_length_filename=CHROM_LENGTHS):
    """
    Given two sets of genomic regions (given as lists of half-closed intervals as 
    tuples in the form: (name, chrom, start, end)) returns a dictionary with the following entries:
	
	'true_overlapping_static': number of regions in :param:`static_regions` that overlapped regions in :param:`to_shuffle_regions`
    'static_pval':  p-value of true overlapping static regions from shuffled permutation test 
    'permuted_static_overlaps': number of overlapping static regions for all shuffled permutations
    'true_overlapping_shuffled': number of regions in :param:`to_shuffle_regions` that overlapped regions in :param:`static_regions`
    'shuffled_pval': p-value of true overlapping to_shuffle regions from shuffled permutation test 
    'permuted_shuffled_overlaps': number of overlapping to_shuffle regions for all shuffled permutations
    
    """   
    log_print('Analyzing overlap between {} static regions and {} shuffled regions ...'.format(len(static_regions), len(to_shuffle_regions)), 1)
    
    chrom_lengths = pandas.read_csv(chrom_length_filename, index_col=0, sep='\t', header=None).iloc[:,0].to_dict()
    log_print('Loaded chromosome lengths from {}'.format(chrom_length_filename), 1)

    # generate dictionaries of intervals per chromosome
    static_regions_by_chrom = convert_interval_tuples_to_chrom_dict(static_regions)
    to_shuffle_regions_by_chrom = convert_interval_tuples_to_chrom_dict(to_shuffle_regions)
                
    # compute the true overlap
    overlapping_static = 0
    overlapping_shuffled = 0
    for chrom in to_shuffle_regions_by_chrom:
        if chrom in static_regions_by_chrom:
            this_overlaps = compute_interval_overlaps(static_regions_by_chrom[chrom], 
                                                                   to_shuffle_regions_by_chrom[chrom])
            
            o1, o2 = count_overlaps(this_overlaps)
            overlapping_static += o1
            overlapping_shuffled += o2
    
    # convert the to_shuffle intervals into arrays of interval and gap sizes that we can easily shuffle.
    size_arrays_by_chrom = {chrom:list(convert_intervals_to_size_arrays(regions, total_size=chrom_lengths[chrom])) for chrom, regions in to_shuffle_regions_by_chrom.items()} # we convert the size array tuple to a list because we will need to replace elements later

    # perform permutation testing
    shuffled_overlaps = numpy.empty(num_permutations, dtype=int)
        
    permutations_per_worker = subdivide(num_permutations, num_cores)
    
    param_vector = zip(permutations_per_worker,
                        itertools.repeat(static_regions_by_chrom), 
                        itertools.repeat({k:[v[0].copy(), v[1].copy(), v[2].copy()] for k,v in size_arrays_by_chrom.items()}),
                        itertools.repeat(chrom_lengths),
                        itertools.repeat(preserve_gap_sizes))
    
    p = multiprocessing.Pool(num_cores)
    results = p.map(overlap_worker, param_vector)
    
    permuted_static_overlaps = numpy.concatenate([result[0] for result in results])
    permuted_shuffled_overlaps = numpy.concatenate([result[1] for result in results])

    static_pval = empirical_p_val(permuted_static_overlaps, numpy.array([overlapping_static]), tail=tail)[0]
    shuffled_pval = empirical_p_val(permuted_shuffled_overlaps, numpy.array([overlapping_shuffled]), tail=tail)[0]

    return {'true_overlapping_static':overlapping_static,
            'static_pval':static_pval, 
            'permuted_static_overlaps':permuted_static_overlaps, 
            'true_overlapping_shuffled':overlapping_shuffled,
            'shuffled_pval':shuffled_pval, 
            'permuted_shuffled_overlaps':permuted_shuffled_overlaps}