import { useState, useCallback, useEffect } from "react";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";

export const useGameLogic = (userId: string | undefined) => {
  const [gameState, setGameState] = useState<"waiting" | "ready" | "clicked">("waiting");
  const [startTime, setStartTime] = useState<number | null>(null);
  const [reactionTime, setReactionTime] = useState<number | null>(null);
  const [bestTime, setBestTime] = useState<number | null>(null);
  const [message, setMessage] = useState("Click 'Start' to begin!");
  const [timeoutId, setTimeoutId] = useState<NodeJS.Timeout | null>(null);
  const [sessionTimes, setSessionTimes] = useState<number[]>([]);
  const [gameId, setGameId] = useState<string | null>(null);

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

  useEffect(() => {
    const fetchGameId = async () => {
      try {
        const { data, error } = await supabase
          .from('brain_games')
          .select('id')
          .eq('title', 'Reaction Game')
          .maybeSingle();
        
        if (error) throw error;
        if (data) setGameId(data.id);
        else toast.error('Game not found');
      } catch (error) {
        console.error('Error fetching game ID:', error);
        toast.error('Failed to initialize game');
      }
    };

    fetchGameId();
  }, []);

  const startGame = useCallback(() => {
    setGameState("waiting");
    setMessage("Wait for the green color...");
    setReactionTime(null);

    const waitTime = Math.floor(Math.random() * 3000) + 2000;
    const id = setTimeout(() => {
      setGameState("ready");
      setMessage("CLICK NOW!");
      setStartTime(Date.now());
      playSound("ready");
    }, waitTime);
    setTimeoutId(id);
  }, [playSound]);

  const handleClick = useCallback(() => {
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
      
      if (gameId && userId) {
        saveGameProgress(gameId, userId, reaction);
      }
    } else if (gameState === "waiting") {
      setMessage("Too soon! Wait for the green color!");
      if (timeoutId) clearTimeout(timeoutId);
      setGameState("clicked");
      playSound("error");
    }
  }, [gameState, startTime, bestTime, gameId, userId, timeoutId, playSound]);

  const getSessionStats = useCallback(() => {
    if (sessionTimes.length === 0) return { avg: 0, best: 0, total: 0 };
    
    const avg = Math.round(sessionTimes.reduce((a, b) => a + b, 0) / sessionTimes.length);
    const best = Math.min(...sessionTimes);
    
    return { avg, best, total: sessionTimes.length };
  }, [sessionTimes]);

  return {
    gameState,
    message,
    reactionTime,
    bestTime,
    sessionTimes,
    startGame,
    handleClick,
    getSessionStats,
  };
};

const saveGameProgress = async (gameId: string, userId: string, score: number) => {
  try {
    const { error } = await supabase.from("game_sessions").insert({
      user_id: userId,
      game_id: gameId,
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