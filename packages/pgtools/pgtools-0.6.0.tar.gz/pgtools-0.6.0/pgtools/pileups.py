import sys
#sys.path.append('/home/dskola/workspace/expression_modeling/')
import matplotlib
#matplotlib.use('Agg')
import collections
import contextlib
import csv
import datetime
import math
import multiprocessing
import os
import re
import shutil
import subprocess
import gzip
import numpy
import scipy.ndimage
import scipy.signal

from model import pp_mappability
# import pp_mappability
from pgtools import toolbox
from model import motifs
from pgtools import myplots
from model import antfarm
from model import filterchains

THREADS = 31
MULTI_PROCESSING_METHOD = 'hybrid'

# print 'Using up to {} cores where possible'.format(THREADS)

try:
    import mkl
except ImportError:
    pass
else:
    # print('MKL library found.')
    mkl.set_num_threads(THREADS)

REPORTING_INTERVAL = 1000000
DEFAULT_CHROMOSOME_DIALECT = 'ucsc'
PILEUP_DTYPE = numpy.float16  # set to half-precision to conserve RAM
VERBOSE = True



NETWORK_TMP_DIR = toolbox.home_path('model_data/tmp')
# LOCAL_TMP_DIR = '/tmp/dskola'
# LOCAL_TMP_DIR = '/dev/shm'  
LOCAL_TMP_DIR = NETWORK_TMP_DIR
CHAINFILE_BASEPATH = toolbox.home_path('model_data/chain_files')
INTERVAL_BASEPATH = toolbox.home_path('model_data/best_intervals')
PILEUP_DATA_FOLDER = toolbox.home_path('model_data/saved_pileups')
# LOCAL_TMP_DIR = NETWORK_TMP_DIR

FRAGMENT_SIZES_FILENAME = toolbox.home_path('model_data/fragment_sizes.tsv')
INTERVAL_FILE_TEMPLATE = '{}To{}.best.txt'
MAX_FILEHANDLES_PER_PILEUP = 100
# MAX_MESSAGE_SIZE = 268000000  # maximum number of vector elements that can be passed in a parameter tuple by multiprocessing.Pool
MAX_MESSAGE_SIZE = 10000000

WHITESPACE = re.compile(r'\s*')


def dbg_print(text, indent_level=0):
    """
    Selective printer for status messages with optional indenting.

    Will print message if global VERBOSE flag is true, and indents a number of tabs equal to <indent level>

    :param text:
    :param indent_level:
    :return:
    """
    if VERBOSE:
        for line in text.split('\n'):
            print(('\t' * indent_level + line))


def get_fragment_size_from_file(replicate_name):
    # print('Checking for pre-computed fragment size for replicate {} ...'.format(replicate_name))

    fragment_length = None
    try:
        with open(FRAGMENT_SIZES_FILENAME, 'rt') as fragment_size_file:
            ss_reader = csv.reader(fragment_size_file, dialect=csv.excel_tab)
            for line in ss_reader:
                # print(line)
                if line[0] == replicate_name:
                    fragment_length = int(line[1])
                    # print('Found pre-computed fragment size of {}'.format(fragment_length))
    except IOError as ie:
        print('No fragment size file found.')
    else:
        if fragment_length is None:
            print('No pre-computed fragment size found .')

    return fragment_length

def get_fragment_size_from_homer(homer_tag_directory):
    homer_info = homer_parse_taginfo(os.path.join(homer_tag_directory, 'tagInfo.txt'))
    fragment_length = homer_info['fragmentLengthEstimate']
    return fragment_length

def save_fragment_length(replicate_name, fragment_length):
    print('Saving fragment size to {}'.format(FRAGMENT_SIZES_FILENAME))
    with open(FRAGMENT_SIZES_FILENAME, 'a') as fragment_size_file:
        ss_writer = csv.writer(fragment_size_file, dialect=csv.excel_tab)
        ss_writer.writerow([replicate_name, str(fragment_length)])

def get_chrom_length_dict(genome_table_fname, dest_chromosome_dialect=DEFAULT_CHROMOSOME_DIALECT):
    print('Getting chromosome lengths from {} and translating names to dialect {}'.format(genome_table_fname, dest_chromosome_dialect))
    with open(genome_table_fname, 'rt') as gt_file:
        length_dict = {}
        for line in gt_file:
            # print line
            split_line = re.split(r'\s', line.strip())
            if len(split_line) > 1:
                # print split_line[0], toolbox.parse_chromosome_ID(split_line[0])
                length_dict[toolbox.convert_chroms(split_line[0], dest=dest_chromosome_dialect)] = int(split_line[1])
                # length_dict[split_line[0].strip()] = int(split_line[1])
    return length_dict


def load_stranded(chrom_lengths, data_filename, name, build, fragment_sizes_filename=FRAGMENT_SIZES_FILENAME,
                  strand_shift=-1, reads_dialect=DEFAULT_CHROMOSOME_DIALECT):
    """
    Wrapper function to load a pileup stranded object from a set of reads and perform a strand-shifted mixdown.

    This is just a kludgy hack in place of refactoring the StrandedPileups and Pileups classes to something more
    sensible.
    
    :param chromosmes:
    :param bed_filename:
    :param name:
    :param build:
    :return:
    """
    new_stranded = StrandedPileups(chrom_lengths=chrom_lengths, input_filename=data_filename, name=name, build=build,
                                   chromosome_dialect=reads_dialect)

    # check if pre-computed strand shift exists:

    rep_path, rep_filename, rep_extension = toolbox.parse_path(data_filename)
    if strand_shift == -1:
        try:
            with open(fragment_sizes_filename, 'rt') as ss_file:
                ss_reader = csv.reader(ss_file, dialect=csv.excel_tab)
                for line in ss_reader:
                    if line[0] == rep_filename:
                        strand_shift = int(line[1])
                        print(('Found pre-computed strand shift of {} for replicate {}'.format(strand_shift,
                                                                                               rep_filename)))
        except IOError:
            print('No strand shift file found.')

    if strand_shift == -1:
        print('No pre-computed strand shift found, computing now...')
        strand_shift = new_stranded.estimateFragmentSize()
        print('Saving strand shift to {}'.format(fragment_sizes_filename))
        with open(fragment_sizes_filename, 'a') as ss_file:
            ss_writer = csv.writer(ss_file, dialect=csv.excel_tab)
            ss_writer.writerow([rep_filename, str(strand_shift)])

    return new_stranded.mixDown(strand_shift)


def load_starts_only(chrom_lengths, input_filename, name, build, chromosome_dialect=DEFAULT_CHROMOSOME_DIALECT):
    """
    Wrapper function to load a pileup object from only the starts of reads (presumed fragment ends)

    :param chromosmes:
    :param bed_filename:
    :param name:
    :param build:
    :return:
    """
    print('Generating pileup vector from read starts in {}'.format(input_filename))
    new_stranded = StrandedPileups(chrom_lengths=chrom_lengths, name=name, build=build,
                                   chromosome_dialect=chromosome_dialect)
    new_stranded.loadFromBed(input_filename=input_filename, region_handling='starts', ignore_strandless=False)
    return new_stranded.mixDown()


def load_soft_masked(config, chrom_lengths, name, build, input_filename, ref_genome_path,
                     chromosome_dialect=DEFAULT_CHROMOSOME_DIALECT, validate=False):
    """
    Convenience function that:
        1. Generates a stranded pileup vector from a readset file using the fragment extension method
        2. Generates a soft mask for the given fragment length from a file of alignable start sites for the given read length.
        3. Applies the soft mask while mixing down the stranded pileup vector to a single strand
        4. Generates a hard mask from regions in the soft mask that are zero on both strands, representing areas with no possible
            fragment density.
        5. Returns both the unstranded, soft-masked, fragment pileup vector and the hard mask.

    Now, will look for a pre-saved pileup data folder in a subfolder of PILEUP_DATA_FOLDER having the name of the tagalign file.
    :return:
    """
    data_save_folder = os.path.join(PILEUP_DATA_FOLDER, toolbox.parse_path(input_filename)[1] + '_data')

    toolbox.establish_path(PILEUP_DATA_FOLDER)

    overall_load_start_time = datetime.datetime.now()

    print('Looking for pre-generated data pileup in {}'.format(data_save_folder))
    generate_data = False
    try:
        unstranded_chip = Pileups.load(data_save_folder, mmap_mode='')

    except (IOError, OSError):
        print('Pre-generated data not found. Will generate now.')
        generate_data = True

    else:
        read_length = unstranded_chip.mode_read_length

    if generate_data:
        print()
        print('Generating pileup vector from {} using fragment extension method'.format(input_filename))

        chip_starts = StrandedPileups(chrom_lengths=chrom_lengths, name='{}_starts'.format(name),
                                      build=config['GENOME_BUILD'],
                                      chromosome_dialect=chromosome_dialect)

        chip_starts.loadFromBed(input_filename=input_filename, region_handling='starts')

        rep_path, rep_name, rep_extension = toolbox.parse_path(input_filename)

        fragment_length = chip_starts.getFragmentSize(replicate_name=rep_name, save_plot_fname=os.path.join(rep_path,
                                                                                                            '{}_fragment_size_cc'.format(
                                                                                                                rep_name)))
        print()
        print('Extending data reads to fragments of size {} ...'.format(fragment_length))
        stranded_chip = chip_starts.fragExtend(fragment_length)
        read_length = chip_starts.mode_read_length  # grab this number before we delete the whole thing
        del chip_starts

    soft_mask_save_folder = os.path.join(PILEUP_DATA_FOLDER,
                                         '{}_{}_soft_mask'.format(config['GENOME_BUILD'], read_length))

    try:
        print('Looking for pre-generated soft mask pileup in {}'.format(soft_mask_save_folder))
        soft_mask=StrandedPileups.load(soft_mask_save_folder, mmap_mode='')
        
    except (IOError, OSError) as ex:
        print('Pre-generated soft mask not found. Generating . . .')
        generate_soft_mask = True
    
    else:
        generate_soft_mask = False

    if generate_soft_mask:
        print()
        print('Generating soft mask ...')

        alignable_starts_filename = os.path.join(ref_genome_path,
                                                 '{}_start_regions_{}.bed'.format(config['GENOME_BUILD'], read_length))

        if not os.path.isfile(alignable_starts_filename):
            mappble_basepairs = pp_mappability.get_mappability(config, read_length, make_region_file=True)

        soft_mask_starts = StrandedPileups(chrom_lengths=chrom_lengths,
                                           name='{}_{}_soft_mask_starts'.format(config['GENOME_BUILD'], read_length),
                                           build=config['GENOME_BUILD'],
                                           chromosome_dialect=chromosome_dialect)
        soft_mask_starts.loadFromBed(input_filename=alignable_starts_filename, ignore_strandless=True,
                                     display_read_lengths=False)

        soft_mask = soft_mask_starts.readStartsToSoftMask(read_length=read_length, fragment_length=fragment_length)

        soft_mask.save(soft_mask_save_folder)

    hard_mask_save_folder = os.path.join(PILEUP_DATA_FOLDER,
                                         '{}_{}_hard_mask'.format(config['GENOME_BUILD'], read_length))

    try:
        print('Looking for pre-generated hard mask pileup in {}'.format(hard_mask_save_folder))
        hard_mask = Pileups.load(hard_mask_save_folder, mmap_mode='')
    
    except (IOError, OSError) as ex:
        print('Pre-generated hard mask not found. Generating . . .')
        generate_hard_mask = True
    
    else:
        generate_hard_mask = False

    if generate_hard_mask:
        print()
        print('Generating hard mask of unalignable regions ...')

        hard_mask = soft_mask.mixDown().nonzero()
        hard_mask.name = '{}_hard_mask'.format(read_length)

        hard_mask.toType(numpy.bool)
        hard_mask.save(hard_mask_save_folder)

    if generate_data:
        print()
        stranded_chip.applySoftMask(soft_mask=soft_mask)
        del soft_mask

        print()
        print('Mixing down stranded ChIP pileups to single-stranded...')

        unstranded_chip = stranded_chip.mixDown()
        del stranded_chip
        unstranded_chip.toType(PILEUP_DTYPE)

        print()
        print('All done loading {} in {}'.format(unstranded_chip.name,
                                                  datetime.datetime.now() - overall_load_start_time))
        unstranded_chip.save(data_save_folder)

    if validate:
        print('Validating...')
        to_use = numpy.nonzero(hard_mask.flatten())[0]
        min_chip = unstranded_chip.flatten()[to_use].min()
        max_chip = unstranded_chip.flatten()[to_use].max()
        print(('Min value: {}, max value: {}'.format(min_chip, max_chip)))
        if max_chip > fragment_length * 2:
            raise Exception(
                'Invalid maximum pileup height {} in {}, should <= 2 * fragment size of {}'.format(max_chip,
                                                                                                   unstranded_chip.name,
                                                                                                   fragment_length))

    print('Loaded successfully in {}.'.format(datetime.datetime.now() - overall_load_start_time))

    return unstranded_chip, hard_mask


def homer_parse_taginfo(tag_info_filename):
    """
    Extract information from HOMER's tagInfo.txt file in the tag directory.
    
    Returns a dictionary consisting of the fields defined by the key-value pairs at the top of the file.
    
    Note that the current format of the tagInfo file is a little wonky, seems to be a work in progress subject to 
    change down the road.
    
    It's basically a 3-column TSV with the chromosome, unique positions, and total tags. But after the header,
    and the global values, there's a set of lines with key-value pairs, then it gives the 3 columns for the
    individual chromosomes.
    
    Values useful for constructing a pileup: fragmentLengthEstimate, peakSizeEstimate, averageTagLength
    
    """
    with open(tag_info_filename, 'rt') as tag_info_file:
        info = {}

        header = tag_info_file.readline()
        assert header == 'name\tUnique Positions\tTotal Tags\n', 'Invalid header found: {}'.format(header)
        global_values = tag_info_file.readline()
        line = tag_info_file.readline()
        # read the key value pairs
        while '=' in line:
            key, value = [x.strip() for x in line.strip().split('=')]
            info[key] = toolbox.smart_convert(value)
            line = tag_info_file.readline()

        return info


def homer_get_mode_tag_length(tag_length_distribution_filename):
    """
    Parses HOMER's tagLengthDistribution.txt file and returns the mode (most common value) of the distribution
    """
    tag_length_frequencies = []
    with open(tag_length_distribution_filename) as tag_length_file:
        tag_length_file.readline()

        tag_length_frequencies = []
        for line in tag_length_file:
            split_line = line.split('\t')
            tag_length_frequencies.append((int(split_line[0]), float(split_line[1])))
    return sorted(tag_length_frequencies, key=lambda x: x[1])[-1][0]


def load_soft_masked_from_homer(config, chrom_lengths, name, build, homer_tag_directory,
                                chromosome_dialect=DEFAULT_CHROMOSOME_DIALECT, conservative_hard_mask=False,
                                mem_map_mode='r',
                                validate=False, disable_soft_mask=False, max_clonality=1.0):
    """
    Convenience function that:
        1. Generates a stranded pileup vector from a readset file using the fragment extension method
        2. Generates a soft mask for the given fragment length from a file of alignable start sites for the given read length.
        3. Applies the soft mask while mixing down the stranded pileup vector to a single strand
        4. Generates a hard mask from regions in the soft mask that are zero on both strands, representing areas with no possible
            fragment density.
        5. Returns both the unstranded, soft-masked, fragment pileup vector and the hard mask.

    Now, will look for a pre-saved pileup data folder in a subfolder of PILEUP_DATA_FOLDER having the name of the tagalign file.
    :return:
    """
    rep_name = homer_tag_directory.strip('/').split(os.path.sep)[-1]
    if rep_name.endswith('/'): rep_name = rep_name[:-1]
    print('Rep name: {}'.format(rep_name))

    data_save_folder = os.path.join(PILEUP_DATA_FOLDER, rep_name + '_data')
    toolbox.establish_path(PILEUP_DATA_FOLDER)
    overall_load_start_time = datetime.datetime.now()

    print('Looking for pre-generated data pileup in {}'.format(data_save_folder))
    generate_data = False
    need_soft_mask = False
    generate_soft_mask = False
    generate_hard_mask = False

    try:
        unstranded_chip = Pileups.load(data_save_folder, mmap_mode=mem_map_mode)

    except (IOError, OSError) as ex:
        print('Pre-generated data not found. Will generate now.')
        generate_data = True

    else:
        read_length = unstranded_chip.mode_read_length

    if generate_data:
        print()
        print('Generating pileup vector from HOMER tag folder {} using fragment extension method'.format(
            homer_tag_directory))

        chip_starts = StrandedPileups(chrom_lengths=chrom_lengths, name='{}_starts'.format(name),
                                      build=build,
                                      chromosome_dialect=chromosome_dialect)

        chip_starts.load_from_homer_tag_directory(input_filename=homer_tag_directory, region_handling='starts')
        chip_starts.mode_read_length = homer_get_mode_tag_length(
            os.path.join(homer_tag_directory, 'tagLengthDistribution.txt'))
            
        if max_clonality is not None:
            print('Filtering to allow maximum {} reads at each locus ...'.format(max_clonality))
            for chrom in chip_starts.spileups:
                for strand in chip_starts.spileups[chrom]:
                    chip_starts.spileups[chrom][strand] = numpy.clip(chip_starts.spileups[chrom][strand], a_min=0, a_max=max_clonality)

        fragment_length = get_fragment_size_from_file(rep_name)
        if not fragment_length:
            # get fragment size from homer

            homer_info = homer_parse_taginfo(os.path.join(homer_tag_directory, 'tagInfo.txt'))
            fragment_length = homer_info['fragmentLengthEstimate']

            save_fragment_length(rep_name, fragment_length)

        print()
        print('Extending data reads to fragments of size {} ...'.format(fragment_length))
        stranded_chip = chip_starts.fragExtend(fragment_length)
        read_length = chip_starts.mode_read_length  # grab this number before we delete the whole thing
        del chip_starts
        need_soft_mask = True
    else:
        fragment_length = get_fragment_size_from_file(rep_name)

    hard_mask_save_folder = os.path.join(PILEUP_DATA_FOLDER, '{}_{}_{}{}_hard_mask'.format(build, read_length, fragment_length,
                                                                                        ['', '_conservative'][
                                                                                            conservative_hard_mask]))

    try:
        print('Looking for pre-generated hard mask pileup in {}'.format(hard_mask_save_folder))
        hard_mask = Pileups.load(hard_mask_save_folder, mmap_mode=mem_map_mode)
    except (IOError, OSError) as ex:
        print('Pre-generated hard mask not found.')
        generate_hard_mask = True
        need_soft_mask = True

    if need_soft_mask:
        soft_mask_save_folder = os.path.join(PILEUP_DATA_FOLDER, '{}_{}_{}_soft_mask'.format(build, read_length, fragment_length))

        try:
            print('Looking for pre-generated soft mask pileup in {}'.format(soft_mask_save_folder))
            soft_mask = StrandedPileups.load(soft_mask_save_folder, mmap_mode=mem_map_mode)

        except (IOError, OSError) as ex:
            print('Pre-generated soft mask not found.')
            generate_soft_mask = True

    if generate_soft_mask:
        print()
        print('Generating soft mask ...')
        ref_genome_path=toolbox.parse_path(config['REFERENCE_GENOME_PATH'])[0]

        alignable_starts_filename = os.path.join(ref_genome_path,
                                                 '{}_start_regions_{}.bed'.format(build, read_length))

        if not os.path.isfile(alignable_starts_filename):
            mappble_basepairs = pp_mappability.get_mappability(config, read_length, make_region_file=True)

        soft_mask_starts = StrandedPileups(chrom_lengths=chrom_lengths,
                                           name='{}_{}_soft_mask_starts'.format(build, read_length),
                                           build=build,
                                           chromosome_dialect=chromosome_dialect)
        soft_mask_starts.loadFromBed(input_filename=alignable_starts_filename, ignore_strandless=True,
                                     display_read_lengths=False)

        soft_mask = soft_mask_starts.readStartsToSoftMask(read_length=read_length, fragment_length=fragment_length)

        soft_mask.save(soft_mask_save_folder)
        if mem_map_mode == 'rw':
            soft_mask.memMap(writable=True)
        elif mem_map_mode == 'r':
            soft_mask.memMap(writable=False)

    if generate_hard_mask:
        print()
        print('Generating hard mask of unalignable regions ...')

        if conservative_hard_mask:
            print('\tUsing conservative approach (excluding all regions impacted by mappability)...')
            hard_mask = soft_mask.mixDown().threshold(min_value=1.999)
        else:
            print(
                '\tUsing permissive approach (excluding only regions that are totally unable to receive fragments because of mappability)')
            hard_mask = soft_mask.mixDown().nonzero()

        hard_mask.name = '{}_hard_mask'.format(read_length)

        hard_mask.toType(numpy.bool)
        hard_mask.save(hard_mask_save_folder)
        
        if mem_map_mode == 'rw':
            hard_mask.memMap(writable=True)
        elif mem_map_mode == 'r':
            hard_mask.memMap(writable=False)

    if generate_data:
        print()
        if disable_soft_mask:
            print('Soft mask application DISABLED')
        else:
            # print('Applying soft mask ...')
            stranded_chip.applySoftMask(soft_mask=soft_mask)
        del soft_mask

        print()
        print('Mixing down stranded ChIP pileups to single-stranded...')

        unstranded_chip = stranded_chip.mixDown()
        del stranded_chip
        unstranded_chip.toType(PILEUP_DTYPE)

        print()
        print('All done loading {} in {}'.format(unstranded_chip.name,
                                                 datetime.datetime.now() - overall_load_start_time))
        unstranded_chip.save(data_save_folder)
        if mem_map_mode == 'rw':
            unstranded_chip.memMap(writable=True)
        elif mem_map_mode == 'r':
            unstranded_chip.memMap(writable=False)

    if validate:
        print('Validating...')
        to_use = numpy.nonzero(hard_mask.flatten())[0]
        min_chip = unstranded_chip.flatten()[to_use].min()
        max_chip = unstranded_chip.flatten()[to_use].max()
        print('Min value: {}, max value: {}'.format(min_chip, max_chip))
        if max_chip > fragment_length * 2:
            raise Exception(
                'Invalid maximum pileup height {} in {}, should <= 2 * fragment size of {}'.format(max_chip,
                                                                                                   unstranded_chip.name,
                                                                                                   fragment_length))

    print('Loaded successfully in {}.'.format(datetime.datetime.now() - overall_load_start_time))

    return unstranded_chip, hard_mask

    
def load_soft_masked_from_homer_nomask(config, chrom_lengths, name, build, homer_tag_directory,
                                chromosome_dialect=DEFAULT_CHROMOSOME_DIALECT,
                                mem_map_mode='r', max_clonality=1.0,
                                validate=False):
    """
    Convenience function that:
        1. Generates a stranded pileup vector from a readset file using the fragment extension method        
        5. Returns both the unstranded, fragment pileup vector.

    Now, will look for a pre-saved pileup data folder in a subfolder of PILEUP_DATA_FOLDER having the name of the tagalign file.
    :return:
    """
    rep_name = homer_tag_directory.strip('/').split(os.path.sep)[-1]
    if rep_name.endswith('/'): rep_name = rep_name[:-1]
    print('Rep name: {}'.format(rep_name))

    data_save_folder = os.path.join(PILEUP_DATA_FOLDER, rep_name + '_data')
    toolbox.establish_path(PILEUP_DATA_FOLDER)
    overall_load_start_time = datetime.datetime.now()

    print('Looking for pre-generated data pileup in {}'.format(data_save_folder))
    generate_data = False

    try:
        unstranded_chip = Pileups.load(data_save_folder, mmap_mode=mem_map_mode)

    except (IOError, OSError) as ex:
        print('Pre-generated data not found. Will generate now.')
        generate_data = True

    else:
        read_length = unstranded_chip.mode_read_length

    if generate_data:
        print()
        print('Generating pileup vector from HOMER tag folder {} using fragment extension method'.format(
            homer_tag_directory))

        chip_starts = StrandedPileups(chrom_lengths=chrom_lengths, name='{}_starts'.format(name),
                                      build=build,
                                      chromosome_dialect=chromosome_dialect)

        chip_starts.load_from_homer_tag_directory(input_filename=homer_tag_directory, region_handling='starts')
        chip_starts.mode_read_length = homer_get_mode_tag_length(
            os.path.join(homer_tag_directory, 'tagLengthDistribution.txt'))
            
        if max_clonality > 0:
            print('Filtering to allow maximum {} reads at each locus ...'.format(max_clonality))
            for chrom in chip_starts.spileups:
                for strand in chip_starts.spileups[chrom]:
                    chip_starts.spileups[chrom][strand] = numpy.clip(chip_starts.spileups[chrom][strand], a_min=0, a_max=max_clonality)            

        fragment_length = get_fragment_size_from_file(rep_name)
        if not fragment_length:
            # get fragment size from homer

            homer_info = homer_parse_taginfo(os.path.join(homer_tag_directory, 'tagInfo.txt'))
            fragment_length = homer_info['fragmentLengthEstimate']

            save_fragment_length(rep_name, fragment_length)

        print()
        print('Extending data reads to fragments of size {} ...'.format(fragment_length))
        stranded_chip = chip_starts.fragExtend(fragment_length)
        read_length = chip_starts.mode_read_length  # grab this number before we delete the whole thing
        del chip_starts

    else:
        fragment_length = get_fragment_size_from_file(rep_name)

    if generate_data:
        print()        
        print('Mixing down stranded ChIP pileups to single-stranded...')

        unstranded_chip = stranded_chip.mixDown()
        del stranded_chip
        unstranded_chip.toType(PILEUP_DTYPE)

        print()
        print('All done loading {} in {}'.format(unstranded_chip.name,
                                                 datetime.datetime.now() - overall_load_start_time))
        unstranded_chip.save(data_save_folder)
        if mem_map_mode == 'rw':
            unstranded_chip.memMap(writable=True)
        elif mem_map_mode == 'r':
            unstranded_chip.memMap(writable=False)

    if validate:
        print('Validating...')
        to_use = numpy.nonzero(hard_mask.flatten())[0]
        min_chip = unstranded_chip.flatten()[to_use].min()
        max_chip = unstranded_chip.flatten()[to_use].max()
        print('Min value: {}, max value: {}'.format(min_chip, max_chip))
        if max_chip > fragment_length * 2:
            raise Exception(
                'Invalid maximum pileup height {} in {}, should <= 2 * fragment size of {}'.format(max_chip,
                                                                                                   unstranded_chip.name,
                                                                                                   fragment_length))

    print('Loaded successfully in {}.'.format(datetime.datetime.now() - overall_load_start_time))

    return unstranded_chip    


def frag_extend_chromslave(params):
    """
    Used to extend stranded chromosomes in a multi-process manner.
    """
    chrom_start_time = datetime.datetime.now()
    chrom, read_starts, frag_length = params
    dbg_print('Extending chromosome {}...'.format(chrom), 1)

    neg_strand, pos_strand = read_starts

    # copy and convert to float64 for optimal speed
    neg_strand = neg_strand.astype(numpy.float64)
    pos_strand = pos_strand.astype(numpy.float64)

    extended_strands = [neg_strand.copy(), pos_strand.copy()]

    for i in range(1, frag_length):
        extended_strands[0][:-i] += neg_strand[i:]
        extended_strands[1][i:] += pos_strand[:-i]
    dbg_print('Done extending chromosome {} in {}'.format(chrom, datetime.datetime.now() - chrom_start_time), 1)

    return chrom, extended_strands


def binding_energy_chromslave(params):
    chrom, sequence_vector, motif = params
    # print 'Chrom: {}, motif: {}'.format(chrom, motif)
    # print 'Sequence vector: {} {}'.format(sequence_vector.shape, sequence_vector[:10])
    # return chrom, (motifs.scan_pwm(sequence_vector[::-1], motif)[::-1], motifs.scan_pwm(sequence_vector, motif))
    return chrom, (
    motifs.scan_pwm(sequence_vector, motifs.motif_rev_complement(motif)), motifs.scan_pwm(sequence_vector, motif))


def soft_mask_generate_chromslave(params, check_empty=False):
    this_chrom_start_time = datetime.datetime.now()
    chrom, fragment_starts, read_length, fragment_length = params

    for i in range(len(fragment_starts)):
        if fragment_starts[i].dtype != numpy.float64:
            fragment_starts[i] = fragment_starts[i].astype(numpy.float64)

    # first check if chromosome is empty
    if not check_empty or numpy.abs(fragment_starts).sum() > 0 or numpy.abs(fragment_starts).sum() > 0:
        dbg_print('Processing chromosome {} ({} bp)...'.format(chrom, len(fragment_starts)), 1)
        soft_mask = {}
        # positive strand
        soft_mask[1] = fragment_starts.copy()  # account for fragment starts (offset 0)
        # progressively shift and add the start sites up to <fragment_length> to effectively extend the fragments
        for offset in range(1, fragment_length):
            soft_mask[1][offset:] += fragment_starts[:-offset]
        soft_mask[1] /= float(fragment_length)

        # negative strand is an image of the positive strand offset by fragment_size + read_length
        soft_mask[-1] = numpy.zeros(len(fragment_starts))
        soft_mask[-1][:-fragment_length + read_length] = soft_mask[1][
                                                         fragment_length - read_length:]
        dbg_print('Done with chromosome {} in {}'.format(chrom, datetime.datetime.now() - this_chrom_start_time), 1)
    else:
        # if empty, soft mask is all zeroes for that chromosome
        dbg_print('Chromosome {} is empty, skipping...'.format(chrom), 1)
        soft_mask = {1: numpy.zeros(len(fragment_starts)), -1: numpy.zeros(len(fragment_starts))}

    return chrom, (soft_mask[-1], soft_mask[1])


def cross_correlate_chromslave(params, check_empty=True):
    start_time = datetime.datetime.now()
    chrom, chunk_idx, chrom_strands = params

    neg_strand, pos_strand = chrom_strands
    del chrom_strands

    if neg_strand.dtype != numpy.float64:
        neg_strand = neg_strand.astype(numpy.float64)
    if pos_strand.dtype != numpy.float64:
        pos_strand = pos_strand.astype(numpy.float64)

    # del chrom_strands
    if (numpy.abs(neg_strand).sum() > 0 and numpy.abs(pos_strand).sum() > 0) or not check_empty:
        dbg_print('Cross-correlating chunk {} of chromosome {} ...'.format(chunk_idx, chrom), 1)
        cc = scipy.signal.fftconvolve(neg_strand, pos_strand[::-1], mode='same')
        dbg_print('Done cross-correlating chunk {} of chromosome {} in {}'.format(chunk_idx, chrom,
                                                                                  datetime.datetime.now() - start_time),
                  1)
    else:
        dbg_print('Chromosome {} is empty, skipping...'.format(chrom), 1)
        cc = numpy.zeros(len(neg_strand))
    # cc = toolbox.replace_with_mem_map(cc, read_only=True, tmp_dir=LOCAL_TMP_DIR)
    return chrom, chunk_idx, cc


class StrandedPileups(object):
    def __init__(self, chrom_lengths={}, input_filename='', name='', build='',
                 chromosome_dialect=DEFAULT_CHROMOSOME_DIALECT, pileup_dtype=PILEUP_DTYPE):
        self.id = toolbox.random_identifier(32)
        self.pileup_dtype = pileup_dtype
        self.save_path = None
        self.name = name
        self.build = build
        self.spileups = {}
        self.chrom_lengths = {}
        # self.genome_size = -1
        self.read_counts = {}
        self.chromosome_dialect = chromosome_dialect
        for chrom in chrom_lengths:
            translated_chrom = toolbox.convert_chroms(chrom, dest=self.chromosome_dialect)
            self.chrom_lengths[translated_chrom] = chrom_lengths[chrom]
            self.spileups[translated_chrom] = {}
            self.spileups[translated_chrom][-1] = numpy.zeros(chrom_lengths[chrom],
                                                              dtype=self.pileup_dtype)  # negative strand
            self.spileups[translated_chrom][1] = numpy.zeros(chrom_lengths[chrom],
                                                             dtype=self.pileup_dtype)  # positive strand
            self.read_counts[translated_chrom] = 0
            # self.genome_size += chrom_lengths[chrom]
        self.is_normalized = False
        self.total_read_length = 0
        self.total_reads = 0
        self.coverage = 0
        self.fragment_size = -1
        self.mean_read_length = -1
        self.mode_read_length = -1
        # self.max_height = -1
        self.input_filename = input_filename

        print(('Initialized new stranded pileup object: {}, genome build: {}, chromosome dialect: {}'.format(self.name,
                                                                                                             self.build,
                                                                                                             self.chromosome_dialect)))

        # print 'Initialized with chromosomes {} in length dict; {} in pileups'.format(', '.join(sorted(list(self.chrom_lengths.keys()))), ', '.join(sorted(list(self.spileups.keys()))))

        if self.input_filename:
            if input_filename.endswith('.bwtout.txt'):
                self.loadFromBowtie(input_filename)
            else:
                self.loadFromBed(input_filename)

    @property
    def genome_size(self):
        return sum(self.chrom_lengths.values())

    def __del__(self):
        if self.save_path and os.path.exists(self.save_path):
            try:
                shutil.rmtree(self.save_path)
            except (OSError, IOError) as ex:
                print(('Tried to delete {} but caught {} instead'.format(self.save_path, ex)))

    def __iadd__(self, other):
        try:
            assert self.build == other.build
            self.name = '({}+{})'.format(self.name, other.name)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    assert len(self.spileups[chrom][strand]) == len(other.spileups[chrom][strand])
                    self.spileups[chrom][strand] += other.pileups[chrom][strand]
            self.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            self.name = '({}+{})'.format(self.name, other)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    self.spileups[chrom][strand] = numpy.add(self.spileups[chrom][strand], other)
        return self

    def __isub__(self, other):
        try:
            assert self.build == other.build
            self.name = '({}-{})'.format(self.name, other.name)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    assert len(self.spileups[chrom][strand]) == len(other.spileups[chrom][strand])
                    self.spileups[chrom][strand] -= other.pileups[chrom][strand]
            self.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            self.name = '({}-{})'.format(self.name, other)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    self.spileups[chrom][strand] = numpy.subtract(self.spileups[chrom][strand], other)
        return self

    def __imul__(self, other):
        try:
            assert self.build == other.build
            self.name = '({}*{})'.format(self.name, other.name)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    assert len(self.spileups[chrom][strand]) == len(other.spileups[chrom][strand])
                    self.spileups[chrom][strand] *= other.pileups[chrom][strand]
            self.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            self.name = '({}*{})'.format(self.name, other)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    self.spileups[chrom][strand] = numpy.multiply(self.spileups[chrom][strand], other)
        return self

    def __idiv__(self, other):
        try:
            assert self.build == other.build
            self.name = '({}/{})'.format(self.name, other.name)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    assert len(self.spileups[chrom][strand]) == len(other.spileups[chrom][strand])
                    self.spileups[chrom][strand] /= other.pileups[chrom][strand].astype(float)
            self.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            self.name = '({}/{})'.format(self.name, other)
            for chrom in self.spileups:

                for strand in self.spileups[chrom]:
                    self.spileups[chrom][strand] = numpy.divide(self.spileups[chrom][strand], float(other))
        return self

    def __add__(self, other):
        result = self.emptyCopy()
        try:
            assert self.build == other.build
            result.name = '({}+{})'.format(self.name, other.name)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    assert len(self.spileups[chrom][strand]) == len(other.spileups[chrom][strand])
                    result.spileups[chrom][strand] = self.spileups[chrom][strand] + other.spileups[chrom][strand]
            result.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    result.spileups[chrom][strand] = numpy.add(self.spileups[chrom][strand], other)
            result.name = '({}+{})'.format(self.name, other)
        return result

    def __sub__(self, other):
        result = self.emptyCopy()
        try:
            assert self.build == other.build
            result.name = '({}-{})'.format(self.name, other.name)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    assert len(self.spileups[chrom][strand]) == len(other.spileups[chrom][strand])
                    result.spileups[chrom][strand] = self.spileups[chrom][strand] - other.spileups[chrom][strand]
            result.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    result.spileups[chrom][strand] = numpy.subtract(self.spileups[chrom][strand], other)
            result.name = '({}-{})'.format(self.name, other)
        return result

    def __mul__(self, other):
        result = self.emptyCopy()
        try:
            assert self.build == other.build
            result.name = '({}*{})'.format(self.name, other.name)
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    assert len(self.spileups[chrom][strand]) == len(other.spileups[chrom][strand])
                    result.spileups[chrom][strand] = self.spileups[chrom][strand] * other.spileups[chrom][strand]
            result.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            for chrom in self.spileups:
                for strand in self.spileups[chrom]:
                    result.spileups[chrom][strand] = numpy.multiply(self.spileups[chrom][strand], other)
            result.name = '({}*{})'.format(self.name, other)
        return result

    def __div__(self, other):
        result = self.emptyCopy()
        try:
            assert self.build == other.build
            result.name = '({}/{})'.format(self.name, other.name)
            for chrom in self.spileups:
                if chrom not in result.spileups: # ToDo: extend this fix to other operations for StrandedPileup
                    result.spileups[chrom] = {}
                for strand in self.spileups[chrom]:
                    assert len(self.spileups[chrom][strand]) == len(other.spileups[chrom][strand])
                    result.spileups[chrom][strand] = self.spileups[chrom][strand] / other.spileups[chrom][strand].astype(float)
            result.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            # print ex
            for chrom in self.spileups:
                if chrom not in result.spileups: # ToDo: extend this fix to other operations for StrandedPileup
                    result.spileups[chrom] = {}
                for strand in self.spileups[chrom]:
                    result.spileups[chrom][strand] = numpy.divide(self.spileups[chrom][strand], float(other))
            result.name = '({}/{})'.format(self.name, other)
        return result

    def __pos__(self):
        return self

    def __neg__(self):
        negated = StrandedPileups(self.chrom_lengths, build=self.build, name=self.name)

        for chrom in self.spileups:
            for strand in self.spileups[chrom]:
                negated.spileups[chrom][strand] = -self.spileups[chrom][strand]
        return negated

    def __len__(self):
        return self.genome_size

    def __abs__(self):
        result = StrandedPileups(self.chrom_lengths, build=self.build, name=self.name)

        for chrom in self.spileups:
            for strand in self.spileups[chrom]:
                result.spileups[chrom] = numpy.abs(self.spileups[chrom])
        return result

    def __repr__(self):
        result = 'Pileups object. Name: {}, Build: {}\n'.format(self.name, self.build)
        result += 'Chromosome lengths:\n'
        for chrom in self.chrom_lengths:
            result += '\t{:>40}\t{:>11}\n'.format(chrom, self.chrom_lengths[chrom])
        try:
            result += 'Data type: {}\n'.format(list(self.spileups.values())[0][1].dtype)
        except Exception:
            pass
        return result

    def loadFromBowtie(self, bowtie_filename, ignore_strandless=False):
        """
        Populate the pileup vector from a bowtie output file (.bwt)
        Each strand will go into a separate vector
        """
        start_time = datetime.datetime.now()
        strand_translator = {'+': 1, '-': -1}
        missing_chroms = set([])

        self.read_length_counts = {}

        self.input_filename = bowtie_filename
        with open(bowtie_filename, 'rt') as bwt_file:
            print(('Computing stranded pileup vectors from reads in {} ...'.format(bowtie_filename)))
            for line_num, line in enumerate(bwt_file):
                if line_num % REPORTING_INTERVAL == 0:
                    dbg_print('Reading line {}'.format(line_num), 1)
                if len(line) > 0:
                    split_line = line.strip().split('\t')
                    strand = strand_translator[split_line[1]]
                    chrom = toolbox.convert_chroms(split_line[2], dest=self.chromosome_dialect)

                    if chrom in self.spileups:
                        self.read_counts[chrom] += 1
                        start_pos = int(split_line[3])
                        end_pos = start_pos + len(split_line[4])
                        read_length = end_pos - start_pos
                        if read_length not in self.read_length_counts:
                            self.read_length_counts[read_length] = 0
                        else:
                            self.read_length_counts[read_length] += 1
                        self.total_read_length += read_length
                        self.spileups[chrom][strand][start_pos:end_pos] += 1
                    else:
                        missing_chroms.add(chrom)

            self.total_reads = sum(self.read_counts.values())
            self.mode_read_length = max(list(self.read_length_counts.items()), key=lambda x: x[1])[0]

            if self.total_reads > 0:
                self.mean_read_length = self.total_read_length / float(self.total_reads)
            else:
                self.mean_read_length = 0

            self.computeCoverage()

        print(('\tMean coverage: {}'.format(self.coverage)))

        if missing_chroms:
            print((
            '\tThe following chromosomes were found in the reads file but not in the defined chromosome structure: {}'.format(
                ', '.join(sorted(list(missing_chroms))))))
        print(('Done in {}.'.format(datetime.datetime.now() - start_time)))

    def loadFromBed(self, input_filename, region_handling=None, ignore_strandless=False,
                    display_read_lengths=True):
        """
        Populate the pileup vector from a BED file (each genomic position will contains a count of the number of BED regions that overlap it)
        Each strand will go into a separate vector
        """
        start_time = datetime.datetime.now()
        strand_translator = {'+': 1, '-': -1}
        self.input_filename = input_filename

        # print 'Chromosome dialect for bed file given as: {}'.format(reads_chromosome_dialect)

        self.read_length_counts = collections.defaultdict(lambda: 0)
        self.total_read_density = collections.defaultdict(lambda: 0)
        missing_chroms = set([])

        start_only = False
        end_only = False

        print(('Computing stranded pileup vectors from regions in {} ...'.format(input_filename)))

        if region_handling == 'starts':
            start_only = True
            print('Using region starts only.')
        elif region_handling == 'ends':
            end_only = True
            print('Using region ends sites only.')
        elif region_handling != None:
            raise ValueError('Received invalid value for parameter <region_handling>. Got {}'.format(region_handling))

        with open(input_filename, 'rt') as tag_file:
            for line_num, line in enumerate(tag_file):
                if line_num % REPORTING_INTERVAL == 0:
                    dbg_print('Reading line {}'.format(line_num), 1)
                split_line = line.strip().split('\t')
                if len(line) > 0:
                    chrom = toolbox.convert_chroms(split_line[0], dest=self.chromosome_dialect)
                    # print split_line
                    if len(split_line) >= 6:
                        strand = strand_translator[split_line[5]]
                    else:
                        strand = 1
                        if not ignore_strandless:
                            raise Exception("\tRead with no strand found on line {}: {}".format(line_num, line))

                    if chrom in self.spileups:
                        self.read_counts[chrom] += 1
                        start_pos = int(split_line[1])
                        end_pos = int(split_line[2]) - 1
                        read_length = end_pos - start_pos + 1
                        self.total_read_density[chrom] += read_length
                        self.read_length_counts[read_length] += 1

                        assert start_pos >= 0
                        assert end_pos < self.chrom_lengths[chrom]

                        if (start_only and strand == 1) or (end_only and strand == -1):
                            self.spileups[chrom][strand][start_pos] += 1
                            # print 'read: {}, updating position {}'.format(line, start_pos)
                        elif (end_only and strand == 1) or (start_only and strand == -1):
                            self.spileups[chrom][strand][end_pos] += 1
                            # print 'read: {}, updating position {}'.format(line, end_pos)
                        else:
                            self.spileups[chrom][strand][start_pos:end_pos] += 1

                    else:
                        if chrom not in missing_chroms:
                            dbg_print('Chromosome {} not found in self!'.format(chrom), 1)
                            missing_chroms.add(chrom)
            print('Done reading file.')
            if missing_chroms:
                print((
                '\tThe following chromosomes were present in the bed file but not in the length dictionary: {}'.format(
                    ', '.join(sorted(list(missing_chroms))))))
                # print '\tChromosome lengths in self:'
            # for chrom in toolbox.numerical_string_sort(self.chrom_lengths):
            # print '\t\t{:<20}: {}'.format(chrom, self.chrom_lengths[chrom])

            if display_read_lengths:
                dbg_print('Read length counts:', 1)
                for read_length in sorted(self.read_length_counts.keys()):
                    dbg_print('{}: {}'.format(read_length, self.read_length_counts[read_length]), 2)

            self.mode_read_length = max(list(self.read_length_counts.items()), key=lambda x: x[1])[0]

            dbg_print('{:<25} {:>10} {:>10}'.format('Chromosome', 'Reads', 'Coverage'), 1)
            for chrom in toolbox.numerical_string_sort(self.read_counts):
                dbg_print('{:<25} {:>10} {:>10}'.format(chrom, self.read_counts[chrom],
                                                        self.total_read_density[chrom] / float(
                                                            self.chrom_lengths[chrom])))

            self.total_reads = sum(self.read_counts.values())

            self.total_read_length = sum(self.total_read_density.values())

            if self.total_reads > 0:
                self.mean_read_length = self.total_read_length / float(self.total_reads)
            else:
                self.mean_read_length = 0

            self.computeCoverage()

        print(('\tMean coverage: {}'.format(self.coverage)))
        print(('Done in {}.'.format(datetime.datetime.now() - start_time)))

    def load_from_homer_tag_directory(self, input_filename, region_handling=None,
                                      display_read_lengths=True):
        """
        Populate the pileup vector from a BED file (each genomic position will contains a count of the number of tags that overlap it)
        Each strand will go into a separate vector.
        
        """
        start_time = datetime.datetime.now()
        strand_translator = {'0': 1, '1': -1}
        self.input_filename = input_filename

        self.read_length_counts = collections.defaultdict(lambda: 0)
        self.total_read_density = collections.defaultdict(lambda: 0)
        missing_chroms = set([])

        start_only = False
        end_only = False

        print('Computing stranded pileup vectors from HOMER tag directory {} ...'.format(input_filename))

        if region_handling == 'starts':
            start_only = True
            print('Using region starts only.')
        elif region_handling == 'ends':
            end_only = True
            print('Using region ends sites only.')
        elif region_handling != None:
            raise ValueError('Received invalid value for parameter <region_handling>. Got {}'.format(region_handling))

        for tag_file in sorted([f for f in os.listdir(input_filename) if f.endswith('.tags.tsv')]):
            print('\tProcessing tag file {}'.format(tag_file))

            with open(os.path.join(input_filename, tag_file), 'rt') as tag_file:
                for line_num, line in enumerate(tag_file):
                    #                    if line_num % REPORTING_INTERVAL == 0:
                    #                        dbg_print('Reading line {}'.format(line_num), 1)

                    split_line = line.strip().split('\t')

                    if len(line) > 0:
                        chrom = toolbox.convert_chroms(split_line[0], dest=self.chromosome_dialect)
                        # print split_line
                        strand = strand_translator[split_line[2]]

                        if chrom in self.spileups:
                            read_length = int(split_line[4])
                            start_pos = int(split_line[1]) - 1

                            if strand == 1:
                                end_pos = start_pos + read_length
                            else:
                                end_pos = start_pos - read_length

                            num_reads = float(split_line[3])
                            assert 0 <= start_pos < self.chrom_lengths[
                                chrom], 'Read start position {} is out of bounds for chromosome {} with bounds [{},{}). Offending line: {}'.format(
                                start_pos, chrom, 0, self.chrom_lengths[chrom], line)
                            assert 0 <= end_pos < self.chrom_lengths[
                                chrom], 'Read end position {} is out of bounds for chromosome {} with bounds [{},{}), strand {} Offending line: {}'.format(
                                end_pos, chrom, 0, self.chrom_lengths[chrom], strand, line)

                            self.read_counts[chrom] += num_reads
                            self.total_read_density[chrom] += read_length * num_reads
                            self.read_length_counts[read_length] += num_reads

                            if (start_only and strand == 1) or (end_only and strand == -1):
                                self.spileups[chrom][strand][start_pos] += num_reads
                                # print 'read: {}, updating position {}'.format(line, start_pos)
                            elif (end_only and strand == 1) or (start_only and strand == -1):
                                self.spileups[chrom][strand][end_pos] += num_reads
                                # print 'read: {}, updating position {}'.format(line, end_pos)
                            else:
                                self.spileups[chrom][strand][start_pos:end_pos] += num_reads

                        else:
                            if chrom not in missing_chroms:
                                dbg_print('Chromosome {} not found in self!'.format(chrom), 1)
                                missing_chroms.add(chrom)
                            #            print '\tDone.'
        print('Done with tag directory')

        if missing_chroms:
            print('\tThe following chromosomes were present in the bed file but not in the length dictionary: {}'.format(
                    ', '.join(sorted(list(missing_chroms)))))

        if display_read_lengths:
            dbg_print('Read length counts:', 1)
            for read_length in sorted(self.read_length_counts.keys()):
                dbg_print('{}: {}'.format(read_length, self.read_length_counts[read_length]), 2)

        self.mode_read_length = max(list(self.read_length_counts.items()), key=lambda x: x[1])[0]

        dbg_print('{:<25} {:>10} {:>10}'.format('Chromosome', 'Reads', 'Coverage'), 1)
        for chrom in toolbox.numerical_string_sort(self.read_counts):
            dbg_print('{:<25} {:>10} {:>10}'.format(chrom, self.read_counts[chrom],
                                                    self.total_read_density[chrom] / float(
                                                        self.chrom_lengths[chrom])))

        self.total_reads = sum(self.read_counts.values())

        self.total_read_length = sum(self.total_read_density.values())

        if self.total_reads > 0:
            self.mean_read_length = self.total_read_length / float(self.total_reads)
        else:
            self.mean_read_length = 0

        self.computeCoverage()

        print('\tMean coverage: {}'.format(self.coverage))
        print('Done in {}.'.format(datetime.datetime.now() - start_time))

    # def computeBindingEnergy(self, fasta_filename, jaspar_filename):
    # """
    # Computes a binding energy profile for the motif defined by <jaspar_filename> interacting with the genomic
    # sequence given in <fasta_filename> for each strand (negative strand uses reverse complement sequence). The
    # binding energy  for each subsequence is
    # :param fasta_filename:
    #     :param jaspar_filename:
    #     :return:
    #     """
    #     start_time = datetime.datetime.now()
    #     print 'Computing binding energy vectors for \'{}\' using motif file {} and reference sequence {}.'.format(
    #         self.name, jaspar_filename, fasta_filename)
    #
    #     with open(fasta_filename, 'rt') as fasta_file:
    #         sequence_dict = toolbox.parse_fasta_dict(fasta_file.read())
    #
    #         # make sure the sequence file matches our vectors
    #         for chrom in self.chrom_lengths:
    #             assert chrom in sequence_dict
    #             assert len(sequence_dict[chrom]) == self.chrom_lengths[chrom]
    #             # print chrom, len(sequence_dict[chrom]), self.chrom_lengths[chrom]
    #
    #     # compute global background dist:
    #     print '\tComputing background distribution of nucleotides...'
    #     background_freqs = {}
    #     for chrom in self.chrom_lengths:
    #         background_freqs = toolbox.dict_add(background_freqs, toolbox.freq(sequence_dict[chrom]))
    #     total_nucleotides = sum(background_freqs.values())
    #     background_model = numpy.zeros(4)
    #     for i, nuc in enumerate(('A', 'C', 'G', 'T')):
    #         background_model[i] = background_freqs[nuc] / float(total_nucleotides)
    #     print '\tA: {:>.2} C: {:>.2} G: {:>.2} T: {:>.2}'.format(*list(background_model))
    #
    #     print '\tGenerating background-aware log PWM...'
    #     pfm = motifs.load_PFM_horizontal(jaspar_filename)
    #     pwm = motifs.pfm_to_pwm_log(pfm, background_model=background_model, pseudo_count=0.01)
    #     score_offset = int(pwm.shape[1] / 2)  # find the midpoint position of the motif
    #
    #     print '\tScanning genome with PWM ...'
    #     for chrom in sorted(self.spileups):
    #         _print('Chrom: {}'.format(chrom), 2)
    #         for strand in self.spileups[chrom]:
    #             _print('Strand: {}'.format(strand), 3)
    #             if strand == 1:
    #                 self.spileups[chrom][strand] = motifs.scan_pwm(seq=sequence_dict[chrom], pwm=pwm,
    #                                                                score_offset=score_offset)
    #             else:
    #                 self.spileups[chrom][strand] = motifs.scan_pwm(seq=toolbox.rev_complement(sequence_dict[chrom]),
    #                                                                pwm=pwm, score_offset=score_offset)[::-1]
    #     print 'Done in {}'.format(datetime.datetime.now() - start_time)
    #

    def computeCoverage(self):
        self.coverage = self.total_read_length / float(self.genome_size)

    def getFragmentSize(self, replicate_name, fragment_size_search_start=100, fragment_size_search_end=1000,
                        save_plot_fname='', derivative_smoothing_factor=10):

        fragment_length = get_fragment_size_from_file(replicate_name)

        if not fragment_length:
            fragment_length = self.estimateFragmentSize(fragment_size_search_start, fragment_size_search_end,
                                                        save_plot_fname=save_plot_fname,
                                                        derivative_smoothing_factor=derivative_smoothing_factor,
                                                        force_split=self.build in ('monDom5',))

            save_fragment_length(replicate_name, fragment_length)

        self.fragment_size = fragment_length

        return fragment_length

    def estimateFragmentSize(self, fragment_size_search_start=50, fragment_size_search_end=500, save_plot_fname='',
                             derivative_smoothing_factor=10, mem_map_inputs=False,
                             force_split=False):
        """
        Computes the optimal distance to shift each strand toward each other in order to maximize the cross-correlation
        of the two strands.
        :param fragment_size_search_start:
        :param fragment_size_search_end:
        :param save_plot_fname:
        :return:
        """

        start_time = datetime.datetime.now()
        multi_processing_method = MULTI_PROCESSING_METHOD

        print('Estimating fragment size by by cross-correlation of positive and negative strands...')
        total_cc = numpy.zeros(fragment_size_search_end - fragment_size_search_start)
        total_cc_counter = numpy.zeros(len(
            total_cc))  # track the number of contributing chromosomes at each position in the vector so later we can take the mean

        print('Generating list of chromosomes to process...')

        param_list = []
        for chrom in sorted(list(self.spileups.keys()), key=lambda x: len(self.spileups[x][-1]), reverse=True):
            # divide each chromosome into roughly-evenly-sized chunks as needed to get around the maximum parameter
            # size limitation of the multiprocessing module.
            num_chunks_needed = int(math.ceil(len(self.spileups[chrom][1]) / float(MAX_MESSAGE_SIZE / 2)))
            if multi_processing_method == 'pool' or multi_processing_method == 'hybrid' or force_split:
                dbg_print(
                    '\tSplitting chromosome {} of size {} into {} chunks...'.format(chrom, len(self.spileups[chrom][1]),
                                                                                    num_chunks_needed))
            else:
                dbg_print('\tPreparing chromosome {} of size {}...'.format(chrom, len(self.spileups[chrom][1])))

            # Note that if the fftconvolve method is later called with mode='same', it is the second argument whose sequence
            # should be reversed otherwise the size and midpoint calculations are thrown off.

            if (
                                multi_processing_method == 'pool' or multi_processing_method == 'hybrid' or force_split) and num_chunks_needed > 1:
                neg_strand_chunks = toolbox.flexible_split(self.spileups[chrom][-1],
                                                           num_chunks_needed)
                pos_strand_chunks = toolbox.flexible_split(self.spileups[chrom][1],
                                                           num_chunks_needed)
            else:
                neg_strand_chunks = [self.spileups[chrom][-1]]
                pos_strand_chunks = [self.spileups[chrom][1]]

            mem_mapped_file_counter = 0
            for chunk_idx in range(len(neg_strand_chunks)):
                if mem_map_inputs and mem_mapped_file_counter < MAX_FILEHANDLES_PER_PILEUP:
                    neg_chunk = toolbox.replace_with_mem_map(neg_strand_chunks[chunk_idx], tmp_dir=LOCAL_TMP_DIR)
                    pos_chunk = toolbox.replace_with_mem_map(pos_strand_chunks[chunk_idx], tmp_dir=LOCAL_TMP_DIR)
                    mem_mapped_file_counter += 2
                else:
                    neg_chunk = neg_strand_chunks[chunk_idx]
                    pos_chunk = pos_strand_chunks[chunk_idx]
                param_list.append((chrom, chunk_idx, (neg_chunk, pos_chunk)))
                del neg_chunk
                del pos_chunk
            del neg_strand_chunks
            del pos_strand_chunks

        dbg_print('Sorting chunks in descending order of size...')
        param_list.sort(key=lambda x: len(x[2][-1]), reverse=True)

        if multi_processing_method == 'antfarm':
            print(('Spawning up to {} sub-processes (using AntFarm) to process {} chromosomes in {} chunks'.format(
                THREADS,
                len(self.spileups),
                len(param_list))))

            # convert parameter list to job dictionary to feed to AntFarm
            job_dict = collections.OrderedDict()
            for paramset in param_list:
                job_dict['{}_{}'.format(paramset[0], paramset[1])] = {'inputs': (paramset[2][0], paramset[2][1]),
                                                                      'num_outputs': 1,
                                                                      'params': (paramset[0], paramset[1])}

            del param_list

            cross_correlate_farm = antfarm.AntFarm(slave_script=toolbox.home_path(
                'workspace/expression_modeling/model/pileup_cross_correlate_chromslave.py'),
                                                   base_path=LOCAL_TMP_DIR,
                                                   job_dict=job_dict, max_threads=THREADS, debug=False)
            results = cross_correlate_farm.execute()

            del job_dict

            # print 'results:{}'.format(results)

            for job_name in results:
                cc = results[job_name][0]
                # print '\t{} {}'.format(job_name, len(cc))
                midpoint = len(cc) / 2
                cc_end = min(midpoint + (fragment_size_search_end - fragment_size_search_start), len(cc))
                total_cc_end = cc_end - midpoint
                # print 'midpoint {}, cc_end {}, total_cc_end {}'.format(midpoint, cc_end, total_cc_end)
                # print 'len cc {} len total_cc {}'.format(len(cc), len(total_cc))
                total_cc[:total_cc_end] += cc[midpoint:cc_end]
                total_cc_counter[:total_cc_end] += 1

        elif multi_processing_method == 'pool' or multi_processing_method == 'hybrid' or multi_processing_method == 'none':
            if multi_processing_method == 'pool':
                print((
                'Spawning up to {} sub-processes (using multiprocessing.Pool) to cross-correlate {} chromosomes in {} chunks'.format(
                    THREADS,
                    len(self.spileups),
                    len(param_list))))

                with contextlib.closing(multiprocessing.Pool(THREADS)) as p:
                    results = p.imap(cross_correlate_chromslave, param_list)

            elif multi_processing_method == 'none':
                print(('Processing {} chromosomes in {} chunks with a single process...'.format(len(self.spileups),
                                                                                                len(param_list))))
            results = list(map(cross_correlate_chromslave, param_list))

            del param_list

            for chrom, chunk_idx, cc in results:
                midpoint = len(cc) / 2
                cc_end = min(midpoint + (fragment_size_search_end - fragment_size_search_start), len(cc))
                total_cc_end = cc_end - midpoint
                total_cc[:total_cc_end] += cc[midpoint:cc_end]
                total_cc_counter[:total_cc_end] += 1


        else:
            raise ValueError(
                'Received invalid value {} for parameter <multi_processing_method> in StrandedPileups.estimateFragmentSize()'.format(
                    multi_processing_method))

        # remove zero positions and take the mean of all contributions to each locus
        total_cc_nz = numpy.nonzero(total_cc_counter)
        total_cc = total_cc[total_cc_nz] / total_cc_counter[total_cc_nz]

        print(('Looking for cross-correlation peaks from {} to {} bp'.format(fragment_size_search_start,
                                                                             fragment_size_search_end)))

        print('\tCalculating first derivative by finite difference...')
        der1 = toolbox.finite_difference(total_cc)
        print('\tSmoothing derivative...')
        smoothed_der1 = scipy.ndimage.gaussian_filter1d(der1, derivative_smoothing_factor)
        print('\tFinding downward 0-crossings...')
        crossings = [c + fragment_size_search_start + 1 for c in
                     toolbox.find_0_crossings(smoothed_der1, 1, rising_falling='falling')]
        print(('\tCandidate fragment lengths: {}'.format(', '.join([str(c) for c in crossings]))))

        fragment_size = crossings[0]
        # full_shift = crossings[0] + strand_shift_window_start
        # full_shift = numpy.argmax(total_cc) + strand_shift_window_start
        half_shift = int(fragment_size / 2)
        print(('Estimated fragment size: {}, strand shift: {}'.format(fragment_size, half_shift)))

        if save_plot_fname:
            print(('Saving cross-correlation plot as {}'.format(save_plot_fname)))
            # print '\tshape of cross-correlation vector: {}'.format(total_cc.shape)
            myplots.plot_cc(start=fragment_size_search_start,
                            signal=total_cc[:min(fragment_size_search_end, len(total_cc))], peak_locations=crossings,
                            fname=save_plot_fname)
        print(('Done in {}'.format(datetime.datetime.now() - start_time)))

        return fragment_size

    def readStartsToSoftMask(self, read_length, fragment_length):
        """
        Assuming this object contains read start sites, return a soft mask whereby each strand consists of
        the proportion of putative fragment starts (within <fragment_length> upstream) are alignable.

        Note: this flavor of soft masking is designed for the fragment extension method. Soft masking with read shifting
         is currently not supported.

        Since this object is assumed to contain only the start sites of positive-strand fragments, we will need to shift
        everything over by <read_length> in order to simulate the ends of negative-strand fragments.

        <multi_processing_method> defines which approach to multi-processing to use:
            "antfarm": use the AntFarm paradigm
            "pool": use multiprocessing.Pool
            "none": only use a single process -- no multi-processing

        """
        start_time = datetime.datetime.now()
        multi_processing_method = MULTI_PROCESSING_METHOD

        new_pileups = self.emptyCopy()
        new_pileups.name = self.name + '_extended_to_{}_bp'.format(fragment_length)

        print((
        'Generating double-stranded soft mask from vector of positive-strand read start sites using fragment length {} and read length {}...'.format(
            fragment_length, read_length)))

        param_list = [(chrom, self.spileups[chrom][1], read_length, fragment_length) for chrom in
                      sorted(list(self.spileups.keys()), key=lambda x: self.chrom_lengths[x],
                             reverse=True)]  # process largest chromosomes first

        if multi_processing_method == 'hybrid':
            # convert parameter list to job dictionary to feed to AntFarm
            job_dict = collections.OrderedDict()
            new_param_list = []
            for paramset in param_list:
                if len(paramset[1]) > MAX_MESSAGE_SIZE:
                    job_dict[paramset[0]] = {'inputs': [paramset[1]], 'num_outputs': 2,
                                             'params': [paramset[2], paramset[3]]}
                else:
                    new_param_list.append(paramset)
            param_list = new_param_list
        elif multi_processing_method == 'antfarm':
            # convert parameter list to job dictionary to feed to AntFarm
            job_dict = collections.OrderedDict()
            for paramset in param_list:
                job_dict[paramset[0]] = {'inputs': [paramset[1]], 'num_outputs': 2,
                                         'params': [paramset[2], paramset[3]]}

        if multi_processing_method == 'antfarm' or multi_processing_method == 'hybrid':
            print('Spawning up to {} subprocesses (using AntFarm) to soft mask {} chromosomes...'.format(THREADS, len(
                job_dict)))

            soft_mask_farm = antfarm.AntFarm(
                slave_script=toolbox.home_path('workspace/expression_modeling/model/pileup_soft_mask_chromslave.py'),
                base_path=LOCAL_TMP_DIR,
                job_dict=job_dict, max_threads=THREADS, debug=False)
            results = soft_mask_farm.execute()
            for chrom in results:
                new_pileups.spileups[chrom] = {-1: results[chrom][0].astype(self.pileup_dtype),
                                               1: results[chrom][1].astype(self.pileup_dtype)}

        if multi_processing_method == 'pool' or multi_processing_method == 'none' or multi_processing_method == 'hybrid':
            if multi_processing_method == 'pool' or multi_processing_method == 'hybrid':
                print(
                    ('Spawning up to {} subprocesses (using multiprocessing.Pool) to process {} chromosomes...'.format(
                        THREADS, len(param_list))))

                with contextlib.closing(multiprocessing.Pool(THREADS)) as p:
                    results = p.imap(soft_mask_generate_chromslave, param_list)

            elif multi_processing_method == 'none':
                print(('Processing {} chromosomes with a single process...'.format(len(self.spileups))))
                results = list(map(soft_mask_generate_chromslave, param_list))

            for chrom, soft_mask in results:
                new_pileups.spileups[chrom] = {-1: soft_mask[0], 1: soft_mask[1]}

        print('Done converting read starts to soft mask in {}'.format(datetime.datetime.now() - start_time))
        return new_pileups

    def applySoftMask(self, soft_mask):
        """
        Just divides the contents by the values in <soft_mask>, ignoring positions with a 0 value in <soft_mask>
        """
        start_time = datetime.datetime.now()
        print(('Applying soft mask {} to {}'.format(soft_mask.name, self.name)))
        for chrom in sorted(self.spileups, key=lambda x: self.chrom_lengths[x], reverse=True):
            dbg_print('Processing chromosome {}...'.format(chrom), 1)
            for strand in self.spileups[chrom]:
                if numpy.abs(self.spileups[chrom][strand]).sum() > 0:
                    maskable_strand = numpy.ma.array(
                        self.spileups[chrom][strand].astype(numpy.float64))  # prevent divide by 0 (divide by 0 -> 0)
                    maskable_strand /= soft_mask.spileups[chrom][strand].astype(numpy.float64)
                    self.spileups[chrom][strand] = maskable_strand.filled(0).astype(self.pileup_dtype)
                else:
                    dbg_print('\tChromosome {}, strand {} was empty so not processed.'.format(chrom, strand))
        print(('Done in {}'.format(datetime.datetime.now() - start_time)))

    def fragExtend(self, fragment_length):
        """
        Assuming contents represent counts of read start sites, extend each start site by <extend> bp downstream on each strand.

        :param extend:
        :return:
        """
        multi_processing_method = MULTI_PROCESSING_METHOD
        new_pileups = self.emptyCopy()
        new_pileups.name = '{}_extended_to_{}bp'.format(self.name, fragment_length)

        start_time = datetime.datetime.now()

        print(('Extending read start sites in {} by {} bp...'.format(self.name, fragment_length - 1)))

        param_list = [(chrom, (self.spileups[chrom][-1], self.spileups[chrom][1]), fragment_length) for chrom in
                      # note extension is fragment size -1 since we already have the start site
                      sorted(list(self.spileups.keys()), key=lambda x: self.chrom_lengths[x], reverse=True)]

        if multi_processing_method == 'hybrid':
            # convert parameter list to job dictionary to feed to AntFarm consisting only of chromosomes too large
            # to use in Pool
            job_dict = collections.OrderedDict()
            new_param_list = []
            for paramset in param_list:
                if len(paramset[1][0]) > MAX_MESSAGE_SIZE:
                    job_dict[paramset[0]] = {'inputs': [paramset[1][0], paramset[1][1]], 'num_outputs': 2,
                                             'params': [paramset[2]]}
                else:
                    new_param_list.append(paramset)
            param_list = new_param_list

        elif multi_processing_method == 'antfarm':
            # convert parameter list to job dictionary to feed to AntFarm
            job_dict = collections.OrderedDict()

            for paramset in param_list:
                job_dict[paramset[0]] = {'inputs': [paramset[1][0], paramset[1][1]], 'num_outputs': 2,
                                         'params': [paramset[2]]}
            del param_list

        if multi_processing_method == 'antfarm' or multi_processing_method == 'hybrid':
            print(('Spawning up to {} subprocesses (using AntFarm) to process {} chromosomes...'.format(THREADS, len(
                job_dict))))

            frag_extend_farm = antfarm.AntFarm(
                slave_script=toolbox.home_path('workspace/expression_modeling/model/pileup_frag_extend_chromslave.py'),
                base_path=LOCAL_TMP_DIR,
                job_dict=job_dict, max_threads=THREADS, debug=False)
            results = frag_extend_farm.execute()
            del job_dict

            for chrom in results:
                new_pileups.spileups[chrom] = {-1: results[chrom][0].astype(self.pileup_dtype),
                                               1: results[chrom][1].astype(self.pileup_dtype)}

        if multi_processing_method == 'pool' or multi_processing_method == 'none' or multi_processing_method == 'hybrid':
            if multi_processing_method == 'pool' or multi_processing_method == 'hybrid':
                print(
                    ('Spawning up to {} subprocesses (using multiprocessing.Pool) to process {} chromosomes...'.format(
                        THREADS, len(param_list))))

                with contextlib.closing(multiprocessing.Pool(THREADS)) as p:
                    results = p.imap(frag_extend_chromslave, param_list)

            elif multi_processing_method == 'none':
                print(('Processing {} chromosomes with a single process...'.format(len(self.spileups))))
                results = list(map(frag_extend_chromslave, param_list))

            for chrom, extended_fragments in results:
                new_pileups.spileups[chrom] = {-1: extended_fragments[0], 1: extended_fragments[1]}

        # else:
        #    raise ValueError(
        #        'Received invalid value {} for parameter <multi_processing_method> in StrandedPileups.fragExtend()'.format(
        #            multi_processing_method))

        print(('All done in {}.'.format(datetime.datetime.now() - start_time)))
        return new_pileups

    def liftoverWithChain(self, source_pileups, chain_basepath, chain_type='normal', destination_dtype=None):
        """
        Uses <chain_file> to liftover the contents of <source_pileups> to itself.
        Chain files are named <Reference>To<Query>
        """
        start_time = datetime.datetime.now()

        if not destination_dtype:
            destination_dtype = self.pileup_dtype

        header_fields = (
            'dummy', 'score', 'tName', 'tSize', 'tStrand', 'tStart', 'tEnd', 'qName', 'qSize', 'qStrand', 'qStart',
            'qEnd',
            'id')

        # generate chain filename
        if chain_type == 'rbest':  # use the reciprocal best chain (filtered to one-to-one AKA single coverage in both directions. See http://genomewiki.ucsc.edu/index.php/HowTo:_Syntenic_Net_or_Reciprocal_Best
            chain_filename = os.path.join(chain_basepath,
                                          '{}.{}.rbest.chain'.format(toolbox.first_lower(self.build),
                                                                     toolbox.first_lower(source_pileups.build)))
        else:  # otherwise use normal chain file (single coverage only in target)
            chain_filename = os.path.join(chain_basepath,
                                          '{}To{}.over.chain'.format(toolbox.first_lower(self.build),
                                                                     toolbox.first_upper(source_pileups.build)))

        missing_chroms = set([])

        print(('Lifting over from {} using chain file {}'.format(source_pileups.name, chain_filename)))

        with open(chain_filename, 'rt') as chain_file:

            self._initialize(pileup_dtype=destination_dtype)

            new_chain = True
            good_chain = False

            for line_num, line in enumerate(chain_file):
                if line_num % REPORTING_INTERVAL == 0:
                    dbg_print('Processing line {}'.format(line_num), 1)

                    # new chain
                    if new_chain and line != '\n':  # insurance against multiple blank lines
                        header = toolbox.parse_line_dict(line, header_fields, split_char=' ', strict=True)
                        assert header['dummy'] == 'chain'
                        new_chain = False
                        # relative offsets within the chain
                        ref_chain_pos = 0
                        query_chain_pos = 0

                        ref_chrom = toolbox.convert_chroms(header['tName'], dest=source_pileups.chromosome_dialect)
                        query_chrom = toolbox.convert_chroms(header['qName'], dest=self.chromosome_dialect)

                        good_chain = False
                        if ref_chrom in self.pileups:
                            try:
                                assert int(header['tSize']) == len(self.pileups[ref_chrom])
                            except AssertionError as ae:
                                print((
                                'Error on line {}, chain {}. Chain file size of {} for reference chromosome {} does not match our size of {}'.format(
                                    line_num, header['id'], header['tSize'], ref_chrom,
                                    len(self.pileups[ref_chrom]))))
                                raise ae
                            else:
                                if query_chrom in source_pileups.pileups:
                                    try:
                                        assert int(header['qSize']) == len(source_pileups.pileups[query_chrom])
                                    except AssertionError as ae:
                                        print((
                                        'Error on line {}, chain {}. Chain file size of {} for query chromosome {} does not match source size of {}'.format(
                                            line_num, header['id'], header['qSize'], query_chrom,
                                            len(self.pileups[query_chrom]))))
                                        raise ae
                                    else:
                                        good_chain = True

                        else:
                            missing_chroms.add(ref_chrom)

                        ref_chain_start = int(header['tStart'])
                        query_chain_start = int(header['qStart'])

                    elif line == '\n':
                        # start a new chain on the next line
                        new_chain = True

                    elif good_chain:
                        # it must be a data line
                        split_line = line.split('\t')
                        size = int(split_line[0])

                        if len(split_line) == 3:
                            ref_diff = int(split_line[1])
                            query_diff = int(split_line[2])
                        elif len(split_line) == 1:
                            ref_diff = 0
                            query_diff = 0
                        else:
                            raise Exception(
                                'Encountered a chain alignment data line of length 2 on line {}. Unsure how to handle this so quitting...'.format(
                                    line_num))

                        ref_start_pos = ref_chain_start + ref_chain_pos
                        ref_end_pos = ref_start_pos + size
                        ref_chain_pos += size + ref_diff

                        query_start_pos = query_chain_start + query_chain_pos
                        query_end_pos = query_start_pos + size
                        query_chain_pos += size + query_diff

                        for strand in (-1, 1):
                            self.spileups[ref_chrom][strand][ref_start_pos:ref_end_pos] = \
                                source_pileups.spileups[query_chrom][strand][
                                query_start_pos:query_end_pos]

        print(('Done in {}.'.format(datetime.datetime.now() - start_time)))
        if missing_chroms:
            print(('The following chromosomes in the chain file were missing in the destination organism: {}'.format(
                ','.join(sorted(list(missing_chroms))))))

    def liftoverWithMappingTable(self, destination_build, destination_chrom_lengths, mapping_table_filename):
        """
        Use <mapping_table_filename> to liftover the pileup vectors in <self>
        and return it as a new pileup object.

        :return:
        """
        CHROM_FIELD = 0
        DESTINATION_FRAG_START = 4
        DESTINATION_INSERTION = 5
        DESTINATION_FRAG_END = 6
        SOURCE_FRAG_START = 8
        SOURCE_INSERTION = 9
        SOURCE_FRAG_END = 10

        with open(mapping_table_filename, 'rt') as mapping_table:
            print(('Lifting over reads to {} using {}...'.format(destination_build, mapping_table_filename)))

            lifted_pileups = StrandedPileups(chrom_lengths=destination_chrom_lengths, name=self.name,
                                             build=destination_build,
                                             chromosome_dialect='ensembl')
            # lifted_pileups._initialize(0)

            table_reader = csv.reader(mapping_table, dialect=csv.excel_tab)
            for line_num, line in enumerate(table_reader):
                # remember mapping table is 1-based
                if line_num % 100000 == 0:
                    dbg_print('Reading line {}'.format(line_num), 1)
                if line[SOURCE_FRAG_START] != line[SOURCE_FRAG_END]:
                    # print line
                    chrom = toolbox.convert_chroms(line[CHROM_FIELD], dest=self.chromosome_dialect)

                    if chrom not in self.spileups:
                        # break
                        raise Exception('Found chromosome {} in mapping table but no record of it in {}.'.format(chrom,
                                                                                                                 self.build))
                    if chrom not in lifted_pileups.spileups:
                        # break
                        raise Exception('Found chromosome {} in mapping table but no record of it in {}.'.format(chrom,
                                                                                                                 destination_build))

                    dest_frag_start = int(line[DESTINATION_FRAG_START]) - 1
                    dest_frag_end = int(line[DESTINATION_FRAG_END]) + 1
                    source_frag_start = int(line[SOURCE_FRAG_START]) - 1
                    source_frag_end = int(line[SOURCE_FRAG_END]) + 1

                    if line[DESTINATION_INSERTION] == r'\N' and line[SOURCE_INSERTION] == r'\N':
                        if source_frag_end - source_frag_start != dest_frag_end - dest_frag_start:
                            raise Exception(
                                'Source ({} bp) and destination ({} bp) fragments not the same size on line {}'.format(
                                    source_frag_end - source_frag_start, dest_frag_end - dest_frag_start, line_num))
                        else:
                            try:
                                for strand in (-1, 1):
                                    lifted_pileups.spileups[chrom][strand][dest_frag_start:dest_frag_end] = \
                                        self.spileups[chrom][strand][
                                        source_frag_start:source_frag_end]
                            except ValueError as ve:
                                print((
                                'Despite checking for this, somehow unequal fragment sizes have slipped through on line {}. Source: {} {} {}, destination: {} {} {}'.format(
                                    line_num, source_frag_start, source_frag_end, source_frag_end - source_frag_start,
                                    dest_frag_start, dest_frag_end, dest_frag_end - dest_frag_start)))
                                print(('chrom: {}'.format(chrom)))
                                print(('source chromosome size: {}'.format(self.spileups[chrom][1].shape)))
                                print(
                                    ('destination chromosome size: {}'.format(lifted_pileups.spileups[chrom][1].shape)))
                                raise ve
        return lifted_pileups

    def mixDown(self, strand_shift=0, extend=0):
        """
        Convert to a standard (unstranded) pileup object using a specified <strand_shift> corresponding
        to half the fragment size.

        If <extend> is non-zero, extend each the signal in the 3' direction by the given amount

        Currently do not support combining <strand_shift> and <extend>

        """
        if strand_shift and extend:
            raise Exception(
                'Using <strand shift> and <extend> at the same time currently not supported (\"Why would you have the stereo and the T.V. on at the same time?\")')

        start_time = datetime.datetime.now()
        if extend:
            print(('Mixing down stranded pileups {} to unstranded using fragment extension of {} bp'.format(self.name,
                                                                                                            extend)))
        else:
            print(('Mixing down stranded pileups {} to unstranded using strand shift of {} bp'.format(self.name,
                                                                                                      strand_shift)))

        new_pileups = self.singleStrandedEmptyCopy()

        for chrom in sorted(self.chrom_lengths, key=lambda x: self.chrom_lengths[x], reverse=True):
            new_pileups.pileups[chrom] = numpy.zeros(self.chrom_lengths[chrom], dtype=numpy.float64)
            dbg_print('Processing chromosome {}...'.format(chrom), 1)
            if numpy.sum(numpy.abs(self.spileups[chrom][-1])) + numpy.sum(numpy.abs(self.spileups[chrom][1])) == 0:
                dbg_print('No data in chromosome {}, skipping...'.format(chrom), 1)
            else:

                for strand in self.spileups[chrom]:
                    # print '\tStrand: {}'.format(strand)
                    current_strand = self.spileups[chrom][strand].astype(numpy.float64)
                    if extend:
                        new_pileups.pileups[chrom] += current_strand
                        for i in range(1, extend + 1):
                            # print '\t\tExtension: {}'.format(i)
                            if strand == 1:
                                new_pileups.pileups[chrom][i:] += current_strand[:-i]
                            else:
                                new_pileups.pileups[chrom][:-i] += current_strand[i:]
                    else:
                        effective_strand_shift = strand * strand_shift
                        # print 'strand: {}, effective shift: {}'.format(strand, effective_strand_shift)
                        if effective_strand_shift > 0:
                            new_pileups.pileups[chrom][effective_strand_shift:] += current_strand[
                                                                                   :-effective_strand_shift]
                        elif effective_strand_shift < 0:
                            new_pileups.pileups[chrom][:effective_strand_shift] += current_strand[
                                                                                   - effective_strand_shift:]
                        else:
                            new_pileups.pileups[chrom] += current_strand

        new_pileups.toType(new_pileups.pileup_dtype)

        print(('Done in {}'.format(datetime.datetime.now() - start_time)))
        # print 'current chromosomes: {}'.format(new_pileups.pileups.keys())

        return new_pileups

    def combineStrands(self, binary_func):
        """
        Return a new single-stranded pileup resulting from the application of <binary_func> to both strands of self.
        :param binary_func:
        :return:
        """
        output = self.singleStrandedEmptyCopy()
        for chrom in self.spileups:
            output.pileups[chrom] = binary_func(self.spileups[chrom][-1], self.spileups[chrom][1])
        return output

    def bindingEnergyToProbability(self, mu, nans_to_zeros=True, pileup_dtype=PILEUP_DTYPE):
        """
        Assumes we contain stranded binding energy data. Returns a stranded pileup of binding probabilities for each strand
        given the energies and concentration parameter mu. NaNs will have a probability of 0.
        :return:
        """
        print('Converting binding energy to probabilities...')
        if nans_to_zeros:
            print('NaNs -> zero probability')
        else:
            print('NaNs will be retained')
        binding_probs = self.emptyCopy()
        self.name += '_binding_probability'
        binding_probs.spileups = {}

        for chrom in self.spileups:
            binding_probs.spileups[chrom] = {}
            for strand in self.spileups[chrom]:
                binding_probs.spileups[chrom][strand] = motifs.binding_probabilities(
                    self.spileups[chrom][strand].astype(numpy.float64), mu)

                if nans_to_zeros:
                    binding_probs.spileups[chrom][strand] = numpy.nan_to_num(binding_probs.spileups[chrom][strand])
                if pileup_dtype != type(binding_probs.spileups[chrom][strand]):
                    binding_probs.spileups[chrom][strand] = binding_probs.spileups[chrom][strand].astype(pileup_dtype)
        return binding_probs

    def copy(self, dtype=numpy.float64):
        """
        Alias for deepCopy()
        :param dtype:
        :return:
        """
        return self.deepCopy()

    def deepCopy(self, dtype=numpy.float64):
        """
        Returns a new pileups object containing the same data (a deep copy) with an optional change of datatype.
        :param other:
        :return:
        """
        new_pu = self.emptyCopy()
        for chrom in self.spileups:
            new_pu.spileups[chrom] = {}
            for strand in self.spileups[chrom]:
                new_pu.spileups[chrom][strand] = self.spileups[chrom][strand].astype(dtype)
        return new_pu

    def shallowCopy(self):
        new_pu = self.emptyCopy()
        for chrom in self.spileups:
            new_pu.spileups[chrom] = {}
            for strand in self.spileups[chrom]:
                new_pu.spileups[chrom][strand] = self.spileups[chrom][strand]
        return new_pu

    def emptyCopy(self):
        """
        Returns a new pileups object containing the same meta-data but with no pileups data
        :return:
        """
        new_pu = StrandedPileups(self.chrom_lengths, name=self.name, build=self.build,
                                 chromosome_dialect=self.chromosome_dialect)
        new_pu.spileups = {}
        new_pu.is_normalized = self.is_normalized
        # new_pu.genome_size = self.genome_size
        new_pu.coverage = self.coverage
        new_pu.total_reads = self.total_reads
        new_pu.mean_read_length = self.mean_read_length
        new_pu.mode_read_length = self.mode_read_length
        new_pu.pileup_dtype = self.pileup_dtype
        new_pu.fragment_size = self.fragment_size
        return new_pu

    def singleStrandedEmptyCopy(self):
        """
        Returns a new single-stranded Pileups object containing the same meta-data and no data
        :return:
        """
        new_pileups = Pileups(chrom_lengths=self.chrom_lengths, name=self.name, build=self.build,
                              chromosome_dialect=self.chromosome_dialect)

        new_pileups.input_filename = self.input_filename

        new_pileups.coverage = self.coverage
        new_pileups.total_reads = self.total_reads

        new_pileups.is_normalized = False
        new_pileups.total_read_length = self.total_read_length
        new_pileups.mean_read_length = self.mean_read_length
        new_pileups.mode_read_length = self.mode_read_length
        new_pileups.pileup_dtype = self.pileup_dtype
        new_pileups.fragment_size = self.fragment_size
        new_pileups.pileups = {}
        return new_pileups

    def save(self, folder_path, gzipped=True):
        print('Saving stranded pileup data to {} ...'.format(folder_path))
        toolbox.establish_path(folder_path)

        for chrom in toolbox.numerical_string_sort(self.chrom_lengths):
            for strand in self.spileups[chrom]:
                print('\tSaving chromosome {} strand {}'.format(chrom, strand))
                if gzipped:
                    with gzip.open(os.path.join(folder_path, '{}_{}.npy.gz'.format(chrom, strand)),
                                   'wb') as strand_file:
                        numpy.save(strand_file, self.spileups[chrom][strand])
                else:
                    numpy.save(os.path.join(folder_path, '{}_{}.npy'.format(chrom, strand)),
                               self.spileups[chrom][strand])

        with open(os.path.join(folder_path, 'meta_data.txt'), 'w') as out_file:
            META_DATA_VARS = (self.name, self.build, self.chromosome_dialect, self.is_normalized)
            out_file.write(','.join(str(v) for v in META_DATA_VARS))

    @classmethod
    def load(cls, folder_path, mmap_mode=''):
        overall_load_start_time = datetime.datetime.now()
        loaded_pileup = cls()
        print('Loading pileup data from {} ...'.format(folder_path))
        
        if mmap_mode:
            print(
                'Loading up to {} chromosomes in mem-mapped mode {} ...'.format(MAX_FILEHANDLES_PER_PILEUP, mmap_mode))

        with open(os.path.join(folder_path, 'meta_data.txt'), 'rt') as meta_data_file:

            meta_data = meta_data_file.read().strip().split(',')
            loaded_pileup.name = str(meta_data[0])
            loaded_pileup.build = str(meta_data[1])
            loaded_pileup.chromosome_dialect = str(meta_data[2])
            loaded_pileup.is_normalized = {'True': True, 'False': False}[meta_data[3]]

        mem_mapped_chrom_count = 0
        
        # sort the chromosomes in order of descending size (so that we mem-map the biggest first)
        # array_fnames = sorted(os.listdir(folder_path), reverse=True, key=lambda x: loaded_pileup.chrom_lengths[toolbox.parse_path(x)[1].split('_')[0]])
        
        for array_fname in toolbox.numerical_string_sort(os.listdir(folder_path)):
            if array_fname.endswith('.npy'):
                start_time = datetime.datetime.now()
                chrom, strand = toolbox.parse_path(array_fname)[1].split('_')
                strand = int(strand)
                if chrom not in loaded_pileup.spileups:
                    loaded_pileup.spileups[chrom] = {}
                if mmap_mode and mem_mapped_chrom_count < MAX_FILEHANDLES_PER_PILEUP:
                    print('\tLoading chromosome {} strand {} mem-mapped ...'.format(chrom, strand))
                    loaded_pileup.spileups[chrom][strand] = numpy.load(os.path.join(folder_path, array_fname),
                                                              mmap_mode=mmap_mode)
                    mem_mapped_chrom_count += 1
                else:
                    print('\tLoading chromosome {} strand {} ...'.format(chrom, strand))
                    loaded_pileup.spileups[chrom][strand] = numpy.load(os.path.join(folder_path, array_fname))

                loaded_pileup.chrom_lengths[chrom] = len(loaded_pileup.spileups[chrom][strand])

            elif array_fname.endswith('.npy.gz'):
                start_time = datetime.datetime.now()
                chrom, strand = array_fname.split('.')[0].split('_')
                strand = int(strand)
                if chrom not in loaded_pileup.spileups:
                    loaded_pileup.spileups[chrom] = {}

                print('\tLoading chromosome {} strand {} ...'.format(chrom, strand))
                with gzip.open(os.path.join(folder_path, array_fname), 'rb') as strand_file:
                    loaded_pileup.spileups[chrom][strand] = numpy.load(strand_file)
                loaded_pileup.chrom_lengths[chrom] = len(loaded_pileup.spileups[chrom][strand])
                print('\tDone loading in {}'.format(datetime.datetime.now() - start_time))

        loaded_pileup.pileup_dtype = list(list(loaded_pileup.spileups.values())[0].values())[0].dtype
        # loaded_pileup.genome_size = sum(loaded_pileup.chrom_lengths.values())
        print('Done loading {} from files in {}'.format(loaded_pileup.name, datetime.datetime.now() - overall_load_start_time))

    def flatten(self):
        """
        Returns a flat vector consisting of the negative strands of all chromosomes concatenated in alpha order followed
        by the positive strands concatenated in alpha chromosome order
        :return:
        """
        flat_vector = numpy.zeros(
            sum([len(s[-1]) for s in list(self.spileups.values())]) + sum(
                [len(s[1]) for s in list(self.spileups.values())]))
        offset = 0
        for strand in (-1, 1):
            for chrom in self.spileups:
                l = len(self.spileups[chrom][strand])
                flat_vector[offset:offset + l] = self.spileups[chrom][strand]
                offset += l
        return flat_vector

    def trimChromosomes(self, chromosomes_to_include=None, chromosomes_to_exclude=None):
        if not chromosomes_to_include:
            new_chromosomes = set(self.pileups.keys())
        new_chromosomes = new_chromosomes.difference_update(set(chromosomes_to_exclude))
        print('Trimming chromosomes to only include: {}'.format(', '.join(new_chromosomes)))
        for chrom in self.spileups:
            if chrom not in new_chromosomes:
                del self.spileups[chrom]
        for chrom in self.chrom_lengths:
            if chrom not in new_chromosomes:
                del self.chrom_lengths[chrom]

    def apply(self, func):
        for chrom in self.spileups:
            for strand in self.spileups[chrom]:
                self.spileups[chrom][strand] = func(self.spileups[chrom][strand])

    def clip(self, min_value=0, max_value=1):
        """
        Constrains the pileup vectors to be bewtween :param:`min_value` and :param:`max_value`
        by applying the numpy.clip function.
        """
        print('Clipping pileup values to be between {} and {}'.format(min_value, max_value))
        for chrom in self.spileups:
            for strand in self.spileups[chrom]:
                self.spileups[chrom][strand] = numpy.clip(self.spileups[chrom][strand], a_min=min_value, a_max=max_value)            
                

    def smooth(self, gaussian_kernel_bandwidth=45):
        """
        Smooth chromosome vectors with a gaussian kernel of width <gaussian_kernel_bandwidth>
        :param gaussian_kernel_bandwidth:
        :return:
        """
        for chrom in self.spileups:
            for strand in self.spileups[chrom]:
                self.spileups[chrom][strand] = scipy.ndimage.gaussian_filter1d(
                    self.spileups[chrom][strand].astype(float),
                    sigma=gaussian_kernel_bandwidth)

    def toType(self, pileup_dtype=PILEUP_DTYPE):
        """
        Converts all pileup chromosome vectors to the specified data type
        :param pileup_dtype:
        :return:
        """
        self.pileup_dtype = pileup_dtype
        for chrom in self.spileups:
            for strand in self.spileups[chrom]:
                self.spileups[chrom][strand] = self.spileups[chrom][strand].astype(pileup_dtype)
                

    def astype(self, pileup_dtype=PILEUP_DTYPE):
        """
        Analogous to the numpy.astype() method, returns a new stranded pileup
        with chromosome data in the specified data type.
        
        :param pileup_dtype:
        :return:
        """
        new_pileup = self.emptyCopy()
        new_pileup.pileup_dtype = pileup_dtype
        
        for chrom in self.spileups:
            new_pileup.spileups[chrom] = {}
            for strand in self.spileups[chrom]:
                new_pileup.spileups[chrom][strand] = self.spileups[chrom][strand].astype(pileup_dtype)              
        return new_pileup
                

    def memMap(self, writable=True, tmp_dir=NETWORK_TMP_DIR):
        """
        Converts pileup chromosome vectors to mem_mapped arrays on disk.
        """
        self.save_path = os.path.join(tmp_dir, 'pileup_{}'.format(self.id))

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        max_chroms_to_map = min(len(self.spileups), MAX_FILEHANDLES_PER_PILEUP)

        for chrom in sorted(self.spileups, key=lambda x: len(list(self.spileups[x].values())[0]), reverse=True)[
                     :max_chroms_to_map]:
            for strand in self.spileups[chrom]:
                vector_fname = os.path.join(self.save_path, '{}_{}.npy'.format(chrom, strand))
                numpy.save(vector_fname, self.spileups[chrom][strand])
                self.spileups[chrom][strand] = numpy.load(vector_fname, mmap_mode=('r', 'r+')[writable])

    def oneStrand(self, strand):
        """
        Returns a Pileups object comprised of only the positive (for <strand> = 1) or negative (for <strand> = -1) strands
        """
        # start_time = datetime.datetime.now()

        new_pileups = Pileups(chrom_lengths=self.chrom_lengths, name=self.name, build=self.build,
                              chromosome_dialect=self.chromosome_dialect)

        new_pileups.input_filename = self.input_filename
        # new_pileups.max_height = self.max_height
        new_pileups.coverage = self.coverage
        new_pileups.total_reads = self.total_reads
        # new_pileups.genome_size = self.genome_size
        new_pileups.is_normalized = False
        new_pileups.total_read_length = self.total_read_length
        new_pileups.mean_read_length = self.mean_read_length
        new_pileups.mode_read_length = self.mode_read_length
        new_pileups.pileup_dtype = self.pileup_dtype
        new_pileups.fragment_size = self.fragment_size
        new_pileups.pileups = {}

        for chrom in self.spileups:
            new_pileups.pileups[chrom] = self.spileups[chrom][strand]

        # print 'Done in {}'.format(datetime.datetime.now() - start_time)

        return new_pileups


class Pileups(object):
    """
    Container for a dictionary of chromosome-length vectors, each containing the number of reads covering that location.
    Includes methods for loading from various aligned-read file formats, and for normalizing to coverage
    """

    def __init__(self, chrom_lengths={}, input_filename='', name='', build='', strand_shift=0,
                 pileup_dtype=PILEUP_DTYPE,
                 chromosome_dialect=DEFAULT_CHROMOSOME_DIALECT):
        self.id = toolbox.random_identifier(32)
        self.pileup_dtype = pileup_dtype
        self.save_path = None
        self.chromosome_dialect = chromosome_dialect
        self.chrom_lengths = {}
        for chrom in chrom_lengths:
            translated_chrom = toolbox.convert_chroms(chrom, dest=self.chromosome_dialect)
            self.chrom_lengths[translated_chrom] = chrom_lengths[chrom]

        self.is_normalized = False
        self.name = name.replace(',', '_')
        self.build = build
        self.pileups = {}
        self.read_counts = {}
        self.total_read_length = 0
        self.total_reads = 0
        self.coverage = 0
        self.mean_read_length = 0
        self.mode_read_length = 0
        # self.max_height = -1

        print(('Initialized new pileup object: {}, genome build: {}, chromosome dialect: {}'.format(self.name,
                                                                                                    self.build,
                                                                                                    self.chromosome_dialect)))

        if input_filename:
            self.loadFromBed(input_filename, strand_shift=strand_shift)

    def __del__(self):
        if self.save_path and os.path.exists(self.save_path):
            try:
                shutil.rmtree(self.save_path)
            except (OSError, IOError) as ex:
                print('Tried to delete {} but caught {} instead'.format(self.save_path, ex))

    @property
    def genome_size(self):
        return sum(self.chrom_lengths.values())


    def save(self, folder_path, gzipped=True):
        print('Saving pileup data to {} ...'.format(folder_path))
        toolbox.establish_path(folder_path)

        for chrom in toolbox.numerical_string_sort(self.chrom_lengths):
            print('\tSaving chromosome {}'.format(chrom))
            if gzipped:
                with gzip.open(os.path.join(folder_path, '{}.npy.gz'.format(chrom)), 'wb') as chrom_file:
                    numpy.save(chrom_file, self.pileups[chrom])
            else:
                numpy.save(os.path.join(folder_path, '{}.npy'.format(chrom)), self.pileups[chrom])

        with open(os.path.join(folder_path, 'meta_data.txt'), 'w') as out_file:
            META_DATA_VARS = (self.name, self.build, self.chromosome_dialect, self.is_normalized, self.mode_read_length)
            out_file.write(','.join(str(v) for v in META_DATA_VARS))

    @classmethod
    def load(cls, folder_path, mmap_mode=''):
        """
        Returns a Pileup object loaded from :param:`folder_path`        
        """
        
        loaded_pileup = cls()
    
        overall_load_start_time = datetime.datetime.now()
        print('Loading pileup data from {} ...'.format(folder_path))
        if mmap_mode:
            print('Loading up to {} chromosomes in mem-mapped mode {}'.format(MAX_FILEHANDLES_PER_PILEUP, mmap_mode))
            
        with open(os.path.join(folder_path, 'meta_data.txt'), 'rt') as meta_data_file:
            meta_data = meta_data_file.read().strip().split(',')
            loaded_pileup.name = str(meta_data[0])
            loaded_pileup.build = str(meta_data[1])
            loaded_pileup.chromosome_dialect = str(meta_data[2])
            loaded_pileup.is_normalized = {'True': True, 'False': False}[meta_data[3]]
            loaded_pileup.mode_read_length = int(meta_data[4])

        mem_mapped_chrom_count = 0

        for array_fname in toolbox.numerical_string_sort(os.listdir(folder_path)):
            if array_fname.endswith('.npy'):
                chrom = toolbox.parse_path(array_fname)[1]
                start_time = datetime.datetime.now()
                if mmap_mode and mem_mapped_chrom_count < MAX_FILEHANDLES_PER_PILEUP:
                    print('\tLoading chromosome {} mem-mapped'.format(chrom))
                    loaded_pileup.pileups[chrom] = numpy.load(os.path.join(folder_path, array_fname), mmap_mode=mmap_mode)
                    mem_mapped_chrom_count += 1
                else:
                    print('\tLoading chromosome {}'.format(chrom))
                    loaded_pileup.pileups[chrom] = numpy.load(os.path.join(folder_path, array_fname))

                loaded_pileup.chrom_lengths[chrom] = len(loaded_pileup.pileups[chrom])
                # print '\tDone loading in {}'.format(datetime.datetime.now() - start_time)

            elif array_fname.endswith('.npy.gz'):
                chrom = array_fname.split('.')[0]
                start_time = datetime.datetime.now()
                print('\tLoading chromosome {}'.format(chrom))
                with gzip.open(os.path.join(folder_path, array_fname), 'rb') as chrom_file:
                    loaded_pileup.pileups[chrom] = numpy.load(chrom_file)
                loaded_pileup.chrom_lengths[chrom] = len(loaded_pileup.pileups[chrom])
                # print '\tDone loading in {}'.format(datetime.datetime.now() - start_time)

        loaded_pileup.pileup_dtype = list(loaded_pileup.pileups.values())[0].dtype
        # self.genome_size = sum(loaded_pileup.chrom_lengths.values())
        print('Done loading {} from files in {}'.format(loaded_pileup.name, datetime.datetime.now() - overall_load_start_time))
        return loaded_pileup

    def _initialize(self, pileup_dtype=None, fill_value=None):
        if pileup_dtype:
            self.pileup_dtype = pileup_dtype

        self.pileups = {}
        self.read_counts = {}

        if fill_value == None:
            if self.pileup_dtype == numpy.str:
                fill_value = ''
            else:
                fill_value = 0

        for chrom in self.chrom_lengths:
            self.pileups[chrom] = numpy.full(self.chrom_lengths[chrom], fill_value=fill_value, dtype=self.pileup_dtype)
            self.read_counts[chrom] = 0

        self.is_normalized = False

        self.total_read_length = 0
        self.total_reads = 0
        self.coverage = 0
        self.mean_read_length = 0
        self.mode_read_length = 0
        # self.max_height = -1

    def loadFromFasta(self, fasta_filename, upper_only=True):
        """
        Populates itself with the genome sequence taken from <fasta_filename>. If <upper_only> is set,
        convert all nucleotides to upper-case.
        :param fasta_filename:
        :return:
        """
        start_time = datetime.datetime.now()
        self.dtype = numpy.character
        with open(fasta_filename, 'rt') as fasta_file:
            print('Loading genome sequence from {}...'.format(fasta_filename))
            self.pileups = {}
            for chrom, seq in list(toolbox.parse_fasta_dict(fasta_file.read()).items()):
                translated_chrom = toolbox.convert_chroms(chrom, dest=self.chromosome_dialect)
                self.pileups[translated_chrom] = numpy.array(list((seq, seq.upper())[upper_only]), dtype=self.dtype)
        only_in_fasta = set(self.pileups.keys()).difference(set(self.chrom_lengths.keys()))
        print('Done loading genome in {}'.format(datetime.datetime.now() - start_time))
        if only_in_fasta:
            print(
                'The following chromosomes were present in the FASTA file but not in the length dictionary: {}'.format(
                    ', '.join(list(only_in_fasta))))
        only_in_self = set(self.chrom_lengths.keys()).difference(set(self.pileups.keys()))
        if only_in_self:
            print('The following chromosomes were present in the length dictionarybut not in the FASTA file: {}'.format(
                ', '.join(list(only_in_self))))

    def loadFromBed(self, tagalign_filename, strand_shift=0):
        """
        Populate the pileup vector from a BED file (each genomic position will contains a count of the number of BED regions that overlap it)
        Will shift + strand reads by - <strand_shift> and - strand reads by <strand_shift>.

        If strand_shift is None, compute the strand shift automatically using cross-correlation
        """
        start_time = datetime.datetime.now()
        self._initialize()

        self.input_filename = tagalign_filename

        self.read_length_counts = collections.defaultdict(lambda: 0)
        missing_chroms = set([])

        with open(tagalign_filename, 'rt') as tag_file:
            print('Computing pileup vectors from reads in {}.'.format(tagalign_filename))
            # print 'Chromosome dialect for BED file specified as: \'{}\''.format(reads_chromosome_dialect)
            print('Using strand shift of {}'.format(strand_shift))
            for line_num, line in enumerate(tag_file):
                if line_num % REPORTING_INTERVAL == 0:
                    dbg_print('Reading line {}'.format(line_num), 1)
                split_line = line.strip().split('\t')
                if len(line) > 0:
                    chrom = toolbox.convert_chroms(split_line[0], dest=self.chromosome_dialect)
                    # print split_line
                    if len(split_line) >= 6:
                        strand = {'+': 1, '-': -1}[split_line[5]]
                    else:
                        strand = 0
                    if chrom in self.pileups:
                        self.read_counts[chrom] += 1
                        start_pos = int(split_line[1]) + strand * strand_shift
                        end_pos = int(split_line[2]) - 1 + strand * strand_shift
                        read_length = end_pos - start_pos + 1
                        self.total_read_length += read_length
                        self.read_length_counts[read_length] += 1
                        self.pileups[chrom][start_pos:end_pos] += 1
                    else:
                        if chrom not in missing_chroms:
                            dbg_print('Chromosome {} not found in self!'.format(chrom), 1)
                            missing_chroms.add(chrom)
            self.total_reads = sum(self.read_counts.values())
            if self.total_reads > 0:
                self.mean_read_length = self.total_read_length / float(self.total_reads)
            else:
                self.mean_read_length = 0
            print('Done reading file.')
            if missing_chroms:
                print(
                    '\tThe following chromosomes were present in the bed file but not in the length dictionary: {}'.format(
                        ', '.join(sorted(list(missing_chroms)))))

            self.mode_read_length = max(list(self.read_length_counts.items()), key=lambda x: x[1])[0]

            self.computeCoverage()
        print('Done in {}.'.format(datetime.datetime.now() - start_time))

    def loadFromWig(self, wig_filename, pileup_dtype=PILEUP_DTYPE):
        """
        Populate with the annotated values from a WIG file.
        All chromosomes must be in a single file (since the arrays are initialized
        at the beginning of this method)
        """
        start_time = datetime.datetime.now()
        self._initialize(pileup_dtype=numpy.float64)
        populated_count = 0
        missing_chroms = set([])
        with open(wig_filename, 'rt') as wig_file:
            print('Populating from WIG file {}'.format(wig_filename))
            for line_num, line in enumerate(wig_file):
                if line_num % 1e6 == 0:
                    dbg_print('Reading line {}.'.format(line_num), 1)
                if line != '\n':
                    line = line.strip()
                    split_line = re.split(WHITESPACE, line)

                    if line.startswith('track'):  # it's a track definition line
                        # so ignore it for now
                        pass
                    # declaration lines
                    elif line.startswith('fixedStep'):
                        split_line = line.split(' ')
                        if len(split_line) > 5 or len(split_line) < 4:
                            raise Exception(
                                'Invalid number of fields ({}) on line {}'.format(len(split_line), line_num))

                        field_split = split_line[1].split('=')
                        if field_split[0] != 'chrom':
                            raise Exception('Missing field "chrom" on line {}'.format(line_num))
                        else:
                            chrom = toolbox.convert_chroms(field_split[1], dest=self.chromosome_dialect)

                        field_split = split_line[2].split('=')
                        if field_split[0] != 'start':
                            raise Exception('Missing field "start" on line {}'.format(line_num))
                        else:
                            region_start = int(field_split[1])

                        if len(split_line) >= 4:
                            field_split = split_line[3].split('=')
                            if field_split[0] != 'step':
                                raise Exception('Missing field "step" on line {}'.format(line_num))
                            else:
                                step = int(field_split[1])
                        else:
                            step = 1

                        if len(split_line) == 5:
                            field_split = split_line[4].split('=')
                            if field_split[0] != 'span':
                                raise Exception('Missing field "span" on line {}'.format(line_num))
                            else:
                                span = int(field_split[1])
                        else:
                            span = 1

                        if chrom in self.pileups:  # only process if we have this chromosome
                            region_type = 'fixed'
                            offset = 0
                        else:
                            missing_chroms.add(chrom)
                            region_type = None

                    elif line.startswith('variableStep'):
                        split_line = line.split(' ')
                        if len(split_line) > 3 or len(split_line) < 2:
                            raise Exception(
                                'Invalid number of fields ({}) on line {}'.format(len(split_line), line_num))

                        field_split = split_line[1].split('=')
                        if field_split[0] != 'chrom':
                            raise Exception('Missing field "chrom" on line {}'.format(line_num))
                        else:
                            chrom = toolbox.convert_chroms(field_split[1], dest=self.chromosome_dialect)

                        if len(split_line) == 3:
                            field_split = split_line[2].split('=')
                            if field_split[0] != 'span':
                                raise Exception('Missing field "span" on line {}'.format(line_num))
                            else:
                                span = int(field_split[1])
                        else:
                            span = 1

                        if chrom in self.pileups:  # only process if we have this chromosome
                            region_type = 'variable'
                        else:
                            missing_chroms.add(chrom)
                            region_type = None

                    # data lines
                    elif region_type == 'fixed':
                        if len(split_line) != 1:
                            # print 'split_line:{}'.format(split_line)
                            raise Exception(
                                'Invalid number of elements for fixedStep data on line {}. Expected {}, found {}. Line: {}'.format(
                                    line_num, 1, len(split_line), line.strip()))

                        data_val = float(split_line[0])
                        start_pos = region_start + offset * step
                        end_pos = start_pos + span
                        self.pileups[chrom][start_pos:end_pos] = data_val
                        populated_count += end_pos - start_pos
                        offset += 1
                    elif region_type == 'variable':
                        if len(split_line) != 2:
                            raise Exception(
                                'Invalid number of elements for variableStep data on line {}. Expected {}, found {}. Line: {}'.format(
                                    line_num, 2, len(split_line), line.strip()))
                        start_pos = int(split_line[0])
                        end_pos = start_pos + span
                        data_val = float(split_line[1])
                        self.pileups[chrom][start_pos:end_pos] = data_val
                        populated_count += end_pos - start_pos

        self.toType(pileup_dtype)

        print('Done in {}'.format(datetime.datetime.now() - start_time))
        print('{} data values added, {} of genome (assuming no overlaps)'.format(populated_count,
                                                                                 populated_count / float(
                                                                                     self.genome_size)))
        if missing_chroms:
            print('The following chromosomes in the WIG file were not present in ourself: {}'.format(
                ', '.join(sorted(list(missing_chroms)))))

    def populateFromProbes(self, probe_dict, interpolate=False, chromosome_endpoint_value=0):
        """
        Given a dictionary (keyed by chromosome name) that contains sequences of tuples in the form (position, value),
        such as might be obtained from a tiled microarray experiment, populate self with a continuous vector of values.

        If interpolate is True, positions between probes will be interpolated as a linear transition between probes.
        Otherwise, the between-probe positions will take on the value of the nearest probe.

        :param probe_value_dict:
        :return:
        """
        print('Populating from microarray probes. Interpolation: {}'.format(('OFF', 'ON')[bool(interpolate)]))
        self._initialize()

        for chrom in probe_dict:
            print('\tPopulating chromosome {}'.format(chrom))
            last_pos = chromosome_endpoint_value
            last_value = 0
            for probe_pos, probe_value in list(probe_dict[chrom]) + [(self.chrom_lengths[chrom],
                                                                      chromosome_endpoint_value)]:  # add a dummy probe for the end of the chromosome
                if probe_pos > self.chrom_lengths[chrom]:
                    print((probe_pos, self.chrom_lengths[chrom]))
                assert probe_pos <= self.chrom_lengths[chrom]
                distance = probe_pos - last_pos
                if interpolate:
                    difference = probe_value - last_value
                    # print 'Last_pos: {}, last_value: {}, probe_pos: {}, probe_value: {}, distance: {}, difference: {}'.format(last_pos, last_value, probe_pos, probe_value, distance, difference)

                    for offset in range(distance):
                        self.pileups[chrom][last_pos + offset] = last_value + difference * (offset / float(distance))
                        # print '\t{} {}'.format(offset, self.pileups[chrom][last_pos + offset])
                else:
                    midpoint = last_pos + int((probe_pos - last_pos) / 2)
                    # print last_pos, probe_pos, midpoint
                    self.pileups[chrom][last_pos:midpoint] = last_value
                    self.pileups[chrom][midpoint:probe_pos] = probe_value
                last_pos = probe_pos
                last_value = probe_value

    def computeCoverage(self):
        self.coverage = self.total_read_length / float(self.genome_size)

    def computeNucleotideFrequencies(self):
        """
        Assumes self contains genomic sequences. Computes the frequency of each nucleotide in the genome and returns
        as a dictionary
        :return:
        """
        return motifs.compute_background_distribution(numpy.concatenate(list(self.pileups.values())), normalize=True)

    def normalize(self, new_coverage=1):
        """
        Converts integer pileup counts to normalized values (to average coverage of 1)
        """
        print('Normalizing {}'.format(self.name))
        if not self.is_normalized:
            start_time = datetime.datetime.now()
            print('Coverage currently {}. Normalizing to mean coverage of 1...'.format(self.coverage))
            for chrom in self.pileups:
                # new_pileup = numpy.zeros(self.chrom_lengths[chrom], dtype = float)
                # new_pileup = self.pileups[chrom] / float(self.coverage)
                self.pileups[chrom] *= (new_coverage / float(self.coverage))
                # self.pileups[chrom] = new_pileup
            self.is_normalized = True
            print('Done in {}.'.format(datetime.datetime.now() - start_time))
        else:
            print('\tAlready normalized. Nothing to do.')

    def mean(self, list_of_pileups):
        """
        Populates itself with the mean of all the Pileup objects in <list_of_pileups>
        """
        start_time = datetime.datetime.now()
        print('Calculating the mean of {} pileups'.format(len(list_of_pileups)))
        self._initialize()
        for pileup in list_of_pileups:
            for chrom in self.chrom_lengths:
                assert self.chrom_lengths[chrom] == pileup.chrom_lengths[chrom]

        for chrom in self.chrom_lengths:
            if numpy.product([chrom in pileup.pileups for pileup in
                              list_of_pileups]):  # only process chromosomes present in all datasets
                self.pileups[chrom] = numpy.mean([pileup.pileups[chrom] for pileup in list_of_pileups], axis=0,
                                                 dtype=float)

        # the mean is normalized if all the input datasets are normalized
        self.is_normalized = bool(numpy.product([pileup.is_normalized for pileup in list_of_pileups]))
        print('Done in {}.'.format(datetime.datetime.now() - start_time))

    def var(self, list_of_pileups):
        """
        Populates itself with the variance of all the Pileup objects in <list_of_pileups>
        """
        start_time = datetime.datetime.now()
        print('Calculating the variance of {} pileups'.format(len(list_of_pileups)))
        self._initialize()
        for pileup in list_of_pileups:
            for chrom in self.chrom_lengths:
                assert self.chrom_lengths[chrom] == pileup.chrom_lengths[chrom]

        for chrom in self.chrom_lengths:
            if numpy.product([chrom in pileup.pileups for pileup in
                              list_of_pileups]):  # only process chromosomes present in all datasets
                self.pileups[chrom] = numpy.var([pileup.pileups[chrom] for pileup in list_of_pileups], axis=0,
                                                dtype=float)

        # the variance is normalized if all the input datasets are normalized
        self.is_normalized = bool(numpy.product([pileup.is_normalized for pileup in list_of_pileups]))
        print('Done in {}.'.format(datetime.datetime.now() - start_time))

    def std(self, list_of_pileups):
        """
        Populates itself with the variance of all the Pileup objects in <list_of_pileups>
        """
        start_time = datetime.datetime.now()
        print('Calculating the variance of {} pileups'.format(len(list_of_pileups)))
        self._initialize()
        for pileup in list_of_pileups:
            for chrom in self.chrom_lengths:
                assert self.chrom_lengths[chrom] == pileup.chrom_lengths[chrom]

        for chrom in self.chrom_lengths:
            if numpy.product([chrom in pileup.pileups for pileup in
                              list_of_pileups]):  # only process chromosomes present in all datasets
                self.pileups[chrom] = numpy.std([pileup.pileups[chrom] for pileup in list_of_pileups], axis=0,
                                                dtype=float)

        # the SD is normalized if all the input datasets are normalized
        self.is_normalized = bool(numpy.product([pileup.is_normalized for pileup in list_of_pileups]))
        print('Done in {}.'.format(datetime.datetime.now() - start_time))

    def product(self, list_of_pileups):
        """
        Populates itself with the product of all the Pileup objects in <list_of_pileups>
        """
        start_time = datetime.datetime.now()
        print('Calculating the product of {} pileups'.format(len(list_of_pileups)))
        self._initialize()
        for pileup in list_of_pileups:
            for chrom in self.chrom_lengths:
                assert self.chrom_lengths[chrom] == pileup.chrom_lengths[chrom]

        for chrom in self.chrom_lengths:
            if numpy.product([chrom in pileup.pileups for pileup in
                              list_of_pileups]):  # only process chromosomes present in all datasets
                self.pileups[chrom] = numpy.product([pileup.pileups[chrom] for pileup in list_of_pileups], axis=0,
                                                    dtype=float)

        # the SD is normalized if all the input datasets are normalized
        self.is_normalized = bool(numpy.product([pileup.is_normalized for pileup in list_of_pileups]))
        print('Done in {}.'.format(datetime.datetime.now() - start_time))

    # def sum(self, list_of_pileups):
        # """
        # Populates itself with the sum of all the Pileup objects in <list_of_pileups>
        # """
        # start_time = datetime.datetime.now()
        # print('Calculating the sum of {} pileups'.format(len(list_of_pileups)))
        # self._initialize()
        # for pileup in list_of_pileups:
            # for chrom in self.chrom_lengths:
                # assert self.chrom_lengths[chrom] == pileup.chrom_lengths[chrom]

        # for chrom in self.chrom_lengths:
            # if numpy.product([chrom in pileup.pileups for pileup in
                              # list_of_pileups]):  # only process chromosomes present in all datasets
                # self.pileups[chrom] = numpy.sum([pileup.pileups[chrom] for pileup in list_of_pileups], axis=0,
                                                # dtype=float)

        #the SD is normalized if all the input datasets are normalized
        # self.is_normalized = bool(numpy.product([pileup.is_normalized for pileup in list_of_pileups]))
        # print('Done in {}.'.format(datetime.datetime.now() - start_time))
        
    def sum(self):
        """
        Returns the scalar sum of the contents of all contigs.
        """
        return self.flatten().astype(float).sum()
        

    def flatten(self, chrom_list=[], include_sex=True):
        """
        Return a flat pileup vector by concatenating the individual chromosome vectors (in lexicographical order by chromosome name)
        """
        # start_time = datetime.datetime.now()
        if not chrom_list:
            chrom_list = list(self.pileups.keys())
        if not include_sex:
            chrom_list = [chrom for chrom in chrom_list if
                          not sum([element in chrom for element in ['X', 'Y', 'Z', 'W']])]

        # print 'Flattening...'
        flat_pileup = numpy.concatenate([self.pileups[chrom] for chrom in toolbox.numerical_string_sort(chrom_list)])
        # print 'Done in {}.'.format(datetime.datetime.now() - start_time)
        return flat_pileup
        
    def clip(self, min_value=0, max_value=1):
        """
        Constrains the pileup vectors to be bewtween :param:`min_value` and :param:`max_value`
        by applying the numpy.clip function.
        """
        print('Clipping pileup values to be between {} and {}'.format(min_value, max_value))
        for chrom in self.pileups:
            self.pileups[chrom] = numpy.clip(self.spileups[chrom], a_min=min_value, a_max=max_value)                            

    def smooth(self, gaussian_kernel_bandwidth=45):
        """
        Smooth chromosome vectors with a gaussian kernel of width <gaussian_kernel_bandwidth>
        :param gaussian_kernel_bandwidth:
        :return:
        """
        new_pileups = self.emptyCopy()
        for chrom in self.pileups:
            new_pileups.pileups[chrom] = scipy.ndimage.gaussian_filter1d(self.pileups[chrom].astype(numpy.float64),
                                                                         sigma=gaussian_kernel_bandwidth)
        return new_pileups

    def applyKernel(self, kernel):
        new_pileups = self.emptyCopy()
        for chrom in self.pileups:
            new_pileups.pileups[chrom] = toolbox.apply_kernel(self.pileups[chrom].astype(numpy.float64), kernel).astype(
                self.pileup_dtype)
        return new_pileups

    def computeBindingEnergy(self, motif, pileup_dtype=PILEUP_DTYPE):
        """
        Assumes that we contain a sequence.
        Given a log-odds PWM, compute binding energies for both the sequence and its reverse complement,
         then return them as a StrandedPileup

        :param motif:
        :return:
        """
        start_time = datetime.datetime.now()
        print(('Generating binding energies for {}'.format(self.name)))
        binding_energies = StrandedPileups(name=self.name + '_binding_energy', build=self.build,
                                           chrom_lengths=self.chrom_lengths)
        binding_energies.spileups = {}
        # chrom, sequence_vector, motif = params
        param_list = [(chrom, self.pileups[chrom][:], motif) for chrom in
                      sorted(list(self.pileups.keys()), key=lambda x: self.chrom_lengths[x], reverse=True)]

        if MULTI_PROCESSING_METHOD == 'hybrid' or MULTI_PROCESSING_METHOD == 'antfarm':
            # convert parameter list to job dictionary to feed to AntFarm consisting only of chromosomes too large
            # to use in Pool
            job_dict = collections.OrderedDict()
            new_param_list = []
            for paramset in param_list:
                if MULTI_PROCESSING_METHOD == 'antfarm' or len(paramset[1]) > MAX_MESSAGE_SIZE:
                    job_dict[paramset[0]] = {'inputs': [paramset[1], paramset[2]], 'num_outputs': 2,
                                             'params': [paramset[0]]}
                else:
                    new_param_list.append(paramset)
            param_list = new_param_list

            print((
            'Spawning up to {} subprocesses (using AntFarm) to compute binding energies for {} chromosomes...'.format(
                THREADS, len(
                    job_dict))))

            binding_energy_farm = antfarm.AntFarm(slave_script=toolbox.home_path(
                'workspace/expression_modeling/model/pileup_binding_energy_chromslave.py'),
                                                  base_path=LOCAL_TMP_DIR,
                                                  job_dict=job_dict, max_threads=THREADS, debug=False)
            results = binding_energy_farm.execute()
            del job_dict

            for chrom in results:
                binding_energies.spileups[chrom] = {-1: results[chrom][0].astype(self.pileup_dtype),
                                                    1: results[chrom][1].astype(self.pileup_dtype)}

        if MULTI_PROCESSING_METHOD == 'pool' or MULTI_PROCESSING_METHOD == 'hybrid':
            print((
            'Spawning up to {} subprocesses (using multiprocessing.Pool) to compute binding energies for {} chromosomes...'.format(
                THREADS, len(param_list))))

            with contextlib.closing(multiprocessing.Pool(THREADS)) as p:
                results = p.imap(binding_energy_chromslave, param_list)

        elif MULTI_PROCESSING_METHOD == 'none':
            print(('Computing binding energies for {} chromosomes with a single process...'.format(len(self.spileups))))
            results = list(map(binding_energy_chromslave, param_list))

        if MULTI_PROCESSING_METHOD in ('pool', 'hybrid', 'none'):

            for chrom, extended_fragments in results:
                binding_energies.spileups[chrom] = {-1: extended_fragments[0], 1: extended_fragments[1]}

        print(('Done computing binding energies in {}'.format(datetime.datetime.now() - start_time)))
        # binding_energies.toType(pileup_dtype)
        return binding_energies

    def liftover(self, build_mapper, source_pileup):
        """
        Populate itself by lifting over all the pileup values from <source_pileup> to self using
        <build_mapper>. The .build attributes must be set in both this object and <source_pileup>.

        Loci that cannot be lifted over will be left as NaN

        """
        start_time = datetime.datetime.now()
        print(('Lifting over {} from {} to {}...'.format(source_pileup.name, source_pileup.build, self.build)))
        self._initialize(None)
        mutliple_dest_count = 0
        lifted_over_count = 0
        no_chromosome_counts = {}
        no_match_count = 0
        for chrom in source_pileup.chrom_lengths:

            for source_pos in range(source_pileup.chrom_lengths[chrom]):
                candidate_dest_loci = build_mapper.liftover_locus(source_build=source_pileup.build,
                                                                  dest_build=self.build, source_locus=(
                        toolbox.convert_chroms(chrom, dest=self.chromosome_dialect),
                        source_pos))
                if candidate_dest_loci:
                    if len(
                            candidate_dest_loci) > 1:  # if the source maps to more than one destination, take note of it and don't lift over
                        mutliple_dest_count += 1
                    else:
                        dest_locus = (toolbox.convert_chroms(candidate_dest_loci[0][0], dest=self.chromosome_dialect),
                                      candidate_dest_loci[0][1])
                        if dest_locus[0] in self.chrom_lengths:  # only liftover chromosomes existing in the destination
                            try:
                                self.pileups[dest_locus[0]][dest_locus[1]] = source_pileup.pileups[chrom][source_pos]
                            except IndexError as ie:
                                print(('Destination position invalid. Source locus: {}, destination locus: {}'.format(
                                    (chrom, source_pos), dest_locus)))
                            else:
                                lifted_over_count += 1
                        else:
                            if chrom not in no_chromosome_counts:
                                no_chromosome_counts[chrom] = 0
                            no_chromosome_counts[chrom] += 1
                else:
                    no_match_count += 1
        print(('Done in {}.'.format(datetime.datetime.now() - start_time)))
        print(('{} total loci lifted over, {} did not (out of {} in the source and {} in the destination).'.format(
            lifted_over_count, no_match_count, source_pileup.genome_size, self.genome_size)))
        print(
            ('{} source loci mapped to multiple destinations (and were not lifted over).'.format(mutliple_dest_count)))
        print(('{} source loci mapped to a chromosome that is not present in the destination. Specifically:'.format(
            sum(no_chromosome_counts.values()))))
        print(('{}'.format(', '.join(['{}: {}'.format(k, no_chromosome_counts[k]) for k in no_chromosome_counts]))))

    def liftoverWithMappingTable(self, destination_build, destination_chrom_lengths, mapping_table_filename,
                                 pileup_dtype=None):
        """
        Use <mapping_table_filename> to liftover the pileup vectors in <self>
        and return it as a new pileup object.

        :return:
        """
        CHROM_FIELD = 0
        DESTINATION_FRAG_START = 4
        DESTINATION_INSERTION = 5
        DESTINATION_FRAG_END = 6
        SOURCE_FRAG_START = 8
        SOURCE_INSERTION = 9
        SOURCE_FRAG_END = 10

        if not pileup_dtype:
            pileup_dtype = self.pileup_dtype

        with open(mapping_table_filename, 'rt') as mapping_table:
            print(('Lifting over reads to {} using {}...'.format(destination_build, mapping_table_filename)))

            lifted_pileups = Pileups(chrom_lengths=destination_chrom_lengths, name=self.name, build=destination_build,
                                     chromosome_dialect=self.chromosome_dialect, pileup_dtype=pileup_dtype)
            lifted_pileups._initialize()

            # print lifted_pileups.pileups

            table_reader = csv.reader(mapping_table, dialect=csv.excel_tab)
            for line_num, line in enumerate(table_reader):
                # remember mapping table is 1-based
                if line_num % 100000 == 0:
                    dbg_print('Reading line {}'.format(line_num), 1)
                if line[SOURCE_FRAG_START] != line[SOURCE_FRAG_END]:
                    # print line
                    chrom = toolbox.convert_chroms(line[CHROM_FIELD], dest=self.chromosome_dialect)

                    if chrom not in self.pileups:
                        warning_message = 'Found chromosome {} in mapping table but no record of it in {}.'.format(
                            chrom,
                            self.build)
                        print(('Warning: {}'.format(warning_message)))
                        break
                        # raise Exception(warning_message)
                    if chrom not in lifted_pileups.pileups:
                        warning_message = 'Found chromosome {} in mapping table but no record of it in {}.'.format(
                            chrom,
                            destination_build)
                        print(('Warning: {}'.format(warning_message)))
                        break
                        # raise Exception(warning_message)

                    dest_frag_start = int(line[DESTINATION_FRAG_START]) - 1
                    dest_frag_end = int(line[DESTINATION_FRAG_END]) + 1
                    source_frag_start = int(line[SOURCE_FRAG_START]) - 1
                    source_frag_end = int(line[SOURCE_FRAG_END]) + 1

                    if line[DESTINATION_INSERTION] == r'\N' and line[SOURCE_INSERTION] == r'\N':
                        if source_frag_end - source_frag_start != dest_frag_end - dest_frag_start:
                            raise Exception(
                                'Source ({} bp) and destination ({} bp) fragments not the same size on line {}'.format(
                                    source_frag_end - source_frag_start, dest_frag_end - dest_frag_start, line_num))
                        else:
                            try:
                                lifted_pileups.pileups[chrom][dest_frag_start:dest_frag_end] = self.pileups[chrom][
                                                                                               source_frag_start:source_frag_end]
                            except ValueError as ve:
                                print(('ValueError on on line {}. Source: {} {} {}, destination: {} {} {}'.format(
                                    line_num, source_frag_start, source_frag_end, source_frag_end - source_frag_start,
                                    dest_frag_start, dest_frag_end, dest_frag_end - dest_frag_start)))
                                print(('chrom: {}'.format(chrom)))
                                print(('source chromosome size: {}'.format(self.pileups[chrom].shape)))
                                print(('destination chromosome size: {}'.format(lifted_pileups.pileups[chrom].shape)))
                                print(line)
                                raise ve
        return lifted_pileups

    def liftoverWithChain(self, source_pileups, interval_basepath=INTERVAL_BASEPATH,
                          chainfile_basepath=CHAINFILE_BASEPATH, score_threshold=None,
                          query_size_threshold=None, ref_size_threshold=None):

        overall_start_time = datetime.datetime.now()
        # get intervals
        best_intervals = filterchains.get_liftover_intervals(dest_build=self.build,
                                                             dest_chrom_lengths=self.chrom_lengths,
                                                             source_build=source_pileups.build,
                                                             source_chrom_lengths=source_pileups.chrom_lengths,
                                                             chainfile_basepath=chainfile_basepath,
                                                             interval_basepath=interval_basepath,
                                                             score_threshold=score_threshold,
                                                             query_size_threshold=query_size_threshold,
                                                             ref_size_threshold=ref_size_threshold,
                                                             source_chromosome_dialect=source_pileups.chromosome_dialect,
                                                             dest_chromosome_dialect=self.chromosome_dialect)

        # apply intervals
        print('Applying mapping intervals...')

        self._initialize()

        for query_chrom in best_intervals:
            if len(best_intervals[query_chrom]) > 0:
                if query_chrom in source_pileups.pileups:
                    print(('\tLifting over chromsome {} (in source) with {} intervals'.format(query_chrom, len(
                        best_intervals[query_chrom]))))
                    start_time = datetime.datetime.now()

                    for interval_idx, interval in enumerate(best_intervals[query_chrom]):
                        # if interval_idx % REPORTING_INTERVAL == 0:
                        # _print(
                        # 'Processing interval {} of {}'.format(interval_idx + 1,
                        # len(best_intervals[query_chrom])), 3)
                        query_start, query_end, ref_chrom, ref_offset, interval_polarity = interval

                        # slicing backwards requires subtracting 1 from both indices to get the same positions as a forward slice
                        ref_start = query_start + ref_offset
                        ref_end = query_end + ref_offset
                        # assert ref_start > 0
                        # assert ref_end < len(self.pileups[ref_chrom])

                        if interval_polarity == -1:
                            query_start -= 1
                            query_end -= 1
                            query_start, query_end = query_end, query_start  # flip around

                        if ref_chrom in self.pileups:

                            try:
                                self.pileups[ref_chrom][ref_start:ref_end] = \
                                    source_pileups.pileups[query_chrom][query_start:(query_end, None)[
                                        query_end == -1]:interval_polarity]  # make sure we include the 0th element in the reverse slice
                            except ValueError as ve:
                                print(('Interval: {}'.format(interval)))
                                print(('Interval polarity: {}'.format(interval_polarity)))
                                print(('Query interval: {} {}, {}, size: {}'.format(query_chrom, query_start, query_end,
                                                                                    query_end - query_start)))
                                print(('Reference offset: {}'.format(ref_offset)))
                                print(('Reference interval: {} {}, {}, size: {}'.format(ref_chrom, ref_start, ref_end,
                                                                                        ref_end - ref_start)))
                                raise ve

                    print(
                        ('\t\tDone with chromosome {} in {}'.format(query_chrom, datetime.datetime.now() - start_time)))
                else:
                    print(('\tQuery chromosome {} not in source'.format(query_chrom)))
            else:
                print(('\tQuery chromosome {} has no mapped intervals, skipping'.format(query_chrom)))

        print(('Done lifting over data from {} to {} in {}.'.format(source_pileups.build, self.build,
                                                                    datetime.datetime.now() - overall_start_time)))

    def liftoverWithChain_old(self, source_pileups, chain_basepath, destination_dtype=None):
        """
        Uses <chain_file> to liftover the contents of <source_pileups> to itself.
        Chain files are named <Reference>To<Query>
        """
        start_time = datetime.datetime.now()
        if not destination_dtype:
            destination_dtype = self.pileup_dtype

        header_fields = (
            'dummy', 'score', 'tName', 'tSize', 'tStrand', 'tStart', 'tEnd', 'qName', 'qSize', 'qStrand', 'qStart',
            'qEnd',
            'id')

        # generate chain filename
        chain_filename = os.path.join(chain_basepath,
                                      '{}To{}.over.chain'.format(toolbox.first_lower(source_pileups.build),
                                                                 toolbox.first_upper(self.build)))

        missing_chroms = set([])

        print(('Lifting over from {} using chain file {}'.format(source_pileups.name, chain_filename)))
        with open(chain_filename, 'rt') as chain_file:

            self._initialize(pileup_dtype=destination_dtype)

            new_chain = True
            good_chain = False

            for line_num, line in enumerate(chain_file):
                # new chain
                if line_num % REPORTING_INTERVAL == 0:
                    dbg_print('Processing line {}'.format(line_num), 1)
                if new_chain and line != '\n':  # insurance against multiple blank lines
                    header = toolbox.parse_line_dict(line, header_fields, split_char=' ', strict=True)
                    assert header['dummy'] == 'chain'
                    new_chain = False
                    # relative offsets within the chain
                    ref_chain_pos = 0
                    query_chain_pos = 0

                    ref_chrom = toolbox.convert_chroms(header['tName'], dest=source_pileups.chromosome_dialect)
                    query_chrom = toolbox.convert_chroms(header['qName'], dest=self.chromosome_dialect)

                    good_chain = False
                    if query_chrom in self.pileups:
                        try:
                            assert int(header['qSize']) == len(self.pileups[query_chrom])
                        except AssertionError as ae:
                            print((
                            'Error on line {}, chain {}. Chain file size of {} for query chromosome {} does not match our size of {}'.format(
                                line_num, header['id'], header['qSize'], query_chrom, len(self.pileups[query_chrom]))))
                            raise ae

                        if ref_chrom in source_pileups.pileups:
                            try:
                                assert int(header['tSize']) == len(source_pileups.pileups[ref_chrom])
                            except AssertionError as ae:
                                print((
                                'Error on line {}, chain {}. Chain file size of {} for reference chromosome {} does not match source size of {}'.format(
                                    line_num, header['id'], header['tSize'], ref_chrom,
                                    len(source_pileups.pileups[ref_chrom]))))
                                raise ae
                            good_chain = True
                    else:
                        missing_chroms.add(query_chrom)

                    ref_chain_start = int(header['tStart'])
                    query_chain_start = int(header['qStart'])

                elif line == '\n':
                    # start a new chain on the next line
                    new_chain = True

                elif good_chain:
                    # it must be a data line
                    split_line = line.split('\t')
                    size = int(split_line[0])

                    if len(split_line) == 3:
                        ref_diff = int(split_line[1])
                        query_diff = int(split_line[2])
                    elif len(split_line) == 1:
                        ref_diff = 0
                        query_diff = 0
                    else:
                        raise Exception(
                            'Encountered a chain alignment data line of length 2 on line {}. Unsure how to handle this.'.format(
                                line_num))

                    ref_start_pos = ref_chain_start + ref_chain_pos
                    ref_end_pos = ref_start_pos + size
                    ref_chain_pos += size + ref_diff

                    query_start_pos = query_chain_start + query_chain_pos
                    query_end_pos = query_start_pos + size
                    query_chain_pos += size + query_diff

                    # print line_num, ref_chrom, ref_start_pos, ref_end_pos, query_chrom, query_start_pos, query_end_pos, ref_chain_pos, query_chain_pos
                    self.pileups[query_chrom][query_start_pos:query_end_pos] = source_pileups.pileups[ref_chrom][
                                                                               ref_start_pos:ref_end_pos]
                    # self.pileups[query_chrom][query_start_pos:query_end_pos] += 1

        print(('Done in {}.'.format(datetime.datetime.now() - start_time)))
        if missing_chroms:
            print(('The following chromosomes in the chain file were missing in the destination organism: {}'.format(
                ','.join(sorted(list(missing_chroms))))))

    def exportToWig(self, output_filename, name='', description='', destination_chromosome_dialect='ucsc',
                    wig_type='fixedStep', convert_to_bigwig=False):
        """
        Exports the contents of the pileup in WIG format (see http://genome.ucsc.edu/goldenpath/help/wiggle.html for specification)
        using "fixedStep" intervals
        """

        start_time = datetime.datetime.now()
        write_count = 0
        total_length = sum(self.chrom_lengths.values())

        WIGTOBIGWIG_PATH = 'wigToBigWig'

        if wig_type not in ('fixedStep', 'variableStep'):
            raise ValueError('Invalid parameter value for parameter <wig_type>. Got {}'.format(wig_type))

        if not name:
            name = self.name

        output_path, output_prefix, output_extension = toolbox.parse_path(output_filename)

        wig_filename = os.path.join(output_path, output_prefix + '.wig')

        print(('Exporting contents of {} to {} in WIG format...'.format(name, wig_filename)))
        with open(output_filename, 'w') as wig_file:
            # write header
            wig_file.write(
                'track type=wiggle_0 name={} description={}\n'.format(
                    self.name.replace(' ', '_'), description.replace(' ', '_')))

            # write track data
            for chrom in toolbox.numerical_string_sort(list(self.pileups.keys())):
                chromOut = toolbox.convert_chroms(chrom, dest=destination_chromosome_dialect)
                dbg_print('Scanning chromosome {} to find first and last non-zero values ...'.format(chrom))
                nz = numpy.nonzero(self.pileups[chrom])[0]
                if len(nz) > 0:
                    start_pos = nz[0]
                    end_pos = nz[-1]

                    print(('\tNon-zero region: {}-{}'.format(start_pos, end_pos)))

                    if wig_type == 'fixedStep':
                        wig_file.write('fixedStep chrom={} start={} step=1\n'.format(
                            chromOut, start_pos))
                        for pos in range(start_pos, end_pos):
                            if write_count % 1e7 == 0:
                                print(('\twriting line {:>10}, {:>3.0f} % done'.format(write_count,
                                                                                       write_count * 100 / float(
                                                                                           total_length))))
                            write_count += 1
                            wig_file.write('{}\n'.format(self.pileups[chrom][pos]))

                    elif wig_type == 'variableStep':
                        wig_file.write('variableStep chrom={}\n'.format(
                            chromOut))
                        for pos in range(start_pos, end_pos):
                            if write_count % 1e7 == 0:
                                print(('\twriting line {:>10}. {:>3.0f} % done'.format(write_count,
                                                                                       write_count * 100 / float(
                                                                                           total_length))))
                            write_count += 1
                            wig_file.write('{} {}\n'.format(pos, self.pileups[chrom][pos]))
                else:
                    print(('\tNo non-zero entries found for chromosome {} of length {}'.format(chrom,
                                                                                               self.chrom_lengths[
                                                                                                   chrom])))

            file_size = wig_file.tell()
        print(('Done in {}.'.format(datetime.datetime.now() - start_time)))
        print(('Resulting file has {} lines, total size: {:.2} MB'.format(write_count, file_size / float(2 ** 20))))

        if convert_to_bigwig:
            start_time = datetime.datetime.now()
            bigwig_filename = os.path.join(output_path, output_prefix + '.bw')
            print(('Converting to bigwig format as {}'.format(bigwig_filename)))
            temp_chromosome_size_filename = os.path.join(output_path, '{}_chrom_sizes.txt'.format(self.build))
            with open(temp_chromosome_size_filename, 'w') as chrom_size_file:
                for chrom in self.chrom_lengths:
                    chrom_size_file.write('{}\t{}\n'.format(
                        toolbox.convert_chroms(chrom, dest=destination_chromosome_dialect),
                        self.chrom_lengths[chrom]))
            cmd_line = [WIGTOBIGWIG_PATH, wig_filename, temp_chromosome_size_filename, bigwig_filename]
            try:
                conversion_output = subprocess.check_output(cmd_line)
            except subprocess.CalledProcessError as cpe:
                print(('Error: {}, {}, {}'.format(cpe.returncode, cpe.message, cpe.output)))
            except Exception as ex:
                print((ex.args, ex.message))
            else:
                print(conversion_output)
                print(('Done in {}.'.format(datetime.datetime.now() - start_time)))

    def exportToBed(self, bed_filename, region_prefix='region',
                    destination_chromosome_dialect='ucsc'):
        """
        Exports the contents of the pileup in BED format
        (see http://genome.ucsc.edu/FAQ/FAQformat.html#format1 for specification)
        """
        start_time = datetime.datetime.now()
        write_count = 0
        print(('Exporting contents of {} to {} in BED format...'.format(self.name, bed_filename)))
        with open(bed_filename, 'w') as bed_file:
            bed_writer = csv.writer(bed_file, dialect=csv.excel_tab)
            # write track data
            for chrom in toolbox.numerical_string_sort(list(self.pileups.keys())):
                previous_value = 0
                region_start = 0
                for pos in range(self.chrom_lengths[chrom]):
                    # if the value changed or we hit the end, then
                    if self.pileups[chrom][pos] != previous_value or pos == self.chrom_lengths[chrom] - 1:
                        if previous_value > 0:  # we're ending a region, write it out
                            if write_count % 1e6 == 0:
                                dbg_print('Writing line {}'.format(write_count), 1)
                            write_count += 1
                            # WIG indexing is one-based
                            chromOut = toolbox.convert_chroms(chrom, dest=destination_chromosome_dialect)
                            chromStart = region_start
                            chromEnd = pos + 1
                            name = '{}_{}'.format(region_prefix, write_count)
                            score = previous_value
                            bed_writer.writerow([chromOut, chromStart, chromEnd, name, score])
                        if self.pileups[chrom][pos] > 0:  # we're starting a new region
                            region_start = pos
                        previous_value = self.pileups[chrom][pos]

            file_size = bed_file.tell()

        print(('Done in {}.'.format(datetime.datetime.now() - start_time)))
        print(('Resulting file has size: {:.2} MB'.format(file_size / float(2 ** 20))))

    def mappabilityFromChain(self, other_build, other_chrom_lengths, from_or_to='from',
                             other_chromosome_dialect=DEFAULT_CHROMOSOME_DIALECT, chainfile_basepath=CHAINFILE_BASEPATH,
                             interval_basepath=INTERVAL_BASEPATH, score_threshold=None,
                             query_size_threshold=None, ref_size_threshold=None):
        overall_start_time = datetime.datetime.now()
        from_or_to = from_or_to.lower()
        assert from_or_to in ('from', 'to')
        print(('Populating with vector of mappability {} {}'.format(from_or_to, other_build)))

        if from_or_to == 'to':
            ref_build = other_build
            query_build = self.build
            ref_chrom_lengths = other_chrom_lengths
            query_chrom_lengths = self.chrom_lengths
            ref_chrom_dialect = other_chromosome_dialect
            query_chrom_dialect = self.chromosome_dialect
        else:
            ref_build = self.build
            query_build = other_build
            ref_chrom_lengths = self.chrom_lengths
            query_chrom_lengths = other_chrom_lengths
            ref_chrom_dialect = self.chromosome_dialect
            query_chrom_dialect = other_chromosome_dialect

            # get intervals
        best_intervals = filterchains.get_liftover_intervals(dest_build=ref_build,
                                                             dest_chrom_lengths=ref_chrom_lengths,
                                                             source_build=query_build,
                                                             source_chrom_lengths=query_chrom_lengths,
                                                             chainfile_basepath=chainfile_basepath,
                                                             interval_basepath=interval_basepath,
                                                             score_threshold=score_threshold,
                                                             query_size_threshold=query_size_threshold,
                                                             ref_size_threshold=ref_size_threshold,
                                                             source_chromosome_dialect=query_chrom_dialect,
                                                             dest_chromosome_dialect=ref_chrom_dialect)

        # apply intervals
        self._initialize()
        missing_query_chroms = set([])
        missing_ref_chroms = set([])

        mapped_counter = 0

        for query_chrom in best_intervals:
            if len(best_intervals[query_chrom]) > 0:
                # print query_chrom, len(self.pileups[query_chrom])
                if from_or_to == 'from' or query_chrom in self.pileups:
                    print(('\tComputing mappability for source chromosome {} with {} intervals'.format(query_chrom, len(
                        best_intervals[query_chrom]))))
                    start_time = datetime.datetime.now()
                    interval_counter = 0
                    for interval_idx, interval in enumerate(best_intervals[query_chrom]):
                        # if interval_idx % REPORTING_INTERVAL == 0:
                        # _print(
                        # 'Processing interval {} of {}'.format(interval_idx + 1,
                        # len(best_intervals[query_chrom])),
                        # 3)
                        query_start, query_end, ref_chrom, ref_offset, interval_polarity = interval
                        if from_or_to == 'from':
                            if ref_chrom in self.pileups:
                                self.pileups[ref_chrom][query_start + ref_offset:query_end + ref_offset] += 1
                                # print self.pileups[ref_chrom][query_start + ref_offset:query_end+ ref_offset]
                            else:
                                missing_ref_chroms.add(ref_chrom)
                        else:
                            self.pileups[query_chrom][query_start:query_end] += 1
                        interval_counter += 1
                        mapped_counter += query_end - query_start
                    print(
                        ('\t\tDone with chromosome {} in {}'.format(query_chrom, datetime.datetime.now() - start_time)))
                else:
                    print(('\tQuery chromosome {} not in self'.format(query_chrom)))
                    missing_query_chroms.add(query_chrom)
            else:
                print(('\tQuery chromosome {} has no mapped intervals, skipping'.format(query_chrom)))
        if missing_query_chroms:
            print(('The following chromosomes in the interval file were missing in the query: {}'.format(
                ', '.join(sorted(list(missing_query_chroms))))))
        if missing_ref_chroms:
            print(('The following chromosomes in the interval file were missing in the reference: {}'.format(
                ', '.join(sorted(list(missing_ref_chroms))))))
        print(('Done computing mappability of {} {} {} in {}.'.format(self.build, from_or_to, other_build,
                                                                      datetime.datetime.now() - overall_start_time)))
        self_covered_loci = self.flatten().astype(numpy.int).sum()
        print((self_covered_loci, self.genome_size))
        print(('Mappings processed for {} loci, covering {} of self ({} of total)'.format(mapped_counter,
                                                                                          self_covered_loci,
                                                                                          self_covered_loci / float(
                                                                                              self.genome_size))))
        print()

    def mappabilityFromMappingTable(self, mapping_table_filename, from_or_to='from'):
        """
        if <from_or_to> = 'from':
            Populate self with a vector counting how many loci in the source organism map
            to loci in self, given a mapping table in <mapping_table_filename>
        if <from_or_to> = 'to':
            Populate self with a vector counting how many loci in self map
            to loci in the source organism, given a mapping table in <mapping_table_filename>
        """
        # Field positions
        CHROM_FIELD = 0
        DESTINATION_FRAG_START = 4
        DESTINATION_INSERTION = 5
        DESTINATION_FRAG_END = 6
        SOURCE_FRAG_START = 8
        SOURCE_INSERTION = 9
        SOURCE_FRAG_END = 10

        self._initialize()

        start_time = datetime.datetime.now()

        with open(mapping_table_filename, 'rt') as mapping_table:
            table_reader = csv.reader(mapping_table, dialect=csv.excel_tab)

            for line_num, line in enumerate(table_reader):
                # remember mapping table is 1-based
                if line_num % 100000 == 0:
                    dbg_print('Reading line {}'.format(line_num), 1)
                if line[SOURCE_FRAG_START] != line[SOURCE_FRAG_END]:
                    # print line
                    chrom = toolbox.convert_chroms(line[CHROM_FIELD], dest=self.chromosome_dialect)

                    if chrom not in self.pileups:
                        warning_message = 'Found chromosome {} in mapping table but no record of it in {}.'.format(
                            chrom, self.build)
                        print(('Warning: {}'.format(warning_message)))
                        break
                        # raise Exception(warning_message)
                    dest_frag_start = int(line[DESTINATION_FRAG_START]) - 1
                    dest_frag_end = int(line[DESTINATION_FRAG_END]) + 1
                    source_frag_start = int(line[SOURCE_FRAG_START]) - 1
                    source_frag_end = int(line[SOURCE_FRAG_END]) + 1

                    if line[DESTINATION_INSERTION] == r'\N' and line[SOURCE_INSERTION] == r'\N':
                        if source_frag_end - source_frag_start != dest_frag_end - dest_frag_start:
                            raise Exception(
                                'Source ({} bp) and destination ({} bp) fragments not the same size on line {}'.format(
                                    source_frag_end - source_frag_start, dest_frag_end - dest_frag_start, line_num))
                        else:
                            try:
                                if from_or_to == 'from':
                                    self.pileups[chrom][dest_frag_start:dest_frag_end] += 1
                                else:
                                    self.pileups[chrom][source_frag_start:source_frag_end] += 1
                            except ValueError as ve:
                                print((
                                'Unequal fragment sizes have slipped through on line {}. May be a chromosome size mismatch.'.format(
                                    line_num)))
                                print(('Source: {} {} {}, destination: {} {} {}'.format(source_frag_start,
                                                                                        source_frag_end,
                                                                                        source_frag_end - source_frag_start,
                                                                                        dest_frag_start, dest_frag_end,
                                                                                        dest_frag_end - dest_frag_start)))
                                print(('chrom: {}'.format(chrom)))
                                raise ve
        print(('Done in {}'.format(datetime.datetime.now() - start_time)))

    def mappabilityFromChain_old(self, chain_file_basepath, other_build, from_or_to='from', use_score=False):
        """
        Populate with a 'mappability' vector derived from <chain_filename> that
        indicates the mappability of each locus in itself to the other species.

        If <use_score> is false, each locus will be 1 if mappable from the
         reference species, 0 otherwise.
        If <use_score> is true, each locus will contain the log10 value of the
         score field for the chain that maps to it, 0 otherwise.

        A note about chain files: The files are named in the form
        ReferenceToQuery, which is counter to my intuition, at least.

        So the build of this pileups object should match the reference build of
        the chain file being used (the first build in the filename)
        """
        start_time = datetime.datetime.now()
        header_fields = (
            'dummy', 'score', 'tName', 'tSize', 'tStrand', 'tStart', 'tEnd', 'qName', 'qSize', 'qStrand', 'qStart',
            'qEnd',
            'id')
        from_or_to = from_or_to.lower()
        assert from_or_to in ('from', 'to')

        print(('Populating with vector of mappability ({}) {} {}'.format(('binary', 'log10_score')[use_score],
                                                                         from_or_to, other_build)))

        if from_or_to == 'from':
            ref_build = other_build
            query_build = self.build
        else:
            ref_build = self.build
            query_build = other_build

        chain_filename = os.path.join(chain_file_basepath, '{}To{}.over.chain'.format(toolbox.first_lower(ref_build),
                                                                                      toolbox.first_upper(query_build)))

        print(('Using chain file: {}'.format(chain_filename)))

        with open(chain_filename, 'rt') as chain_file:
            self._initialize()

            new_chain = True
            good_chain = False

            mapped_count = 0
            # total_ref = 0
            # total_query = 0

            for line_num, line in enumerate(chain_file):
                # new chain
                if line_num % REPORTING_INTERVAL == 0:
                    dbg_print('Reading line {}'.format(line_num), 1)
                if new_chain and line != '\n':  # insurance against multiple blank lines
                    header = toolbox.parse_line_dict(line, header_fields, split_char=' ', strict=True)
                    assert header['dummy'] == 'chain'
                    new_chain = False
                    # relative offsets within the chain
                    ref_chain_pos = 0
                    query_chain_pos = 0

                    ref_chrom = toolbox.convert_chroms(header['tName'], dest=self.chromosome_dialect)
                    query_chrom = toolbox.convert_chroms(header['qName'], dest=self.chromosome_dialect)

                    ref_size = int(header['tSize'])
                    query_size = int(header['qSize'])

                    # total_ref += ref_size
                    # total_query += query_size

                    good_chain = False
                    if from_or_to == 'from':
                        if query_chrom in self.pileups:
                            assert query_size == len(self.pileups[query_chrom])
                            good_chain = True
                    else:
                        if ref_chrom in self.pileups:
                            assert ref_size == len(self.pileups[ref_chrom])
                            good_chain = True

                            # print ref_chrom, query_chrom, good_chain
                    ref_chain_start = int(header['tStart'])
                    query_chain_start = int(header['qStart'])

                elif line == '\n':
                    # start a new chain on the next line
                    new_chain = True

                elif good_chain:
                    # it must be a data line
                    split_line = line.split('\t')
                    size = int(split_line[0])

                    if len(split_line) == 3:
                        ref_diff = int(split_line[1])
                        query_diff = int(split_line[2])
                    elif len(split_line) == 1:
                        ref_diff = 0
                        query_diff = 0
                    else:
                        raise Exception(
                            'Encountered a chain alignment data line of length 2 on line {}. Unsure how to handle this.'.format(
                                line_num))

                    ref_start_pos = ref_chain_start + ref_chain_pos
                    ref_end_pos = ref_start_pos + size
                    ref_chain_pos += size + ref_diff

                    query_start_pos = query_chain_start + query_chain_pos
                    query_end_pos = query_start_pos + size
                    query_chain_pos += size + query_diff

                    mapped_count += size

                    if use_score:
                        score = math.log10(int(header['score']))
                    else:
                        score = 1

                    if from_or_to == 'from':
                        self.pileups[query_chrom][query_start_pos:query_end_pos] += score
                    else:
                        self.pileups[ref_chrom][ref_start_pos:ref_end_pos] += score

        print(('Done in {}.'.format(datetime.datetime.now() - start_time)))
        self_covered_loci = self.flatten().astype(numpy.int).sum()
        print(('Mappings processed for {} loci, covering {} of self ({} of total)'.format(mapped_count,
                                                                                          self_covered_loci,
                                                                                          self_covered_loci / float(
                                                                                              self.genome_size))))

    def copy(self, dtype=None):
        """
        Alias for deepCopy()
        :param dtype:
        :return:
        """
        if not dtype:
            dtype = self.pileup_dtype
        return self.deepCopy(dtype)

    def deepCopy(self, dtype=None):
        """
        Returns a new pileups object containing the same data (a deep copy) with an optional change of datatype.
        :param other:
        :return:
        """
        if not dtype:
            dtype = self.pileup_dtype

        new_pu = self.emptyCopy()
        # print 'Creating deep copy of {}'.format(self.name)
        for chrom in self.pileups:
            # print '\t{}'.format(chrom)
            new_pu.pileups[chrom] = self.pileups[chrom].astype(dtype=dtype)
        return new_pu

    def shallowCopy(self):
        new_pu = self.emptyCopy()
        # print 'Creating shallow copy of {}'.format(self.name)
        for chrom in self.pileups:
            new_pu.pileups[chrom] = self.pileups[chrom]
        return new_pu

    def emptyCopy(self):
        """
        Returns a new pileups object containing the same meta-data but with no pileups data
        :return:
        """
        # print 'Creating empty copy of {}'.format(self.name)
        new_pu = Pileups(self.chrom_lengths, name=self.name, build=self.build,
                         chromosome_dialect=self.chromosome_dialect)
        new_pu.pileups = {}
        new_pu.is_normalized = self.is_normalized
        # new_pu.genome_size = self.genome_size
        new_pu.coverage = self.coverage
        # new_pu.max_height = self.max()
        new_pu.total_reads = self.total_reads
        new_pu.mean_read_length = self.mean_read_length
        new_pu.mode_read_length = self.mode_read_length
        new_pu.pileup_dtype = self.pileup_dtype
        return new_pu

    def apply(self, func):
        for chrom in self.pileups:
            self.pileups[chrom] = func(self.pileups[chrom])

    def toType(self, pileup_dtype=PILEUP_DTYPE):
        """
        Converts all pileup chromosome vectors to the specified data type
        :param pileup_dtype:
        :return:
        """
        self.pileup_dtype = pileup_dtype
        for chrom in self.pileups:
            self.pileups[chrom] = self.pileups[chrom].astype(pileup_dtype)
            
    def astype(self, pileup_dtype=PILEUP_DTYPE):
        """
        Analogous to the numpy.astype() method, returns a new  pileup
        with chromosome data in the specified data type.
        
        :param pileup_dtype:
        :return:
        """
        new_pileup = self.emptyCopy()
        new_pileup.pileup_dtype = pileup_dtype
        
        for chrom in self.pileups:
            new_pileup.pileups[chrom] = self.pileups[chrom].astype(pileup_dtype)  
            
        return new_pileup            

    def memMap(self, writable=True, tmp_dir=NETWORK_TMP_DIR):
        """
        Converts pileup chromosome vectors to mem_mapped arrays on disk.
        """
        self.save_path = os.path.join(tmp_dir, 'pileup_{}'.format(self.id))
        print('Saving to {} in mem mapped mode. Writable: {}'.format(self.save_path, writable))

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        max_chroms_to_map = min(len(self.pileups), MAX_FILEHANDLES_PER_PILEUP)

        for chrom in sorted(self.pileups, key=lambda x: len(x), reverse=True)[:max_chroms_to_map]:
            vector_fname = os.path.join(self.save_path, '{}.npy'.format(chrom))
            numpy.save(vector_fname, self.pileups[chrom])
            self.pileups[chrom] = numpy.load(vector_fname, mmap_mode=('r', 'r+')[writable])

    def ceil(self):
        result = Pileups(self.chrom_lengths, build=self.build, name=self.name)

        for chrom in self.chrom_lengths:
            result.pileups[chrom] = numpy.ceil(self.pileups[chrom])
        return result

    def floor(self):
        result = Pileups(self.chrom_lengths, build=self.build, name=self.name)

        for chrom in self.chrom_lengths:
            result.pileups[chrom] = numpy.floor(self.pileups[chrom])
        return result

    def round(self, decimals=0):
        result = Pileups(self.chrom_lengths, build=self.build, name=self.name)

        for chrom in self.chrom_lengths:
            result.pileups[chrom] = numpy.round(self.pileups[chrom], decimals=decimals)
        return result

    def logical_and(self, other):
        result = Pileups(self.chrom_lengths, build=self.build, name=self.name)
        for chrom in self.pileups:
            if chrom in other.pileups:
                result.pileups[chrom] = numpy.logical_and(self.pileups[chrom], other.pileups.chrom)
        return result

    def logical_or(self, other):
        result = Pileups(self.chrom_lengths, build=self.build, name=self.name)
        for chrom in self.pileups:
            if chrom in other.pileups:
                result.pileups[chrom] = numpy.logical_or(self.pileups[chrom], other.pileups.chrom)
        return result

    def logical_not(self):
        result = Pileups(self.chrom_lengths, build=self.build, name=self.name)
        for chrom in self.pileups:
            result.pileups[chrom] = numpy.logical_not(self.pileups[chrom])
        return result

    @property
    def max(self):
        """
        Maximum value contained in any chromosome
        :return:
        """
        self.max_height = float('-Inf')
        for chrom in self.pileups:
            self.max_height = max(self.max_height, max(self.pileups[chrom]))
        return self.max_height

    def fill(self, value):
        """
        Fill up the chromosome arrays with <value>
        """
        print(('Filling chromosome vectors with {}'.format(value)))
        self._initialize()
        for chrom in self.chrom_lengths:
            self.pileups[chrom] = numpy.full(self.chrom_lengths[chrom], value, dtype=float)
        print('Done.')

    def nonzero(self):
        """
        Returns a new pileup object consisting of boolean vectors marking whether or not a position was 0 in the parent
        pileup object
        """
        new_pileups = self.copy()
        for chrom in new_pileups.pileups:
            new_pileups.pileups[chrom] = numpy.greater(self.pileups[chrom], 0)
        return new_pileups

    def threshold(self, min_value=None, max_value=None):
        """
        Returns a new pileup object where every value less than <min_value> or greater than <max_value> 
        has been replaced by 0
        :param min_value:
        :param max_value:
        :return:
        """
        print('Replacing all values {}{}{} with 0'.format(('', 'below {}'.format(min_value))[bool(min_value)],
                                                          ('', ' or ')[bool(min_value) and bool(max_value)],
                                                          ('', 'above {}'.format(max_value))[bool(max_value)]))
        new_pileups = self.copy()
        for chrom in new_pileups.pileups:
            print('\tProcessing chromosome {} ...'.format(chrom))
            new_pileups.pileups[chrom] = self.pileups[chrom][:]
            if min_value is not None:
                new_pileups.pileups[chrom] *= numpy.greater(self.pileups[chrom], min_value).astype(float)
            if max_value is not None:
                new_pileups.pileups[chrom] *= numpy.less(self.pileups[chrom], max_value).astype(float)
        return new_pileups
         

    def __iadd__(self, other):
        try:
            assert self.build == other.build
            self.name = '({}+{})'.format(self.name, other.name)
            for chrom in self.chrom_lengths:
                assert len(self.pileups[chrom]) == len(other.pileups[chrom])
                self.pileups[chrom] += other.pileups[chrom]
            self.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            self.name = '({}+{})'.format(self.name, other)
            for chrom in self.chrom_lengths:
                self.pileups[chrom] = numpy.add(self.pileups[chrom], other)
        return self

    def __isub__(self, other):
        try:
            assert self.build == other.build
            self.name = '({}-{})'.format(self.name, other.name)
            for chrom in self.chrom_lengths:
                assert len(self.pileups[chrom]) == len(other.pileups[chrom])
                self.pileups[chrom] -= other.pileups[chrom]
                self.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            self.name = '({}-{})'.format(self.name, other)
            for chrom in self.chrom_lengths:
                self.pileups[chrom] = numpy.subtract(self.pileups[chrom], other)
        return self

    def __imul__(self, other):
        try:
            # type(other) == type(self):
            assert self.build == other.build
            self.name = '({}*{})'.format(self.name, other.name)
            for chrom in self.chrom_lengths:
                assert len(self.pileups[chrom]) == len(other.pileups[chrom])
                self.pileups[chrom] *= other.pileups[chrom]
            self.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            self.name = '({}*{})'.format(self.name, other)
            for chrom in self.chrom_lengths:
                self.pileups[chrom] = numpy.multiply(self.pileups[chrom], other)

        return self

    def __idiv__(self, other):
        try:
            assert self.build == other.build
            self.name = '({}/{})'.format(self.name, other.name)
            for chrom in self.chrom_lengths:
                assert len(self.pileups[chrom]) == len(other.pileups[chrom])
                self.pileups[chrom] /= other.pileups[chrom]
            self.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            self.name = '({}/{})'.format(self.name, other)
            for chrom in self.chrom_lengths:
                self.pileups[chrom] = numpy.divide(self.pileups[chrom], other)

        return self

    def __add__(self, other):
        result = self.emptyCopy()
        try:
            assert self.build == other.build
            result.name = '({}+{})'.format(self.name, other.name)
            for chrom in self.chrom_lengths:
                assert len(self.pileups[chrom]) == len(other.pileups[chrom])
                result.pileups[chrom] = self.pileups[chrom] + other.pileups[chrom]
            result.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            for chrom in self.pileups:
                result.pileups[chrom] = numpy.add(self.pileups[chrom], other)
            result.name = '({}+{})'.format(self.name, other)
        return result

    def __sub__(self, other):
        result = self.emptyCopy()
        try:
            assert self.build == other.build
            result.name = '({}-{})'.format(self.name, other.name)
            for chrom in self.chrom_lengths:
                assert len(self.pileups[chrom]) == len(other.pileups[chrom])
                result.pileups[chrom] = self.pileups[chrom] - other.pileups[chrom]
            result.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError):
            for chrom in self.pileups:
                result.pileups[chrom] = numpy.subtract(self.pileups[chrom], other)
            result.name = '({}-{})'.format(self.name, other)
        return result

    def __mul__(self, other):
        result = self.emptyCopy()
        try:
            assert self.build == other.build
            result.name = '({}*{})'.format(self.name, other.name)
            for chrom in self.chrom_lengths:
                # if chrom in other.chrom_lengths:
                    assert len(self.pileups[chrom]) == len(other.pileups[chrom])
                    result.pileups[chrom] = self.pileups[chrom] * other.pileups[chrom]
            result.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError) as ex:
            print(ex)
            for chrom in self.pileups:
                result.pileups[chrom] = numpy.multiply(self.pileups[chrom], other)
            result.name = '({}*{})'.format(self.name, other)
        return result

    def __div__(self, other):
        result = self.emptyCopy()
        try:
            assert self.build == other.build
            result.name = '({}/{})'.format(self.name, other.name)
            for chrom in self.chrom_lengths:
                # if chrom in other.chrom_lengths:
                    assert len(self.pileups[chrom]) == len(other.pileups[chrom])
                    result.pileups[chrom] = self.pileups[chrom] / other.pileups[chrom].astype(float)
            result.is_normalized = self.is_normalized and other.is_normalized
        except (AttributeError, ValueError) as ex:
            print(ex)
            for chrom in self.pileups:
                result.pileups[chrom] = numpy.divide(self.pileups[chrom], float(other))
            result.name = '({}/{})'.format(self.name, other)
        return result

    def __pos__(self):
        return self

    def __neg__(self):
        negated = Pileups(self.chrom_lengths, build=self.build, name=self.name)

        for chrom in self.chrom_lengths:
            negated.pileups[chrom] = -self.pileups[chrom]

        return negated

    def __len__(self):
        return self.genome_size

    def __abs__(self):
        result = Pileups(self.chrom_lengths, build=self.build, name=self.name)

        for chrom in self.chrom_lengths:
            result.pileups[chrom] = numpy.abs(self.pileups[chrom])
        return result

    def __repr__(self):
        result = 'Pileups object. Name: {}, Build: {}\n'.format(self.name, self.build)
        result += 'Chromosome lengths:\n'
        for chrom in self.chrom_lengths:
            result += '\t{:>40}\t{:>11}\n'.format(chrom, self.chrom_lengths[chrom])
        try:
            result += 'Data type: {}\n'.format(list(self.pileups.values())[0].dtype)
        except Exception:
            pass
        return result


def pileup_sum(pileup_sequence):
    """
    Returns the sum of a sequence of pileup objects
    :param pileup_sequence:
    :return:
    """
    sum_total = pileup_sequence[0]
    if len(pileup_sequence) > 1:
        for pu in pileup_sequence[1:]:
            sum_total += pu
    return sum_total


def pileup_product(pileup_sequence):
    product_total = pileup_sequence[0].deepCopy()
    if len(pileup_sequence) > 1:
        for pu in pileup_sequence[1:]:
            product_total *= pu
    return product_total


def test():
    import pp_config

    schmidt_configs = {'C57B6_mm9': pp_config.read_config('config/schmidt_mouse.txt'),
                       'human': pp_config.read_config('config/schmidt_human.txt')}

    configs = schmidt_configs
    control_configs = schmidt_configs

    for config in list(configs.values()):
        for k in config:
            if type(config[k]) == str:
                config[k] = config[k].replace('oasis', 'oasis_local')
        del config
    chroms = {}
    for organism in ('C57B6_mm9',):
        chroms[organism] = get_chrom_length_dict(
            os.path.join(os.environ['HOME'], '.local', 'opt', 'idrCode', 'genome_tables',
                         'genome_table.{}.txt'.format(configs[organism]['IDR_GENOME_NAME'])))
    test1 = Pileups(chrom_lengths=chroms['C57B6_mm9'], build='mm9')
    test1.loadFromWig(
        '/cellar/users/dskola/oasis_local/wigs/GSM1014195_mm9_wgEncodeUwDnaseLiverC57bl6MAdult8wksSigRep2.wig')


if __name__ == '__main__':
    test()
