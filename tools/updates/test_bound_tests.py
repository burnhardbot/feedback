import unittest
from bound_tests import bound_command, apply_bound_report
from test_process_test_comment import event, comments, FakeGitHub, ROLES
from continuous_tests import BEGIN, END

REGISTRY = {"schema":1,"builds":[{"version":"v1.2.46","buildId":"fixture-build","packageSha256":"a"*64,"status":"prepared"}]}
def report(ident="T03", status="PASS", detail="OBS am Testrechner geprüft"):
    return event(body=f"/test {ident} {status} v1.2.46 build:fixture-build sha256:{'a'*64} – {detail}")

class BoundTests(unittest.TestCase):
    def test_blocked_new_build_never_clears_historical_pass(self):
        e=report('T04','BLOCKIERT');g=FakeGitHub(comments(e))
        self.assertIn('historical',apply_bound_report(g,e,ROLES,REGISTRY));self.assertIn('- [x] **T04',g.body);self.assertFalse(g.patches)
    def test_exact_build_required(self):
        self.assertEqual(bound_command(report()["comment"]["body"],REGISTRY)["buildId"],"fixture-build")
        for body in [event()["comment"]["body"],report()["comment"]["body"].replace("a"*64,"b"*64),report()["comment"]["body"].replace("fixture-build","other-build")]:
            with self.assertRaises(ValueError): bound_command(body,REGISTRY)
    def test_history_pass_survives_regression_and_retry(self):
        e=report("T04","FAIL");g=FakeGitHub(comments(e));g.body += BEGIN+"\n"+END
        self.assertIn("T05",apply_bound_report(g,e,ROLES,REGISTRY))
        self.assertIn("- [x] **T04",g.body);self.assertIn("- [ ] **T05",g.body)
        self.assertIn("already",apply_bound_report(g,e,ROLES,REGISTRY));self.assertEqual(g.body.count("**T05"),1)
    def test_changed_evidence_is_not_old_event(self):
        e=report();g=FakeGitHub(comments(report(detail="Nachträglich veränderte Aussage")))
        self.assertIn("edited",apply_bound_report(g,e,ROLES,REGISTRY));self.assertFalse(g.patches)
    def test_unauthorized_never_writes(self):
        e=report();e["sender"]["login"]=e["comment"]["user"]["login"]="public-visitor";g=FakeGitHub(comments(e))
        self.assertIn("unauthorized",apply_bound_report(g,e,ROLES,REGISTRY));self.assertFalse(g.patches)
    def test_missing_observation_rejected(self):
        with self.assertRaises(ValueError):bound_command(report(detail="")["comment"]["body"],REGISTRY)
    def test_screenshot_markdown_is_preserved(self):
        e=report(detail="OBS Fenster am Testgerät geprüft\n![Screenshot](https://github.com/user-attachments/assets/fixture)")
        self.assertEqual(bound_command(e["comment"]["body"],REGISTRY)["id"],"T03")
    def test_newer_report_blocks_old_regression(self):
        old=report("T04","FAIL");new=report("T04","PASS");new["comment"]["id"]=101;new["comment"]["created_at"]="2026-11-13T15:00:00Z"
        g=FakeGitHub(comments(old,new));g.body+=BEGIN+"\n"+END
        self.assertIn("superseded",apply_bound_report(g,old,ROLES,REGISTRY));self.assertFalse(g.patches)
    def test_repeated_open_regression_does_not_allocate_again(self):
        e=report("T04","FAIL");g=FakeGitHub(comments(e));g.body+=BEGIN+"\n"+END
        apply_bound_report(g,e,ROLES,REGISTRY)
        later=report("T04","FAIL");later["comment"]["id"]=101;later["comment"]["created_at"]="2026-11-13T15:00:00Z";g.comments.append(later["comment"])
        self.assertIn("existing open",apply_bound_report(g,later,ROLES,REGISTRY));self.assertNotIn("**T06",g.body)

if __name__=="__main__":unittest.main()
