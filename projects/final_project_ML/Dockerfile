# Use the official Python image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
# COPY . /app
COPY app.py /app/
COPY data/train_pivot_sparse.npz /app/data/train_pivot_sparse.npz
COPY data/train_pivot.csv /app/data/train_pivot.csv
COPY models/fm_model.pkl /app/models/fm_model.pkl
COPY templates/ /app/templates/
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV MODEL_PATH /app/

# Run app.py when the container launches
CMD ["python", "app.py"]



# # Используем базовый образ с поддержкой Python
# FROM python:3.8

# RUN mkdir /app
# RUN mkdir /app/data
# RUN mkdir /app/models
# RUN mkdir /app/templates

# # Устанавливаем необходимые библиотеки
# COPY requirements.txt /app/requirements.txt
# WORKDIR /app
# # RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Копируем файлы и папки
# COPY app.py /app/
# COPY data/train_pivot_sparse.npz /app/data/train_pivot_sparse.npz
# COPY data/train_pivot.csv /app/data/train_pivot.csv
# COPY models/fm_model.pkl /app/models/fm_model.pkl
# COPY templates/ /app/templates/

# # Запускаем скрипт при старте контейнера
# CMD ["python", "app.py"]