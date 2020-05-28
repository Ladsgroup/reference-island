<?php

namespace ReferenceIsland;

use PDO;

class MatchesRepository {
    private $db;

    public function __construct(PDO $db)
    {
        $this->db = $db;
    }

    public function getMatchesByFlag( $flag = -1 ): iterable {
            $sql = $flag !== -1 ? "SELECT * FROM refs WHERE ref_flag = :flag" : "SELECT * FROM refs";
            $query = $this->db->prepare($sql);

            $query->execute(['flag' => $flag]);

            while($row = $query->fetch(PDO::FETCH_ASSOC)){
                yield $row;
            }
    }

    public function getMatchesCountByFlag(int $flag = -1): int {
        $sql = $flag === -1 ? "SELECT COUNT(ref_flag) FROM refs" : "SELECT COUNT(ref_flag) FROM refs WHERE ref_flag = :flag";
        $query = $this->db->prepare($sql);

        $query->execute(['flag' => $flag]);
        return (int)$query->fetchColumn();
    }

}
