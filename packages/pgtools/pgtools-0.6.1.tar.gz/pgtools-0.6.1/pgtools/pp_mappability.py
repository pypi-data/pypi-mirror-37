import argparse
import csv
import datetime
import os
import re
import subprocess

import pysam
from pgtools import toolbox

from model import pp_config
from model import pp_filteralignments


def calculate_read_length(config, read_filename, num_lines_to_check=0):
    """
    :param config:
    :param read_filename:
    :return:

    Given a filename containing reads, will attempt to infer the file format from the extension, then apply
    an appropriate method to compute the read length of the file.

    For .tagAlign files, will calculate the mode of the read length (difference between end and start points)

    Other file formats such as BAM and FASTQ may be implemented later.
    """

    if read_filename.endswith('.tagAlign'):
        print(('Calculating read length for {} using {} reads...'.format(read_filename,
                                                                        ('all', 'first {}'.format(num_lines_to_check))[
                                                                            bool(num_lines_to_check)])))
        read_lengths = {}
        with open(read_filename, 'rU') as read_file:
            if num_lines_to_check:
                lines_to_read = read_file.readlines(num_lines_to_check)
            else:
                lines_to_read = read_file
            for line in lines_to_read:
                split_line = line.split('\t')
                length = int(split_line[2]) - int(split_line[1])
                if length not in read_lengths:
                    read_lengths[length] = 0
                read_lengths[length] += 1
        length_mode = max(iter(list(read_lengths.keys())), key=(lambda x: read_lengths[x]))
        print(('\tread length: {}'.format(length_mode)))
        return length_mode


def get_mappability(config, read_length, make_region_file=True):
    """
    :param config:
    :param read_length:
    :return:

    Will look for a mappability look-up table and try to find the mappability value for the given read length there.
    If not found, will compute the mappability de novo and add it to the table for future reference.
    
    If <make_region_file> is True, will also ensure that a bed file of mappable regions exists in REFERENCE_GENOME_PATH
    and generate it if necessary.
    """

    genome_path, genome_fname, genome_ext = toolbox.parse_path(config['REFERENCE_GENOME_PATH'])

    specifc_temp_dir = os.path.join(config['TMP_PATH'], config['GENOME_BUILD'], str(read_length))

    aligned_reads_filepath = os.path.join(specifc_temp_dir, 'mappable_samfile.sam')
    mappability_table_filename = os.path.join(genome_path, 'mappability_table.tsv')

    print('Looking for genome mappability table in {}'.format(mappability_table_filename))
    mappability = None
    try:
        with open(mappability_table_filename, 'rU') as mappability_table_file:
            mappability_table = csv.reader(mappability_table_file, dialect=csv.excel_tab)
            for line in mappability_table:
                if int(line[0]) == read_length:
                    mappability_table_file.close()
                    mappability = int(line[1])
                    print('Found pre-computed mappable size of {} for read length {}'.format(mappability,
                                                                                             read_length))
                    break
                    # return mappability
        if not mappability:
            print('Pre-computed mappable size not found.')
    except IOError as ioe:
        print('Mappability table doesn\'t exist')

    # see if we need to generate reads and align them
    genome_path, dummy, dummy = toolbox.parse_path(config['REFERENCE_GENOME_PATH'])
    mappability_bed_filepath = os.path.join(genome_path,
                                            '{}_mappable_regions_{}.bed'.format(config['GENOME_BUILD'], read_length))

    starts_bed_filepath = os.path.join(genome_path,
                                       '{}_start_regions_{}.bed'.format(config['GENOME_BUILD'], read_length))

    need_region_files = make_region_file and not (
        os.path.isfile(mappability_bed_filepath) and os.path.isfile(starts_bed_filepath))

    need_to_align = not mappability or (need_region_files and not os.path.isfile(aligned_reads_filepath + '_done'))

    if need_to_align:
        print('Computing mappability from synthetic genomic reads')
        mappability = compute_mappability(config, bowtie2_index_filepath=config['BOWTIE2_INDEX_PATH'],
                                          genome_filepath=config['REFERENCE_GENOME_PATH'],
                                          aligned_reads_filepath=aligned_reads_filepath,
                                          read_length=read_length, force_alignment=not mappability)

        print(('Calculated mappable size of {}'.format(mappability)))

        with open(mappability_table_filename, 'a') as mappability_table_file:
            mappability_table = csv.writer(mappability_table_file, dialect=csv.excel_tab)
            mappability_table.writerow([read_length, mappability])
            print('Updated mappability table.')

    # generate the bed files if necessary.
    if need_region_files:
        print('Generating mappable region bed files')
        generate_mappability_bed(config=config, read_length=read_length)

    return mappability


def smart_run(func, params, input_filename, output_filename):
    """
    Checks that input from the previous step has completed and output from this step has not completed. Uses empty
    files with the name of FILENAME_done to track progress.

    If <input_filename> is empty, don't bother checking it (useful when the input is generated by some external process)

    :param func:
    :param params:
    :param input_filename:
    :param output_filename:
    :return:
    """

    if not input_filename or (os.path.isfile(input_filename) and os.path.isfile(input_filename + '_done')):
        if os.path.isfile(output_filename) and os.path.isfile(output_filename + '_done'):
            print('Output file {} already exists and is complete. Skipping...'.format(output_filename))
        else:
            try:
                start_time = datetime.datetime.now()
                return_val = func(**params)
            except Exception as ex:
                raise ex
            else:
                # create an empty file to flag completion.
                with open(output_filename + '_done', 'w') as flag_file:
                    flag_file.write('')
                print('Done in {}'.format(datetime.datetime.now() - start_time))
                return return_val
    else:
        raise Exception('Input file {} does not exist or is not complete!'.format(input_filename))


def compute_mappability(config, bowtie2_index_filepath, genome_filepath, aligned_reads_filepath, read_length,
                        force_alignment=False):
    """
    :param config:
    :param read_length:
    :return:
    """

    print('Establishing temp path...')
    specifc_temp_dir = os.path.join(config['TMP_PATH'], config['GENOME_BUILD'], str(read_length))
    toolbox.establish_path(specifc_temp_dir, silent=False)

    # first generate all possible reads of length <read_length>
    print('Generating self reads...')
    reads_filepath = os.path.join(specifc_temp_dir, '{}_{}_allreads.txt'.format(config['GENOME_BUILD'], read_length))
    smart_run(generate_all_reads,
              params=dict(genome_filepath=genome_filepath, reads_filepath=reads_filepath, read_length=read_length),
              input_filename='', output_filename=reads_filepath)

    # now align them to the index of the same genome
    print('Aligning reads to self...')
    # aligned_reads_filepath = os.path.join(specifc_temp_dir, 'mappable_samfile.sam')
    if force_alignment:  # force the alignment to re-run
        try:
            os.remove(aligned_reads_filepath)
        except OSError as oe:
            print('Aligned reads file {} did not exist'.format(aligned_reads_filepath))
        else:
            print('Deleted existing aligned reads file {} to force re-run of alignment'.format(aligned_reads_filepath))

    mappability = smart_run(align_to_self,
                            params=dict(config=config, bowtie2_index_filepath=bowtie2_index_filepath,
                                        reads_filepath=reads_filepath, output_sam_filepath=aligned_reads_filepath,
                                        read_length=read_length), input_filename=reads_filepath,
                            output_filename=aligned_reads_filepath)

    print('Deleting synthetic reads file ...')
    os.remove(reads_filepath)  # delete the massive reads file now that we're done with it.

    return mappability


def generate_mappability_bed(config, read_length):
    print('Establishing temp path...')
    specifc_temp_dir = os.path.join(config['TMP_PATH'], config['GENOME_BUILD'], str(read_length))
    toolbox.establish_path(specifc_temp_dir, silent=False)

    print('Filtering out multi-mappers...')
    aligned_reads_filepath = os.path.join(specifc_temp_dir, 'mappable_samfile.sam')
    filtered_sam_filepath = os.path.join(specifc_temp_dir, 'mappable_filtered_samfile.sam')
    print(smart_run(pp_filteralignments.filter_multimappers,
                    dict(config=config, input_filename=aligned_reads_filepath, output_filename=filtered_sam_filepath),
                    input_filename=aligned_reads_filepath, output_filename=filtered_sam_filepath))

    print('Generating BAM file from SAM file...')
    bam_filepath = os.path.join(specifc_temp_dir, 'mappable_bamfile.bam')
    print(smart_run(pp_filteralignments.convert_to_bam,
                    dict(config=config, input_filename=filtered_sam_filepath, output_filename=bam_filepath),
                    input_filename=filtered_sam_filepath, output_filename=bam_filepath))

    print('Sorting BAM file...')
    sorted_fileprefix = os.path.join(specifc_temp_dir, 'mappable_sorted_bamfile')
    sorted_filepath = os.path.join(specifc_temp_dir, 'mappable_sorted_bamfile.bam')
    print(smart_run(pp_filteralignments.sort_bam,
                    dict(config=config, input_filename=bam_filepath, output_filename=sorted_fileprefix),
                    input_filename=bam_filepath, output_filename=sorted_filepath))

    print('Indexing BAM file...')
    bam_index_filepath = os.path.join(specifc_temp_dir, 'mappable_sorted_bamfile.bam.bai')
    print(smart_run(pp_filteralignments.index_bam, dict(config=config, input_filename=sorted_filepath),
                    input_filename=sorted_filepath, output_filename=bam_index_filepath))

    genome_path = toolbox.parse_path(config['REFERENCE_GENOME_PATH'])[0]
    mappability_bed_filepath = os.path.join(genome_path,
                                            '{}_mappable_regions_{}.bed'.format(config['GENOME_BUILD'], read_length))

    print('Generating BED file of alignable regions...')
    smart_run(covered_regions_to_bed, dict(input_bam_filename=sorted_filepath,
                                           output_bed_filename=mappability_bed_filepath, starts_only=False),
              input_filename=sorted_filepath, output_filename=mappability_bed_filepath)

    starts_bed_filepath = os.path.join(genome_path,
                                       '{}_start_regions_{}.bed'.format(config['GENOME_BUILD'], read_length))
    print('Generating BED file of alignable start sites...')
    smart_run(covered_regions_to_bed, dict(input_bam_filename=sorted_filepath,
                                           output_bed_filename=starts_bed_filepath, starts_only=True),
              input_filename=sorted_filepath, output_filename=starts_bed_filepath)

    print('Deleting intermediate files...')
    os.remove(os.path.join(specifc_temp_dir, 'mappable_samfile.sam'))
    os.remove(os.path.join(specifc_temp_dir, 'mappable_filtered_samfile.sam'))
    os.remove(os.path.join(specifc_temp_dir, 'mappable_bamfile.bam'))
    os.remove(os.path.join(specifc_temp_dir, 'mappable_sorted_bamfile.bam'))
    os.remove(os.path.join(specifc_temp_dir, 'mappable_sorted_bamfile.bam.bai'))


def generate_all_reads(genome_filepath, reads_filepath, read_length):
    """
    :param genome_filepath:
    :param read_length:
    :return:

    Generates a FASTA file containing all possible reads of length <read_length> from <genome_filepath> and outputs it to <reads_filepath>
    """
    # parse FASTA file one sequence at a time to keep memory footprint reasonable

    start_time = datetime.datetime.now()
    with open(genome_filepath, 'rU') as genome_file:
        with open(reads_filepath, 'w') as reads_file:
            print(('Generating {} with all possible reads of length {} from genome {}'.format(reads_filepath,
                                                                                             read_length,
                                                                                             genome_filepath)))
            done = False
            cur_sequence = ''
            # cur_line = genome_file.next()
            while not done:
                try:
                    cur_line = next(genome_file)
                except StopIteration:
                    done = True
                if cur_line.startswith('>') or done:
                    for start_pos in range(len(cur_sequence) - read_length + 1):
                        reads_file.write(
                            cur_sequence[start_pos:start_pos + read_length] + '\n')  # write every possible read
                        # reads_file.write(toolbox.rev_complement(cur_sequence[start_pos:start_pos+read_length])+'')  # and its reverse complement
                    cur_sequence = ''
                else:
                    cur_sequence += cur_line.strip('\n')
            print(('Done in {}'.format(datetime.datetime.now() - start_time)))


def align_to_self(config, bowtie2_index_filepath, reads_filepath, output_sam_filepath, read_length):
    """
    Performs an alignment of the reads in <reads_filepath> against the reference genome specified by the config.
    Parses the bowtie2 output to determine the number of mappable bases.
    Also generates a BED file containing all mappable regions for this current <read_length> and outputs it to
    the same path as the reference genome.

    :param config:
    :param bowtie2_index_filepath:
    :param reads_filepath:
    :param read_length:
    :return:
    """
    start_time = datetime.datetime.now()
    print('Aligning reads to genome index {}'.format(bowtie2_index_filepath))

    cmd_line = [config['BOWTIE2_PATH'], '-r', '-N', '0', '-D', '0', '-R', '0', '--dpad', '0', '--score-min',
                '\'C,0,-1\'', '-p', str(config['THREADS']), '--no-unal', '-x', bowtie2_index_filepath, '-U',
                reads_filepath,
                '-S', output_sam_filepath]

    print('using command line: {}'.format(' '.join(cmd_line)))

    process_output = subprocess.check_output(cmd_line, stderr=subprocess.STDOUT).decode()
    print(process_output)
    bowtie2_stats = parse_bowtie2_output(process_output)

    print('Done in {}'.format(datetime.datetime.now() - start_time))
    return bowtie2_stats['aligned_1']


def parse_bowtie2_output(bowtie2_output_text):
    # parse the output:
    results = {}
    reads_match = re.search(r'(\d+) reads; of these:', bowtie2_output_text)
    if reads_match:
        results['total reads'] = int(reads_match.group(1))
    else:
        results['total reads'] = -1

    aligned_0_match = re.search(r'\s+(\d+)\s+\([\d.]+%\)\s+aligned 0 times', bowtie2_output_text)
    if aligned_0_match:
        results['aligned_0'] = int(aligned_0_match.group(1))
    else:
        results['aligned_0'] = -1

    aligned_1_match = re.search(r'\s+(\d+)\s+\([\d.]+%\)\s+aligned exactly 1 time', bowtie2_output_text)
    if aligned_1_match:
        results['aligned_1'] = int(aligned_1_match.group(1))
    else:
        results['aligned_1'] = -1

    aligned_multi_match = re.search(r'\s+(\d+)\s+\([\d.]+%\)\s+aligned >1 times', bowtie2_output_text)
    if aligned_multi_match:
        results['aligned_multi'] = int(aligned_multi_match.group(1))
    else:
        results['aligned_multi'] = -1
    return results


def covered_regions_to_bed(input_bam_filename, output_bed_filename, starts_only=False):
    """
    If <starts_only> is True, analyzes <input_bam_filename> to generate a BED file of all regions with a read starting
     at that position and outputs it to <output_bed_filename>.
    Otherwise, do the same thing for regions with coverage > 0 (i.e. covered by any portion of a read)

    :param input_bam_filename:
    :param output_bed_filename:
    :return:
    """

    def covered_regions(bam_file, starts_only=False):
        chroms = [x['SN'] for x in bam_file.header['SQ']]
        regions = {}
        # print 'chromosomes: {}'.format(chroms)
        for chrom in chroms:
            # print 'processing chromosome {}'.format(chrom)
            regions[chrom] = []
            current_region_start = 0
            previous_pos = -1
            if starts_only:
                # only record regions covered by a start position
                for read in bam_file.fetch(reference=chrom):
                    if read.pos - previous_pos > 1:
                        # there is a gap between start-covered regions
                        if previous_pos >= 0:
                            # this must not be the first region transition, so we need to wrap up the region we just finished
                            regions[chrom].append((current_region_start, previous_pos))
                        current_region_start = read.pos
                    previous_pos = read.pos
            else:
                for x in bam_file.pileup(chrom):
                    # record regions covered by any part of a read
                    if x.n > 0:
                        if x.pos - previous_pos > 1:  # we've left the old region behind and are starting a new one
                            if previous_pos >= 0:  # if this is not the first region transition, then we're finishing an old one
                                regions[chrom].append((current_region_start, previous_pos))
                            current_region_start = x.pos
                        previous_pos = x.pos
            if previous_pos:  # finish final region
                regions[chrom].append((current_region_start, previous_pos))
        return regions

    def regions_to_BED(regions, bed_filename):
        # print 'regions_to_BED'
        with open(bed_filename, 'w') as bed_file:
            bed_writer = csv.writer(bed_file, dialect=csv.excel_tab)
            for chrom in sorted(regions.keys()):
                for region in regions[chrom]:
                    bed_writer.writerow([chrom, region[0], region[
                        1] + 1])  # add one to the end position to comply with semi-open interval of BED files

    samfile = pysam.Samfile(input_bam_filename, 'rb')
    print(('Computing regions covered by {} in {}'.format(('reads', 'read starts')[starts_only], input_bam_filename)))
    print(('Outputting to {}'.format(output_bed_filename)))

    regions_to_BED(covered_regions(samfile, starts_only=starts_only), output_bed_filename)


def main():
    parser = argparse.ArgumentParser(
        description='Returns or computes the mappability of a genome for a given read size. Will update a table of mappability values by read length stored in the same folder as the reference genome.')
    parser.add_argument('config_file', help='The file that contains the configuration and parameters for this pipeline')
    parser.add_argument('read_length', type=int, help='Read length for which we want to compute mappability')
    # parser.add_argument('--count', '-c', action = 'store_true')
    parser.add_argument('--regions', '-r', action='store_true')
    args = parser.parse_args()

    config = pp_config.read_config(args.config_file)

    mappability = get_mappability(config, args.read_length, make_region_file=args.regions)
    print(('Total mappable basepairs = {} with read length {}'.format(mappability, args.read_length)))


def test():
    # print generate_BED_file(config=pp_config.read_config('config/sc_local.txt'), read_length=10)
    print((covered_regions_to_bed('/home/phage/oasis/tmp/mappable_sorted_bamfile.bam',
                                 '/home/phage/oasis/tmp/mouse_mappable_regions_42.bed')))


if __name__ == '__main__':
    # test()
    main()
