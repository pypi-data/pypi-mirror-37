"""
@Author: Amardjia Amine
@Mail: amardjia.amine@gmail.com
@Licence: MIT

# laylib for pygame package:

This package is made to fast prototype your multimedia applications
like games on pygame.

Write clean and pragmatic design. It lets you focus on the game engine
itself, so you dont have to take care about several details like setting
up the window, loading and cheking data (images, sound, font, fx, music,
resources names...).
All you need to do is to put your resources into a specific data folder
and use them in your game class 'MyEngine()'.

You don't need to reinvent the wheel, some repetitive parts of code
(main loop, getting the delta time, closing the window, drawing text...)
are already described and ready to use in the default engine.

See the README.MD for more details.

Release History:

- v0.0.1 Work in progress
- v0.1   The first proper release
- v1.1.1 Now we can set the 'time_unit' to change the delta_time unit.
- v1.1.2 Removed functions: load_global/destroy_global from Resources class.
         + Bug version fix (setup.py file).
"""


__version__ = "1.1.2"

import pygame as pg
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(message)s')


class Environment(object):

    def __init__(self,
                 screenWidth,
                 screenHeight,
                 fullscreen,
                 windowTitle):

        flag = 0
        pg.init()
        if not pg.display.get_init():
            logging.info('unable to init display pygame')
            self.destroy()
        else:
            pg.display.set_caption(windowTitle)
            if fullscreen:
                flag |= pg.FULLSCREEN
                # try the HWA if available..
                flag |= pg.HWSURFACE
                flag |= pg.DOUBLEBUF
            pg.display.set_mode((screenWidth, screenHeight), flag)
            logging.info('Display done (driver -> {})'
                         .format(pg.display.get_driver()))
            logging.info(pg.display.Info())
            pg.key.set_mods(0)
            pg.key.set_repeat(10, 10)
            pg.mixer.init()
            if pg.mixer.get_init():
                logging.info('initialize the mixer done...')
            else:
                logging.info('Unable to initialize the mixer')
                pg.mixer.quit()
            # set the font:
            pg.font.init()
            if not pg.font.get_init():
                logging.info('Unable to initialize the font')
                pg.font.quit()
            else:
                logging.info('initialize the font done: default type ->{}'
                             .format(pg.font.get_default_font()))

    def load_complete(
            self,
            instance,
            dataFolder=None,
            persistenceLayer=None,
            fileLevels=None):
        """
        -- load_complete():
        copy an instance of your game engine and use it in the main.py

        1) - load_game(dataFolder, persistenceLayer):
        this function load game resources and get infos from persistence
        layer, this function must call the Resources class to load all the
        data from the data folder.
        optional if you have no data to load. Just keep it empty
        by default on the engine.

        #PARAMS:
        * dataFolder: this folder contains all the resources:(sound,
        images font..etc)

        * persistenceLayer: this file contains the data structure of all
        resources. It will be created automatically after calling the
        class Resources(data_folder).save(persistenceLayer)

        2) - destroy_game(): at the end destroy all resources if necessary
        3) - main_loop(): the main loop of the game(event, update, draw...
        ticks).
        4) - load_levels(): useful if the game contains levels. optional
        if no levels to load. keep it empty on the engine
        """

        # get instance of the game(The Engine() class)
        self.gInstance = instance
        if dataFolder and persistenceLayer:
            self.gInstance.load_game(dataFolder, persistenceLayer)
        if dataFolder and fileLevels:
            self.gInstance.load_levels(dataFolder, fileLevels)

    def destroy(self):
        """
        destroy the environement
        """
        if self.gInstance:
            self.gInstance.destroy_game()
        pg.mixer.quit()
        pg.font.quit()
        pg.quit()
