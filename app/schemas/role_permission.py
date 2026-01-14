from pydantic import BaseModel

class AssignPermissionRequest(BaseModel):
    permission_id: int
