<?php
    if(!isset($_SERVER['HTTP_X_GITHUB_EVENT'])){
        exit;
    }

    if($_SERVER['HTTP_X_GITHUB_EVENT'] != 'pull_request'){
        exit;
    }

    $logfile_path = '../logs/staging.log';
    $datetime_string = date('c');

    $payload = json_decode($_POST["payload"]);

    $branch = $payload->pull_request->head->ref;
    // Check if current branch is a game branch
    $is_game_branch = substr($branch, 0, 5) === 'game-';

    // If it is not a merge to master from game branch, exit
    // if($payload->action != 'synchronize'
    //     || !$is_game_branch 
    //     || $payload->pull_request->base->ref != 'master'){

    //     $message = $payload->action . ': ' . $payload->pull_request->base->ref . ': ' . $branch . ': ' . $payload->pull_request->merged;
    //     file_put_contents($logfile_path, $datetime_string . ' ' . $message . PHP_EOL, FILE_APPEND);

    //     exit;
    // }

    $script_path = '../reference-island/wikidata_game/stage.sh';

    $output = shell_exec($script_path . ' ' . $branch);

    $message = 'Attempting to deploy ' . $payload->pull_request->head->sha . ' of ' . $payload->pull_request->head->ref . PHP_EOL;
    $message .= $output ? $output : 'An error occurred while trying to stage' . $branch . '. Please see ~/error.log for more information.';
    
    file_put_contents($logfile_path, $datetime_string . ' ' . $message . PHP_EOL, FILE_APPEND);
?>