import os
import shutil
from pathlib import Path
from textnode import *
from inline_markdown import markdown_to_html_node, extract_title

def copy_static(src, dst):
    # clean destination
    if os.path.exists(dst):
        shutil.rmtree(dst)
    # ensure base and images dirs
    os.makedirs(dst)
    os.makedirs(os.path.join(dst, 'images'), exist_ok=True)
    # walk source
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        base_dest = dst if rel == '.' else os.path.join(dst, rel)
        # replicate subdirs
        for d in dirs:
            os.makedirs(os.path.join(base_dest, d), exist_ok=True)
        for f in files:
            src_file = os.path.join(root, f)
            # map style.css to index.css at root, and root pngs under images/
            if rel == '.' and f.lower() == 'style.css':
                dst_sub = dst
                dst_name = 'index.css'
            elif rel == '.' and f.lower().endswith('.png'):
                dst_sub = os.path.join(dst, 'images')
                dst_name = f
            else:
                dst_sub = base_dest
                dst_name = f
            os.makedirs(dst_sub, exist_ok=True)
            dst_file = os.path.join(dst_sub, dst_name)
            print(f"Copying {src_file} to {dst_file}")
            shutil.copy(src_file, dst_file)

# Generate HTML page from markdown using template
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # read markdown
    with open(from_path, 'r', encoding='utf-8') as f:
        md = f.read()
    # read template
    with open(template_path, 'r', encoding='utf-8') as f:
        tpl = f.read()
    # convert markdown to HTML
    node = markdown_to_html_node(md)
    content_html = node.to_html()
    # extract title
    title = extract_title(md)
    # replace placeholders
    html = tpl.replace('{{ Title }}', title).replace('{{ Content }}', content_html)
    # ensure dest directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    # write output
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages from markdown files in the content directory.
    
    Args:
        dir_path_content: Path to the content directory
        template_path: Path to the HTML template file
        dest_dir_path: Path to the public directory where HTML files will be written
    """
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Process all items in the content directory
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(src_path) and src_path.endswith('.md'):
            # For markdown files, generate corresponding HTML
            if item == 'index.md':
                # For index.md, generate index.html in the current directory
                dest_path = os.path.join(dest_dir_path, 'index.html')
            else:
                # For other markdown files, generate .html file in the same directory
                dest_path = os.path.join(dest_dir_path, os.path.splitext(item)[0] + '.html')
            
            generate_page(src_path, template_path, dest_path)
            
        elif os.path.isdir(src_path):
            # For directories, create corresponding directory in destination and recurse
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, new_dest_dir)

def main():
    # Set up paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    static_dir = os.path.join(project_root, 'static')
    public_dir = os.path.join(project_root, 'public')
    content_dir = os.path.join(project_root, 'content')
    template_path = os.path.join(project_root, 'template.html')
    
    # Clear and copy static files
    print("Copying static files...")
    copy_static(static_dir, public_dir)
    
    # Generate all pages recursively
    print("Generating HTML pages...")
    generate_pages_recursive(content_dir, template_path, public_dir)
    
    print("Site generation complete!")

main()