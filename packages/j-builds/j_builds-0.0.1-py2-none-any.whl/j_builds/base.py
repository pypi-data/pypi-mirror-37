import asyncio
from typing import Tuple, List
from abc import ABC, abstractmethod

from .printer import printer


async def run(cmd: str) -> Tuple[bool, str, str]:
    printer.scheduled(cmd)
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    # print(f'[{cmd!r} exited with {proc.returncode}]')
    # if stdout:
    #    print(f'[stdout]\n{stdout.decode()}')
    # if stderr:
    #    print(f'[stderr]\n{stderr.decode()}')

    if not proc.returncode:  # return code 0 means success
        printer.success(cmd)
    else:
        printer.error(cmd)

    return proc.returncode == 0, stdout.decode(), stderr.decode()


class Cmds(ABC):

    @staticmethod
    async def run(cmd):
        return await run(cmd)

    @abstractmethod
    async def aysnc_cmds(self)-> List[bool]:
        pass

    def run_all(self) -> bool:
        return all(asyncio.run(self.aysnc_cmds()))
