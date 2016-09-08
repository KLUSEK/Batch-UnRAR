#!/usr/bin/env python

import os, sys

class Unrar(object):
    def __init__(self):
        # Class Variables
        #------------------
        self.unrar_bin = '/usr/bin/unrar'
        self.mark_file_name = '.unrared'
        self.extensions_unrar = ['.rar', '.r01']        # List of extensions for auto-extract to look for
        self.supported_filetypes = []                   # Filled by extensions_list function
        self.extensions_list()

        # Check for proper number of parameters (TODO: and that parameters are correct)
        if len(sys.argv) < 2:
            self.display_help()
        # Check that we can find unrar on this system
        self.unrar_check()
        # Check that the download directory parameters is actually a directory
        self.check_arguments()
        # self.traverse_directories()
	self.scan_for_archives(self.download_dir)

    '''Displays script command line usage help'''
    def display_help(self):
        print 'usage: ' + sys.argv[0] + ' [options] [download_directory]'
        print 'options:'
        print '     -h, --help      Display this help message'
        exit()

    '''Creates the list of extensions supported by the script'''
    def extensions_list(self):
        self.supported_filetypes.extend(self.extensions_unrar)       # rar support

    '''Sanity check to make sure unrar is found on the system'''
    def unrar_check(self):
        if self.unrar_bin == False:
            print 'Error: ' + self.unrar_bin + ' not found in the system path \n'
            exit()

    '''Ensure download dir argument is in fact a directory'''
    def check_arguments(self):
        if os.path.isdir(sys.argv[1]):
            self.download_dir = os.path.abspath(sys.argv[1])

    '''Scan the download directory and its subdirectories'''
    def traverse_directories(self):
        # Search download directory and all subdirectories
        for dirname, dirnames, filenames in os.walk(self.download_dir):
            self.scan_for_archives(dirname)

    '''Check for rar files in each directory'''
    def scan_for_archives(self, dir):
        # Look for a .rar archive in dir
        found = False
        dir_listing = os.listdir(dir)
        # First archive that is found with .rar extension is extracted
        # (for directories that have more than one archives in it)
        for filename in dir_listing:
            for ext in self.supported_filetypes:
                if filename.endswith(ext):
                   # If a .rar archive is found, check to see if it has been extracted previously
                   print "Need to extract: " + filename
                   # Start extracting file
                   self.start_unrar(dir, filename)
                   found = True
                   break

            if (found == True):
	        break


    '''Extract a rar archive'''
    def start_unrar(self, dir, archive_name):
        # Create command line arguments for rar extractions
        cmd_args = ['','','','','']
        cmd_args[0] = self.unrar_bin                    # unrar
        cmd_args[1] = 'x'                               # command line switches: x - extract
        cmd_args[2] = '-y'                              # y - assume yes to all queries (overwrite)
        cmd_args[3] = os.path.join(dir, archive_name)   # archive path
        cmd_args[4] = dir                               # destination

        try:
            os.spawnv(os.P_WAIT, self.unrar_bin, cmd_args)
            print 'Done.'
        except OSError:
            print 'Error: ' + self.unrar_bin + ' not found in the given path \n'
            exit()

if __name__ == '__main__':
    obj = Unrar()
