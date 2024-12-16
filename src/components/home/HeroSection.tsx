import { Button } from "@/components/ui/button";

export const HeroSection = () => (
  <section className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-primary to-secondary p-8 mb-12 animate-fade-in">
    <div className="relative z-10">
      <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
        Welcome to Hyperfocus Studios
      </h1>
      <p className="text-xl text-white/90 mb-6 max-w-2xl">
        Unlock your brain's full potential with our innovative courses and brain training exercises.
      </p>
      <Button 
        className="bg-white text-primary hover:bg-gray-100 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 duration-200"
      >
        Start Learning
      </Button>
    </div>
    <div className="absolute inset-0 bg-black/10" />
  </section>
);