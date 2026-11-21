import { TrainStopSchema } from "@/lib/types";
import { Clock, MapPin } from "lucide-react";

interface Props {
  train1Number: string;
  train2Number: string;
  stops1: TrainStopSchema[];
  stops2: TrainStopSchema[];
  destinationCode: string;
}

export default function UpcomingStationsTable({
  train1Number,
  train2Number,
  stops1,
  stops2,
  destinationCode,
}: Props) {
  // Up to next 5 stops
  const nextStops1 = stops1.slice(0, 5);
  const nextStops2 = stops2.slice(0, 5);

  return (
    <div className="bg-surface-card border border-surface-border rounded-2xl p-6 mb-8 shadow-lg">
      <div className="mb-4">
        <h3 className="text-base font-bold text-white flex items-center space-x-2">
          <Clock className="w-4 h-4 text-rail-cyan" />
          <span>Upcoming Intermediate Station Comparison</span>
        </h3>
        <p className="text-xs text-slate-400">
          Scheduled vs expected arrival timings for upcoming route milestones
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Train 1 Stops */}
        <div className="bg-surface/50 border border-surface-border rounded-xl p-4">
          <div className="text-xs font-bold text-rail-cyan uppercase tracking-wider mb-3">
            Train {train1Number} Next Halts
          </div>
          <div className="space-y-2.5">
            {nextStops1.length === 0 ? (
              <span className="text-xs text-slate-500">Approaching destination</span>
            ) : (
              nextStops1.map((s, idx) => (
                <div
                  key={idx}
                  className={`flex items-center justify-between p-2 rounded-lg text-xs ${
                    s.station_code === destinationCode
                      ? "bg-rail-leader/15 border border-rail-leader/40 font-bold"
                      : "bg-surface-card border border-surface-border/60"
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    <span className="text-white font-medium">
                      {s.station_name} ({s.station_code})
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-slate-300 font-mono">
                      {s.scheduled_arrival || s.scheduled_departure || "--"}
                    </span>
                    {s.delay_arrival_min > 0 && (
                      <span className="text-[10px] text-rail-amber ml-1.5 font-bold">
                        +{s.delay_arrival_min}m
                      </span>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Train 2 Stops */}
        <div className="bg-surface/50 border border-surface-border rounded-xl p-4">
          <div className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-3">
            Train {train2Number} Next Halts
          </div>
          <div className="space-y-2.5">
            {nextStops2.length === 0 ? (
              <span className="text-xs text-slate-500">Approaching destination</span>
            ) : (
              nextStops2.map((s, idx) => (
                <div
                  key={idx}
                  className={`flex items-center justify-between p-2 rounded-lg text-xs ${
                    s.station_code === destinationCode
                      ? "bg-rail-leader/15 border border-rail-leader/40 font-bold"
                      : "bg-surface-card border border-surface-border/60"
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    <span className="text-white font-medium">
                      {s.station_name} ({s.station_code})
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-slate-300 font-mono">
                      {s.scheduled_arrival || s.scheduled_departure || "--"}
                    </span>
                    {s.delay_arrival_min > 0 && (
                      <span className="text-[10px] text-rail-amber ml-1.5 font-bold">
                        +{s.delay_arrival_min}m
                      </span>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
