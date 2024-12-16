import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

interface FontSectionProps {
  fontFamily: string;
  fontColor: string;
  onFontFamilyChange: (value: string) => void;
  onFontColorChange: (value: string) => void;
}

export function FontSection({ fontFamily, fontColor, onFontFamilyChange, onFontColorChange }: FontSectionProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <span className="text-lg">Aa</span>
        <h3 className="text-lg font-semibold">Font Settings</h3>
      </div>
      <div className="grid gap-4">
        <div>
          <Label>Font Family</Label>
          <select
            className="w-full p-2 border rounded-md"
            value={fontFamily}
            onChange={(e) => onFontFamilyChange(e.target.value)}
          >
            <option value="Inter">Inter</option>
            <option value="Arial">Arial</option>
            <option value="Times New Roman">Times New Roman</option>
            <option value="Comic Sans MS">Comic Sans MS</option>
          </select>
        </div>
        <div>
          <Label>Font Color</Label>
          <Input
            type="color"
            value={fontColor}
            onChange={(e) => onFontColorChange(e.target.value)}
          />
        </div>
      </div>
    </div>
  );
}