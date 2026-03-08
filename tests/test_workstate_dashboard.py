import copy
import runpy
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "tools" / "workstate-dashboard.py"
)
TOOLS_DIR = SCRIPT_PATH.parent


class WorkstateDashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(TOOLS_DIR))
        cls.mod = runpy.run_path(str(SCRIPT_PATH))
        cls.globals = cls.mod["get_sessions_json"].__globals__

    def setUp(self):
        self.globals["sessions"].clear()
        self.globals["expired"].clear()
        self.original_warn_seconds = self.globals["WARN_SECONDS"]
        self.original_stale_seconds = self.globals["STALE_SECONDS"]
        self.original_service_cache = copy.deepcopy(self.globals["_service_status_cache"])
        self.original_probe_http_service = self.globals["_probe_http_service"]
        self.original_probe_statuspage_service = self.globals["_probe_statuspage_service"]
        self.original_fetch_statuspage_summary = self.globals["_fetch_statuspage_summary"]

    def tearDown(self):
        self.globals["WARN_SECONDS"] = self.original_warn_seconds
        self.globals["STALE_SECONDS"] = self.original_stale_seconds
        self.globals["_service_status_cache"].clear()
        self.globals["_service_status_cache"].update(copy.deepcopy(self.original_service_cache))
        self.globals["_probe_http_service"] = self.original_probe_http_service
        self.globals["_probe_statuspage_service"] = self.original_probe_statuspage_service
        self.globals["_fetch_statuspage_summary"] = self.original_fetch_statuspage_summary

    def test_staleness_thresholds(self):
        now_iso = self.mod["now_iso"]()
        self.assertEqual(self.mod["staleness"](now_iso), "ok")

        self.globals["WARN_SECONDS"] = 1
        self.globals["STALE_SECONDS"] = 2
        self.assertEqual(self.mod["staleness"]("1970-01-01T00:00:00+00:00"), "idle")

    def test_session_lifecycle(self):
        upsert = self.mod["upsert_session"]

        body, code = upsert({"session_id": "s1", "name": "session-1", "task": "t1"})
        self.assertEqual(code, 200)
        self.assertEqual(body["active_sessions"], 1)
        self.assertIn("s1", self.globals["sessions"])

        body, code = upsert({"session_id": "s1", "task": "t2", "status": "Running"})
        self.assertEqual(code, 200)
        self.assertEqual(self.globals["sessions"]["s1"].task, "t2")
        self.assertEqual(self.globals["sessions"]["s1"].history[-1], "t1")

        body, code = upsert({"session_id": "s1", "status": "Done", "task": "done"})
        self.assertEqual(code, 200)
        self.assertNotIn("s1", self.globals["sessions"])
        self.assertGreaterEqual(len(self.globals["expired"]), 1)

    def test_template_file_present(self):
        template = Path(__file__).resolve().parents[1] / "tools" / "workstate-dashboard.template.html"
        self.assertTrue(template.exists())

    def test_get_sessions_json_includes_dashboard_and_service_cache(self):
        self.globals["_service_status_cache"]["data"] = {
            "items": [{"id": "frontend", "state": "online", "label": "Online"}],
            "summary": {"online": 1, "degraded": 0, "offline": 0},
            "updated_at": "2026-03-08T00:00:00+00:00",
        }

        payload = self.mod["get_sessions_json"]()

        self.assertEqual(payload["services"]["items"][0]["id"], "frontend")
        self.assertIn("service_groups", payload["dashboard"])
        self.assertIn("page_groups", payload["dashboard"])

    def test_get_service_statuses_uses_configured_groups(self):
        dashboard = self.globals["DASHBOARD_UI_CONFIG"]
        statuspage_components = {}
        for group in dashboard["service_groups"]:
            for service in group.get("services", []):
                if service.get("kind") == "statuspage_component":
                    statuspage_components[service["component_id"]] = {
                        "status": "operational",
                        "description": "ok",
                    }

        self.globals["_fetch_statuspage_summary"] = lambda timeout=10.0: statuspage_components
        self.globals["_probe_http_service"] = lambda service, timeout=5.0: {
            "id": service["id"],
            "name": service["name"],
            "display_url": service.get("display_url", ""),
            "link_url": service.get("link_url", ""),
            "state": "online",
            "label": "Online",
            "detail": "HTTP 200",
            "latency_ms": 12,
            "checked_at": "2026-03-08T00:00:00+00:00",
        }
        self.globals["_probe_statuspage_service"] = lambda service, components: {
            "id": service["id"],
            "name": service["name"],
            "display_url": service.get("display_url", ""),
            "link_url": service.get("link_url", ""),
            "state": "online",
            "label": "Operational",
            "detail": "ok",
            "latency_ms": None,
            "checked_at": "2026-03-08T00:00:00+00:00",
        }

        result = self.mod["_get_service_statuses"]()
        expected_count = sum(
            len(group.get("services", [])) for group in dashboard["service_groups"]
        )

        self.assertEqual(len(result["items"]), expected_count)
        self.assertEqual(result["summary"]["online"], expected_count)
        self.assertEqual(result["summary"]["degraded"], 0)
        self.assertEqual(result["summary"]["offline"], 0)


if __name__ == "__main__":
    unittest.main()
