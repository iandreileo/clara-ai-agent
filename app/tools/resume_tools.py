from langchain_core.tools import tool
from app.services.http_service import HTTPClient
from app.api.v1.models import PersonalInfo, WorkExperience, Education
from langchain_core.runnables import RunnableConfig
from app.core.config import settings

# List to collect all tools
resume_tools = []

def get_user_token(config: RunnableConfig) -> str:
    configuration = config.get("configurable", {})
    
    return configuration.get("user_token", None)

@tool
async def save_personal_info(personal_info: PersonalInfo, *, config: RunnableConfig) -> str:
    """Saves the personal information section of the resume."""
    user_token = get_user_token(config)

    # get the args from the state
    print("Personal info:", personal_info)

    async with HTTPClient() as client:
        response = await client.post(
            settings.RESUME_API_BASE_URL,
            json=personal_info.model_dump(),
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        print("Response:", response)

    return "Personal information saved successfully"


@tool
async def save_work_experience(work_experience: list[WorkExperience], *, config: RunnableConfig) -> str:
    """Saves the work experience section of the resume."""
    user_token = get_user_token(config)
    
    print("Work experience:", work_experience)

    # iterate over the work experience list and convert each item to a dictionary
    work_experience_list = [work_experience.model_dump() for work_experience in work_experience]

    print("Work experience list:", work_experience_list)

    async with HTTPClient() as client:
        response = await client.post(
            settings.RESUME_API_BASE_URL,
            json=work_experience_list,
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        print("Response:", response)

    return "Work experience saved successfully"

@tool
async def save_education(education: list[Education], *, config: RunnableConfig) -> str:
    """Saves the education section of the resume."""
    user_token = get_user_token(config)
    
    print("Education:", education)

    # iterate over the education list and convert each item to a dictionary
    education_list = [education.model_dump() for education in education]

    print("Education list:", education_list)

    async with HTTPClient() as client:
        response = await client.post(
            settings.RESUME_API_BASE_URL,
            json=education_list,
            headers={"Authorization": f"Bearer {user_token}"}
        )
        
        print("Response:", response)

    return "Education information saved successfully" 



resume_tools = [
    save_personal_info,
    save_work_experience,
    save_education
]