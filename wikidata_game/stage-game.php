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
    $actions = ['synchronize', 'opened', 'reopened'];

    $branch = $payload->pull_request->head->ref;
    // Check if current branch is a game branch
    $is_game_branch = substr($branch, 0, 5) === 'game-';

    if($payload->action === 'closed'){
        $root = $_SERVER['DOCUMENT_ROOT'];
        $status = NULL;
        $output = [];
        exec('rm ' . $root . 'stage/' . $branch . '-api.php', $output, $status);

        $message = $status === 0 ? $branch . '-api.php was successfully removed' :  'An error occurred while trying to clean ' . $branch . '. Please see ~/error.log for more information.';

        file_put_contents($logfile_path, $datetime_string . ' ' . $message . PHP_EOL, FILE_APPEND);
        exit;
    }

    // If it is not an update to a game branch pull request, exit
    if(!in_array($payload->action, $actions)
        || !$is_game_branch 
        || $payload->pull_request->base->ref != 'master'){
        exit;
    }

    $script_path = '../reference-island/wikidata_game/stage.sh';

    $output = shell_exec($script_path . ' ' . $branch);

    $message = 'Attempting to deploy ' . $payload->pull_request->head->sha . ' of ' . $payload->pull_request->head->ref . ' to staging environment.' . PHP_EOL;
    $message .= $output ? $output : 'An error occurred while trying to stage ' . $branch . '. Please see ~/error.log for more information.';
    
    file_put_contents($logfile_path, $datetime_string . ' ' . $message . PHP_EOL, FILE_APPEND);
?>