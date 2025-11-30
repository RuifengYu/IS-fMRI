# EXPT_EPROJ_self
Episodic projection for localizing the default mode network. Adapted from Lauren DiNicola's EPROJ expt but with only "self" conditions.

Steps to run:
- Start up `EPROJ/EPROJ.psyexp` with Psychopy 2022.* (newer versions of Psychopy are NOT compatible)
- Run `python scan_setup.py` to initialize subject info before each run.

During the expt:
- Press `space` on the first screen after explaining the task, then wait for the trigger
- Manual trigger (for debugging): `command` + `=` on the second screen

Subject data is stored under `EPROJ/data`.
Stimuli are stored under `EPROJ/Supporting_Files/Spreadsheets/*.xlsx`.
