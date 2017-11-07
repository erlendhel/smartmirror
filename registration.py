''' Wrapper for the functions used in user registration '''

from db import smartmirrordb
from facerec import register_face
from speech_rec import registration_speech


class Registration(object):
    db = None
    speech = None

    def __init__(self):
        self.db = smartmirrordb.UserDB()
        self.speech = registration_speech.Registration()

    def set_user_name(self, name):
        # name = self.speech.get_name()
        print(name)
        self.db.register_user(name, None, None, None, None, None)
        id = self.db.get_max_id()
        return id

    def add_user_face(self, id):
        path = register_face.add_face(id)
        self.db.update_path(id, path)
        
if __name__ == '__main__':
    reg = Registration()
    id = reg.set_user_name('Placeholder')
    reg.add_user_face(id)
    del register_face.camera
