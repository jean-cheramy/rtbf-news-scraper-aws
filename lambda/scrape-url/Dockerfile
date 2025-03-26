# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.12

# Copy function code
COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the function
CMD ["main.handler"]
