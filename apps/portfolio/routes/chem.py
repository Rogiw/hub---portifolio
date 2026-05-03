from fastapi import APIRouter
from apps.services.GitHub_repositories import GitHubRepositoriesService
from apps.portfolio.projects.local_projects import LOCAL_PROJECTS

service = GitHubRepositoriesService(ttl_seconds=300)

router = APIRouter(
    prefix="/chem",
    tags=["chem"],
)

@router.get("/projects")
async def list_chem_projects():
    github_projects = await service.list_chem_projects("rogiw")
    local_projects = [proj for proj in LOCAL_PROJECTS if proj["type"] == "chem"]

    return {"projects": github_projects + local_projects}

@router.get("/lab")
async def list_chem_labs():
    return {"lab": ["lab de quimica em desenvolvimento"]}

@router.get("/experiments")
async def list_chem_experiments():
    return {"experiments": ["alguns experimentos químicos"]}
