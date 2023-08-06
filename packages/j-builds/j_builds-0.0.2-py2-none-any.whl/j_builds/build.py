from typing import List
from .git import GitCmds
from .docker import DockerCmds


def build(repos: List[str], docker_namespace: str) -> bool:
    if not GitCmds(repos).run_all():
        return False  # failed to pull some repo, abort

    if not DockerCmds(repos, docker_namespace).run_all():
        return False  # falid to build/push image

    return True
