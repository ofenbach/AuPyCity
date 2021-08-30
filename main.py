
from ui import UI


if __name__ == '__main__':
    """ Load UI Items, Display Default UI """
    interface = UI()
    interface.load_ui()
    interface.display_default_ui()
    interface.display_loop()