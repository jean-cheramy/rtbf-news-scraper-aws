# lambda/topic_modeling/Dockerfile
FROM public.ecr.aws/lambda/python:3.12

# Use microdnf instead of yum
RUN microdnf update -y && \
    microdnf install -y gcc gcc-c++ make && \
    microdnf clean all && \
    rm -rf /var/cache/yum

# Copy requirements file
COPY main.py .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the CMD to your handler
CMD [ "main.handler" ]