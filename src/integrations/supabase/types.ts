export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      brain_games: {
        Row: {
          category: string
          created_at: string
          description: string
          difficulty: string
          id: string
          image_url: string
          points: number | null
          title: string
          updated_at: string
        }
        Insert: {
          category: string
          created_at?: string
          description: string
          difficulty: string
          id?: string
          image_url: string
          points?: number | null
          title: string
          updated_at?: string
        }
        Update: {
          category?: string
          created_at?: string
          description?: string
          difficulty?: string
          id?: string
          image_url?: string
          points?: number | null
          title?: string
          updated_at?: string
        }
        Relationships: []
      }
      categories: {
        Row: {
          created_at: string
          description: string | null
          icon: string | null
          id: string
          name: string
        }
        Insert: {
          created_at?: string
          description?: string | null
          icon?: string | null
          id?: string
          name: string
        }
        Update: {
          created_at?: string
          description?: string | null
          icon?: string | null
          id?: string
          name?: string
        }
        Relationships: []
      }
      categories_courses: {
        Row: {
          category_id: string
          course_id: string
        }
        Insert: {
          category_id: string
          course_id: string
        }
        Update: {
          category_id?: string
          course_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "categories_courses_category_id_fkey"
            columns: ["category_id"]
            isOneToOne: false
            referencedRelation: "categories"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "categories_courses_course_id_fkey"
            columns: ["course_id"]
            isOneToOne: false
            referencedRelation: "courses"
            referencedColumns: ["id"]
          },
        ]
      }
      courses: {
        Row: {
          created_at: string
          description: string
          difficulty: string
          duration: string
          id: string
          image_url: string
          rating: number
          title: string
          updated_at: string
        }
        Insert: {
          created_at?: string
          description: string
          difficulty: string
          duration: string
          id?: string
          image_url: string
          rating: number
          title: string
          updated_at?: string
        }
        Update: {
          created_at?: string
          description?: string
          difficulty?: string
          duration?: string
          id?: string
          image_url?: string
          rating?: number
          title?: string
          updated_at?: string
        }
        Relationships: []
      }
      exercises: {
        Row: {
          category: string
          created_at: string
          description: string
          difficulty: string
          id: string
          image_url: string
          points: number
          title: string
          updated_at: string
        }
        Insert: {
          category: string
          created_at?: string
          description: string
          difficulty: string
          id?: string
          image_url: string
          points?: number
          title: string
          updated_at?: string
        }
        Update: {
          category?: string
          created_at?: string
          description?: string
          difficulty?: string
          id?: string
          image_url?: string
          points?: number
          title?: string
          updated_at?: string
        }
        Relationships: []
      }
      focus_sessions: {
        Row: {
          category: string
          created_at: string
          duration: number
          id: string
          notes: string | null
          user_id: string
        }
        Insert: {
          category: string
          created_at?: string
          duration: number
          id?: string
          notes?: string | null
          user_id: string
        }
        Update: {
          category?: string
          created_at?: string
          duration?: number
          id?: string
          notes?: string | null
          user_id?: string
        }
        Relationships: []
      }
      game_sessions: {
        Row: {
          completed_at: string
          created_at: string
          duration: number
          game_id: string
          id: string
          score: number
          user_id: string
        }
        Insert: {
          completed_at?: string
          created_at?: string
          duration: number
          game_id: string
          id?: string
          score?: number
          user_id: string
        }
        Update: {
          completed_at?: string
          created_at?: string
          duration?: number
          game_id?: string
          id?: string
          score?: number
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "game_sessions_game_id_fkey"
            columns: ["game_id"]
            isOneToOne: false
            referencedRelation: "brain_games"
            referencedColumns: ["id"]
          },
        ]
      }
      posts: {
        Row: {
          content: string
          created_at: string
          id: string
          image_url: string | null
          likes: number | null
          updated_at: string
          user_id: string
        }
        Insert: {
          content: string
          created_at?: string
          id?: string
          image_url?: string | null
          likes?: number | null
          updated_at?: string
          user_id: string
        }
        Update: {
          content?: string
          created_at?: string
          id?: string
          image_url?: string | null
          likes?: number | null
          updated_at?: string
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "posts_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
        ]
      }
      profile_addons: {
        Row: {
          category: string
          code: string
          created_at: string
          description: string | null
          id: string
          name: string
          user_id: string
        }
        Insert: {
          category: string
          code: string
          created_at?: string
          description?: string | null
          id?: string
          name: string
          user_id: string
        }
        Update: {
          category?: string
          code?: string
          created_at?: string
          description?: string | null
          id?: string
          name?: string
          user_id?: string
        }
        Relationships: []
      }
      profiles: {
        Row: {
          avatar_url: string | null
          background_type: string | null
          background_value: string | null
          bio: string | null
          connected_accounts: Json | null
          created_at: string
          custom_css: string | null
          custom_html: string | null
          custom_sections: Json | null
          font_color: string | null
          font_family: string | null
          id: string
          layout_config: Json | null
          layout_template: string | null
          mood: string | null
          music_collection: Json | null
          playlist_url: string | null
          profile_stats: Json | null
          social_links: Json | null
          updated_at: string
          username: string | null
        }
        Insert: {
          avatar_url?: string | null
          background_type?: string | null
          background_value?: string | null
          bio?: string | null
          connected_accounts?: Json | null
          created_at?: string
          custom_css?: string | null
          custom_html?: string | null
          custom_sections?: Json | null
          font_color?: string | null
          font_family?: string | null
          id: string
          layout_config?: Json | null
          layout_template?: string | null
          mood?: string | null
          music_collection?: Json | null
          playlist_url?: string | null
          profile_stats?: Json | null
          social_links?: Json | null
          updated_at?: string
          username?: string | null
        }
        Update: {
          avatar_url?: string | null
          background_type?: string | null
          background_value?: string | null
          bio?: string | null
          connected_accounts?: Json | null
          created_at?: string
          custom_css?: string | null
          custom_html?: string | null
          custom_sections?: Json | null
          font_color?: string | null
          font_family?: string | null
          id?: string
          layout_config?: Json | null
          layout_template?: string | null
          mood?: string | null
          music_collection?: Json | null
          playlist_url?: string | null
          profile_stats?: Json | null
          social_links?: Json | null
          updated_at?: string
          username?: string | null
        }
        Relationships: []
      }
      shared_layouts: {
        Row: {
          created_at: string
          css: string
          description: string | null
          html: string | null
          id: string
          name: string
          preview_image_url: string | null
          updated_at: string
          user_id: string
        }
        Insert: {
          created_at?: string
          css: string
          description?: string | null
          html?: string | null
          id?: string
          name: string
          preview_image_url?: string | null
          updated_at?: string
          user_id: string
        }
        Update: {
          created_at?: string
          css?: string
          description?: string | null
          html?: string | null
          id?: string
          name?: string
          preview_image_url?: string | null
          updated_at?: string
          user_id?: string
        }
        Relationships: []
      }
      user_progress: {
        Row: {
          completed_at: string
          course_id: string | null
          exercise_id: string | null
          id: string
          score: number
          user_id: string
        }
        Insert: {
          completed_at?: string
          course_id?: string | null
          exercise_id?: string | null
          id?: string
          score?: number
          user_id: string
        }
        Update: {
          completed_at?: string
          course_id?: string | null
          exercise_id?: string | null
          id?: string
          score?: number
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "user_progress_course_id_fkey"
            columns: ["course_id"]
            isOneToOne: false
            referencedRelation: "courses"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "user_progress_exercise_id_fkey"
            columns: ["exercise_id"]
            isOneToOne: false
            referencedRelation: "exercises"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type PublicSchema = Database[Extract<keyof Database, "public">]

export type Tables<
  PublicTableNameOrOptions extends
    | keyof (PublicSchema["Tables"] & PublicSchema["Views"])
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
        Database[PublicTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
      Database[PublicTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : PublicTableNameOrOptions extends keyof (PublicSchema["Tables"] &
        PublicSchema["Views"])
    ? (PublicSchema["Tables"] &
        PublicSchema["Views"])[PublicTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  PublicEnumNameOrOptions extends
    | keyof PublicSchema["Enums"]
    | { schema: keyof Database },
  EnumName extends PublicEnumNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = PublicEnumNameOrOptions extends { schema: keyof Database }
  ? Database[PublicEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : PublicEnumNameOrOptions extends keyof PublicSchema["Enums"]
    ? PublicSchema["Enums"][PublicEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof PublicSchema["CompositeTypes"]
    | { schema: keyof Database },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof Database
  }
    ? keyof Database[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends { schema: keyof Database }
  ? Database[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof PublicSchema["CompositeTypes"]
    ? PublicSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never
