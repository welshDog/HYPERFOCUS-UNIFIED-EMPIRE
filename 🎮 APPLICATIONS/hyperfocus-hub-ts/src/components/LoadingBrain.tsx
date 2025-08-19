import { Brain } from 'lucide-react';

export function LoadingBrain() {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <Brain className="w-12 h-12 animate-pulse text-primary" />
      <p className="text-lg font-medium text-muted-foreground">Loading...</p>
    </div>
  );
}