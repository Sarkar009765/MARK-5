import os
import shutil
from pathlib import Path
from tools.base import Tool, registry
from utils import logger

class ListFilesTool(Tool):
    name = "list_files"
    description = "List files in a directory"
    parameters = {
        "path": {"type": "string", "description": "Directory path"},
        "pattern": {"type": "string", "description": "File pattern (optional)"}
    }
    
    def execute(self, path: str = ".", pattern: str = "*") -> str:
        try:
            p = Path(path)
            files = list(p.glob(pattern))
            if not files:
                return "No files found"
            return "\n".join([f.name for f in files[:20]])
        except Exception as e:
            return f"Error: {e}"


class ReadFileTool(Tool):
    name = "read_file"
    description = "Read a file's contents"
    parameters = {
        "path": {"type": "string", "description": "File path"}
    }
    
    def execute(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()[:2000]
        except Exception as e:
            return f"Error reading: {e}"


class WriteFileTool(Tool):
    name = "write_file"
    description = "Write to a file"
    parameters = {
        "path": {"type": "string", "description": "File path"},
        "content": {"type": "string", "description": "Content to write"}
    }
    requires_confirmation = True
    
    def execute(self, path: str, content: str) -> str:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Written to {path}"
        except Exception as e:
            return f"Error: {e}"


class DeleteFileTool(Tool):
    name = "delete_file"
    description = "Delete a file"
    parameters = {
        "path": {"type": "string", "description": "File path"}
    }
    requires_confirmation = True
    
    def execute(self, path: str) -> str:
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return f"Deleted {path}"
        except Exception as e:
            return f"Error: {e}"


class CreateFolderTool(Tool):
    name = "create_folder"
    description = "Create a new directory"
    parameters = {
        "path": {"type": "string", "description": "Folder path"}
    }
    
    def execute(self, path: str) -> str:
        try:
            os.makedirs(path, exist_ok=True)
            return f"Created {path}"
        except Exception as e:
            return f"Error: {e}"


class FileInfoTool(Tool):
    name = "file_info"
    description = "Get file information"
    parameters = {
        "path": {"type": "string", "description": "File path"}
    }
    
    def execute(self, path: str) -> str:
        try:
            p = Path(path)
            if not p.exists():
                return "File not found"
            stat = p.stat()
            return (f"Name: {p.name}\n"
                    f"Size: {stat.st_size} bytes\n"
                    f"Modified: {stat.st_mtime}")
        except Exception as e:
            return f"Error: {e}"


registry.register(ListFilesTool())
registry.register(ReadFileTool())
registry.register(WriteFileTool())
registry.register(DeleteFileTool())
registry.register(CreateFolderTool())
registry.register(FileInfoTool())