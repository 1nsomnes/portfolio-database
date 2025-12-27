# generated using gemini btw
import os
import yaml
import json

def generate_blog_index():
    blog_dir = 'blogs'
    output_file = 'blogs.json'
    blog_list = []

    # Check if the blogs directory exists
    if not os.path.exists(blog_dir):
        print(f"Error: The directory '{blog_dir}' was not found.")
        return

    # Loop through every file in the blogs folder
    for filename in os.listdir(blog_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(blog_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Split the content by the triple dashes
                # [0] is empty, [1] is the front matter, [2] is the body
                parts = content.split('---')
                
                if len(parts) >= 3:
                    front_matter_raw = parts[1]
                    try:
                        # Parse the YAML front matter into a dictionary
                        data = yaml.safe_load(front_matter_raw)
                        blog_list.append(data)
                    except yaml.YAMLError as exc:
                        print(f"Error parsing YAML in {filename}: {exc}")

    # Sort the blogs by date (newest first)
    blog_list.sort(key=lambda x: x.get('date', ''), reverse=True)

    # Write the list to blogs.json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(blog_list, f, indent=2)
    
    print(f"Success! {len(blog_list)} blogs indexed in {output_file}")

if __name__ == "__main__":
    generate_blog_index()
