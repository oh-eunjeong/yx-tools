import json
import tempfile
import unittest
from pathlib import Path

from cloudflare_speedtest import load_deploy_json


class DeployJsonTests(unittest.TestCase):
    def test_load_deploy_json_returns_worker_domain_and_uuid(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "deploy_result.json"
            p.write_text(json.dumps({
                "workerDomain": "example.pages.dev",
                "uuid": "abc",
            }), encoding="utf-8")

            worker_domain, uuid = load_deploy_json(str(p))
            self.assertEqual(worker_domain, "example.pages.dev")
            self.assertEqual(uuid, "abc")

    def test_load_deploy_json_accepts_snake_case_worker_domain(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "deploy_result.json"
            p.write_text(json.dumps({
                "worker_domain": "example.pages.dev",
                "uuid": "abc",
            }), encoding="utf-8")

            worker_domain, uuid = load_deploy_json(str(p))
            self.assertEqual(worker_domain, "example.pages.dev")
            self.assertEqual(uuid, "abc")

    def test_load_deploy_json_rejects_missing_fields(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "deploy_result.json"
            p.write_text(json.dumps({
                "workerDomain": "",
                "uuid": "",
            }), encoding="utf-8")

            with self.assertRaises(ValueError):
                load_deploy_json(str(p))


if __name__ == "__main__":
    unittest.main()

