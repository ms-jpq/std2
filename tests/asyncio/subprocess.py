from unittest import IsolatedAsyncioTestCase

from ...std2.asyncio.subprocess import call


class Call(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        stdin = b"tee"
        proc = await call("tee", stdin=stdin)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, stdin)
        self.assertEqual(proc.stderr, b"")
