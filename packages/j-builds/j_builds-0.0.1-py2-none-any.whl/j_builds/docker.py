import asyncio
from typing import List, Tuple

from .base import Cmds


class DockerCmds(Cmds):
    def __init__(self, repos: List[str], namespace: str) -> None:
        self.repos = repos
        self.namespace = namespace

    async def get_image_tag(self, repo: str) -> Tuple[bool, str]:
        # this could could can be overriden if you want a different tag
        git_cmd = 'git --no-pager log -1 --pretty=%h'
        cmd = f'cd {repo} && {git_cmd}'
        cmd_success, git_hash, _ = await self.run(cmd)

        return cmd_success, git_hash[:-1]  # \n

    async def build(self, repo: str, tag: str) -> bool:
        docker_cmd = 'docker build .'
        tag_arg = f'--tag {self.namespace}/{repo}:{tag}'
        latest_tag_arg = f'--tag {self.namespace}/{repo}:latest'
        cmd = f'cd {repo} && {docker_cmd} {tag_arg} {latest_tag_arg}'

        return (await self.run(cmd))[0]

    async def docker_push(self, target_repo: str, tag: str) -> bool:
        cmd = f'docker push {self.namespace}/{target_repo}:{tag}'

        return (await self.run(cmd))[0]

    async def build_push(self, repo: str) -> bool:
        tag_cmd_success, tag = await self.get_image_tag(repo)
        if tag_cmd_success:
            build_cmd_success = await self.build(repo, tag)
            if build_cmd_success:
                return all(await asyncio.gather(
                    *[self.docker_push(repo, _tag) for _tag in [tag, 'latest']]
                ))

        return False

    async def aysnc_cmds(self) -> List[bool]:
        return await asyncio.gather(
            *[self.build_push(entry) for entry in self.repos]
        )
