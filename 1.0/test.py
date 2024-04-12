import numpy as np
from matplotlib import pyplot as plt
from tensorflow import keras
import keras
from keras import layers

with open(f"resources/shortdata.csv", 'r') as file:
    data = file.read()

# Prepare data
header = data.split("\n")[0].split(",")
lines = data.split("\n")[1:]
underlying = np.zeros((len(lines),))
raw_data = np.zeros((len(lines), len(header) - 1))

for i, line in enumerate(lines):
    values = [float(x) for x in line.split(",")[1:]]
    underlying[i] = float(values[0])
    raw_data[i, :] = [float(x) for x in values]

# Split data
num_train_samples = int(0.5 * len(raw_data))
num_val_samples = int(0.25 * len(raw_data))
num_test_samples = int(0.25 * len(raw_data))

# Normalize data
mean = raw_data[:num_train_samples].mean(axis=0)
std = raw_data[:num_train_samples].std(axis=0)
raw_data -= mean
raw_data /= std

# Plot data
plt.plot(range(len(underlying)), underlying)
plt.show()
plt.boxplot(raw_data)
plt.show()

batch_size = 100
sampling_rate = 1
sequence_length = 10
delay = 3

train_dataset = keras.utils.timeseries_dataset_from_array(
    data=raw_data[:-delay],
    targets=underlying[delay:],
    sampling_rate=sampling_rate,
    sequence_length=sequence_length,
    shuffle=True,
    batch_size=batch_size,
    end_index=num_train_samples)

val_dataset = keras.utils.timeseries_dataset_from_array(
    data=raw_data[:-delay],
    targets=underlying[delay:],
    sampling_rate=sampling_rate,
    sequence_length=sequence_length,
    shuffle=True,
    batch_size=batch_size,
    start_index=num_train_samples,
    end_index=num_train_samples + num_val_samples)

test_dataset = keras.utils.timeseries_dataset_from_array(
    data=raw_data[:-delay],
    targets=underlying[delay:],
    sampling_rate=sampling_rate,
    sequence_length=sequence_length,
    shuffle=True,
    batch_size=batch_size,
    start_index=num_train_samples + num_val_samples)

for inputs, outputs in train_dataset:
    print("inputs shape:", inputs.shape)
    print("outputs shape:", outputs.shape)

# Define the model architecture
inputs = keras.Input(shape=(sequence_length, raw_data.shape[-1]))
outputs = layers.Dense(1)(layers.Dropout(0.5)(layers.LSTM(32, recurrent_dropout=0.25)(inputs)))

model = keras.Model(inputs, outputs)

# Keep best version of the model during training, and prepare model for training
callbacks = [keras.callbacks.ModelCheckpoint("models/financeLSTM.keras", save_best_only=True)]
model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])

# Train the model
history = model.fit(train_dataset, epochs=10, validation_data=val_dataset, callbacks=callbacks)

# Access the completed model
model = keras.models.load_model("models/financeLSTM.keras")

# Make predictions on the test dataset
predictions = model.predict(test_dataset)

# Denormalize the predictions and actual values
denormalized_predictions = predictions * std[0] + mean[0]
denormalized_actual_values = underlying[-len(predictions):]  # Assuming 'underlying' contains the original actual values

# Plot the training and validation MAE
test_mae = history.history["mae"]
val_mae = history.history["val_mae"]
epochs = range(1, len(test_mae) + 1)

plt.figure()
plt.plot(epochs, test_mae, "r", label="Training MAE")
plt.plot(epochs, val_mae, "b", label="Validation MAE")
plt.title("Training and validation MAE")
plt.legend()
plt.show()
