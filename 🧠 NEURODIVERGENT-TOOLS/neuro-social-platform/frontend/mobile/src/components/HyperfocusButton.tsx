import React from 'react';
import { TouchableOpacity, Text, StyleSheet, Vibration } from 'react-native';
import { useHapticFeedback } from '../hooks/useHapticFeedback';

interface HyperfocusButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'success' | 'dopamine';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  adhdFriendly?: boolean;
}

export const HyperfocusButton: React.FC<HyperfocusButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  adhdFriendly = true
}) => {
  const { triggerHaptic } = useHapticFeedback();

  const handlePress = () => {
    if (adhdFriendly) {
      triggerHaptic('success'); // Dopamine boost!
      Vibration.vibrate(50); // Gentle confirmation
    }
    onPress();
  };

  return (
    <TouchableOpacity
      style={[
        styles.button,
        styles[variant],
        styles[size],
        disabled && styles.disabled
      ]}
      onPress={handlePress}
      disabled={disabled}
      accessible={true}
      accessibilityLabel={title}
      accessibilityHint="Double tap to activate"
    >
      <Text style={[styles.text, styles[`${variant}Text`]]}>{title}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  primary: {
    backgroundColor: '#6366F1', // Calming purple
  },
  secondary: {
    backgroundColor: '#F3F4F6',
    borderWidth: 1,
    borderColor: '#D1D5DB',
  },
  success: {
    backgroundColor: '#10B981', // Dopamine green
  },
  dopamine: {
    backgroundColor: '#F59E0B', // Achievement gold
  },
  small: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    minHeight: 36,
  },
  medium: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    minHeight: 44,
  },
  large: {
    paddingHorizontal: 24,
    paddingVertical: 16,
    minHeight: 52,
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    fontWeight: '600',
    fontSize: 16,
  },
  primaryText: {
    color: '#FFFFFF',
  },
  secondaryText: {
    color: '#374151',
  },
  successText: {
    color: '#FFFFFF',
  },
  dopamineText: {
    color: '#FFFFFF',
  },
});