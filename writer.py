"""Something smart here

By Thomas Memelink, 2021
"""

import argparse
from typing import Any, Dict, List, Optional
from pathlib import Path
import glob

from mutagen.flac import FLAC 


FILE_TYPE_WHITELIST = ['flac']


def set_save_metadata(files: List[Path], metadata: Optional[Dict[str,Any]]) -> None:
    if not metadata:
        raise ValueError('No metadata to write')
    for file in files:
        audio = FLAC(file)
        for key, value in metadata.items():
            audio[key] = value
            audio.save()

def get_dir_files(input_dir: Path, file_type: str) -> List[Path]:
    pattern = f'*.{file_type}'
    files_in_dir = input_dir.glob(pattern=pattern)
    return [Path(file_path).absolute() for file_path in files_in_dir] 


def parse_args() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_folder',
                        help='Absolute path to the root folder', type=str)
    parser.add_argument('-f', '--file_type',
                        help='Filetype, current options: [\'flac\']', type=str)
    parser.add_argument('-a', '--album',
                        help='Album name to change metadata into', type=str)
    return parser.parse_args()


def check_input(input_dir: str, file_type: str, metadata: Optional[Dict[str,Any]]) -> None:
    
    def str_check(check_string: str, value_name: str):
        if not check_string:
            raise ValueError(f'No value set for {value_name}')
        if not type(check_string) is str:
            raise TypeError(f'{value_name} is not a string')
        
    
    str_check(input_dir, 'input_dir')
    str_check(file_type, 'file_type')
    
    if metadata:
        for key, value in metadata.items():
            str_check(value, key)
    
    if not file_type in FILE_TYPE_WHITELIST:
        raise ValueError(f'File_type not in whitelist, currently allowed: {FILE_TYPE_WHITELIST}')
    path = Path(input_dir)
    if not path.exists():          
        raise NotADirectoryError('File path does not exits')


def main(input_dir: str, file_type: str, al) -> None:
    check_input(input_dir, file_type, metadata)
    input_dir = Path(input_dir)

    
    files_in_dir = get_dir_files(input_dir, file_type)

    set_save_metadata(files_in_dir, metadata)
    
if __name__ == '__main__':

    args = parse_args()
    input_dir = args.input_folder 
    file_type = args.file_type
    album = args.album

    metadata = {
        'album':  album
    }
    
    main(input_dir, file_type, metadata)
    
    
     
    
    