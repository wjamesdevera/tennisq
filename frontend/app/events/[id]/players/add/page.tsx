import CreatePlayerForm from "@/app/components/create_player_form";
import { getEvent } from "@/app/lib/api";
import { notFound } from "next/navigation";

type Props = {
  params: Promise<{ id: string }>;
};

export default async function AddPlayerPage({ params }: Props) {
  const { id } = await params;

  const event = await getEvent(id).catch(() => null);
  if (!event?.data) notFound();

  const { name, date } = event.data;

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="mb-2 flex w-full max-w-5xl flex-col items-center justify-between font-mono text-sm lg:flex">
        <h2 className="text-xl font-bold">Event: {name}</h2>
        <p>Event Date: {new Date(date).toLocaleDateString()}</p>
      </div>
      <CreatePlayerForm id={id} />
    </main>
  );
}
