import { Progress } from "@/components/ui/progress";

interface GameControlsProps {
  moves: number;
  progress: number;
}

export const GameControls = ({ moves, progress }: GameControlsProps) => {
  return (
    <div className="flex justify-between items-center">
      <div className="space-y-1">
        <p className="text-sm font-medium">Moves</p>
        <p className="text-2xl font-bold">{moves}</p>
      </div>
      <div className="space-y-1">
        <p className="text-sm font-medium">Progress</p>
        <Progress value={progress} />
      </div>
    </div>
  );
};