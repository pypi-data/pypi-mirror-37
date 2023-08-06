import logging, os, uuid

class UserBase():
    
    def __init__(self, _project):
        self._path = None
        self.uuid4 = uuid.uuid4()
        self.project = _project
        self._name = 'Untitled user {0}'.format(len(self.project.users))
        self.name = self._name
        self.connection = 'local'
        
        self.project += self

    @property
    def name(self):
        """
        Get and set setup name

        :rtype: str
        """
        return self._name

    @property
    def path(self):
        if self.project.path is None: return None
        return os.path.join(self.project.path, 'users', self.name)


    @name.setter
    def name(self, value):      self._name = value

    def __unicode__(self):  return self.name
    def __str__(self):      return self.__unicode__()
        