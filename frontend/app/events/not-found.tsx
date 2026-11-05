import Link from "next/link";
export default async function EventNotFoundPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="max-w-5xl w-full flex flex-col items-center justify-between font-mono text-sm lg:flex mb-2">
        <h2 className="font-bold text-xl">Event Not Found</h2>
        <p>The event you are looking for does not exist.</p>
        <Link href="/" className="text-blue-500 hover:underline">
          Go back to Home Page
        </Link>
      </div>
    </main>
  );
}
