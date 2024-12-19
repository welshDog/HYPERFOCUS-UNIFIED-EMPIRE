import React, { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/integrations/supabase/client";
import { toast } from "sonner";

export const MemoryGame = () => {
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

  return (
    <div className="space-y-6 p-4">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold">Memory Game</h2>
        <p className="text-muted-foreground">
          Match all the cards with the least moves possible!
        </p>
      </div>

      <div className="flex justify-between items-center">
        <div className="space-y-1">
          <p className="text-sm font-medium">Moves</p>
          <p className="text-2xl font-bold">{moves}</p>
        </div>
        <div className="space-y-1">
          <p className="text-sm font-medium">Progress</p>
          <Progress value={(matched.length / (cards.length / 2)) * 100} />
        </div>
      </div>

      <div className="grid grid-cols-3 md:grid-cols-4 gap-4">
        {cards.map((card, index) => (
          <Card
            key={index}
            className={`aspect-square flex items-center justify-center text-3xl cursor-pointer transition-all duration-300 hover:scale-105 ${
              flipped.includes(index) || matched.includes(card)
                ? "bg-primary text-primary-foreground"
                : "bg-card hover:bg-card/90"
            }`}
            onClick={() => handleCardClick(index)}
          >
            {flipped.includes(index) || matched.includes(card) ? card : "❓"}
          </Card>
        ))}
      </div>

      {matched.length === cards.length / 2 && (
        <div className="text-center space-y-2">
          <h3 className="text-xl font-bold">Game Complete!</h3>
          <p>Final Score: {score}</p>
        </div>
      )}
    </div>
  );
};