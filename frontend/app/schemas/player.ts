interface Player {
  id: number;
  name: string;
  rank: number;
  games_won: number;
  games_lost: number;
  sets_won: number;
  sets_lost: number;
  matches_played: number;
  created_at: string;
  updated_at: string;
}

interface PlayerTableRow {
  id: number;
  name: string;
  rank: number;
  games_won: number;
  games_lost: number;
  sets_won: number;
  sets_lost: number;
  matches_played: number;
}
