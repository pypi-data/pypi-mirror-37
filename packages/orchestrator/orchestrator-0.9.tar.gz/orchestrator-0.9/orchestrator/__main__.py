#!/usr/bin/python3

import xml.etree.ElementTree as ET
import shlex
import subprocess
import argparse
import time

'''
import logging
logging.basicConfig()
log = logging.getLogger(__file__)

log.info ('----------------------')
log.info (' Volcano Orchestrator ')
log.info ('----------------------')
'''

# Parse arguments
g_parser = argparse.ArgumentParser()
g_parser.add_argument('--bin', dest='bin')
g_args = g_parser.parse_args()

g_args.pipe_streams = False
g_args.default_process_restart_timeout_sec = 1.0

#g_WorkingDir = os.getcwd()

class VolcanoProcess:
    def __init__(self, node):
        original_exec = node.attrib.get('file', '')
        if original_exec=='':
            raise Exception ('Error parsing config file: attribute "file" not specified for node')

        self.name_ = node.attrib.get('name', original_exec)
        self.restart = node.attrib.get('restart', '1')=='1'

        '''
        if g_args.bin is not None and original_exec[0]!='/' and original_exec[0]!='.':
            self.executable = g_args.bin + '/' + original_exec
        else:
            self.executable = original_exec
        '''
        self.executable = original_exec
        self.params = node.attrib.get('params', '')
        self.process = None
        self.process_die_time = None

    def name(self):
        return self.name_

    def launch(self):
        if self.params=='':
            args=[]
        else:
            args=shlex.split(self.params)
        args.insert (0, self.executable)
        
        self.process_die_time = None
        if g_args.pipe_streams:
            self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            self.process = subprocess.Popen(args)

    def communicate(self):
        ret_code = self.process.poll()
        if ret_code is None:
            # Process still running
            if g_args.pipe_streams:
                line = self.process.stdout.readline()
                while line != '':
                    msg = line.decode('utf-8').rstrip('\r\n')  # to prevent printing several newlines
                    print ('{} {}'.format(self.name(), msg))
                    line = self.process.stdout.readline()
        else:
            if self.restart:
                if self.process_die_time is None:   # just noticed!
                    print ('%s failed with code %d. Relaunching' % (self.name(), ret_code))
                    self.process_die_time = time.perf_counter()
                elif (time.perf_counter() - self.process_die_time) > g_args.default_process_restart_timeout_sec:
                    self.launch ()
            else:
                print ('%s failed with code %d. No restart, exiting' % (self.name(), ret_code))
                return ret_code
        return None


g_Processes = []

g_tree = ET.parse('proc.xml')
for node in g_tree.getroot():
    if node.tag=='Proc': # Lib for compatability with prev volcano
        g_Processes.append ( VolcanoProcess(node) )

if len(g_Processes)==0:
    raise Exception('No processes specified')

try:
    for p in g_Processes:
        print ('Launching %s...' % p.name())
        p.launch ()
    # if we dont pipe streams (processes just inherit stdout) we dont need to check very often
    sleep_time_sec = 1.0 if g_args.pipe_streams else 0.1

    stop = False
    while not stop:
        time.sleep (sleep_time_sec)
        for p in g_Processes:
            ret_code = p.communicate ()
            if ret_code is not None:
                stop = True
                break   # exit for-loop

except KeyboardInterrupt:
    print ("\n\n << Keyboard interrupt >> \n\n")
finally:
    print ("Stop all processes...")
    for p in g_Processes:
        if p.process is not None:
            print ("Killing %s..." % p.name())
            p.process.kill()
            print ("Killed %s..." % p.name())

