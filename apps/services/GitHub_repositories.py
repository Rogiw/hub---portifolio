import os, re, time, base64
from typing import Any
import httpx
from dotenv import load_dotenv
load_dotenv()




    
    

class GitHubRepositoriesService:
    GITHUB_API = "https://api.github.com"
    MARKER = "))--COMPUTHUB--(("

    def __init__(self, ttl_seconds: int = 360) -> None:
        self.ttl_seconds = ttl_seconds
        self._cache_projects: list[dict[str, Any]] = []
        self._cache_updated_at: float = 0.0

    """"))--COMPUTHUB--(( {
     "project_type": "chem",
     "status": "active",
     "created_at": "2024-01-01T00:00:00Z",
     "description": "Description of the project",
     "url": "}"""

    def _headersGITHUB(self) -> dict[str, Any]:
        token = os.getenv("GITHUB_TOKEN")
        if token is None:
            raise ValueError("GITHUB_TOKEN environment variable is not set.")
        headers = {"Authorization": f"token {token}"}
        return headers
    
    def _is_cache_valid(self) -> bool:
        if not self._cache_projects:
            return False
        return (time.time() - self._cache_updated_at)

    """tabela com simbolos regex
    r""	string “crua” (Python não interpreta \)
    \	escape (torna caractere literal)
    .	qualquer caractere
    \w	letra, número ou _
    \d	dígito (0-9)
    \s	espaço (inclui tab/quebra)
    +	um ou mais
    *	zero ou mais
    ?	opcional / não guloso
    .*?	qualquer coisa (mínimo possível)
    ()	grupo / captura
    []	conjunto de caracteres
    ^	início da linha
    $	fim da linha
    {}	quantidade ou literal (com \{ \})
    \( \)	parênteses literais
    \{ \}	chaves literais
    `	` limite de palavra
    """

    def extract_project_type(self, readme_text: str) -> str | None:
        pattern = r"\)\)\-\-COMPUTHUB\-\-\(\(\{.*?type\s*:\s*(\w+).*?\}"
        match = re.search(pattern, readme_text, re.DOTALL)
        if not match:
            return ValueError("Autor do projeto não colocou o type do projeto no readme")
        return match.group(1)
    
    async def _fetch_projects_from_github(self, username: str) -> list[dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            repositories = await client.get(f"{self.GITHUB_API}/users/{username}/repos", headers=self._headersGITHUB())
            repositories.raise_for_status()
            repositories = repositories.json()


            """estamos validadando os projetos do usuário, verificando se eles possuem o marcador específico no nome ou descrição"""

            projects: list[dict[str, Any]] = []
            for repositorie in repositories:
                readme_url = f"{self.GITHUB_API}/repos/{username}/{repositorie['name']}/readme"
                readme_response = await client.get(readme_url, headers=self._headersGITHUB())
                if readme_response.status_code is not 200:
                    continue
                    
                """estamos pegando o readme vendo se tem aquela marcação acima para adicionar a lista de projetos"""

                readme_text = readme_response.json().get("content", "")
                
                project_type = self.extract_project_type(readme_text)
                
                if self.MARKER and project_type:
                    projects.append(
                        {
                            "name": repositorie["name"],
                            "type": project_type,
                            "description": repositorie.get("description", ""),
                            "created_at": repositorie["created_at"],
                            "url": repositorie["html_url"]
                        }
                    )
            return projects
    
    async def list_projects(self, username: str) -> list[dict[str, Any]]:
        if self._is_cache_valid():
            return self._cache_projects
        
        projects = await self._fetch_projects_from_github(username)
        self._cache_projects = projects
        self._cache_updated_at = time.time()
        return projects
    
    async def list_projects_by_type(self, username:str, project_type: str) -> list[dict[str, Any]]:
        projects = await self.list_projects(username)
        return [project for project in projects if project["type"] == project_type]
    
    async def list_chem_projects(self, username:str) -> list[dict[str, Any]]:
        return await self.list_projects_by_type(username, "chem")
    
    async def list_dev_projects(self, username:str) -> list[dict[str, Any]]:
        return await self.list_projects_by_type(username, "dev")