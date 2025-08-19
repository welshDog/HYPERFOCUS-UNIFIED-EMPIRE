import { Palette } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface BackgroundSectionProps {
  backgroundType: 'color' | 'image';
  backgroundValue: string;
  onChange: (type: 'color' | 'image', value: string) => void;
}

export function BackgroundSection({ backgroundType, backgroundValue, onChange }: BackgroundSectionProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Palette className="h-5 w-5" />
        <h3 className="text-lg font-semibold">Background</h3>
      </div>
      <div className="grid gap-4">
        <div className="flex items-center gap-4">
          <Label>
            <input
              type="radio"
              name="background_type"
              value="color"
              checked={backgroundType === 'color'}
              onChange={() => onChange('color', backgroundValue)}
              className="mr-2"
            />
            Color
          </Label>
          <Label>
            <input
              type="radio"
              name="background_type"
              value="image"
              checked={backgroundType === 'image'}
              onChange={() => onChange('image', backgroundValue)}
              className="mr-2"
            />
            Image
          </Label>
        </div>
        {backgroundType === 'color' ? (
          <Input
            type="color"
            value={backgroundValue}
            onChange={(e) => onChange(backgroundType, e.target.value)}
          />
        ) : (
          <Input
            type="url"
            placeholder="Enter image URL"
            value={backgroundValue}
            onChange={(e) => onChange(backgroundType, e.target.value)}
          />
        )}
      </div>
    </div>
  );
}