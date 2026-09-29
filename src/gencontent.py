from block_markdown import markdown_to_html_node
from inline_markdown import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        md_contents = file.read()
    with open(template_path) as file:
        template = file.read()
    node = markdown_to_html_node(md_contents)
    html = node.to_html()
    title = extract_title(md_contents)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    with open(dest_path, "w") as file:
        file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    main_dir = os.listdir(dir_path_content)
    for item in main_dir:
        src_path = os.path.join(dir_path_content, item)
        if os.path.isfile(src_path):
            html_item = item.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, html_item)
            generate_page(src_path, template_path, dest_path)
        else:
            dest_path = os.path.join(dest_dir_path, item)
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dest_path)