import asyncio
from typing import List

from .base import Cmds


class GitCmds(Cmds):
    def __init__(self, repos: List[str], branch_name: str = 'master') -> None:
        self.repos = repos
        self.branch_name = branch_name

    async def pull_master(self, target_repo: str) -> bool:
        cmd = f'cd {target_repo} && git pull origin {self.branch_name}'
        return (await self.run(cmd))[0]

    async def aysnc_cmds(self) -> List[bool]:
        return await asyncio.gather(
            *[self.pull_master(entry) for entry in self.repos]
        )
