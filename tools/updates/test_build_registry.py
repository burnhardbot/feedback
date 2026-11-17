import json
import unittest
from publish_github import publish
from continuous_tests import validate_manifest
from test_publish_github import FakeGitHub, manifest

class BuildRegistryTests(unittest.TestCase):
    def test_register_exact_package_without_installation_claim(self):
        g=FakeGitHub();m={**manifest('v1.2.46','T20'),'package_sha256':'a'*64}
        publish(g,m);data=json.loads(g.files['docs/updates/build-registry.json'][0])
        self.assertEqual(data['builds'][0]['packageSha256'],'a'*64);self.assertEqual(data['builds'][0]['status'],'prepared')
        publish(g,m);self.assertEqual(len(json.loads(g.files['docs/updates/build-registry.json'][0])['builds']),1)
    def test_same_build_cannot_be_rebound_to_another_package(self):
        g=FakeGitHub();m={**manifest('v1.2.46','T20'),'package_sha256':'a'*64};publish(g,m)
        before=dict(g.files)
        with self.assertRaises(ValueError):publish(g,{**m,'package_sha256':'b'*64})
        self.assertEqual(before,g.files)
    def test_private_infrastructure_never_enters_public_manifest(self):
        for text in ['Server http://100.100.100.100:3001','Korrektur #104','Pfad C:\\Tools\\private','Webhook: geheim','Server rechner.tailnet.ts.net']:
            with self.assertRaises(ValueError):validate_manifest({**manifest('v1.2.46','T20'),'changes':[text]})
    def test_invalid_package_digest_and_installation_claim_rejected(self):
        for patch in [{'package_sha256':'not a checksum'},{'status':'installed'}]:
            with self.assertRaises(ValueError):validate_manifest({**manifest('v1.2.46','T20'),**patch})

if __name__=='__main__':unittest.main()
