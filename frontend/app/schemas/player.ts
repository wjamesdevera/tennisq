interface Player {
  id: number;
  name: string;
  rank: number;
  gamesWon: number;
  gamesLost: number;
  setsWon: number;
  setsLost: number;
  matchesPlayed: number;
  createdAt: string;
  updatedAt: string;
}

interface GetPlayersResponse {
  status: string;
  data: {
    total: number;
    limit: number;
    offset: number;
    players: Player[];
  };
}

interface PlayerTableRow {
  id: number;
  name: string;
  rank: number;
  gamesWon: number;
  gamesLost: number;
  setsWon: number;
  setsLost: number;
  matchesPlayed: number;
}
