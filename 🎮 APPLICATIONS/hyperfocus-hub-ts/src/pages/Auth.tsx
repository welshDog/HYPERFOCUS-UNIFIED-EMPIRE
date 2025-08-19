import { Auth } from "@supabase/auth-ui-react";
import { ThemeSupa } from "@supabase/auth-ui-shared";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/integrations/supabase/client";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export default function AuthPage() {
  const navigate = useNavigate();
  const { session } = useAuth();

  useEffect(() => {
    if (session) {
      console.log("User is authenticated, redirecting to home");
      navigate("/");
    }
  }, [session, navigate]);

  const handleLogin = async () => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: window.location.origin,
        }
      });
      
      if (error) {
        console.error('Error logging in:', error.message);
        toast.error('Failed to login: ' + error.message);
      }
    } catch (error) {
      console.error('Error during login:', error);
      toast.error('An unexpected error occurred during login');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-2xl font-bold text-center mb-8 text-primary">Welcome to Hyperfocus Studios</h1>
        <div className="space-y-6">
          <Auth
            supabaseClient={supabase}
            appearance={{
              theme: ThemeSupa,
              variables: {
                default: {
                  colors: {
                    brand: 'rgb(var(--color-primary))',
                    brandAccent: 'rgb(var(--color-primary))',
                  }
                }
              }
            }}
            theme="light"
            providers={["google"]}
          />
          <div className="text-center">
            <Button 
              onClick={handleLogin}
              className="w-full"
              size="lg"
            >
              Login with Google
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}