import unittest
import borobudur.schema
import colander


class TestRepository(unittest.TestCase):

    def test_register(self):
        repository = borobudur.schema.SchemaRepository()
        friend = repository.add_mapping("Friend", {
            "rank": colander.SchemaNode(colander.Int(), validator=colander.Range(0, 9999)),
            "name": colander.SchemaNode(colander.String()),
            })
        self.assertIsNot(friend, None)
        self.assertEquals(friend, repository.get("Friend"))
        self.assertEquals(len(friend.children), 2)


    def test_child(self):
        """
        testing by counting mapping children
        """

        repository = borobudur.schema.SchemaRepository()
        project = repository.add_mapping("Project", {
            "rank": colander.SchemaNode(colander.Int(), validator=colander.Range(0, 9999)),
            "name": colander.SchemaNode(colander.String()),
        })
        self.assertEquals(len(project.children), 2)

        name_only = repository.add_child("Project", "name_only", {
            "remove": ["rank"],
        })
        self.assertEquals(len(name_only.children), 1)

        nothing = repository.modify(name_only, "nothing", {
            "remove": ["name"],
        })
        self.assertEquals(len(nothing.children), 0)

        int_named = repository.add_child("Project", "int_named_friend", {
            "alter": {
                "name": colander.SchemaNode(colander.Int())
            }
        })
        self.assertEquals(len(int_named.children), 2)


    def test_embedded(self):
        repository = borobudur.schema.SchemaRepository()
        project = repository.add_mapping("Project", {
            "rank": colander.SchemaNode(colander.Int(), validator=colander.Range(0, 9999)),
            "name": colander.SchemaNode(colander.String()),
            })

        name_only = repository.add_child("Project", "name_only", {
            "remove": ["rank"],
            })

        phone = repository.add_mapping("Phone", {
            "name": colander.SchemaNode(colander.String()),
            "project": project
        })

        altered_phone = repository.add_child("Phone", "altered_phone", {
            "alter": {
                "friend": name_only,
                }
        })

    def test_sequence(self):
        repository = borobudur.schema.SchemaRepository()
        friend = repository.add_mapping("Friend", {
            "rank": colander.SchemaNode(colander.Int(), validator=colander.Range(0, 9999)),
            "name": colander.SchemaNode(colander.String()),
            })
        friends = repository.add_sequence("Friends", friend)


