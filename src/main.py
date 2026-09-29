import os
import shutil
import sys
from gencontent import generate_pages_recursive

def create_clean_dest(dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

def copy_files_recursive(source_dir, dest_dir): 
    main_dir = os.listdir(source_dir)
    for item in main_dir:
        src_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_files_recursive(src_path, dest_path)

def main():    
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"     
    create_clean_dest("docs")
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
main()