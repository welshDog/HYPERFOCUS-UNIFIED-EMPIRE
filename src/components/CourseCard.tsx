import { Clock, Star, User } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface CourseCardProps {
  title: string;
  description: string;
  duration: string;
  difficulty: string;
  rating: number;
  image_url: string;
  instructor?: string;
  topics?: string[];
}

export function CourseCard({
  title,
  description,
  duration,
  difficulty,
  rating,
  image_url,
  instructor = "Expert Instructor",
  topics = ["Focus", "Memory"],
}: CourseCardProps) {
  return (
    <Card className="group overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
      <div className="relative aspect-video overflow-hidden">
        <img
          src={image_url}
          alt={`Cover image for ${title}`}
          className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
        />
        <Badge
          variant="secondary"
          className="absolute right-2 top-2 bg-white/90 dark:bg-gray-900/90"
        >
          {difficulty}
        </Badge>
      </div>
      
      <CardHeader className="space-y-2">
        <CardTitle className="line-clamp-1 text-lg">{title}</CardTitle>
        <CardDescription className="line-clamp-2">{description}</CardDescription>
      </CardHeader>
      
      <CardContent>
        <div className="grid gap-4">
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <User className="h-4 w-4" />
              <span>{instructor}</span>
            </div>
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span>{duration}</span>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <div className="flex items-center">
              <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
              <span className="ml-1 text-sm font-medium">{rating.toFixed(1)}</span>
            </div>
            {topics.map((topic) => (
              <Badge key={topic} variant="outline" className="text-xs">
                {topic}
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}