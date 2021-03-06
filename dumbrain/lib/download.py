import sys
import os
from os import path
import time

import tempfile
from zipfile import ZipFile

from tqdm import tqdm
import requests
import urllib

# Global
_download_pbar = None

def mkdirp( folder ):
    if not path.exists( folder ):
        print( 'Directory', folder, 'didn\'t exist, making' )
        os.makedirs( folder )

def download( url, dest_file, show_progress=True, loading_bar=tqdm ):
    """
    Downloads file to given file. Path to file should exist. Uses _download_pbar
    global
    """

    def reporthook( count, part_size, total_size ):
        global _download_pbar
        if _download_pbar is None:
            _download_pbar = loading_bar( total = total_size )
        _download_pbar.update( part_size )

    urllib.request.urlretrieve( url, dest_file, reporthook=reporthook )
    global _download_pbar
    _download_pbar.close()
    _download_pbar = None

def unzip( zip_filename, dest_folder, loading_bar=tqdm ):
    zip_file = ZipFile( zip_filename )

    all_files = zip_file.infolist()
    uncompressed_size = sum( ( file.file_size for file in zip_file.infolist() ) )

    files = zip_file
    with loading_bar( total=uncompressed_size ) as pbar:
        for file in all_files:
            zip_file.extract( file, dest_folder )
            pbar.update( file.file_size )

def downloadAndUnzip( download_url, save_folder, loading_bar=tqdm ):
    mkdirp( save_folder )

    temp_zip_filename = 'temp.zip'

    with tempfile.TemporaryDirectory() as temp_dir:
        full_temp_zip_filename = path.join( temp_dir, temp_zip_filename )
        download( download_url, full_temp_zip_filename, loading_bar=loading_bar )
        unzip( full_temp_zip_filename, save_folder, loading_bar=loading_bar )

def uploadColabAndUnzip( save_folder, loading_bar=tqdm ):
    from google.colab import files
    mkdirp( save_folder )

    temp_zip_filename = 'temp.zip'

    with tempfile.TemporaryDirectory() as temp_dir:
        full_temp_zip_filename = path.join( temp_dir, temp_zip_filename )
        uploaded_files = files.upload()

        if( len( uploaded_files.keys() ) > 1 ):
            raise RuntimeError( 'More than one file upload' )

        uploaded_file = list( uploaded_files.values() )[ 0 ]            
        with open( full_temp_zip_filename, 'wb' ) as f:
            f.write( uploaded_file )

        unzip( full_temp_zip_filename, save_folder, loading_bar=loading_bar )

def validateArgs( argv ):
    if not len( argv ) == 3:
        print( 'Usage: download.py <url> <save folder>' )
        sys.exit( 1 )
    return argv[ 1 ], argv[ 2 ]

if __name__ == '__main__':
    download_url, save_folder = validateArgs( sys.argv )
    print( 'Downloading and unzipping', download_url, 'to', save_folder )
    downloadAndUnzip( download_url, save_folder )