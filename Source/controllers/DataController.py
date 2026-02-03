from .BaseController import BaseController
from fastapi import UploadFile, File
from models import ResponseSignal
from .ProjectController import ProjectController
import re


class DataController(BaseController):
    
    def __init__(self):
        super().__init__()

    def validate_uploaded_file(self, file: UploadFile):
       if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
           return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
       return True, ResponseSignal.UPLOAD_SUCCESS.value 
    


    def generate_unique_filename(self, original_file_name: str, project_id: str):
        
        random_filename = self.get_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name = self.get_clean_file_name(original_file_name=original_file_name)

        new_file_path = os.path.join(project_path, f"{random_filename}_{cleaned_file_name}")


    def get_clean_file_name(self, original_file_name: str):
       cleaned_file_name = re.sub(r'[^\w.]','',original_file_name.strip())

       cleaned_file_name = cleaned_file_name.replace(" ","_")

       return cleaned_file_name