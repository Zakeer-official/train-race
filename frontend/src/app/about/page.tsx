import { ShieldCheck, Database, Radio, Cpu, Activity, AlertCircle } from "lucide-react";
import { fetchProviderHealth } from "@/lib/api";

export const revalidate = 0;

export default async function AboutPage() {
  const providerHealth = await fetchProviderHealth();

  return (
    <div className="max-w-4xl mx-auto py-6 space-y-12">
      <div className="text-center">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-rail-cyan/10 border border-rail-cyan/30 text-rail-cyan text-xs font-bold mb-3">
          <Database className="w-3.5 h-3.5" />
          <span>DATA TRANSPARENCY & METHODOLOGY</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
          About Train Race
        </h1>
        <p className="text-sm text-slate-400 mt-2 max-w-2xl mx-auto">
          How Train Race integrates railway data, computes ETA predictions, and determines head-to-head race leaders.
        </p>
      </div>

      {/* Provider Health Card */}
      <div className="bg-surface-card border border-surface-border rounded-2xl p-6 shadow-xl">
        <div className="flex items-center justify-between pb-4 mb-4 border-b border-surface-border">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-rail-cyan/10 border border-rail-cyan/30 text-rail-cyan rounded-xl">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Active Data Provider Status</h3>
              <p className="text-xs text-slate-400">Current railway telemetry connection health</p>
            </div>
          </div>
          <span className="flex items-center space-x-1.5 px-3 py-1 bg-rail-leader/15 border border-rail-leader/40 text-rail-leader text-xs font-black rounded-lg">
            <span className="w-2 h-2 rounded-full bg-rail-leader animate-ping"></span>
            <span>{providerHealth.status || "OPERATIONAL"}</span>
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="bg-surface/60 border border-surface-border rounded-xl p-3">
            <span className="text-slate-400 block mb-1">Provider Adapter</span>
            <span className="font-bold text-white text-sm">{providerHealth.provider || "Demo Simulation Engine"}</span>
          </div>
          <div className="bg-surface/60 border border-surface-border rounded-xl p-3">
            <span className="text-slate-400 block mb-1">Telemetry Latency</span>
            <span className="font-bold text-rail-cyan text-sm">{providerHealth.latency_ms || 1.5} ms</span>
          </div>
          <div className="bg-surface/60 border border-surface-border rounded-xl p-3">
            <span className="text-slate-400 block mb-1">Feed Type</span>
            <span className="font-bold text-emerald-400 text-sm">
              {providerHealth.is_live ? "Live RapidAPI / NTES" : "High-Fidelity Synthetic Simulation"}
            </span>
          </div>
        </div>
      </div>

      {/* Prediction Hierarchy (Levels 1 to 4) */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-rail-cyan" />
          <span>Multi-Level ETA Calculation Hierarchy</span>
        </h2>
        <p className="text-xs text-slate-400">
          The comparison engine avoids simplistic geographical distance. Trains operate on strict track blocks, interlocking signaling, and varying speed restrictions.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <div className="bg-surface-card border border-rail-cyan/40 rounded-xl p-5">
            <span className="text-[10px] font-black uppercase text-rail-cyan bg-rail-cyan/15 px-2 py-0.5 rounded">
              LEVEL 1: LIVE TELEMETRY
            </span>
            <h4 className="text-base font-bold text-white mt-2">GPS Coordinates & Live Speed</h4>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              When live GPS and speed telemetry are available, remaining travel duration is estimated using dynamic cruising speeds blended with scheduled intermediate halt durations.
            </p>
          </div>

          <div className="bg-surface-card border border-purple-500/40 rounded-xl p-5">
            <span className="text-[10px] font-black uppercase text-purple-400 bg-purple-500/15 px-2 py-0.5 rounded">
              LEVEL 2: STATION SEQUENCE
            </span>
            <h4 className="text-base font-bold text-white mt-2">Station Sequence Physics Model</h4>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              If GPS is temporarily silent, the engine projects remaining distance from the latest reported station halt along the official railway sequence graph.
            </p>
          </div>

          <div className="bg-surface-card border border-surface-border rounded-xl p-5">
            <span className="text-[10px] font-black uppercase text-amber-400 bg-amber-500/15 px-2 py-0.5 rounded">
              LEVEL 3: TIMETABLE BLEND
            </span>
            <h4 className="text-base font-bold text-white mt-2">Scheduled Arrival + Delay</h4>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              Derived by applying the latest observed station departure delay directly against the official destination arrival timetable.
            </p>
          </div>

          <div className="bg-surface-card border border-surface-border rounded-xl p-5">
            <span className="text-[10px] font-black uppercase text-red-400 bg-red-500/15 px-2 py-0.5 rounded">
              LEVEL 4: STALE ALERT
            </span>
            <h4 className="text-base font-bold text-white mt-2">Stale Warning State</h4>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              When telemetry is older than 15 minutes, Train Race displays an explicit stale status rather than falsely portraying trains at stale positions.
            </p>
          </div>
        </div>
      </div>

      {/* Disclaimers & Disclosures */}
      <div className="bg-surface-card border border-surface-border rounded-2xl p-6 text-xs text-slate-400 space-y-3">
        <div className="font-bold text-slate-200 flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 text-rail-amber" />
          <span>Important Passenger Disclaimers</span>
        </div>
        <p className="leading-relaxed">
          1. <strong>Not an Official Portal:</strong> Train Race is an independent analytical application. For official reservation, ticket cancellation, or NTES status, please refer to official Indian Railways portals (e.g., irctc.co.in or enquiry.indianrail.gov.in).
        </p>
        <p className="leading-relaxed">
          2. <strong>Operational Variables:</strong> Unforeseen operational factors such as freight train crossing precedence, track maintenance blocks, signal failures, and adverse weather can dramatically affect final arrival outcomes.
        </p>
      </div>
    </div>
  );
}
