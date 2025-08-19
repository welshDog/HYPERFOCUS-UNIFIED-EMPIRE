import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

const HeroSection = () => (
  <section 
    className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary to-secondary p-12 mb-12 animate-fade-in"
    role="banner"
    aria-label="Welcome section"
  >
    <motion.div 
      className="relative z-10 max-w-2xl"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6">
        Ready to unlock your full potential?
      </h1>
      <p className="text-xl text-white/90 mb-8 max-w-xl">
        Discover courses tailored to your learning style and boost your cognitive abilities.
      </p>
      <div className="flex flex-wrap gap-4">
        <Button 
          size="lg"
          className="bg-white text-primary hover:bg-gray-100 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 duration-200"
          aria-label="Get started with HyperFocus"
        >
          Get Started
        </Button>
        <Button 
          size="lg"
          variant="outline"
          className="bg-transparent border-white text-white hover:bg-white/10"
          aria-label="Learn more about our courses"
        >
          Learn More
        </Button>
      </div>
    </motion.div>
    
    {/* Decorative elements */}
    <div className="absolute bottom-0 right-0 w-64 h-64 bg-yellow-400 rounded-full -mr-32 -mb-32 blur-3xl opacity-20" />
    <div className="absolute top-0 right-0 w-96 h-96 bg-purple-600 rounded-full -mr-48 -mt-48 blur-3xl opacity-20" />
  </section>
);

export default HeroSection;