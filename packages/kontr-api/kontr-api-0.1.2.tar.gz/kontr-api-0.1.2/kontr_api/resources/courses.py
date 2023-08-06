from kontr_api.resources.default import Default, Defaults


class Courses(Defaults):
    def __init__(self, parent):
        super().__init__(parent, instance_klass=Course)


class Course(Default):
    @property
    def projects(self):
        from kontr_api.resources.projects import Projects
        return Projects(self)

    @property
    def roles(self):
        from kontr_api.resources.roles import Roles
        return Roles(self)

    @property
    def groups(self):
        from kontr_api.resources.groups import Groups
        return Groups(self)
