# Python object for simple interfacing with bdata objects. 
# Derek Fujimoto
# Oct 2018

from bdata import bdata,bdict
import numpy as np

# =========================================================================== #
class betapy(object):
    """
        Class fields depend on bdata object fields. 
    """
    
    # dictionary holding descriptions of attributes
    _descr_dict = {
        'bdata':            'bdata object',
        
        'Bn':               'Backward detector counts, negative helicity',
        'Bp':               'Backward detector counts, positive helicity',
        'Fp':               'Forward detector counts, positive helicity',
        'Fn':               'Forward detector counts, negative helicity',
        'Ln':               'Left detector counts, negative helicity',
        'Lp':               'Left detector counts, positive helicity',
        'Rn':               'Right detector counts, negative helicity',
        'Rp':               'Right detector counts, positive helicity',
        
        'NBMBp':            'Neutral beam monitor backward detector counts, positive helicity',
        'NBMBn':            'Neutral beam monitor backward detector counts, negative helicity',
        'NBMFp':            'Neutral beam monitor forward detector counts, positive helicity',
        'NBMFn':            'Neutral beam monitor forward detector counts, negative helicity',
        
        'Rb_Cell_mV_set':   'Set voltages of Rb cell (V)',
        
        'asymf':            'Frequency associated with asymmetry calculation in Hz',
        'asymt':            'Time associated with asymmetry calculation in seconds',
        'asymt':            'Voltage associated with asymmetry calculation in volts',
        
        'asymc':            'Combined asymmetry',
        'asymp':            'Positive helicity asymmetry',
        'asymn':            'Negative helicity asymmetry',
        
        'asymp_raw':        'Positive helicity asymmetry (uncombined)',
        'asymn_raw':        'Negative helicity asymmetry (uncombined)',
        
        'alpha_diff':       'Alpha diffusion ratio: N_alph/N_beta',
        
        'asymp_wiA_atag':   'Beta positive helicity asymmetry with alpha coincidence',
        'asymn_wiA_atag':   'Beta negative helicity asymmetry with alpha coincidence',
        'asymc_wiA_atag':   'Beta combined helicity asymmetry with alpha coincidence',
        'asymp_noA_atag':   'Beta positive helicity asymmetry with alpha not in coincidence',
        'asymn_noA_atag':   'Beta negative helicity asymmetry with alpha not in coincidence',
        'asymc_noA_atag':   'Beta combined helicity asymmetry with alpha not in coincidence',
    
        'asym_dif_p':       'Difference combined, positive helicity asymmetry as a function of freq.',
        'asym_dif_n':       'Difference combined, negative helicity asymmetry as a function of freq.',
        'asym_dif_c':       'Difference combined, combined helicity asymmetry as a function of freq.',
        
        'asym_sl_p':        'Slope combined, positive helicity asymmetry as a function of freq.',
        'asym_sl_n':        'Slope combined, negative helicity asymmetry as a function of freq.',
        'asym_sl_c':        'Slope combined, combined helicity asymmetry as a function of freq.',
        
        'asym_raw_p':       'Positive helicity raw asymmetry keyed by [freq,time]',
        'asym_raw_n':       'Negative helicity raw asymmetry keyed by [freq,time]',
        'asym_raw_c':       'Combined helicity raw asymmetry keyed by [freq,time]',
            
        'start_time':       'Epoch time of start of run',
        'end_time':         'Epoch time of end of run',
        'duration':         'Duration of run in s',
    }
            
    # list of keys to skip printing description
    _skiplist = [ 'Const','FluM2']
    
    # ======================================================================= #
    def __init__(self,run,year=0):
        """
            Read bdata object and organize fields.
        """
        
        # read
        bd = bdata(run,year)
        setattr(self,'bdata',bd)
        
        # assign all non-bdict , non-list objects
        for k in bd.__dict__.keys():
            d_ele = getattr(bd,k)
            if type(d_ele) != bdict and 'list' not in k:
                setattr(self,k.replace(' ','_'),d_ele)
        
        # assign histograms
        for k in bd.hist.keys():
            key = k.replace('+','p').replace('-','n').replace(' ','_')
            setattr(self,key,bd.hist[k].data)
        
        # assign variables
        for k in bd.ppg.keys():
            if k in ['mode','init_mode']:
                setattr(self,k.replace(' ','_'),bd.ppg[k].units)
            else:
                setattr(self,k.replace(' ','_'),bd.ppg[k].mean)
            self._descr_dict[k] = bd.ppg[k].description
        
        for k in bd.camp.keys():
            setattr(self,k.replace(' ','_'),bd.camp[k].mean)
            setattr(self,k+'_std',bd.camp[k].std)
            self._descr_dict[k] = bd.camp[k].description
            
        for k in bd.epics.keys():
            setattr(self,k.replace(' ','_'),bd.epics[k].mean)
            setattr(self,k+'_std',bd.epics[k].std)
            self._descr_dict[k] = bd.epics[k].description
            
        # assign beam energy
        try:
            setattr(self,'beam_kev',bd.beam_kev())
            self._descr_dict['beam_kev'] = 'Implantation energy at the sample in keV'
        except Exception as err:
            pass
        
        # set asymmetries
        self.set_asym()
        
        # set doctring
        self.set_asym.__func__.__doc__ = self.set_asym.__doc__+\
                                         self.bdata.asym.__doc__
        
    # ======================================================================= #
    def __repr__(self):
        """
            Nice printing of parameters.
        """
        
        d = self.__dict__
        dkeys = list(d.keys())
        
        if dkeys:
            items = []
            dkeys.sort()
            
            for key in dkeys:
                
                # skip conditions
                if  (key in self._skiplist) or \
                    ('_err' in key) or \
                    ('_std' in key) or \
                    (key[0] == '_'):
                        
                    continue
                
                # format output
                if key in self._descr_dict.keys():
                    items.append([key,self._descr_dict[key]])
                elif not hasattr(d[key],'__iter__'):
                    items.append([key,d[key]])                
                elif d[key].__class__ == str:
                    items.append([key,d[key]])                
                else:
                    items.append([key,d[key].__class__])
                
                            
            m = max(map(len,dkeys)) + 1
            s = '\n'.join([k.rjust(m)+': '+str(v) for k, v in sorted(items)])
            return s
        else:
            return self.__class__.__name__ + "()"

    # ======================================================================= #
    def set_asym(self,**asym_args):
        """
        Reset asymmetry data fields. Inputs are passed to bdata.asym. 
        Note: "option" input is unused. 

        bdata.asym docstring follows 

        ======================================================================
            
        """
        
        # remove option
        if 'option' in asym_args.keys():
            del asym_args['option']
    
        # get bdata object
        bd = self.bdata
    
        # get axis 
        if bd.mode in ['20','2h']:
            x = 'asymt'
        elif bd.mode == '1n':
            x = 'asymv'
        elif bd.mode == '1f':
            x = 'asymf'
        else:
            x = 'asyx'
        
        # assign asymetries
        if self.mode != '2e':
            
            # combined and split helicities
            for i in 'cpn':
                try: 
                    a = bd.asym(i,**asym_args)
                except Exception as err:
                    print(err)
                else:
                    setattr(self,x,a[0])
                    setattr(self,'asym%s'%i,a[1])
                    setattr(self,'asym%s_err'%i,a[2])
            
            # alpha diffusion and tagging
            if self.mode == '2h':
                try: 
                    a = bd.asym('ad',**asym_args)
                except Exception as err:
                    print(err)
                else:
                    setattr(self,x,a[0])
                    setattr(self,'alpha_diff',a[1])
                    setattr(self,'alpha_diff_err',a[2])
                
                try: 
                    a = bd.asym('at',**asym_args)
                except Exception as err:
                    print(err)
                else:
                    setattr(self,x,a['time_s'])
                    for i in a.keys():
                        if 'T' not in i and 'time' not in i:                        
                            setattr(self,'asym%s_atag'%i,a[i][0])
                            setattr(self,'asym%s_atag_err'%i,a[i][1])
                        
            # raw scans
            if self.mode in ['1f','1n']:
                try: 
                    a = bd.asym('r',**asym_args)
                except Exception as err:
                    print(err)
                else:
                    setattr(self,'asymp_raw',a['p'][0])
                    setattr(self,'asymp_raw_err',a['p'][1])
                    setattr(self,'asymn_raw',a['n'][0])
                    setattr(self,'asymn_raw_err',a['n'][1])
        
        # 2e mode
        else:
            try: 
                a = bd.asym()
            except Exception as err:
                print(err)
            else:
                for k in a.keys():
                    if k not in ['freq','time']:
                        setattr(self,'asym_%s'%k,a[k][0])
                        setattr(self,'asym_%s_err'%k,a[k][1])
                    else:
                        setattr(self,'asymt',a[k])
    
