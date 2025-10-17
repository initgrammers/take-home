"use client";

import Link from "next/link";
import { useEffect, useMemo, useState, use } from "react";

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

export default function PayReservationPage({ params }: { params: Promise<{ roomId: string; reservationId: string }> }) {
  const { roomId, reservationId } = use(params);
  const [room, setRoom] = useState<Room | null>(null);
  const [reservation, setReservation] = useState<Reservation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        setLoading(true);
        setError(null);
        const [roomRes, reservationsRes] = await Promise.all([
          fetch(`/api/rooms/${roomId}`, { cache: "no-store" }),
          fetch(`/api/rooms/${roomId}/reservations`, { cache: "no-store" }),
        ]);
        const roomData = await roomRes.json();
        const reservationsData = (await reservationsRes.json()) as Reservation[];
        const found = (reservationsData || []).find((r) => r.id === reservationId) || null;
        if (mounted) {
          setRoom(roomData ?? null);
          setReservation(found);
          if (!found) setError("Reservation not found for this room");
        }
      } catch (e) {
        if (mounted) setError("Failed to load reservation details");
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, [roomId, reservationId]);

  function generateId(): string {
    try {
      if (typeof crypto !== "undefined" && typeof (crypto as any).randomUUID === "function") {
        return (crypto as any).randomUUID();
      }
      const cryptoObj = typeof window !== "undefined" ? window.crypto : undefined;
      if (cryptoObj && typeof cryptoObj.getRandomValues === "function") {
        const bytes = new Uint8Array(16);
        cryptoObj.getRandomValues(bytes);
        bytes[6] = (bytes[6] & 0x0f) | 0x40;
        bytes[8] = (bytes[8] & 0x3f) | 0x80;
        const toHex = (n: number) => n.toString(16).padStart(2, "0");
        const hex = Array.from(bytes, toHex).join("");
        return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
      }
    } catch {}
    const template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx";
    return template.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  const nights = useMemo(() => {
    if (!reservation) return 0;
    const s = new Date(reservation.start_date);
    const e = new Date(reservation.end_date);
    const msDay = 24 * 60 * 60 * 1000;
    const diffDays = Math.max(0, Math.round((e.getTime() - s.getTime()) / msDay));
    return diffDays || 1; // at least 1 night
  }, [reservation]);

  const total = useMemo(() => {
    if (!room) return 0;
    return Math.round((room.price_per_night * nights + Number.EPSILON) * 100) / 100;
  }, [room, nights]);

  async function handlePay() {
    setSubmitting(true);
    setMessage(null);
    setError(null);
    try {
      if (!reservation || !room) throw new Error("Missing reservation or room data");
      if (String(reservation.status).toLowerCase() !== "active") {
        throw new Error("Reservation is not active");
      }
      const payload = {
        id: generateId(),
        reservation_id: reservation.id,
        amount: total,
      };
      const res = await fetch("/api/payments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(err?.detail || "Failed to process payment");
      }
      setMessage("Payment completed successfully");
    } catch (e: any) {
      setError(e.message || "Payment failed");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="p-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Pay reservation</h1>
        <Link href={`/rooms/${roomId}`} className="text-sm text-blue-600">Back</Link>
      </div>

      {loading ? (
        <p className="text-sm text-gray-600">Loading...</p>
      ) : error ? (
        <p className="text-sm text-red-600">{error}</p>
      ) : !reservation ? (
        <p className="text-sm text-gray-600">Reservation not found.</p>
      ) : (
        <div className="grid gap-4 max-w-md">
          <div className="rounded border p-4 bg-white/60">
            <p className="font-medium">{reservation.guest_email}</p>
            <p className="text-xs text-gray-600">
              {new Date(reservation.start_date).toLocaleDateString()} — {new Date(reservation.end_date).toLocaleDateString()}
            </p>
            <p className="text-xs text-gray-700 mt-2">Status: {reservation.status}</p>
          </div>

          <div className="rounded border p-4 bg-white/60">
            <p className="text-sm">Room: {room?.name}</p>
            <p className="text-sm">Price per night: ${room?.price_per_night?.toFixed?.(2) || room?.price_per_night}</p>
            <p className="text-sm">Nights: {nights}</p>
            <p className="text-sm font-semibold">Total: ${total.toFixed(2)}</p>
          </div>

          <button
            onClick={handlePay}
            disabled={submitting || String(reservation.status).toLowerCase() !== "active"}
            className="rounded bg-black text-white px-4 py-2 text-sm disabled:opacity-50"
          >
            {submitting ? "Processing..." : "Pay now"}
          </button>
          {String(reservation.status).toLowerCase() !== "active" && (
            <p className="text-xs text-gray-600">Esta reserva no está activa (posiblemente cancelada). No es posible realizar el pago.</p>
          )}
          {message && <p className="text-sm text-green-600">{message}</p>}
          {error && <p className="text-sm text-red-600">{error}</p>}
          {!message && !error && (
            <p className="text-xs text-gray-600"></p>
          )}
        </div>
      )}
    </main>
  );
}