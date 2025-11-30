#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.1.4),
    on Thu Dec  2 19:44:01 2021
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

import psychopy
psychopy.useVersion('2021.1.4')


from psychopy import locale_setup
from psychopy import prefs
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '4'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

import pandas as pd
exp_info = pd.read_csv('../exp_info.csv')

participant=exp_info.at[0, 'participant']
session=exp_info.at[0,'session']
mriMode=exp_info.at[0,'mriMode']


offset_x=0
offset_y=0

windowSize=848
colorSize=100
farPos=(windowSize/2)-(colorSize/2)
nearPos=(windowSize/2)-((colorSize/2)*3)
cornerPos=(windowSize/2)-(15)


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.1.4'
expName = 'VIS_CAL_SCAN'  # from the Builder filename that created this script
expInfo = {'': ''}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + '../../data_output/%s/%s/%s_%s_%s' % (participant,session,participant,session, expName)

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/cnlpp2/Desktop/iCere_Control_Pilot2/VIS_CAL/VIS_CAL_SCAN_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1792, 1120], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='scanProjector', color=[-1.000,-1.000,-1.000], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='pix')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "Y_Adjust"
Y_AdjustClock = core.Clock()
adjust_back = visual.Rect(
    win=win, name='adjust_back',
    width=(windowSize, windowSize)[0], height=(windowSize, windowSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor=(0.7647, 0.7647, 0.7647),
    opacity=None, depth=0.0, interpolate=True)
botLeftBlack = visual.Rect(
    win=win, name='botLeftBlack',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='black',
    opacity=None, depth=-1.0, interpolate=True)
botRightBlack = visual.Rect(
    win=win, name='botRightBlack',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='black',
    opacity=None, depth=-2.0, interpolate=True)
topRightBlack = visual.Rect(
    win=win, name='topRightBlack',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='black',
    opacity=None, depth=-3.0, interpolate=True)
topLeftBlack = visual.Rect(
    win=win, name='topLeftBlack',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='black',
    opacity=None, depth=-4.0, interpolate=True)
botLeftYel = visual.Rect(
    win=win, name='botLeftYel',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='yellow',
    opacity=None, depth=-5.0, interpolate=True)
botRightYel = visual.Rect(
    win=win, name='botRightYel',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='yellow',
    opacity=None, depth=-6.0, interpolate=True)
topRightYel = visual.Rect(
    win=win, name='topRightYel',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='yellow',
    opacity=None, depth=-7.0, interpolate=True)
topLeftYel = visual.Rect(
    win=win, name='topLeftYel',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='yellow',
    opacity=None, depth=-8.0, interpolate=True)
botRightMag = visual.Rect(
    win=win, name='botRightMag',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='magenta',
    opacity=None, depth=-9.0, interpolate=True)
botLeftMag = visual.Rect(
    win=win, name='botLeftMag',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='magenta',
    opacity=None, depth=-10.0, interpolate=True)
topRightMag = visual.Rect(
    win=win, name='topRightMag',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='magenta',
    opacity=None, depth=-11.0, interpolate=True)
topLeftMag = visual.Rect(
    win=win, name='topLeftMag',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='magenta',
    opacity=None, depth=-12.0, interpolate=True)
botRightCyan = visual.Rect(
    win=win, name='botRightCyan',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='cyan',
    opacity=None, depth=-13.0, interpolate=True)
botLeftCyan = visual.Rect(
    win=win, name='botLeftCyan',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='cyan',
    opacity=None, depth=-14.0, interpolate=True)
topRightCyan = visual.Rect(
    win=win, name='topRightCyan',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='cyan',
    opacity=None, depth=-15.0, interpolate=True)
topLeftCyan = visual.Rect(
    win=win, name='topLeftCyan',
    width=(colorSize, colorSize)[0], height=(colorSize, colorSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor='cyan',
    opacity=None, depth=-16.0, interpolate=True)
fix_pres = visual.ImageStim(
    win=win,
    name='fix_pres', 
    image='Supporting_Files/Screens/Black_Grey_Crosshair.png', mask=None,
    ori=0.0, pos=[0,0], size=(25,25),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-17.0)
UP = visual.TextStim(win=win, name='UP',
    text='7\n\n6\n\n5\n\n4\n\n3\n\n2\n\n1\n',
    font='Open Sans',
    pos=[0,0], height=30.0, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-18.0);
DOWN = visual.TextStim(win=win, name='DOWN',
    text='\n-1\n\n-2\n\n-3\n\n-4\n\n-5\n\n-6\n\n-7',
    font='Open Sans',
    pos=[0,0], height=30.0, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-19.0);
LEFT = visual.TextStim(win=win, name='LEFT',
    text='A     B     C     D     E     F    G     ',
    font='Open Sans',
    pos=[0,0], height=30.0, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-20.0);
RIGHT = visual.TextStim(win=win, name='RIGHT',
    text='     H     I     J     K     L     M     N',
    font='Open Sans',
    pos=[0,0], height=30.0, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-21.0);
adj_press = keyboard.Keyboard()
expInfo['participant']=participant
expInfo['session']=session
expInfo['mriMode']=mriMode

# Initialize components for Routine "vis_cal_disp"
vis_cal_dispClock = core.Clock()
background_check = visual.Rect(
    win=win, name='background_check',
    width=(windowSize, windowSize)[0], height=(windowSize, windowSize)[1],
    ori=0.0, pos=[0,0],
    lineWidth=1.0,     colorSpace='rgb',  lineColor=None, fillColor=(0.7647, 0.7647, 0.7647),
    opacity=None, depth=0.0, interpolate=True)
middle_fix = visual.ImageStim(
    win=win,
    name='middle_fix', 
    image='Supporting_Files/Screens/Black_Grey_Crosshair.png', mask=None,
    ori=0.0, pos=[0,0], size=(25,25),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-1.0)
top_right_fix = visual.ImageStim(
    win=win,
    name='top_right_fix', 
    image='Supporting_Files/Screens/Black_Grey_Crosshair.png', mask=None,
    ori=0.0, pos=[0,0], size=(25,25),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-2.0)
top_left_fix = visual.ImageStim(
    win=win,
    name='top_left_fix', 
    image='Supporting_Files/Screens/Black_Grey_Crosshair.png', mask=None,
    ori=0.0, pos=[0,0], size=(25,25),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-3.0)
bottom_left_fix = visual.ImageStim(
    win=win,
    name='bottom_left_fix', 
    image='Supporting_Files/Screens/Black_Grey_Crosshair.png', mask=None,
    ori=0.0, pos=[0,0], size=(25,25),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-4.0)
bottom_right_fix = visual.ImageStim(
    win=win,
    name='bottom_right_fix', 
    image='Supporting_Files/Screens/Black_Grey_Crosshair.png', mask=None,
    ori=0.0, pos=[0,0], size=(25,25),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=-5.0)
cal_check_resp = keyboard.Keyboard()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
redo_screencal = data.TrialHandler(nReps=50.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='redo_screencal')
thisExp.addLoop(redo_screencal)  # add the loop to the experiment
thisRedo_screencal = redo_screencal.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisRedo_screencal.rgb)
if thisRedo_screencal != None:
    for paramName in thisRedo_screencal:
        exec('{} = thisRedo_screencal[paramName]'.format(paramName))

for thisRedo_screencal in redo_screencal:
    currentLoop = redo_screencal
    # abbreviate parameter names if possible (e.g. rgb = thisRedo_screencal.rgb)
    if thisRedo_screencal != None:
        for paramName in thisRedo_screencal:
            exec('{} = thisRedo_screencal[paramName]'.format(paramName))
    
    # set up handler to look after randomisation of conditions etc
    vis_cal_loop = data.TrialHandler(nReps=500.0, method='sequential', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='vis_cal_loop')
    thisExp.addLoop(vis_cal_loop)  # add the loop to the experiment
    thisVis_cal_loop = vis_cal_loop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisVis_cal_loop.rgb)
    if thisVis_cal_loop != None:
        for paramName in thisVis_cal_loop:
            exec('{} = thisVis_cal_loop[paramName]'.format(paramName))
    
    for thisVis_cal_loop in vis_cal_loop:
        currentLoop = vis_cal_loop
        # abbreviate parameter names if possible (e.g. rgb = thisVis_cal_loop.rgb)
        if thisVis_cal_loop != None:
            for paramName in thisVis_cal_loop:
                exec('{} = thisVis_cal_loop[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Y_Adjust"-------
        continueRoutine = True
        # update component parameters for each repeat
        fix_pres.setPos((offset_x, offset_y))
        UP.setPos((offset_x, offset_y+(windowSize/4)))
        DOWN.setPos((offset_x, offset_y-(windowSize/4)))
        LEFT.setPos((offset_x-(windowSize/4), offset_y))
        RIGHT.setPos((offset_x+(windowSize/4), offset_y))
        adj_press.keys = []
        adj_press.rt = []
        _adj_press_allKeys = []
        # keep track of which components have finished
        Y_AdjustComponents = [adjust_back, botLeftBlack, botRightBlack, topRightBlack, topLeftBlack, botLeftYel, botRightYel, topRightYel, topLeftYel, botRightMag, botLeftMag, topRightMag, topLeftMag, botRightCyan, botLeftCyan, topRightCyan, topLeftCyan, fix_pres, UP, DOWN, LEFT, RIGHT, adj_press]
        for thisComponent in Y_AdjustComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        Y_AdjustClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Y_Adjust"-------
        while continueRoutine:
            # get current time
            t = Y_AdjustClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=Y_AdjustClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *adjust_back* updates
            if adjust_back.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                adjust_back.frameNStart = frameN  # exact frame index
                adjust_back.tStart = t  # local t and not account for scr refresh
                adjust_back.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(adjust_back, 'tStartRefresh')  # time at next scr refresh
                adjust_back.setAutoDraw(True)
            if adjust_back.status == STARTED:  # only update if drawing
                adjust_back.setPos((offset_x, offset_y))
            
            # *botLeftBlack* updates
            if botLeftBlack.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                botLeftBlack.frameNStart = frameN  # exact frame index
                botLeftBlack.tStart = t  # local t and not account for scr refresh
                botLeftBlack.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(botLeftBlack, 'tStartRefresh')  # time at next scr refresh
                botLeftBlack.setAutoDraw(True)
            if botLeftBlack.status == STARTED:  # only update if drawing
                botLeftBlack.setPos((offset_x-nearPos, offset_y-nearPos))
            
            # *botRightBlack* updates
            if botRightBlack.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                botRightBlack.frameNStart = frameN  # exact frame index
                botRightBlack.tStart = t  # local t and not account for scr refresh
                botRightBlack.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(botRightBlack, 'tStartRefresh')  # time at next scr refresh
                botRightBlack.setAutoDraw(True)
            if botRightBlack.status == STARTED:  # only update if drawing
                botRightBlack.setPos((offset_x+nearPos, offset_y-nearPos))
            
            # *topRightBlack* updates
            if topRightBlack.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                topRightBlack.frameNStart = frameN  # exact frame index
                topRightBlack.tStart = t  # local t and not account for scr refresh
                topRightBlack.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(topRightBlack, 'tStartRefresh')  # time at next scr refresh
                topRightBlack.setAutoDraw(True)
            if topRightBlack.status == STARTED:  # only update if drawing
                topRightBlack.setPos((offset_x+nearPos, offset_y+nearPos))
            
            # *topLeftBlack* updates
            if topLeftBlack.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                topLeftBlack.frameNStart = frameN  # exact frame index
                topLeftBlack.tStart = t  # local t and not account for scr refresh
                topLeftBlack.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(topLeftBlack, 'tStartRefresh')  # time at next scr refresh
                topLeftBlack.setAutoDraw(True)
            if topLeftBlack.status == STARTED:  # only update if drawing
                topLeftBlack.setPos((offset_x-nearPos, offset_y+nearPos))
            
            # *botLeftYel* updates
            if botLeftYel.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                botLeftYel.frameNStart = frameN  # exact frame index
                botLeftYel.tStart = t  # local t and not account for scr refresh
                botLeftYel.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(botLeftYel, 'tStartRefresh')  # time at next scr refresh
                botLeftYel.setAutoDraw(True)
            if botLeftYel.status == STARTED:  # only update if drawing
                botLeftYel.setPos((offset_x-farPos, offset_y-nearPos))
            
            # *botRightYel* updates
            if botRightYel.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                botRightYel.frameNStart = frameN  # exact frame index
                botRightYel.tStart = t  # local t and not account for scr refresh
                botRightYel.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(botRightYel, 'tStartRefresh')  # time at next scr refresh
                botRightYel.setAutoDraw(True)
            if botRightYel.status == STARTED:  # only update if drawing
                botRightYel.setPos((offset_x+farPos, offset_y-nearPos))
            
            # *topRightYel* updates
            if topRightYel.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                topRightYel.frameNStart = frameN  # exact frame index
                topRightYel.tStart = t  # local t and not account for scr refresh
                topRightYel.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(topRightYel, 'tStartRefresh')  # time at next scr refresh
                topRightYel.setAutoDraw(True)
            if topRightYel.status == STARTED:  # only update if drawing
                topRightYel.setPos((offset_x+farPos, offset_y+nearPos))
            
            # *topLeftYel* updates
            if topLeftYel.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                topLeftYel.frameNStart = frameN  # exact frame index
                topLeftYel.tStart = t  # local t and not account for scr refresh
                topLeftYel.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(topLeftYel, 'tStartRefresh')  # time at next scr refresh
                topLeftYel.setAutoDraw(True)
            if topLeftYel.status == STARTED:  # only update if drawing
                topLeftYel.setPos((offset_x-farPos, offset_y+nearPos))
            
            # *botRightMag* updates
            if botRightMag.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                botRightMag.frameNStart = frameN  # exact frame index
                botRightMag.tStart = t  # local t and not account for scr refresh
                botRightMag.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(botRightMag, 'tStartRefresh')  # time at next scr refresh
                botRightMag.setAutoDraw(True)
            if botRightMag.status == STARTED:  # only update if drawing
                botRightMag.setPos((offset_x+nearPos, offset_y-farPos))
            
            # *botLeftMag* updates
            if botLeftMag.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                botLeftMag.frameNStart = frameN  # exact frame index
                botLeftMag.tStart = t  # local t and not account for scr refresh
                botLeftMag.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(botLeftMag, 'tStartRefresh')  # time at next scr refresh
                botLeftMag.setAutoDraw(True)
            if botLeftMag.status == STARTED:  # only update if drawing
                botLeftMag.setPos((offset_x-nearPos, offset_y-farPos))
            
            # *topRightMag* updates
            if topRightMag.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                topRightMag.frameNStart = frameN  # exact frame index
                topRightMag.tStart = t  # local t and not account for scr refresh
                topRightMag.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(topRightMag, 'tStartRefresh')  # time at next scr refresh
                topRightMag.setAutoDraw(True)
            if topRightMag.status == STARTED:  # only update if drawing
                topRightMag.setPos((offset_x+nearPos, offset_y+farPos))
            
            # *topLeftMag* updates
            if topLeftMag.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                topLeftMag.frameNStart = frameN  # exact frame index
                topLeftMag.tStart = t  # local t and not account for scr refresh
                topLeftMag.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(topLeftMag, 'tStartRefresh')  # time at next scr refresh
                topLeftMag.setAutoDraw(True)
            if topLeftMag.status == STARTED:  # only update if drawing
                topLeftMag.setPos((offset_x-nearPos, offset_y+farPos))
            
            # *botRightCyan* updates
            if botRightCyan.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                botRightCyan.frameNStart = frameN  # exact frame index
                botRightCyan.tStart = t  # local t and not account for scr refresh
                botRightCyan.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(botRightCyan, 'tStartRefresh')  # time at next scr refresh
                botRightCyan.setAutoDraw(True)
            if botRightCyan.status == STARTED:  # only update if drawing
                botRightCyan.setPos((offset_x+farPos, offset_y-farPos))
            
            # *botLeftCyan* updates
            if botLeftCyan.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                botLeftCyan.frameNStart = frameN  # exact frame index
                botLeftCyan.tStart = t  # local t and not account for scr refresh
                botLeftCyan.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(botLeftCyan, 'tStartRefresh')  # time at next scr refresh
                botLeftCyan.setAutoDraw(True)
            if botLeftCyan.status == STARTED:  # only update if drawing
                botLeftCyan.setPos((offset_x-farPos, offset_y-farPos))
            
            # *topRightCyan* updates
            if topRightCyan.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                topRightCyan.frameNStart = frameN  # exact frame index
                topRightCyan.tStart = t  # local t and not account for scr refresh
                topRightCyan.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(topRightCyan, 'tStartRefresh')  # time at next scr refresh
                topRightCyan.setAutoDraw(True)
            if topRightCyan.status == STARTED:  # only update if drawing
                topRightCyan.setPos((offset_x+farPos, offset_y+farPos))
            
            # *topLeftCyan* updates
            if topLeftCyan.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                topLeftCyan.frameNStart = frameN  # exact frame index
                topLeftCyan.tStart = t  # local t and not account for scr refresh
                topLeftCyan.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(topLeftCyan, 'tStartRefresh')  # time at next scr refresh
                topLeftCyan.setAutoDraw(True)
            if topLeftCyan.status == STARTED:  # only update if drawing
                topLeftCyan.setPos((offset_x-farPos, offset_y+farPos))
            
            # *fix_pres* updates
            if fix_pres.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fix_pres.frameNStart = frameN  # exact frame index
                fix_pres.tStart = t  # local t and not account for scr refresh
                fix_pres.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix_pres, 'tStartRefresh')  # time at next scr refresh
                fix_pres.setAutoDraw(True)
            
            # *UP* updates
            if UP.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                UP.frameNStart = frameN  # exact frame index
                UP.tStart = t  # local t and not account for scr refresh
                UP.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(UP, 'tStartRefresh')  # time at next scr refresh
                UP.setAutoDraw(True)
            
            # *DOWN* updates
            if DOWN.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                DOWN.frameNStart = frameN  # exact frame index
                DOWN.tStart = t  # local t and not account for scr refresh
                DOWN.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(DOWN, 'tStartRefresh')  # time at next scr refresh
                DOWN.setAutoDraw(True)
            
            # *LEFT* updates
            if LEFT.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                LEFT.frameNStart = frameN  # exact frame index
                LEFT.tStart = t  # local t and not account for scr refresh
                LEFT.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(LEFT, 'tStartRefresh')  # time at next scr refresh
                LEFT.setAutoDraw(True)
            
            # *RIGHT* updates
            if RIGHT.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                RIGHT.frameNStart = frameN  # exact frame index
                RIGHT.tStart = t  # local t and not account for scr refresh
                RIGHT.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(RIGHT, 'tStartRefresh')  # time at next scr refresh
                RIGHT.setAutoDraw(True)
            
            # *adj_press* updates
            waitOnFlip = False
            if adj_press.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                adj_press.frameNStart = frameN  # exact frame index
                adj_press.tStart = t  # local t and not account for scr refresh
                adj_press.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(adj_press, 'tStartRefresh')  # time at next scr refresh
                adj_press.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(adj_press.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(adj_press.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if adj_press.status == STARTED and not waitOnFlip:
                theseKeys = adj_press.getKeys(keyList=['up', 'down', 'left', 'right', 'space', 'r'], waitRelease=False)
                _adj_press_allKeys.extend(theseKeys)
                if len(_adj_press_allKeys):
                    adj_press.keys = _adj_press_allKeys[-1].name  # just the last key pressed
                    adj_press.rt = _adj_press_allKeys[-1].rt
            if adj_press.keys == 'up':
                if offset_y < 80:
                    offset_y=offset_y+20
                continueRoutine = False
            elif adj_press.keys == 'down':
                if offset_y > -80:
                    offset_y=offset_y-20
                continueRoutine = False
            elif adj_press.keys == 'left':
                if offset_x > -100:
                    offset_x=offset_x-20
                continueRoutine = False
            elif adj_press.keys == 'right':
                if offset_x < 100:
                    offset_x=offset_x+20
                continueRoutine = False
            #elif adj_press.keys == 'r':
            #    offset_x=0
            #    offset_y=0
            #    continueRoutine = False
            elif adj_press.keys == 'space':
                vis_cal_loop.finished = True
                continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Y_AdjustComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Y_Adjust"-------
        for thisComponent in Y_AdjustComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        vis_cal_loop.addData('adjust_back.started', adjust_back.tStartRefresh)
        vis_cal_loop.addData('adjust_back.stopped', adjust_back.tStopRefresh)
        vis_cal_loop.addData('botLeftBlack.started', botLeftBlack.tStartRefresh)
        vis_cal_loop.addData('botLeftBlack.stopped', botLeftBlack.tStopRefresh)
        vis_cal_loop.addData('botRightBlack.started', botRightBlack.tStartRefresh)
        vis_cal_loop.addData('botRightBlack.stopped', botRightBlack.tStopRefresh)
        vis_cal_loop.addData('topRightBlack.started', topRightBlack.tStartRefresh)
        vis_cal_loop.addData('topRightBlack.stopped', topRightBlack.tStopRefresh)
        vis_cal_loop.addData('topLeftBlack.started', topLeftBlack.tStartRefresh)
        vis_cal_loop.addData('topLeftBlack.stopped', topLeftBlack.tStopRefresh)
        vis_cal_loop.addData('botLeftYel.started', botLeftYel.tStartRefresh)
        vis_cal_loop.addData('botLeftYel.stopped', botLeftYel.tStopRefresh)
        vis_cal_loop.addData('botRightYel.started', botRightYel.tStartRefresh)
        vis_cal_loop.addData('botRightYel.stopped', botRightYel.tStopRefresh)
        vis_cal_loop.addData('topRightYel.started', topRightYel.tStartRefresh)
        vis_cal_loop.addData('topRightYel.stopped', topRightYel.tStopRefresh)
        vis_cal_loop.addData('topLeftYel.started', topLeftYel.tStartRefresh)
        vis_cal_loop.addData('topLeftYel.stopped', topLeftYel.tStopRefresh)
        vis_cal_loop.addData('botRightMag.started', botRightMag.tStartRefresh)
        vis_cal_loop.addData('botRightMag.stopped', botRightMag.tStopRefresh)
        vis_cal_loop.addData('botLeftMag.started', botLeftMag.tStartRefresh)
        vis_cal_loop.addData('botLeftMag.stopped', botLeftMag.tStopRefresh)
        vis_cal_loop.addData('topRightMag.started', topRightMag.tStartRefresh)
        vis_cal_loop.addData('topRightMag.stopped', topRightMag.tStopRefresh)
        vis_cal_loop.addData('topLeftMag.started', topLeftMag.tStartRefresh)
        vis_cal_loop.addData('topLeftMag.stopped', topLeftMag.tStopRefresh)
        vis_cal_loop.addData('botRightCyan.started', botRightCyan.tStartRefresh)
        vis_cal_loop.addData('botRightCyan.stopped', botRightCyan.tStopRefresh)
        vis_cal_loop.addData('botLeftCyan.started', botLeftCyan.tStartRefresh)
        vis_cal_loop.addData('botLeftCyan.stopped', botLeftCyan.tStopRefresh)
        vis_cal_loop.addData('topRightCyan.started', topRightCyan.tStartRefresh)
        vis_cal_loop.addData('topRightCyan.stopped', topRightCyan.tStopRefresh)
        vis_cal_loop.addData('topLeftCyan.started', topLeftCyan.tStartRefresh)
        vis_cal_loop.addData('topLeftCyan.stopped', topLeftCyan.tStopRefresh)
        vis_cal_loop.addData('fix_pres.started', fix_pres.tStartRefresh)
        vis_cal_loop.addData('fix_pres.stopped', fix_pres.tStopRefresh)
        vis_cal_loop.addData('UP.started', UP.tStartRefresh)
        vis_cal_loop.addData('UP.stopped', UP.tStopRefresh)
        vis_cal_loop.addData('DOWN.started', DOWN.tStartRefresh)
        vis_cal_loop.addData('DOWN.stopped', DOWN.tStopRefresh)
        vis_cal_loop.addData('LEFT.started', LEFT.tStartRefresh)
        vis_cal_loop.addData('LEFT.stopped', LEFT.tStopRefresh)
        vis_cal_loop.addData('RIGHT.started', RIGHT.tStartRefresh)
        vis_cal_loop.addData('RIGHT.stopped', RIGHT.tStopRefresh)
        # check responses
        if adj_press.keys in ['', [], None]:  # No response was made
            adj_press.keys = None
        vis_cal_loop.addData('adj_press.keys',adj_press.keys)
        if adj_press.keys != None:  # we had a response
            vis_cal_loop.addData('adj_press.rt', adj_press.rt)
        vis_cal_loop.addData('adj_press.started', adj_press.tStartRefresh)
        vis_cal_loop.addData('adj_press.stopped', adj_press.tStopRefresh)
        # the Routine "Y_Adjust" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 500.0 repeats of 'vis_cal_loop'
    
    
    # ------Prepare to start Routine "vis_cal_disp"-------
    continueRoutine = True
    # update component parameters for each repeat
    middle_fix.setPos((offset_x, offset_y))
    top_right_fix.setPos((offset_x+cornerPos, offset_y+cornerPos))
    top_left_fix.setPos((offset_x-cornerPos, offset_y+cornerPos))
    bottom_left_fix.setPos((offset_x-cornerPos, offset_y-cornerPos))
    bottom_right_fix.setPos((offset_x+cornerPos, offset_y-cornerPos))
    cal_check_resp.keys = []
    cal_check_resp.rt = []
    _cal_check_resp_allKeys = []
    print("SPACE to continue, R to reset")
    # keep track of which components have finished
    vis_cal_dispComponents = [background_check, middle_fix, top_right_fix, top_left_fix, bottom_left_fix, bottom_right_fix, cal_check_resp]
    for thisComponent in vis_cal_dispComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    vis_cal_dispClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "vis_cal_disp"-------
    while continueRoutine:
        # get current time
        t = vis_cal_dispClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=vis_cal_dispClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *background_check* updates
        if background_check.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            background_check.frameNStart = frameN  # exact frame index
            background_check.tStart = t  # local t and not account for scr refresh
            background_check.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(background_check, 'tStartRefresh')  # time at next scr refresh
            background_check.setAutoDraw(True)
        if background_check.status == STARTED:  # only update if drawing
            background_check.setPos((offset_x, offset_y))
        
        # *middle_fix* updates
        if middle_fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            middle_fix.frameNStart = frameN  # exact frame index
            middle_fix.tStart = t  # local t and not account for scr refresh
            middle_fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(middle_fix, 'tStartRefresh')  # time at next scr refresh
            middle_fix.setAutoDraw(True)
        
        # *top_right_fix* updates
        if top_right_fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            top_right_fix.frameNStart = frameN  # exact frame index
            top_right_fix.tStart = t  # local t and not account for scr refresh
            top_right_fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(top_right_fix, 'tStartRefresh')  # time at next scr refresh
            top_right_fix.setAutoDraw(True)
        
        # *top_left_fix* updates
        if top_left_fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            top_left_fix.frameNStart = frameN  # exact frame index
            top_left_fix.tStart = t  # local t and not account for scr refresh
            top_left_fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(top_left_fix, 'tStartRefresh')  # time at next scr refresh
            top_left_fix.setAutoDraw(True)
        
        # *bottom_left_fix* updates
        if bottom_left_fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            bottom_left_fix.frameNStart = frameN  # exact frame index
            bottom_left_fix.tStart = t  # local t and not account for scr refresh
            bottom_left_fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(bottom_left_fix, 'tStartRefresh')  # time at next scr refresh
            bottom_left_fix.setAutoDraw(True)
        
        # *bottom_right_fix* updates
        if bottom_right_fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            bottom_right_fix.frameNStart = frameN  # exact frame index
            bottom_right_fix.tStart = t  # local t and not account for scr refresh
            bottom_right_fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(bottom_right_fix, 'tStartRefresh')  # time at next scr refresh
            bottom_right_fix.setAutoDraw(True)
        
        # *cal_check_resp* updates
        waitOnFlip = False
        if cal_check_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            cal_check_resp.frameNStart = frameN  # exact frame index
            cal_check_resp.tStart = t  # local t and not account for scr refresh
            cal_check_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(cal_check_resp, 'tStartRefresh')  # time at next scr refresh
            cal_check_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(cal_check_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(cal_check_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if cal_check_resp.status == STARTED and not waitOnFlip:
            theseKeys = cal_check_resp.getKeys(keyList=['space', 'r'], waitRelease=False)
            _cal_check_resp_allKeys.extend(theseKeys)
            if len(_cal_check_resp_allKeys):
                cal_check_resp.keys = _cal_check_resp_allKeys[-1].name  # just the last key pressed
                cal_check_resp.rt = _cal_check_resp_allKeys[-1].rt
        if cal_check_resp.keys == 'r':
            continueRoutine = False
        if cal_check_resp.keys == 'space':
            redo_screencal.finished = True
            continueRoutine = False
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in vis_cal_dispComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "vis_cal_disp"-------
    for thisComponent in vis_cal_dispComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    redo_screencal.addData('background_check.started', background_check.tStartRefresh)
    redo_screencal.addData('background_check.stopped', background_check.tStopRefresh)
    redo_screencal.addData('middle_fix.started', middle_fix.tStartRefresh)
    redo_screencal.addData('middle_fix.stopped', middle_fix.tStopRefresh)
    redo_screencal.addData('top_right_fix.started', top_right_fix.tStartRefresh)
    redo_screencal.addData('top_right_fix.stopped', top_right_fix.tStopRefresh)
    redo_screencal.addData('top_left_fix.started', top_left_fix.tStartRefresh)
    redo_screencal.addData('top_left_fix.stopped', top_left_fix.tStopRefresh)
    redo_screencal.addData('bottom_left_fix.started', bottom_left_fix.tStartRefresh)
    redo_screencal.addData('bottom_left_fix.stopped', bottom_left_fix.tStopRefresh)
    redo_screencal.addData('bottom_right_fix.started', bottom_right_fix.tStartRefresh)
    redo_screencal.addData('bottom_right_fix.stopped', bottom_right_fix.tStopRefresh)
    # check responses
    if cal_check_resp.keys in ['', [], None]:  # No response was made
        cal_check_resp.keys = None
    redo_screencal.addData('cal_check_resp.keys',cal_check_resp.keys)
    if cal_check_resp.keys != None:  # we had a response
        redo_screencal.addData('cal_check_resp.rt', cal_check_resp.rt)
    redo_screencal.addData('cal_check_resp.started', cal_check_resp.tStartRefresh)
    redo_screencal.addData('cal_check_resp.stopped', cal_check_resp.tStopRefresh)
    # the Routine "vis_cal_disp" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 50.0 repeats of 'redo_screencal'

exp_info.at[0, 'offset_x'] =  offset_x
exp_info.at[0, 'offset_y'] =  offset_y
exp_info.to_csv('../exp_info.csv', index=False)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
