import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";

export const useMemoryGame = () => {
  const [cards, setCards] = useState<string[]>([]);
  const [flipped, setFlipped] = useState<number[]>([]);
  const [matched, setMatched] = useState<string[]>([]);
  const [moves, setMoves] = useState(0);
  const [score, setScore] = useState(0);
  const { session } = useAuth();

  useEffect(() => {
    // Generate random card pairs
    const emojis = ["🧠", "⚡️", "🎯", "🎲", "🔮", "🎪"];
    const shuffled = [...emojis, ...emojis].sort(() => Math.random() - 0.5);
    setCards(shuffled);
  }, []);

  const handleCardClick = (index: number) => {
    if (flipped.length < 2 && !flipped.includes(index)) {
      setFlipped((prev) => [...prev, index]);
    }
  };

  useEffect(() => {
    if (flipped.length === 2) {
      const [first, second] = flipped;
      if (cards[first] === cards[second]) {
        setMatched((prev) => [...prev, cards[first]]);
      }
      setTimeout(() => setFlipped([]), 1000);
      setMoves((prev) => prev + 1);
    }
  }, [flipped, cards]);

  useEffect(() => {
    if (matched.length === cards.length / 2) {
      const finalScore = Math.max(100 - moves * 5, 10);
      setScore(finalScore);
      saveGameProgress(finalScore);
    }
  }, [matched, cards.length, moves]);

  const saveGameProgress = async (finalScore: number) => {
    if (!session?.user) return;

    try {
      const { error } = await supabase.from("game_sessions").insert({
        user_id: session.user.id,
        game_id: "memory-game",
        score: finalScore,
        duration: moves,
      });

      if (error) throw error;
      toast.success("Game progress saved!");
    } catch (error) {
      console.error("Error saving game progress:", error);
      toast.error("Failed to save game progress");
    }
  };

  return {
    cards,
    flipped,
    matched,
    moves,
    score,
    handleCardClick,
  };
};