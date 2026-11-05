import { getEvent } from "../lib/api";
import { redirect } from "next/navigation";

export default async function EventPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const eventData = await getEvent(id);
  if (!eventData) {
    return <div>Event not found</div>;
  }

  const openAddPlayerForm = () => {
    console.log("Add Player button clicked");
  };
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="max-w-5xl w-full flex flex-col items-center justify-between font-mono text-sm lg:flex mb-2">
        <h2 className="font-bold text-xl">Event: {eventData.data.name}</h2>
        <p>Event Date: {new Date(eventData.data.date).toLocaleDateString()}</p>
      </div>
    </main>
  );
}
