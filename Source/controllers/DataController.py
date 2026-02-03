from .BaseController import BaseController
from fastapi import UploadFile, File
from models import ResponseSignal


class DataController(BaseController):
    
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile):
       if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
           return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
       return True, ResponseSignal.UPLOAD_SUCCESS.value 