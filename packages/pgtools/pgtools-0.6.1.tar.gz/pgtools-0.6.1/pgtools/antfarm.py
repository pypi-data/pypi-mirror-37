"""
Idea:

Create a class that implements a kludgy, disk-I/O-based multiprocessing system. By keeping exchanged arrays on disk
and spawning separate subprocesses for the workers, we keep memory footprint to a minimum while taking advantage
of parallel processing for improved runtime.
"""

import os
import sys
import shutil
# import collections
import subprocess
import time
import datetime

import numpy



from pgtools import toolbox

DEBUG = False
RANDOM_IDENTIFIER_SIZE = 32
MAX_THREADS = 31
SLEEP_DELAY = 1
IDLE_STATUS_INTERVAL = 60

COMPLETE_FLAG_FNAME_TEMPLATE = '{}_complete'
INPUT_FNAME_TEMPLATE = '{}_input_{}.npy'
OUTPUT_FNAME_TEMPLATE = '{}_output_{}.npy'

# PYTHON_CALL = os.path.join(os.environ['HOME'], 'anaconda/bin/python')
PYTHON_CALL = 'python'
#PYTHON_CALL = ''

class AntFarm(object):
    # Assume first parameter is the base path

    def __init__(self, slave_script, base_path, job_dict, max_threads=MAX_THREADS, debug=True):
        """
        :param slave_script: fully-qualified path to a python script that will execute each job
        :param base_path:
        :param job_dict: keyed by external job identifier (e.g. chromosome name)
            contains a dict of:
                inputs: ordered list of numpy arrays to be passed as input to worker script
                num_outputs: number of numpy arrays to be returned from worker script
                params: list of all other parameters to be passed to worker script
        :param max_threads:
        :param debug:
        :return:
        """
        self.max_threads = max_threads
        self.debug = DEBUG

        self.overall_id = toolbox.random_identifier(32)
        self.base_path = os.path.join(base_path, 'AntFarm_colony_{}'.format(self.overall_id))

        toolbox.establish_path(self.base_path)

        self.slave_script = slave_script

        # re-key the passed job dictionary to use internal random identifiers
        self.pending = []
        self.job_dict = {}
        for external_job_id in job_dict:
            new_id = toolbox.random_identifier(RANDOM_IDENTIFIER_SIZE)
            self.job_dict[new_id] = job_dict[external_job_id]
            self.job_dict[new_id]['external_id'] = external_job_id
            self.pending.append(new_id)

        self.pending = self.pending[::-1]  # reverse order since we pop from the end of the list
        self.idle_timer = 1
        self.completed = set([])
        self.active = set([])
        self.results = {}
        self.process_handles = {}
        self.start_times = {}
        self.input_fnames = {}

    def __del__(self):
        self._purge_files()

    def _purge_files(self):
        """
        Remove all temp files
        :return:
        """
        if os.path.exists(self.base_path):
            try:
                shutil.rmtree(self.base_path)
            except (OSError, IOError) as ex:
                print(('Tried to delete {} but caught {} instead'.format(self.base_path, ex)))

    def _print(self, text):
        """
        Only print <text> if self.debug is true
        :param text:
        :return:
        """
        if self.debug:
            print(text)

    def _scanCompleted(self, active_jobs):
        """
        Scans the basepath for marker files that indicate job completion for the given list of active jobs
        and return a list of completed job ids.
        :return:
        """
        # all_files = os.listdir(self.colony_basepath)
        completed_ids = set([])
        for job_id in active_jobs:
            if os.path.isfile(os.path.join(self.base_path, COMPLETE_FLAG_FNAME_TEMPLATE.format(job_id))):
                completed_ids.add(job_id)
        return completed_ids

    def _getResults(self, job_ids):
        """
        Read the output arrays into the results dictionary, reap the process and compute the run time.
        :param jobs_to_process: a list of job_ids
        :return: None
        """
        for job_id in job_ids:
            print(('\t{} done in {}'.format(self.job_dict[job_id]['external_id'], datetime.datetime.now() - self.start_times[job_id])))
            self.results[job_id] = []

            self._print('Deleting input arrays {}'.format(', '.join(self.input_fnames[job_id])))
            for input_fname in self.input_fnames[job_id]:
                    os.remove(input_fname)

            for output_index in range(self.job_dict[job_id]['num_outputs']):
                self._print('Loading output array {} for job {}'.format(output_index, job_id))
                result_fname = os.path.join(self.base_path, OUTPUT_FNAME_TEMPLATE.format(job_id, output_index))
                self.results[job_id].append(
                    numpy.load(result_fname))

                self._print('Deleting output array {}'.format(result_fname))
                os.remove(result_fname)

            indicator_fname = os.path.join(self.base_path, COMPLETE_FLAG_FNAME_TEMPLATE.format(job_id))
            self._print('Deleting indicator file {}'.format(indicator_fname))
            os.remove(indicator_fname)

            self._print('Reaping process for {}'.format(job_id))
            self.process_handles[job_id].wait()

        return

    def _startProcess(self):
        """
        Executes the next job_id in the self.pending queue, and moves its ID to self.active

        Command line format:
            python <slave_script> <base_path> <job_id> <input_array_filenames> <params>

        where <input_array_filenames> are given as a comma-separated list
        :return:
        """
        assert len(self.pending) > 0
        new_job_id = self.pending.pop()
        self.active.add(new_job_id)

        # Prepare input arrays as files.

        input_array_fnames = []
        for input_index, input_array in enumerate(self.job_dict[new_job_id]['inputs']):
            input_array_fname = os.path.join(self.base_path, INPUT_FNAME_TEMPLATE.format(new_job_id, input_index))
            input_array_fnames.append(input_array_fname)
            self._print('Saving input array {} for job {} to {}'.format(input_index, new_job_id, input_array_fname))
            numpy.save(input_array_fname, input_array)
            self._print('\tDone.')

        cmd_line = [PYTHON_CALL, self.slave_script, self.base_path, new_job_id, ','.join(input_array_fnames)] + [str(p)
                                                                                                                 for
                                                                                                              p in
                                                                                                              self.job_dict[
                                                                                                                  new_job_id][
                                                                                                                  'params']]
        print('Starting {} ...'.format(self.job_dict[new_job_id]['external_id']))
        self._print('Starting subprocess for job {} ({}) with command line {}'.format(new_job_id,
                                                                                 self.job_dict[new_job_id][
                                                                                           'external_id'],
                                                                                       ' '.join(cmd_line)))

        self.start_times[new_job_id] = datetime.datetime.now()
        self.process_handles[new_job_id] = subprocess.Popen(cmd_line)
        self.input_fnames[new_job_id] = input_array_fnames
        self.idle_timer = 1

    def execute(self):
        """
        Run all the jobs in the job queue and return control to the calling process when done.
        :return:
        """
        overall_start_time = datetime.datetime.now()
        while len(self.active) > 0 or len(self.pending) > 0:
            if len(self.active) > 0:
                newly_completed = self._scanCompleted(self.active)
                if newly_completed:
                    self.idle_timer = 1
                    self._print('Found {} newly completed jobs: {}'.format(len(newly_completed),
                                                                            ', '.join(list(newly_completed))))
                    self.completed.update(newly_completed)  # add newly-completed jobs to completed
                    self.active.difference_update(newly_completed)  # and remove them from active
                    self._getResults(newly_completed)  # get results and clean up
            # start new jobs if slots are available
            while self.max_threads - len(self.active) > 0 and len(self.pending) > 0:
                self._startProcess()
            time.sleep(SLEEP_DELAY)  # slow down our polling a bit to avoid disk thrashing
            self.idle_timer = (self.idle_timer + 1) % IDLE_STATUS_INTERVAL
            if self.idle_timer == 0:
                self._print('Waiting for {} jobs to complete: {}'.format(len(self.active), ', '.join(
                    [self.job_dict[job_id]['external_id'] for job_id in self.active])))

        self._print('All done in {}'.format(datetime.datetime.now() - overall_start_time))

        # return results dictionary re-keyed back to external job IDs
        return dict(((self.job_dict[job_id]['external_id'], self.results[job_id]) for job_id in self.results))
