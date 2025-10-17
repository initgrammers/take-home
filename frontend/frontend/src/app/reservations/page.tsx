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
};

async function getBaseUrl() {
  const h = await headers();
  const host = h.get("host") ?? "localhost:3000";
  const proto = h.get("x-forwarded-proto") ?? "http";
  return `${proto}://${host}`;
}

async function fetchAllReservations(): Promise<Reservation[]> {
  try {
    const base = await getBaseUrl();
    const res = await fetch(`${base}/api/reservations`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch reservations");
    return (await res.json()) as Reservation[];
  } catch (e) {
    console.error(e);
    return [];
  }
}

async function fetchRoom(roomId: string): Promise<Room | null> {
  try {
    const base = await getBaseUrl();
    const res = await fetch(`${base}/api/rooms/${roomId}`, { cache: "no-store" });
    if (!res.ok) return null;
    return (await res.json()) as Room;
  } catch {
    return null;
  }
}

export default async function AllReservationsPage() {
  const reservations = await fetchAllReservations();
  const uniqueRoomIds = Array.from(new Set(reservations.map((r) => r.room_id)));
  const roomsMap = new Map<string, Room | null>();
  await Promise.all(
    uniqueRoomIds.map(async (rid) => {
      const room = await fetchRoom(rid);
      roomsMap.set(rid, room);
    })
  );

  return (
    <main className="p-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">All reservations</h1>
        <Link href="/rooms" className="text-sm text-blue-600">Back to Rooms</Link>
      </div>

      {reservations.length === 0 ? (
        <p className="text-sm text-gray-600">No hay reservas.</p>
      ) : (
        <div className="grid gap-4">
          {reservations.map((r) => {
            const room = roomsMap.get(r.room_id);
            return (
              <div key={r.id} className="rounded border p-4 bg-white/60">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{r.guest_email}</p>
                    <p className="text-xs text-gray-600">
                      {new Date(r.start_date).toLocaleDateString()} — {new Date(r.end_date).toLocaleDateString()}
                    </p>
                    <p className="text-xs text-gray-700 mt-1">Room: {room?.name || r.room_id}</p>
                  </div>
                  <span className="text-xs uppercase tracking-wide text-gray-700">{r.status}</span>
                </div>
                <div className="mt-3 flex gap-2">
                  <Link href={`/rooms/${r.room_id}`} className="text-xs text-blue-600">See room</Link>
                  {String(r.status).toLowerCase() === "active" ? (
                    <Link href={`/rooms/${r.room_id}/reservations/${r.id}/pay`} className="text-xs text-blue-600">Pay</Link>
                  ) : (
                    <span className="text-xs text-gray-500">Not available (reservation not active)</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </main>
  );
}