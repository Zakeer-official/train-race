import { Trophy, Clock, AlertTriangle, ShieldCheck } from "lucide-react";
import { RaceLeaderInfo } from "@/lib/types";

interface Props {
  leader: RaceLeaderInfo;
  destinationName: string;
  destinationCode: string;
}

export default function RaceLeaderBanner({
  leader,
  destinationName,
  destinationCode,
}: Props) {
  if (leader.is_tie) {
    return (
      <div className="w-full bg-surface-card border border-rail-amber/40 rounded-2xl p-5 mb-8 shadow-lg shadow-rail-amber/10 flex flex-col sm:flex-row items-center justify-between">
        <div className="flex items-center space-x-4 mb-3 sm:mb-0">
          <div className="p-3 bg-rail-amber/10 border border-rail-amber/30 rounded-xl text-rail-amber">
            <Clock className="w-8 h-8" />
          </div>
          <div>
            <div className="text-xs uppercase tracking-wider font-bold text-rail-amber">
              Projected Dead Heat
            </div>
            <h2 className="text-xl sm:text-2xl font-black text-white">
              Simultaneous Arrival Predicted
            </h2>
            <p className="text-sm text-slate-300 mt-0.5">
              Both trains are projected to reach {destinationName} ({destinationCode}) at the same time.
            </p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs text-slate-400">ETA Margin</div>
          <div className="text-2xl font-black text-rail-amber">0 min</div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full bg-gradient-to-r from-surface-card via-surface-card to-[#0e2722] border-2 border-rail-leader/50 rounded-2xl p-6 mb-8 shadow-xl shadow-rail-leader/15">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        {/* Left: Trophy and Announcement */}
        <div className="flex items-center space-x-4">
          <div className="p-3.5 bg-rail-leader/15 border border-rail-leader/40 rounded-2xl text-rail-leader shrink-0">
            <Trophy className="w-9 h-9" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-black uppercase tracking-widest text-rail-leader bg-rail-leader/10 border border-rail-leader/30 px-2 py-0.5 rounded-full">
                Predicted Race Leader
              </span>
              <span className="text-xs text-slate-400">Destination: {destinationName} ({destinationCode})</span>
            </div>
            <h1 className="text-xl sm:text-3xl font-extrabold text-white mt-1">
              Train {leader.leader_train_number}{" "}
              <span className="text-slate-300 text-base sm:text-xl font-medium">
                ({leader.leader_train_name})
              </span>
            </h1>
            <p className="text-sm sm:text-base text-emerald-300/90 font-medium mt-1">
              {leader.summary_message}
            </p>
          </div>
        </div>

        {/* Right: Lead Margin Badge */}
        <div className="flex md:flex-col items-center md:items-end justify-between w-full md:w-auto pt-3 md:pt-0 border-t md:border-t-0 border-surface-border">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Lead Advantage
          </span>
          <div className="flex items-baseline space-x-1.5">
            <span className="text-3xl sm:text-4xl font-black text-rail-leader">
              {leader.margin_minutes}
            </span>
            <span className="text-sm font-bold text-slate-300">MIN EARLIER</span>
          </div>
        </div>
      </div>
    </div>
  );
}
