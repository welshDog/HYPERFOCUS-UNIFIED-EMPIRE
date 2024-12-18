import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

interface CodeEditorProps {
  initialHtml?: string;
  initialCss?: string;
  onSave: (html: string, css: string) => void;
}

export function CodeEditor({ initialHtml = '', initialCss = '', onSave }: CodeEditorProps) {
  const [html, setHtml] = useState(initialHtml);
  const [css, setCss] = useState(initialCss);

  const handleSave = () => {
    try {
      onSave(html, css);
      toast.success("Code changes saved successfully");
    } catch (error) {
      console.error("Error saving code:", error);
      toast.error("Failed to save code changes");
    }
  };

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Label>Custom HTML</Label>
        <Textarea
          value={html}
          onChange={(e) => setHtml(e.target.value)}
          placeholder="Enter your custom HTML..."
          className="font-mono min-h-[200px]"
        />
      </div>
      
      <div className="space-y-2">
        <Label>Custom CSS</Label>
        <Textarea
          value={css}
          onChange={(e) => setCss(e.target.value)}
          placeholder="Enter your custom CSS..."
          className="font-mono min-h-[200px]"
        />
      </div>

      <Button onClick={handleSave}>Save Changes</Button>
    </div>
  );
}