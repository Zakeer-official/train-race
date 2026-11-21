"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Compass, Sparkles, AlertCircle, ArrowRight, Check, Search, Train } from "lucide-react";
import { createRace, fetchCommonStations } from "@/lib/api";
import { CommonStationOption } from "@/lib/types";

export default function CreateRacePage() {
  const router = useRouter();

  const [train1, setTrain1] = useState("12656");
  const [train2, setTrain2] = useState("12705");
  const [destination, setDestination] = useState("MABD");

  const [commonStations, setCommonStations] = useState<CommonStationOption[]>([]);
  const [isLoadingStations, setIsLoadingStations] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Dynamic lookup of common stations whenever train numbers are entered
  useEffect(() => {
    if (train1.trim().length >= 4 && train2.trim().length >= 4) {
      let isCurrent = true;
      setIsLoadingStations(true);
      fetchCommonStations(train1.trim(), train2.trim())
        .then((stations) => {
          if (!isCurrent) return;
          setCommonStations(stations);
          if (stations.length > 0) {
            // If current destination is not in common list, select the first one
            const exists = stations.some(
              (s) => s.station_code.toUpperCase() === destination.toUpperCase()
            );
            if (!exists) {
              setDestination(stations[0].station_code);
            }
          }
        })
        .catch(() => {
          if (isCurrent) setCommonStations([]);
        })
        .finally(() => {
          if (isCurrent) setIsLoadingStations(false);
        });

      return () => {
        isCurrent = false;
      };
    }
  }, [train1, train2]);

  const handlePreset = (t1: string, t2: string, dest: string) => {
    setTrain1(t1);
    setTrain2(t2);
    setDestination(dest);
    setErrorMessage(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!train1.trim() || !train2.trim() || !destination.trim()) {
      setErrorMessage("Please specify both train numbers and a common destination.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const race = await createRace(
        train1.trim(),
        train2.trim(),
        destination.trim().toUpperCase()
      );
      router.push(`/race/${race.id}`);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to initiate train race.");
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-6">
      <div className="text-center mb-8">
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-rail-cyan/10 border border-rail-cyan/30 text-rail-cyan text-xs font-bold mb-3">
          <Compass className="w-3.5 h-3.5" />
          <span>RACE CONFIGURATION</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
          Configure a Train Race
        </h1>
        <p className="text-sm text-slate-400 mt-2">
          Select two competing trains and a shared upcoming destination station.
        </p>
      </div>

      {/* Quick Presets */}
      <div className="bg-surface-card border border-surface-border rounded-2xl p-5 mb-8">
        <div className="flex items-center space-x-2 text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">
          <Sparkles className="w-4 h-4 text-rail-cyan" />
          <span>Quick Benchmark Presets</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <button
            type="button"
            onClick={() => handlePreset("12656", "12705", "MABD")}
            className="text-left p-3.5 bg-surface hover:bg-surface-border/50 border border-surface-border rounded-xl transition-all group"
          >
            <div className="flex justify-between items-center text-xs font-bold text-white group-hover:text-rail-cyan">
              <span>Navjeevan vs Gouthami SF</span>
              <span className="text-[10px] text-rail-leader bg-rail-leader/15 px-2 py-0.5 rounded">
                MABD
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">
              12656 & 12705 racing towards Mahbubabad (MABD)
            </p>
          </button>

          <button
            type="button"
            onClick={() => handlePreset("12951", "12953", "NDLS")}
            className="text-left p-3.5 bg-surface hover:bg-surface-border/50 border border-surface-border rounded-xl transition-all group"
          >
            <div className="flex justify-between items-center text-xs font-bold text-white group-hover:text-rail-cyan">
              <span>Mumbai Rajdhani vs August Kranti</span>
              <span className="text-[10px] text-rail-leader bg-rail-leader/15 px-2 py-0.5 rounded">
                NDLS
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">
              12951 & 12953 racing towards New Delhi (NDLS)
            </p>
          </button>
        </div>
      </div>

      {/* Main Configuration Form */}
      <form
        onSubmit={handleSubmit}
        className="bg-surface-card border border-surface-border rounded-2xl p-6 sm:p-8 shadow-xl space-y-6"
      >
        {errorMessage && (
          <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Train 1 Input */}
          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
              Train 1 Number
            </label>
            <div className="relative">
              <input
                type="text"
                value={train1}
                onChange={(e) => setTrain1(e.target.value)}
                placeholder="e.g. 12656"
                className="w-full bg-surface border border-surface-border rounded-xl px-4 py-3 text-white font-mono font-bold focus:outline-none focus:border-rail-cyan transition-colors"
                required
              />
              <Train className="w-4 h-4 text-slate-500 absolute right-3.5 top-3.5" />
            </div>
            <span className="text-[11px] text-slate-500 mt-1 block">
              e.g. 12656 (Navjeevan SF Express)
            </span>
          </div>

          {/* Train 2 Input */}
          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
              Train 2 Number
            </label>
            <div className="relative">
              <input
                type="text"
                value={train2}
                onChange={(e) => setTrain2(e.target.value)}
                placeholder="e.g. 12705"
                className="w-full bg-surface border border-surface-border rounded-xl px-4 py-3 text-white font-mono font-bold focus:outline-none focus:border-purple-400 transition-colors"
                required
              />
              <Train className="w-4 h-4 text-slate-500 absolute right-3.5 top-3.5" />
            </div>
            <span className="text-[11px] text-slate-500 mt-1 block">
              e.g. 12705 (Gouthami SF Express)
            </span>
          </div>
        </div>

        {/* Common Destination Selection */}
        <div>
          <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
            Common Destination Station Code
          </label>
          <div className="relative">
            <input
              type="text"
              value={destination}
              onChange={(e) => setDestination(e.target.value.toUpperCase())}
              placeholder="e.g. MABD"
              className="w-full bg-surface border border-surface-border rounded-xl px-4 py-3 text-white font-mono font-bold focus:outline-none focus:border-rail-leader transition-colors uppercase"
              required
            />
            <Search className="w-4 h-4 text-slate-500 absolute right-3.5 top-3.5" />
          </div>

          {/* Autodetected Common Stations */}
          <div className="mt-3">
            <div className="text-[11px] font-semibold text-slate-400 mb-2 flex items-center justify-between">
              <span>Discovered Common Upcoming Stations:</span>
              {isLoadingStations && (
                <span className="text-rail-cyan animate-pulse">Scanning routes...</span>
              )}
            </div>

            {commonStations.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {commonStations.map((st) => (
                  <button
                    key={st.station_code}
                    type="button"
                    onClick={() => setDestination(st.station_code)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center space-x-1.5 border ${
                      destination.toUpperCase() === st.station_code.toUpperCase()
                        ? "bg-rail-leader text-slate-950 border-rail-leader shadow-md shadow-rail-leader/20"
                        : "bg-surface text-slate-300 border-surface-border hover:border-slate-500"
                    }`}
                  >
                    <span>{st.station_name}</span>
                    <span className="font-mono text-[10px] opacity-80">
                      ({st.station_code})
                    </span>
                    {destination.toUpperCase() === st.station_code.toUpperCase() && (
                      <Check className="w-3.5 h-3.5" />
                    )}
                  </button>
                ))}
              </div>
            ) : (
              <p className="text-[11px] text-slate-500">
                Enter valid train numbers to auto-detect common intersecting route stations.
              </p>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-4 border-t border-surface-border">
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full flex items-center justify-center space-x-2 py-4 px-6 bg-gradient-to-r from-rail-blue to-rail-cyan text-slate-950 font-black text-base rounded-xl hover:opacity-95 transition-all shadow-lg shadow-rail-cyan/20 disabled:opacity-50"
          >
            {isSubmitting ? (
              <span>Initiating Race Telemetry...</span>
            ) : (
              <>
                <span>Launch Live Race</span>
                <ArrowRight className="w-5 h-5 text-slate-950" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
