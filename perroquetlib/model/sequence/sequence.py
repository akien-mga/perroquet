# -*- coding: utf-8 -*-

# Copyright (C) 2009-2011 Frédéric Bertolus.
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Perroquet. If not, see <http://www.gnu.org/licenses/>.

"""A module that deal with words.
Usage: from sequence import Sequence"""

import re

from word import Word

class Sequence:
    """A class that implement a sequence manipulation with a reference"""
    def __init__(self, language):
        # self._symbolList = what is between words (or "")
        # self._wordList = a list of Words items that we want to find
        # self._workValidityList = 1 if the word if good, 0 if it is empty
        #        -levenshtein between it and the normal word otherwise
        #
        # self._activeWordIndex = the word that is currently being edited
        # self.get_active_word().get_pos() = the position in that word
        #
        # self._helpChar = the char printed when you want a hint
        #
        # Note: self._symbolList, self._wordList
        #  have always the same length

        self._symbolList = []
        self._wordList = []

        self._activeWordIndex = 0

        self._helpChar = '~'

        self.language = language
        allChar = self.language.availableChars
        self.validChar = "[" + allChar + "]"
        self.notValidChar = "[^" + allChar + "]"
        self.repeat_count = 0

        self.beginTime = 0
        self.endTime = 0

    def load(self, text):
        textToParse = text
        
        ignoreRule = '^(([(\[][^)\]]*[)\]])|([A-Z]+:)).*'
        
        self._symbolList.append('')
        while len(textToParse) > 0:
            
            
            # search ignored block
            if re.match(ignoreRule, textToParse):
                m = re.search(ignoreRule, textToParse)
                ignore = m.group(1)
                sizeToCut = len(ignore)
                textToParse = textToParse[sizeToCut:]
                self._symbolList[-1] = self._symbolList[-1] + ignore
                 
            # if the text begin with a word followed by a not word char
            elif re.match('^(' + self.validChar + '+)' + self.notValidChar,
                        textToParse):
                m = re.search('^(' + self.validChar + '+)' + self.notValidChar,
                              textToParse)
                word = m.group(1)
                sizeToCut = len(word)
                textToParse = textToParse[sizeToCut:]
                self._wordList.append(Word(word, self.language))
                self._symbolList.append('')
            # if the text begin with no word char
            elif re.match('^(' + self.notValidChar + ')',
                          textToParse):
                m = re.search('^(' + self.notValidChar + ')',
                              textToParse)
                symbol = m.group(1)
                sizeToCut = len(symbol)
                textToParse = textToParse[sizeToCut:]
                self._symbolList[-1] = self._symbolList[-1] + symbol

            # if there is only one word or one separator
            else:
                # if there is only one word
                if re.match('^(' + self.validChar + '+)', textToParse):
                    self._wordList.append(Word(textToParse, self.language))
                # if there is only one separator
                else:
                    self._symbolList.append(textToParse)
                break

    def get_symbols(self):
        return self._symbolList

    def get_words(self):
        return self._wordList

    def get_word_count(self):
        return len(self._wordList)

    def get_active_word_index(self):
        return self._activeWordIndex

    def set_active_word_index(self, index):
        if index == -1:
            index = self.get_word_count()

        if index < 0 or index > self.get_word_count():
            raise AttributeError, str(index)

        self._activeWordIndex = index

    def get_last_index(self):
        return len(self._wordList) - 1

    def get_active_word(self):
        return self.get_words()[self.get_active_word_index()]

    def get_word_found(self):
        return len([w for w in self.get_words() if w.is_valid()])

    def next_word(self, loop=False):
        "go to the next non valid word "

    def previous_word(self, loop=False):
        "go to the previous non valid word"
        
    def select_sequence_word(self, wordIndex, wordIndexPos):
        """Go to the first editable position after the position of wordIndex
        word and wordIndexPos character"""
        raise NotImplementedError

    def write_char(self, char):
        raise NotImplementedError

    def _write_sentence(self, sentence):
        """write many chars. a ' ' mean next word.
        Only for tests"""
        raise NotImplementedError

    def delete_next_char(self):
        """delete the next deletable character"""
        raise NotImplementedError

    def delete_previous_char(self):
        """delete the previous deletable character"""
        raise NotImplementedError

    def first_word(self):
        """goto first editable character"""
        raise NotImplementedError

    def last_word(self):
        """goto last editable character"""
        raise NotImplementedError

    def next_char(self):
        """goto next editable character"""
        raise NotImplementedError

    def previous_char(self):
        """goto to previous editable character"""
        raise NotImplementedError

    def is_valid(self):
        """Return True if the entire sequence is valid, else return False"""
        raise NotImplementedError

    def is_empty(self):
        return all(w.is_empty() for w in self.get_words())

    def complete_all(self):
        """Reveal all words"""
        for w in self.get_words():
            w.complete()

    def complete_word(self):
         self.get_active_word().complete()

    def reset(self):
        "RAZ the current seq"
        for w in self.get_words():
            w.reset()

    def update_after_write(self):
        "update after a modification of the text"
        pass

    def get_time_begin(self):
        return self.beginTime

    def get_time_end(self):
        return self.endTime

    def set_time_begin(self, time):
        self.beginTime = time

    def set_time_end(self, time):
        self.endTime = time

    # Reveal a letter on the first invalid word after the cursor.
    # Warning: recusive method
    def show_hint(self):
        if not self.get_active_word().is_valid():
            # Reveal a letter on the current word
            self.get_active_word().show_hint()
            if self.get_active_word().is_valid():
                    self.next_word()

        else:
            # The current word is complete try the next word
            if self.get_active_word_index() == self.get_word_count()-1:
                # The current word is the last word, so do nothing
                return
            else:
                # There is a next word, try the hint on the next word
                self.next_word()
                self.show_hint()

    def set_repeat_count(self, repeat_count):
        self.repeat_count = repeat_count

    def get_repeat_count(self):
        return self.repeat_count
        
    def update_cursor_position(self):
        if not self.is_valid():
            if self.get_active_word().is_valid():
                # if the sequence is invalide and the current word valid,
                # go to the end of the word.
                # Usefull with alias, when 2 is replace with two, the cursor is 
                # at the position 1 so is displayed after the t
                self.get_active_word().end()                

    def __print__(self):
        return "-".join(w.get_text() for w in self.get_words()) + " VS " + \
                "-".join(w.get_valid() for w in self.get_words())

    def __repr__(self):
        return self.__print__()
