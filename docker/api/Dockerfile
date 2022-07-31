FROM python:3.7

# Working directory is the project root directory
WORKDIR /usr/src/server

# Add requirements.txt file to the image
ADD requirements.txt .

# Install the dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install zsh and oh-my-zsh
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)"

# Start the API server
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]