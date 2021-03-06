import sys


class ControllerError(BaseException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PygameDummyController(object):
    def __init__(self, plugged=0):
        self.default = 1.0

    def getAxis(self, button):
        return self.default

    def getButtons(self, button):
        return int(self.default)

    def getHats(self, button):
        return int(self.default)


class PygameController(object):
    # axis for which axis to read (button)
    # plugged for which controller to select

    def __init__(self, plugged=0):
        import pygame
        self.pygame = pygame
        self.pygame.init()
        try:
            self.joystick = self.pygame.joystick.Joystick(plugged)
            self.joystick.init()
            self.num_axis = self.joystick.get_numaxes()
            self.num_buttons = self.joystick.get_numbuttons()
            self.num_hats = self.joystick.get_numhats()

        except Exception:
            print("PygameController: no controllers found.")
            self.joystick = None

    def handleEvents(self):
        if self.joystick:
            self.pygame.event.pump()
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    sys.exit(0)
        else:
            return -1

    def getAxis(self, button):
        if self.joystick:
            self.handleEvents()
            if self.num_axis:
                return self.joystick.get_axis(button)
            else:
                raise ControllerError("No Axis")
        else:
            return -1

    def getButtons(self, button):
        if self.joystick:
            self.handleEvents()
            if self.num_buttons:
                return self.joystick.get_button(button)
            else:
                raise ControllerError("No Buttons")
        else:
            return -1

    def getHats(self, button):
        if self.joystick:
            self.handleEvents()
            if self.num_hats:
                return self.joystick.get_hat(button)
            else:
                raise ControllerError("No Hats")
        else:
            return -1

    def __del__(self):
        self.pygame.quit()
