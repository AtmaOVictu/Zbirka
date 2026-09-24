#!/usr/bin/env python3
"""Test script to verify Qt alignment fix."""
import sys

try:
    from PyQt6.QtCore import Qt
    print(f"PyQt6.QtCore.Qt imported successfully")
    print(f"Has Qt.AlignmentFlag: {hasattr(Qt, 'AlignmentFlag')}")
    
    if hasattr(Qt, 'AlignmentFlag'):
        print(f"Qt.AlignmentFlag.AlignCenter = {Qt.AlignmentFlag.AlignCenter}")
        print(f"Qt.AlignmentFlag.AlignLeft = {Qt.AlignmentFlag.AlignLeft}")
    
    # Test the import that knowledge_renderer does
    from comprehension.ui.knowledge_renderer import MandalaView, TorusView
    print("knowledge_renderer imports successfully!")
    
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
