from typing import Dict, List, Optional
from datetime import datetime
import json
import os
from collections import defaultdict
import hashlib
from .models import PDFMetadata, PDFDocument
import logging

logger = logging.getLogger(__name__)

class PDFStateManager:
    _instance = None
    _initialized = False
    STORAGE_FILE = "pdf_metadata.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PDFStateManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.initialize()
            self.__class__._initialized = True

    def initialize(self):
        self.pdfs: Dict[str, PDFDocument] = {}
        self.filename_index: Dict[str, List[str]] = defaultdict(list)
        self.size_index: Dict[int, List[str]] = defaultdict(list)
        self.date_index: Dict[datetime.date, List[str]] = defaultdict(list)
        self.load_state()

    def save_state(self):
        """Persist the current state to a JSON file"""
        try:
            state = {
                'pdfs': {
                    pdf_id: {
                        'pdf_id': pdf.pdf_id,
                        'filename': pdf.filename,
                        'path': pdf.path,
                        'extracted_text': pdf.extracted_text,
                        'created_at': pdf.created_at.isoformat()
                    } for pdf_id, pdf in self.pdfs.items()
                },
                'filename_index': {k: v for k, v in self.filename_index.items()},
                'size_index': {str(k): v for k, v in self.size_index.items()},  # Convert int keys to str
                'date_index': {k.isoformat(): v for k, v in self.date_index.items()}  # Convert dates to ISO format
            }
            
            with open(self.STORAGE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
                
            logger.info(f"State saved successfully to {self.STORAGE_FILE}")
        except Exception as e:
            logger.error(f"Error saving state: {str(e)}")

    def load_state(self):
        """Load the state from the JSON file"""
        try:
            if not os.path.exists(self.STORAGE_FILE):
                logger.info(f"No existing state file found at {self.STORAGE_FILE}")
                return

            with open(self.STORAGE_FILE, 'r') as f:
                state = json.load(f)

            # Restore PDFs
            for pdf_id, pdf_data in state['pdfs'].items():
                self.pdfs[pdf_id] = PDFDocument(
                    pdf_id=pdf_data['pdf_id'],
                    filename=pdf_data['filename'],
                    path=pdf_data['path'],
                    content=None,  # Content is not stored in JSON
                    extracted_text=pdf_data['extracted_text'],
                    created_at=datetime.fromisoformat(pdf_data['created_at'])
                )

            # Restore indices
            self.filename_index.update(state['filename_index'])
            self.size_index.update({int(k): v for k, v in state['size_index'].items()})
            self.date_index.update({
                datetime.fromisoformat(k).date(): v 
                for k, v in state['date_index'].items()
            })

            logger.info(f"State loaded successfully from {self.STORAGE_FILE}")
        except Exception as e:
            logger.error(f"Error loading state: {str(e)}")

    def add_pdf(self, pdf_id: str, filename: str, content: bytes, path: str, extracted_text: Optional[str] = None) -> None:
        """Add a new PDF and update indices"""
        try:
            file_hash = hashlib.sha256(content).hexdigest()
            metadata = PDFMetadata(
                filename=filename,
                upload_date=datetime.now(),
                file_size=len(content),
                file_hash=file_hash,
                content_type="application/pdf"
            )
            
            self.pdfs[pdf_id] = PDFDocument(
                pdf_id=pdf_id,
                filename=filename,
                content=None,  # Don't store content in memory
                path=path,
                extracted_text=extracted_text,
                created_at=datetime.now()
            )
            
            # Update indices
            self.filename_index[filename].append(pdf_id)
            self.size_index[len(content)].append(pdf_id)
            self.date_index[metadata.upload_date.date()].append(pdf_id)
            
            # Save state after each addition
            self.save_state()
            
            logger.info(f"PDF {filename} (ID: {pdf_id}) added successfully")
        except Exception as e:
            logger.error(f"Error adding PDF: {str(e)}")
            raise

    def get_pdf(self, pdf_id: str) -> Optional[PDFDocument]:
        """Get PDF by ID"""
        pdf = self.pdfs.get(pdf_id)
        print(pdf)
        if pdf and os.path.exists(pdf.path):
            # Load content from file if needed
            with open(pdf.path, 'rb') as f:
                content = f.read()
            pdf.content = content
        return pdf

    def get_all_pdfs(self) -> List[PDFDocument]:
        """Get all PDFs"""
        return list(self.pdfs.values())

    def search_by_filename(self, filename: str) -> List[PDFDocument]:
        """Search PDFs by filename"""
        pdf_ids = self.filename_index.get(filename, [])
        return [self.pdfs[pid] for pid in pdf_ids if pid in self.pdfs]

    def search_by_size_range(self, min_size: int, max_size: int) -> List[PDFDocument]:
        """Search PDFs by size range"""
        results = []
        for size, pdf_ids in self.size_index.items():
            if min_size <= size <= max_size:
                results.extend([self.pdfs[pid] for pid in pdf_ids if pid in self.pdfs])
        return results
