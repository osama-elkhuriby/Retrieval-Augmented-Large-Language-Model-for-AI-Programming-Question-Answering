from .BaseController import BaseController
from fastapi import UploadFile, File


class DataController(BaseController):
    
    def __init__(self):
        super().__init__(self)

    def validate_uploaded_file(self, file: UploadFile):
       if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
           return False, "File type not allowed."
       return True, "File is valid." 