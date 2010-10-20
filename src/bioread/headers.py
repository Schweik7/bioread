# coding: utf8
# Part of the bioread package for reading BIOPAC data.
#
# Copyright (c) 2010 Board of Regents of the University of Wisconsin System
#
# Written by John Ollinger <ollinger@wisc.edu> and Nate Vack <njvack@wisc.edu>
# at the Waisman Laboratory for Brain Imaging and Behavior, University of
# Wisconsin-Madison

from struct_dict import StructDict
from file_versions import *

class Header(object):
    """
    Represents a binary header and its unpacking
    """
    
    def __init__(self, struct_dict):
        self.struct_dict = struct_dict
        self.offset = None
        self.unpacked = {}
    
    def unpack_from_str(self, str_data):
        self.raw_data = str_data
        self.__unpack_data()
        
    def unpack_from_file(self, data_file, offset):
        self.offset = offset
        data_file.seek(offset)
        self.raw_data = data_file.read(self.struct_dict.len_bytes)
        self.__unpack_data()
    
    @property
    def effective_len_bytes(self):
        """ 
        This will be overridden frequently -- it's used in navigating files.
        """
        return self.struct_dict.len_bytes

    @property
    def format_string(self):
        return self.struct_dict.format_string
    
    def __unpack_data(self):
        self.data = self.struct_dict.unpack(self.raw_data)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __str__(self):
        return str(self.data)


class VersionedHeaderStructure(object):
    def __init__(self, *structure_elements):
        self.structure_elements = structure_elements
    
    def elements_for(self, version):
        return [se for se in self.structure_elements if se[2] <= version]
    

class BiopacHeader(Header):
    """
    A simple superclass for GraphHeader, ChannelHeader, and friends.
    """
    def __init__(self, header_structure, file_version, byte_order_flag):
        self.file_version = file_version
        self.byte_order_flag = byte_order_flag
        self.header_structure = header_structure
        sd = StructDict(
            byte_order_flag, header_structure.elements_for(file_version))
        super(BiopacHeader, self).__init__(sd)


class GraphHeader(BiopacHeader):
    """
    The main Graph Header for an AcqKnowledge file. Note that this is known
    to be wrong for more modern files -- but for the purposes of this
    reader, we don't care. Enough fields are right that we can still find
    our way around.
    """
    def __init__(self, file_version, byte_order_flag):
        super(GraphHeader, self).__init__(
            self.__h_elts, file_version, byte_order_flag)
    
    @property
    def effective_len_bytes(self):
        return self.data['lExtItemHeaderLen']
    
    @property
    def __h_elts(self):
        return VersionedHeaderStructure(
        ('nItemHeaderLen'           ,'h'    ,V_ALL ),
        ('lVersion'                 ,'l'    ,V_ALL ),
        ('lExtItemHeaderLen'        ,'l'    ,V_20a ),
        ('nChannels'                ,'h'    ,V_20a ),
        ('nHorizAxisType'           ,'h'    ,V_20a ),
        ('nCurChannel'              ,'h'    ,V_20a ),
        ('dSampleTime'              ,'d'    ,V_20a ),
        ('dTimeOffset'              ,'d'    ,V_20a ),
        ('dTimeScale'               ,'d'    ,V_20a ),
        ('dTimeCursor1'             ,'d'    ,V_20a ),
        ('dTimeCursor2'             ,'d'    ,V_20a ),
        ('rcWindow'                 ,'4h'   ,V_20a ),
        ('nMeasurement'             ,'6h'   ,V_20a ),
        ('fHilite'                  ,'h'    ,V_20a ),
        ('dFirstTimeOffset'         ,'d'    ,V_20a ),
        ('nRescale'                 ,'h'    ,V_20a ),
        ('szHorizUnits1'            ,'40s'  ,V_20a ),
        ('szHorizUnits2'            ,'10s'  ,V_20a ),
        ('nInMemory'                ,'h'    ,V_20a ),
        ('fGrid'                    ,'h'    ,V_20a ),
        ('fMarkers'                 ,'h'    ,V_20a ),
        ('nPlotDraft'               ,'h'    ,V_20a ),
        ('nDispMode'                ,'h'    ,V_20a ),
        ('rRReserved'               ,'h'    ,V_20a ),
        ('BShowToolBar'             ,'h'    ,V_30r ),
        ('BShowChannelButtons'      ,'h'    ,V_30r ),
        ('BShowMeasurements'        ,'h'    ,V_30r ),
        ('BShowMarkers'             ,'h'    ,V_30r ),
        ('BShowJournal'             ,'h'    ,V_30r ),
        ('CurXChannel'              ,'h'    ,V_30r ),
        ('MmtPrecision'             ,'h'    ,V_30r ),
        ('NMeasurementRows'         ,'h'    ,V_303 ),
        ('mmt40'                    ,'40h'  ,V_303 ),
        ('mmtChan40'                ,'40h'  ,V_303 ),
        ('MmtCalcOpnd1'             ,'40h'  ,V_35x ),
        ('MmtCalcOpnd2'             ,'40h'  ,V_35x ),
        ('MmtCalcOp'                ,'40h'  ,V_35x ),
        ('MmtCalcConstant'          ,'40d'  ,V_35x ),
        ('bNewGridWithMinor'        ,'l'    ,V_370 ),
        ('colorMajorGrid'           ,'4B'   ,V_370 ),
        ('colorMinorGrid'           ,'4B'   ,V_370 ),
        ('wMajorGridStyle'          ,'h'    ,V_370 ),
        ('wMinorGridStyle'          ,'h'    ,V_370 ),
        ('wMajorGridWidth'          ,'h'    ,V_370 ),
        ('wMinorGridWidth'          ,'h'    ,V_370 ),
        ('bFixedUnitsDiv'           ,'l'    ,V_370 ),
        ('bMid_Range_Show'          ,'l'    ,V_370 ),
        ('dStart_Middle_Point'      ,'d'    ,V_370 ),
        ('dOffset_Point'            ,'d'    ,V_370 ),
        ('hGrid'                    ,'d'    ,V_370 ),
        ('vGrid'                    ,'d'    ,V_370 ),
        ('bEnableWaveTools'         ,'l'    ,V_370 ),
        ('Reserved'                 ,'20b'  ,V_381 ),
        ('bOverlapMode'             ,'l'    ,V_381 ),
        ('bShowHardware'            ,'l'    ,V_381 ),
        ('bXAutoPlot'               ,'l'    ,V_381 ),
        ('bXAutoScroll'             ,'l'    ,V_381 ),
        ('bStartButtonVisible'      ,'l'    ,V_381 ),
        ('bCompressed'              ,'l'    ,V_381 ),
        ('bAlwaysStartButtonVisible','l'    ,V_381 ),
        ('pathVideo'                ,'260s' ,V_382 ),
        ('optSyncDelay'             ,'l'    ,V_382 ),
        ('syncDelay'                ,'d'    ,V_382 ),
        ('bHRP_PasteMeasurements'   ,'l'    ,V_382 ),
        ('graphType'                ,'l'    ,V_390 ),
        ('mmtCalcExpr'              ,'10240s',V_390 ),
        ('mmtMomentOrder'           ,'40l'  ,V_390 ),
        ('mmtTimeDelay'             ,'40l'  ,V_390 ),
        ('mmtEmbedDim'              ,'40l'  ,V_390 ),
        ('mmtMIDelay'               ,'40l'  ,V_390 ),
        )


class ChannelHeader(BiopacHeader):
    """
    The main Channel Header for an AcqKnowledge file. Note that this is known
    to be wrong for more modern files -- but for the purposes of this
    reader, we don't care. Enough fields are right that we can still find
    our way around.
    """
    def __init__(self, file_version, byte_order_flag):
        self.file_version = file_version
        super(ChannelHeader, self).__init__(
            self.__h_elts, file_version, byte_order_flag)
    
    @property
    def __version_bin(self):
        bin = 'Unknown'
        if self.file_version < V_400:
            bin = 'PRE_4'
        else:
            bin = 'POST_4'
        return bin
    
    @property
    def effective_len_bytes(self):
        return self.data['lChanHeaderLen']
    
    @property
    def __h_elts(self):
        return self.__h_elt_versions[self.__version_bin]
    
    @property
    def __h_elt_versions(self):
        return {
            'PRE_4' : VersionedHeaderStructure(
                ('lChanHeaderLen'           ,'l'    ,V_20a ),
                ('nNum'                     ,'h'    ,V_20a ),
                ('szCommentText'            ,'40s'  ,V_20a ),
                ('rgbColor'                 ,'4B'   ,V_20a ),
                ('nDispChan'                ,'h'    ,V_20a ),
                ('dVoltOffset'              ,'d'    ,V_20a ),
                ('dVoltScale'               ,'d'    ,V_20a ),
                ('szUnitsText'              ,'20s'  ,V_20a ),
                ('lBufLength'               ,'l'    ,V_20a ),
                ('dAmplScale'               ,'d'    ,V_20a ),
                ('dAmplOffset'              ,'d'    ,V_20a ),
                ('nChanOrder'               ,'h'    ,V_20a ),
                ('nDispSize'                ,'h'    ,V_20a ),
                ('plotMode'                 ,'h'    ,V_30r ),
                ('vMid'                     ,'d'    ,V_30r ),
                ('szDescription'            ,'128s' ,V_370 ),
                ('nVarSampleDivider'        ,'h'    ,V_370 ),
                ('vertPrecision'            ,'h'    ,V_373 ),
                ('activeSegmentColor'       ,'4b'   ,V_382 ),
                ('activeSegmentStyle'       ,'l'    ,V_382 ),
            ),
            'POST_4' : VersionedHeaderStructure(
                ('lChanHeaderLen'           ,'l'    ,V_20a ),
                ('nNum'                     ,'h'    ,V_20a ),
                ('szCommentText'            ,'40s'  ,V_20a ),
                ('notColor'                 ,'4B'   ,V_20a ),
                ('nDispChan'                ,'h'    ,V_20a ),
                ('dVoltOffset'              ,'d'    ,V_20a ),
                ('dVoltScale'               ,'d'    ,V_20a ),
                ('szUnitsText'              ,'20s'  ,V_20a ),
                ('lBufLength'               ,'l'    ,V_20a ),
                ('dAmplScale'               ,'d'    ,V_20a ),
                ('dAmplOffset'              ,'d'    ,V_20a ),
                ('nChanOrder'               ,'h'    ,V_20a ),
                ('nDispSize'                ,'h'    ,V_20a ),
                ('unknown'                  ,'40s'  ,V_400 ),
                ('nVarSampleDivider'        ,'h'    ,V_400 ),
            )
        }
    


class ForeignHeader(BiopacHeader):
    """
    The Foreign Data header for AcqKnowledge files. This does some tricky
    stuff based on file versions, ultimately to correctly determine
    the effective length.
    """
    def __init__(self, file_version, byte_order_flag):
        self.file_version = file_version
        super(ForeignHeader, self).__init__(
            self.__h_elts, file_version, byte_order_flag)

    @property
    def __version_bin(self):
        bin = 'Unknown'
        if self.file_version <= V_390:
            bin = "PRE_4"
        elif self.file_version < V_41a:
            bin = "EARLY_4"
        else:
            bin = "LATE_4"
        return bin
    
    @property
    def effective_len_bytes(self):
        return self.__effective_len_byte_versions[self.__version_bin]()
    
    @property
    def __h_elts(self):
        return self.__h_elt_versions[self.__version_bin]
    
    @property
    def __effective_len_byte_versions(self):
        # Make a hash of functions so we don't evaluate all code paths
        return {
            "PRE_4"     : lambda: self.data['nLength'],
            "EARLY_4"   : lambda: self.data['lLengthExtended'] + 8,
            "LATE_4"    : lambda: self.data['nLength'] + 8 # always correct?
        }
    
    @property
    def __h_elt_versions(self):
        return {
            "PRE_4" : VersionedHeaderStructure(
                ('nLength'                  ,'h'    ,V_20a ),
                ('nType'                    ,'h'    ,V_20a ),
            ),
            "EARLY_4" : VersionedHeaderStructure(
                ('nLength'                  ,'h'    ,V_400 ),
                ('nType'                    ,'h'    ,V_400 ),
                ('lReserved'                ,'l'    ,V_400 ),
                ('lLengthExtended'          ,'l'    ,V_400 ),
            ),
            "LATE_4" : VersionedHeaderStructure(
                ('nLength'                  ,'h'    ,V_400 ),
                ('nType'                    ,'h'    ,V_400 ),
                ('lReserved'                ,'l'    ,V_400 ),
            )
        }


class ChannelDTypeHeader(BiopacHeader):
    def __init__(self, file_version, byte_order_flag):
        super(ChannelDTypeHeader, self).__init__(
            self.__h_elts, file_version, byte_order_flag)
    
    @property
    def __h_elts(self):
        # This lets the standard effective_len_bytes work fine, I think.
        return VersionedHeaderStructure(
        ('nSize'                    ,'h'    ,V_20a ),
        ('nType'                    ,'h'    ,V_20a ),
        )