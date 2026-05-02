"aqui será a lista de todos os projetos, e a criação de novos projetos"
from fastapi import APIRouter
from apps.services.GitHub_repositories import GitHubRepositoriesService

router = APIRouter(
    prefix="/Projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)
service = GitHubRepositoriesService(ttl_seconds=300)  # Cache de 5 minutos

LOCAL_PROJECTS = [
    {
        "name": "Projeto Local 1",
        "type": "chem",
        "description": "Descrição do Projeto Local 1",
        "created_at": "2024-01-01T00:00:00Z",
        "url": ""
        },
    {
        "name": "Projeto Local 2",
        "type": "dev",
        "description": "Descrição do Projeto Local 2",
        "created_at": "2024-02-01T00:00:00Z",
        "url": "",
        },
]

@router.get("/")
def home():
    return {"message": "Welcome to the Projects API!"}

@router.get("/chemprojects")
async def list_chem_projects():
    github_projects = await service.list_chem_projects("rogiw")
    return {"projects": github_projects + [proj for proj in LOCAL_PROJECTS if proj["type"] == "chem"]}
    
@router.get("/devprojects")
async def list_chem_projects():
    github_projects = await service.list_chem_projects("rogiw")
    return {"projects": github_projects + [proj for proj in LOCAL_PROJECTS if proj["type"] == "dev"]}