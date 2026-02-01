import struct
import os

class VC:    
    def hasTables(self):
        return True

    def parseTables(self, stream):
        return _parseTables(stream)

    def parseTKeyTDat(self, stream):
        size = findBlock(stream, 'TKEY')
        
        TKey = []
        for i in range(int(size / 12)): # TKEY entry size - 12
            TKey.append( struct.unpack('I8s', stream.read(12)) )
        
        datSize = findBlock(stream, 'TDAT')
        TDat = stream.read(datSize)

        Entries = []

        for entry in TKey:
            key = entry[1]
            value = TDat[entry[0]:].decode('utf-16').split('\x00', 1) [0]
            Entries.append( (key.split(b'\x00')[0].decode(), value) ) # TODO: charmap
        
        return Entries

class SA:
    def __init__(self, encoding):
        self.encoding = encoding

    def hasTables(self):
        return True

    def parseTables(self, stream):
        return _parseTables(stream)

    def parseTKeyTDat(self, stream):
        size = findBlock(stream, 'TKEY')
        
        TKey = []
        for i in range(int(size / 8)): # TKEY entry size - 8
            TKey.append( struct.unpack('II', stream.read(8)) )
        
        datSize = findBlock(stream, 'TDAT')
        TDat = stream.read(datSize)

        Entries = []

        for entry in TKey:
            key = f'0x{entry[1]:08X}'
            value = TDat[entry[0]:].decode(self.encoding).split('\x00', 1) [0]

            Entries.append( (key, value) ) # TODO: charmap
        
        return Entries


def findBlock(stream, block):
    while stream.peek(4) [:4] != block.encode():
        stream.seek(1, os.SEEK_CUR)

    _, size = struct.unpack('4sI', stream.read(8))

    return size

def getVersion(stream):
    bytes = stream.peek(8) [:8]

    # SA
    word1, word2 = struct.unpack('HH', bytes[:4])
    if word1 == 4 and bytes[4:] == 'TABL'.encode():
        if word2 == 8:
            return 'sa'
        if word2 == 16:
            return 'sa-mobile'
    
    if bytes[:4] == 'TABL'.encode():
        return 'vc'
    
    return None

def getReader(version):
    if version == 'vc':
        return VC()
    if version == 'sa':
        return SA('cp1252')
    if version == 'sa-mobile':
        return SA('utf-16')
    return None

# Internal functions
def _parseTables(stream):
    size = findBlock(stream, 'TABL')
    Tables = []
        
    for i in range(int(size / 12)): # TABL entry size - 12
        rawName, offset = struct.unpack('8sI', stream.read(12))
        Tables.append( (rawName.split(b'\x00')[0].decode(), offset) )
    
    return Tables

import sys
import os
import errno

args = sys.argv[1:]
outDirName = os.path.splitext(args[0])[0]

def createOutputDir(path):
    try:
        os.makedirs( path )
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def readOutTable(gxt, reader, name):
    createOutputDir(os.path.join(outDirName, name))

    with open(os.path.join(outDirName, name, name + '.txt'), 'w', encoding='utf-8') as f:
        for text in reader.parseTKeyTDat(gxt):
            f.write( text[0] + '\t' + text[1] + '\n' )


# TODO: Parse arguments
with open(args[0], 'rb') as gxt:
    gxtversion = getVersion(gxt)

    if not gxtversion:
        print('Unknown GXT version!', file=sys.stderr)
        exit(1)

    print("Detected GXT version: {}".format(gxtversion))

    gxtReader = getReader(gxtversion)
    
    Tables = []
    if gxtReader.hasTables(): # type: ignore
        Tables = gxtReader.parseTables(gxt) # type: ignore

    readOutTable(gxt, gxtReader, 'MAIN')

    if Tables:
        for t in Tables[1:]:
            gxt.seek(t[1])
            readOutTable(gxt, gxtReader, t[0])