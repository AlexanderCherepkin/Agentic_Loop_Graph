from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from docx.document import Document as _Document
    from docx.opc.package import PackagePart as _PackagePart
    
    class Document(_Document):
        def __init__(self, source: Any = ...) -> None: ...
    
    # Re-export main types
    Document = _Document

__all__ = ['Document']