<?php declare(strict_types=1);

function array_has_keys(array $keys, array $arr): bool {
    foreach($keys as $key){
        if(!array_key_exists($key, $arr)){
            return FALSE;
        }
    }

   return TRUE; 
}

function getDb(array $db_cnf): PDO {
    $required_keys = ['user', 'password', 'dbhost', 'dbname'];
    
    if(!array_has_keys($required_keys, $db_cnf)){
        throw new InvalidArgumentException('Database configuration is missing one of the following required keys: ' 
                                            . implode($required_keys, ', '));
    }
    
    $dbhost = $db_cnf['dbhost'];
    $dbname = $db_cnf['dbname'];
    $dbuser = $db_cnf['user'];
    $dbpass = $db_cnf['password'];

    return new PDO('mysql:host=' . $dbhost . ';dbname=' . $dbname . ';charset=utf8', $dbuser, $dbpass);
}

function getMatches(PDO $db, int $flag = -1): array {
    $sql = $flag === -1 ? "SELECT * FROM refs WHERE ref_flag = :flag" : "SELECT * FROM refs";
    $query = $db->prepare($sql);
    
    $query->execute(['flag' => $flag]);
    return $query->fetchAll();
}

function countMatches(PDO $db, int $flag = -1): int {
    $sql = $flag === -1 ? "SELECT COUNT(ref_flag) FROM refs" : "SELECT COUNT(ref_flag) FROM refs WHERE ref_flag = :flag";
    $query = $db->prepare($sql);
    
    $query->execute(['flag' => $flag]);
    return (int)$query->fetchColumn();
}
// GLOBALS
const FLAGS = [
    'PENDING' => 0,
    'ACCEPTED' => 1,
    'REJECTED' => 2
];

$config_dir = getenv('CONFIG_PATH') ? getenv('CONFIG_PATH') : dirname($_SERVER['DOCUMENT_ROOT']);
$mycnf_path = $config_dir . 'replica.my.cnf';
$dbmycnf = parse_ini_file($mycnf_path);
$db = getDb($dbmycnf);

// SCRIPT
$all_matches = countMatches($db);
$accepted_matches = countMatches($db, FLAGS['ACCEPTED']);
$rejected_matches = countMatches($db, FLAGS['REJECTED']);
?>


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
