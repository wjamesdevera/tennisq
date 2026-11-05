import { NextResponse } from "next/server";

export async function POST(
  request: Request,
  { params }: { params: Promise<{ eventId: string }> },
) {
  try {
    const body = await request.json();
    const { eventId } = await params;

    const res = await fetch(
      `${process.env.BACKEND_API_URL}/v1/events/${eventId}/players`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      },
    );

    const data = await res.json();

    if (!res.ok) {
      return NextResponse.json(
        { message: data.message || "Failed to add player to event" },
        { status: res.status },
      );
    }

    return NextResponse.json(data, { status: 201 });
  } catch {
    return NextResponse.json({ message: "Invalid JSON body" }, { status: 500 });
  }
}
