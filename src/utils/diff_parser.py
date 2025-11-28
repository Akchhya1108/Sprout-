"""
Diff Parser Module
Parses git diff output into structured, readable format
"""

from typing import List, Dict
import re


class DiffParser:
    """
    Parses git diff output into structured data
    
    A git diff looks like:
    diff --git a/file.py b/file.py
    @@ -1,3 +1,4 @@
    -old line
    +new line
    
    We need to extract: which files changed, what was added/removed
    """
    
    @staticmethod
    def parse_diff(diff_text: str) -> List[Dict[str, any]]:
        """
        Parse diff text into list of file changes
        
        Args:
            diff_text: Raw git diff output
        
        Returns:
            List of dictionaries, each representing a changed file
        
        Example return:
        [
            {
                'file_path': 'src/main.py',
                'additions': ['print("hello")', 'x = 5'],
                'deletions': ['print("goodbye")'],
                'change_summary': '+2, -1'
            }
        ]
        """
        if not diff_text or not diff_text.strip():
            return []
        
        # Split diff into chunks (one per file)
        file_diffs = re.split(r'\ndiff --git', diff_text)
        
        parsed_files = []
        
        for file_diff in file_diffs:
            if not file_diff.strip():
                continue
            
            # Extract file path
            file_path = DiffParser._extract_file_path(file_diff)
            if not file_path:
                continue
            
            # Extract additions and deletions
            additions, deletions = DiffParser._extract_changes(file_diff)
            
            # Create summary
            parsed_files.append({
                'file_path': file_path,
                'additions': additions,
                'deletions': deletions,
                'addition_count': len(additions),
                'deletion_count': len(deletions),
                'change_summary': f"+{len(additions)}, -{len(deletions)}"
            })
        
        return parsed_files
    
    @staticmethod
    def _extract_file_path(file_diff: str) -> str:
        """
        Extract file path from diff chunk
        
        Looks for patterns like:
        a/src/main.py b/src/main.py
        or
        --- a/src/main.py
        +++ b/src/main.py
        """
        # Try to find "a/filepath b/filepath" pattern
        match = re.search(r'a/(.*?)\s+b/', file_diff)
        if match:
            return match.group(1)
        
        # Try to find "+++ b/filepath" pattern
        match = re.search(r'\+\+\+ b/(.*)', file_diff)
        if match:
            return match.group(1).strip()
        
        return ""
    
    @staticmethod
    def _extract_changes(file_diff: str) -> tuple:
        """
        Extract added and deleted lines from diff
        
        Lines starting with + are additions
        Lines starting with - are deletions
        (But ignore +++ and --- which are file markers)
        
        Returns:
            (additions, deletions) tuple of lists
        """
        additions = []
        deletions = []
        
        lines = file_diff.split('\n')
        
        for line in lines:
            # Skip file markers and chunk headers
            if line.startswith('+++') or line.startswith('---'):
                continue
            if line.startswith('@@'):
                continue
            
            # Addition
            if line.startswith('+'):
                additions.append(line[1:].strip())  # Remove the +
            
            # Deletion
            elif line.startswith('-'):
                deletions.append(line[1:].strip())  # Remove the -
        
        return additions, deletions
    
    @staticmethod
    def get_summary(diff_text: str) -> str:
        """
        Get a human-readable summary of changes
        
        Args:
            diff_text: Raw git diff
        
        Returns:
            Summary string like "3 files changed: 12 additions, 5 deletions"
        """
        parsed = DiffParser.parse_diff(diff_text)
        
        if not parsed:
            return "No changes detected"
        
        total_additions = sum(f['addition_count'] for f in parsed)
        total_deletions = sum(f['deletion_count'] for f in parsed)
        file_count = len(parsed)
        
        return (
            f"{file_count} file(s) changed: "
            f"{total_additions} addition(s), {total_deletions} deletion(s)"
        )


# Test the parser
if __name__ == "__main__":
    # Sample diff for testing
    sample_diff = """diff --git a/src/main.py b/src/main.py
index 1234567..abcdefg 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,4 @@
 def hello():
-    print("old")
+    print("new")
+    return True
"""
    
    print("🧪 Testing DiffParser\n")
    
    parser = DiffParser()
    parsed = parser.parse_diff(sample_diff)
    
    print("Parsed result:")
    for file_data in parsed:
        print(f"\n📄 File: {file_data['file_path']}")
        print(f"   Changes: {file_data['change_summary']}")
        print(f"   Additions: {file_data['additions']}")
        print(f"   Deletions: {file_data['deletions']}")
    
    print(f"\n📊 Summary: {parser.get_summary(sample_diff)}")