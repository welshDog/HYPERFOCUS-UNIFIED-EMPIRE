# Using the ML Strategy in BROski Bot

## What is the ML Strategy?

The Machine Learning strategy uses a pre-trained neural network model to predict price movements and generate trading signals. Unlike traditional indicator-based strategies (RSI, MACD), the ML strategy can detect complex patterns in market data.

## Prerequisites

To use the ML strategy, you need:

1. A pre-trained model file (typically `.h5` format)
2. TensorFlow/Keras libraries installed

## How to Set Up the ML Strategy

When configuring the ML strategy in the setup wizard, you'll see:

```
Note: ML strategy requires a pre-trained model file.
Enter model path [models/prediction_model.h5]:
```

### Options for This Step:

1. **Use the default path** - Press Enter to accept the default path
2. **Specify a custom path** - If you have your own trained model, enter its path

### About the Confidence Threshold

After setting the model path, you'll be asked for a confidence threshold:

```
Enter confidence threshold [0.75]:
```

This value (between 0 and 1) determines how confident the model must be to generate a signal:
- **Higher values** (0.8-0.9): Fewer signals, but potentially more reliable
- **Lower values** (0.6-0.7): More signals, but potentially more false positives
- **Recommended**: Start with 0.75-0.85 and adjust based on performance

## Getting a Pre-trained Model

### Option 1: Create a Sample Model (Recommended for Starters)

Run the provided training script:
```
python train_model.py
```

This will:
1. Download historical price data from MEXC
2. Prepare the data for training
3. Build and train an LSTM neural network
4. Save the model to `models/prediction_model.h5`

### Option 2: Create Your Own Model

If you're familiar with machine learning:
1. Create a model using TensorFlow/Keras
2. Ensure your model outputs a single value between 0-1 (probability)
3. Save it in H5 format
4. Point the bot to your model file

## How the ML Strategy Works

1. **Data Collection**: The bot collects recent price data
2. **Feature Engineering**: Calculates technical indicators from the data
3. **Prediction**: Passes the processed data through the neural network
4. **Signal Generation**:
   - If prediction > confidence_threshold → BUY signal
   - If prediction < (1 - confidence_threshold) → SELL signal

## Performance Considerations

- ML models typically perform best when market conditions are similar to their training data
- The included training script creates a basic model - advanced users may want to build more sophisticated models
- Regular retraining (e.g., monthly) is recommended to adapt to changing market conditions
- Keep an eye on model performance and adjust the confidence threshold as needed

## Requirements

To use the ML strategy, you'll need these Python packages installed:
```
pip install tensorflow scikit-learn pandas numpy matplotlib
