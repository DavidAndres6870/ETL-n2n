FROM public.ecr.aws/lambda/python:3.11

# Copy requirenmets.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY n2n_functions.py ${LAMBDA_TASK_ROOT}

# Set the CMD  to your handler (could also be done as parameter override outside of the Dokerfile)
CMD [ "lambda_function.lambda_handler" ]