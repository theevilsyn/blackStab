FROM python:3.8

# Create checker directory
RUN mkdir /checker
WORKDIR /checker
ENV HOME /checker

# Add Python dependencies
COPY requirements.txt /tmp/
RUN python -m pip install --upgrade pip
RUN pip install --requirement /tmp/requirements.txt

# Set Python stream unbuffered
ENV PYTHONUNBUFFERED TRUE
ENV PWNLIB_NOTERM=true

# Set up protobuf
COPY proto /checker/proto/
COPY checker.py
COPY admin_client /checker/admin_client
COPY cloud_client /checker/cloud_client
RUN python -m grpc_tools.protoc -I /app/proto --python_out=. --grpc_python_out=. checker.proto
ENTRYPOINT ["python","/app/server.py"]
