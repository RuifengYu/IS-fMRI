function InnerLang_Practice(subjectId, varargin)
% INNERLANG_PRACTICE
% Practice session for the InnerLang fMRI experiment
%
% INPUT ARGUMENTS (Required):
%   subjectId         - Subject identifier (e.g., 'S001')
%
% OPTIONAL ARGUMENTS (name/value pairs):
%   'SkipSyncTests'     - Skip Psychtoolbox sync tests (default: from config)
%
% EXAMPLE:
%   InnerLang_Practice('S001')

% ============================================================================
% SECTION 1: INPUT VALIDATION AND PARSING
% ============================================================================

arguments
    subjectId {mustBeTextScalar}
end

arguments (Repeating)
    varargin
end

% Parse optional arguments
opts = parseOptionalArguments(varargin{:});

% Load experiment configuration (timings, colors, paths, etc.)
config = getPracticeConfig();

% ============================================================================
% SECTION 2: STIMULUS PREPARATION
% ============================================================================

% Define practice stimuli (fixed order)
practiceStimuli = {
    'Imagine saying the sentence: Change is inevitable.', ...
    'Think about a tradition you value.', ...
    'Imagine saying the sentence: Sequences have order.', ...
    'Think about what you need to feel safe.' ...
};

% Process stimuli into structured format
trials = cell(1, length(practiceStimuli));
for i = 1:length(practiceStimuli)
    rawText = string(practiceStimuli{i});
    if startsWith(rawText, "Think about ")
        basePrompt = "Think about";
        content = extractAfter(rawText, "Think about ");
    elseif startsWith(rawText, "Imagine saying the sentence: ")
        basePrompt = "Imagine saying the sentence:";
        content = extractAfter(rawText, "Imagine saying the sentence: ");
    else
        basePrompt = "";
        content = rawText;
    end
    trials{i} = struct('condition', '', 'prompt', char(basePrompt), 'content', char(content));
end

% ============================================================================
% SECTION 3: PSYCHTOOLBOX INITIALIZATION
% ============================================================================

% Initialize Psychtoolbox with modern color space
PsychDefaultSetup(2);

% Configure vertical blank synchronization (VBL sync)
skipSyncDefault = false;
if isfield(config, 'psychtoolbox') && isfield(config.psychtoolbox, 'skipSyncTests')
    skipSyncDefault = logical(config.psychtoolbox.skipSyncTests);
end
if ~isempty(opts.skipSyncTests)
    skipSyncDefault = logical(opts.skipSyncTests);
end
Screen('Preference', 'SkipSyncTests', double(skipSyncDefault));

% Initialize audio subsystem for beep cues
audio = initializeAudioSubsystem(config);

% Configure Psychtoolbox imaging pipeline
PsychImaging('PrepareConfiguration');
PsychImaging('AddTask', 'General', 'UseRetinaResolution');
PsychImaging('AddTask', 'FinalFormatting', 'UseRetinaResolution');

% Select screen (use highest-numbered screen if not specified)
screenNumber = config.screenNumber;
if isempty(screenNumber)
    screenNumber = max(Screen('Screens'));
end

% Open fullscreen window
[window, windowRect] = PsychImaging('OpenWindow', screenNumber, config.colors.backgroundNormalized);
[centerX, centerY]   = RectCenter(windowRect);

% Configure text properties
Screen('TextFont', window, config.text.font);
Screen('TextSize', window, config.text.baseSize);
Screen('TextColor', window, config.colors.textNormalized);

% Hide mouse cursor and unify keyboard names
HideCursor;
KbName('UnifyKeyNames');
escapeKey = KbName('ESCAPE');
% Use keyboard key '1' instead of button box (temporary)
button1Key = KbName('1');
if button1Key == 0
    button1Key = KbName('1!');  % Alternative key code
end

% ============================================================================
% SECTION 4: DATA STRUCTURE INITIALIZATION
% ============================================================================

% Initialize practice data structure
practiceData = struct();
practiceData.subjectId = char(subjectId);
practiceData.startTimestamp = char(datetime("now", "Format", "yyyy-MM-dd HH:mm:ss"));

% Preallocate trial data structures
timingTemplate = struct('promptOnset', NaN, 'fixationEnd', NaN, 'duration', NaN);
trialTemplate = struct('condition', '', 'prompt', '', 'content', '', 'timing', timingTemplate);
practiceData.trials = repmat(trialTemplate, 1, length(trials));

% Initialize attention check records (one per trial)
practiceData.attentionChecks = struct('afterTrial', {}, 'responded', {}, 'responseKey', {}, 'rt', {}, 'onset', {});

% ============================================================================
% SECTION 5: EXPERIMENT EXECUTION
% ============================================================================

try
    % ------------------------------------------------------------------------
    % 5.1: PRE-PRACTICE SETUP
    % ------------------------------------------------------------------------
    
    % Show "Practice Session" message (5 seconds)
    Screen('FillRect', window, config.colors.backgroundNormalized);
    Screen('TextSize', window, config.text.baseSize);
    Screen('TextFont', window, config.text.font);
    Screen('TextColor', window, config.colors.textNormalized);
    DrawFormattedText(window, 'Practice Session', 'center', 'center', config.colors.textNormalized, [], [], [], 1.5);
    Screen('Flip', window);
    waitWithAbort(5, escapeKey);  % Display for 5 seconds
    
    % Initial fixation period (12 seconds)
    displayFixation(window, centerX, centerY, config, config.timings.runFixation, escapeKey);
    
    % Record practice start time
    practiceStartTime = GetSecs;
    totalTrials = length(trials);

    % ------------------------------------------------------------------------
    % 5.2: MAIN TRIAL LOOP
    % ------------------------------------------------------------------------
    
    for trialIdx = 1:totalTrials
        % Get current stimulus
        stimulus = trials{trialIdx};
        
        % Present trial: show text for 5s, then fixation for 10s
        trialInfo = presentTrial(window, stimulus, centerX, centerY, config, escapeKey, audio);
    
        % Store trial information
        practiceData.trials(trialIdx).condition = stimulus.condition;
        practiceData.trials(trialIdx).prompt = stimulus.prompt;
        practiceData.trials(trialIdx).content = stimulus.content;
    
        % Store timing data (relative to practice start)
        practiceData.trials(trialIdx).timing = struct( ...
            'promptOnset', trialInfo.startTime - practiceStartTime, ...
            'fixationEnd', trialInfo.endTime - practiceStartTime, ...
            'duration', trialInfo.endTime - trialInfo.startTime ...
        );

        % Attention check after EVERY trial (button image 2s, blank 1s)
        attentionInfo = displayAttentionCheck(window, centerX, centerY, config, button1Key, escapeKey);
        practiceData.attentionChecks(end+1) = struct( ...
            'afterTrial', trialIdx, ...
            'responded',  attentionInfo.responded, ...
            'responseKey', attentionInfo.responseKey, ...
            'rt',          attentionInfo.responseTime, ...
            'onset',       attentionInfo.startTime - practiceStartTime ...
        );
    end

    % ------------------------------------------------------------------------
    % 5.3: POST-PRACTICE
    % ------------------------------------------------------------------------
    
    % Final fixation period
    displayFixation(window, centerX, centerY, config, config.timings.runFixation, escapeKey);

    % ------------------------------------------------------------------------
    % 5.4: DATA SAVING
    % ------------------------------------------------------------------------
    
    % Record end timestamp and runtime
    practiceData.endTimestamp = char(datetime("now", "Format", "yyyy-MM-dd HH:mm:ss"));
    practiceData.runtimeSeconds = GetSecs - practiceStartTime;

    % Generate output filename with timestamp
    timestamp = datestr(now, 'yyyymmdd_HHMMSS');
    outputName = sprintf('%s_practice_%s.csv', char(subjectId), timestamp);
    outputPath = fullfile(config.outputDir, outputName);

    % Create output directory if it doesn't exist
    if ~exist(config.outputDir, 'dir')
        mkdir(config.outputDir);
    end

    % Prepare CSV data - create a table with one row per trial
    numTrials = length(practiceData.trials);
    
    % Preallocate arrays for efficiency
    subjectIdCol = repmat({char(subjectId)}, numTrials, 1);
    startTimestampCol = repmat({practiceData.startTimestamp}, numTrials, 1);
    endTimestampCol = repmat({practiceData.endTimestamp}, numTrials, 1);
    trialIndexCol = (1:numTrials)';
    promptCol = cell(numTrials, 1);
    contentCol = cell(numTrials, 1);
    promptOnsetCol = zeros(numTrials, 1);
    fixationEndCol = zeros(numTrials, 1);
    trialDurationCol = zeros(numTrials, 1);
    attentionResponseKeyCol = cell(numTrials, 1);  % '1' for response, 'miss' for no response
    attentionRTCol = nan(numTrials, 1);
    
    for t = 1:numTrials
        trial = practiceData.trials(t);
        attention = practiceData.attentionChecks(t);
        
        promptCol{t} = trial.prompt;
        contentCol{t} = trial.content;
        promptOnsetCol(t) = trial.timing.promptOnset;
        fixationEndCol(t) = trial.timing.fixationEnd;
        trialDurationCol(t) = trial.timing.duration;
        % Store response key: '1' if responded, 'miss' if not
        attentionResponseKeyCol{t} = attention.responseKey;
        attentionRTCol(t) = attention.rt;
    end
    
    % Create table
    csvData = table(subjectIdCol, startTimestampCol, endTimestampCol, ...
        trialIndexCol, promptCol, contentCol, ...
        promptOnsetCol, fixationEndCol, trialDurationCol, ...
        attentionResponseKeyCol, attentionRTCol, ...
        'VariableNames', {'subjectId', 'startTimestamp', 'endTimestamp', ...
        'trialIndex', 'prompt', 'content', ...
        'promptOnset', 'fixationEnd', 'trialDuration', ...
        'attentionResponseKey', 'attentionRT'});
    
    % Write to CSV file
    writetable(csvData, outputPath);

    % ------------------------------------------------------------------------
    % 5.5: CLEANUP
    % ------------------------------------------------------------------------
    
    % Release resources
    releaseAudioSubsystem(audio);
    sca;  % Close all screens
    ShowCursor;
    
    fprintf('Practice session completed. Data saved to %s\n', outputPath);
    fprintf('CSV file contains %d trials with timing data.\n', numTrials);

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
function opts = parseOptionalArguments(varargin)
opts.skipSyncTests = [];

if isempty(varargin)
    return;
end

if mod(numel(varargin), 2) ~= 0
    error('Optional arguments must be provided as name/value pairs.');
end

for idx = 1:2:numel(varargin) 
    name = lower(string(varargin{idx}));
    value = varargin{idx+1};
    switch name
        case "skipsynctests" 
            opts.skipSyncTests = logical(value);
        otherwise
            error('Unknown optional arguments: %s', name);
    end
end
end

% ----------------------------------------------------------------------------
% FUNCTION: getPracticeConfig
% ----------------------------------------------------------------------------
function config = getPracticeConfig()
    config.screenNumber = [];
    config.outputDir = 'data';
    config.psychtoolbox.skipSyncTests = true;
    
    config.colors.background = [255 255 255];
    config.colors.text       = [0 0 0];
    config.colors.backgroundNormalized = config.colors.background / 255;
    config.colors.textNormalized       = config.colors.text / 255;
    
    config.text.font = 'Arial';
    config.text.baseSize = 72;
    config.text.promptSize = 64;
    config.text.contentSize = 72;
    
    config.timings.prompt             = 5;   % Stimulus presentation time
    config.timings.postPromptFixation = 10;  % Thinking period (10 seconds for practice)
    config.timings.runFixation        = 12;  % Pre-practice and post-practice fixation
    config.timings.attentionImage     = 2;   % Attention check image display time
    config.timings.attentionBlank     = 1;   % Attention check blank time
    
    config.text.attentionSize = 108; % Font size for attention check text
    
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
    
    config.audio.enabled    = true;
    config.audio.sampleRate = 44100;
    config.audio.frequency  = 800;
    config.audio.duration   = 0.1;
    config.audio.volume     = 1.0;
end

% ----------------------------------------------------------------------------
% FUNCTION: initializeAudioSubsystem
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
function releaseAudioSubsystem(audio)
PsychPortAudio('Stop', audio.handle, 1);
PsychPortAudio('Close', audio.handle);
end

% ----------------------------------------------------------------------------
% FUNCTION: displayAttentionCheck
% ----------------------------------------------------------------------------
% Displays attention check: button image for 2 seconds, then blank for 1 second
% Records key presses during both periods (total 3 seconds)
% Expected response: Key "1" (keyboard, temporary replacement for button box)
% Returns: Structure with response information
% ----------------------------------------------------------------------------
function info = displayAttentionCheck(window, centerX, centerY, config, button1Key, escapeKey)
while KbCheck; end  % Clear keyboard buffer before starting

info = struct('startTime', NaN, 'responded', false, 'responseTime', NaN, 'responseKey', '', ...
              'imageOnset', NaN, 'blankOnset', NaN);

% Phase 1: Display button image for 2 seconds
info.startTime = GetSecs;  % Start time for reaction time calculation (from button image onset)
info.imageOnset = info.startTime;
totalDuration = config.timings.attentionImage + config.timings.attentionBlank;  % Total 3 seconds (2s image + 1s blank)

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
deadlineImage = info.startTime + config.timings.attentionImage;
deadlineTotal = info.startTime + totalDuration;  % Total 3-second window

while GetSecs < deadlineImage
    currentTime = GetSecs;
    if currentTime <= deadlineTotal
        [isDown, secs, keyCode] = KbCheck;
        if isDown
            if escapeKey > 0 && keyCode(escapeKey)
                if ~isempty(texture), Screen('Close', texture); end
                error('ExperimentAbort:UserEscaped', 'User pressed ESC to abort.');
            end
            % Check for button 1 key (try multiple key codes)
            keyPressed = false;
            if button1Key > 0 && keyCode(button1Key)
                keyPressed = true;
            elseif keyCode(KbName('1!'))
                keyPressed = true;
            elseif keyCode(KbName('1'))
                keyPressed = true;
            end
            
            if keyPressed && ~info.responded && secs <= deadlineTotal
                info.responded = true;
                info.responseTime = secs - info.startTime;
                info.responseKey = '1';
            end
        end
    end
    WaitSecs(0.001);  % Check more frequently
end

% Phase 2: Blank screen for 1 second
info.blankOnset = GetSecs;
if ~isempty(texture)
    Screen('Close', texture);
end
Screen('FillRect', window, config.colors.backgroundNormalized);
Screen('Flip', window);

% Monitor for button press during blank period (1 second)
deadlineBlank = info.blankOnset + config.timings.attentionBlank;
while GetSecs < deadlineBlank
    currentTime = GetSecs;
    if currentTime <= deadlineTotal
        [isDown, secs, keyCode] = KbCheck;
        if isDown
            if escapeKey > 0 && keyCode(escapeKey)
                error('ExperimentAbort:UserEscaped', 'User pressed ESC to abort.');
            end
            % Check for button 1 key (try multiple key codes)
            keyPressed = false;
            if button1Key > 0 && keyCode(button1Key)
                keyPressed = true;
            elseif keyCode(KbName('1!'))
                keyPressed = true;
            elseif keyCode(KbName('1'))
                keyPressed = true;
            end
            
            if keyPressed && ~info.responded && secs <= deadlineTotal
                info.responded = true;
                info.responseTime = secs - info.startTime;
                info.responseKey = '1';
            end
        end
    end
    WaitSecs(0.001);  % Check more frequently
end

% Clear any remaining key presses after the 3-second window
while KbCheck; end

% Mark as miss if no response was recorded within the 3-second window (2s image + 1s blank)
if ~info.responded
    info.responseKey = 'miss';
    % responseTime remains NaN for misses (no response time to record)
end
end

% ----------------------------------------------------------------------------
% FUNCTION: applyAlphaOnWhite
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
% FUNCTION: waitWithAbort
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
function playAudioCue(audio)
PsychPortAudio('FillBuffer', audio.handle, audio.wave);
PsychPortAudio('Start', audio.handle, 1, 0, 1);
end

% ----------------------------------------------------------------------------
% FUNCTION: presentTrial
% ----------------------------------------------------------------------------
function trialInfo = presentTrial(window, stimulus, centerX, centerY, config, escapeKey, audio)

% Display stimulus text (two lines: prompt and content)
Screen('FillRect', window, config.colors.backgroundNormalized);

% Set font sizes
Screen('TextSize', window, config.text.promptSize);
Screen('TextFont', window, config.text.font);
Screen('TextColor', window, config.colors.textNormalized);

% Draw prompt line (first line, larger size)
lineSpacing = config.text.promptSize * 1.5;
promptY = centerY - lineSpacing;
DrawFormattedText(window, stimulus.prompt, 'center', promptY, config.colors.textNormalized, [], [], [], 1.5);

% Draw content line (second line, bold)
Screen('TextSize', window, config.text.contentSize);
Screen('TextStyle', window, 1);  % 1 = bold
contentY = centerY + lineSpacing * 0.5;
DrawFormattedText(window, stimulus.content, 'center', contentY, config.colors.textNormalized, [], [], [], 1.5);
Screen('TextStyle', window, 0);  % 0 = normal (reset to normal style)

Screen('Flip', window);

% Record prompt onset time
trialInfo = struct();
trialInfo.startTime = GetSecs;

% Wait for 5 seconds (stimulus presentation time)
waitWithAbort(config.timings.prompt, escapeKey);

% Display fixation cross
Screen('FillRect', window, config.colors.backgroundNormalized);
Screen('TextSize', window, config.text.baseSize);
drawFixationCross(window, centerX, centerY, config);
Screen('Flip', window);

% Play start beep and wait for fixation period (10 seconds for practice)
playAudioCue(audio);
waitWithAbort(config.timings.postPromptFixation, escapeKey);

% Play end beep and record end time
playAudioCue(audio); 
trialInfo.endTime = GetSecs;
trialInfo.duration = trialInfo.endTime - trialInfo.startTime;
end

% ----------------------------------------------------------------------------
% FUNCTION: displayFixation
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
function drawFixationCross(window, centerX, centerY, config)
crossSize = 40;
thickness = 5;
shiftedY  = centerY - 36;  % Slightly shifted up
Screen('DrawLine', window, config.colors.textNormalized, ...
    centerX - crossSize, shiftedY, centerX + crossSize, shiftedY, thickness);
Screen('DrawLine', window, config.colors.textNormalized, ...
    centerX, shiftedY - crossSize, centerX, shiftedY + crossSize, thickness);
end

