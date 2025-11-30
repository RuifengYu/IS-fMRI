% STARTUP.M
% This file is automatically executed when MATLAB starts in this directory
% or when you run: startup

fprintf('=== Adding Psychtoolbox to MATLAB Path ===\n');

% Get the current directory (where this script is located)
currentDir = fileparts(mfilename('fullpath'));
ptbPath = fullfile(currentDir, 'Psychtoolbox');

% Check if Psychtoolbox exists
if exist(ptbPath, 'dir')
    % Check if Screen.m exists
    screenFile = fullfile(ptbPath, 'PsychBasic', 'Screen.m');
    if exist(screenFile, 'file')
        % Add to path (only if not already in path)
        if isempty(strfind(path, ptbPath))
            addpath(genpath(ptbPath));
            fprintf('✓ Psychtoolbox added to path\n');
        else
            fprintf('✓ Psychtoolbox already in path\n');
        end
    else
        fprintf('⚠ Warning: Psychtoolbox found but Screen.m not found\n');
    end
else
    fprintf('⚠ Warning: Psychtoolbox directory not found at: %s\n', ptbPath);
end

fprintf('\n');


