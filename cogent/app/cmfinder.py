#!/usr/bin/env python

from cogent.app.util import CommandLineApplication, \
     CommandLineAppResult, ResultPath
from cogent.app.parameters import Parameter, FlagParameter, ValuedParameter,\
     MixedParameter,Parameters
from sys import exit
from os.path import isfile

class CMfinder(CommandLineApplication):
    """The application controller for CMfinder 0.2 application


    Options:
    -b               Do not use BLAST search to locate anchors
    -v               Verbose. Print running information, and save intermediate
                     results
    -c <number>      The maximum number of candidates in each sequence. Default
                     40. No bigger than 100.
    -m <number>      The minimum length of candidates. Default 30
    -M <number>      The maximum length of candidates. Default 100
    -n <number>      The maximum number of output motifs. Default 3
    -f <number>      The fraction of the sequences expected to contain the
                     motif. Default 0.80
    -s <number>      The number of stem-loops in the motif
    -h               Show help


    """
    #-n default is 3, set to 3 because of resultpath concerns
    _parameters = {
        '-b':FlagParameter(Prefix='-',Name='b',Value=True), 
        '-v':FlagParameter(Prefix='-',Name='v'),
        '-c':ValuedParameter(Prefix='-',Name='c',Value=None,Delimiter=' '),
        '-m':ValuedParameter(Prefix='-',Name='m',Value=None,Delimiter=' '),
        '-M':ValuedParameter(Prefix='-',Name='M',Value=None,Delimiter=' '),
        '-n':ValuedParameter(Prefix='-',Name='n',Value=3,Delimiter=' '),
        '-f':ValuedParameter(Prefix='-',Name='f',Value=None,Delimiter=' '),
        '-s':ValuedParameter(Prefix='-',Name='s',Value=None,Delimiter=' ')}
    _command = 'cmfinder.pl'
    _input_handler = '_input_as_string'


    def _get_result_paths(self,data):
        """Specifies the paths of output files generated by the application
        
        data: the data the instance the application is called on
        
        CMfinder produces it's output in two files .align and .motif
        it also prints an output to sdtout.

        """
        result={}
        if not isinstance(data,list):
            inputPath = str(data)
        else:
            inputPath=self._input_filename
        itr=self.Parameters['-n'].Value
        for i in range(itr):
            nr=str(i+1)
            try:           #unknown nr of output files
                f = open((inputPath+'.motif.h1.'+nr))  #if exists add to path
                f.close()
                result[('cm_'+nr)] =\
                    ResultPath(Path=(inputPath+'.cm.h1.'+nr))
                result[('motif_'+nr)] =\
                    ResultPath(Path=(inputPath+'.motif.h1.'+nr))
            
            except IOError: # else no more outputs
                break
        if self._input_filename is not None:
            result['_input_filename'] = ResultPath(self._input_filename)
       
        if isfile(self.WorkingDir+'latest.cm'):
            result['latest'] =\
                ResultPath(Path=(self.WorkingDir+'latest.cm'))
        else:
            pass

        return result

class CombMotif(CommandLineApplication):
    """
    Application controller for the combmotif.pl program

    Only works for input as string since filnames are needed to located input
    """
    
    _command = 'CombMotif.pl'
    _input_handler = '_input_as_string'
    
    def _input_as_string(self,data):
        """ Return data as a string """
        input = str(data) +' '+str(data)+'.motif'  
        return input

    def _input_as_lines(self,data):
        """ """
        print 'Use input as string with cmfinder input_filename as input'
        exit(1)

    def _get_result_paths(self,data):
        """Specifies the paths of output files generated by the application
        
        data: the data the instance of the application is called on
        
        CombMotif will generate an output, the combination that was possible,
        the modified _get_result_path will detect that output and return the 
        path to that output file. Since the output is not possible to predict
        one has to try all possible outputs.

        Assumes that one stem loop is used may correct this later
        """
        result={}
        filename = str(data)
        motifList = []
        mnr = 0 #motif number
        if not isinstance(data,list):
            inputPath = str(data)
        else:
            inputPath=self._input_filename
        for h in range(2): #numbers of stem loops in each motif, recommended 1-2
            if h == 0:
                s = '.motif.h1.'
            else:
                s = '.motif.h2.'
            for i in range(1,6):
                for x in range(1,6): #two combined motifs
                    if x == i:
                        continue
                    try:
                        z = str(i)
                        w = str(x)
                        file = filename+s+z+'.'+w
                        f = open((file))
                        #print 'found',file
                        f.close()
                        mnr += 1
                        n = str(mnr)
                        result['comb'+n] = ResultPath(Path=file)
                    except IOError:
                        pass
                    for y in range(1,6): # three combined motifs
                        if y == x:
                            continue
                        try:
                            z = str(i)
                            w = str(x)
                            q = str(y)
                            file = filename+s+z+'.'+w+'.'+q
                            f = open((file))
                            #print 'found', file
                            f.close()
                            mnr += 1
                            n = str(mnr)
                            result['comb'+n] = ResultPath(Path=file)
                        except IOError: 
                            pass
                        for k in range(1,6): # four combined motifs
                            if k == y:
                                continue
                            try:
                                z = str(i)
                                w = str(x)
                                q = str(y)
                                v = str(k)
                                file = filename+s+z+'.'+w+'.'+q+'.'+v
                                f = open(file)
                                #print 'found',file
                                f.close()
                                mnr += 1
                                n = str(mnr)
                                result['comb'+n] = ResultPath(Path=file)
                            except IOError:
                                pass
                            for j in range(1,6): #five combined motifs
                                if j == k:
                                    continue
                                try:
                                    z = str(i)
                                    w = str(x)
                                    q = str(y)
                                    v = str(k)
                                    u = str(j)
                                    file = filename+s+z+'.'+w+'.'+q+'.'+v+'.'+u
                                    f = open(file)
                                    #print 'found',file
                                    f.close()
                                    mnr += 1
                                    n = str(mnr)
                                    result['comb'+n] = ResultPath(Path=file)
                                except IOError:
                                    pass        
        return result
    
