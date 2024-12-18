import * as z from "zod"

export const profileFormSchema = z.object({
  background_type: z.enum(["color", "image"]),
  background_value: z.string()
    .min(1, "Background value is required")
    .refine(
      (val) => {
        if (val.startsWith("#")) {
          return /^#[0-9A-F]{6}$/i.test(val)
        }
        return true // Allow any string for image URLs
      },
      {
        message: "Invalid color format",
      }
    ),
  font_family: z.string().min(1, "Font family is required"),
  font_color: z.string()
    .min(1, "Font color is required")
    .regex(/^#[0-9A-F]{6}$/i, "Invalid color format"),
  bio: z.string().max(500, "Bio must be less than 500 characters"),
  mood: z.string().max(100, "Mood must be less than 100 characters"),
  playlist_url: z.string().url("Invalid URL").or(z.literal("")),
  social_links: z.object({
    twitter: z.string().url("Invalid Twitter URL").or(z.literal("")),
    instagram: z.string().url("Invalid Instagram URL").or(z.literal("")),
    github: z.string().url("Invalid GitHub URL").or(z.literal("")),
    myspace: z.string().url("Invalid MySpace URL").or(z.literal(""))
  }),
  custom_html: z.string().optional(),
  custom_css: z.string().optional(),
  layout_template: z.string().optional(),
  connected_accounts: z.record(z.string()).optional(),
  music_collection: z.array(z.string()).optional(),
  profile_stats: z.record(z.unknown()).optional(),
  custom_sections: z.record(z.unknown()).optional()
});

export type ProfileFormValues = z.infer<typeof profileFormSchema>