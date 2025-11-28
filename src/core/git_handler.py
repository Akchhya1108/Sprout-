"""
Git Handler Module
Handles all Git operations: reading repos, getting diffs, analyzing changes
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from git import Repo, InvalidGitRepositoryError, GitCommandError


class GitHandler:
    """
    Manages Git repository operations
    
    This class is like a translator between our Python code and Git.
    It can read repositories, get changes, and understand what's been modified.
    """
    
    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize the Git handler
        
        Args:
            repo_path: Path to git repository. If None, uses current directory.
        
        Why Optional[str]? It means repo_path can be a string OR None.
        """
        # If no path provided, use current directory
        self.repo_path = repo_path or os.getcwd()
        self.repo = None
        self._load_repository()
    
    def _load_repository(self) -> None:
        """
        Load the Git repository
        
        The underscore _ before the name means this is a "private" method -
        only used inside this class, not called from outside.
        
        Raises:
            InvalidGitRepositoryError: If the path is not a git repo
        """
        try:
            # Repo() is from GitPython - it connects to a git repository
            self.repo = Repo(self.repo_path, search_parent_directories=True)
            print(f"✅ Loaded repository: {self.repo.working_dir}")
        except InvalidGitRepositoryError:
            raise InvalidGitRepositoryError(
                f"❌ Not a git repository: {self.repo_path}\n"
                f"Run 'git init' to create one, or navigate to an existing repo."
            )
    
    def is_repo_dirty(self) -> bool:
        """
        Check if repository has uncommitted changes
        
        Returns:
            True if there are changes, False if everything is committed
        
        "Dirty" in Git terms = has changes that aren't committed yet
        """
        return self.repo.is_dirty(untracked_files=True)
    
    def get_staged_changes(self) -> str:
        """
        Get the diff of staged changes (what you've done 'git add' on)
        
        Returns:
            String containing the diff output
        
        This is like running 'git diff --cached' in the terminal
        """
        try:
            # Get diff between HEAD (last commit) and staging area
            diff = self.repo.git.diff('--cached', '--unified=3')
            
            if not diff:
                return ""
            
            return diff
        except GitCommandError as e:
            print(f"❌ Error getting staged changes: {e}")
            return ""
    
    def get_unstaged_changes(self) -> str:
        """
        Get the diff of unstaged changes (modified but not 'git add'ed)
        
        Returns:
            String containing the diff output
        
        This is like running 'git diff' in the terminal
        """
        try:
            # Get diff of working directory vs staging area
            diff = self.repo.git.diff('--unified=3')
            
            if not diff:
                return ""
            
            return diff
        except GitCommandError as e:
            print(f"❌ Error getting unstaged changes: {e}")
            return ""
    
    def get_all_changes(self) -> str:
        """
        Get both staged AND unstaged changes
        
        Returns:
            Combined diff of all changes
        
        Useful when user hasn't staged anything yet
        """
        staged = self.get_staged_changes()
        unstaged = self.get_unstaged_changes()
        
        # Combine both diffs
        if staged and unstaged:
            return f"{staged}\n\n{unstaged}"
        return staged or unstaged
    
    def get_changed_files(self) -> List[str]:
        """
        Get list of files that have been modified
        
        Returns:
            List of file paths
        
        Example: ['src/main.py', 'README.md', 'tests/test_git.py']
        """
        changed_files = []
        
        # Get staged files
        staged = self.repo.index.diff("HEAD")
        for item in staged:
            changed_files.append(item.a_path)
        
        # Get unstaged files
        unstaged = self.repo.index.diff(None)
        for item in unstaged:
            changed_files.append(item.a_path)
        
        # Get untracked files (new files not added to git yet)
        untracked = self.repo.untracked_files
        changed_files.extend(untracked)
        
        # Remove duplicates and return
        return list(set(changed_files))
    
    def get_file_content(self, file_path: str) -> Optional[str]:
        """
        Get the content of a specific file
        
        Args:
            file_path: Path to the file
        
        Returns:
            File content as string, or None if file doesn't exist
        """
        full_path = Path(self.repo.working_dir) / file_path
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"⚠️  File not found: {file_path}")
            return None
        except UnicodeDecodeError:
            # Binary file - can't read as text
            print(f"⚠️  Cannot read binary file: {file_path}")
            return None
    
    def stage_all_changes(self) -> None:
        """
        Stage all changes (like 'git add .')
        
        Useful for testing - adds all modified files to staging area
        """
        try:
            self.repo.git.add(A=True)  # A=True means 'git add --all'
            print("✅ All changes staged")
        except GitCommandError as e:
            print(f"❌ Error staging changes: {e}")
    
    def get_repository_info(self) -> Dict[str, str]:
        """
        Get basic information about the repository
        
        Returns:
            Dictionary with repo info
        """
        return {
            "path": self.repo.working_dir,
            "branch": self.repo.active_branch.name,
            "has_changes": str(self.is_repo_dirty()),
            "total_commits": str(len(list(self.repo.iter_commits()))),
        }


# Example usage (will remove this later, just for testing)
if __name__ == "__main__":
    """
    This code only runs when you execute this file directly.
    It won't run when you import GitHandler into other files.
    """
    try:
        # Create a handler for the current directory
        handler = GitHandler()
        
        # Print repository info
        print("\n📊 Repository Info:")
        info = handler.get_repository_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Check for changes
        print(f"\n🔍 Has changes: {handler.is_repo_dirty()}")
        
        # Get changed files
        changed_files = handler.get_changed_files()
        if changed_files:
            print(f"\n📝 Changed files ({len(changed_files)}):")
            for file in changed_files:
                print(f"  - {file}")
        else:
            print("\n✨ No changes detected")
        
        # Get diff
        diff = handler.get_all_changes()
        if diff:
            print(f"\n📄 Diff preview (first 500 chars):")
            print(diff[:500])
            print("..." if len(diff) > 500 else "")
        
    except InvalidGitRepositoryError as e:
        print(e)