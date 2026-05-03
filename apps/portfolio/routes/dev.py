from fastapi import APIRouter
from apps.services.GitHub_repositories import GitHubRepositoriesService
from apps.portfolio.projects.local_projects import LOCAL_PROJECTS

router = APIRouter(
    prefix="/dev",
    tags=["dev"],
)

service = GitHubRepositoriesService(ttl_seconds=300)


@router.get("/projects")
async def list_dev_projects():
    github_projects = await service.list_dev_projects("rogiw")
    local_projects = [proj for proj in LOCAL_PROJECTS if proj["type"] == "dev"]

    return {"projects": github_projects + local_projects}


@router.get("/lab")
async def list_dev_labs():
    return {"lab": ["alguns laboratórios de desenvolvimento"]}
