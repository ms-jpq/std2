from subprocess import CalledProcessError
from unittest import IsolatedAsyncioTestCase

from ...std2.asyncio.subprocess import call


class Call(IsolatedAsyncioTestCase):
    async def test_1(self) -> None:
        stdin = b"tee"
        proc = await call("tee", stdin=stdin)
        self.assertEqual(proc.code, 0)
        self.assertEqual(proc.out, stdin)
        self.assertEqual(proc.err, "")

    async def test_2(self) -> None:
        stdin = b"tee"
        with self.assertRaises(CalledProcessError) as ctx:
            await call("tee", stdin=stdin, expected_code=2)

        self.assertEqual(ctx.exception.returncode, 0)
        self.assertEqual(ctx.exception.stdout, stdin)
        self.assertEqual(ctx.exception.stderr, "")
