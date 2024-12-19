import { Sidebar } from "@/components/Sidebar";
import { Card } from "@/components/ui/card";
import { MemoryGame } from "@/components/games/MemoryGame";
import { Brain, Zap, Timer } from "lucide-react";
import { useState } from "react";

export default function Train() {
  const [selectedGame, setSelectedGame] = useState<string | null>(null);

  const games = [
    {
      id: "memory",
      name: "Memory Game",
      description: "Test and improve your memory skills",
      icon: Brain,
    },
    {
      id: "reaction",
      name: "Reaction Game",
      description: "Improve your reaction time",
      icon: Zap,
      comingSoon: true,
    },
    {
      id: "focus",
      name: "Focus Timer",
      description: "Stay focused with Pomodoro technique",
      icon: Timer,
      comingSoon: true,
    },
  ];

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <div className="max-w-6xl mx-auto space-y-8">
          <div className="space-y-2">
            <h1 className="text-4xl font-bold">Brain Training</h1>
            <p className="text-muted-foreground">
              Challenge yourself with brain training exercises
            </p>
          </div>

          {!selectedGame ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {games.map((game) => (
                <Card
                  key={game.id}
                  className={`p-6 space-y-4 cursor-pointer transition-all duration-300 hover:shadow-lg ${
                    game.comingSoon ? "opacity-50" : "hover:scale-105"
                  }`}
                  onClick={() =>
                    !game.comingSoon && setSelectedGame(game.id)
                  }
                >
                  <div className="flex items-center space-x-4">
                    <div className="p-2 bg-primary/10 rounded-lg">
                      <game.icon className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-semibold">{game.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        {game.description}
                      </p>
                    </div>
                  </div>
                  {game.comingSoon && (
                    <span className="text-xs font-medium text-muted-foreground">
                      Coming Soon
                    </span>
                  )}
                </Card>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              <button
                onClick={() => setSelectedGame(null)}
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                ← Back to games
              </button>
              {selectedGame === "memory" && <MemoryGame />}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}