from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum


class ProjectModel(BaseDataModel):
    def __init__(self, db_client:object):
        super().__init__(db_client = db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTIONS_PROJECT_NAME.value]

    async def create_project(self, project:Project):

        result = await self.collection.insert_one(project.dict())

        return result.inserted_id
    
    