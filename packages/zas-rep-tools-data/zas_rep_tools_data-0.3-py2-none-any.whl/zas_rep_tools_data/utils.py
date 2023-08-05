#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# : Utilities 
# Author:
# c(Student) ->     {'Egor Savin'}
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import inspect, os

#path_to_zas_rep_tools_data = inspect.getfile(inspect.currentframe()) # script filename (usually with path)
path_to_data_folder = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "data") # script directory

path_to_models = os.path.join(path_to_data_folder, "data/models") # script directory

path_to_someweta_models = os.path.join(path_to_models, "SoMeWeTa")

path_to_stop_words = os.path.join(path_to_data_folder, "stop_words")