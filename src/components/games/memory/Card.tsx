import { Card as UICard } from "@/components/ui/card";

interface CardProps {
  emoji: string;
  isFlipped: boolean;
  isMatched: boolean;
  onClick: () => void;
}

export const Card = ({ emoji, isFlipped, isMatched, onClick }: CardProps) => {
  return (
    <UICard
      className={`aspect-square flex items-center justify-center text-3xl cursor-pointer transition-all duration-300 hover:scale-105 ${
        isFlipped || isMatched
          ? "bg-primary text-primary-foreground"
          : "bg-card hover:bg-card/90"
      }`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      aria-label={`Memory card ${isFlipped || isMatched ? emoji : "face down"}`}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          onClick();
        }
      }}
    >
      {isFlipped || isMatched ? emoji : "❓"}
    </UICard>
  );
};