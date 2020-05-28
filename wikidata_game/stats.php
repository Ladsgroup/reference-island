<?php declare(strict_types=1);

require_once('includes/constants.php');
require_once('includes/setup-db.php');

$all_matches = $countMatches();
$accepted_matches = $countMatches(FLAGS['ACCEPTED']);
$rejected_matches = $countMatches(FLAGS['REJECTED']);
$acceptance_rate = ($accepted_matches * 100) / ($rejected_matches +  $accepted_matches);

include_once('views/stats-page.php');
?>