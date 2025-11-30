function InnerLang(subjectId, runId, setId, varargin)
% INNERLANG
% fMRI experiment for investigating individual differences in inner language processing
%
% INPUT ARGUMENTS (Required):
%   subjectId         - Subject identifier (e.g., 'S001')
%   runId             - Run identifier: 'run1', 'run2', 'run3', or 'run4'
%   setId             - Stimulus set for both conditions: 'set1', 'set2', 'set3', or 'set4'
%                       (same set is used for both spontaneous and specific conditions)
%
% OPTIONAL ARGUMENTS (name/value pairs):
%   'SkipSyncTests'     - Skip Psychtoolbox sync tests (default: from config)
%
% EXAMPLE:
%   InnerLang('S001', 'run1', 'set1')

% ============================================================================
% SECTION 1: INPUT VALIDATION AND PARSING
% ============================================================================

arguments
    subjectId {mustBeTextScalar}
    runId {mustBeTextScalar}
    setId {mustBeTextScalar}
end

arguments (Repeating)
    varargin
end

% Parse optional arguments
opts = parseOptionalArguments(varargin{:});

% Add trigger utils to path (for fMRI trigger detection)
TRIGGER_UTIL_DIR = fullfile(fileparts(mfilename('fullpath')), 'EXPT_EPROJself_ptb-main', 'TOOL_Matlab_trigger_utils');
addpath(TRIGGER_UTIL_DIR);

% Load experiment configuration (timings, colors, paths, etc.)
config = getExperimentConfig();

% Convert string identifiers to numeric indices
runNumber = parseRunIdentifier(runId);
setNumber = parseSetIdentifier(setId);  % Same set for both conditions

% ============================================================================
% SECTION 2: STIMULUS PREPARATION
% ============================================================================

% Get the presentation pattern for this run
% Pattern is a string like 'srrrsrsr' where 's'=specific, 'r'=spontaneous
% Only one order set now
runPattern = config.runPatterns{runNumber};

% Build the complete stimulus library
stimuliSets = buildStimuliSets();

% Prepare trial list based on run pattern and selected set
trials = prepareRunTrials(runNumber,runPattern,setNumber,setNumber,stimuliSets);

% ============================================================================
% SECTION 3: PSYCHTOOLBOX INITIALIZATION
% ============================================================================

% Initialize Psychtoolbox with modern color space
PsychDefaultSetup(2);

% Configure vertical blank synchronization (VBL sync)
% Skip sync tests (can be overridden by optional argument)
skipSyncTests = false;
if isfield(config, 'psychtoolbox') && isfield(config.psychtoolbox, 'skipSyncTests')
    skipSyncTests = config.psychtoolbox.skipSyncTests;
end
if ~isempty(opts.skipSyncTests)
    skipSyncTests = opts.skipSyncTests;
end
Screen('Preference', 'SkipSyncTests', double(skipSyncTests));

% Initialize audio subsystem for beep cues
audio = initializeAudioSubsystem(config);

% Configure Psychtoolbox imaging pipeline
PsychImaging('PrepareConfiguration');
PsychImaging('AddTask', 'General', 'UseRetinaResolution');      % Handle Retina displays
PsychImaging('AddTask', 'FinalFormatting', 'UseRetinaResolution');

% Select screen (use max screen number for external monitor)
screens = Screen('Screens');
screenNumber = config.screenNumber;
if isempty(screenNumber)
    screenNumber = max(screens);
end

% Open fullscreen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, config.colors.backgroundNormalized);
[centerX, centerY]   = RectCenter(windowRect);

% Set up blending for smooth lines (same as make_window.m)
Screen('BlendFunction', window, 'GL_SRC_ALPHA', 'GL_ONE_MINUS_SRC_ALPHA');

% Configure text properties
Screen('TextFont', window, config.text.font);
Screen('TextSize', window, config.text.baseSize);
Screen('TextColor', window, config.colors.textNormalized);

% Hide mouse cursor and unify keyboard names
HideCursor;
KbName('UnifyKeyNames');
escapeKey = KbName('ESCAPE');
% Use keyboard key '1' instead of button box
button1Key = KbName('1!');

% ============================================================================
% SECTION 4: DATA STRUCTURE INITIALIZATION
% ============================================================================

% Initialize run data structure (only what's needed for CSV output)
runData = struct();
runData.subjectId = char(subjectId);
runData.runNumber = runNumber;
runData.runId     = sprintf('run%d', runNumber);
runData.setId     = sprintf('set%d', setNumber);
runData.startTimestamp = char(datetime("now", "Format", "yyyy-MM-dd HH:mm:ss"));

% Preallocate trial data structures (simplified - only fields used in CSV)
timingTemplate   = struct('promptOnset', NaN, 'fixationEnd', NaN, 'duration', NaN);
trialTemplate    = struct( ...
    'condition', '', ...
    'prompt', '', ...
    'content', '', ...
    'timing',  timingTemplate ...
);
runData.trials = repmat(trialTemplate, 1, numel(trials));

% Initialize attention check records (one per trial)
runData.attentionChecks = struct('afterTrial', {}, 'responded', {}, 'responseKey', {}, 'rt', {}, 'onset', {}, 'imageOnset', {}, 'blankOnset', {});

% Setup CSV output file (shared across all runs for this subject and set)
% Create output directory if it doesn't exist
if ~exist(config.outputDir, 'dir')
    mkdir(config.outputDir);
end

% Generate output filename (without runId, so all runs write to same file)
% Use subjectId and setId only, so all runs for this subject/set use the same file
outputName = sprintf('%s_set%d.csv', char(subjectId), setNumber);
outputPath = fullfile(config.outputDir, outputName);

% Check if file exists to determine if we need to write header
fileExists = exist(outputPath, 'file') == 2;



% ============================================================================
% SECTION 5: EXPERIMENT EXECUTION
% ============================================================================

try
    % ------------------------------------------------------------------------
    % 5.1: PRE-RUN SETUP
    % ------------------------------------------------------------------------
    
    % Show run start message and wait for trigger
    Screen('FillRect', window, config.colors.backgroundNormalized);
    Screen('TextSize', window, config.text.baseSize);
    Screen('TextFont', window, config.text.font);
    Screen('TextColor', window, config.colors.textNormalized);
    runStartText = sprintf('Run %d\n\nWaiting for trigger to start', runNumber);
    DrawFormattedText(window, runStartText, 'center', 'center', config.colors.textNormalized, [], [], [], 1.5);
    Screen('Flip', window);
    
    % Wait for fMRI trigger signal ('t' key from scanner)
    % This uses KbQueue for reliable trigger detection (same as run_eproj_self.m)
    fprintf('Waiting for fMRI trigger...\n');
    runStartTime = wait_for_trigger_kbqueue_all_dvc();
    fprintf('Trigger received at time: %.4f\n', runStartTime);
    
    % Initial fixation period before run starts (12 seconds)
    displayFixation(window, centerX, centerY, config, config.timings.runFixation, escapeKey);
    totalTrials  = numel(trials);
    attentionRecords = struct('afterTrial', {}, 'responded', {}, 'responseKey', {}, 'rt', {}, 'onset', {}, 'imageOnset', {}, 'blankOnset', {});

    % ------------------------------------------------------------------------
    % 5.2: MAIN TRIAL LOOP
    % ------------------------------------------------------------------------
    
    for trialIdx = 1:totalTrials
        % Get current stimulus
        stimulus  = trials(trialIdx);
        
        % Present trial: show text for 5s, then fixation for 30s
        trialInfo = presentTrial(window, stimulus, centerX, centerY, config, escapeKey, audio);
    
        % Store trial information
        runData.trials(trialIdx).condition = stimulus.condition;  % 'spontaneous' or 'specific'
        runData.trials(trialIdx).prompt    = stimulus.prompt;
        runData.trials(trialIdx).content   = stimulus.content;
    
        % Store timing data (relative to run start)
        runData.trials(trialIdx).timing = struct( ...
            'promptOnset', trialInfo.startTime   - runStartTime, ...  % When prompt appeared
            'fixationEnd', trialInfo.endTime     - runStartTime, ...  % When fixation ended
            'duration',    trialInfo.endTime     - trialInfo.startTime ... % Total trial duration
        );

        % Attention check after EVERY trial
        attentionInfo = displayAttentionCheck(window, centerX, centerY, config, button1Key, escapeKey);
        attentionRecords(end+1) = struct( ...
            'afterTrial', trialIdx, ...
            'responded',  attentionInfo.responded, ...
            'responseKey', attentionInfo.responseKey, ...
            'rt',          attentionInfo.responseTime, ...  % responseTime from displayAttentionCheck
            'onset',       attentionInfo.startTime - runStartTime, ...
            'imageOnset',  attentionInfo.imageOnset - runStartTime, ...
            'blankOnset',  attentionInfo.blankOnset - runStartTime ...
        );
    
        % Real-time CSV output: write immediately after each trial + attention check
        rowData = table(...
            {char(subjectId)}, runNumber, setNumber, ...
            trialIdx, {stimulus.condition}, {stimulus.prompt}, {stimulus.content}, ...
            trialInfo.startTime - runStartTime, ...
            trialInfo.endTime - runStartTime, ...
            trialInfo.endTime - trialInfo.startTime, ...
            attentionInfo.responseKey, attentionInfo.responseTime, ...
            'VariableNames', {'subjectId', 'runNumber', 'setId', ...
            'trialIndex', 'condition', 'prompt', 'content', ...
            'promptOnset', 'fixationEnd', 'trialDuration', ...
            'attentionResponseKey', 'attentionRT'});
        
        % Write to CSV (append mode, write header only if file doesn't exist)
        writetable(rowData, outputPath, 'WriteMode', 'append', 'WriteVariableNames', ~fileExists);
        fileExists = true;  % File exists after first write
    
        % Mid-run fixation break (after trial 4)
        if trialIdx == config.midRunTrialIndex && trialIdx < totalTrials
            displayFixation(window, centerX, centerY, config, config.timings.runFixation, escapeKey);
        end
    end

    % ------------------------------------------------------------------------
    % 5.3: POST-RUN
    % ------------------------------------------------------------------------
    
    % Final fixation period
    displayFixation(window, centerX, centerY, config, config.timings.runFixation, escapeKey);

    % Store attention check records
    runData.attentionChecks = attentionRecords;
    
    % Record final end timestamp and runtime (after final fixation)
    runData.endTimestamp = char(datetime("now", "Format", "yyyy-MM-dd HH:mm:ss"));
    runData.runtimeSeconds = GetSecs - runStartTime;



    % ------------------------------------------------------------------------
    % 5.5: CLEANUP
    % ------------------------------------------------------------------------
    
    % Release resources
    releaseAudioSubsystem(audio);
    sca;  % Close all screens
    ShowCursor;
    
    fprintf('Run %d (set %s) completed. Data saved to %s\n', ...
        runNumber, runData.setId, outputPath);
    fprintf('CSV file contains %d trials with timing and attention check data.\n', totalTrials);

catch ME
    % ------------------------------------------------------------------------
    % ERROR HANDLING
    % ------------------------------------------------------------------------
    % Ensure resources are released even if an error occurs
    releaseAudioSubsystem(audio);
    sca;  
    ShowCursor;
    rethrow(ME);  % Re-throw error after cleanup
end

end

% ============================================================================
% HELPER FUNCTIONS
% ============================================================================


% ----------------------------------------------------------------------------
% FUNCTION: parseOptionalArguments
% ----------------------------------------------------------------------------
% Parses optional name/value pair arguments
% Supported options:
%   'SkipSyncTests'    - Boolean, whether to skip Psychtoolbox sync tests
% ----------------------------------------------------------------------------
function opts = parseOptionalArguments(varargin)
opts.skipSyncTests = [];

if isempty (varargin)
    return;
end

if mod(numel(varargin), 2) ~= 0
    error('Optional arguments must be provided as name/value pairs.');
end

for idx = 1:2:numel(varargin) 
    name = lower(string(varargin {idx}));
    value = varargin {idx+1};
    switch name
        case "skipsynctests" 
            opts.skipSyncTests = logical(value);
        otherwise
            error ('Unknown optional arguments: %s',name);
    end
end
end

% ----------------------------------------------------------------------------
% FUNCTION: getExperimentConfig
% ----------------------------------------------------------------------------
% Returns a structure containing all experiment configuration parameters:
%   - Screen settings
%   - Colors and text properties
%   - Timing parameters
%   - Audio settings
%   - Image file paths
%   - Run patterns (4 runs)
% ----------------------------------------------------------------------------
function config = getExperimentConfig()
    config.screenNumber = [];
    config.outputDir = 'data';
    config.psychtoolbox.skipSyncTests = true; % Set to false for formal experiments
    
    config.colors.background = [255 255 255];
    config.colors.text       = [0 0 0];
    config.colors.red        = [255 0 0];  % Red color for thinking period fixation cross
    config.colors.backgroundNormalized = config.colors.background / 255;
    config.colors.textNormalized       = config.colors.text / 255;
    config.colors.redNormalized        = config.colors.red / 255;
    
    config.text.font = 'Arial';
    config.text.baseSize = 72;       % 1.5x larger font for scanner viewing (48*1.5)
    config.text.promptSize = 64;    % promptSize + 5 more (59+5)
    config.text.contentSize = 72;    % 1.5x larger for content line (48*1.5)
    config.text.attentionSize = 108; % 1.5x larger (72*1.5)
    
    config.timings.prompt             = 5;   % Stimulus presentation time
    config.timings.postPromptFixation = 30;  % Thinking period
    config.timings.trialTotal         = 35;  % Total trial time
    config.timings.attentionImage     = 2;   % Attention check image display time
    config.timings.attentionBlank     = 1;   % Attention check blank time
    config.timings.runFixation        = 12;  % Pre-run, mid-run, post-run fixation
    config.midRunTrialIndex           = 4;   % Mid-run break after 4 trials
    
    config.audio.enabled    = true;
    config.audio.sampleRate = 44100;
    config.audio.frequency  = 800;
    config.audio.duration   = 0.1;
    config.audio.volume     = 1.0;
    
    % Button image path for attention checks (try multiple possible paths)
    if exist('button/button.png', 'file') == 2
        config.images.button = 'button/button.png';
    elseif exist('button.jpeg', 'file') == 2
        config.images.button = 'button.jpeg';
    elseif exist('button/button.jpeg', 'file') == 2
        config.images.button = 'button/button.jpeg';
    else
        config.images.button = '';  % Will use text fallback
    end
    
    % Run patterns: 4 runs, 8 trials each (4 spontaneous + 4 specific)
    config.runPatterns = { ...
        's r r s s r r s', ...  % Run 1
        's r s r r s r s', ...  % Run 2
        'r s r s s r s r', ...  % Run 3
        'r s s r r s s r' ...   % Run 4
    };
end

% ----------------------------------------------------------------------------
% FUNCTION: buildStimuliSets
% ----------------------------------------------------------------------------
% Builds the complete stimulus library organized by:
%   - Condition (spontaneous/specific)
%   - Set number (1, 2, 3, or 4)
%   - Run number (1, 2, 3, or 4)
%   - Item index (1-16)
%
% Each stimulus set contains 16 items distributed across 4 runs (4 per run).
% The same 16 items appear in different orders across the 4 sets.
% ----------------------------------------------------------------------------
function stimuli = buildStimuliSets()

% Define spontaneous stimuli (R)
% These are open-ended questions that prompt natural thinking
% Each set has 16 items distributed across 4 runs (4 per run)

% Set 1
stimuli.spontaneous(1).runs(1).items = buildStimulusGroup({ ...
    'Think about what you plan to do tomorrow.', 1; ...
    'Think about what you look for in a meaningful relationship.', 2; ...
    'Think about what kind of person you want to be.', 3; ...
    'Think about what you would do to relax.', 4 ...
});
stimuli.spontaneous(1).runs(2).items = buildStimulusGroup({ ...
    'Think about what your perfect weekend would include.', 5; ...
    'Think about how you have changed these years.', 6; ...
    'Think about how you handle conflicting opinions.', 7; ...
    'Think about what makes you feel fulfilled.', 8 ...
});
stimuli.spontaneous(1).runs(3).items = buildStimulusGroup({ ...
    'Think about a hobby that you want to start.', 9; ...
    'Think about a decision you are currently facing.', 10; ...
    'Think about what success means to you.', 11; ...
    'Think about something you want to accomplish this year.', 12 ...
});
stimuli.spontaneous(1).runs(4).items = buildStimulusGroup({ ...
    'Think about something you want to buy recently.', 13; ...
    'Think about where you would like to travel next.', 14; ...
    'Think about a trait you appreciate about yourself.', 15; ...
    'Think about something you are curious about.', 16 ...
});


% Set 2
stimuli.spontaneous(2).runs(1).items = buildStimulusGroup({ ...
    'Think about something you want to buy recently.', 1; ...
    'Think about what kind of person you want to be.', 2; ...
    'Think about what your perfect weekend would include.', 3; ...
    'Think about what makes you feel fulfilled.', 4 ...
});
stimuli.spontaneous(2).runs(2).items = buildStimulusGroup({ ...
    'Think about something you are curious about.', 5; ...
    'Think about what you plan to do tomorrow.', 6; ...
    'Think about what success means to you.', 7; ...
    'Think about what you look for in a meaningful relationship.', 8 ...
});
stimuli.spontaneous(2).runs(3).items = buildStimulusGroup({ ...
    'Think about how you have changed these years.', 9; ...
    'Think about something you want to accomplish this year.', 10; ...
    'Think about where you would like to travel next.', 11; ...
    'Think about what you would do to relax.', 12 ...
});
stimuli.spontaneous(2).runs(4).items = buildStimulusGroup({ ...
    'Think about a decision you are currently facing.', 13; ...
    'Think about how you handle conflicting opinions.', 14; ...
    'Think about a trait you appreciate about yourself.', 15; ...
    'Think about a hobby that you want to start.', 16 ...
});


% Set 3
stimuli.spontaneous(3).runs(1).items = buildStimulusGroup({ ...
    'Think about what you would do to relax.', 1; ...
    'Think about a decision you are currently facing.', 2; ...
    'Think about what you look for in a meaningful relationship.', 3; ...
    'Think about something you want to buy recently.', 4 ...
});
stimuli.spontaneous(3).runs(2).items = buildStimulusGroup({ ...
    'Think about what kind of person you want to be.', 5; ...
    'Think about where you would like to travel next.', 6; ...
    'Think about what makes you feel fulfilled.', 7; ...
    'Think about something you are curious about.', 8 ...
});
stimuli.spontaneous(3).runs(3).items = buildStimulusGroup({ ...
    'Think about a trait you appreciate about yourself.', 9; ...
    'Think about how you handle conflicting opinions.', 10; ...
    'Think about what your perfect weekend would include.', 11; ...
    'Think about something you want to accomplish this year.', 12 ...
});
stimuli.spontaneous(3).runs(4).items = buildStimulusGroup({ ...
    'Think about a hobby that you want to start.', 13; ...
    'Think about how you have changed these years.', 14; ...
    'Think about what you plan to do tomorrow.', 15; ...
    'Think about what success means to you.', 16 ...
});

% Set 4
stimuli.spontaneous(4).runs(1).items = buildStimulusGroup({ ...
    'Think about what makes you feel fulfilled.', 1; ...
    'Think about what you look for in a meaningful relationship.', 2; ...
    'Think about something you want to buy recently.', 3; ...
    'Think about what you would do to relax.', 4 ...
});
stimuli.spontaneous(4).runs(2).items = buildStimulusGroup({ ...
    'Think about what your perfect weekend would include.', 5; ...
    'Think about what success means to you.', 6; ...
    'Think about where you would like to travel next.', 7; ...
    'Think about how you have changed these years.', 8 ...
});
stimuli.spontaneous(4).runs(3).items = buildStimulusGroup({ ...
    'Think about a decision you are currently facing.', 9; ...
    'Think about what kind of person you want to be.', 10; ...
    'Think about a hobby that you want to start.', 11; ...
    'Think about something you want to accomplish this year.', 12 ...
});
stimuli.spontaneous(4).runs(4).items = buildStimulusGroup({ ...
    'Think about something you are curious about.', 13; ...
    'Think about what you plan to do tomorrow.', 14; ...
    'Think about a trait you appreciate about yourself.', 15; ...
    'Think about how you handle conflicting opinions.', 16 ...
});

% Define specific stimuli (S)
% These are sentences that participants imagine saying
% Each set has 16 items distributed across 4 runs (4 per run)

% Set 1
stimuli.specific(1).runs(1).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Adaptation takes time.', 1; ...
    'Imagine saying the sentence: Technology changes society.', 2; ...
    'Imagine saying the sentence: Attention is selective.', 3; ...
    'Imagine saying the sentence: Markets reflect demand.', 4 ...
});
stimuli.specific(1).runs(2).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Information can be stored.', 5; ...
    'Imagine saying the sentence: Diversity exists in life.', 6; ...
    'Imagine saying the sentence: Abstraction simplifies complexity.', 7; ...
    'Imagine saying the sentence: Language enables communication.', 8 ...
});
stimuli.specific(1).runs(3).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Preparation facilitates action.', 9; ...
    'Imagine saying the sentence: Reasoning uses logic.', 10; ...
    'Imagine saying the sentence: Context affects meaning.', 11; ...
    'Imagine saying the sentence: Questions lead to discovery.', 12 ...
});
stimuli.specific(1).runs(4).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Sleep restores energy.', 13; ...
    'Imagine saying the sentence: Resources can be limited.', 14; ...
    'Imagine saying the sentence: Frequency relates to probability.', 15; ...
    'Imagine saying the sentence: Experience shapes perspectives.', 16 ...
});

% Set 2
stimuli.specific(2).runs(1).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Markets reflect demand.', 1; ...
    'Imagine saying the sentence: Frequency relates to probability.', 2; ...
    'Imagine saying the sentence: Resources can be limited.', 3; ...
    'Imagine saying the sentence: Context affects meaning.', 4 ...
});
stimuli.specific(2).runs(2).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Experience shapes perspectives.', 5; ...
    'Imagine saying the sentence: Technology changes society.', 6; ...
    'Imagine saying the sentence: Sleep restores energy.', 7; ...
    'Imagine saying the sentence: Reasoning uses logic.', 8 ...
});
stimuli.specific(2).runs(3).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Language enables communication.', 9; ...
    'Imagine saying the sentence: Abstraction simplifies complexity.', 10; ...
    'Imagine saying the sentence: Questions lead to discovery.', 11; ...
    'Imagine saying the sentence: Attention is selective.', 12 ...
});
stimuli.specific(2).runs(4).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Information can be stored.', 13; ...
    'Imagine saying the sentence: Diversity exists in life.', 14; ...
    'Imagine saying the sentence: Adaptation takes time.', 15; ...
    'Imagine saying the sentence: Preparation facilitates action.', 16 ...
});

% Set 3
stimuli.specific(3).runs(1).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Sleep restores energy.', 1; ...
    'Imagine saying the sentence: Technology changes society.', 2; ...
    'Imagine saying the sentence: Resources can be limited.', 3; ...
    'Imagine saying the sentence: Attention is selective.', 4 ...
});
stimuli.specific(3).runs(2).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Preparation facilitates action.', 5; ...
    'Imagine saying the sentence: Questions lead to discovery.', 6; ...
    'Imagine saying the sentence: Markets reflect demand.', 7; ...
    'Imagine saying the sentence: Reasoning uses logic.', 8 ...
});
stimuli.specific(3).runs(3).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Adaptation takes time.', 9; ...
    'Imagine saying the sentence: Language enables communication.', 10; ...
    'Imagine saying the sentence: Experience shapes perspectives.', 11; ...
    'Imagine saying the sentence: Frequency relates to probability.', 12 ...
});
stimuli.specific(3).runs(4).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Diversity exists in life.', 13; ...
    'Imagine saying the sentence: Context affects meaning.', 14; ...
    'Imagine saying the sentence: Abstraction simplifies complexity.', 15; ...
    'Imagine saying the sentence: Information can be stored.', 16 ...
});

% Set 4
stimuli.specific(4).runs(1).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Frequency relates to probability.', 1; ...
    'Imagine saying the sentence: Questions lead to discovery.', 2; ...
    'Imagine saying the sentence: Experience shapes perspectives.', 3; ...
    'Imagine saying the sentence: Markets reflect demand.', 4 ...
});
stimuli.specific(4).runs(2).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Reasoning uses logic.', 5; ...
    'Imagine saying the sentence: Resources can be limited.', 6; ...
    'Imagine saying the sentence: Language enables communication.', 7; ...
    'Imagine saying the sentence: Context affects meaning.', 8 ...
});
stimuli.specific(4).runs(3).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Diversity exists in life.', 9; ...
    'Imagine saying the sentence: Abstraction simplifies complexity.', 10; ...
    'Imagine saying the sentence: Information can be stored.', 11; ...
    'Imagine saying the sentence: Attention is selective.', 12 ...
});
stimuli.specific(4).runs(4).items = buildStimulusGroup({ ...
    'Imagine saying the sentence: Sleep restores energy.', 13; ...
    'Imagine saying the sentence: Adaptation takes time.', 14; ...
    'Imagine saying the sentence: Technology changes society.', 15; ...
    'Imagine saying the sentence: Preparation facilitates action.', 16 ...
});
end

% ----------------------------------------------------------------------------
% FUNCTION: buildStimulusGroup
% ----------------------------------------------------------------------------
% Processes raw stimulus text and creates structured stimulus objects
% Input: Cell array with {text, index} pairs
% Output: Array of structures with fields: prompt, content
% ----------------------------------------------------------------------------
function group = buildStimulusGroup(cellArray)
count = size(cellArray, 1);
groupTemplate = struct('prompt','', 'content','');
group = repmat(groupTemplate, 1, count);

for i = 1:count
    rawText = string(cellArray{i,1});
    if startsWith(rawText, "Think about ")
        basePrompt = "Think about";
        content    = extractAfter(rawText, "Think about ");
    elseif startsWith(rawText, "Imagine saying the sentence: ")
        basePrompt = "Imagine saying the sentence:";
        content    = extractAfter(rawText, "Imagine saying the sentence: ");
    else
        basePrompt = "";
        content    = rawText;
    end
    group(i).prompt   = char(basePrompt);
    group(i).content  = char(content);
end
end

% ----------------------------------------------------------------------------
% FUNCTION: prepareRunTrials
% ----------------------------------------------------------------------------
% Creates the trial sequence for a run based on:
%   - Run pattern (e.g., 'srrsrsrssr')
%   - Selected stimulus sets
%   - Run number
%
% Returns:
%   trialList    - Array of trial structures ready for presentation
% ----------------------------------------------------------------------------
function trialList = prepareRunTrials(runNumber,runPattern,spontaneousSetNumber,specificSetNumber,stimuliSets)
% Remove spaces from pattern string
patternChars = char(strrep(runPattern, ' ', ''));
numTrials = numel(patternChars);

% Get the stimuli for this run and set
spontaneousItems = stimuliSets.spontaneous(spontaneousSetNumber).runs(runNumber).items;
specificItems    = stimuliSets.specific(specificSetNumber).runs(runNumber).items;

% Initialize counters for tracking which stimulus to use next
spontIdx = 1;
specIdx  = 1;

% Preallocate trial list
emptyTrial = struct('condition','', 'prompt','', 'content','');
trialList  = repmat(emptyTrial, 1, numTrials);

% Build trial list by iterating through pattern
for t = 1:numTrials
    symbol = lower(patternChars(t));
    switch symbol
        case 'r'  % Spontaneous trial
            item = spontaneousItems(spontIdx);
            trialList(t) = struct('condition','spontaneous', 'prompt',item.prompt, 'content',item.content);
            spontIdx = spontIdx + 1;
        case 's'  % Specific trial
            item = specificItems(specIdx);
            trialList(t) = struct('condition','specific', 'prompt',item.prompt, 'content',item.content);
            specIdx = specIdx + 1;
        otherwise
            error('Invalid pattern symbol "%s" in run pattern.', symbol);
    end
end
end

% ----------------------------------------------------------------------------
% FUNCTION: initializeAudioSubsystem
% ----------------------------------------------------------------------------
% Initializes Psychtoolbox audio subsystem and prepares beep sound
% Returns: Structure with audio handle and beep waveform
% ----------------------------------------------------------------------------
function audio = initializeAudioSubsystem(config)
if ~isfield(config, 'audio') || ~config.audio.enabled
    error('Audio configuration is required for this script.');
end

InitializePsychSound;
audioHandle = PsychPortAudio('Open', [], [], 0, config.audio.sampleRate, 1);
beepWave    = MakeBeep(config.audio.frequency, config.audio.duration, config.audio.sampleRate);
if size(beepWave,1) > 1
    beepWave = beepWave';
end
beepWave = config.audio.volume * beepWave;

audio = struct('handle', audioHandle, 'wave', beepWave);
end

% ----------------------------------------------------------------------------
% FUNCTION: releaseAudioSubsystem
% ----------------------------------------------------------------------------
% Closes and releases audio resources
% ----------------------------------------------------------------------------
function releaseAudioSubsystem(audio)
if isfield(audio, 'handle') && ~isempty(audio.handle)
    try
        PsychPortAudio('Stop', audio.handle, 1);
        PsychPortAudio('Close', audio.handle);
    catch
        % Ignore errors during cleanup
    end
end
end

% ----------------------------------------------------------------------------
% IDENTIFIER PARSING FUNCTIONS
% ----------------------------------------------------------------------------
% These functions convert string identifiers (e.g., 'run1') to numeric indices

function runNumber = parseRunIdentifier(runId)
runId = lower(char(runId));
switch runId
    case 'run1'
        runNumber = 1;
    case 'run2'
        runNumber = 2;
    case 'run3'
        runNumber = 3;
    case 'run4'
        runNumber = 4;
    otherwise
        error('Run must be "run1", "run2", "run3", or "run4". Got: %s', runId);
end
end

function setNumber = parseSetIdentifier(setId)
setId = lower(char(setId));
switch setId
    case 'set1'
        setNumber = 1;
    case 'set2'
        setNumber = 2;
    case 'set3'
        setNumber = 3;
    case 'set4'
        setNumber = 4;
    otherwise
        error('Set must be "set1", "set2", "set3", or "set4". Got: %s', setId);
end
end


% ----------------------------------------------------------------------------
% INPUT/OUTPUT FUNCTIONS
% ----------------------------------------------------------------------------

% ----------------------------------------------------------------------------
% FUNCTION: waitWithAbort
% ----------------------------------------------------------------------------
% Waits for specified duration, checking for ESC key to abort
% Used for fixation periods and timing delays
% ----------------------------------------------------------------------------
function waitWithAbort(duration, escapeKey)
if duration <= 0
    return;
end
deadline = GetSecs + duration;
while GetSecs < deadline
    if nargin >= 2 && ~isempty(escapeKey) && escapeKey > 0
        [isDown, ~, keyCode] = KbCheck;
        if isDown && keyCode(escapeKey)
            error('ExperimentAbort:UserEscaped', 'User pressed ESC to abort.');
        end
    end
    remaining = deadline - GetSecs;
    pauseDuration = min(0.01, max(remaining, 0));
    WaitSecs(pauseDuration);
end
end

% ----------------------------------------------------------------------------
% FUNCTION: playAudioCue
% ----------------------------------------------------------------------------
% Plays a beep sound using PsychPortAudio
% Used to mark the start and end of fixation periods
% ----------------------------------------------------------------------------
function playAudioCue(audio)
PsychPortAudio('FillBuffer', audio.handle, audio.wave);
PsychPortAudio('Start', audio.handle, 1, 0, 1);
end

% ----------------------------------------------------------------------------
% FUNCTION: presentTrial
% ----------------------------------------------------------------------------
% Main trial presentation function
% Sequence:
%   1. Display stimulus text (prompt + content) for 5 seconds
%   2. Show fixation cross
%   3. Play start beep
%   4. Wait 30 seconds (fixation period)
%   5. Play end beep
% Returns: Structure with timing information
% ----------------------------------------------------------------------------
function trialInfo = presentTrial(window, stimulus, centerX, centerY, config, escapeKey, audio)

% Display stimulus text (two lines: prompt and content)
Screen('FillRect', window, config.colors.backgroundNormalized);

% Set font sizes
Screen('TextSize', window, config.text.promptSize);
Screen('TextFont', window, config.text.font);
Screen('TextColor', window, config.colors.textNormalized);

% Draw prompt line (first line, larger size)
% Calculate spacing based on font size to avoid overlap
lineSpacing = config.text.promptSize * 1.5;  % Spacing between lines
promptY = centerY - lineSpacing;
DrawFormattedText(window, stimulus.prompt, 'center', promptY, config.colors.textNormalized, [], [], [], 1.5);

% Draw content line (second line, bold)
Screen('TextSize', window, config.text.contentSize);
Screen('TextStyle', window, 1);  % 1 = bold
contentY = centerY + lineSpacing * 0.5;  % Position below center with spacing
DrawFormattedText(window, stimulus.content, 'center', contentY, config.colors.textNormalized, [], [], [], 1.5);
Screen('TextStyle', window, 0);  % 0 = normal (reset to normal style)

Screen('Flip', window);

% Record prompt onset time
trialInfo = struct();
trialInfo.startTime = GetSecs;

% Wait for 5 seconds (stimulus presentation time)
waitWithAbort(config.timings.prompt, escapeKey);

% Display fixation cross (red for thinking period)
Screen('FillRect', window, config.colors.backgroundNormalized);
Screen('TextSize', window, config.text.baseSize);
drawFixationCross(window, centerX, centerY, config, config.colors.redNormalized);
Screen('Flip', window);

% Wait for fixation period (30 seconds) - start beep removed
waitWithAbort(config.timings.postPromptFixation, escapeKey);

% Play end beep and record end time
playAudioCue(audio); 
trialInfo.endTime = GetSecs;
trialInfo.duration = trialInfo.endTime - trialInfo.startTime;
end

% ----------------------------------------------------------------------------
% FUNCTION: applyAlphaOnWhite
% ----------------------------------------------------------------------------
% Applies alpha channel to image, compositing on white background
% Used for PNG images with transparency
% ----------------------------------------------------------------------------
function img = applyAlphaOnWhite(imgData, alphaChannel)
imgData      = double(imgData) / 255;
alphaChannel = double(alphaChannel) / 255;
if ndims(imgData) == 2
    imgData = repmat(imgData, [1, 1, 3]);
end
if ndims(alphaChannel) == 2
    alphaChannel = repmat(alphaChannel, [1, 1, 3]);
end
white = ones(size(imgData));
img = imgData .* alphaChannel + white .* (1 - alphaChannel);
img = uint8(round(img * 255));
end

% ----------------------------------------------------------------------------
% FUNCTION: displayFixation
% ----------------------------------------------------------------------------
% Displays fixation cross for specified duration
% Used for ITI, pre-run, post-run, and mid-run breaks
% ----------------------------------------------------------------------------
function displayFixation(window, centerX, centerY, config, duration, escapeKey)
Screen('FillRect', window, config.colors.backgroundNormalized);
drawFixationCross(window, centerX, centerY, config);
Screen('Flip', window);
waitWithAbort(duration, escapeKey);
end

% ----------------------------------------------------------------------------
% FUNCTION: drawFixationCross
% ----------------------------------------------------------------------------
% Draws a centered fixation cross (horizontal and vertical lines)
% Optional color parameter: if provided, uses that color; otherwise uses default text color
% ----------------------------------------------------------------------------
function drawFixationCross(window, centerX, centerY, config, color)
if nargin < 5
    color = config.colors.textNormalized;  % Default to text color
end
crossSize = 40;
thickness = 5;
shiftedY  = centerY - 36;  % Slightly shifted up
Screen('DrawLine', window, color, ...
    centerX - crossSize, shiftedY, centerX + crossSize, shiftedY, thickness);
Screen('DrawLine', window, color, ...
    centerX, shiftedY - crossSize, centerX, shiftedY + crossSize, thickness);
end

% ----------------------------------------------------------------------------
% FUNCTION: displayAttentionCheck
% ----------------------------------------------------------------------------
% Displays attention check: button image for 2 seconds, then blank for 1 second
% Records key presses during both periods (total 3 seconds)
% Expected response: Key "1" (keyboard, temporary replacement for button box)
% ----------------------------------------------------------------------------
function info = displayAttentionCheck(window, centerX, centerY, config, button1Key, escapeKey)
while KbCheck; end  % Clear keyboard buffer before starting

info = struct('startTime', NaN, 'responded', false, 'responseTime', NaN, 'responseKey', NaN, ...
              'imageOnset', NaN, 'blankOnset', NaN);

% Phase 1: Display button image for 2 seconds
info.startTime = GetSecs;
info.imageOnset = info.startTime;
totalDuration = config.timings.attentionImage + config.timings.attentionBlank;  % Total 3 seconds

% Load and display button image
buttonPath = config.images.button;
if ~isempty(buttonPath) && exist(buttonPath, 'file') == 2
    [imgData, ~, alpha] = imread(buttonPath);
    if ~isempty(alpha)
        imgData = applyAlphaOnWhite(imgData, alpha);
    end
    if ~isa(imgData, 'uint8')
        imgData = im2uint8(imgData);
    end
    imgDims = size(imgData);
    if numel(imgDims) == 2
        imgData = repmat(imgData, [1, 1, 3]);
    elseif imgDims(3) == 4
        imgData = imgData(:, :, 1:3);
    elseif imgDims(3) == 1
        imgData = repmat(imgData, [1, 1, 3]);
    end
    texture = Screen('MakeTexture', window, imgData);
    [imgHeight, imgWidth, ~] = size(imgData);
    windowRect = Screen('Rect', window);
    screenX = windowRect(3) - windowRect(1);
    screenY = windowRect(4) - windowRect(2);
    scale = min(screenX/imgWidth, screenY/imgHeight) * 0.167;  % Scale to ~1/3 of original (1/6 of screen)
    scaledWidth = round(imgWidth * scale);
    scaledHeight = round(imgHeight * scale);
    destRect = [centerX - scaledWidth/2, centerY - scaledHeight/2, ...
                centerX + scaledWidth/2, centerY + scaledHeight/2];
    Screen('FillRect', window, config.colors.backgroundNormalized);
    Screen('DrawTexture', window, texture, [], destRect, [], 0);
    Screen('Flip', window);
else
    % Fallback: text if image not found
    Screen('FillRect', window, config.colors.backgroundNormalized);
    Screen('TextSize', window, config.text.attentionSize);
    DrawFormattedText(window, 'Press the button 1', 'center', 'center', config.colors.textNormalized);
    Screen('Flip', window);
    texture = [];
end

% Monitor for button press during image display (2 seconds)
% Record responses only within the total 3-second window
deadlineImage = info.startTime + config.timings.attentionImage;
deadlineTotal = info.startTime + totalDuration;  % Total 3-second window

while GetSecs <= deadlineImage
    % Check for a response (using KbCheck(-1) to check all devices, like run_eproj_self.m)
    [press, ~, key] = KbCheck(-1);
    if press
        % Check for ESC key to abort
        if escapeKey > 0 && key(escapeKey)
            if ~isempty(texture), Screen('Close', texture); end
            error('ExperimentAbort:UserEscaped', 'User pressed ESC to abort.');
        end
        
        % Check for button 1 key (using find(key) == KbName('1!') like run_eproj_self.m)
        if find(key) == KbName('1!')
            % Record first response time
            if ~info.responded
                info.responded = true;
                info.responseTime = GetSecs - info.startTime;
                info.responseKey = 1;
            end
        end
    end
end

% Phase 2: Blank screen for 1 second
info.blankOnset = GetSecs;
if ~isempty(texture)
    Screen('Close', texture);
end
Screen('FillRect', window, config.colors.backgroundNormalized);
Screen('Flip', window);

% Monitor for button press during blank period (1 second)
% Continue recording responses within the total 3-second window
while GetSecs <= deadlineTotal
    % Check for a response (using KbCheck(-1) to check all devices, like run_eproj_self.m)
    [press, ~, key] = KbCheck(-1);
    if press
        % Check for ESC key to abort
        if escapeKey > 0 && key(escapeKey)
            error('ExperimentAbort:UserEscaped', 'User pressed ESC to abort.');
        end
        
        % Check for button 1 key (using find(key) == KbName('1!') like run_eproj_self.m)
        if find(key) == KbName('1!')
            % Record first response time
            if ~info.responded
                info.responded = true;
                info.responseTime = GetSecs - info.startTime;
                info.responseKey = 1;
            end
        end
    end
end

% Clear any remaining key presses after the 3-second window
% Responses after this point are considered misses
while KbCheck; end

% If no response was recorded, responseKey and responseTime remain NaN
end

