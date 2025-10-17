"use client";

import { useEffect, useMemo, useState, use } from "react";
import Link from "next/link";


export default function NewReservationPage({ params }: { params: Promise<{ roomId: string }> }) {
  const { roomId } = use(params);
  const [start, setStart] = useState<string>("");
  const [end, setEnd] = useState<string>("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [guestEmail, setGuestEmail] = useState<string>("");

  // Existing ACTIVE reservations to help pick dates and block in calendar
  const [existing, setExisting] = useState<Array<{ start_date: string; end_date: string }>>([]);

  // Helpers para bloquear fechas reservadas
  const stripTime = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const reservedRanges = useMemo(
    () => existing.map((r) => ({ start: stripTime(new Date(r.start_date)), end: stripTime(new Date(r.end_date)) })),
    [existing]
  );
  const doesRangeOverlap = (s: Date, e: Date) => reservedRanges.some(({ start, end }) => !(e < start || s > end));
  const today = stripTime(new Date());

  const canSubmit = useMemo(() => {
    const hasDates = Boolean(start && end);
    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(guestEmail);
    if (!hasDates || !emailValid) return false;
    const s = new Date(start);
    const e = new Date(end);
    if (Number.isNaN(s.getTime()) || Number.isNaN(e.getTime())) return false;
    return !doesRangeOverlap(stripTime(s), stripTime(e));
  }, [start, end, reservedRanges, guestEmail]);

  // Generador de UUID seguro en frontend (fallback si no existe crypto.randomUUID)
  function generateId(): string {
    try {
      if (typeof crypto !== "undefined" && typeof (crypto as any).randomUUID === "function") {
        return (crypto as any).randomUUID();
      }
      const cryptoObj = typeof window !== "undefined" ? window.crypto : undefined;
      if (cryptoObj && typeof cryptoObj.getRandomValues === "function") {
        const bytes = new Uint8Array(16);
        cryptoObj.getRandomValues(bytes);
        // version 4
        bytes[6] = (bytes[6] & 0x0f) | 0x40;
        // variant
        bytes[8] = (bytes[8] & 0x3f) | 0x80;
        const toHex = (n: number) => n.toString(16).padStart(2, "0");
        const hex = Array.from(bytes, toHex).join("");
        return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
      }
    } catch (e) {
      // ignore
    }
    const template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx";
    return template.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === "x" ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  async function handleCreate() {
    setSubmitting(true);
    setError(null);
    setSuccess(null);
    try {
      const payload = {
        id: generateId(),
        room_id: roomId,
        guest_email: guestEmail,
        start_date: start,
        end_date: end,
      };
      const res = await fetch("/api/reservations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(err?.detail || "Failed to create reservation");
      }
      setSuccess("Reservation created successfully");
      // Refresh active reservations list and clear inputs
      await refreshExisting();
      setStart("");
      setEnd("");
      setGuestEmail("");
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  }

  // Fetch ACTIVE reservations for this room
  useEffect(() => {
    (async () => {
      try {
        await refreshExisting();
      } catch {}
    })();
  }, [roomId]);

  function toISODate(d: Date | undefined) {
    if (!d) return "";
    return new Date(d.getFullYear(), d.getMonth(), d.getDate()).toISOString().split("T")[0];
  }

  // Refresca las reservas ACTIVAS del backend para este roomId
  async function refreshExisting() {
    try {
      const res = await fetch(`/api/rooms/${roomId}/reservations`, { cache: "no-store" });
      const data = await res.json();
      setExisting(
        (data || [])
          .filter((r: any) => (r?.status ? String(r.status).toLowerCase() === "active" : true))
          .map((r: any) => ({ start_date: r.start_date, end_date: r.end_date }))
      );
    } catch (e) {
      console.error(e);
    }
  }

  return (
    <main className="p-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">New reservation</h1>
        <Link href={`/rooms/${roomId}`} className="text-sm text-blue-600">Back</Link>
      </div>

      <section className="mb-6">
        <h2 className="font-semibold mb-2">Active reservations</h2>
        {existing.length === 0 ? (
          <p className="text-sm text-gray-600">None.</p>
        ) : (
          <ul className="text-sm text-gray-700 space-y-1">
            {existing.map((r, idx) => (
              <li key={idx}>
                {new Date(r.start_date).toLocaleDateString()} — {new Date(r.end_date).toLocaleDateString()}
              </li>
            ))}
          </ul>
        )}
      </section>

      <div className="grid gap-4 max-w-md">
        <label className="flex flex-col gap-1">
          <span className="text-sm">Guest email</span>
          <input
            type="email"
            value={guestEmail}
            onChange={(e) => setGuestEmail(e.target.value)}
            placeholder="guest@example.com"
            className="border rounded px-2 py-1 text-sm"
          />
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-sm">Start date</span>
          <input
            type="date"
            value={start}
            min={toISODate(today)}
            onChange={(e) => {
              const s = e.target.value;
              setStart(s);
              if (s && end) {
                const sDay = stripTime(new Date(s));
                const eDay = stripTime(new Date(end));
                if (doesRangeOverlap(sDay, eDay)) {
                  setError("El rango seleccionado se solapa con una reserva existente");
                } else {
                  setError(null);
                }
              }
            }}
            className="border rounded px-2 py-1 text-sm"
          />
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-sm">End date</span>
          <input
            type="date"
            value={end}
            min={start || toISODate(today)}
            onChange={(e) => {
              const eVal = e.target.value;
              setEnd(eVal);
              if (start && eVal) {
                const sDay = stripTime(new Date(start));
                const eDay = stripTime(new Date(eVal));
                if (doesRangeOverlap(sDay, eDay)) {
                  setError("El rango seleccionado se solapa con una reserva existente");
                } else {
                  setError(null);
                }
              }
            }}
            className="border rounded px-2 py-1 text-sm"
          />
        </label>

        <div className="text-xs text-gray-600">
          {start && end ? (
            <>Selected: {new Date(start).toLocaleDateString()} — {new Date(end).toLocaleDateString()}</>
          ) : (
            <>Introduce fechas válidas que no se solapen con reservas activas y un correo válido.</>
          )}
        </div>

        <button
          onClick={handleCreate}
          disabled={!canSubmit || submitting}
          className="rounded bg-black text-white px-4 py-2 text-sm disabled:opacity-50"
        >
          {submitting ? "Creating..." : "Create reservation"}
        </button>
        {error && <p className="text-sm text-red-600">{error}</p>}
        {!error && !canSubmit && (start || end) && (
          <p className="text-xs text-gray-600">Selecciona un rango válido que no se solape con reservas existentes.</p>
        )}
        {success && <p className="text-sm text-green-600">{success}</p>}
      </div>
    </main>
  );
}