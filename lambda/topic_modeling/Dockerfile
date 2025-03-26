# lambda/topic_modeling/Dockerfile
FROM public.ecr.aws/lambda/python:3.9

# Install system dependencies
RUN yum install -y gcc-c++

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY index.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "index.handler" ]
