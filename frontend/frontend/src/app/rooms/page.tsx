import Link from "next/link";
import { headers } from "next/headers";

export const dynamic = "force-dynamic";

async function getBaseUrl() {
  const h = await headers();
  const host = h.get("host") ?? "localhost:3000";
  const proto = h.get("x-forwarded-proto") ?? "http";
  return `${proto}://${host}`;
}

async function fetchRooms() {
  try {
    const base = await getBaseUrl();
    const res = await fetch(`${base}/api/rooms`, { cache: "no-store" });
    if (!res.ok) throw new Error("Failed to fetch rooms");
    const raw = (await res.json()) as { id: string; name: string; price_per_night: number }[];
    return raw.map((r) => ({ id: r.id, name: r.name, price: r.price_per_night }));
  } catch (e) {
    console.error(e);
    return [] as { id: string; name: string; price: number }[];
  }
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat("es-ES", { style: "currency", currency: "EUR" }).format(value);
}

export default async function RoomsPage() {
  const rooms = await fetchRooms();

  return (
    <main className="p-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Rooms</h1>
        <Link
          href="/reservations"
          className="px-3 py-2 text-sm rounded bg-blue-600 text-white hover:bg-blue-700"
        >
          Show all reservations
        </Link>
      </div>

      {rooms.length === 0 ? (
        <p className="text-sm text-gray-600">There are no rooms available..</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {rooms.map((room) => (
            <div key={room.id} className="rounded border p-4 bg-white/60">
              <h2 className="font-medium">{room.name}</h2>
              <p className="text-sm text-gray-700">{formatCurrency(room.price)}</p>
              <div className="mt-3">
                <Link href={`/rooms/${room.id}`} className="text-sm text-blue-600">
                  See details
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}