"""
Test script for GitHandler
This lets us manually test our Git functionality
"""

import sys
from pathlib import Path

# Add src to Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.git_handler import GitHandler


def test_git_handler():
    """Test the GitHandler with our test repository"""
    
    # Point to our test repo (adjust path if needed)
    test_repo_path = Path(__file__).parent.parent.parent / "sprout-test-repo"
    
    print(f"🧪 Testing GitHandler with: {test_repo_path}\n")
    
    try:
        # Create handler
        handler = GitHandler(str(test_repo_path))
        
        # Test 1: Repository info
        print("=" * 50)
        print("TEST 1: Repository Info")
        print("=" * 50)
        info = handler.get_repository_info()
        for key, value in info.items():
            print(f"{key}: {value}")
        
        # Test 2: Changed files
        print("\n" + "=" * 50)
        print("TEST 2: Changed Files")
        print("=" * 50)
        changed = handler.get_changed_files()
        print(f"Found {len(changed)} changed file(s):")
        for file in changed:
            print(f"  📄 {file}")
        
        # Test 3: Staged changes
        print("\n" + "=" * 50)
        print("TEST 3: Staged Changes")
        print("=" * 50)
        staged = handler.get_staged_changes()
        if staged:
            print("Staged diff:")
            print(staged[:300])  # First 300 chars
            print("..." if len(staged) > 300 else "")
        else:
            print("No staged changes")
        
        # Test 4: Unstaged changes
        print("\n" + "=" * 50)
        print("TEST 4: Unstaged Changes")
        print("=" * 50)
        unstaged = handler.get_unstaged_changes()
        if unstaged:
            print("Unstaged diff:")
            print(unstaged[:300])
        else:
            print("No unstaged changes")
        
        # Test 5: All changes combined
        print("\n" + "=" * 50)
        print("TEST 5: All Changes")
        print("=" * 50)
        all_changes = handler.get_all_changes()
        if all_changes:
            print(f"Total diff length: {len(all_changes)} characters")
            print("Preview:")
            print(all_changes[:400])
            print("..." if len(all_changes) > 400 else "")
        else:
            print("No changes detected")
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_git_handler()