export async function getPlayers(eventId: string): Promise<GetPlayersResponse> {
  const res = await fetch(
    `${process.env.BACKEND_API_URL}/v1/events/${eventId}/players?limit=100&offset=0`,
    { method: "GET" },
  );
  if (!res.ok) {
    throw new Error("Failed to fetch players");
  }
  return res.json();
}

export async function getEvent(
  eventId: string,
): Promise<{ status: string; data: Event }> {
  const res = await fetch(
    `${process.env.BACKEND_API_URL}/v1/events/${eventId}`,
    {
      method: "GET",
    },
  );
  if (!res.ok) {
    throw new Error("Failed to fetch events");
  }
  return res.json();
}

export async function createEvent(
  eventData: CreateEvent,
): Promise<{ status: string; data: Event }> {
  const res = await fetch("/api/events", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(eventData),
  });
  if (!res.ok) {
    throw new Error("Failed to create event");
  }
  return res.json();
}
