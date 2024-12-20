import React, { useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { GameCard } from "./reaction/GameCard";
import { GameStats } from "./reaction/GameStats";
import { GameSummary } from "./reaction/GameSummary";
import { useGameLogic } from "./reaction/useGameLogic";

export const ReactionGame = () => {
  const [showSummary, setShowSummary] = useState(false);
  const { session } = useAuth();
  const {
    gameState,
    message,
    reactionTime,
    bestTime,
    startGame,
    handleClick,
    getSessionStats,
  } = useGameLogic(session?.user?.id);

  return (
    <div className="space-y-6 p-4">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold">Reaction Game</h2>
        <p className="text-muted-foreground">
          Test your reaction speed! Click when the color changes to green.
        </p>
      </div>

      <GameStats
        reactionTime={reactionTime}
        bestTime={bestTime}
        onShowSummary={() => setShowSummary(true)}
      />

      <GameCard
        gameState={gameState}
        message={message}
        onClick={gameState === "clicked" ? startGame : handleClick}
      />

      <GameSummary
        open={showSummary}
        onOpenChange={setShowSummary}
        stats={getSessionStats()}
      />
    </div>
  );
};