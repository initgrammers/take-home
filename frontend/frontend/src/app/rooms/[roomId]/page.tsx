import Link from "next/link";
import { headers } from "next/headers";

export const dynamic = "force-dynamic";

type Reservation = {
  id: string;
  room_id: string;
  guest_email: string;
  start_date: string;
  end_date: string;
  status: string;
};

type Room = {
  id: string;
  name: string;
  price_per_night: number;
};

async function getBaseUrl() {
  const h = await headers();
  const host = h.get("host") ?? "localhost:3000";
  const proto = h.get("x-forwarded-proto") ?? "http";
  return `${proto}://${host}`;
}

async function fetchReservations(roomId: string) {
  try {
      const base = await getBaseUrl();
      const res = await fetch(`${base}/api/rooms/${roomId}/reservations`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch reservations");
    return (await res.json()) as Reservation[];
  } catch (e) {
    console.error(e);
    return [] as Reservation[];
  }
}

async function fetchRoom(roomId: string) {
  try {
      const base = await getBaseUrl();
      const res = await fetch(`${base}/api/rooms/${roomId}`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch room");
    return (await res.json()) as Room;
  } catch (e) {
    console.error(e);
    return null as unknown as Room;
  }
}

export default async function RoomReservationsPage({ params }: { params: Promise<{ roomId: string }> }) {
  const { roomId } = await params;
  const [room, reservations] = await Promise.all([fetchRoom(roomId), fetchReservations(roomId)]);
  const roomName = room?.name ?? roomId;

  return (
    <main className="p-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Reservations for {roomName}</h1>
        <Link
          href={`/rooms/${roomId}/new-reservation`}
          className="rounded bg-black text-white px-4 py-2 text-sm hover:bg-gray-800"
        >
          New reservation
        </Link>
      </div>

      {reservations.length === 0 ? (
        <p className="text-sm text-gray-600">No reservations found for this room.</p>
      ) : (
        <div className="grid gap-4">
          {reservations.map((r) => (
            <div key={r.id}>
              {String(r.status).toLowerCase() === "active" ? (
                <Link
                  href={`/rooms/${roomId}/reservations/${r.id}/pay`}
                  className="rounded border p-4 bg-white/60 block hover:bg-white"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">{r.guest_email}</p>
                      <p className="text-xs text-gray-600">
                        {new Date(r.start_date).toLocaleDateString()} — {new Date(r.end_date).toLocaleDateString()}
                      </p>
                    </div>
                    <span className="text-xs uppercase tracking-wide text-gray-700">{r.status}</span>
                  </div>
                </Link>
              ) : (
                <div className="rounded border p-4 bg-white/60">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">{r.guest_email}</p>
                      <p className="text-xs text-gray-600">
                        {new Date(r.start_date).toLocaleDateString()} — {new Date(r.end_date).toLocaleDateString()}
                      </p>
                    </div>
                    <span className="text-xs uppercase tracking-wide text-gray-700">{r.status}</span>
                  </div>
                  <p className="mt-2 text-xs text-gray-500">Not available (reservation not active)</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </main>
  );
}