from pydantic import BaseModel

class AssignRoleRequest(BaseModel):
    role_code: str
    app_code: str
