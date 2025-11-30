#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.5),
    on Mon Oct  7 21:25:07 2024
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# Run 'Before Experiment' code from variables
import pandas as pd
exp_info = pd.read_csv('../exp_info.csv')

participant=str(exp_info.at[0, 'participant'])
session=str(exp_info.at[0,'session'])
mriMode=str(exp_info.at[0,'mriMode'])
offset_x=exp_info.at[0,'offset_x']
offset_y=exp_info.at[0,'offset_y']
run=str(exp_info.at[0,'EPROJ_run'])

print('Participant: ' + participant)
print('Session: ' + session)
print('Run Number: ' + run)
print('Offset_X: ' + str(offset_x))
print('Offset_Y: ' + str(offset_y))
print('MRI Mode: ' + mriMode)

LeftIndex='9'
LeftMiddle='8'
LeftRing='7'

#RightIndex='2'
#LeftIndex='7'
usable_keys=['1','2','3']
# trigger='equal'

# Shared Variables
box_w=848
box_h=848

fix_w=25
fix_h=25

stay_still_h=40
stay_still_y=60

# EPROJ
letter_h=38
stimulus_duration=10
pos_x=15
pos_y=0
pos_wrap=695


timePrecise=core.Clock()
# Run 'Before Experiment' code from SyncGenerator_CC
import threading

class SyncGenerator(threading.Thread):

    def __init__(self, TR=1.0, TA=1.0, volumes=617, sync='equal', skip=0,
                 sound=False, **kwargs):
        """Class for a character-emitting metronome thread
        (emulate MR sync pulse).

        Aim: Allow testing of temporal robustness of fMRI scripts by emulating
        a hardware sync pulse. Adds an arbitrary 'sync' character to the key
        buffer, with sub-millisecond precision (less precise if CPU is maxed).
        Recommend: TR=1.000 or higher and less than 100% CPU. Shorter TR
        --> higher CPU load.

        Parameters:
            TR:      seconds between volume acquisitions
            TA:      seconds to acquire one volume
            volumes: number of 3D volumes to obtain in a given scanning run
            sync:    character used as flag for sync timing, default='5'
            skip:    how many frames to silently omit initially during T1
                     stabilization, no sync pulse. Not needed to test script
                     timing, but will give more accurate feel to start of run.
                     aka "discdacqs".
            sound:   simulate scanner noise
        """
        if TR < 0.1:
            msg = 'SyncGenerator:  whole-brain TR < 0.1 not supported'
            raise ValueError(msg)
        self.TR = TR
        self.TA = TA
        self.hogCPU = 0.035
        self.timesleep = self.TR
        self.volumes = int(volumes)
        self.sync = sync
        self.skip = skip
        self.playSound = sound
        if self.playSound:  # pragma: no cover
            self.sound1 = Sound(800, secs=self.TA, volume=0.15, autoLog=False)
            self.sound2 = Sound(813, secs=self.TA, volume=0.15, autoLog=False)

        self.clock = core.Clock()
        self.stopflag = False
        threading.Thread.__init__(self, None, 'SyncGenerator', None)
        self.running = False

    def run(self):
        self.running = True
        if self.skip:
            for i in range(int(self.skip)):
                if self.playSound:  # pragma: no cover
                    self.sound1.play()
                    self.sound2.play()
                # emulate T1 stabilization without data collection
                core.wait(self.TR, hogCPUperiod=0)
        self.clock.reset()
        for vol in range(1, self.volumes + 1):
            if self.playSound:  # pragma: no cover
                self.sound1.play()
                self.sound2.play()
            if self.stopflag:
                break
            # "emit" a sync pulse by placing a key in the buffer:
            event._onPygletKey(symbol=self.sync, modifiers=0,
                               emulated=True)
            # wait for start of next volume, doing our own hogCPU for
            # tighter sync:
            core.wait(self.timesleep - self.hogCPU, hogCPUperiod=0)
            while self.clock.getTime() < vol * self.TR:
                pass  # hogs the CPU for tighter sync
        self.running = False
        return self


    def stop(self):
        self.stopflag = True


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.5'
expName = 'EPROJ'  # from the Builder filename that created this script
expInfo = {
    'participant': '',
    'session': '',
    'run_num': '',
    'mriMode': 'scan',
}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + '../../data_output/%s/%s/%s_%s_%s' % (participant,session,participant,session, expName + run)

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/luria/EXPT/EXPT_EPROJ_self/EPROJ/EPROJ_lastrun.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1792, 1120], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='scanProjector', color=(-1.0000, -1.0000, -1.0000), colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='pix')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "Variable_Setting_Eproj" ---
# Run 'Begin Experiment' code from variables
import os

# Filename=os.path.join('itis','csv',expInfo['participant'],expInfo['session'] + '.csv')
# print 'Loading from ', Filename


import time
expInfo['expStartWallTime'] = time.ctime()

expInfo['participant']=participant
expInfo['session']=session
expInfo['run_num']=run
expInfo['mriMode']=mriMode

# --- Initialize components for Routine "Eproj_Instructions" ---
Eproj_Instruction_Screen = visual.ImageStim(
    win=win,
    name='Eproj_Instruction_Screen', 
    image='Supporting_Files/Screens/EPROJ.png', mask=None, anchor='center',
    ori=0, pos=[0,0], size=(848,848),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=0.0)
E_key_resp_42 = keyboard.Keyboard()

# --- Initialize components for Routine "Eproj_ReadyScreen" ---
polygon_fix = visual.Rect(
    win=win, name='polygon_fix',
    width=(box_w,box_h)[0], height=(box_w,box_h)[1],
    ori=0.0, pos=(offset_x, offset_y), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=(0.7647, 0.7647, 0.7647), fillColor=(0.7647, 0.7647, 0.7647),
    opacity=None, depth=0.0, interpolate=True)
Ready_E = visual.ImageStim(
    win=win,
    name='Ready_E', 
    image='Supporting_Files/Images/Black_Grey_Crosshair.png', mask=None, anchor='center',
    ori=0, pos=(offset_x+0, offset_y+0), size=(fix_w, fix_h),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=True, depth=-1.0)
stay_still_a_CC = visual.TextStim(win=win, name='stay_still_a_CC',
    text='STAY VERY STILL',
    font='Arial',
    pos=(offset_x+0, offset_y+stay_still_y), height=stay_still_h, wrapWidth=1000.0, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-2.0);
stay_still_b_CC = visual.TextStim(win=win, name='stay_still_b_CC',
    text='STAY VERY STILL',
    font='Arial',
    pos=(offset_x+0, offset_y-stay_still_y), height=stay_still_h, wrapWidth=1000.0, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-3.0);
# Run 'Begin Experiment' code from trigger_code_Eproj
fmriClock = core.Clock() # clock for syncing with fMRI scanner

#trigger = 'parallel'
trigger = 'usb'
if trigger == 'parallel':
    from psychopy import parallel 
elif trigger == 'usb':
   from psychopy.hardware.emulator import launchScan    


settings = {
   'TR': 2, # duration (sec) per volume 
  'volumes': 309, # number of whole 3D volumes / frames
  'sync': ['num_add', 'equal'], # character to use as the sync timing event; assumed to come at start of a volume
  'skip': 0, # number of volumes lacking a sync pulse at start of scan for T1 stab -- (? LMD)
}


# --- Initialize components for Routine "fixation_init" ---
task_frame_fix1 = visual.Rect(
    win=win, name='task_frame_fix1',units='pix', 
    width=(box_w,box_h)[0], height=(box_w,box_h)[1],
    ori=0.0, pos=(offset_x+0, offset_y+0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=(0.7647, 0.7647, 0.7647), fillColor=(0.7647, 0.7647, 0.7647),
    opacity=None, depth=0.0, interpolate=True)
E_fix_init = visual.ImageStim(
    win=win,
    name='E_fix_init', 
    image='Supporting_Files/Images/Black_Grey_Crosshair.png', mask=None, anchor='center',
    ori=0, pos=(offset_x+0, offset_y+0), size=(fix_w, fix_h),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=False, depth=-1.0)

# --- Initialize components for Routine "fixation_inner" ---
task_frame_fix3 = visual.Rect(
    win=win, name='task_frame_fix3',units='pix', 
    width=(box_w,box_h)[0], height=(box_w,box_h)[1],
    ori=0.0, pos=(offset_x+0, offset_y+0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=(0.7647, 0.7647, 0.7647), fillColor=(0.7647, 0.7647, 0.7647),
    opacity=None, depth=0.0, interpolate=True)
E_fix_pres = visual.ImageStim(
    win=win,
    name='E_fix_pres', 
    image='Supporting_Files/Images/Black_Grey_Crosshair.png', mask=None, anchor='center',
    ori=0, pos=(offset_x+0, offset_y+0), size=(fix_w, fix_h),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=False, depth=-1.0)
Eproj_offtime_Response = keyboard.Keyboard()

# --- Initialize components for Routine "trial" ---
task_frame_trial = visual.Rect(
    win=win, name='task_frame_trial',units='pix', 
    width=(box_w,box_h)[0], height=(box_w,box_h)[1],
    ori=0.0, pos=(offset_x+0, offset_y+0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=(0.7647, 0.7647, 0.7647), fillColor=(0.7647, 0.7647, 0.7647),
    opacity=None, depth=0.0, interpolate=True)
EprojStimuli = visual.TextStim(win=win, name='EprojStimuli',
    text='',
    font='Arial',
    units='pix', pos=(pos_x+offset_x, pos_y+offset_y), height=letter_h, wrapWidth=pos_wrap, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-1.0);
EprojResponse = keyboard.Keyboard()
# Run 'Begin Experiment' code from code_2
import time
expInfo['expStartWallTime'] = time.ctime()



# --- Initialize components for Routine "fixation_wrap" ---
task_frame_fix2 = visual.Rect(
    win=win, name='task_frame_fix2',units='pix', 
    width=(box_w,box_h)[0], height=(box_w,box_h)[1],
    ori=0.0, pos=(offset_x+0, offset_y+0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=(0.7647, 0.7647, 0.7647), fillColor=(0.7647, 0.7647, 0.7647),
    opacity=None, depth=0.0, interpolate=True)
E_fix_wrap = visual.ImageStim(
    win=win,
    name='E_fix_wrap', 
    image='Supporting_Files/Images/Black_Grey_Crosshair.png', mask=None, anchor='center',
    ori=0, pos=(offset_x+0, offset_y+0), size=(fix_w, fix_h),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=512, interpolate=False, depth=-1.0)

# --- Initialize components for Routine "blank" ---
task_frame_blank = visual.Rect(
    win=win, name='task_frame_blank',units='pix', 
    width=(box_w,box_h)[0], height=(box_w,box_h)[1],
    ori=0.0, pos=(offset_x+0, offset_y+0), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=(0.7647, 0.7647, 0.7647), fillColor=(0.7647, 0.7647, 0.7647),
    opacity=None, depth=0.0, interpolate=True)

# --- Initialize components for Routine "Eproj_waitForFinish" ---
# Run 'Begin Experiment' code from finishCode_CC
# EXP_DURATION = 617

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "Variable_Setting_Eproj" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
Variable_Setting_EprojComponents = []
for thisComponent in Variable_Setting_EprojComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Variable_Setting_Eproj" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Variable_Setting_EprojComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Variable_Setting_Eproj" ---
for thisComponent in Variable_Setting_EprojComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Variable_Setting_Eproj" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "Eproj_Instructions" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
Eproj_Instruction_Screen.setPos((offset_x+0, offset_y+0))
E_key_resp_42.keys = []
E_key_resp_42.rt = []
_E_key_resp_42_allKeys = []
# keep track of which components have finished
Eproj_InstructionsComponents = [Eproj_Instruction_Screen, E_key_resp_42]
for thisComponent in Eproj_InstructionsComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Eproj_Instructions" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Eproj_Instruction_Screen* updates
    if Eproj_Instruction_Screen.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Eproj_Instruction_Screen.frameNStart = frameN  # exact frame index
        Eproj_Instruction_Screen.tStart = t  # local t and not account for scr refresh
        Eproj_Instruction_Screen.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Eproj_Instruction_Screen, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'Eproj_Instruction_Screen.started')
        Eproj_Instruction_Screen.setAutoDraw(True)
    
    # *E_key_resp_42* updates
    waitOnFlip = False
    if E_key_resp_42.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        E_key_resp_42.frameNStart = frameN  # exact frame index
        E_key_resp_42.tStart = t  # local t and not account for scr refresh
        E_key_resp_42.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(E_key_resp_42, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'E_key_resp_42.started')
        E_key_resp_42.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(E_key_resp_42.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(E_key_resp_42.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if E_key_resp_42.status == STARTED and not waitOnFlip:
        theseKeys = E_key_resp_42.getKeys(keyList=['space'], waitRelease=False)
        _E_key_resp_42_allKeys.extend(theseKeys)
        if len(_E_key_resp_42_allKeys):
            E_key_resp_42.keys = _E_key_resp_42_allKeys[-1].name  # just the last key pressed
            E_key_resp_42.rt = _E_key_resp_42_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Eproj_InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Eproj_Instructions" ---
for thisComponent in Eproj_InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Eproj_Instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# --- Prepare to start Routine "Eproj_ReadyScreen" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# Run 'Begin Routine' code from trigger_code_Eproj
if expInfo['mriMode'] != 'test': # or 'scan' !
    assert expInfo['mriMode'] == 'scan'

#### #       waitMsgStim = visual.TextStim(win, color='White', text=wait_msg)
### #       waitMsgStim.draw()
### #       win.flip()

# keep track of which components have finished
Eproj_ReadyScreenComponents = [polygon_fix, Ready_E, stay_still_a_CC, stay_still_b_CC]
for thisComponent in Eproj_ReadyScreenComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Eproj_ReadyScreen" ---
while continueRoutine and routineTimer.getTime() < 0.1:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *polygon_fix* updates
    if polygon_fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        polygon_fix.frameNStart = frameN  # exact frame index
        polygon_fix.tStart = t  # local t and not account for scr refresh
        polygon_fix.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(polygon_fix, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'polygon_fix.started')
        polygon_fix.setAutoDraw(True)
    if polygon_fix.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > polygon_fix.tStartRefresh + 0.1-frameTolerance:
            # keep track of stop time/frame for later
            polygon_fix.tStop = t  # not accounting for scr refresh
            polygon_fix.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'polygon_fix.stopped')
            polygon_fix.setAutoDraw(False)
    
    # *Ready_E* updates
    if Ready_E.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        Ready_E.frameNStart = frameN  # exact frame index
        Ready_E.tStart = t  # local t and not account for scr refresh
        Ready_E.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(Ready_E, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'Ready_E.started')
        Ready_E.setAutoDraw(True)
    if Ready_E.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > Ready_E.tStartRefresh + 0.1-frameTolerance:
            # keep track of stop time/frame for later
            Ready_E.tStop = t  # not accounting for scr refresh
            Ready_E.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Ready_E.stopped')
            Ready_E.setAutoDraw(False)
    
    # *stay_still_a_CC* updates
    if stay_still_a_CC.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        stay_still_a_CC.frameNStart = frameN  # exact frame index
        stay_still_a_CC.tStart = t  # local t and not account for scr refresh
        stay_still_a_CC.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(stay_still_a_CC, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'stay_still_a_CC.started')
        stay_still_a_CC.setAutoDraw(True)
    if stay_still_a_CC.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > stay_still_a_CC.tStartRefresh + 0.1-frameTolerance:
            # keep track of stop time/frame for later
            stay_still_a_CC.tStop = t  # not accounting for scr refresh
            stay_still_a_CC.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stay_still_a_CC.stopped')
            stay_still_a_CC.setAutoDraw(False)
    
    # *stay_still_b_CC* updates
    if stay_still_b_CC.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        stay_still_b_CC.frameNStart = frameN  # exact frame index
        stay_still_b_CC.tStart = t  # local t and not account for scr refresh
        stay_still_b_CC.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(stay_still_b_CC, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'stay_still_b_CC.started')
        stay_still_b_CC.setAutoDraw(True)
    if stay_still_b_CC.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > stay_still_b_CC.tStartRefresh + 0.1-frameTolerance:
            # keep track of stop time/frame for later
            stay_still_b_CC.tStop = t  # not accounting for scr refresh
            stay_still_b_CC.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stay_still_b_CC.stopped')
            stay_still_b_CC.setAutoDraw(False)
    # Run 'Each Frame' code from trigger_code_Eproj
    
    #if key_resp_trigger.keys == trigger:
    #    task_format_inst.finished = True
    #    continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Eproj_ReadyScreenComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Eproj_ReadyScreen" ---
for thisComponent in Eproj_ReadyScreenComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from trigger_code_Eproj
globalClock=fmriClock
mode=expInfo['mriMode']
wait_timeout=300
log=True
instr='select Scan or Test, press enter'
wait_msg='waiting'
simResponses=None
esc_key='escape'

if not 'sync' in settings:
        settings.update({'sync': '5'})
if not 'skip' in settings:
        settings.update({'skip': 0})
try:
        wait_timeout = max(0.01, float(wait_timeout))
except ValueError:
        msg = "wait_timeout must be number-like, but instead it was {}."
        raise ValueError(msg.format(wait_timeout))

stringify = lambda x: "{}".format(x)  # convert to str/unicode
if type(settings['sync']) == list:
    settings['sync'] = list(map(stringify, settings['sync']))
if type(settings['sync']) == str:
    settings['sync'] = stringify(settings['sync'])

settings['TR'] = float(settings['TR'])
settings['volumes'] = int(settings['volumes'])
settings['skip'] = int(settings['skip'])
msg = "vol: %(volumes)d  TR: %(TR).3fs  skip: %(skip)d  sync: '%(sync)s'"
runInfo = msg % settings

if log:  # pragma: no cover
        logging.exp('launchScan: ' + runInfo)

instructions = visual.TextStim(
        win, text=instr, height=.05, pos=(0, 0), color=.4, autoLog=False)

parameters = visual.TextStim(
        win, text=runInfo, height=.05, pos=(0, -0.5), color=.4, autoLog=False)

    # if a valid mode was specified, use it; otherwise query via RatingScale:
mode = "{}".format(mode).capitalize()
if mode not in ['Scan', 'Test']:
        run_type = visual.RatingScale(win, choices=['Scan', 'Test'],
                                      marker='circle',
                                      markerColor='DarkBlue', size=.8,
                                      stretch=.3, pos=(0.8, -0.9),
                                      markerStart='Test',
                                      lineColor='DarkGray', autoLog=False)
        while run_type.noResponse:
            instructions.draw()
            parameters.draw()
            run_type.draw()
            win.flip()
            if event.getKeys([esc_key]):
                break
        mode = run_type.getRating()

doSimulation = bool(mode == 'Test')

win.mouseVisible = False
if doSimulation:
        wait_msg += ' (simulation)'
#    msg = visual.TextStim(win, color='DarkGray', text=wait_msg, autoLog=False)
#    msg.draw()
#    win.flip()


event.clearEvents()  # do before starting the threads
if doSimulation:
        syncPulse = SyncGenerator(TR=1,TA=1,volumes=617, sync='equal', skip=0, sound=False)
        syncPulse.start()  # start emitting sync pulses
        core.runningThreads.append(syncPulse)
        if simResponses:
            roboResponses = ResponseEmulator(simResponses)
            # start emitting simulated user responses
            roboResponses.start()
            core.runningThreads.append(roboResponses)

# wait for first sync pulse:

timeoutClock = core.Clock()  # zeroed now

allKeys = []
while True:
    allKeys = event.getKeys()
    if allKeys:
        print('allKeys', allKeys)
        print('settings[sync]', settings['sync'])
        print(type(settings['sync']))
    if type(settings['sync']) == list and any([key in allKeys for key in settings['sync']]):
        break
    if type(settings['sync']) == str and settings['sync'] in allKeys:
        break
    if esc_key and esc_key in allKeys:  # pragma: no cover
        core.quit()
    if timeoutClock.getTime() > wait_timeout:
        msg = 'Waiting for scanner has timed out in %.3f seconds.'
        raise RuntimeError(msg % wait_timeout)

#allKeys = []
# while not settings['sync'] in allKeys:
#print('allKeys', allKeys)
#print('settings[sync]', settings['sync'])
#while not any([key in allKeys for key in settings['sync']]) if type(settings['sync']) == list else \
#        not settings['sync'] in allKeys:
#    allKeys = event.getKeys()
#    if esc_key and esc_key in allKeys:  # pragma: no cover
#        core.quit()
#    if timeoutClock.getTime() > wait_timeout:
#        msg = 'Waiting for scanner has timed out in %.3f seconds.'
#        raise RuntimeError(msg % wait_timeout)
if globalClock:
        globalClock.reset()
if log:  # pragma: no cover
        logging.exp('launchScan: start of scan')
    # blank the screen on first sync pulse received:

elapsed = 1










#if trigger == 'usb':
#       vol = launchScan(win, MR_settings, wait_msg='STAY VERY STILL',
#             globalClock=fmriClock, # <-- how you know the time! 
#             mode=expInfo['mriMode']) # <-- mode passed in
#elif trigger == 'parallel':
#       parallel.setPortAddress(0x378)
#       pin = 10; wait_msg = ""
#       pinStatus = parallel.readPin(pin)
#       while True:
#           if pinStatus != parallel.readPin(pin) or len(event.getKeys('esc')):
#              break
#              # start exp when pin values change
#       globalClock.reset()
#       logging.defaultClock.reset()
#       logging.exp('parallel trigger: start of scan')
#       win.flip()  # blank the screen on first sync pulse received
#else:
#   fmriClock.reset()

expInfo['triggerWallTime'] = time.ctime()
#core.wait(1)



routineTimer.reset()
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-0.100000)

# --- Prepare to start Routine "fixation_init" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
fixation_initComponents = [task_frame_fix1, E_fix_init]
for thisComponent in fixation_initComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "fixation_init" ---
while continueRoutine and routineTimer.getTime() < 7.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *task_frame_fix1* updates
    if task_frame_fix1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        task_frame_fix1.frameNStart = frameN  # exact frame index
        task_frame_fix1.tStart = t  # local t and not account for scr refresh
        task_frame_fix1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(task_frame_fix1, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'task_frame_fix1.started')
        task_frame_fix1.setAutoDraw(True)
    if task_frame_fix1.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > task_frame_fix1.tStartRefresh + 7.0-frameTolerance:
            # keep track of stop time/frame for later
            task_frame_fix1.tStop = t  # not accounting for scr refresh
            task_frame_fix1.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'task_frame_fix1.stopped')
            task_frame_fix1.setAutoDraw(False)
    
    # *E_fix_init* updates
    if E_fix_init.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        E_fix_init.frameNStart = frameN  # exact frame index
        E_fix_init.tStart = t  # local t and not account for scr refresh
        E_fix_init.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(E_fix_init, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'E_fix_init.started')
        E_fix_init.setAutoDraw(True)
    if E_fix_init.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > E_fix_init.tStartRefresh + 7-frameTolerance:
            # keep track of stop time/frame for later
            E_fix_init.tStop = t  # not accounting for scr refresh
            E_fix_init.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'E_fix_init.stopped')
            E_fix_init.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in fixation_initComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "fixation_init" ---
for thisComponent in fixation_initComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-7.000000)

# set up handler to look after randomisation of conditions etc
eproj_trials = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions("Supporting_Files/Spreadsheets/Eproj_Scan_Run" + expInfo['run_num'] +".xlsx"),
    seed=None, name='eproj_trials')
thisExp.addLoop(eproj_trials)  # add the loop to the experiment
thisEproj_trial = eproj_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisEproj_trial.rgb)
if thisEproj_trial != None:
    for paramName in thisEproj_trial:
        exec('{} = thisEproj_trial[paramName]'.format(paramName))

for thisEproj_trial in eproj_trials:
    currentLoop = eproj_trials
    # abbreviate parameter names if possible (e.g. rgb = thisEproj_trial.rgb)
    if thisEproj_trial != None:
        for paramName in thisEproj_trial:
            exec('{} = thisEproj_trial[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "fixation_inner" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    Eproj_offtime_Response.keys = []
    Eproj_offtime_Response.rt = []
    _Eproj_offtime_Response_allKeys = []
    # keep track of which components have finished
    fixation_innerComponents = [task_frame_fix3, E_fix_pres, Eproj_offtime_Response]
    for thisComponent in fixation_innerComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "fixation_inner" ---
    while continueRoutine and routineTimer.getTime() < 10.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *task_frame_fix3* updates
        if task_frame_fix3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            task_frame_fix3.frameNStart = frameN  # exact frame index
            task_frame_fix3.tStart = t  # local t and not account for scr refresh
            task_frame_fix3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(task_frame_fix3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'task_frame_fix3.started')
            task_frame_fix3.setAutoDraw(True)
        if task_frame_fix3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > task_frame_fix3.tStartRefresh + 10.0-frameTolerance:
                # keep track of stop time/frame for later
                task_frame_fix3.tStop = t  # not accounting for scr refresh
                task_frame_fix3.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'task_frame_fix3.stopped')
                task_frame_fix3.setAutoDraw(False)
        
        # *E_fix_pres* updates
        if E_fix_pres.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            E_fix_pres.frameNStart = frameN  # exact frame index
            E_fix_pres.tStart = t  # local t and not account for scr refresh
            E_fix_pres.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(E_fix_pres, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'E_fix_pres.started')
            E_fix_pres.setAutoDraw(True)
        if E_fix_pres.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > E_fix_pres.tStartRefresh + 10-frameTolerance:
                # keep track of stop time/frame for later
                E_fix_pres.tStop = t  # not accounting for scr refresh
                E_fix_pres.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'E_fix_pres.stopped')
                E_fix_pres.setAutoDraw(False)
        
        # *Eproj_offtime_Response* updates
        waitOnFlip = False
        if Eproj_offtime_Response.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            Eproj_offtime_Response.frameNStart = frameN  # exact frame index
            Eproj_offtime_Response.tStart = t  # local t and not account for scr refresh
            Eproj_offtime_Response.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(Eproj_offtime_Response, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'Eproj_offtime_Response.started')
            Eproj_offtime_Response.status = STARTED
            # AllowedKeys looks like a variable named `usable_keys`
            if not type(usable_keys) in [list, tuple, np.ndarray]:
                if not isinstance(usable_keys, str):
                    logging.error('AllowedKeys variable `usable_keys` is not string- or list-like.')
                    core.quit()
                elif not ',' in usable_keys:
                    usable_keys = (usable_keys,)
                else:
                    usable_keys = eval(usable_keys)
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(Eproj_offtime_Response.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(Eproj_offtime_Response.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if Eproj_offtime_Response.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > Eproj_offtime_Response.tStartRefresh + 10.0-frameTolerance:
                # keep track of stop time/frame for later
                Eproj_offtime_Response.tStop = t  # not accounting for scr refresh
                Eproj_offtime_Response.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Eproj_offtime_Response.stopped')
                Eproj_offtime_Response.status = FINISHED
        if Eproj_offtime_Response.status == STARTED and not waitOnFlip:
            theseKeys = Eproj_offtime_Response.getKeys(keyList=list(usable_keys), waitRelease=False)
            _Eproj_offtime_Response_allKeys.extend(theseKeys)
            if len(_Eproj_offtime_Response_allKeys):
                Eproj_offtime_Response.keys = _Eproj_offtime_Response_allKeys[0].name  # just the first key pressed
                Eproj_offtime_Response.rt = _Eproj_offtime_Response_allKeys[0].rt
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in fixation_innerComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "fixation_inner" ---
    for thisComponent in fixation_innerComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if Eproj_offtime_Response.keys in ['', [], None]:  # No response was made
        Eproj_offtime_Response.keys = None
    eproj_trials.addData('Eproj_offtime_Response.keys',Eproj_offtime_Response.keys)
    if Eproj_offtime_Response.keys != None:  # we had a response
        eproj_trials.addData('Eproj_offtime_Response.rt', Eproj_offtime_Response.rt)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-10.000000)
    
    # --- Prepare to start Routine "trial" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    EprojStimuli.setText(Question

)
    EprojResponse.keys = []
    EprojResponse.rt = []
    _EprojResponse_allKeys = []
    # Run 'Begin Routine' code from code_2
    EprojStimuli.alignText = 'left'
    
    timePrecise.reset()
    hasResponded = False 
    
    eproj_trials.addData('globalClockTime_start',globalClock.getTime())
    # keep track of which components have finished
    trialComponents = [task_frame_trial, EprojStimuli, EprojResponse]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "trial" ---
    while continueRoutine and routineTimer.getTime() < 10.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *task_frame_trial* updates
        if task_frame_trial.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            task_frame_trial.frameNStart = frameN  # exact frame index
            task_frame_trial.tStart = t  # local t and not account for scr refresh
            task_frame_trial.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(task_frame_trial, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'task_frame_trial.started')
            task_frame_trial.setAutoDraw(True)
        if task_frame_trial.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > task_frame_trial.tStartRefresh + 10.0-frameTolerance:
                # keep track of stop time/frame for later
                task_frame_trial.tStop = t  # not accounting for scr refresh
                task_frame_trial.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'task_frame_trial.stopped')
                task_frame_trial.setAutoDraw(False)
        
        # *EprojStimuli* updates
        if EprojStimuli.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            EprojStimuli.frameNStart = frameN  # exact frame index
            EprojStimuli.tStart = t  # local t and not account for scr refresh
            EprojStimuli.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(EprojStimuli, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'EprojStimuli.started')
            EprojStimuli.setAutoDraw(True)
        if EprojStimuli.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > EprojStimuli.tStartRefresh + 10.0-frameTolerance:
                # keep track of stop time/frame for later
                EprojStimuli.tStop = t  # not accounting for scr refresh
                EprojStimuli.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'EprojStimuli.stopped')
                EprojStimuli.setAutoDraw(False)
        
        # *EprojResponse* updates
        waitOnFlip = False
        if EprojResponse.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            EprojResponse.frameNStart = frameN  # exact frame index
            EprojResponse.tStart = t  # local t and not account for scr refresh
            EprojResponse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(EprojResponse, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'EprojResponse.started')
            EprojResponse.status = STARTED
            # AllowedKeys looks like a variable named `usable_keys`
            if not type(usable_keys) in [list, tuple, np.ndarray]:
                if not isinstance(usable_keys, str):
                    logging.error('AllowedKeys variable `usable_keys` is not string- or list-like.')
                    core.quit()
                elif not ',' in usable_keys:
                    usable_keys = (usable_keys,)
                else:
                    usable_keys = eval(usable_keys)
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(EprojResponse.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(EprojResponse.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if EprojResponse.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > EprojResponse.tStartRefresh + 10.0-frameTolerance:
                # keep track of stop time/frame for later
                EprojResponse.tStop = t  # not accounting for scr refresh
                EprojResponse.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'EprojResponse.stopped')
                EprojResponse.status = FINISHED
        if EprojResponse.status == STARTED and not waitOnFlip:
            theseKeys = EprojResponse.getKeys(keyList=list(usable_keys), waitRelease=False)
            _EprojResponse_allKeys.extend(theseKeys)
            if len(_EprojResponse_allKeys):
                EprojResponse.keys = _EprojResponse_allKeys[0].name  # just the first key pressed
                EprojResponse.rt = _EprojResponse_allKeys[0].rt
        # Run 'Each Frame' code from code_2
        if EprojResponse.keys and not hasResponded:
            hasResponded = True
            
            respTime = EprojResponse.rt
            
            # log some stuffs
            #
            # task_blocks.addData('actualChoiceOffset', fmriClock.getTime())
            # task_blocks.addData('responseTime', respTime)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "trial" ---
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if EprojResponse.keys in ['', [], None]:  # No response was made
        EprojResponse.keys = None
    eproj_trials.addData('EprojResponse.keys',EprojResponse.keys)
    if EprojResponse.keys != None:  # we had a response
        eproj_trials.addData('EprojResponse.rt', EprojResponse.rt)
    # Run 'End Routine' code from code_2
    logging.flush()
    
    eproj_trials.addData('globalClockTime_end',globalClock.getTime())
    eproj_trials.addData('trial_duration',timePrecise.getTime())
    
    
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-10.000000)
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'eproj_trials'


# --- Prepare to start Routine "fixation_wrap" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
fixation_wrapComponents = [task_frame_fix2, E_fix_wrap]
for thisComponent in fixation_wrapComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "fixation_wrap" ---
while continueRoutine and routineTimer.getTime() < 10.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *task_frame_fix2* updates
    if task_frame_fix2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        task_frame_fix2.frameNStart = frameN  # exact frame index
        task_frame_fix2.tStart = t  # local t and not account for scr refresh
        task_frame_fix2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(task_frame_fix2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'task_frame_fix2.started')
        task_frame_fix2.setAutoDraw(True)
    if task_frame_fix2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > task_frame_fix2.tStartRefresh + 10.0-frameTolerance:
            # keep track of stop time/frame for later
            task_frame_fix2.tStop = t  # not accounting for scr refresh
            task_frame_fix2.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'task_frame_fix2.stopped')
            task_frame_fix2.setAutoDraw(False)
    
    # *E_fix_wrap* updates
    if E_fix_wrap.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        E_fix_wrap.frameNStart = frameN  # exact frame index
        E_fix_wrap.tStart = t  # local t and not account for scr refresh
        E_fix_wrap.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(E_fix_wrap, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'E_fix_wrap.started')
        E_fix_wrap.setAutoDraw(True)
    if E_fix_wrap.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > E_fix_wrap.tStartRefresh + 10-frameTolerance:
            # keep track of stop time/frame for later
            E_fix_wrap.tStop = t  # not accounting for scr refresh
            E_fix_wrap.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'E_fix_wrap.stopped')
            E_fix_wrap.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in fixation_wrapComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "fixation_wrap" ---
for thisComponent in fixation_wrapComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-10.000000)

# --- Prepare to start Routine "blank" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
blankComponents = [task_frame_blank]
for thisComponent in blankComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "blank" ---
while continueRoutine and routineTimer.getTime() < 0.1:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *task_frame_blank* updates
    if task_frame_blank.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        task_frame_blank.frameNStart = frameN  # exact frame index
        task_frame_blank.tStart = t  # local t and not account for scr refresh
        task_frame_blank.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(task_frame_blank, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'task_frame_blank.started')
        task_frame_blank.setAutoDraw(True)
    if task_frame_blank.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > task_frame_blank.tStartRefresh + 0.1-frameTolerance:
            # keep track of stop time/frame for later
            task_frame_blank.tStop = t  # not accounting for scr refresh
            task_frame_blank.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'task_frame_blank.stopped')
            task_frame_blank.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in blankComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "blank" ---
for thisComponent in blankComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-0.100000)

# --- Prepare to start Routine "Eproj_waitForFinish" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
Eproj_waitForFinishComponents = []
for thisComponent in Eproj_waitForFinishComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Eproj_waitForFinish" ---
while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Eproj_waitForFinishComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Eproj_waitForFinish" ---
for thisComponent in Eproj_waitForFinishComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from finishCode_CC
logging.exp("Experiment Finished")

# the Routine "Eproj_waitForFinish" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
# Run 'End Experiment' code from variables
exp_info.at[0, 'EPROJ_run'] =  (int(expInfo['run_num'])+1)
exp_info.to_csv('../exp_info.csv', index=False)

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
