import { useMemoryGame } from "@/hooks/useMemoryGame";
import { Card } from "./memory/Card";
import { GameControls } from "./memory/GameControls";

export const MemoryGame = () => {
  const { cards, flipped, matched, moves, score, handleCardClick } = useMemoryGame();

  return (
    <div className="space-y-6 p-4">
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-bold">Memory Game</h2>
        <p className="text-muted-foreground">
          Match all the cards with the least moves possible!
        </p>
      </div>

      <GameControls
        moves={moves}
        progress={(matched.length / (cards.length / 2)) * 100}
      />

      <div className="grid grid-cols-3 md:grid-cols-4 gap-4">
        {cards.map((card, index) => (
          <Card
            key={index}
            emoji={card}
            isFlipped={flipped.includes(index)}
            isMatched={matched.includes(card)}
            onClick={() => handleCardClick(index)}
          />
        ))}
      </div>

      {matched.length === cards.length / 2 && (
        <div className="text-center space-y-2 animate-fade-in">
          <h3 className="text-xl font-bold">Game Complete!</h3>
          <p>Final Score: {score}</p>
        </div>
      )}
    </div>
  );
};