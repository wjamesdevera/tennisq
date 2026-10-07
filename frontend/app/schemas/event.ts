interface CreateEvent {
  name: string;
  description?: string;
  date: string;
  maxPlayers: number;
}

interface Event {
  id: number;
  name: string;
  description?: string;
  date: string;
  maxPlayers: number;
  createdAt: string;
  updatedAt: string;
}
