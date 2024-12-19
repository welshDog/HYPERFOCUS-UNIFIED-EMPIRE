import React, { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";

export const ReactionGame = () => {
  const [gameState, setGameState] = useState<"waiting" | "ready" | "clicked">("waiting");
  const [startTime, setStartTime] = useState<number | null>(null);
  const [reactionTime, setReactionTime] = useState<number | null>(null);
  const [bestTime, setBestTime] = useState<number | null>(null);
  const [message, setMessage] = useState("Click 'Start' to begin!");
  const [timeoutId, setTimeoutId] = useState<NodeJS.Timeout | null>(null);
  const { session } = useAuth();

  const startGame = () => {
    setGameState("waiting");
    setMessage("Wait for the green color...");
    setReactionTime(null);

    // Random wait time (2-5 seconds)
    const waitTime = Math.floor(Math.random() * 3000) + 2000;
    const id = setTimeout(() => {
      setGameState("ready");
      setMessage("CLICK NOW!");
      setStartTime(Date.now());
    }, waitTime);
    setTimeoutId(id);
  };

  const handleClick = () => {
    if (gameState === "ready" && startTime) {
      const reaction = Date.now() - startTime;
      setReactionTime(reaction);
      setGameState("clicked");
      setMessage(`Your reaction time: ${reaction}ms`);
      
      if (!bestTime || reaction < bestTime) {
        setBestTime(reaction);
      }
      
      saveGameProgress(reaction);
    } else if (gameState === "waiting") {
      setMessage("Too soon! Wait for the green color!");
      if (timeoutId) clearTimeout(timeoutId);
      setGameState("clicked");
    }
  };

  const saveGameProgress = async (score: number) => {
    if (!session?.user) return;

    try {
      const { error } = await supabase.from("game_sessions").insert({
        user_id: session.user.id,
        game_id: "reaction-game",
        score: score,
        duration: score,
      });

      if (error) throw error;
      toast.success("Game progress saved!");
    } catch (error) {
      console.error("Error saving game progress:", error);
      toast.error("Failed to save game progress");
    }
  };

  return (
    <div className="space-y-6 p-4">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold">Reaction Game</h2>
        <p className="text-muted-foreground">
          Test your reaction speed! Click when the color changes to green.
        </p>
      </div>

      <div className="flex justify-between items-center">
        <div className="space-y-1">
          <p className="text-sm font-medium">Current Time</p>
          <p className="text-2xl font-bold">{reactionTime ? `${reactionTime}ms` : "-"}</p>
        </div>
        <div className="space-y-1">
          <p className="text-sm font-medium">Best Time</p>
          <p className="text-2xl font-bold">{bestTime ? `${bestTime}ms` : "-"}</p>
        </div>
      </div>

      <Card
        className={`aspect-video flex items-center justify-center cursor-pointer transition-all duration-300 ${
          gameState === "ready"
            ? "bg-primary text-primary-foreground"
            : "bg-card hover:bg-card/90"
        }`}
        onClick={gameState === "clicked" ? startGame : handleClick}
      >
        <div className="text-center space-y-4">
          <p className="text-xl font-medium">{message}</p>
          <p className="text-sm text-muted-foreground">
            {gameState === "clicked" ? "Click to play again" : ""}
          </p>
        </div>
      </Card>
    </div>
  );
};