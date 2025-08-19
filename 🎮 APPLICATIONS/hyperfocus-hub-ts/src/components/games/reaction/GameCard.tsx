import React from "react";
import { Card } from "@/components/ui/card";

interface GameCardProps {
  gameState: "waiting" | "ready" | "clicked";
  message: string;
  onClick: () => void;
}

export const GameCard = ({ gameState, message, onClick }: GameCardProps) => {
  return (
    <Card
      className={`aspect-video flex items-center justify-center cursor-pointer transition-all duration-300 ${
        gameState === "ready"
          ? "bg-primary text-primary-foreground animate-pulse"
          : "bg-card hover:bg-card/90"
      } ${gameState === "clicked" ? "animate-fade-in" : ""}`}
      onClick={onClick}
    >
      <div className="text-center space-y-4">
        <p className="text-xl font-medium">{message}</p>
        <p className="text-sm text-muted-foreground">
          {gameState === "clicked" ? "Click to play again" : ""}
        </p>
      </div>
    </Card>
  );
};