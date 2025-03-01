import os
import shutil
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
__package__ = "slurm"
from .context import (
    Dispatcher,
    my_file_cmp,
    setUpModule,  # noqa: F401
)


@unittest.skipIf(not shutil.which("sbatch"), "requires Slurm")
class TestDispatcher(unittest.TestCase):
    def setUp(self):
        os.makedirs("loc", exist_ok=True)
        os.makedirs("rmt", exist_ok=True)
        os.makedirs("loc/task0", exist_ok=True)
        os.makedirs("loc/task1", exist_ok=True)
        os.makedirs("loc/task2", exist_ok=True)
        for ii in ["loc/task0", "loc/task1", "loc/task2"]:
            with open(os.path.join(ii, "test0"), "w") as fp:
                fp.write("this is test0 from " + ii + "\n")
        work_profile = {"work_path": "rmt"}
        self.disp = Dispatcher(work_profile, "local", "slurm")

    def tearDown(self):
        shutil.rmtree("loc")
        shutil.rmtree("rmt")
        if os.path.exists("dpgen.log"):
            os.remove("dpgen.log")

    def test_sub_success(self):
        tasks = ["task0", "task1", "task2"]
        self.disp.run_jobs(
            None,
            "cp test0 test1",
            "loc",
            tasks,
            2,
            [],
            ["test0"],
            ["test1", "hereout.log", "hereerr.log"],
            outlog="hereout.log",
            errlog="hereerr.log",
        )
        for ii in tasks:
            my_file_cmp(
                self, os.path.join("loc", ii, "test0"), os.path.join("loc", ii, "test1")
            )
            self.assertTrue(os.path.isfile(os.path.join("loc", ii, "hereout.log")))
            self.assertTrue(os.path.isfile(os.path.join("loc", ii, "hereerr.log")))
