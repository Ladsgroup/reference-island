<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reference Treasure Hunt - Game Stats</title>
</head>
<body>
    <h1>Reference Treasure Hunt - Game Stats</h1>
    <h2>Total Matches</h2>
    <ul>
        <li>
            <strong># Matches Total</strong>: <?php echo $all_matches ?>
        </li>
        <li>
            <strong># Accepted Matches</strong>: <?php echo $accepted_matches ?>
        </li>
        <li>
            <strong># Rejected Matches</strong>: <?php echo $rejected_matches ?>
        </li>
        <li>
            <strong>Rejected : Accepted Ratio</strong>: 1 : <?php echo ($accepted_matches / $rejected_matches) ?>
        </li>
    </ul>
</body>
</html>