import React from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";

interface GameSummaryProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  stats: {
    avg: number;
    best: number;
    total: number;
  };
}

export const GameSummary = ({ open, onOpenChange, stats }: GameSummaryProps) => {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Session Summary</DialogTitle>
          <DialogDescription>Your performance in this session:</DialogDescription>
        </DialogHeader>
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-sm text-muted-foreground">Average Time</p>
              <p className="text-2xl font-bold">{stats.avg}ms</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-muted-foreground">Best Time</p>
              <p className="text-2xl font-bold">{stats.best}ms</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-muted-foreground">Games Played</p>
              <p className="text-2xl font-bold">{stats.total}</p>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};