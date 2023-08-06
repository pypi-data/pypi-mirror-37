""" Module for VetRedRockGui
"""
from __future__ import print_function, absolute_import
from __future__ import division, unicode_literals


# import sys
# import pdb

from collections import OrderedDict

# from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMainWindow
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
# from PyQt5 import QtCore

from matplotlib import rcParams

from astropy.units import Quantity
# from astropy import units as u
from astropy.io import fits

from linetools.guis import utils as ltgu
from linetools.guis import line_widgets as ltgl
from linetools.guis import spec_widgets as ltgsp
from linetools.guis import simple_widgets as ltgsm
from linetools.spectra.xspectrum1d import XSpectrum1D
from linetools.spectra import utils as lspu
from linetools import utils as ltu

try:
    basestring
except NameError:  # For Python 3
    basestring = str

class VetRedRockGui(QMainWindow):
    """ GUI for vetting RedRock redshifts
    """
    def __init__(self, redrock_file, parent=None, zdict=None, coadd_dict=None,
                 outfile='tmp.json', unit_test=False, screen_scale=1.,
                 **kwargs):
        QMainWindow.__init__(self, parent)
        """
        redrock_file = str
          Input RedRock output FITS file from our redrock script
        parent : Widget parent, optional
        zsys : float, optional
          intial redshift
        exten : int, optional
          extension for the spectrum in multi-extension FITS file
        norm : bool, optional
          True if the spectrum is normalized
        screen_scale : float, optional
          Scale the default sizes for the gui size
        """
        #reload(ltgl)
        #reload(ltgsp)
        # INIT

        # Load up
        self.outfile = outfile
        self.rr_hdul = fits.open(redrock_file)
        if coadd_dict is not None:
            self.slit_info = {}
            for key in coadd_dict.keys():
                if isinstance(coadd_dict[key], dict):
                    if '2D_xval' in coadd_dict[key].keys():
                        name = coadd_dict[key]['outfile'].replace('.fits','')
                        self.slit_info[name] = {}
                        self.slit_info[name]['xval'] = coadd_dict[key]['2D_xval']
                        self.slit_info[name]['Gslit'] = coadd_dict[key]['Gemini_slit']
        else:
            self.slit_info = None

        # names, spectra, zs = [], [], []
        names, spectra = [], []
        if zdict is None:
            self.zdict = OrderedDict()
            load_z = True
        else:
            self.zdict = OrderedDict()
            load_z = False
        for hdu in self.rr_hdul[1:]:
            # Grab the spectrum
            spec_file = hdu.name
            # tmp = XSpectrum1D.from_file(spec_file.replace('FITS','fits'))
            spectra.append(XSpectrum1D.from_file(spec_file.replace('FITS','fits'), masking='edges'))
            names.append(spec_file.replace('.FITS', ''))
            # RedRock
            data = hdu.data
            # Init the dict
            if load_z:
                self.zdict[names[-1]] = {}
                self.zdict[names[-1]]['zRR'] = data['z']
                self.zdict[names[-1]]['ZQ'] = -99
                self.zdict[names[-1]]['Comment'] = ''
                self.zdict[names[-1]]['z'] = data['z'][0]
            else:
                self.zdict[names[-1]] = zdict[names[-1]]
        # Collate
        ispec = lspu.collate(spectra, masking='edges')
        # Fill
        ispec.labels = names
        ispec.stypes = ['galaxy']*ispec.nspec
        # ispec.z = zs  # DO NOT SET THE REDSHIFT HERE

        self.RRi = 0

        self.scale = screen_scale

        # Needed to avoid crash in large spectral files
        rcParams['agg.path.chunksize'] = 20000
        rcParams['axes.formatter.useoffset'] = False  # avoid scientific notation in axes tick labels

        # Build a widget combining several others
        self.main_widget = QWidget()

        # Status bar
        self.create_status_bar()

        # ZQ window
        self.ZQ_widg = ltgsm.EditBox(-99, 'ZQ', '{:d}')
        self.ZQ_values = [-99, -1, 0, 1, 3, 4]
        # Comment window
        self.comment_widg = ltgsm.EditBox('', 'Comment', '{:s}')

        # Grab the pieces and tie together
        self.pltline_widg = ltgl.PlotLinesWidget(status=self.statusBar,
            screen_scale=self.scale)
        self.pltline_widg.setMaximumWidth(300*self.scale)

        # Hook the spec widget to Plot Line
        self.spec_widg = ltgsp.ExamineSpecWidget(ispec,status=self.statusBar,
                                                 parent=self, llist=self.pltline_widg.llist,
                                                screen_scale=self.scale,
                                                 **kwargs)
        # Reset redshift from spec
        # Auto set line list if spec has proper object type
        if hasattr(self.spec_widg.spec, 'stypes'):
            if self.spec_widg.spec.stypes[self.spec_widg.select].lower() == 'galaxy':
                self.pltline_widg.llist = ltgu.set_llist('Galaxy',in_dict=self.pltline_widg.llist)
            elif self.spec_widg.spec.stypes[self.spec_widg.select].lower() == 'absorber':
                self.pltline_widg.llist = ltgu.set_llist('Strong',in_dict=self.pltline_widg.llist)
            self.pltline_widg.llist['Plot'] = True
            idx = self.pltline_widg.lists.index(self.pltline_widg.llist['List'])
            self.pltline_widg.llist_widget.setCurrentRow(idx)
        #
        self.pltline_widg.spec_widg = self.spec_widg
        # Multi spec
        self.mspec_widg = ltgsp.MultiSpecWidget(self.spec_widg, extra_method=self)

        self.spec_widg.canvas.mpl_connect('key_press_event', self.on_key)
        self.spec_widg.canvas.mpl_connect('button_press_event', self.on_click)

        self.prev_select = 0  # Index of previous spectrum;  starts at 0

        # Legend -- specific to this GUI
        self.legend = {}
        self.wv_dict = {'*': 3727., '(': 3950., ')': 4940., '_': 6564.}
        self.legend['zoom'] = self.wv_dict
        self.legend['&'] = 'Toggle through ZQ'
        self.legend['#'] = 'Toggle through zRR (WARNING: will not necessary start at the first one)'
        self.legend['%'] = 'Set z=0 (for stars)'
        self.legend['9'] = 'Skip to next spectrum with ZQ=-99'
        self.legend['x'] = 'Next spectrum'
        for key, value in self.legend.items():
            print(key, value)

        # Extras
        extras = QWidget()
        extras.setMinimumWidth(180*self.scale)
        extras.setMaximumWidth(280*self.scale)
        vbox = QVBoxLayout()
        qbtn = QPushButton(self)
        qbtn.setText('Quit')
        qbtn.clicked.connect(self.quit)
        vbox.addWidget(self.pltline_widg)
        vbox.addWidget(self.ZQ_widg)
        vbox.addWidget(self.comment_widg)
        vbox.addWidget(self.mspec_widg)
        vbox.addWidget(qbtn)
        extras.setLayout(vbox)

        # Main window
        hbox = QHBoxLayout()
        hbox.addWidget(self.spec_widg)
        hbox.addWidget(extras)

        self.main_widget.setLayout(hbox)

        # Point MainWindow
        self.setCentralWidget(self.main_widget)
        if unit_test:
            self.quit()

        # Giddy up
        self.run_with_select(save=False)

    def create_status_bar(self):
        """ Status bar for the GUI
        """
        self.status_text = QLabel("XSpec")
        self.statusBar().addWidget(self.status_text, 1)

    def on_key(self, event):
        """ Over-loads keys
        """
        z = self.pltline_widg.llist['z']
        # Change ZQ
        if event.key in ['&']:
            # ZQ
            ZQ = int(self.ZQ_widg.value)
            idx = self.ZQ_values.index(ZQ)
            if self.ZQ_values[idx] == self.ZQ_values[0]:
                new_idx = len(self.ZQ_values)-1
            else:
                new_idx = idx-1
            # Set
            self.ZQ_widg.setv(str(self.ZQ_values[new_idx]))
        if event.key in self.wv_dict.keys():
            # Zoom in on a feature
            z_wv = (1+z)*self.wv_dict[event.key]
            self.spec_widg.psdict['x_minmax'] = [z_wv-110., z_wv+110.]
            self.spec_widg.on_draw()

        if event.key == '%': # Next one
            self.pltline_widg.setz(str(0.))

        if event.key == '#': # Toggle through zRR
            if self.RRi < 2:
                self.RRi += 1
            else:
                self.RRi = 0
            name = self.spec_widg.spec.labels[self.spec_widg.select]
            self.pltline_widg.setz(str(self.zdict[name]['zRR'][self.RRi]))

        # Jumping around
        if event.key == 'x': # Next one
            idx = min(self.spec_widg.select + 1, len(self.zdict)-1)
            self.mspec_widg.mspec_widget.setCurrentRow(idx)
        if event.key == '9': # Next -99 case
            #QtCore.pyqtRemoveInputHook()
            #pdb.set_trace()
            #QtCore.pyqtRestoreInputHook()
            ZQs = [self.zdict[key]['ZQ'] for key in self.zdict.keys()]
            idx = ZQs.index(-99)
            if idx >= 0:
                self.mspec_widg.mspec_widget.setCurrentRow(idx)
            else:
                print("You have done them all!!")

    def on_click(self, event):
        """ Over-loads click events
        """
        if event.button == 3: # Set redshift
            if event.xdata is None:  # Mac bug [I think]
                return
            if self.pltline_widg.llist['List'] is None:
                return
            self.select_line_widg = ltgl.SelectLineWidget(
                self.pltline_widg.llist[self.pltline_widg.llist['List']]._data,
                scale=self.scale)
            self.select_line_widg.exec_()
            line = self.select_line_widg.line
            if line.strip() == 'None':
                return
            #
            quant = line.split('::')[1].lstrip()
            spltw = quant.split(' ')
            #QtCore.pyqtRemoveInputHook()
            #pdb.set_trace()
            #QtCore.pyqtRestoreInputHook()
            wrest = Quantity(float(spltw[0]), unit=self.pltline_widg.llist[
                self.pltline_widg.llist['List']]._data['wrest'].unit) # spltw[1])  [A bit risky!]
            z = event.xdata/wrest.value - 1.
            self.pltline_widg.llist['z'] = z
            print("z={:.5f}".format(z))
            self.statusBar().showMessage('z = {:f}'.format(z))

            self.pltline_widg.zbox.setText('{:.5f}'.format(self.pltline_widg.llist['z']))

            # Draw
            self.spec_widg.on_draw()

    def run_with_select(self, save=True):
        # Save previous
        if save:
            self.save(self.prev_select)
        # Grab name
        name = self.spec_widg.spec.labels[self.spec_widg.select]
        # Print zRR
        print("zRR for {} = {}".format(name, self.zdict[name]['zRR']))
        # Print slit info
        if self.slit_info is not None:
            print(self.slit_info[name])
        # Set redshift from dict
        self.pltline_widg.setz(str(self.zdict[name]['z']))
        # Set ZQ
        self.ZQ_widg.set_text(self.zdict[name]['ZQ'])
        # Set Comment
        self.comment_widg.set_text(self.zdict[name]['Comment'])
        # Set previous
        self.prev_select = self.spec_widg.select
        # Legend
        for key,value in self.legend.items():
            print(key,value)
        self.RRi = 99

    def save(self, idx):
        # Update dict
        self.update_dict(idx)
        # Save
        cjson = ltu.jsonify(self.zdict)
        ltu.savejson(self.outfile, cjson, overwrite=True, easy_to_read=True)
        print("Wrote: {:s}".format(self.outfile))

    def update_dict(self, idx=None):
        # Set idx
        if idx is None:
            idx = self.spec_widg.select
        # Grab name
        name = self.spec_widg.spec.labels[idx]
        # Set z
        self.zdict[name]['z'] = self.pltline_widg.llist['z']
        # Set ZQ
        self.zdict[name]['ZQ'] = int(self.ZQ_widg.value)
        # Comment
        self.zdict[name]['Comment'] = self.comment_widg.value

    # Quit
    def quit(self):
        self.save(self.spec_widg.select)
        self.close()

        
