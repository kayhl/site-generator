from textnode import TextNode, TextType
import os
import shutil

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")

main()








# copy from source to destination (static to public for us)
# delete all of destination/public
# copy all files/subdirectories/nestings
# try logging to see what happens when it runs