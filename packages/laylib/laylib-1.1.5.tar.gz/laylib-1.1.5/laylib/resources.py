""" laylib-pygame summary:

            This class regroups all functions to load & save resources, sound,
            images, fonts..etc and some util-functions to print text in
            the screen & stuffs like that.
TODO:
            - manage the image.set_colorkey((255, 255, 255)) for transparency
            - add description of how to parse data and create persistence layer
            - add setter method for constants:
                                                DEFAULT_FX_VOLUME
                                                DEFAULT_MUSIC_VOLUME
                                                DEFAULT_FONT_SIZE
Date:       17/07/2017
Author:     Amardjia Amine.
"""

import pygame as pg
import os
import pprint
import pickle
import json
import logging

SOUND_TITLE = 0
SOUND_VOLUME = 1
FONT_NAME = 0
FONT_SIZE = 1
# parser slipted to name, split_arg[_EXT]
_NAME = 0
_EXT = 1

logging.basicConfig(level=logging.ERROR,
                    format='%(levelname)s: %(message)s')

"""
Use these values to parametrize:

- The fx volume sound
- The music volume
- The font size
"""

DEFAULT_FX_VOLUME = 0.8
DEFAULT_MUSIC_VOLUME = 1.0
DEFAULT_FONT_SIZE = 20


class Resources(object):
    """ Resources manager:
    Load or save (creat resources.res file) all resources files,
    with json parsing method or pickle
    """

    def __init__(self, data_folder=''):
        self.data_folder = data_folder
        self.global_data = None
        # pm: if we want use pickle instead of json module
        self.pm = PersistenceManager(data_folder)
        self.img = Image(data_folder)
        self.snd = Sound(data_folder)
        self.msc = Music(data_folder)
        self.fnt = Font(data_folder)

    """---------------------------------------------------------
    Method 1: Parsing data with json from the persistence layer:
    ---------------------------------------------------------"""

    def jsave_info(self, data, fileName, indent=True):
        if not indent:
            inf = json.dumps(data)
        else:
            inf = json.dumps(data, indent=4, sort_keys=True)
        fileName = os.path.join(self.data_folder, fileName)
        with open(fileName, "w") as fp:
            fp.write(inf)

    def jget_info(self, fileName):
        fileName = os.path.join(self.data_folder, fileName)
        with open(fileName, "r") as fp:
            str = fp.read()
        return json.loads(str)

    """---------------------------------------------------------
    Method 2: parsing with pickle:
    ---------------------------------------------------------"""

    def save(self, fileName):
        """
        to automate the creation of persistence file of resources
        call this method.
        """
        fileName = os.path.join(self.data_folder, fileName)
        self.pm._resources_save(fileName)

    def get(self, fileName):
        fileName = os.path.join(self.data_folder, fileName)
        return self.pm._resources_get(fileName)

    def show(self):
        """
        show all the data loaded with their index
        show the content of parser, this function is useful
        when you want to know the index of each resource.
        """
        self.pm._show()


class PersistenceManager(object):
    """
    Persistence Manager: automate the creation of a persistence layer for data
    - save and parse.
    - load the persitence layer and return the data structure
    - The file is created into a binary format using pickle module.
    """
    _PARSER_VERSION = '0.2.2'
    # class constants:
    IMAGE_TYPE = ['bmp', 'jpg', 'png', 'jpeg', 'tif', 'pgm'
                  'gif', 'pcx', 'tga', 'lbm', 'pbm', 'xpm']
    IMAGE_TYPE += [x.upper() for x in IMAGE_TYPE]
    MUSIC_TYPE = ['mp3', 'wma', 'ogg']
    MUSIC_TYPE += [x.upper() for x in MUSIC_TYPE]
    FX_TYPE = ['wav', 'midi']
    FX_TYPE += [x.upper() for x in FX_TYPE]
    FONT_TYPE = ['ttf', 'otf', 'ttc']
    FONT_TYPE += [x.upper() for x in FONT_TYPE]

    def __init__(self, folder='data'):
        self.parser = {
            'version': '',
            'imgList': [],
            'sndList': [],
            'mscList': [],
            'fntList': [],
            'other': [],
            'unknown': []
        }
        self.pp = pprint.PrettyPrinter(indent=4)
        self.files_list = os.listdir(folder)

    def _show(self):
        """
        show the content of parser, this function is useful
        when you want to know the index of each resource.
        callable from Ressource class.
        """
        self.pp.pprint(self.parser)

    def _create_parserGroup(self):
        """
        sort the group list
        """
        self.parser["version"] = str(self._PARSER_VERSION)

        for file in self.files_list:
            split_arg = file.split('.')
            # check if the file got '.ext' or not (parser version 0.2.2)
            if len(split_arg) < 2:
                self.parser["unknown"].append(file)
            else:
                if split_arg[_EXT] in self.IMAGE_TYPE:
                    self.parser["imgList"].append(file)
                elif split_arg[_EXT] in self.MUSIC_TYPE:
                    conf_file = [file, DEFAULT_MUSIC_VOLUME]
                    self.parser["mscList"].append(conf_file)
                elif split_arg[_EXT] in self.FX_TYPE:
                    conf_file = [file, DEFAULT_FX_VOLUME]
                    self.parser["sndList"].append(conf_file)
                elif split_arg[_EXT] in self.FONT_TYPE:
                    conf_file = [file, DEFAULT_FONT_SIZE]
                    self.parser["fntList"].append(conf_file)
                else:
                    self.parser["other"].append(file)

    def _resources_get(self, persistence_file):
        """ load binary """
        with open(persistence_file, 'rb') as fp:
            data = pickle.load(fp)
            self.parser = data
        return data

    def _resources_save(self, persistence_file):
        """ automate saving binary """
        self._create_parserGroup()
        with open(persistence_file, 'wb') as fp:
            pickle.dump(self.parser, fp, pickle.HIGHEST_PROTOCOL)


class Image(object):
    """
    Images resources manager
    """

    def __init__(self, data_folder):
        self.data_folder = data_folder

    def load_image(self, name, alpha, scale=1.0):
        """ load an image file and enable the transparency key"""
        name = os.path.join(self.data_folder, name)
        try:
            image = pg.image.load(name)
            if alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
        except pg.error:
            logging.error('Could not load image {}'.format(name))
            raise SystemExit(pg.get_error())
        rect = image.get_rect()
        if scale < 1.0:
            image = pg.transform.scale(
                image, (int(rect.w * scale), int(rect.h * scale)))
        return image

    def loadGroup(self, imgList, alpha, scale=1.0):
        """ Load and return a list of images"""
        image = []
        for name in imgList:
            image.append(self.load_image(name, alpha, scale))
        return image


class Sound(object):
    """
    class for Fx sounds effect
    """

    def __init__(self, data_folder):
        self.data_folder = data_folder

    def load_sound(self, name, volume=1.0):
        """load the sound fx and set it to a specific volume"""
        name = os.path.join(self.data_folder, name)
        try:
            sound = pg.mixer.Sound(name)
        except pg.error:
            logging.error('unable to load {}'.format(name))
        sound.set_volume(volume)
        return sound

    def loadGroup(self, soundList):
        """ load all the fx """
        sounds = []
        for snd in soundList:
            sounds.append(self.load_sound(snd[SOUND_TITLE], snd[SOUND_VOLUME]))
        return sounds

    def play_fx(self, channel, sound_fx):
        """ play on a specific channel fx """
        if not pg.mixer.Channel(channel).get_busy():
            pg.mixer.Channel(channel).play(sound_fx)

    def fade_out_fx(channel, time):
        """ fade out sound in time """
        pass

    def stop_fx(self, sound_fx):
        pass


class Music(object):
    """
    for mixer music mp3: return the titles as list of string
    """

    def __init__(self, data_folder):
        self.data_folder = data_folder

    def get_playList(self, musicList):
        """ return the play list titles """
        playlist = []
        for title in musicList:
            playlist.append(os.path.join(self.data_folder, title[SOUND_TITLE]))
        # queue
        if playlist:
            first_music = playlist[0]
            pg.mixer.music.load(first_music)
        for track in playlist:
            if track != first_music:
                pg.mixer.music.queue(track)
        return playlist

    def play(self, loops=0, start=0.0):
        pg.mixer.music.play()


class Font(object):
    """
    font manager and some functions for printing text
    """

    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.screen = pg.display.get_surface()

    def load_font(self, name, size):
        """ get the font from file data """
        name = os.path.join(self.data_folder, name)
        try:
            font = pg.font.Font(name, size)
        except pg.error:
            logging.error('unable to load {}'.format(name))
        return font

    def loadGroup(self, fntList):
        """get all the fonts """
        fonts = []
        for fnt in fntList:
            fonts.append(self.load_font(fnt[FONT_NAME], fnt[FONT_SIZE]))
        return fonts

    def render(self, font, message, vect, color=(255, 255, 255)):
        """
        functions to print text in the screen with white by default.
        """
        self.screen.blit(font.render(message, True, color), vect)
