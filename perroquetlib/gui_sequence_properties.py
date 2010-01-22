# -*- coding: utf-8 -*-

# Copyright (C) 2009-2010 Frédéric Bertolus.
#
# This file is part of Perroquet.
#
# Perroquet is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Perroquet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Perroquet.  If not, see <http://www.gnu.org/licenses/>.


import gtk, time, urllib, re, os, gettext
import locale
from perroquetlib.config import Config
_ = gettext.gettext

class GuiSequenceProperties:
    def __init__(self, config, core, parent):

        self.core = core
        self.config = config
        self.parent = parent

        print self.parent

        self.builder = gtk.Builder()
        self.builder.set_translation_domain("perroquet")
        self.builder.add_from_file(self.config.Get("ui_sequence_properties_path"))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object("dialogExerciceProperties")

        self.pagePaths = self.builder.get_object("pagePaths")
        self.pageSequences = self.builder.get_object("pageSequences")

        self.dialog.set_modal(True)
        self.dialog.set_transient_for(self.parent)



    def Run(self):
        self.Load()
        self.dialog.run()
        self.dialog.destroy()
    def Load(self):
        (videoPath,exercicePath,translationPath)  = self.core.GetPaths()

        if videoPath == "":
            videoPath = "None"

        if exercicePath == "":
            exercicePath = "None"

        if translationPath == "":
            translationPath = "None"



        videoChooser = self.builder.get_object("filechooserbuttonVideoProp")
        exerciceChooser = self.builder.get_object("filechooserbuttonExerciceProp")
        translationChooser = self.builder.get_object("filechooserbuttonTranslationProp")
        videoChooser.set_filename(videoPath)
        exerciceChooser.set_filename(exercicePath)
        translationChooser.set_filename(translationPath)


    def on_buttonExercicePropOk_clicked(self,widget,data=None):
        dialogExerciceProperties = self.builder.get_object("dialogExerciceProperties")

        videoChooser = self.builder.get_object("filechooserbuttonVideoProp")
        videoPath = videoChooser.get_filename()
        exerciceChooser = self.builder.get_object("filechooserbuttonExerciceProp")
        exercicePath = exerciceChooser.get_filename()
        translationChooser = self.builder.get_object("filechooserbuttonTranslationProp")
        translationPath = translationChooser.get_filename()
        if videoPath == "None" or videoPath == None:
            videoPath = ""
        if exercicePath == "None" or exercicePath == None:
            exercicePath = ""
        if translationPath == "None" or translationPath == None:
            translationPath = ""

        self.core.UpdatePaths(videoPath,exercicePath, translationPath)
        #dialogExerciceProperties.hide()
        self.dialog.response(gtk.RESPONSE_OK)

    def on_buttonExercicePropCancel_clicked(self,widget,data=None):
        print "Cancel"
        #dialogExerciceProperties = self.builder.get_object("dialogExerciceProperties")
        #dialogExerciceProperties.hide()
        self.dialog.response(gtk.RESPONSE_CANCEL)