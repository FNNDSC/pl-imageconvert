#!/usr/bin/env python                                            
#
# imageconvert ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp
from pyimgconvert  import pyimgconvert

Gstr_title = """

       _        _                                                          _   
      | |      (_)                                                        | |  
 _ __ | |______ _ _ __ ___   __ _  __ _  ___  ___ ___  _ ____   _____ _ __| |_ 
| '_ \| |______| | '_ ` _ \ / _` |/ _` |/ _ \/ __/ _ \| '_ \ \ / / _ \ '__| __|
| |_) | |      | | | | | | | (_| | (_| |  __/ (_| (_) | | | \ V /  __/ |  | |_ 
| .__/|_|      |_|_| |_| |_|\__,_|\__, |\___|\___\___/|_| |_|\_/ \___|_|   \__|
| |                                __/ |                                       
|_|                               |___/                                        

"""

class Imageconvert(ChrisApp):
    """
    An app to ....
    """
    AUTHORS                 = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A ChRIS plugin app that acts as a Python wrapper around Linux CLI "convert" which works as an entrypoint around the Linux image processing ImageMagick.'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'An app to ...'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '0.1'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """

        self.add_argument('-i', '--inputFile', dest='inputFile', type=str,
                          optional=False, help='name of the input file within the inputDir')

        self.add_argument('-o', '--outputFile', dest='outputFile', type=str, optional=True,
                          help='output file', default='sample')

        self.add_argument("-a", "--args", dest='args', type=str,
                           optional=True, default="", help="medcon arguments to pass")

        self.add_argument('-y', '--synopsis', dest='synopsis', type=bool, action='store_true',
                          default=False, optional=True, help='short synopsis')


    def show_man_page(self, ab_shortOnly=False):
        """
        Print the app's man page.
        """

        scriptName = os.path.basename(sys.argv[0])
        shortSynopsis = '''

        NAME

        imageconvert.py - converts images to the desired format

        SYNOPSIS

            python imageconvert.py                                         \\
                [-i <inputFile>] [--inputFile <inputFile>]                  \\
                [-o <outputFile>] [--ouputFile <outputFile>]                \\
                [-a <args>] [--args <args>]                                 \\
                [-h] [--help]                                               \\
                [--json]                                                    \\
                [--man]                                                     \\
                [--meta]                                                    \\
                [--savejson <DIR>]                                          \\
                [-v <level>] [--verbosity <level>]                          \\
                [--version]                                                 \\
                <inputDir>                                                  \\
                <outputDir> 


        ''' %scriptName
        description = '''

        DESCRIPTION

        Python wrapper around Linux CLI "convert" which works as 
        an entrypoint around the Linux image processing 'ImageMagick'.

        ARGS

            [-I|--inputDir <inputDir>]  
            Input directory that contains the image files to convert 

            [-i|--inputFile <inputFile>]
            Input file within the inputDir that needs to be converted  

            [-O|--outputDir <outputDir>]                            
            Output Directory that will store the required output  

            [-o|--outputFile <outputFile>]
            Name of the outputFile that should be used to store the resultant
            output in the outputDir

            [-a|--args <convertArgsToPass>]
            Arguments that are upposed to be passed to the "magick convert"

            [-x|--man]
            Show full help.

            [-y|--synopsis]
            Show brief help.

            [--version]
            If specified, print the version number and exit.

            [-v|--verbosity <level>]
            Set the app verbosity level. 

            GITHUB
                 o See https://github.com/FNNDSC/pyimgconvert for more help and source.
        ''' % (scriptName)

        if ab_shortOnly:
            return shortSynopsis
        else:
            return shortSynopsis + description

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())

        options.inputDir        = options.inputdir
        options.outputDir       = options.outputdir
        options.inputFile       = options.inputFile
        options.outputFile      = options.outputFile
            
        imgConverter = pyimgconvert.object_factoryCreate(options).C_convert

        if options.version:
            print("Version: %s" % options.version)
            sys.exit(1)

        if options.man or options.synopsis:
            if options.man:
                str_help = self.show_man_page(False)
            else:
                str_help = self.show_man_page(True)
            print(str_help)
            sys.exit(1)

        imgConverter.img_convert()

# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Imageconvert()
    chris_app.launch()
