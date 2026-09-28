from block_markdown import markdown_to_html_node
from inline_markdown import extract_title

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