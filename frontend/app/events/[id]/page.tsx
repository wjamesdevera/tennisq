import EventPlayerTable from "@/app/components/event_player_table";
import { getEvent, getPlayers } from "@/app/lib/api";
import { notFound } from "next/dist/client/components/navigation";
import Link from "next/link";

export default async function EventPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const playerData = await getPlayers(id).catch(() => notFound());
  const eventData = await getEvent(id).catch(() => notFound());
  const players = playerData["data"]["players"].map((player) => ({
    id: player.id,
    name: player.name,
    rank: player.rank,
    gamesWon: player.gamesWon,
    gamesLost: player.gamesLost,
    setsWon: player.setsWon,
    setsLost: player.setsLost,
    matchesPlayed: player.matchesPlayed,
  }));

  const openAddPlayerForm = () => {
    console.log("Add Player button clicked");
  };

  return (
    <>
      <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <div className="max-w-5xl w-full flex flex-col items-center justify-between font-mono text-sm lg:flex mb-2">
          <h2 className="font-bold text-xl">Event: {eventData.data.name}</h2>
          <p>
            Event Date: {new Date(eventData.data.date).toLocaleDateString()}
          </p>
        </div>
        <div className="rounded-lg border border-gray-100 p-4 max-w-5xl w-full flex flex-col items-center justify-between font-mono text-sm lg:flex mb-4">
          <h3 className="font-bold text-lg">Next Match Up</h3>
          <div className="flex flex-row items-center justify-center gap-4 w-full">
            <div className="rounded-lg border border-gray-300 p-4 max-w-5xl w-full flex flex-col items-center justify-between font-mono text-sm lg:flex mb-2">
              <h4 className="font-bold text-lg">Team 1</h4>
              <ul>
                <li>Player Name</li>
                <li>Player Name</li>
              </ul>
            </div>
            <div className="font-bold text-lg">vs</div>
            <div className="rounded-lg border border-gray-300 p-4 max-w-5xl w-full flex flex-col items-center justify-between font-mono text-sm lg:flex mb-2">
              <h4 className="font-bold text-lg">Team 2</h4>
              <ul>
                <li>Player Name</li>
                <li>Player Name</li>
              </ul>
            </div>
          </div>
        </div>
        <div className="p-4 max-w-5xl w-full flex flex-col items-center justify-between font-mono text-sm lg:flex mb-4">
          <Link
            href={`/events/${id}/players/add`}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Add Player
          </Link>
        </div>
        <article className="max-w-5xl w-full flex flex-col items-center justify-between font-mono text-sm lg:flex">
          <EventPlayerTable rows={players} />
        </article>
      </main>
    </>
  );
}
