from dumbrain.lib.download import downloadAndUnzip
import retro.data
import os
from tqdm import tqdm

def main():
    romdir = 'data/roms/'
    downloadAndUnzip( 'http://aiml.mikelyons.org/datasets/sonic/Sonic%20Roms.zip', romdir, loading_bar=tqdm )
    roms = [ os.path.join( romdir, rom ) for rom in os.listdir( romdir ) ]
    retro.data.merge( *roms, quiet=False )

if __name__ == '__main__':
    main()
