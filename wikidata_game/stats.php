<?php declare(strict_types=1);


use ReferenceIsland\MatchesRepository;

require __DIR__ . '/vendor/autoload.php';

require_once('includes/constants.php');
require_once('includes/responses.php');
require_once('includes/setup-db.php');

$matchesRepository = new MatchesRepository($db);

if(isset($_GET['dump']) && $_GET['dump'] === 'rejected'){
    $rejected = $matchesRepository->getMatchesByFlag(FLAGS['REJECTED']);
    csvDumpResponse('rejected-matches', $rejected);
    exit();
}

$total_matches =  $matchesRepository->getMatchesCountByFlag();
$accepted_matches = $matchesRepository->getMatchesCountByFlag(FLAGS['ACCEPTED']);
$rejected_matches = $matchesRepository->getMatchesCountByFlag(FLAGS['REJECTED']);

$total_reviewed = ($rejected_matches +  $accepted_matches);
$acceptance_rate = ($accepted_matches * 100) / $total_reviewed;

include_once('views/stats-page.php');
?>
