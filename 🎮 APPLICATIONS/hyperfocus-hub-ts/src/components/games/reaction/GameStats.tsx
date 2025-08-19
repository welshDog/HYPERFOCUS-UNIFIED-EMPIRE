import React from "react";

interface GameStatsProps {
  reactionTime: number | null;
  bestTime: number | null;
  onShowSummary: () => void;
}

export const GameStats = ({ reactionTime, bestTime, onShowSummary }: GameStatsProps) => {
  return (
    <div className="flex justify-between items-center">
      <div className="space-y-1">
        <p className="text-sm font-medium">Current Time</p>
        <p className="text-2xl font-bold">{reactionTime ? `${reactionTime}ms` : "-"}</p>
      </div>
      <div className="space-y-1">
        <p className="text-sm font-medium">Best Time</p>
        <p className="text-2xl font-bold">{bestTime ? `${bestTime}ms` : "-"}</p>
      </div>
      <button
        onClick={onShowSummary}
        className="text-sm text-primary hover:text-primary/80 transition-colors"
      >
        View Session Stats
      </button>
    </div>
  );
};