import Link from "next/link";
import { Zap, Compass, Trophy, TrendingDown, Radio, ArrowRight, ShieldCheck } from "lucide-react";
import { fetchRecentRaces } from "@/lib/api";

export const revalidate = 0;

export default async function LandingPage() {
  const recentRaces = await fetchRecentRaces();

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center pt-8 pb-12 max-w-4xl mx-auto">
        <div className="inline-flex items-center space-x-2 bg-rail-cyan/10 border border-rail-cyan/30 text-rail-cyan text-xs font-bold px-3 py-1 rounded-full mb-6">
          <Zap className="w-3.5 h-3.5" />
          <span>REAL-TIME DUAL TRAIN PREDICTION PLATFORM</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white leading-tight">
          Don&apos;t just track trains. <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-rail-cyan via-blue-400 to-rail-leader">
            Predict who reaches first.
          </span>
        </h1>

        <p className="mt-6 text-base sm:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
          The real-time Indian Railway head-to-head comparison engine. Track two trains simultaneously towards a common destination, analyze delay propagation, and predict the exact arrival gap.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/create"
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-8 py-4 bg-gradient-to-r from-rail-blue to-rail-cyan text-slate-950 font-extrabold text-base rounded-xl hover:opacity-95 transition-all shadow-lg shadow-rail-cyan/25 group"
          >
            <Compass className="w-5 h-5 text-slate-950 group-hover:rotate-45 transition-transform" />
            <span>Start a Live Race</span>
          </Link>
          <Link
            href="/about"
            className="w-full sm:w-auto inline-flex items-center justify-center space-x-2 px-6 py-4 bg-surface-card border border-surface-border text-slate-200 font-bold text-base rounded-xl hover:bg-surface-border/50 transition-colors"
          >
            <span>Prediction Methodology</span>
          </Link>
        </div>
      </section>

      {/* Featured Example Hero Preview Card */}
      <section className="bg-gradient-to-b from-surface-card to-surface border border-surface-border rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
          <Zap className="w-96 h-96 text-rail-cyan" />
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 mb-6 border-b border-surface-border">
          <div>
            <span className="text-xs font-bold text-rail-cyan uppercase tracking-wider">
              Featured Head-to-Head Comparison
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">
              Navjeevan SF (12656) vs Gouthami SF (12705)
            </h2>
            <p className="text-sm text-slate-400">
              Racing towards common destination: <strong className="text-white">Mahbubabad (MABD)</strong>
            </p>
          </div>
          <div className="mt-4 sm:mt-0">
            <span className="inline-flex items-center space-x-2 px-3 py-1.5 bg-rail-leader/15 border border-rail-leader/40 text-rail-leader text-xs font-black rounded-lg">
              <Trophy className="w-4 h-4" />
              <span>12656 Predicted Leader (+24m margin)</span>
            </span>
          </div>
        </div>

        {/* Comparison Preview Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-surface/80 border border-rail-leader/40 rounded-2xl p-5">
            <div className="flex justify-between items-start mb-3">
              <div>
                <span className="text-xs font-extrabold text-rail-leader bg-rail-leader/15 px-2 py-0.5 rounded">
                  LEADER
                </span>
                <h3 className="text-xl font-black text-white mt-1">Train 12656</h3>
                <p className="text-xs text-slate-400">Navjeevan Superfast Express</p>
              </div>
              <div className="text-right">
                <span className="text-xs text-slate-400">Predicted ETA</span>
                <div className="text-2xl font-black text-rail-leader">02:32</div>
              </div>
            </div>
            <div className="text-xs text-slate-300 space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-400">Current Position:</span>
                <span className="font-semibold">Warangal (WL) • 82 km/h</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Delay:</span>
                <span className="text-yellow-400 font-semibold">+18 min (Recovering)</span>
              </div>
            </div>
          </div>

          <div className="bg-surface/80 border border-surface-border rounded-2xl p-5">
            <div className="flex justify-between items-start mb-3">
              <div>
                <span className="text-xs font-bold text-slate-400 bg-surface px-2 py-0.5 rounded">
                  CHASING
                </span>
                <h3 className="text-xl font-black text-white mt-1">Train 12705</h3>
                <p className="text-xs text-slate-400">Gouthami Superfast Express</p>
              </div>
              <div className="text-right">
                <span className="text-xs text-slate-400">Predicted ETA</span>
                <div className="text-2xl font-black text-white">02:56</div>
              </div>
            </div>
            <div className="text-xs text-slate-300 space-y-1">
              <div className="flex justify-between">
                <span className="text-slate-400">Current Position:</span>
                <span className="font-semibold">Kazipet (KZJ) • 74 km/h</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Delay:</span>
                <span className="text-slate-300 font-semibold">+7 min (Steady)</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <Link
            href="/create"
            className="inline-flex items-center space-x-1.5 text-sm font-bold text-rail-cyan hover:underline"
          >
            <span>Launch this race or configure your own</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* Product Principles Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-surface-card border border-surface-border rounded-2xl p-6">
          <div className="p-3 bg-rail-cyan/10 border border-rail-cyan/30 text-rail-cyan rounded-xl w-fit mb-4">
            <Radio className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Simultaneous Tracking</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Eliminates constant app-switching. View both trains side by side on desktop and stacked seamlessly on mobile devices.
          </p>
        </div>

        <div className="bg-surface-card border border-surface-border rounded-2xl p-6">
          <div className="p-3 bg-rail-leader/10 border border-rail-leader/30 text-rail-leader rounded-xl w-fit mb-4">
            <TrendingDown className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Multi-Level ETA Engine</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Separates timetable schedules, live telemetry speed, intermediate halt durations, and observed delay propagation for transparent arrival forecasts.
          </p>
        </div>

        <div className="bg-surface-card border border-surface-border rounded-2xl p-6">
          <div className="p-3 bg-purple-500/10 border border-purple-500/30 text-purple-400 rounded-xl w-fit mb-4">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Frictionless Public Sharing</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Generate unique race links that family or co-passengers can open instantly via WhatsApp without logins, app downloads, or configuration.
          </p>
        </div>
      </section>

      {/* Recent Races Section */}
      {recentRaces.length > 0 && (
        <section className="space-y-4">
          <h3 className="text-xl font-extrabold text-white">Recently Created Races</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {recentRaces.map((r) => (
              <Link
                key={r.id}
                href={`/race/${r.id}`}
                className="bg-surface-card border border-surface-border hover:border-rail-cyan/50 rounded-xl p-4 transition-all block group"
              >
                <div className="flex justify-between items-center text-xs text-slate-400 mb-2">
                  <span>Race ID: {r.id}</span>
                  <span className="text-[10px] font-bold text-rail-leader bg-rail-leader/15 px-2 py-0.5 rounded">
                    ACTIVE
                  </span>
                </div>
                <div className="font-extrabold text-white text-base group-hover:text-rail-cyan transition-colors">
                  {r.train1_number} vs {r.train2_number}
                </div>
                <div className="text-xs text-slate-400 mt-1">
                  Towards Destination: <strong className="text-slate-200">{r.destination_station_code}</strong>
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
