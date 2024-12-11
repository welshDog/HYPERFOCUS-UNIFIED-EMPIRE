import { Brain, Clock, Star } from "lucide-react";

interface CourseCardProps {
  title: string;
  description: string;
  duration: string;
  difficulty: string;
  rating: number;
  imageUrl: string;
}

export function CourseCard({ title, description, duration, difficulty, rating, imageUrl }: CourseCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:animate-card-hover transition-all duration-300">
      <div className="relative h-48">
        <img src={imageUrl} alt={title} className="w-full h-full object-cover" />
        <div className="absolute top-2 right-2 bg-white px-2 py-1 rounded-full text-sm font-medium text-primary">
          {difficulty}
        </div>
      </div>
      
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600 text-sm mb-4">{description}</p>
        
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center">
            <Clock className="w-4 h-4 mr-1" />
            <span>{duration}</span>
          </div>
          <div className="flex items-center">
            <Star className="w-4 h-4 mr-1 text-yellow-400" />
            <span>{rating.toFixed(1)}</span>
          </div>
          <div className="flex items-center">
            <Brain className="w-4 h-4 mr-1 text-primary" />
            <span>+10 XP</span>
          </div>
        </div>
      </div>
    </div>
  );
}