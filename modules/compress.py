import os
import sys
import re
import subprocess

file_pattern = re.compile(r'^(.*?)(-\d{5}|-meta)?\.(cdx|warc|warc\.gz)$')

def compress_similar_files(directory, output_dir):
    file_groups = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            match = file_pattern.match(file)
            if match:
                base_name = match.group(1)
                if base_name not in file_groups:
                    file_groups[base_name] = []
                file_groups[base_name].append(os.path.join(root, file))
    
    for base_name, file_list in file_groups.items():
        archive_name = os.path.join(output_dir, f'{base_name}.7z')
        print(f'Compressing files for {base_name} into {archive_name}')
        
        compression_command = [
            '7z', 'a', '-t7z', '-m0=LZMA2', '-mmt=on', '-mx9', '-md=64m', 
            '-mfb=64', '-ms=16g', '-mqs=on', '-sccUTF-8', '-bb0', '-bse0', 
            '-bsp2', f'-w{output_dir}', archive_name
        ] + file_list
        
        result = subprocess.run(compression_command)
        
        if result.returncode == 0:
            print(f'Successfully compressed {base_name}. Deleting original files...')
            for file_path in file_list:
                try:
                    os.remove(file_path)
                    print(f'Deleted {file_path}')
                except OSError as e:
                    print(f'Error deleting {file_path}: {e}')
        else:
            print(f'Failed to compress {base_name}. Skipping file deletion.')

def compress(data_folder):
    directory = f'{data_folder}/__finishedWarcs/'
    output_dir = f'{data_folder}/__compressedWarcs/'
    compress_similar_files(directory, output_dir)

if __name__ == '__main__':
    try:
        data_folder = sys.argv[1]
        if not os.path.isdir(data_folder):
            raise ValueError("data_folder is not a path")
    except:
        print("Folder was not specified. Exiting.")
        sys.exit(1)
    
    compress(data_folder)
