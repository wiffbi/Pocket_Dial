#__init__.py
import Live

if Live.Application.get_application().get_major_version() == 9:
    from PocketDial9 import PocketDial
else:
    from PocketDial8 import PocketDial

def create_instance(c_instance):
    return PocketDial(c_instance)
