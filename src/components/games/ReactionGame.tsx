import React, { useState, useEffect, useCallback } from "react";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

export const ReactionGame = () => {
  const [gameState, setGameState] = useState<"waiting" | "ready" | "clicked">("waiting");
  const [startTime, setStartTime] = useState<number | null>(null);
  const [reactionTime, setReactionTime] = useState<number | null>(null);
  const [bestTime, setBestTime] = useState<number | null>(null);
  const [message, setMessage] = useState("Click 'Start' to begin!");
  const [timeoutId, setTimeoutId] = useState<NodeJS.Timeout | null>(null);
  const [sessionTimes, setSessionTimes] = useState<number[]>([]);
  const [showSummary, setShowSummary] = useState(false);
  const { session } = useAuth();

  // Sound effects
  const playSound = useCallback((type: "ready" | "success" | "error") => {
    const frequency = type === "ready" ? 800 : type === "success" ? 1200 : 400;
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = frequency;
    gainNode.gain.value = 0.1;
    
    oscillator.start();
    gainNode.gain.exponentialRampToValueAtTime(0.00001, audioContext.currentTime + 0.1);
    
    setTimeout(() => {
      oscillator.stop();
      audioContext.close();
    }, 100);
  }, []);

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
      playSound("ready");
    }, waitTime);
    setTimeoutId(id);
  };

  const handleClick = () => {
    if (gameState === "ready" && startTime) {
      const reaction = Date.now() - startTime;
      setReactionTime(reaction);
      setGameState("clicked");
      setMessage(`Your reaction time: ${reaction}ms`);
      setSessionTimes(prev => [...prev, reaction]);
      
      if (!bestTime || reaction < bestTime) {
        setBestTime(reaction);
        playSound("success");
      }
      
      saveGameProgress(reaction);
    } else if (gameState === "waiting") {
      setMessage("Too soon! Wait for the green color!");
      if (timeoutId) clearTimeout(timeoutId);
      setGameState("clicked");
      playSound("error");
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

  const getSessionStats = () => {
    if (sessionTimes.length === 0) return { avg: 0, best: 0, total: 0 };
    
    const avg = Math.round(sessionTimes.reduce((a, b) => a + b, 0) / sessionTimes.length);
    const best = Math.min(...sessionTimes);
    
    return { avg, best, total: sessionTimes.length };
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
        <button
          onClick={() => setShowSummary(true)}
          className="text-sm text-primary hover:text-primary/80 transition-colors"
        >
          View Session Stats
        </button>
      </div>

      <Card
        className={`aspect-video flex items-center justify-center cursor-pointer transition-all duration-300 ${
          gameState === "ready"
            ? "bg-primary text-primary-foreground animate-pulse"
            : "bg-card hover:bg-card/90"
        } ${gameState === "clicked" ? "animate-fade-in" : ""}`}
        onClick={gameState === "clicked" ? startGame : handleClick}
      >
        <div className="text-center space-y-4">
          <p className="text-xl font-medium">{message}</p>
          <p className="text-sm text-muted-foreground">
            {gameState === "clicked" ? "Click to play again" : ""}
          </p>
        </div>
      </Card>

      <Dialog open={showSummary} onOpenChange={setShowSummary}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Session Summary</DialogTitle>
            <DialogDescription>
              Your performance in this session:
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Average Time</p>
                <p className="text-2xl font-bold">{getSessionStats().avg}ms</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Best Time</p>
                <p className="text-2xl font-bold">{getSessionStats().best}ms</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-muted-foreground">Games Played</p>
                <p className="text-2xl font-bold">{getSessionStats().total}</p>
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};