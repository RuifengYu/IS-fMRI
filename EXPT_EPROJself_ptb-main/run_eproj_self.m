function run_eproj_self(subj_id, run_num)
%
% PTB implementation of Lauren DiNicola's EPROJ DMN-A localizer
% By Sam Hutchinson for Kanwisher Lab 1/10/25
% Based on Buckner lab python code, edited by Evlab
%
% Participants are instructed to read a 3-4 line question and 3 potential
% responses and choose the best response, taking care to consider each
% option
%
% The questions will be about the participants themselves, either:
% 1) their present self
% 2) their future self
% 3) their past self
%
% DMN-A contrast is 2&3 > 1
%
% TIMING INFO:
%
% (14 x 5 sec fix) + (15 x 10 sec stim) + (2x12 fixation at start and end) = 244 seconds
% If TR = 2sec, IPS = 122
%

sca;
clc;

TRIGGER_UTIL_DIR = [pwd filesep 'TOOL_Matlab_trigger_utils'];
addpath(TRIGGER_UTIL_DIR);

%set these
full_window = 1;
in_scanner = 1;

%experiment parameters
block_len = 10; %seconds
fix_len = 12;
isi_len = 5;

%these also have a fixation at beginning, end, and between each
% so each run has 15 stim blocks, 16 fix blocks
designs = [1 2 1 3 1 1 2 3 2 2 1 3 3 2 3
           2 1 3 1 1 3 2 2 1 1 2 3 3 3 2
           2 2 1 1 1 3 1 2 2 3 2 3 3 3 2
           1 1 3 2 2 3 3 1 1 3 2 1 2 3 2
           3 2 1 2 3 2 1 3 3 3 1 1 2 1 2
           1 2 2 1 1 2 3 3 3 2 3 2 3 1 1];

designs_actual = [0 1 0 2 0 1 0 3 0 1 0 1 0 2 0 3 0 2 0 2 0 1 0 3 0 3 0 2 0 3 0
                  0 2 0 1 0 3 0 1 0 1 0 3 0 2 0 2 0 1 0 1 0 2 0 3 0 3 0 3 0 2 0
                  0 2 0 2 0 1 0 1 0 1 0 3 0 1 0 2 0 2 0 3 0 2 0 3 0 3 0 3 0 2 0
                  0 1 0 1 0 3 0 2 0 2 0 3 0 3 0 1 0 1 0 3 0 2 0 1 0 2 0 3 0 2 0
                  0 3 0 2 0 1 0 2 0 3 0 2 0 1 0 3 0 3 0 3 0 1 0 1 0 2 0 1 0 2 0
                  0 1 0 2 0 2 0 1 0 1 0 2 0 3 0 3 0 3 0 2 0 3 0 2 0 3 0 1 0 1 0];

run_design = designs_actual(run_num, :);
num_blocks = length(run_design);

%open stim file
file_name = ['./Supporting_Files/Spreadsheets/Eproj_Scan_Run' num2str(run_num) '.xlsx'];
stim_table = readtable(file_name);


%initialzie PTB
fprintf('Initializing PsychToolbox...\n');
Screen('Preference', 'Verbosity', 0);
Screen('Preference', 'SkipSyncTests', 1);
Screen('Preference', 'VisualDebugLevel', 0);
Screen('Preference', 'SuppressAllWarnings', 1);

%open log text file
logtext = fopen(['./logs/' subj_id '_run' num2str(run_num) '_log.txt'], 'w');

%set keys for scanner
KbName('UnifyKeyNames'); %to ensure cross-computer compatibility
% trigger_key = KbName('=+');

%opens the PTB window, pass 1 for full window or 0 for a small window
[window, windowRect, windowData] = make_window(full_window);
[x0 y0] = RectCenter(windowRect);   % Screen center.
if full_window == 1
    HideCursor;
end

%wait for scanning trigger

DrawFormattedText(window, 'Waiting for scanner trigger...', 'center', 'center');
% img = imread('./Supporting_Files/Screens/EPROJ.png');
% imgTexture = Screen('MakeTexture', window, img);
% Screen('DrawTexture', window, imgTexture);

Screen('Flip', window);
% if in_scanner == 1
%     KbName('UnifyKeyNames');
%     go = 0;
%     while go == 0
%         [touch, ~, key_code] = KbCheck(-1);
%         WaitSecs(0.0001);
%         if touch && key_code(trigger_key)
%             go = 1;
%         end
%     end
% else
%     WaitSecs(2);+
% end

run_start_time = wait_for_trigger_kbqueue_all_dvc;

Screen('Flip', window);

%main experiment loop
%set timing variables to measure latency
% experiment_start = GetSecs;
experiment_start = run_start_time;

cpu_time = experiment_start;
real_time = 0;
num_stims = 0;
for block_idx = 1:num_blocks

    block_type = run_design(block_idx);

    %log precise info about timing
    block_start = GetSecs;
    log.block(block_idx).block_start = GetSecs - experiment_start;
    log.block(block_idx).block_type = block_type;

    if block_type == 0 %fixation

        if block_idx == 1 || block_idx == num_blocks

            correction_time = GetSecs - cpu_time;
            real_time = real_time + fix_len + correction_time;
            cpu_time = cpu_time + fix_len + correction_time;

        else

            correction_time = GetSecs - cpu_time;
            real_time = real_time + isi_len + correction_time;
            cpu_time = cpu_time + isi_len + correction_time;
            
        end


        %draws fixation at center
        draw_fix(window, windowData.xCent, windowData.yCent, 0, 0);

        waittime = cpu_time - GetSecs;
        WaitSecs(waittime);
        %while GetSecs <= cpu_time
        %end
        Screen('Flip', window);

        %log timing info
        log.block(block_idx).block_len = GetSecs - block_start;
        log.block(block_idx).block_end = real_time;

    else %stim blocks

        num_stims = num_stims + 1;
        trial_text_raw = stim_table(num_stims, 3).Question{1,1};

        %format trial text
        trial_text = '';
        trial_parts = strsplit(trial_text_raw, '\n');
        for pid=1:length(trial_parts)

            part = trial_parts{pid};
            part = strip(part);
            part = regexprep(part, ' +', ' ');
            part = [part '\n'];
            trial_text = [trial_text part];

        end
        trial_text = strrep(trial_text, ':\n(', ':\n\n(');
        trial_text = strip(trial_text);

        correction_time = GetSecs - cpu_time;
        real_time = real_time + block_len + correction_time;
        cpu_time = cpu_time + block_len + correction_time;

        %show text
        Screen(window,'TextSize',30);
        DrawFormattedText(window, trial_text, 'center', 'center', [255], 50, [], [], 1.5);
        Screen('Flip', window);
        fprintf(['Trial (type' (num2str(block_type)) '): ' trial_text]);
        fprintf(logtext, '%s\n', ['Trial (type' (num2str(block_type)) '): ' trial_text]);

        %monitor keys
        user_ans = [];
        trial_rt = 0;
        while GetSecs <= cpu_time
            %check for a response
            [press, ~, key] = KbCheck(-1);
            if press

                if trial_rt == 0
                    trial_rt = GetSecs() - block_start;
                end

                if find(key) == KbName('1!')
                    user_ans(end+1) = find(key);
                elseif find(key) == KbName('2@')
                    user_ans(end+1) = find(key);
                elseif find(key) == KbName('3#')
                    user_ans(end+1) = find(key);
                end
            end
        end

        %log response
        if isempty(user_ans)
            log.block(block_idx).answer = 0;
            fprintf('No press')
            fprintf(logtext, '%s\n', ['No press']);

        elseif user_ans(end) == KbName('1!')
            log.block(block_idx).answer = 1;
            fprintf('Pressed 1')
            fprintf(logtext, '%s\n', ['Pressed 1']);

        elseif user_ans(end) == KbName('2@')
            log.block(block_idx).answer = 2;
            fprintf('Pressed 2')
            fprintf(logtext, '%s\n', ['Pressed 2']);
        
        elseif user_ans(end) == KbName('3#')
            log.block(block_idx).answer = 3;
            fprintf('Pressed 3')
            fprintf(logtext, '%s\n', ['Pressed 3']);
        end

        fprintf(['Trial RT: ' num2str(trial_rt)]);
        fprintf(logtext, '%s\n', ['Trial RT: ' num2str(trial_rt)]);
        log.block(block_idx).rt = trial_rt;

        %log timing info
        log.block(block_idx).block_len = GetSecs - block_start;
        log.block(block_idx).block_end = real_time;

        %save all expt info
        save(sprintf('./logs/log_%s_%s.mat', subj_id, int2str(run_num)), 'log');

    end

end

%save all expt info,  %save out para file with onset, condition, duration
save(sprintf('./logs/log_%s_%s.mat', subj_id, int2str(run_num)), 'log');
fclose(logtext);

block_onsets = round([log.block(:).block_start]', 1);
block_types = [log.block(:).block_type]';
block_durs = round([log.block(:).block_len]', 1);
T1 = table(block_onsets, block_types, block_durs, 'VariableNames', {'Onset', 'Condition', 'Duration'});
para_name1 = sprintf('./paras/%s_%s_eproj.para', subj_id, int2str(run_num));
writetable(T1, para_name1, 'FileType', 'text', 'Delimiter', 'tab', 'WriteVariableNames', false);


%close the screen and print done
sca;
fprintf('Run %s done!', int2str(run_num))

end

