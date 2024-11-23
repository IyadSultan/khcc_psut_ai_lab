# Contents from: .\combine.py
import os

def get_html_files_recursively(directory):
    """
    Recursively get all HTML files from directory and subdirectories.
    Uses os.walk() to traverse through all subdirectories at any depth.
    Excludes any directories named '.venv'.
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        # Exclude '.venv' folders from the search
        dirs[:] = [d for d in dirs if d != '.venv']
        for file in files:
            if file.endswith('.html'):
                file_list.append(os.path.join(root, file))
    return file_list

def get_html_summary(html_file):
    """
    Extract title and first comment from HTML file as summary
    """
    summary = ""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for title tag content
            title_start = content.find('<title>')
            title_end = content.find('</title>')
            if title_start > -1 and title_end > -1:
                title = content[title_start+7:title_end].strip()
                summary += f"Title: {title}\n"
            
            # Look for first HTML comment
            comment_start = content.find('<!--')
            comment_end = content.find('-->')
            if comment_start > -1 and comment_end > -1:
                comment = content[comment_start+4:comment_end].strip()
                summary += f"Description: {comment}\n"
                
    except Exception as e:
        summary = f"Error reading file: {str(e)}\n"
        
    return summary

def main():
    # Define the base directory (current directory in this case)
    base_directory = "."
    output_file = 'html_summary.txt'

    # Remove output file if it exists
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except Exception as e:
            print(f"Error removing existing {output_file}: {str(e)}")
            return

    # Get all HTML files recursively
    html_files = get_html_files_recursively(base_directory)
    html_files.sort()

    # Write summaries to output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("# HTML Files Summary\n")
        outfile.write(f"# Generated from directory: {os.path.abspath(base_directory)}\n")
        outfile.write(f"# Total HTML files found: {len(html_files)}\n\n")
        
        for file in html_files:
            outfile.write(f"\n### {file} ###\n")
            outfile.write(get_html_summary(file))
            outfile.write("-" * 80 + "\n")
    
    print(f"Successfully generated summary of {len(html_files)} HTML files in {output_file}")
    print("Files processed:")
    for file in html_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()