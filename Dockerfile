##********************** MAIN BUILD **********************##
FROM python:3.12-alpine


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Install the service
COPY --from=zricethezav/gitleaks:latest /usr/bin/ /usr/local/bin/


# Install git and its dependencies
RUN apk add --no-cache git


# Configure Git to treat /scan as a safe directory
RUN git config --global --add safe.directory /scan


# Set the working directory in the container
WORKDIR /usr/src/app


# Copy the current directory contents into the container
COPY . .


# Install dependencies and the package
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt && \
    python setup.py install && \
    rm -rf /root/.cache/pip


# Run secret-exposure-analysis when the container launches
ENTRYPOINT ["secret_exposure_analysis"]