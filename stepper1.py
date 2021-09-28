import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
spi = spidev.SpiDev()
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.uix.slider import Slider
from kivy.properties import ObjectProperty
from threading import Thread

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'stepper1'

# Init a 200 steps per revolution stepper on Port 0
s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=2)

class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER

Window.clearcolor = (0.92, 0.97, 0.97, 1)  # White

class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """

    my_slider = ObjectProperty(None)
    slider_label = ObjectProperty(None)
    position_label = ObjectProperty(None)

    def start_stepper(self):
        """
        Function that turns on the stepper
        """
        s0.go_until_press(0, self.my_slider.value*6400)

    def stop_stepper(self):
        """
        Function that turns off stepper
        """
        s0.softStop()

    def change_direction(self):
        """
        Function that runs stepper counter-clockwise
        """
        s0.go_until_press(1, self.my_slider.value*6400)

    def speed_slider(self):
        """
        create slider to control the speed of the motor (range 1 to 5)
        """
        self.my_slider
        self.slider_label
        s0.set_speed(self.my_slider.value)

    def get_position(self):
        """
        function that prints position of stepper to label on screen
        """
        self.position_label.text = str(s0.get_position_in_units())

    def thread_spin(self):
        Thread(target=self.spin).start()

    def spin(self):
        self.get_position()
        s0.set_speed(1)
        s0.start_relative_move(15)
        self.get_position()
        sleep(15)
        self.get_position()

        sleep(11)
        s0.set_speed(5)
        s0.start_relative_move(10)
        sleep(2)
        self.get_position()

        sleep(8)
        s0.goHome()
        sleep(10)
        self.get_position()

        s0.set_speed(8)
        s0.start_relative_move(32)
        sleep(6)
        self.get_position()

        sleep(10)
        s0.goHome()
        sleep(5)
        self.get_position()


Builder.load_file('stepper1.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()



