import { TrainLivePerformance } from "@/lib/types";
import { Flag, Train } from "lucide-react";

interface Props {
  train1: TrainLivePerformance;
  train2: TrainLivePerformance;
  destinationName: string;
  destinationCode: string;
}

export default function ProgressTracker({
  train1,
  train2,
  destinationName,
  destinationCode,
}: Props) {
  // Compute progress percentage based on remaining stops vs total stops to destination
  const getProgressPercent = (train: TrainLivePerformance) => {
    const totalRemaining = train.remaining_distance_km;
    // Approximating total journey slice
    const totalSlice = Math.max(100, totalRemaining + 50);
    const completed = totalSlice - totalRemaining;
    return Math.min(96, Math.max(8, Math.round((completed / totalSlice) * 100)));
  };

  const p1 = getProgressPercent(train1);
  const p2 = getProgressPercent(train2);

  return (
    <div className="bg-surface-card border border-surface-border rounded-2xl p-6 mb-8 shadow-lg">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>Route Trajectory to {destinationName}</span>
          </h3>
          <p className="text-xs text-slate-400">
            Real-time track progress convergence towards common destination station ({destinationCode})
          </p>
        </div>
        <div className="flex items-center space-x-4 text-xs font-semibold">
          <div className="flex items-center space-x-1.5 text-rail-cyan">
            <span className="w-2.5 h-2.5 rounded-full bg-rail-cyan"></span>
            <span>Train {train1.train_number}</span>
          </div>
          <div className="flex items-center space-x-1.5 text-purple-400">
            <span className="w-2.5 h-2.5 rounded-full bg-purple-400"></span>
            <span>Train {train2.train_number}</span>
          </div>
        </div>
      </div>

      {/* Track 1 */}
      <div className="mb-6">
        <div className="flex justify-between text-xs text-slate-400 mb-1.5">
          <span className="font-semibold text-slate-300">
            {train1.current_station_name} ({train1.current_station_code})
          </span>
          <span className="text-rail-cyan font-bold">
            {train1.remaining_distance_km} km remaining
          </span>
        </div>
        <div className="relative w-full h-3 bg-surface rounded-full overflow-visible border border-surface-border">
          <div
            className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-600 to-rail-cyan rounded-full transition-all duration-700"
            style={{ width: `${p1}%` }}
          ></div>
          <div
            className="absolute -top-2 transition-all duration-700 -ml-3 flex flex-col items-center"
            style={{ left: `${p1}%` }}
          >
            <div className="p-1 bg-rail-cyan text-black rounded-full shadow-md shadow-rail-cyan/50">
              <Train className="w-3.5 h-3.5" />
            </div>
            <span className="text-[10px] font-black text-rail-cyan mt-0.5">
              {train1.train_number}
            </span>
          </div>
          {/* Destination Flag */}
          <div className="absolute right-0 -top-2 flex flex-col items-center">
            <div className="p-1 bg-rail-leader text-black rounded-full">
              <Flag className="w-3 h-3" />
            </div>
          </div>
        </div>
      </div>

      {/* Track 2 */}
      <div>
        <div className="flex justify-between text-xs text-slate-400 mb-1.5">
          <span className="font-semibold text-slate-300">
            {train2.current_station_name} ({train2.current_station_code})
          </span>
          <span className="text-purple-400 font-bold">
            {train2.remaining_distance_km} km remaining
          </span>
        </div>
        <div className="relative w-full h-3 bg-surface rounded-full overflow-visible border border-surface-border">
          <div
            className="absolute top-0 left-0 h-full bg-gradient-to-r from-indigo-600 to-purple-400 rounded-full transition-all duration-700"
            style={{ width: `${p2}%` }}
          ></div>
          <div
            className="absolute -top-2 transition-all duration-700 -ml-3 flex flex-col items-center"
            style={{ left: `${p2}%` }}
          >
            <div className="p-1 bg-purple-400 text-black rounded-full shadow-md shadow-purple-400/50">
              <Train className="w-3.5 h-3.5" />
            </div>
            <span className="text-[10px] font-black text-purple-400 mt-0.5">
              {train2.train_number}
            </span>
          </div>
          {/* Destination Flag */}
          <div className="absolute right-0 -top-2 flex flex-col items-center">
            <div className="p-1 bg-rail-leader text-black rounded-full">
              <Flag className="w-3 h-3" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
